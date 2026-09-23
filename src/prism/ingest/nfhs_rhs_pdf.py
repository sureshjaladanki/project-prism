"""NFHS-6 fact sheets and RHS 2021-22 PDF parsers. Stop when cells are ambiguous."""

from __future__ import annotations

import csv
import re
from io import BytesIO, StringIO

import pdfplumber
from pdfplumber.utils.exceptions import PdfminerException

from prism.ingest.parsed_table import ParsedTable
from prism.ingest.pdf_word_columns import (
    PdfColumn,
    PdfWord,
    cluster_rows,
    is_amount_token,
    nearest_column,
    page_words,
)
from prism.schema import YesNo

PARSER_NAME = "nfhs-rhs-pdf"
PARSER_VERSION = "1.0.0"
PARSER = f"{PARSER_NAME}-{PARSER_VERSION}"

PDF_Y_TOL = 4.0

NFHS_VALUE_COLUMNS = (
    "nfhs6_urban",
    "nfhs6_rural",
    "nfhs6_total",
    "nfhs5_total",
)
NFHS_COLUMNS = ("geography", "indicator") + NFHS_VALUE_COLUMNS
NFHS_PDF_COLUMNS = (
    PdfColumn("nfhs6_urban", "Urban"),
    PdfColumn("nfhs6_rural", "Rural"),
    PdfColumn("nfhs6_total", "Total"),
    PdfColumn("nfhs5_total", "Total"),
)

RHS_VALUE_COLUMNS = ("sc_2022", "phc_2022", "chc_2022")
RHS_COLUMNS = ("geography",) + RHS_VALUE_COLUMNS
RHS_ALL_VALUE_COLUMNS = (
    "sc_2005",
    "phc_2005",
    "chc_2005",
    "sc_2022",
    "phc_2022",
    "chc_2022",
)

_IND = re.compile(r"^\d+\.")
_COLLAPSE = re.compile(r"[^a-z0-9]+")
_SERIAL = re.compile(r"^\d+$")
_WITHHELD = frozenset({"-", "–", "—", "---", "..", "..."})

NFHS_FRAME_NAMES = (
    "India",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
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
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra & Nagar Haveli and Daman & Diu",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "NCT of Delhi",
    "Puducherry",
)


def _empty_fail(flags: str) -> ParsedTable:
    return ParsedTable(
        csv_text="",
        row_count=0,
        nulls="not parsed",
        flags=flags,
        lineage_ok=YesNo.no,
    )


