"""Desk store: immutable directory, preview slices, C2 does not unpublish C1."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from prism.desk_store import DeskSlice, DeskStoreError, load_desk, write_desk
from prism.paths import render_dir
from prism.pointer_store import PublishError, publish_citizen, read_citizen_pointer
from prism.render import SHELL_PAGES, RenderIncompleteError, _mark_complete
from prism.schema import Completeness, RefreshTrigger
from prism.template_bind import C1_TEMPLATE_ID, C2_TEMPLATE_ID
from prism.vintage_store import write_vintage
from tests.desk_fixtures import (
    C1_SLICE_HTML,
    C2_SLICE_HTML,
    stamp_render,
    write_complete_c1_desk,
)
from tests.factories import CREATED_AT, make_series_write


def test_desk_directory_is_immutable(tmp_path: Path) -> None:
    desk, _manifest = write_complete_c1_desk(tmp_path, b"PARQUET", CREATED_AT)
    with pytest.raises(DeskStoreError, match="immutable"):
        write_desk(
            tmp_path,
            created_at=CREATED_AT,
            slices=desk.slices,
            completeness=Completeness.complete,
        )


def test_desk_adding_c2_does_not_drop_c1(tmp_path: Path) -> None:
    c1_desk, c1 = write_complete_c1_desk(tmp_path, b"PARQUET-C1", CREATED_AT)
    publish_citizen(
        tmp_path,
        c1_desk.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    later = datetime(2026, 9, 19, 12, 0, tzinfo=UTC)
    c2 = write_vintage(
        tmp_path,
        created_at=later,
        trigger=RefreshTrigger.on_demand,
        series=(make_series_write("census-2011-pca-sd", b"PARQUET-C2"),),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=("census-2011-pca-sd",),
    )
    both = write_desk(
        tmp_path,
        created_at=later,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=c1.vintage_id),
            DeskSlice(template_id=C2_TEMPLATE_ID, vintage_id=c2.vintage_id),
        ),
        completeness=Completeness.complete,
    )
    dest = stamp_render(tmp_path, both.desk_id, (C1_SLICE_HTML, C2_SLICE_HTML))
    publish_citizen(
        tmp_path,
        both.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    assert read_citizen_pointer(tmp_path) == both.desk_id
    record = load_desk(tmp_path, both.desk_id)
    assert {item.template_id for item in record.slices} == {
        C1_TEMPLATE_ID,
        C2_TEMPLATE_ID,
    }
    assert (dest / C1_SLICE_HTML).exists()
    assert (dest / C2_SLICE_HTML).exists()
    assert (render_dir(tmp_path, c1_desk.desk_id) / C1_SLICE_HTML).exists()


def test_incomplete_c2_slice_does_not_move_pointer(tmp_path: Path) -> None:
    first_desk, first = write_complete_c1_desk(tmp_path, b"PARQUET-A", CREATED_AT)
    publish_citizen(
        tmp_path,
        first_desk.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    later = datetime(2026, 9, 19, 13, 0, tzinfo=UTC)
    c2 = write_vintage(
        tmp_path,
        created_at=later,
        trigger=RefreshTrigger.on_demand,
        series=(make_series_write("census-2011-pca-sd", b"PARQUET-C2"),),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=("census-2011-pca-sd",),
    )
    both = write_desk(
        tmp_path,
        created_at=later,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=first.vintage_id),
            DeskSlice(template_id=C2_TEMPLATE_ID, vintage_id=c2.vintage_id),
        ),
        completeness=Completeness.complete,
    )
    dest = render_dir(tmp_path, both.desk_id)
    dest.mkdir(parents=True)
    required = SHELL_PAGES + (C1_SLICE_HTML, C2_SLICE_HTML)
    with pytest.raises(RenderIncompleteError, match="required template failed"):
        _mark_complete(dest, required)
    with pytest.raises(PublishError, match="render is not complete"):
        publish_citizen(
            tmp_path,
            both.desk_id,
            render_complete=True,
            contract_tests_passed=True,
        )
    assert read_citizen_pointer(tmp_path) == first_desk.desk_id
