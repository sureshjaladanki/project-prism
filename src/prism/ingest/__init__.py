"""Ingest: retrieve official bytes, tidy producer tables, write lineage."""

from prism.ingest.run import ingest, ingest_c1, ingest_c2, ingest_c3
from prism.ingest.xlsx_cpi_period import PARSER

__all__ = ["PARSER", "ingest", "ingest_c1", "ingest_c2", "ingest_c3"]
