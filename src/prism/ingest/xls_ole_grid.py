"""OLE .xls rectangular cell grid. Stop if the workbook cannot be read as cells."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import xlrd  # type: ignore[import-untyped]
from xlrd import XLRDError

from prism.ingest.retrieve import is_xls_ole

try:
    from xlrd.compdoc import CompDocError  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    CompDocError = XLRDError

_XLS_OPEN_ERRORS = (XLRDError, CompDocError, OSError)


@dataclass(frozen=True)
class XlsSheet:
    name: str
    rows: tuple[tuple[str, ...], ...]


def _cell_text(cell: Any) -> str:
    ctype = int(cell.ctype)
    value = cell.value
    if ctype in {xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK}:
        return ""
    if ctype == xlrd.XL_CELL_ERROR:
        return ""
    if ctype == xlrd.XL_CELL_BOOLEAN:
        return "1" if value else "0"
    if ctype in {xlrd.XL_CELL_NUMBER, xlrd.XL_CELL_DATE}:
        number = float(value)
        if number.is_integer():
            return str(int(number))
        return str(value)
    return str(value).strip()


def _expand_merges(
    rows: list[list[str]], merged: list[tuple[int, int, int, int]]
) -> list[list[str]]:
    width = max((len(row) for row in rows), default=0)
    grid = [row + [""] * (width - len(row)) for row in rows]
    for row_lo, row_hi, col_lo, col_hi in merged:
        if row_lo >= len(grid) or col_lo >= width:
            continue
        origin = grid[row_lo][col_lo]
        if origin == "":
            continue
        for row in range(row_lo, min(row_hi, len(grid))):
            for col in range(col_lo, min(col_hi, width)):
                if grid[row][col] == "":
                    grid[row][col] = origin
    return grid


def _open_book(payload: bytes) -> Any | None:
    try:
        return xlrd.open_workbook(file_contents=payload, formatting_info=True)
    except _XLS_OPEN_ERRORS:
        try:
            return xlrd.open_workbook(file_contents=payload, formatting_info=False)
        except _XLS_OPEN_ERRORS:
            return None


def read_xls_sheets(payload: bytes) -> tuple[XlsSheet, ...] | None:
    if not is_xls_ole(payload):
        return None
    book = _open_book(payload)
    if book is None:
        return None
    try:
        sheets: list[XlsSheet] = []
        for index in range(int(book.nsheets)):
            sheet = book.sheet_by_index(index)
            width = int(sheet.ncols)
            raw_rows = [
                [_cell_text(sheet.cell(row, col)) for col in range(width)]
                for row in range(int(sheet.nrows))
            ]
            merged = list(sheet.merged_cells)
            grid = _expand_merges(raw_rows, merged) if merged else raw_rows
            sheets.append(
                XlsSheet(
                    name=str(sheet.name),
                    rows=tuple(tuple(row) for row in grid),
                )
            )
    finally:
        book.release_resources()
    if not sheets:
        return None
    return tuple(sheets)
