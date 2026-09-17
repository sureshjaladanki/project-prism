"""Ingest: retrieve official bytes, tidy producer tables, write lineage."""

from prism.ingest.c1 import ingest_c1
from prism.ingest.parse import PARSER

__all__ = ["PARSER", "ingest_c1"]
