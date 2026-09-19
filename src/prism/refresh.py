"""Refresh contract: vintage ids, triggers, and slice series bindings from the catalog."""

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
    YesNo,
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

ORGI = (
    "Office of the Registrar General & Census Commissioner, India (ORGI), "
    "Ministry of Home Affairs"
)
ORGI_VSD = "Office of the Registrar General of India, Vital Statistics Division (ORGI)"
NCP_MOHFW = (
    "National Commission on Population, Ministry of Health & Family Welfare "
    "(Technical Group on Population Projections)"
)

ORGI_LICENCE = (
    "Not stated on the artifact. ORGI site footer: all rights reserved. "
    "NADA: © 2026, ORGI Digital Library, All Rights Reserved. Not stated as CC-BY."
)
NCP_LICENCE = (
    "Not stated on the title pages fetched. Government of India report. "
    "Not stated as CC-BY."
)

PRODUCER_SLUG_ORGI = "orgi"
PRODUCER_SLUG_NCP_MOHFW = "ncp-mohfw"

C2_FRAME_A_ID = "c2-frame-a"
C2_FRAME_B_ID = "c2-frame-b"
C2_FRAME_C_ID = "c2-frame-c"
C2_FRAME_D_ID = "c2-frame-d"
C2_FRAME_E_ID = "c2-frame-e"

C2_GEOGRAPHY_VINTAGE_2011 = "2011"
C2_GEOGRAPHY_VINTAGE_2024 = "2024"
C2_GEOGRAPHY_VINTAGE_2019 = "2019"

SERIES_CENSUS_2011_PCA_SD = "census-2011-pca-sd"
SERIES_CENSUS_2011_A02_DECADAL = "census-2011-a02-decadal"
SERIES_SRS_BULLETIN_2024 = "srs-bulletin-2024"
SERIES_SRS_STATISTICAL_REPORT_2024 = "srs-statistical-report-2024"
SERIES_NCP_PROJECTIONS_2011_2036_TABLE8 = "ncp-projections-2011-2036-table8"

CITE_C2_CARD_1 = "cite-c2-census-2011-pca-sd"
CITE_C2_CARD_2 = "cite-c2-census-2011-a02-decadal"
CITE_C2_CARD_3 = "cite-c2-srs-bulletin-2024"
CITE_C2_CARD_4 = "cite-c2-srs-statistical-report-2024"
CITE_C2_CARD_5 = "cite-c2-ncp-projections-2011-2036-table8"

CAVEAT_C2_CARD_1 = "caveat-c2-census-2011-pca-sd"
CAVEAT_C2_CARD_2 = "caveat-c2-census-2011-a02-decadal"
CAVEAT_C2_CARD_3 = "caveat-c2-srs-bulletin-2024"
CAVEAT_C2_CARD_4 = "caveat-c2-srs-statistical-report-2024"
CAVEAT_C2_CARD_5 = "caveat-c2-ncp-projections-2011-2036-table8"

C2_CARD_1_SOURCE_VINTAGE = "2011"
C2_CARD_2_SOURCE_VINTAGE = "2011"
C2_CARD_3_SOURCE_VINTAGE = "2024"
C2_CARD_4_SOURCE_VINTAGE = "2024"
C2_CARD_5_SOURCE_VINTAGE = "2011-2036-table8"

MOF_BUDGET = "Ministry of Finance, Budget Division, Government of India"
CGA = "Controller General of Accounts (CGA), Department of Expenditure, Ministry of Finance"

MOF_BUDGET_LICENCE = (
    "Not stated on the PDF. indiabudget.gov.in Terms of Use: content provided "
    "by Ministry of Finance; NIC hosts; disclaimer, not an open licence. "
    "Not stated as CC-BY."
)
CGA_LICENCE = (
    "CGA site footer: website belongs to Controller General of Accounts, "
    "Ministry of Finance; © 2016, All rights reserved, National Informatics "
    "Centre Services Inc. Not stated as CC-BY."
)

PRODUCER_SLUG_MOF_BUDGET = "mof-budget"
PRODUCER_SLUG_CGA = "cga"

C3_FRAME_A_ID = "c3-frame-a"
C3_FRAME_B_ID = "c3-frame-b"
C3_FRAME_C_ID = "c3-frame-c"

C3_GEOGRAPHY_VINTAGE_2026 = "2026"
C3_GEOGRAPHY_VINTAGE_2024 = "2024"

SERIES_BUDGET_2026_27_TAX_REVENUE = "budget-2026-27-tax-revenue"
SERIES_BUDGET_2026_27_NON_TAX_REVENUE = "budget-2026-27-non-tax-revenue"
SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS = "budget-2026-27-capital-receipts"
SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS = "budget-2026-27-annex1-trends-receipts"
SERIES_BUDGET_2026_27_EXPENDITURE_STAT1 = "budget-2026-27-expenditure-stat1"
SERIES_BUDGET_2026_27_DEFICIT_STATISTICS = "budget-2026-27-deficit-statistics"
SERIES_BUDGET_2026_27_LIABILITIES = "budget-2026-27-liabilities"
SERIES_BUDGET_2026_27_FRBM_STATEMENTS = "budget-2026-27-frbm-statements"
SERIES_BUDGET_2026_27_AFS = "budget-2026-27-afs"
SERIES_CGA_MONTHLY_GLANCE_2026_07 = "cga-monthly-glance-2026-07"
SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1 = "cga-finance-accounts-2024-25-stat1"

