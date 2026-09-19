"""Desk + render stamps for pointer tests. Not a second schema."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from prism.desk_store import DeskRecord, DeskSlice, write_desk
from prism.paths import render_complete_path, render_dir
from prism.refresh import SERIES_CPI_GENERAL_BASE_2024
from prism.schema import Completeness, RefreshTrigger, VintageManifest
from prism.template_bind import C1_TEMPLATE_ID
from prism.vintage_store import write_vintage
from tests.factories import make_series_write

C1_SLICE_HTML = "prices/retail-prices/index.html"
C2_SLICE_HTML = "people/population/index.html"


def stamp_render(
    data_root: Path, desk_id: str, pages: tuple[str, ...] = (C1_SLICE_HTML,)
) -> Path:
    dest = render_dir(data_root, desk_id)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text("home\n", encoding="utf-8")
    for rel in pages:
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")
    render_complete_path(data_root, desk_id).write_text("ok\n", encoding="utf-8")
    return dest


def write_complete_c1_desk(
    data_root: Path, payload: bytes, created_at: datetime
) -> tuple[DeskRecord, VintageManifest]:
    manifest = write_vintage(
        data_root,
        created_at=created_at,
        trigger=RefreshTrigger.on_demand,
        series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, payload),),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    desk = write_desk(
        data_root,
        created_at=created_at,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=manifest.vintage_id),
        ),
        completeness=Completeness.complete,
    )
    stamp_render(data_root, desk.desk_id)
    return desk, manifest