def _to_csv(fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _ok_rows(
    fieldnames: tuple[str, ...],
    rows: list[dict[str, str]],
    value_columns: tuple[str, ...],
    flags: str,
) -> ParsedTable:
    nulls = sum(1 for row in rows for name in value_columns if row[name] == "")
    return ParsedTable(
        csv_text=_to_csv(fieldnames, rows),
        row_count=len(rows),
        nulls=f"{nulls} empty value cells" if nulls else "none",
        flags=flags,
        lineage_ok=YesNo.yes,
    )


def _collapse(text: str) -> str:
    return _COLLAPSE.sub("", text.lower())


def _match_nfhs_geography(raw: str) -> str | None:
    collapsed = _collapse(raw)
    for name in NFHS_FRAME_NAMES:
        if _collapse(name) == collapsed:
            return name
    aliases = {
        _collapse("Andaman & Nicobar Islands"): "Andaman and Nicobar Islands",
        _collapse("Jammu & Kashmir"): "Jammu and Kashmir",
    }
    return aliases.get(collapsed)


def _nfhs_title_geography(words: list[PdfWord]) -> str | None:
    if not words:
        return None
    top = min(word.top for word in words)
    head = sorted(
        (word for word in words if abs(word.top - top) <= 4.0),
        key=lambda word: word.x0,
    )
    parts: list[str] = []
    for word in head:
        if word.text in {"-", "–", "—"}:
            break
        token = _collapse(word.text)
        if token in {"key", "ke", "y", "indicators", "indicator"}:
            break
        parts.append(word.text)
    if not parts:
        return None
    return _match_nfhs_geography(" ".join(parts))


def _assign_nfhs_table(
    words: list[PdfWord],
) -> tuple[list[dict[str, str]], int, int] | None:
    """Like assign_pdf_table, but gutter footnote digits left of Urban stay labels."""

    buckets = cluster_rows(words, PDF_Y_TOL)
    header_words: list[PdfWord] | None = None
    header_index: int | None = None
    tokens = tuple(column.token for column in NFHS_PDF_COLUMNS)
    names = tuple(column.name for column in NFHS_PDF_COLUMNS)
    for index, bucket in enumerate(buckets):
        remaining = list(tokens)
        used: list[PdfWord] = []
        for word in sorted(bucket, key=lambda item: item.x0):
            if remaining and word.text == remaining[0]:
                used.append(word)
                remaining.pop(0)
        if remaining:
            continue
        header_words = used
        header_index = index
        break
    if header_words is None or header_index is None:
        return None
    centers = tuple((word.x0 + word.x1) / 2 for word in header_words)
    gaps = [centers[i + 1] - centers[i] for i in range(len(centers) - 1)]
    half = min(gaps) / 2
    # Gutter is left of the Urban column band — footnote digits are not cells.
    left = centers[0] - half
    assigned = 0
    ambiguous = 0
    rows: list[dict[str, str]] = []
    for bucket in buckets[header_index + 1 :]:
        record = {name: "" for name in names}
        labels: list[str] = []
        for word in bucket:
            if word.xmid < left:
                labels.append(word.text)
                continue
            if not is_amount_token(word.text):
                labels.append(word.text)
                continue
            if word.text.strip() in {"…", "...", "..", ".", "-", "–", "—"}:
                column = nearest_column(word.xmid, centers, half)
                if column is None:
                    ambiguous += 1
                    continue
                assigned += 1
                continue
            column = nearest_column(word.xmid, centers, half)
            if column is None:
                ambiguous += 1
                continue
            assigned += 1
            record[names[column]] = word.text.lstrip("*")
        if not labels and not any(record.values()):
            continue
        record["line_label"] = " ".join(labels)
        rows.append(record)
    return rows, assigned, ambiguous


def parse_nfhs_6_factsheets(payload: bytes) -> ParsedTable:
    if not payload.startswith(b"%PDF"):
        return _empty_fail("nfhs fact sheets is not a pdf")
    try:
        document = pdfplumber.open(BytesIO(payload))
    except PdfminerException as exc:
        return _empty_fail(f"nfhs fact sheets pdf open failed: {exc}")
    rows: list[dict[str, str]] = []
    assigned_n = 0
    try:
        for page in document.pages:
            words = page_words(page)
            collapsed = _collapse(" ".join(word.text for word in words[:50]))
            if "keyindicators" not in collapsed:
                continue
            geography = _nfhs_title_geography(words)
            assigned = _assign_nfhs_table(words)
            if assigned is None:
                continue
            if geography is None:
                return _empty_fail(
                    "nfhs fact sheets: geography title did not map uniquely to Frame C; "
                    "not guessing"
                )
            part_rows, part_assigned, ambiguous = assigned
            if ambiguous:
                return _empty_fail(
                    f"nfhs fact sheets {geography}: {ambiguous} amount tokens "
                    "did not map uniquely; not guessing"
                )
            assigned_n += part_assigned
            for row in part_rows:
                label = row.get("line_label", "").strip()
                if not _IND.match(label):
                    continue
                rows.append(
                    {
                        "geography": geography,
                        "indicator": label,
                        **{name: row.get(name, "") for name in NFHS_VALUE_COLUMNS},
                    }
                )
    finally:
        document.close()
    if not rows:
        return _empty_fail("nfhs fact sheets: no Key Indicators rows found")
    geos = {row["geography"] for row in rows}
    if "India" not in geos:
        return _empty_fail("nfhs fact sheets missing India rows")
    if "Manipur" in geos:
        return _empty_fail(
            "nfhs fact sheets unexpectedly contains Manipur; Frame C says absent"
        )
    missing = [name for name in NFHS_FRAME_NAMES if name not in geos]
    if missing:
        return _empty_fail(
            "nfhs fact sheets missing Frame C units: " + ", ".join(missing)
        )
    return _ok_rows(
        NFHS_COLUMNS,
        rows,
        NFHS_VALUE_COLUMNS,
        f"pdfplumber words; assigned={assigned_n}; ambiguous=0; y_tol={PDF_Y_TOL}; "
        f"geographies={len(geos)}",
    )


def _rhs_is_statement1(words: list[PdfWord]) -> bool:
    head = " ".join(word.text for word in sorted(words, key=lambda w: (w.top, w.x0))[:40])
    collapsed = _collapse(head)
    return "comparativestatement1" in collapsed and "functioning" in collapsed


def _consume_rhs_header(row: list[PdfWord]) -> list[PdfWord] | None:
    tokens = ("Sub", "Centre", "PHCs", "CHCs", "Sub", "Centre", "PHCs", "CHCs")
    remaining = list(tokens)
    used: list[PdfWord] = []
    for word in sorted(row, key=lambda item: item.x0):
        if remaining and word.text == remaining[0]:
            used.append(word)
            remaining.pop(0)
    if remaining:
        return None
    return used


def _rhs_centers(header: list[PdfWord]) -> tuple[float, ...]:
    return (
        (header[0].xmid + header[1].xmid) / 2,
        header[2].xmid,
        header[3].xmid,
        (header[4].xmid + header[5].xmid) / 2,
        header[6].xmid,
        header[7].xmid,
    )


def _assign_rhs_statement1(
    words: list[PdfWord],
) -> tuple[list[dict[str, str]], int, int] | None:
    buckets = cluster_rows(words, PDF_Y_TOL)
    header: list[PdfWord] | None = None
    header_index: int | None = None
    for index, bucket in enumerate(buckets):
        found = _consume_rhs_header(bucket)
        if found is None:
            continue
        header = found
        header_index = index
        break
    if header is None or header_index is None:
        return None
    centers = _rhs_centers(header)
    left = min(word.x0 for word in header) - 8
    gaps = [centers[i + 1] - centers[i] for i in range(len(centers) - 1)]
    half = min(gaps) / 2
    assigned = 0
    ambiguous = 0
    rows: list[dict[str, str]] = []
    for bucket in buckets[header_index + 1 :]:
        record = {name: "" for name in RHS_ALL_VALUE_COLUMNS}
        labels: list[str] = []
        for word in bucket:
            if word.xmid < left:
                labels.append(word.text)
                continue
            if not is_amount_token(word.text):
                labels.append(word.text)
                continue
            if word.text.strip() in _WITHHELD:
                column = nearest_column(word.xmid, centers, half)
                if column is None:
                    ambiguous += 1
                    continue
                assigned += 1
                continue
            column = nearest_column(word.xmid, centers, half)
            if column is None:
                ambiguous += 1
                continue
            assigned += 1
            record[RHS_ALL_VALUE_COLUMNS[column]] = word.text.lstrip("*")
        label = " ".join(labels).strip()
        if _SERIAL.fullmatch(label):
            label = ""
        else:
            label = re.sub(r"^\d+\s+", "", label).strip()
        if not label and not any(record.values()):
            continue
        record["line_label"] = label
        rows.append(record)
    return rows, assigned, ambiguous


def _rhs_note_label(label: str) -> bool:
    low = label.lower()
    return (
        low.startswith("notes")
        or "bifurcat" in low
        or "merged as" in low
        or "came to existence" in low
    )


def _stitch_rhs_rows(rows: list[dict[str, str]]) -> list[dict[str, str]] | None:
    out: list[dict[str, str]] = []
    index = 0
    while index < len(rows):
        row = rows[index]
        label = row.get("line_label", "").strip()
        if _rhs_note_label(label):
            break
        values = {name: row.get(name, "") for name in RHS_ALL_VALUE_COLUMNS}
        if not label:
            # Trailing page number / orphan amounts after the table.
            if not any(values.values()):
                index += 1
                continue
            return None
        # Dadra wrap: 2005 on the label line, 2022 amounts on the next blank-label line.
        if index + 1 < len(rows):
            nxt = rows[index + 1]
            nxt_label = nxt.get("line_label", "").strip()
            if not nxt_label and any(
                nxt.get(name, "") for name in ("sc_2022", "phc_2022", "chc_2022")
            ):
                if not any(values[name] for name in ("sc_2022", "phc_2022", "chc_2022")):
                    for name in ("sc_2022", "phc_2022", "chc_2022"):
                        values[name] = nxt.get(name, "")
                    index += 1
        out.append(
            {
                "geography": label,
                "sc_2022": values["sc_2022"],
                "phc_2022": values["phc_2022"],
                "chc_2022": values["chc_2022"],
            }
        )
        index += 1
    return out


def parse_rhs_2021_22(payload: bytes) -> ParsedTable:
    if not payload.startswith(b"%PDF"):
        return _empty_fail("rhs yearbook is not a pdf")
    try:
        document = pdfplumber.open(BytesIO(payload))
    except PdfminerException as exc:
        return _empty_fail(f"rhs yearbook pdf open failed: {exc}")
    try:
        for page in document.pages:
            words = page_words(page)
            if not _rhs_is_statement1(words):
                continue
            assigned = _assign_rhs_statement1(words)
            if assigned is None:
                return _empty_fail(
                    "rhs Statement 1: Sub Centre/PHCs/CHCs header not found"
                )
            raw_rows, assigned_n, ambiguous = assigned
            if ambiguous:
                return _empty_fail(
                    f"rhs Statement 1: {ambiguous} amount tokens did not map "
                    "uniquely; not guessing"
                )
            stitched = _stitch_rhs_rows(raw_rows)
            if stitched is None:
                return _empty_fail(
                    "rhs Statement 1: wrapped State/UT rows did not stitch uniquely"
                )
            kept = [
                row
                for row in stitched
                if row["geography"] and not _rhs_note_label(row["geography"])
            ]
            # Keep geographies even when 2022 cells are blank (e.g. Daman & Diu after merge)
            if not any("all india" in row["geography"].lower() for row in kept):
                return _empty_fail("rhs Statement 1 missing All India/ Total row")
            ordered = [
                {name: row.get(name, "") for name in RHS_COLUMNS} for row in kept
            ]
            return _ok_rows(
                RHS_COLUMNS,
                ordered,
                RHS_VALUE_COLUMNS,
                f"pdfplumber words; assigned={assigned_n}; ambiguous=0; "
                f"y_tol={PDF_Y_TOL}; statement=1",
            )
    finally:
        document.close()
    return _empty_fail("rhs Comparative Statement 1 not found")


from prism.catalog.registry import ParserSpec, register_parser

register_parser(
    "nfhs-6-factsheets-pdf",
    ParserSpec(parse=parse_nfhs_6_factsheets, lineage_name=PARSER, kind="pdf"),
)
register_parser(
    "rhs-2021-22-pdf",
    ParserSpec(parse=parse_rhs_2021_22, lineage_name=PARSER, kind="pdf"),
)