CITE_C3_CARD_1 = "cite-c3-budget-2026-27-tax-revenue"
CITE_C3_CARD_2 = "cite-c3-budget-2026-27-non-tax-revenue"
CITE_C3_CARD_3 = "cite-c3-budget-2026-27-capital-receipts"
CITE_C3_CARD_4 = "cite-c3-budget-2026-27-annex1-trends-receipts"
CITE_C3_CARD_5 = "cite-c3-budget-2026-27-expenditure-stat1"
CITE_C3_CARD_6 = "cite-c3-budget-2026-27-deficit-statistics"
CITE_C3_CARD_7 = "cite-c3-budget-2026-27-liabilities"
CITE_C3_CARD_8 = "cite-c3-budget-2026-27-frbm-statements"
CITE_C3_CARD_9 = "cite-c3-budget-2026-27-afs"
CITE_C3_CARD_10 = "cite-c3-cga-monthly-glance-2026-07"
CITE_C3_CARD_11 = "cite-c3-cga-finance-accounts-2024-25-stat1"

CAVEAT_C3_CARD_1 = "caveat-c3-budget-2026-27-tax-revenue"
CAVEAT_C3_CARD_2 = "caveat-c3-budget-2026-27-non-tax-revenue"
CAVEAT_C3_CARD_3 = "caveat-c3-budget-2026-27-capital-receipts"
CAVEAT_C3_CARD_4 = "caveat-c3-budget-2026-27-annex1-trends-receipts"
CAVEAT_C3_CARD_5 = "caveat-c3-budget-2026-27-expenditure-stat1"
CAVEAT_C3_CARD_6 = "caveat-c3-budget-2026-27-deficit-statistics"
CAVEAT_C3_CARD_7 = "caveat-c3-budget-2026-27-liabilities"
CAVEAT_C3_CARD_8 = "caveat-c3-budget-2026-27-frbm-statements"
CAVEAT_C3_CARD_9 = "caveat-c3-budget-2026-27-afs"
CAVEAT_C3_CARD_10 = "caveat-c3-cga-monthly-glance-2026-07"
CAVEAT_C3_CARD_11 = "caveat-c3-cga-finance-accounts-2024-25-stat1"

C3_BUDGET_SOURCE_VINTAGE = "2026-27"
C3_CGA_MONTHLY_SOURCE_VINTAGE = "2026-07"
C3_CGA_FA_SOURCE_VINTAGE = "2024-25"


@dataclass(frozen=True)
class SeriesBinding:
    card: int
    series_id: str
    name: str
    producer: str
    producer_slug: str
    next_release: date | Literal["unknown"]
    geography_frame_id: str
    geography_vintage: str
    source_vintage: str
    citation_id: str
    caveat_id: str


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


def _named_hole_series_ids() -> frozenset[str]:
    from prism.catalog import default_catalog

    return default_catalog().named_hole_series_ids()


def _named_hole_citation_ids() -> frozenset[str]:
    from prism.catalog import default_catalog

    return default_catalog().named_hole_citation_ids()


def lineage_blocks_completeness(series_id: str, lineage_ok: YesNo) -> bool:
    """Named holes may be lineage_ok: no on a complete vintage. Other series may not."""

    if lineage_ok is YesNo.yes:
        return False
    return series_id not in _named_hole_series_ids()


def lineage_record_blocks_completeness(record: LineageRecord) -> bool:
    if record.lineage_ok is YesNo.yes:
        return False
    return record.citation_id not in _named_hole_citation_ids()


def _as_binding(entry: object) -> SeriesBinding:
    return SeriesBinding(
        card=entry.card,  # type: ignore[attr-defined]
        series_id=entry.series_id,  # type: ignore[attr-defined]
        name=entry.name,  # type: ignore[attr-defined]
        producer=entry.producer,  # type: ignore[attr-defined]
        producer_slug=entry.producer_slug,  # type: ignore[attr-defined]
        next_release=entry.next_release,  # type: ignore[attr-defined]
        geography_frame_id=entry.geography_frame_id,  # type: ignore[attr-defined]
        geography_vintage=entry.geography_vintage,  # type: ignore[attr-defined]
        source_vintage=entry.source_vintage,  # type: ignore[attr-defined]
        citation_id=entry.citation_id,  # type: ignore[attr-defined]
        caveat_id=entry.caveat_id,  # type: ignore[attr-defined]
    )


def _slice_bindings(slice_id: str) -> tuple[SeriesBinding, ...]:
    from prism.catalog import default_catalog

    return tuple(
        _as_binding(entry) for entry in default_catalog().slice(slice_id).series
    )


C1_SERIES: tuple[SeriesBinding, ...] = _slice_bindings("c1")
C1_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C1_SERIES)
C1_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C1_SERIES
}

C2_SERIES: tuple[SeriesBinding, ...] = _slice_bindings("c2")
C2_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C2_SERIES)
C2_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C2_SERIES
}

C3_SERIES: tuple[SeriesBinding, ...] = _slice_bindings("c3")
C3_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C3_SERIES)
C3_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C3_SERIES
}

C3_NAMED_HOLE_SERIES_IDS: tuple[str, ...] = tuple(
    binding.series_id
    for binding in C3_SERIES
    if binding.series_id in _named_hole_series_ids()
)
C3_LINEAGE_REQUIRED_SERIES_IDS: tuple[str, ...] = tuple(
    series_id
    for series_id in C3_SERIES_IDS
    if series_id not in C3_NAMED_HOLE_SERIES_IDS
)
NAMED_HOLE_SERIES_IDS: frozenset[str] = _named_hole_series_ids()
NAMED_HOLE_CITATION_IDS: frozenset[str] = _named_hole_citation_ids()


def scheduled_series_on(day: date) -> tuple[SeriesBinding, ...]:
    """Schedule follows each series' next_release, not a hidden global clock."""

    from prism.catalog import default_catalog

    bindings = [
        _as_binding(entry)
        for item in default_catalog().slices
        for entry in item.series
        if entry.next_release != "unknown" and entry.next_release == day
    ]
    return tuple(bindings)
