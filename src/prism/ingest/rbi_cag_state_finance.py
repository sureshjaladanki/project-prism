"""Tidy RBI State Finances XLSX and CAG CFRA glance PDF. Stop when cells are ambiguous.

Fetch note: `rbidocs.rbi.org.in` often returns a WAF/bot-challenge HTML page to
automated GET (TLS/WAF). Catalog URLs stay on the RBI listing artifact links; ingest
records lineage_ok=no when magic is not XLSX. Parsers still accept real Study of
Budgets workbook bytes (and test fixtures). CAG glance PDF fetches, but multi-row
fragmented headers are not a unique column map — lineage_ok=no rather than guess.
"""

from __future__ import annotations

import csv
import re
from io import BytesIO, StringIO

import pdfplumber
from openpyxl import load_workbook  # type: ignore[import-untyped]
from pdfplumber.utils.exceptions import PdfminerException

from prism.catalog.registry import ParserSpec, register_parser
from prism.ingest.parsed_table import ParsedTable
from prism.ingest.retrieve import is_pdf, is_xlsx
from prism.schema import YesNo

PARSER_NAME = "rbi-cag-c5"
PARSER_VERSION = "1.0.0"
PARSER = f"{PARSER_NAME}-{PARSER_VERSION}"

FRAME_A_GEOGRAPHIES = (
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Puducherry",
    "All States and UTs",
)
FRAME_A_SET = frozenset(FRAME_A_GEOGRAPHIES)

TIDY_COLUMNS = (
    "geography",
    "line_label",
    "accounts_2023_24",
    "re_2024_25",
    "be_2025_26",
)
VALUE_COLUMNS = TIDY_COLUMNS[2:]

_YEAR_TOKEN = re.compile(r"(20\d{2})\s*[-–—]\s*(\d{2})")
_WITHHELD = frozenset(
    {"-", "–", "—", "..", "...", "…", ".", "n.a.", "na", "n/a", "not available"}
)
_MIN_GEO_ROWS = 5


def _empty_fail(flags: str) -> ParsedTable:
    return ParsedTable(
        csv_text="",
        row_count=0,
        nulls="not parsed",
        flags=flags,
        lineage_ok=YesNo.no,
    )


