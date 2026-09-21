"""C3 ingest: reconstructable Budget/CGA tables; Card 8 stays a named hole."""

from __future__ import annotations

import csv
import io
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from prism.catalog import default_catalog
from prism.ingest.parse_c3 import (
    PARSER,
    parse_cga_monthly_html,
    parse_deficit_statistics_xlsx,
    parse_expenditure_stat1_xlsx,
    parse_frbm_statements_pdf,
    parse_receipt_xlsx,
)
from prism.ingest.run import ingest_c3
from prism.refresh import (
    CITE_C3_CARD_1,
    CITE_C3_CARD_5,
    CITE_C3_CARD_6,
    CITE_C3_CARD_8,
    CITE_C3_CARD_10,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_MONTHLY_GLANCE_2026_07,
)
from prism.schema import SourceChanged, YesNo
from tests.c3_ingest_fixtures import (
    STUB_PDF,
    cga_monthly_html_bytes,
    deficit_statistics_bytes,
    expenditure_stat1_bytes,
    receipt_workbook_bytes,
)

_C3 = default_catalog()
TAX_URL = _C3.artifact("receipt-budget-tr-xlsx").url
NON_TAX_URL = _C3.artifact("receipt-budget-ntr-xlsx").url
CAPITAL_URL = _C3.artifact("receipt-budget-ctr-xlsx").url
ANNEX1_URL = _C3.artifact("receipt-budget-annex1-pdf").url
STAT1_URL = _C3.artifact("expenditure-stat1-xlsx").url
BAG_URL = _C3.artifact("budget-at-a-glance-xlsx").url
LIABILITIES_URL = _C3.artifact("receipt-annex91-pdf").url
FRBM_URL = _C3.artifact("frbm1-pdf").url
AFS_URL = _C3.artifact("allafs-pdf").url
CGA_MONTHLY_URL = _C3.artifact("cga-monthly-html").url
CGA_FA_URL = _C3.artifact("cga-fa-stat1-pdf").url
XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
FIRST_AT = datetime(2026, 9, 18, 8, 0, 0, tzinfo=UTC)
PRODUCER_PROBE = Path("data/_c3_probe")


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def _client() -> httpx.Client:
    receipt = receipt_workbook_bytes()
    stat1 = expenditure_stat1_bytes()
    bag = deficit_statistics_bytes()
    html = cga_monthly_html_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url in {TAX_URL, NON_TAX_URL, CAPITAL_URL}:
            return httpx.Response(
                200, content=receipt, headers={"content-type": XLSX_TYPE}
            )
        if url == STAT1_URL:
            return httpx.Response(
                200, content=stat1, headers={"content-type": XLSX_TYPE}
            )
        if url == BAG_URL:
            return httpx.Response(200, content=bag, headers={"content-type": XLSX_TYPE})
        if url == CGA_MONTHLY_URL:
            return httpx.Response(
                200, content=html, headers={"content-type": "text/html"}
            )
        if url in {ANNEX1_URL, LIABILITIES_URL, FRBM_URL, AFS_URL, CGA_FA_URL}:
            return httpx.Response(
                200, content=STUB_PDF, headers={"content-type": "application/pdf"}
            )
        return httpx.Response(404, content=b"unexpected-url")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parser_version_is_stable() -> None:
    assert PARSER == "union-c3-1.2.0"


