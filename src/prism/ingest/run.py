"""Dispatch ingest to the slice that owns each series_id."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import httpx

from prism.ingest.c1 import ingest_c1
from prism.ingest.c2 import ingest_c2
from prism.ingest.c3 import ingest_c3
from prism.ingest.retrieve import IngestError, new_client
from prism.refresh import (
    C1_SERIES_BY_ID,
    C1_SERIES_IDS,
    C2_SERIES_BY_ID,
    C2_SERIES_IDS,
    C3_SERIES_BY_ID,
    C3_SERIES_IDS,
)
from prism.schema import LineageRecord

_IngestSlice = Callable[..., tuple[LineageRecord, ...]]

_SLICES: tuple[tuple[frozenset[str], _IngestSlice], ...] = (
    (frozenset(C1_SERIES_IDS), ingest_c1),
    (frozenset(C2_SERIES_IDS), ingest_c2),
    (frozenset(C3_SERIES_IDS), ingest_c3),
)

_KNOWN = {**C1_SERIES_BY_ID, **C2_SERIES_BY_ID, **C3_SERIES_BY_ID}


def ingest(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    if series_ids is not None:
        unknown = [series_id for series_id in series_ids if series_id not in _KNOWN]
        if unknown:
            raise IngestError("unknown series_id: " + ", ".join(unknown))
    own_client = client is None
    http = client if client is not None else new_client()
    records: list[LineageRecord] = []
    try:
        for owned, runner in _SLICES:
            wanted = (
                None
                if series_ids is None
                else tuple(series_id for series_id in series_ids if series_id in owned)
            )
            if wanted == ():
                continue
            records.extend(
                runner(
                    data_root,
                    client=http,
                    retrieved_at=retrieved_at,
                    series_ids=wanted,
                )
            )
    finally:
        if own_client:
            http.close()
    return tuple(records)
