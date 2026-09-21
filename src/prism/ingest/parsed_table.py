"""Producer table result from an ingest parse. No mapping."""

from __future__ import annotations

from dataclasses import dataclass

from prism.schema import YesNo


@dataclass(frozen=True)
class ParsedTable:
    csv_text: str
    row_count: int
    nulls: str
    flags: str
    lineage_ok: YesNo
