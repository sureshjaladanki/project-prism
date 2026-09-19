"""Render a CMS desk. Preview includes unpublished slices; citizen does not."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

from prism.cms_site import (
    allowed_hrefs,
    build_site_catalog,
    dump_site_catalog,
    filter_hottest_rail,
)
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
    bind_pages_for_desk,
    write_contract_schema,
)

SHELL_PAGES = (
    "index.html",
    "404.html",
    "how-this-works/index.html",
    "sources/index.html",
    "people/index.html",
    "work/index.html",
    "money/index.html",
    "prices/index.html",
    "delivery/index.html",
)
REQUIRED_PAGES = SHELL_PAGES + ("prices/retail-prices/index.html",)
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
    return render(data_root, vintage_id, cms_root, set_preview=set_preview)


def render(
    data_root: Path,
    vintage_id: str,
    cms_root: Path,
    *,
    set_preview: bool = False,
    cms_mode: str = "preview",
) -> Path:
    if set_preview:
        cms_mode = "preview"
    pages = bind_pages_for_desk(data_root, cms_root, cms_mode=cms_mode)
    for page in pages:
        assert_single_vintage(page, page.vintage_id)
    dest = _write_render_tree(data_root, vintage_id, cms_root, pages, cms_mode=cms_mode)
    if set_preview:
        if read_citizen_pointer(data_root) == vintage_id:
            raise RenderError(
                "refusing to set preview as an alias of citizen in this pass"
            )
        publish_preview(data_root, vintage_id, render_complete=True)
    return dest


def _write_render_tree(
    data_root: Path,
    vintage_id: str,
    cms_root: Path,
    pages: tuple[BoundPage, ...],
    *,
    cms_mode: str = "preview",
) -> Path:
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
    catalog = build_site_catalog(vintage_id, pages, cms_mode=cms_mode)
    allowed = allowed_hrefs(catalog)
    pages = tuple(
        replace(page, body_html=filter_hottest_rail(page.body_html, allowed))
        for page in pages
    )
    _write_bound_inputs(bound_dir, catalog, pages)
    write_contract_schema(cms_root / "generated" / "contract-schema.json")
    required = SHELL_PAGES + tuple(
        f"{page.path.strip('/')}/index.html" for page in pages
    )
    try:
        _run_astro_build(cms_root, tmp, bound_dir)
        for page in pages:
            _write_chart_specs(tmp, page)
        _drop_astro_internals(tmp)
        _mark_complete(tmp, required)
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


def _write_bound_inputs(
    bound_dir: Path, catalog: dict[str, object], pages: tuple[BoundPage, ...]
) -> None:
    (bound_dir / "site.json").write_bytes(dump_site_catalog(catalog))
    for page in pages:
        slice_dir = bound_dir / "slices" / page.template_id
        slice_dir.mkdir(parents=True)
        (slice_dir / "body.html").write_text(
            page.body_html, encoding="utf-8", newline="\n"
        )
        payload = {
            "template_id": page.template_id,
            "vintage_id": page.vintage_id,
            "charts": page.charts,
        }
        (slice_dir / "bound.json").write_bytes(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode(
                "utf-8"
            )
            + b"\n"
        )


def _write_chart_specs(dest: Path, page: BoundPage) -> None:
    charts_dir = dest / page.path.strip("/") / "charts"
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


def _mark_complete(dest: Path, required: tuple[str, ...] = REQUIRED_PAGES) -> None:
    missing = [name for name in required if not (dest / name).exists()]
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
