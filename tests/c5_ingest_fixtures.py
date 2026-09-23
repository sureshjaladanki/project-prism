"""Tiny RBI State Finances–shaped xlsx for C5 ingest tests. Not producer bytes."""

from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook

from prism.ingest.rbi_cag_state_finance import FRAME_A_GEOGRAPHIES


def rbi_sf_geo_rows_workbook_bytes() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Appendix1"
    sheet.append(["Major Deficit Indicators"])
    sheet.append([])
    sheet.append(
        [
            "State / UT",
            "Accounts 2023-24",
            "Revised Estimates 2024-25",
            "Budget Estimates 2025-26",
        ]
    )
    for index, name in enumerate(FRAME_A_GEOGRAPHIES[:8]):
        sheet.append([name, 1000 + index, 1100 + index, 1200 + index])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def rbi_sf_waf_html_bytes() -> bytes:
    return (
        b"<!DOCTYPE html><html><head><title>challenge</title></head>"
        b"<body><form><input/><button>submit</button></form></body></html>"
    )
