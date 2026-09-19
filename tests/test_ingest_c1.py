"""C1 ingest: same retrieve script, producer tables, LineageRecord."""

from __future__ import annotations

import csv
import io
import os
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from prism.catalog import default_catalog
from prism.ingest import PARSER, ingest_c1
from prism.ingest.parse import (
    parse_cpi_back_series,
    parse_cpi_cfpi,
    parse_cpi_division_group,
    parse_cpi_general,
)
from prism.ingest.retrieve import IngestError
from prism.refresh import (
    CITE_C1_CARD_1,
    CITE_C1_CARD_2,
    CITE_C1_CARD_3,
    CITE_C1_CARD_4,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import LineageRecord, SourceChanged, YesNo
from tests.cpi_xlsx_fixtures import (
    annex_workbook_bytes,
    back_series_bytes,
    monthly_workbook_bytes,
)

_C1 = default_catalog()
MONTHLY_URL = _C1.artifact("mospi-cpi-monthly-2026-08").url
ANNEX_URL = _C1.artifact("mospi-cpi-monthly-2026-08").companions[0].url
BACK_SERIES_URL = _C1.artifact("mospi-cpi-back-series").url
XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
FIRST_AT = datetime(2026, 9, 16, 8, 0, 0, tzinfo=UTC)
SECOND_AT = datetime(2026, 9, 16, 9, 0, 0, tzinfo=UTC)
MONTHLY_FILENAME = "1789491098345-Data_August_CPI_2026_14092026.xlsx"


def _client(
    *,
    monthly: bytes | None = None,
    annex: bytes | None = None,
    back: bytes | None = None,
    monthly_status: int = 200,
    annex_status: int = 200,
    back_status: int = 200,
) -> httpx.Client:
    monthly_bytes = monthly if monthly is not None else monthly_workbook_bytes()
    annex_bytes = annex if annex is not None else annex_workbook_bytes()
    back_bytes = back if back is not None else back_series_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        headers = {"content-type": XLSX_TYPE}
        if url == MONTHLY_URL:
            body = monthly_bytes if monthly_status == 200 else b"not-found"
            return httpx.Response(monthly_status, content=body, headers=headers)
        if url == ANNEX_URL:
            body = annex_bytes if annex_status == 200 else b"not-found"
            return httpx.Response(annex_status, content=body, headers=headers)
        if url == BACK_SERIES_URL:
            body = back_bytes if back_status == 200 else b"not-found"
            return httpx.Response(back_status, content=body, headers=headers)
        return httpx.Response(404, content=b"unexpected-url")

    return httpx.Client(transport=httpx.MockTransport(handler))


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def test_parser_version_is_stable() -> None:
    assert PARSER == "mospi-cpi-xlsx-1.0.0"


def test_general_keeps_sectors_and_omits_chandigarh_rural() -> None:
    parsed = parse_cpi_general(monthly_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert {row["Sector"] for row in rows} == {"Rural", "Urban", "Combined"}
    chandigarh = [row for row in rows if row["State Name"] == "Chandigarh"]
    assert {row["Sector"] for row in chandigarh} == {"Urban", "Combined"}
    dash = [
        row
        for row in rows
        if row["State Name"] == "Jammu And Kashmir" and row["Sector"] == "Rural"
    ]
    assert dash[0]["inflation (%)"] == ""
    assert "Chandigarh Rural" in parsed.nulls


def test_cfpi_is_group_food_only() -> None:
    parsed = parse_cpi_cfpi(monthly_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert {row["Group code"] for row in rows} == {"01.1"}
    assert {row["Group Name"] for row in rows} == {"Food"}
    assert "Division" not in parsed.csv_text.splitlines()[0]


def test_division_group_does_not_use_item_sheet() -> None:
    parsed = parse_cpi_division_group(monthly_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    assert parsed.row_count == 7
    assert "should-not-appear" not in parsed.csv_text
    rows = _rows(parsed.csv_text)
    names = {row["Division Name"] for row in rows if row["Division Name"]}
    assert "Food and beverages" in names
    assert {row["Group Name"] for row in rows if row["Group Name"]} == {
        "Food",
        "Beverages",
    }


def test_back_series_all_india_blank_inflation_null() -> None:
    parsed = parse_cpi_back_series(back_series_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert {row["State name"] for row in rows} == {"All India"}
    assert {row["State code"] for row in rows} == {"00"}
    blanks = [row for row in rows if row["Year"] == "2013"]
    assert all(row["Inflation (%)"] == "" for row in blanks)
    filled = [row for row in rows if row["Year"] == "2014"]
    assert filled[0]["Inflation (%)"] == "9.29"


def test_second_retrieve_same_script_new_stamp_same_checksum(tmp_path: Path) -> None:
    monthly = monthly_workbook_bytes()
    annex = annex_workbook_bytes()
    back = back_series_bytes()
    first = ingest_c1(
        tmp_path,
        client=_client(monthly=monthly, annex=annex, back=back),
        retrieved_at=FIRST_AT,
    )
    second = ingest_c1(
        tmp_path,
        client=_client(monthly=monthly, annex=annex, back=back),
        retrieved_at=SECOND_AT,
    )
    assert len(first) == 4
    assert all(
        record.source_changed is SourceChanged.first_retrieve for record in first
    )
    assert all(record.lineage_ok is YesNo.yes for record in first)
    assert all(record.lineage_ok is YesNo.yes for record in second)
    assert all(record.source_changed is SourceChanged.no for record in second)
    assert {record.retrieved_at for record in first} == {"20260916T080000Z"}
    assert {record.retrieved_at for record in second} == {"20260916T090000Z"}
    assert [record.checksum for record in first] == [
        record.checksum for record in second
    ]
    assert first[0].checksum == first[1].checksum == first[2].checksum
    assert first[3].checksum != first[0].checksum
    general_raw = (
        tmp_path
        / "raw"
        / "mospi"
        / SERIES_CPI_GENERAL_BASE_2024
        / "2026-08"
        / "20260916T080000Z"
        / MONTHLY_FILENAME
    )
    cfpi_raw = (
        tmp_path
        / "raw"
        / "mospi"
        / SERIES_CPI_CFPI_BASE_2024
        / "2026-08"
        / "20260916T080000Z"
        / MONTHLY_FILENAME
    )
    assert os.path.samefile(general_raw, cfpi_raw)
    lineage_path = (
        tmp_path
        / "lineage"
        / "mospi"
        / SERIES_CPI_GENERAL_BASE_2024
        / "2026-08"
        / "lineage.json"
    )
    on_disk = LineageRecord.model_validate_json(lineage_path.read_bytes())
    assert on_disk.source_changed is SourceChanged.no
    assert on_disk.parser == PARSER
    assert on_disk.citation_id == CITE_C1_CARD_1
    assert not (tmp_path / "vintages").exists()
    assert not (tmp_path / "pointers").exists()
    second_raw = (
        tmp_path
        / "raw"
        / "mospi"
        / SERIES_CPI_GENERAL_BASE_2024
        / "2026-08"
        / "20260916T090000Z"
        / MONTHLY_FILENAME
    )
    assert second_raw.exists()
    assert general_raw.exists()


def test_lineage_binds_citation_ids(tmp_path: Path) -> None:
    records = ingest_c1(tmp_path, client=_client(), retrieved_at=FIRST_AT)
    assert [record.citation_id for record in records] == [
        CITE_C1_CARD_1,
        CITE_C1_CARD_2,
        CITE_C1_CARD_3,
        CITE_C1_CARD_4,
    ]
    derived = tmp_path.parent / records[0].derived_path
    text = derived.read_text(encoding="utf-8")
    assert "Annexure" not in text.splitlines()[0]
    assert "should-not-appear" not in text


def test_http_404_stops_without_substitution(tmp_path: Path) -> None:
    records = ingest_c1(
        tmp_path,
        client=_client(monthly_status=404),
        retrieved_at=FIRST_AT,
        series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    assert len(records) == 1
    assert records[0].lineage_ok is YesNo.no
    assert "http_404" in records[0].flags
    table = (
        tmp_path
        / "derived"
        / "mospi"
        / SERIES_CPI_GENERAL_BASE_2024
        / "2026-08"
        / "table.csv"
    )
    assert not table.exists()


def test_unknown_series_fails_fast(tmp_path: Path) -> None:
    with pytest.raises(IngestError, match="unknown series_id"):
        ingest_c1(tmp_path, client=_client(), series_ids=("not-a-c1-series",))
