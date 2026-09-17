"""Refresh contract: vintage ids, triggers, and locked C1 series bindings."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

from prism.schema import (
    InputManifest,
    LineageRecord,
    RefreshTrigger,
    SourceChanged,
    canonical_json_bytes,
)

STORE_TIMEZONE = UTC
DISPLAY_TIMEZONE = ZoneInfo("Asia/Kolkata")

VINTAGE_ID_PATTERN = re.compile(r"^dv-\d{8}-[0-9a-f]{12}$")

MOSPI_NSO_PSD = (
    "National Statistics Office, Price Statistics Division, "
    "Ministry of Statistics and Programme Implementation (MoSPI)"
)

C1_LICENCE = (
    "Not stated on the workbook or press PDF. MoSPI Copyrights Policy: "
    "reproduce accurately, not in a derogatory or misleading context, "
    "source acknowledged. GSDD 2026 Category A (open access) lists "
    "Consumer Price Index (CPI). Not stated as CC-BY."
)

C1_FRAME_A_ID = "c1-frame-a"
C1_FRAME_B_ID = "c1-frame-b"
C1_GEOGRAPHY_VINTAGE = "2024"

SERIES_CPI_GENERAL_BASE_2024 = "cpi-general-base-2024"
SERIES_CPI_CFPI_BASE_2024 = "cpi-cfpi-base-2024"
SERIES_CPI_DIVISION_GROUP_BASE_2024 = "cpi-division-group-base-2024"
SERIES_CPI_BACK_SERIES_LINKED_BASE_2024 = "cpi-back-series-linked-base-2024"

CITE_C1_CARD_1 = "cite-c1-cpi-general-base-2024-2026-08"
CITE_C1_CARD_2 = "cite-c1-cpi-cfpi-base-2024-2026-08"
CITE_C1_CARD_3 = "cite-c1-cpi-division-group-base-2024-2026-08"
CITE_C1_CARD_4 = "cite-c1-cpi-back-series-linked-base-2024"

CAVEAT_C1_CARD_1 = "caveat-c1-cpi-general-base-2024"
CAVEAT_C1_CARD_2 = "caveat-c1-cpi-cfpi-base-2024"
CAVEAT_C1_CARD_3 = "caveat-c1-cpi-division-group-base-2024"
CAVEAT_C1_CARD_4 = "caveat-c1-cpi-back-series-linked-base-2024"

CARDS_1_3_NEXT_RELEASE = date(2026, 10, 12)
CARDS_1_3_SOURCE_VINTAGE = "2026-08"
CARD_4_SOURCE_VINTAGE = "2013-2024-linked"


@dataclass(frozen=True)
class C1SeriesBinding:
    card: int
    series_id: str
    name: str
    next_release: date | Literal["unknown"]
    geography_frame_id: str
    source_vintage: str
    citation_id: str
    caveat_id: str


C1_SERIES: tuple[C1SeriesBinding, ...] = (
    C1SeriesBinding(
        card=1,
        series_id=SERIES_CPI_GENERAL_BASE_2024,
        name="Consumer Price Index (CPI) General — Rural, Urban and Combined (Base 2024=100)",
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_1,
        caveat_id=CAVEAT_C1_CARD_1,
    ),
    C1SeriesBinding(
        card=2,
        series_id=SERIES_CPI_CFPI_BASE_2024,
        name=(
            "Consumer Food Price Index (CFPI) — Rural, Urban and Combined; "
            "same values as CPI Group name Food, Group code 01.1 (Base 2024=100)"
        ),
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_2,
        caveat_id=CAVEAT_C1_CARD_2,
    ),
    C1SeriesBinding(
        card=3,
        series_id=SERIES_CPI_DIVISION_GROUP_BASE_2024,
        name=(
            "CPI Division indexes and CPI Group indexes, Rural / Urban / Combined "
            "(Base 2024=100), COICOP 2018 (12 Divisions, 43 Groups)"
        ),
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_3,
        caveat_id=CAVEAT_C1_CARD_3,
    ),
    C1SeriesBinding(
        card=4,
        series_id=SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
        name="CPI Back Series Index Inflation Based on Base Year 2024 (linked General only)",
        next_release="unknown",
        geography_frame_id=C1_FRAME_B_ID,
        source_vintage=CARD_4_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_4,
        caveat_id=CAVEAT_C1_CARD_4,
    ),
)

C1_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C1_SERIES)

C1_SERIES_BY_ID: dict[str, C1SeriesBinding] = {
    binding.series_id: binding for binding in C1_SERIES
}


def ensure_utc(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        raise ValueError("store datetimes must be timezone-aware UTC")
    if moment.utcoffset() != timedelta(0):
        raise ValueError("store datetimes must be UTC")
    return moment.astimezone(STORE_TIMEZONE)


def display_in_kolkata(moment: datetime) -> datetime:
    return ensure_utc(moment).astimezone(DISPLAY_TIMEZONE)


def vintage_id_for(run_date_utc: date, input_manifest: InputManifest) -> str:
    digest = hashlib.sha256(canonical_json_bytes(input_manifest)).hexdigest()[:12]
    vintage_id = f"dv-{run_date_utc.strftime('%Y%m%d')}-{digest}"
    if VINTAGE_ID_PATTERN.fullmatch(vintage_id) is None:
        raise ValueError(f"vintage_id_rule produced an invalid id: {vintage_id}")
    return vintage_id


def trigger_from_lineage(record: LineageRecord) -> RefreshTrigger | None:
    """source_change fires on first retrieve or a checksum change. no is not a trigger."""

    if record.source_changed is SourceChanged.no:
        return None
    return RefreshTrigger.source_change


def scheduled_series_on(day: date) -> tuple[C1SeriesBinding, ...]:
    """Schedule follows each series' next_release, not a hidden global clock."""

    return tuple(
        binding
        for binding in C1_SERIES
        if binding.next_release != "unknown" and binding.next_release == day
    )
