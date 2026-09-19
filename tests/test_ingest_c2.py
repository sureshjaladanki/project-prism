"""C2 ingest: PCA and A-02 tables of record; PDF artifacts stop without guessing."""

from __future__ import annotations

import csv
import io
import os
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from prism.ingest.c2 import (
    A02_XLS_URL,
    NCP_TABLE8_URL,
    PCA_URL,
    SRS_BULLETIN_URL,
    SRS_STAT_URL,
    ingest_c2,
)
from prism.ingest.parse_c2 import (
    PARSER,
    parse_census_2011_a02_xls,
    parse_census_2011_pca_sd,
    parse_ncp_projections_table8,
    parse_srs_bulletin_2024,
    parse_srs_statistical_report_2024,
)
from prism.refresh import (
    CITE_C2_CARD_1,
    CITE_C2_CARD_2,
    CITE_C2_CARD_5,
    SERIES_CENSUS_2011_A02_DECADAL,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
)
from prism.schema import SourceChanged, YesNo
from tests.c2_ingest_fixtures import (
    a02_workbook_bytes,
    bulletin_table1_pdf_bytes,
    ole_xls_bytes,
    pca_workbook_bytes,
    scanned_projection_pdf_bytes,
    table3_fertility_pdf_bytes,
    table8_projection_pdf_bytes,
)

XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
FIRST_AT = datetime(2026, 9, 18, 8, 0, 0, tzinfo=UTC)


def _client() -> httpx.Client:
    pca = pca_workbook_bytes()
    xls = a02_workbook_bytes()
    pdf = scanned_projection_pdf_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == PCA_URL:
            return httpx.Response(200, content=pca, headers={"content-type": XLSX_TYPE})
        if url == A02_XLS_URL:
            return httpx.Response(
                200, content=xls, headers={"content-type": "application/vnd.ms-excel"}
            )
        if url in {SRS_BULLETIN_URL, SRS_STAT_URL, NCP_TABLE8_URL}:
            return httpx.Response(200, content=pdf, headers={"content-type": "application/pdf"})
        return httpx.Response(404, content=b"unexpected-url")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parser_version_is_stable() -> None:
    assert PARSER == "orgi-c2-1.2.0"


