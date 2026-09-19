"""Refresh contract: vintage ids, triggers, and locked C1 / C2 / C3 series bindings."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

from prism.paths import PRODUCER_SLUG_MOSPI
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


C1_SERIES: tuple[SeriesBinding, ...] = (
    SeriesBinding(
        card=1,
        series_id=SERIES_CPI_GENERAL_BASE_2024,
        name="Consumer Price Index (CPI) General — Rural, Urban and Combined (Base 2024=100)",
        producer=MOSPI_NSO_PSD,
        producer_slug=PRODUCER_SLUG_MOSPI,
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        geography_vintage=C1_GEOGRAPHY_VINTAGE,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_1,
        caveat_id=CAVEAT_C1_CARD_1,
    ),
    SeriesBinding(
        card=2,
        series_id=SERIES_CPI_CFPI_BASE_2024,
        name=(
            "Consumer Food Price Index (CFPI) — Rural, Urban and Combined; "
            "same values as CPI Group name Food, Group code 01.1 (Base 2024=100)"
        ),
        producer=MOSPI_NSO_PSD,
        producer_slug=PRODUCER_SLUG_MOSPI,
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        geography_vintage=C1_GEOGRAPHY_VINTAGE,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_2,
        caveat_id=CAVEAT_C1_CARD_2,
    ),
    SeriesBinding(
        card=3,
        series_id=SERIES_CPI_DIVISION_GROUP_BASE_2024,
        name=(
            "CPI Division indexes and CPI Group indexes, Rural / Urban / Combined "
            "(Base 2024=100), COICOP 2018 (12 Divisions, 43 Groups)"
        ),
        producer=MOSPI_NSO_PSD,
        producer_slug=PRODUCER_SLUG_MOSPI,
        next_release=CARDS_1_3_NEXT_RELEASE,
        geography_frame_id=C1_FRAME_A_ID,
        geography_vintage=C1_GEOGRAPHY_VINTAGE,
        source_vintage=CARDS_1_3_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_3,
        caveat_id=CAVEAT_C1_CARD_3,
    ),
    SeriesBinding(
        card=4,
        series_id=SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
        name="CPI Back Series Index Inflation Based on Base Year 2024 (linked General only)",
        producer=MOSPI_NSO_PSD,
        producer_slug=PRODUCER_SLUG_MOSPI,
        next_release="unknown",
        geography_frame_id=C1_FRAME_B_ID,
        geography_vintage=C1_GEOGRAPHY_VINTAGE,
        source_vintage=CARD_4_SOURCE_VINTAGE,
        citation_id=CITE_C1_CARD_4,
        caveat_id=CAVEAT_C1_CARD_4,
    ),
)

C1_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C1_SERIES)

C1_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C1_SERIES
}

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


C2_SERIES: tuple[SeriesBinding, ...] = (
    SeriesBinding(
        card=1,
        series_id=SERIES_CENSUS_2011_PCA_SD,
        name=(
            "Census of India 2011 — Primary Census Abstract (PCA SD): "
            "population, households, and related PCA columns as published"
        ),
        producer=ORGI,
        producer_slug=PRODUCER_SLUG_ORGI,
        next_release="unknown",
        geography_frame_id=C2_FRAME_A_ID,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2011,
        source_vintage=C2_CARD_1_SOURCE_VINTAGE,
        citation_id=CITE_C2_CARD_1,
        caveat_id=CAVEAT_C2_CARD_1,
    ),
    SeriesBinding(
        card=2,
        series_id=SERIES_CENSUS_2011_A02_DECADAL,
        name="Census of India 2011 — Table A-02: Decadal variation in population since 1901",
        producer=ORGI,
        producer_slug=PRODUCER_SLUG_ORGI,
        next_release="unknown",
        geography_frame_id=C2_FRAME_B_ID,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2011,
        source_vintage=C2_CARD_2_SOURCE_VINTAGE,
        citation_id=CITE_C2_CARD_2,
        caveat_id=CAVEAT_C2_CARD_2,
    ),
    SeriesBinding(
        card=3,
        series_id=SERIES_SRS_BULLETIN_2024,
        name=(
            "Sample Registration System (SRS) Bulletin — estimated Birth Rate, "
            "Death Rate, Natural Growth Rate and Infant Mortality Rate"
        ),
        producer=ORGI_VSD,
        producer_slug=PRODUCER_SLUG_ORGI,
        next_release="unknown",
        geography_frame_id=C2_FRAME_C_ID,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2024,
        source_vintage=C2_CARD_3_SOURCE_VINTAGE,
        citation_id=CITE_C2_CARD_3,
        caveat_id=CAVEAT_C2_CARD_3,
    ),
    SeriesBinding(
        card=4,
        series_id=SERIES_SRS_STATISTICAL_REPORT_2024,
        name=(
            "Sample Registration System (SRS) Statistical Report 2024 — "
            "fertility and mortality indicators as published "
            "(including Crude Birth Rate and Total Fertility Rate)"
        ),
        producer=ORGI,
        producer_slug=PRODUCER_SLUG_ORGI,
        next_release="unknown",
        geography_frame_id=C2_FRAME_D_ID,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2024,
        source_vintage=C2_CARD_4_SOURCE_VINTAGE,
        citation_id=CITE_C2_CARD_4,
        caveat_id=CAVEAT_C2_CARD_4,
    ),
    SeriesBinding(
        card=5,
        series_id=SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
        name=(
            "Census of India 2011 — Population Projections for India and States "
            "2011–2036 (projections, not a census)"
        ),
        producer=NCP_MOHFW,
        producer_slug=PRODUCER_SLUG_NCP_MOHFW,
        next_release="unknown",
        geography_frame_id=C2_FRAME_E_ID,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2019,
        source_vintage=C2_CARD_5_SOURCE_VINTAGE,
        citation_id=CITE_C2_CARD_5,
        caveat_id=CAVEAT_C2_CARD_5,
    ),
)

C2_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C2_SERIES)

C2_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C2_SERIES
}

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


C3_SERIES: tuple[SeriesBinding, ...] = (
    SeriesBinding(
        card=1,
        series_id=SERIES_BUDGET_2026_27_TAX_REVENUE,
        name="Receipt Budget, 2026-2027 — I. Tax Revenue (major heads as published)",
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_1,
        caveat_id=CAVEAT_C3_CARD_1,
    ),
    SeriesBinding(
        card=2,
        series_id=SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
        name="Receipt Budget, 2026-2027 — II. Non-Tax Revenue",
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_2,
        caveat_id=CAVEAT_C3_CARD_2,
    ),
    SeriesBinding(
        card=3,
        series_id=SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
        name=(
            "Receipt Budget, 2026-2027 — III. Capital Receipts "
            "(Non-Debt Receipts and Debt Receipts / Borrowings as printed)"
        ),
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_3,
        caveat_id=CAVEAT_C3_CARD_3,
    ),
    SeriesBinding(
        card=4,
        series_id=SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS,
        name="Receipt Budget, 2026-2027 — Annex-1 Trends in Receipts",
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_4,
        caveat_id=CAVEAT_C3_CARD_4,
    ),
    SeriesBinding(
        card=5,
        series_id=SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
        name="Expenditure Profile 2026-2027 — Statement 1 Summary of Expenditure",
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_5,
        caveat_id=CAVEAT_C3_CARD_5,
    ),
    SeriesBinding(
        card=6,
        series_id=SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
        name=(
            "Budget at a Glance 2026-2027 — Deficit Statistics "
            "(Fiscal Deficit, Revenue Deficit, Effective Revenue Deficit, "
            "Primary Deficit, and Sources of Financing Fiscal Deficit)"
        ),
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_6,
        caveat_id=CAVEAT_C3_CARD_6,
    ),
    SeriesBinding(
        card=7,
        series_id=SERIES_BUDGET_2026_27_LIABILITIES,
        name=(
            "Receipt Budget, 2026-2027 — Part B: 1 (i) Statement of "
            "Liabilities of the Central Government"
        ),
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_7,
        caveat_id=CAVEAT_C3_CARD_7,
    ),
    SeriesBinding(
        card=8,
        series_id=SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
        name=(
            "Statements of Fiscal Policy as required under the Fiscal "
            "Responsibility and Budget Management Act, 2003 (Budget 2026-2027)"
        ),
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_8,
        caveat_id=CAVEAT_C3_CARD_8,
    ),
    SeriesBinding(
        card=9,
        series_id=SERIES_BUDGET_2026_27_AFS,
        name="Annual Financial Statement of the Central Government for 2026-2027",
        producer=MOF_BUDGET,
        producer_slug=PRODUCER_SLUG_MOF_BUDGET,
        next_release="unknown",
        geography_frame_id=C3_FRAME_A_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_BUDGET_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_9,
        caveat_id=CAVEAT_C3_CARD_9,
    ),
    SeriesBinding(
        card=10,
        series_id=SERIES_CGA_MONTHLY_GLANCE_2026_07,
        name=(
            "Union Government Accounts at a Glance as at the end of July 2026 "
            "(Monthly Accounts)"
        ),
        producer=CGA,
        producer_slug=PRODUCER_SLUG_CGA,
        next_release="unknown",
        geography_frame_id=C3_FRAME_B_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
        source_vintage=C3_CGA_MONTHLY_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_10,
        caveat_id=CAVEAT_C3_CARD_10,
    ),
    SeriesBinding(
        card=11,
        series_id=SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
        name=(
            "Finance Accounts, Union Government, 2024-2025 — No. 1 Summary of "
            "Transactions (receipts and disbursements, Actuals)"
        ),
        producer=CGA,
        producer_slug=PRODUCER_SLUG_CGA,
        next_release="unknown",
        geography_frame_id=C3_FRAME_C_ID,
        geography_vintage=C3_GEOGRAPHY_VINTAGE_2024,
        source_vintage=C3_CGA_FA_SOURCE_VINTAGE,
        citation_id=CITE_C3_CARD_11,
        caveat_id=CAVEAT_C3_CARD_11,
    ),
)

C3_SERIES_IDS: tuple[str, ...] = tuple(binding.series_id for binding in C3_SERIES)

C3_SERIES_BY_ID: dict[str, SeriesBinding] = {
    binding.series_id: binding for binding in C3_SERIES
}

# Card 8 FRBM statutory packet: listed, cited, unknown / not a table.
C3_NAMED_HOLE_SERIES_IDS: tuple[str, ...] = (SERIES_BUDGET_2026_27_FRBM_STATEMENTS,)
C3_LINEAGE_REQUIRED_SERIES_IDS: tuple[str, ...] = tuple(
    series_id
    for series_id in C3_SERIES_IDS
    if series_id not in C3_NAMED_HOLE_SERIES_IDS
)
NAMED_HOLE_SERIES_IDS: frozenset[str] = frozenset(C3_NAMED_HOLE_SERIES_IDS)
NAMED_HOLE_CITATION_IDS: frozenset[str] = frozenset(
    C3_SERIES_BY_ID[series_id].citation_id for series_id in C3_NAMED_HOLE_SERIES_IDS
)


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


def lineage_blocks_completeness(series_id: str, lineage_ok: YesNo) -> bool:
    """Named holes may be lineage_ok: no on a complete vintage. Other series may not."""

    if lineage_ok is YesNo.yes:
        return False
    return series_id not in NAMED_HOLE_SERIES_IDS


def lineage_record_blocks_completeness(record: LineageRecord) -> bool:
    if record.lineage_ok is YesNo.yes:
        return False
    return record.citation_id not in NAMED_HOLE_CITATION_IDS


def scheduled_series_on(day: date) -> tuple[SeriesBinding, ...]:
    """Schedule follows each series' next_release, not a hidden global clock."""

    return tuple(
        binding
        for binding in C1_SERIES
        if binding.next_release != "unknown" and binding.next_release == day
    )
