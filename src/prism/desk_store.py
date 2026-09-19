"""Immutable published desks. Pointers name a desk_id, never a vintage_id."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from prism.paths import DESK_FILENAME, desk_dir, desk_path, desks_dir, vintage_dir
from prism.refresh import DESK_ID_PATTERN, desk_id_for, ensure_utc
from prism.schema import Completeness, ContractModel, NonEmptyStr, canonical_json_bytes
from prism.vintage_store import load_manifest


class DeskStoreError(ValueError):
    pass


class DeskSlice(ContractModel):
    template_id: NonEmptyStr
    vintage_id: NonEmptyStr


class DeskInput(ContractModel):
    """Hashed into desk_id. Does not include desk_id."""

    created_at: datetime
    slices: tuple[DeskSlice, ...]
    completeness: Completeness


class DeskRecord(ContractModel):
    desk_id: NonEmptyStr
    created_at: datetime
    slices: tuple[DeskSlice, ...]
    completeness: Completeness


def write_desk(
    data_root: Path,
    *,
    created_at: datetime,
    slices: tuple[DeskSlice, ...],
    completeness: Completeness,
) -> DeskRecord:
    created_at = ensure_utc(created_at)
    if not slices:
        raise DeskStoreError("a desk must list at least one slice")
    templates = [item.template_id for item in slices]
    if len(templates) != len(set(templates)):
        raise DeskStoreError("duplicate template_id on desk")
    for binding in slices:
        if not vintage_dir(data_root, binding.vintage_id).exists():
            raise DeskStoreError(f"vintage {binding.vintage_id} does not exist")
        manifest = load_manifest(data_root, binding.vintage_id)
        if (
            completeness is Completeness.complete
            and manifest.completeness is Completeness.failed
        ):
            raise DeskStoreError(
                f"complete desk cannot list failed vintage {binding.vintage_id}"
            )

    payload = DeskInput(
        created_at=created_at, slices=slices, completeness=completeness
    )
    desk_id = desk_id_for(created_at.date(), payload)
    dest = desk_dir(data_root, desk_id)
    if dest.exists():
        raise DeskStoreError(f"desk {desk_id} is immutable and already exists")

    desks_dir(data_root).mkdir(parents=True, exist_ok=True)
    tmp = desks_dir(data_root) / f".tmp-{desk_id}"
    if tmp.exists():
        raise DeskStoreError(f"stale temp desk directory at {tmp.as_posix()}")
    tmp.mkdir()
    record = DeskRecord(
        desk_id=desk_id,
        created_at=created_at,
        slices=slices,
        completeness=completeness,
    )
    try:
        (tmp / DESK_FILENAME).write_bytes(canonical_json_bytes(record))
        tmp.rename(dest)
    except Exception:
        if tmp.exists():
            shutil.rmtree(tmp)
        raise
    return record


def ensure_desk(
    data_root: Path,
    *,
    created_at: datetime,
    slices: tuple[DeskSlice, ...],
    completeness: Completeness,
) -> DeskRecord:
    created_at = ensure_utc(created_at)
    payload = DeskInput(
        created_at=created_at, slices=slices, completeness=completeness
    )
    desk_id = desk_id_for(created_at.date(), payload)
    dest = desk_dir(data_root, desk_id)
    if dest.exists():
        return load_desk(data_root, desk_id)
    return write_desk(
        data_root,
        created_at=created_at,
        slices=slices,
        completeness=completeness,
    )


def load_desk(data_root: Path, desk_id: str) -> DeskRecord:
    if DESK_ID_PATTERN.fullmatch(desk_id) is None:
        raise DeskStoreError(f"invalid desk_id: {desk_id}")
    return DeskRecord.model_validate_json(desk_path(data_root, desk_id).read_bytes())


def list_desks(data_root: Path) -> tuple[DeskRecord, ...]:
    root = desks_dir(data_root)
    if not root.exists():
        return ()
    records: list[DeskRecord] = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or DESK_ID_PATTERN.fullmatch(path.name) is None:
            continue
        records.append(load_desk(data_root, path.name))
    return tuple(records)


def latest_desk(data_root: Path) -> DeskRecord | None:
    records = list_desks(data_root)
    if not records:
        return None
    return max(records, key=lambda item: item.created_at)


def preview_slices(data_root: Path) -> tuple[DeskSlice, ...]:
    """Latest complete vintage per catalog slice, including unpublished slices."""

    from prism.catalog import default_catalog
    from prism.vintage_store import latest_manifest_with_series

    catalog = default_catalog()
    rows: list[DeskSlice] = []
    for item in catalog.slices:
        series_ids = tuple(entry.series_id for entry in item.series)
        manifest = latest_manifest_with_series(data_root, series_ids)
        if manifest is None or manifest.completeness is Completeness.failed:
            continue
        rows.append(
            DeskSlice(template_id=item.template_id, vintage_id=manifest.vintage_id)
        )
    if not rows:
        raise DeskStoreError("no complete vintage for any catalog slice")
    return tuple(rows)


def slices_from_cli(specs: tuple[str, ...]) -> tuple[DeskSlice, ...]:
    from prism.catalog import CatalogError, default_catalog

    catalog = default_catalog()
    rows: list[DeskSlice] = []
    for spec in specs:
        if "=" not in spec:
            raise DeskStoreError(
                f"invalid --slice {spec!r}; expected slice_id=vintage_id"
            )
        slice_id, vintage_id = spec.split("=", 1)
        try:
            item = catalog.slice(slice_id)
        except CatalogError as exc:
            raise DeskStoreError(f"unknown slice-id {slice_id!r}") from exc
        rows.append(DeskSlice(template_id=item.template_id, vintage_id=vintage_id))
    return tuple(rows)
