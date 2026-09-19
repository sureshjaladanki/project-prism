"""Atomic citizen and preview pointers. Preview is not an alias of citizen."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from prism.paths import (
    citizen_pointer_path,
    pointers_dir,
    preview_pointer_path,
    render_complete_path,
    vintage_dir,
)
from prism.refresh import VINTAGE_ID_PATTERN
from prism.schema import Completeness, VintageManifest
from prism.vintage_store import load_manifest


class PublishError(ValueError):
    pass


def _lock_dir(data_root: Path) -> Path:
    return pointers_dir(data_root) / ".publish.lock"


def _acquire_publish_lock(data_root: Path) -> Path:
    pointers_dir(data_root).mkdir(parents=True, exist_ok=True)
    lock = _lock_dir(data_root)
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise PublishError("another publish is in progress") from exc
    return lock


def _write_pointer_atomic(path: Path, vintage_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(vintage_id + "\n")
        os.replace(tmp_name, path)
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def _read_pointer(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return None
    return text


def read_citizen_pointer(data_root: Path) -> str | None:
    return _read_pointer(citizen_pointer_path(data_root))


def read_preview_pointer(data_root: Path) -> str | None:
    return _read_pointer(preview_pointer_path(data_root))


def _assert_distinct_pointer_files(data_root: Path) -> None:
    citizen = citizen_pointer_path(data_root)
    preview = preview_pointer_path(data_root)
    if citizen == preview:
        raise PublishError("preview must not be the citizen pointer path")
    if citizen.exists() and preview.exists() and os.path.samefile(citizen, preview):
        raise PublishError("preview must not be an alias of citizen")


def _require_publishable(
    data_root: Path, vintage_id: str, *, render_complete: bool
) -> VintageManifest:
    if VINTAGE_ID_PATTERN.fullmatch(vintage_id) is None:
        raise PublishError(f"invalid vintage_id: {vintage_id}")
    if not vintage_dir(data_root, vintage_id).exists():
        raise PublishError(f"vintage {vintage_id} does not exist")
    manifest = load_manifest(data_root, vintage_id)
    if manifest.completeness is Completeness.failed:
        raise PublishError("a failed vintage is never the citizen or preview pointer")
    if not render_complete or not render_complete_path(data_root, vintage_id).exists():
        raise PublishError("render is not complete; pointer will not move")
    return manifest


def publish_preview(data_root: Path, vintage_id: str, *, render_complete: bool) -> None:
    lock = _acquire_publish_lock(data_root)
    try:
        _require_publishable(data_root, vintage_id, render_complete=render_complete)
        _write_pointer_atomic(preview_pointer_path(data_root), vintage_id)
        _assert_distinct_pointer_files(data_root)
    finally:
        lock.rmdir()


def publish_citizen(
    data_root: Path,
    vintage_id: str,
    *,
    render_complete: bool,
    contract_tests_passed: bool,
) -> None:
    previous = read_citizen_pointer(data_root)
    lock = _acquire_publish_lock(data_root)
    try:
        if not contract_tests_passed:
            raise PublishError(
                "contract tests have not passed; citizen pointer will not move"
            )
        _require_publishable(data_root, vintage_id, render_complete=render_complete)
        _write_pointer_atomic(citizen_pointer_path(data_root), vintage_id)
        _assert_distinct_pointer_files(data_root)
    except Exception:
        current = read_citizen_pointer(data_root)
        if current != previous and previous is not None:
            _write_pointer_atomic(citizen_pointer_path(data_root), previous)
        raise
    finally:
        if lock.exists():
            lock.rmdir()
