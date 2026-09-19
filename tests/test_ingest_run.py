"""Unified ingest dispatches by series_id; it does not fetch unknown ids."""

from __future__ import annotations

from pathlib import Path

import pytest

from prism.cli import app
from prism.ingest import ingest
from prism.ingest.retrieve import IngestError
from prism.refresh import (
    C1_SERIES_IDS,
    C2_SERIES_IDS,
    C3_SERIES_IDS,
    SERIES_CPI_GENERAL_BASE_2024,
)


def test_ingest_rejects_unknown_series_id(tmp_path: Path) -> None:
    with pytest.raises(IngestError, match="unknown series_id"):
        ingest(tmp_path, series_ids=("not-a-series",))


def test_ingest_rejects_mixed_known_and_unknown(tmp_path: Path) -> None:
    with pytest.raises(IngestError, match="bogus"):
        ingest(
            tmp_path,
            series_ids=(SERIES_CPI_GENERAL_BASE_2024, "bogus"),
        )


def test_cli_has_one_ingest_command() -> None:
    names = {command.name for command in app.registered_commands}
    assert "ingest" in names
    assert "ingest-c2" not in names
    assert "ingest-c3" not in names


def test_slice_ids_are_disjoint() -> None:
    assert set(C1_SERIES_IDS).isdisjoint(C2_SERIES_IDS)
    assert set(C1_SERIES_IDS).isdisjoint(C3_SERIES_IDS)
    assert set(C2_SERIES_IDS).isdisjoint(C3_SERIES_IDS)