def _norm(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _cell(value: object) -> str:
    text = _norm(value)
    if text.lower() in _WITHHELD:
        return ""
    return text


def _to_csv(fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _ok(
    fieldnames: tuple[str, ...],
    rows: list[dict[str, str]],
    value_columns: tuple[str, ...],
    flags: str,
) -> ParsedTable:
    nulls = sum(1 for row in rows for column in value_columns if row[column] == "")
    return ParsedTable(
        csv_text=_to_csv(fieldnames, rows),
        row_count=len(rows),
        nulls=f"{nulls} empty value cells" if nulls else "none",
        flags=flags,
        lineage_ok=YesNo.yes,
    )


def _year_status_column(header: str) -> str | None:
    """Map a printed header to accounts_2023_24 / re_2024_25 / be_2025_26 when clear."""

    collapsed = header.lower().replace("–", "-").replace("—", "-")
    match = _YEAR_TOKEN.search(header)
    if match is None:
        return None
    start, end = match.group(1), match.group(2)
    year_key = f"{start}_{end}"
    if "account" in collapsed or re.search(r"\bA\b", header):
        if year_key == "2023_24":
            return "accounts_2023_24"
    if "revised" in collapsed or re.search(r"\bRE\b", header):
        if year_key == "2024_25":
            return "re_2024_25"
    if "budget" in collapsed or re.search(r"\bBE\b", header):
        if year_key == "2025_26":
            return "be_2025_26"
    # Bare year columns only when the Study trio is unambiguous by year alone.
    if year_key == "2023_24" and "2024" not in collapsed and "2025" not in collapsed:
        return "accounts_2023_24"
    if year_key == "2024_25":
        return "re_2024_25"
    if year_key == "2025_26":
        return "be_2025_26"
    return None


def _grid_from_sheet(rows: list[tuple[object, ...]]) -> list[list[str]]:
    return [[_cell(cell) for cell in row] for row in rows]


def _find_geo_row_table(
    grid: list[list[str]],
) -> tuple[int, dict[int, str], list[dict[str, str]]] | None:
    """Geography in column 0; Accounts/RE/BE (or clear year) columns across."""

    for header_index, header in enumerate(grid):
        if len(header) < 3:
            continue
        column_map: dict[int, str] = {}
        for index, cell in enumerate(header[1:], start=1):
            mapped = _year_status_column(cell)
            if mapped is None:
                continue
            if mapped in column_map.values():
                return None
            column_map[index] = mapped
        if len(column_map) < 1:
            continue
        if not set(VALUE_COLUMNS).issuperset(column_map.values()):
            # Extra mapped years outside the locked trio — stop rather than invent.
            if not set(column_map.values()).issubset(VALUE_COLUMNS):
                continue
        out: list[dict[str, str]] = []
        for raw in grid[header_index + 1 :]:
            if not raw:
                continue
            geography = raw[0]
            if geography not in FRAME_A_SET:
                continue
            record = {
                "geography": geography,
                "line_label": "as published",
                "accounts_2023_24": "",
                "re_2024_25": "",
                "be_2025_26": "",
            }
            for index, column in column_map.items():
                record[column] = raw[index] if index < len(raw) else ""
            if not any(record[column] for column in VALUE_COLUMNS):
                continue
            out.append(record)
        if len(out) >= _MIN_GEO_ROWS:
            return header_index, column_map, out
    return None


def _find_geo_column_table(
    grid: list[list[str]],
) -> tuple[int, list[dict[str, str]]] | None:
    """Indicators in column 0; Frame A geographies across columns; one year-status sheet."""

    for header_index, header in enumerate(grid):
        geo_at: dict[int, str] = {}
        for index, cell in enumerate(header):
            if cell in FRAME_A_SET:
                geo_at[index] = cell
        if len(geo_at) < _MIN_GEO_ROWS:
            continue
        # Require a year/status cue on this or the prior row.
        cue_rows = grid[max(0, header_index - 2) : header_index + 1]
        cue = " ".join(cell for row in cue_rows for cell in row)
        status_column = _year_status_column(cue)
        if status_column is None:
            # Single-vintage sheet labelled only in the title block.
            lower = cue.lower()
            if "2023-24" in lower.replace("–", "-") and "account" in lower:
                status_column = "accounts_2023_24"
            elif "2024-25" in lower.replace("–", "-") and (
                "revised" in lower or " re" in lower
            ):
                status_column = "re_2024_25"
            elif "2025-26" in lower.replace("–", "-") and (
                "budget" in lower or " be" in lower
            ):
                status_column = "be_2025_26"
            else:
                continue
        out: list[dict[str, str]] = []
        for raw in grid[header_index + 1 :]:
            if not raw:
                continue
            label = raw[0]
            if label == "" or label in FRAME_A_SET:
                continue
            for index, geography in geo_at.items():
                value = raw[index] if index < len(raw) else ""
                if value == "":
                    continue
                record = {
                    "geography": geography,
                    "line_label": label,
                    "accounts_2023_24": "",
                    "re_2024_25": "",
                    "be_2025_26": "",
                }
                record[status_column] = value
                out.append(record)
        if len({row["geography"] for row in out}) >= _MIN_GEO_ROWS:
            return header_index, out
    return None


def parse_rbi_sf_xlsx(payload: bytes) -> ParsedTable:
    if not is_xlsx(payload):
        head = payload.lstrip()[:64].lower()
        if b"<html" in head or b"<!doctype" in head:
            return _empty_fail(
                "rbidocs waf html (not xlsx); browser-capable fetch path required"
            )
        return _empty_fail("rbi sf artifact is not an xlsx")
    workbook = load_workbook(BytesIO(payload), read_only=True, data_only=True)
    try:
        sheet_names = list(workbook.sheetnames)
        for name in sheet_names:
            grid = _grid_from_sheet(list(workbook[name].iter_rows(values_only=True)))
            geo_rows = _find_geo_row_table(grid)
            if geo_rows is not None:
                _header_index, column_map, rows = geo_rows
                return _ok(
                    TIDY_COLUMNS,
                    rows,
                    VALUE_COLUMNS,
                    f"sheet={name}; orientation=geo-rows; "
                    f"columns={','.join(sorted(column_map.values()))}",
                )
            geo_cols = _find_geo_column_table(grid)
            if geo_cols is not None:
                _header_index, rows = geo_cols
                return _ok(
                    TIDY_COLUMNS,
                    rows,
                    VALUE_COLUMNS,
                    f"sheet={name}; orientation=geo-columns",
                )
    finally:
        workbook.close()
    return _empty_fail(
        "rbi sf xlsx has no clear Frame A geography × Accounts/RE/BE column map"
    )


def parse_cag_cfra_glance_pdf(payload: bytes) -> ParsedTable:
    if not is_pdf(payload):
        return _empty_fail("cag cfra glance artifact is not a pdf")
    try:
        pdf = pdfplumber.open(BytesIO(payload))
    except PdfminerException:
        return _empty_fail("cag cfra glance: not a readable pdf")
    try:
        # Glance tables use fragmented multi-row headers (State/UT / SOTR split
        # across rows). No unique single-row column map — stop.
        probed = 0
        for page in pdf.pages:
            tables = page.extract_tables() or []
            for table in tables:
                if len(table) < 10:
                    continue
                probed += 1
                header = " ".join(_norm(cell) for cell in table[0])
                if "State" in header or "SOTR" in header or "Grant" in header:
                    return _empty_fail(
                        "cag glance table headers are multi-row / fragmented; "
                        "no unique column map — not guessing"
                    )
        if probed == 0:
            return _empty_fail("cag glance pdf has no state-sized extractable tables")
        return _empty_fail(
            "cag glance pdf tables lack a unique State/UT column map — not guessing"
        )
    finally:
        pdf.close()


register_parser(
    "rbi-sf-xlsx",
    ParserSpec(parse=parse_rbi_sf_xlsx, lineage_name=PARSER, kind="xlsx"),
)
register_parser(
    "cag-cfra-glance-pdf",
    ParserSpec(parse=parse_cag_cfra_glance_pdf, lineage_name=PARSER, kind="pdf"),
)
