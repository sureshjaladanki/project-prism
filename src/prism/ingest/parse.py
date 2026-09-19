"""Tidy producer tables from MoSPI CPI workbooks. No new concepts."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pandas as pd  # type: ignore[import-untyped]

from prism.ingest.retrieve import IngestError
from prism.schema import YesNo

PARSER_NAME = "mospi-cpi-xlsx"
PARSER_VERSION = "1.0.0"
PARSER = f"{PARSER_NAME}-{PARSER_VERSION}"

GENERAL_SHEET = "General"
GROUP_SHEET = "Group"
DIVISION_SHEET = "Division"
BACK_SHEET = "Sheet1"
CFPI_GROUP_CODE = "01.1"
CFPI_GROUP_NAME = "Food"

GENERAL_COLUMNS = (
    "Base Year",
    "State Code",
    "State Name",
    "Sector",
    "year",
    "month",
    "index",
    "inflation (%)",
    "status",
)
GROUP_COLUMNS = (
    "Base Year",
    "State Code",
    "State Name",
    "Sector",
    "Group Name",
    "Group code",
    "year",
    "month",
    "index",
    "inflation (%)",
    "status",
)
DIVISION_COLUMNS = (
    "Base Year",
    "State Code",
    "State Name",
    "Sector",
    "Division Name",
    "Division code",
    "year",
    "month",
    "index",
    "inflation (%)",
    "status",
)
BACK_COLUMNS = (
    "Base Year",
    "State code",
    "State name",
    "Sector",
    "Year",
    "Month",
    "Group",
    "Index",
    "Inflation (%)",
)
DIVISION_GROUP_COLUMNS = (
    "Base Year",
    "State Code",
    "State Name",
    "Sector",
    "Division Name",
    "Division code",
    "Group Name",
    "Group code",
    "year",
    "month",
    "index",
    "inflation (%)",
    "status",
)

_WITHHELD = frozenset(
    {
        "-",
        "–",
        "—",
        "not available",
        "n/a",
        "na",
        "n.a.",
    }
)
_STATE_CODE_COLUMNS = frozenset({"State Code", "State code"})


@dataclass(frozen=True)
class ParsedTable:
    csv_text: str
    row_count: int
    nulls: str
    flags: str
    lineage_ok: YesNo


def _is_null(value: object) -> bool:
    if value is None:
        return True
    try:
        result = pd.isna(value)
    except (TypeError, ValueError):
        result = False
    if isinstance(result, bool) and result:
        return True
    return isinstance(value, str) and value.strip() == ""


def _cell(value: object) -> object | None:
    if _is_null(value):
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.lower() in _WITHHELD:
            return None
        return stripped
    return value


def _state_code(value: object) -> str | None:
    cleaned = _cell(value)
    if cleaned is None:
        return None
    text = str(cleaned).strip()
    if text.isdigit() and len(text) <= 2:
        return text.zfill(2)
    return text


def _read_sheet(data: bytes, sheet: str) -> pd.DataFrame:
    frame = pd.read_excel(
        BytesIO(data), sheet_name=sheet, dtype=object, engine="openpyxl"
    )
    if not isinstance(frame, pd.DataFrame):
        raise IngestError(f"sheet {sheet!r} did not return a table")
    return frame


def _require_columns(
    frame: pd.DataFrame, expected: tuple[str, ...], sheet: str
) -> None:
    missing = [name for name in expected if name not in frame.columns]
    if missing:
        raise IngestError(f"sheet {sheet!r} missing columns: {', '.join(missing)}")


def _cleanse(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.map(_cell)
    for column in cleaned.columns:
        if column in _STATE_CODE_COLUMNS:
            cleaned[column] = cleaned[column].map(_state_code)
    return cleaned.dropna(how="all")


def _nulls_note(frame: pd.DataFrame, value_columns: tuple[str, ...], extra: str) -> str:
    parts = [
        f"{column}: {int(frame[column].isna().sum())} null"
        for column in value_columns
        if column in frame.columns
    ]
    if extra:
        parts.append(extra)
    return "; ".join(parts) if parts else "none"


def _to_csv(frame: pd.DataFrame) -> str:
    return str(frame.to_csv(index=False, na_rep="", lineterminator="\n"))


def _ok_table(
    frame: pd.DataFrame, value_columns: tuple[str, ...], extra_nulls: str
) -> ParsedTable:
    if len(frame) == 0:
        return ParsedTable(
            csv_text=_to_csv(frame),
            row_count=0,
            nulls="no data rows",
            flags="empty_table",
            lineage_ok=YesNo.no,
        )
    return ParsedTable(
        csv_text=_to_csv(frame),
        row_count=len(frame),
        nulls=_nulls_note(frame, value_columns, extra_nulls),
        flags="none",
        lineage_ok=YesNo.yes,
    )


def _failed(message: str) -> ParsedTable:
    return ParsedTable(
        csv_text="",
        row_count=0,
        nulls="parse_failed",
        flags=message,
        lineage_ok=YesNo.no,
    )


def _chandigarh_rural_note(frame: pd.DataFrame, name_col: str) -> str:
    if name_col not in frame.columns or "Sector" not in frame.columns:
        return ""
    names = frame[name_col].astype("string")
    chandigarh = frame[names == "Chandigarh"]
    if chandigarh.empty:
        return ""
    rural = chandigarh[chandigarh["Sector"].astype("string") == "Rural"]
    if rural.empty:
        return "Chandigarh Rural: no row (withheld as published; not imputed)"
    return ""


def parse_cpi_general(data: bytes) -> ParsedTable:
    try:
        frame = _cleanse(_read_sheet(data, GENERAL_SHEET))
        _require_columns(frame, GENERAL_COLUMNS, GENERAL_SHEET)
        frame = frame.loc[:, list(GENERAL_COLUMNS)]
    except IngestError as exc:
        return _failed(str(exc))
    extra = _chandigarh_rural_note(frame, "State Name")
    return _ok_table(frame, ("index", "inflation (%)"), extra)


def parse_cpi_cfpi(data: bytes) -> ParsedTable:
    try:
        frame = _cleanse(_read_sheet(data, GROUP_SHEET))
        _require_columns(frame, GROUP_COLUMNS, GROUP_SHEET)
        codes = frame["Group code"].astype("string")
        names = frame["Group Name"].astype("string")
        code_food = codes == CFPI_GROUP_CODE
        name_food = names == CFPI_GROUP_NAME
        if int(code_food.sum()) != int(name_food.sum()) or bool(
            (code_food != name_food).any()
        ):
            return _failed(
                "ambiguous CFPI filter: Group code 01.1 and Group Name Food disagree"
            )
        food = frame.loc[code_food, list(GROUP_COLUMNS)].copy()
        if "Division code" in food.columns or "Division Name" in food.columns:
            return _failed(
                "CFPI table includes Division columns; expected Group 01.1 only"
            )
    except IngestError as exc:
        return _failed(str(exc))
    extra = _chandigarh_rural_note(food, "State Name")
    extra = (
        extra
        + ("; " if extra else "")
        + "CFPI = Group Food 01.1 only; Division 01 excluded"
    )
    return _ok_table(food, ("index", "inflation (%)"), extra)


def parse_cpi_division_group(data: bytes) -> ParsedTable:
    try:
        division = _cleanse(_read_sheet(data, DIVISION_SHEET))
        group = _cleanse(_read_sheet(data, GROUP_SHEET))
        _require_columns(division, DIVISION_COLUMNS, DIVISION_SHEET)
        _require_columns(group, GROUP_COLUMNS, GROUP_SHEET)
        stacked = pd.concat([division, group], ignore_index=True, sort=False)
        for column in DIVISION_GROUP_COLUMNS:
            if column not in stacked.columns:
                stacked[column] = None
        stacked = stacked.loc[:, list(DIVISION_GROUP_COLUMNS)]
    except IngestError as exc:
        return _failed(str(exc))
    extra = (
        "Division rows have empty Group columns; Group rows have empty Division columns "
        "(sheet union, producer columns only)"
    )
    extra_geo = _chandigarh_rural_note(stacked, "State Name")
    if extra_geo:
        extra = extra + "; " + extra_geo
    return _ok_table(
        stacked,
        (
            "index",
            "inflation (%)",
            "Division Name",
            "Division code",
            "Group Name",
            "Group code",
        ),
        extra,
    )


def parse_cpi_back_series(data: bytes) -> ParsedTable:
    try:
        frame = _cleanse(_read_sheet(data, BACK_SHEET))
        _require_columns(frame, BACK_COLUMNS, BACK_SHEET)
        frame = frame.loc[:, list(BACK_COLUMNS)]
    except IngestError as exc:
        return _failed(str(exc))
    extra = "blank Inflation (%) kept null; All India only as published; no State/UT rows invented"
    return _ok_table(frame, ("Index", "Inflation (%)"), extra)


from prism.catalog.registry import ParserSpec, register_parser

register_parser(
    "mospi-cpi-general",
    ParserSpec(parse=parse_cpi_general, lineage_name=PARSER, kind="xlsx"),
)
register_parser(
    "mospi-cpi-cfpi",
    ParserSpec(parse=parse_cpi_cfpi, lineage_name=PARSER, kind="xlsx"),
)
register_parser(
    "mospi-cpi-division-group",
    ParserSpec(parse=parse_cpi_division_group, lineage_name=PARSER, kind="xlsx"),
)
register_parser(
    "mospi-cpi-back-series",
    ParserSpec(parse=parse_cpi_back_series, lineage_name=PARSER, kind="xlsx"),
)
