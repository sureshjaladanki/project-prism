"""Ingest accuracy gate: raw fixture bytes must equal hand-verified derived CSV.

No network. No new persona. Each producer file shape under tests/fixtures/ingest/
carries raw + expected.csv. A corrupt raw fails. A hole in the raw stays empty,
never a fabricated zero.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Callable
from pathlib import Path

import pytest

from prism.ingest.budget_cga_xlsx_pdf_html import (
    parse_cga_monthly_html,
    parse_receipt_xlsx,
)
from prism.ingest.census_srs_xlsx_pdf import (
    parse_census_2011_a02_xls,
    parse_census_2011_pca_sd,
    parse_srs_bulletin_2024,
)
from prism.ingest.parsed_table import ParsedTable
from prism.ingest.xlsx_cpi_period import parse_cpi_general
from prism.schema import YesNo

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "ingest"

_SHAPES: tuple[tuple[str, str, Callable[[bytes], ParsedTable]], ...] = (
    ("xlsx_cpi_period", "raw.xlsx", parse_cpi_general),
    ("xlsx_census_pca", "raw.xlsx", parse_census_2011_pca_sd),
    ("xls_census_a02", "raw.xls", parse_census_2011_a02_xls),
    ("pdf_srs_bulletin", "raw.pdf", parse_srs_bulletin_2024),
    ("xlsx_budget_receipt", "raw.xlsx", parse_receipt_xlsx),
    ("html_cga_monthly", "raw.html", parse_cga_monthly_html),
)


def _shape_dir(name: str) -> Path:
    path = _FIXTURES / name
    assert path.is_dir(), f"missing fixture shape: {path}"
    return path


@pytest.mark.parametrize(("shape", "raw_name", "parse"), _SHAPES, ids=[s[0] for s in _SHAPES])
def test_ingest_accuracy_gate_matches_expected(
    shape: str,
    raw_name: str,
    parse: Callable[[bytes], ParsedTable],
) -> None:
    folder = _shape_dir(shape)
    raw = (folder / raw_name).read_bytes()
    expected = (folder / "expected.csv").read_text(encoding="utf-8")
    parsed = parse(raw)
    assert parsed.lineage_ok is YesNo.yes, parsed.flags
    assert parsed.csv_text == expected


@pytest.mark.parametrize(("shape", "raw_name", "parse"), _SHAPES, ids=[s[0] for s in _SHAPES])
def test_ingest_accuracy_gate_corrupt_raw_fails(
    shape: str,
    raw_name: str,
    parse: Callable[[bytes], ParsedTable],
) -> None:
    folder = _shape_dir(shape)
    raw = (folder / raw_name).read_bytes()
    corrupt = b"not-a-producer-table\x00" + raw[:32]
    try:
        parsed = parse(corrupt)
    except Exception:  # noqa: BLE001 — openpyxl/zipfile raise on mangled xlsx
        return
    assert parsed.lineage_ok is YesNo.no
    assert parsed.row_count == 0


def test_ingest_accuracy_gate_holes_are_empty_not_zero() -> None:
    """Withheld / blank producer cells stay empty in derived CSV — never '0'."""
    cpi = parse_cpi_general((_shape_dir("xlsx_cpi_period") / "raw.xlsx").read_bytes())
    assert cpi.lineage_ok is YesNo.yes
    rows = list(csv.DictReader(io.StringIO(cpi.csv_text)))
    jk = next(row for row in rows if row["State Name"] == "Jammu And Kashmir")
    assert jk["inflation (%)"] == ""
    assert jk["inflation (%)"] != "0"

    receipt = parse_receipt_xlsx(
        (_shape_dir("xlsx_budget_receipt") / "raw.xlsx").read_bytes()
    )
    assert receipt.lineage_ok is YesNo.yes
    receipt_rows = list(csv.DictReader(io.StringIO(receipt.csv_text)))
    cgst = next(row for row in receipt_rows if row["line_label"] == "CGST")
    cess = next(
        row for row in receipt_rows if row["line_label"] == "GST Compensation Cess"
    )
    assert cgst["budget_2025_2026"] == ""
    assert cgst["budget_2025_2026"] != "0"
    assert cess["budget_2026_2027"] == ""
    assert cess["budget_2026_2027"] != "0"
