"""Pointer store: atomic write, preview is not citizen, failed desk stays off citizen."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from prism.desk_store import DeskSlice, write_desk
from prism.paths import (
    citizen_pointer_path,
    preview_pointer_path,
    render_complete_path,
    render_dir,
)
from prism.pointer_store import (
    PublishError,
    publish_citizen,
    publish_preview,
    read_citizen_pointer,
    read_preview_pointer,
)
from prism.refresh import C1_SERIES_IDS, SERIES_CPI_GENERAL_BASE_2024
from prism.schema import Completeness, RefreshTrigger
from prism.template_bind import C1_TEMPLATE_ID
from prism.vintage_store import write_vintage
from tests.desk_fixtures import write_complete_c1_desk
from tests.factories import CREATED_AT, make_series_write


def test_preview_is_not_an_alias_of_citizen(tmp_path: Path) -> None:
    desk, _manifest = write_complete_c1_desk(tmp_path, b"PARQUET", CREATED_AT)
    publish_preview(tmp_path, desk.desk_id, render_complete=True)
    assert read_preview_pointer(tmp_path) == desk.desk_id
    assert read_citizen_pointer(tmp_path) is None
    assert citizen_pointer_path(tmp_path) != preview_pointer_path(tmp_path)
    assert not citizen_pointer_path(tmp_path).exists()


def test_failed_desk_cannot_become_citizen_pointer(tmp_path: Path) -> None:
    manifest = write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET"),),
        completeness=Completeness.failed,
        previous=None,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    desk = write_desk(
        tmp_path,
        created_at=CREATED_AT,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=manifest.vintage_id),
        ),
        completeness=Completeness.failed,
    )
    render_dir(tmp_path, desk.desk_id).mkdir(parents=True)
    render_complete_path(tmp_path, desk.desk_id).write_text("ok\n", encoding="utf-8")
    with pytest.raises(PublishError, match="failed desk"):
        publish_citizen(
            tmp_path,
            desk.desk_id,
            render_complete=True,
            contract_tests_passed=True,
        )
    assert read_citizen_pointer(tmp_path) is None


def test_citizen_requires_contract_tests_passed(tmp_path: Path) -> None:
    desk, _manifest = write_complete_c1_desk(tmp_path, b"PARQUET", CREATED_AT)
    with pytest.raises(PublishError, match="contract tests"):
        publish_citizen(
            tmp_path,
            desk.desk_id,
            render_complete=True,
            contract_tests_passed=False,
        )
    assert read_citizen_pointer(tmp_path) is None


def test_complete_vintage_missing_required_c1_series_fails(tmp_path: Path) -> None:
    from prism.vintage_store import VintageStoreError

    with pytest.raises(VintageStoreError, match="missing required series"):
        write_vintage(
            tmp_path,
            created_at=CREATED_AT,
            trigger=RefreshTrigger.on_demand,
            series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET"),),
            completeness=Completeness.complete,
            previous=None,
            required_series_ids=C1_SERIES_IDS,
        )


def test_immutable_vintage_directory_not_overwritten(tmp_path: Path) -> None:
    from prism.vintage_store import VintageStoreError

    write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET"),),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    with pytest.raises(VintageStoreError, match="immutable"):
        write_vintage(
            tmp_path,
            created_at=CREATED_AT,
            trigger=RefreshTrigger.on_demand,
            series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET"),),
            completeness=Completeness.complete,
            previous=None,
            required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
        )


def test_preview_and_citizen_can_name_same_desk_as_separate_files(
    tmp_path: Path,
) -> None:
    later = datetime(2026, 9, 16, 11, 0, tzinfo=UTC)
    desk, _manifest = write_complete_c1_desk(tmp_path, b"PARQUET", later)
    publish_preview(tmp_path, desk.desk_id, render_complete=True)
    publish_citizen(
        tmp_path,
        desk.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    assert read_preview_pointer(tmp_path) == desk.desk_id
    assert read_citizen_pointer(tmp_path) == desk.desk_id
    assert not citizen_pointer_path(tmp_path).samefile(preview_pointer_path(tmp_path))