def test_pca_keeps_india_and_state_drops_district() -> None:
    parsed = parse_census_2011_pca_sd(pca_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert len(rows) == 4
    assert {row["Level"] for row in rows} == {"India", "STATE"}
    assert "SHOULD NOT APPEAR" not in {row["Name"] for row in rows}
    assert "parked_district_rows=1" in parsed.flags


def test_a02_reads_ole_cells_and_parks_district() -> None:
    parsed = parse_census_2011_a02_xls(a02_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert [row["name"] for row in rows] == ["INDIA", "", "Arunachal Pradesh *", "Daman & Diu"]
    assert rows[0]["census_year"] == "1901 $"
    assert rows[0]["variation_absolute"] == ""
    assert rows[1]["census_year"] == "2011"
    assert rows[1]["state_code"] == ""
    assert rows[2]["persons"] == ""
    assert rows[3]["census_year"] == "1900"
    assert "SHOULD NOT APPEAR" not in {row["name"] for row in rows}
    assert "parked_district_rows=2" in parsed.flags
    assert "xlrd cells" in parsed.flags
    assert "sheet=A-2" in parsed.flags


def test_unreadable_ole_xls_is_not_ok() -> None:
    parsed = parse_census_2011_a02_xls(ole_xls_bytes())
    assert parsed.lineage_ok is YesNo.no
    assert "not a readable workbook" in parsed.flags
    assert "companion PDF" in parsed.flags


def test_producer_a02_xls_if_present() -> None:
    path = Path(os.environ.get("TEMP", "/tmp")) / "prism-c2-a02-2026-09-18" / "00 A 2-India.xls"
    if not path.is_file():
        pytest.skip("producer A-02 xls not in temp")
    parsed = parse_census_2011_a02_xls(path.read_bytes())
    assert parsed.lineage_ok is YesNo.yes
    assert parsed.row_count == 432
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert rows[0]["name"] == "INDIA"
    assert rows[0]["state_code"] == "00"
    assert rows[-1]["census_year"] == "2011"


def test_bulletin_table1_maps_words_and_stitches_dnh() -> None:
    parsed = parse_srs_bulletin_2024(bulletin_table1_pdf_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert rows[0]["line_label"] == "India"
    assert rows[0]["birth_total"] == "18.3"
    assert rows[1]["line_label"] == "3. Dadra & Nagar Haveli and Daman & Diu"
    assert "pdfplumber words" in parsed.flags


def test_table3_maps_india_tfr() -> None:
    parsed = parse_srs_statistical_report_2024(table3_fertility_pdf_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert rows[0]["geography"] == "India"
    assert rows[0]["line_label"] == "Total Fertility Rate"
    assert rows[0]["total"] == "1.9"
    assert rows[0]["rural"] == "2.1"
    assert rows[0]["urban"] == "1.5"


def test_table8_maps_india_2011_and_drops_page_number() -> None:
    parsed = parse_ncp_projections_table8(table8_projection_pdf_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    india_2011 = [
        row for row in rows if row["geography"] == "INDIA" and row["year"] == "2011"
    ]
    assert len(india_2011) == 1
    assert india_2011[0]["persons"] == "12,10,855"
    assert {row["year"] for row in rows} == {"2011", "2036"}
    assert {row["geography"] for row in rows} == {"INDIA", "PUNJAB", "GOA"}


def test_producer_bulletin_table1_if_present() -> None:
    path = (
        Path(os.environ.get("TEMP", "/tmp"))
        / "prism-c2-pdfs-2026-09-18"
        / "SRS_Bulletin_2024_Vol_59_No_1.pdf"
    )
    if not path.is_file():
        pytest.skip("producer SRS bulletin pdf not in temp")
    parsed = parse_srs_bulletin_2024(path.read_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    by_label = {row["line_label"]: row for row in rows}
    assert by_label["India"]["birth_total"] == "18.3"
    assert by_label["India"]["imr_total"] == "24"
    assert any(
        "Dadra & Nagar Haveli and Daman & Diu" in row["line_label"] for row in rows
    )
    assert by_label["6. Puducherry"]["birth_total"]


def test_producer_table3_if_present() -> None:
    path = (
        Path(os.environ.get("TEMP", "/tmp"))
        / "prism-c2-pdfs-2026-09-18"
        / "SRS_STAT_2024.pdf"
    )
    if not path.is_file():
        pytest.skip("producer SRS statistical report pdf not in temp")
    parsed = parse_srs_statistical_report_2024(path.read_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    india_tfr = [
        row
        for row in rows
        if row["geography"] == "India" and row["line_label"] == "Total Fertility Rate"
    ]
    assert len(india_tfr) == 1
    assert india_tfr[0]["total"] == "1.9"
    geos = {row["geography"] for row in rows}
    assert "Andhra Pradesh" in geos
    assert "West Bengal" in geos
    assert "Himachal Pradesh" in geos


def test_producer_table8_if_present() -> None:
    path = (
        Path(os.environ.get("TEMP", "/tmp"))
        / "prism-c2-pdfs-2026-09-18"
        / "Report_Population_Projection_2019.pdf"
    )
    if not path.is_file():
        pytest.skip("producer NCP projection pdf not in temp")
    parsed = parse_ncp_projections_table8(path.read_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    india_2011 = [
        row for row in rows if row["geography"] == "INDIA" and row["year"] == "2011"
    ]
    assert len(india_2011) == 1
    assert india_2011[0]["persons"] == "12,10,855"
    assert "TELANGANA" in {row["geography"] for row in rows}
    assert "LADAKH*" in {row["geography"] for row in rows}


def test_scanned_table8_is_not_ok() -> None:
    parsed = parse_ncp_projections_table8(scanned_projection_pdf_bytes())
    assert parsed.lineage_ok is YesNo.no
    assert "scanned pages" in parsed.flags


def test_ingest_c2_pca_and_a02_ok_pdfs_stop(tmp_path: Path) -> None:
    records = ingest_c2(tmp_path, client=_client(), retrieved_at=FIRST_AT)
    by_cite = {record.citation_id: record for record in records}
    pca = by_cite[CITE_C2_CARD_1]
    assert pca.lineage_ok is YesNo.yes
    assert pca.source_changed is SourceChanged.first_retrieve
    assert pca.row_count == 4
    table = tmp_path / "derived" / "orgi" / SERIES_CENSUS_2011_PCA_SD / "2011" / "table.csv"
    assert table.is_file()
    a02 = by_cite[CITE_C2_CARD_2]
    assert a02.lineage_ok is YesNo.yes
    assert a02.row_count == 4
    assert a02.parser == PARSER
    a02_table = (
        tmp_path / "derived" / "orgi" / SERIES_CENSUS_2011_A02_DECADAL / "2011" / "table.csv"
    )
    assert a02_table.is_file()
    table8 = by_cite[CITE_C2_CARD_5]
    assert table8.lineage_ok is YesNo.no
    assert table8.citation_id == CITE_C2_CARD_5
    raw_pca = tmp_path / "raw" / "orgi" / SERIES_CENSUS_2011_PCA_SD / "2011"
    assert any(raw_pca.rglob("DDW_PCA0000_2011_Indiastatedist.xlsx"))
    raw_a02 = tmp_path / "raw" / "orgi" / SERIES_CENSUS_2011_A02_DECADAL / "2011"
    assert any(raw_a02.rglob("00 A 2-India.xls"))
    raw_proj = tmp_path / "raw" / "ncp-mohfw" / SERIES_NCP_PROJECTIONS_2011_2036_TABLE8
    assert any(raw_proj.rglob("Report_Population_Projection_2019.pdf"))
