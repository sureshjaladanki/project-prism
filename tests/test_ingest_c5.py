"""C5 ingest: RBI SF xlsx tidy when structure is clear; WAF/CAG stop cleanly."""

from __future__ import annotations

import csv
import io

from prism.ingest.rbi_cag_state_finance import (
    PARSER,
    parse_cag_cfra_glance_pdf,
    parse_rbi_sf_xlsx,
)
from prism.schema import YesNo
from tests.c5_ingest_fixtures import rbi_sf_geo_rows_workbook_bytes, rbi_sf_waf_html_bytes


def test_rbi_sf_geo_rows_parses() -> None:
    parsed = parse_rbi_sf_xlsx(rbi_sf_geo_rows_workbook_bytes())
    assert parsed.lineage_ok is YesNo.yes
    assert parsed.row_count == 8
    assert PARSER in ("rbi-cag-c5-1.0.0", PARSER)
    rows = list(csv.DictReader(io.StringIO(parsed.csv_text)))
    assert rows[0]["geography"] == "Andhra Pradesh"
    assert rows[0]["accounts_2023_24"] == "1000"
    assert rows[0]["re_2024_25"] == "1100"
    assert rows[0]["be_2025_26"] == "1200"


def test_rbi_sf_waf_html_fails_cleanly() -> None:
    parsed = parse_rbi_sf_xlsx(rbi_sf_waf_html_bytes())
    assert parsed.lineage_ok is YesNo.no
    assert "waf" in parsed.flags.lower()


def test_cag_glance_stops_without_guessing() -> None:
    # Minimal PDF with no usable state table.
    stub = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
    parsed = parse_cag_cfra_glance_pdf(stub)
    assert parsed.lineage_ok is YesNo.no
