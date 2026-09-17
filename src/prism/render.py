"""Render template + one vintage to a complete static tree. Preview is not citizen."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from prism.paths import (
    RENDER_COMPLETE_MARKER,
    render_complete_path,
    render_dir,
    renders_dir,
)
from prism.pointer_store import publish_preview, read_citizen_pointer
from prism.template_bind import (
    BoundPage,
    RenderError,
    assert_single_vintage,
    bind_c1_page,
    write_contract_schema,
)

REQUIRED_PAGES = ("index.html",)
BOUND_DIRNAME = ".bound"


class RenderIncompleteError(RenderError):
    pass


def render_c1(
    data_root: Path,
    vintage_id: str,
    cms_root: Path,
    *,
    set_preview: bool = False,
) -> Path:
    page = bind_c1_page(data_root, vintage_id, cms_root)
    assert_single_vintage(page, vintage_id)
    dest = _write_render_tree(data_root, vintage_id, cms_root, page)
    if set_preview:
        if read_citizen_pointer(data_root) == vintage_id:
            raise RenderError("refusing to set preview as an alias of citizen in this pass")
        publish_preview(data_root, vintage_id, render_complete=True)
    return dest


def _write_render_tree(data_root: Path, vintage_id: str, cms_root: Path, page: BoundPage) -> Path:
    dest = render_dir(data_root, vintage_id)
    parent = renders_dir(data_root)
    parent.mkdir(parents=True, exist_ok=True)
    tmp = parent / f".tmp-{vintage_id}"
    old = parent / f".old-{vintage_id}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    bound_dir = cms_root / BOUND_DIRNAME
    if bound_dir.exists():
        shutil.rmtree(bound_dir)
    bound_dir.mkdir()
    _write_bound_inputs(bound_dir, page)
    write_contract_schema(cms_root / "generated" / "contract-schema.json")
    try:
        _run_astro_build(cms_root, tmp, bound_dir)
        _write_chart_specs(tmp, page)
        _drop_astro_internals(tmp)
        _mark_complete(tmp)
        if dest.exists():
            if old.exists():
                shutil.rmtree(old)
            dest.rename(old)
        tmp.rename(dest)
        if old.exists():
            shutil.rmtree(old)
    except Exception:
        if tmp.exists():
            shutil.rmtree(tmp)
        raise
    finally:
        if bound_dir.exists():
            shutil.rmtree(bound_dir)
    if not render_complete_path(data_root, vintage_id).exists():
        raise RenderIncompleteError("render did not write COMPLETE")
    return dest


def _write_bound_inputs(bound_dir: Path, page: BoundPage) -> None:
    (bound_dir / "body.html").write_text(page.body_html, encoding="utf-8", newline="\n")
    payload = {
        "template_id": page.template_id,
        "vintage_id": page.vintage_id,
        "charts": page.charts,
    }
    (bound_dir / "bound.json").write_bytes(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")


def _write_chart_specs(dest: Path, page: BoundPage) -> None:
    charts_dir = dest / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    for chart_id, spec in page.charts.items():
        path = charts_dir / f"{chart_id}.vl.json"
        path.write_text(
            json.dumps(spec, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def _drop_astro_internals(dest: Path) -> None:
    for path in dest.iterdir():
        if path.suffix == ".mjs" or path.name.startswith("manifest_"):
            path.unlink()


def _mark_complete(dest: Path) -> None:
    missing = [name for name in REQUIRED_PAGES if not (dest / name).exists()]
    if missing:
        raise RenderIncompleteError(
            "required template failed to render: " + ", ".join(missing)
        )
    (dest / RENDER_COMPLETE_MARKER).write_text("ok\n", encoding="utf-8", newline="\n")


def _run_astro_build(cms_root: Path, out_dir: Path, bound_dir: Path) -> None:
    npm = shutil.which("npm")
    if npm is None:
        raise RenderError("npm is required to build the Astro tree")
    env = os.environ.copy()
    env["PRISM_RENDER_OUT"] = str(out_dir.resolve())
    env["PRISM_BOUND_DIR"] = str(bound_dir.resolve())
    env["ASTRO_TELEMETRY_DISABLED"] = "1"
    if not (cms_root / "node_modules" / "astro").exists():
        subprocess.run([npm, "install"], cwd=cms_root, env=env, check=True)
    try:
        subprocess.run([npm, "run", "build"], cwd=cms_root, env=env, check=True)
    except subprocess.CalledProcessError as exc:
        raise RenderError(f"Astro build failed with exit {exc.returncode}") from exc