def test_receipt_xlsx_maps_year_columns() -> None:
    parsed = parse_receipt_xlsx(receipt_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert rows[0]["line_label"] == "Corporation Tax"
    assert rows[0]["major_head"] == "0020"
    assert rows[0]["actuals_2024_2025"] == "911000"
    assert rows[1]["budget_2025_2026"] == ""
    assert rows[2]["line_label"] == "GST Compensation Cess"
    assert rows[2]["budget_2026_2027"] == ""
    assert "sheet=ReceiptReport123" in parsed.flags


def test_statement1_reads_gapped_be_total_column() -> None:
    parsed = parse_expenditure_stat1_xlsx(expenditure_stat1_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert "Central Expenditure" in rows[0]["line_label"]
    assert rows[0]["actuals_2024_2025_total"] == "3"
    assert rows[0]["budget_2026_2027_total"] == "13"
    assert rows[0]["budget_2026_2027_capital"] == "11"


def test_deficit_sheet_not_other_bag_sheets() -> None:
    parsed = parse_deficit_statistics_xlsx(deficit_statistics_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert "Fiscal Deficit" in rows[0]["line_label"]
    assert rows[0]["actuals_2024_2025"] == "1574431"
    assert "should-not-appear" not in parsed.csv_text
    assert "sheet=Deficit Statistics" in parsed.flags


def test_cga_monthly_html_expands_seven_columns() -> None:
    parsed = parse_cga_monthly_html(cga_monthly_html_bytes())
    assert parsed.lineage_ok is YesNo.yes
    rows = _rows(parsed.csv_text)
    assert rows[0]["line_label"] == "Revenue Receipts"
    assert rows[0]["be_2026_2027"] == "3533150"
    assert "colspan/rowspan expanded" in parsed.flags


def test_frbm_pdf_is_named_hole() -> None:
    parsed = parse_frbm_statements_pdf(STUB_PDF)
    assert parsed.lineage_ok is YesNo.no
    assert "not a reconstructable" in parsed.flags
    assert "page 9" in parsed.flags


def test_ingest_c3_lands_xlsx_and_html_card_8_stays_hole(tmp_path: Path) -> None:
    records = ingest_c3(tmp_path, client=_client(), retrieved_at=FIRST_AT)
    assert len(records) == 11
    by_cite = {record.citation_id: record for record in records}
    tax = by_cite[CITE_C3_CARD_1]
    assert tax.lineage_ok is YesNo.yes
    assert tax.source_changed is SourceChanged.first_retrieve
    assert tax.parser == PARSER
    assert (
        tmp_path
        / "derived"
        / "mof-budget"
        / SERIES_BUDGET_2026_27_TAX_REVENUE
        / "2026-27"
        / "table.csv"
    ).is_file()
    assert by_cite[CITE_C3_CARD_5].lineage_ok is YesNo.yes
    assert by_cite[CITE_C3_CARD_6].lineage_ok is YesNo.yes
    assert by_cite[CITE_C3_CARD_10].lineage_ok is YesNo.yes
    hole = by_cite[CITE_C3_CARD_8]
    assert hole.lineage_ok is YesNo.no
    assert "not a reconstructable" in hole.flags
    raw_tax = (
        tmp_path / "raw" / "mof-budget" / SERIES_BUDGET_2026_27_TAX_REVENUE / "2026-27"
    )
    assert any(raw_tax.rglob("tr.xlsx"))
    raw_html = tmp_path / "raw" / "cga" / SERIES_CGA_MONTHLY_GLANCE_2026_07 / "2026-07"
    assert any(raw_html.rglob("DATA2627.htm"))
    raw_frbm = (
        tmp_path
        / "raw"
        / "mof-budget"
        / SERIES_BUDGET_2026_27_FRBM_STATEMENTS
        / "2026-27"
    )
    assert any(raw_frbm.rglob("frbm1.pdf"))
    assert not (
        tmp_path
        / "derived"
        / "mof-budget"
        / SERIES_BUDGET_2026_27_FRBM_STATEMENTS
        / "2026-27"
        / "table.csv"
    ).is_file()
    assert not (tmp_path / "vintages").exists()
    assert by_cite[CITE_C3_CARD_5].citation_id
    assert (
        tmp_path
        / "derived"
        / "mof-budget"
        / SERIES_BUDGET_2026_27_EXPENDITURE_STAT1
        / "2026-27"
        / "table.csv"
    ).is_file()


def test_producer_stat1_and_deficit_if_present() -> None:
    stat1 = PRODUCER_PROBE / SERIES_BUDGET_2026_27_EXPENDITURE_STAT1
    bag = PRODUCER_PROBE / "budget-2026-27-deficit-statistics"
    if not stat1.is_file() or not bag.is_file():
        pytest.skip("producer C3 xlsx not in data/_c3_probe")
    parsed_stat1 = parse_expenditure_stat1_xlsx(stat1.read_bytes())
    assert parsed_stat1.lineage_ok is YesNo.yes
    assert parsed_stat1.row_count >= 10
    rows = _rows(parsed_stat1.csv_text)
    assert any("Central Expenditure" in row["line_label"] for row in rows)
    parsed_bag = parse_deficit_statistics_xlsx(bag.read_bytes())
    assert parsed_bag.lineage_ok is YesNo.yes
    labels = {row["line_label"] for row in _rows(parsed_bag.csv_text)}
    assert any("Fiscal Deficit" in label for label in labels)
