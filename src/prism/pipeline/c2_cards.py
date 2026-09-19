"""C2 citation cards, caveat notes, and geography frames — attached, not rewritten."""

from __future__ import annotations

import re
from datetime import date

from prism.ingest.c2 import (
    A02_XLS_URL,
    NCP_TABLE8_URL,
    PCA_URL,
    SRS_BULLETIN_URL,
    SRS_STAT_URL,
)
from prism.refresh import (
    C2_FRAME_A_ID,
    C2_FRAME_B_ID,
    C2_FRAME_C_ID,
    C2_FRAME_D_ID,
    C2_FRAME_E_ID,
    C2_GEOGRAPHY_VINTAGE_2011,
    C2_GEOGRAPHY_VINTAGE_2019,
    C2_GEOGRAPHY_VINTAGE_2024,
    C2_SERIES_BY_ID,
    CAVEAT_C2_CARD_1,
    CAVEAT_C2_CARD_2,
    CAVEAT_C2_CARD_3,
    CAVEAT_C2_CARD_4,
    CAVEAT_C2_CARD_5,
    CITE_C2_CARD_1,
    CITE_C2_CARD_2,
    CITE_C2_CARD_3,
    CITE_C2_CARD_4,
    CITE_C2_CARD_5,
    NCP_LICENCE,
    NCP_MOHFW,
    ORGI,
    ORGI_LICENCE,
    ORGI_VSD,
    SERIES_CENSUS_2011_A02_DECADAL,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
    SERIES_SRS_BULLETIN_2024,
    SERIES_SRS_STATISTICAL_REPORT_2024,
)
from prism.schema import (
    CaveatNote,
    Citation,
    CodeSystem,
    GeographyUnit,
    GeographyVintage,
)

_SLUG = re.compile(r"[^a-z0-9]+")
SRS_RELEASE = date(2026, 5, 1)
NCP_RELEASE = date(2019, 11, 1)

FRAME_A_UNITS: tuple[tuple[str, str], ...] = (
    ("00", "India"),
    ("01", "JAMMU & KASHMIR"),
    ("02", "HIMACHAL PRADESH"),
    ("03", "PUNJAB"),
    ("04", "CHANDIGARH"),
    ("05", "UTTARAKHAND"),
    ("06", "HARYANA"),
    ("07", "NCT OF DELHI"),
    ("08", "RAJASTHAN"),
    ("09", "UTTAR PRADESH"),
    ("10", "BIHAR"),
    ("11", "SIKKIM"),
    ("12", "ARUNACHAL PRADESH"),
    ("13", "NAGALAND"),
    ("14", "MANIPUR"),
    ("15", "MIZORAM"),
    ("16", "TRIPURA"),
    ("17", "MEGHALAYA"),
    ("18", "ASSAM"),
    ("19", "WEST BENGAL"),
    ("20", "JHARKHAND"),
    ("21", "ODISHA"),
    ("22", "CHHATTISGARH"),
    ("23", "MADHYA PRADESH"),
    ("24", "GUJARAT"),
    ("25", "DAMAN & DIU"),
    ("26", "DADRA & NAGAR HAVELI"),
    ("27", "MAHARASHTRA"),
    ("28", "ANDHRA PRADESH"),
    ("29", "KARNATAKA"),
    ("30", "GOA"),
    ("31", "LAKSHADWEEP"),
    ("32", "KERALA"),
    ("33", "TAMIL NADU"),
    ("34", "PUDUCHERRY"),
    ("35", "ANDAMAN & NICOBAR ISLANDS"),
)
FRAME_B_UNITS: tuple[tuple[str, str], ...] = (
    ("00", "INDIA"),
    ("01", "Jammu & Kashmir"),
    ("02", "Himachal Pradesh"),
    ("03", "Punjab"),
    ("04", "Chandigarh"),
    ("05", "Uttarakhand"),
    ("06", "Haryana"),
    ("07", "NCT OF Delhi"),
    ("08", "Rajasthan"),
    ("09", "Uttar Pradesh"),
    ("10", "Bihar"),
    ("11", "Sikkim"),
    ("12", "Arunachal Pradesh *"),
    ("13", "Nagaland   ^"),
    ("14", "Manipur"),
    ("15", "Mizoram"),
    ("16", "Tripura"),
    ("17", "Meghalaya"),
    ("18", "Assam"),
    ("19", "West Bengal"),
    ("20", "Jharkhand"),
    ("21", "Odisha"),
    ("22", "Chhattisgarh"),
    ("23", "Madhya Pradesh   $$"),
    ("24", "Gujarat"),
    ("25", "Daman & Diu"),
    ("26", "Dadra & Nagar Haveli"),
    ("27", "Maharashtra  ##"),
    ("28", "Andhra Pradesh @@"),
    ("29", "Karnataka"),
    ("30", "Goa"),
    ("31", "Lakshadweep"),
    ("32", "Kerala"),
    ("33", "Tamil Nadu"),
    ("34", "Puducherry"),
    ("35", "Andaman & Nicobar Islands"),
)
FRAME_C_NAMES: tuple[str, ...] = (
    "India",
    "1. Andhra Pradesh",
    "2. Assam",
    "3. Bihar",
    "4. Chhattisgarh",
    "5. NCT of Delhi",
    "6. Gujarat",
    "7. Haryana",
    "8. Jammu & Kashmir",
    "9. Jharkhand",
    "10. Karnataka",
    "11. Kerala",
    "12. Madhya Pradesh",
    "13. Maharashtra",
    "14. Odisha",
    "15. Punjab",
    "16. Rajasthan",
    "17. Tamil Nadu",
    "18. Telangana",
    "19. Uttar Pradesh",
    "20. Uttarakhand",
    "21. West Bengal",
    "1. Arunachal Pradesh",
    "2. Goa",
    "3. Himachal Pradesh",
    "4. Manipur*",
    "5. Meghalaya",
    "6. Mizoram",
    "7. Nagaland",
    "8. Sikkim",
    "9. Tripura",
    "1. Andaman & Nicobar Islands",
    "2. Chandigarh",
    "3. Dadra & Nagar Haveli and Daman & Diu",
    "4. Ladakh",
    "5. Lakshadweep",
    "6. Puducherry",
)
FRAME_D_NAMES: tuple[str, ...] = (
    "India",
    "Andhra Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Delhi",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu & Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Tamil Nadu",
    "Telangana",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
)
FRAME_E_NAMES: tuple[str, ...] = (
    "INDIA",
    "JAMMU & KASHMIR*(UT)",
    "HIMACHAL PRADESH",
    "PUNJAB",
    "CHANDIGARH*",
    "UTTARAKHAND",
    "HARYANA",
    "NCT OF DELHI*",
    "RAJASTHAN",
    "UTTAR PRADESH",
    "BIHAR",
    "SIKKIM",
    "ARUNACHAL PRADESH",
    "NAGALAND",
    "MANIPUR",
    "MIZORAM",
    "TRIPURA",
    "MEGHALAYA",
    "ASSAM",
    "WEST BENGAL",
    "JHARKHAND",
    "ODISHA",
    "CHHATTISGARH",
    "MADHYA PRADESH",
    "GUJARAT",
    "DAMAN & DIU*",
    "DADRA & NAGAR",
    "MAHARASHTRA",
    "ANDHRA PRADESH",
    "KARNATAKA",
    "GOA",
    "LAKSHADWEEP*",
    "KERALA",
    "TAMIL NADU",
    "PUDUCHERRY*",
    "ANDAMAN & NICOBAR",
    "TELANGANA",
    "LADAKH*",
)

CENSUS_2011_MISSING: tuple[str, ...] = (
    "Telangana as a STATE row (not on this file; 2014 split is after this vintage)",
    "Ladakh as a UT row (not on this file)",
    "districts and below (parked; do not pull, do not recode)",
    "today’s merged UT Dadra and Nagar Haveli and Daman and Diu as one row",
)
CENSUS_2011_BREAKS = (
    "2011 Census map. Do not recode 01 / 28 / 25+26 onto Frame C or Frame E. "
    "Do not spelling-merge Frame A names with Frame B. Crosswalk: none."
)


def _slug(text: str) -> str:
    ascii_only = text.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG.sub("-", ascii_only.lower()).strip("-")
    if slug == "":
        raise ValueError(f"geography name has no slug: {text!r}")
    return slug[:80]


def _census_frame(
    *,
    frame_id: str,
    units: tuple[tuple[str, str], ...],
    missing: tuple[str, ...],
    breaks: str,
) -> GeographyVintage:
    return GeographyVintage(
        frame_id=frame_id,
        geography_vintage=C2_GEOGRAPHY_VINTAGE_2011,
        code_system=CodeSystem.census,
        frame="Union | state | UT",
        units_included=tuple(
            GeographyUnit(
                code=code, name_en=name, geography_vintage=C2_GEOGRAPHY_VINTAGE_2011
            )
            for code, name in units
        ),
        units_missing=missing,
        breaks=breaks,
        crosswalk="none",
    )


def _printed_frame(
    *,
    frame_id: str,
    geography_vintage: str,
    names: tuple[str, ...],
    missing: tuple[str, ...],
    breaks: str,
) -> GeographyVintage:
    return GeographyVintage(
        frame_id=frame_id,
        geography_vintage=geography_vintage,
        code_system=CodeSystem.none,
        frame="Union | state | UT",
        units_included=tuple(
            GeographyUnit(
                code=_slug(name),
                name_en=name,
                geography_vintage=geography_vintage,
            )
            for name in names
        ),
        units_missing=missing,
        breaks=breaks,
        crosswalk="none",
    )


FRAME_A_GEOGRAPHY = _census_frame(
    frame_id=C2_FRAME_A_ID,
    units=FRAME_A_UNITS,
    missing=CENSUS_2011_MISSING,
    breaks=CENSUS_2011_BREAKS,
)
FRAME_B_GEOGRAPHY = _census_frame(
    frame_id=C2_FRAME_B_ID,
    units=FRAME_B_UNITS,
    missing=CENSUS_2011_MISSING
    + ("some early census years are N.A. on included units — missing observations",),
    breaks=CENSUS_2011_BREAKS
    + " Keep footnote marks on Frame B names; do not strip them to join Frame A.",
)
FRAME_C_GEOGRAPHY = _printed_frame(
    frame_id=C2_FRAME_C_ID,
    geography_vintage=C2_GEOGRAPHY_VINTAGE_2024,
    names=FRAME_C_NAMES,
    missing=(
        "districts and below (parked)",
        (
            "2011-only labels: undivided Andhra Pradesh; undivided Jammu & Kashmir state; "
            "separate Daman & Diu; separate Dadra & Nagar Haveli"
        ),
    ),
    breaks=(
        "2024 SRS Table 1 stubs as printed, including numbering. "
        "Do not recode Frame A/B codes onto these rows. Manipur* is one unit."
    ),
)
FRAME_D_GEOGRAPHY = _printed_frame(
    frame_id=C2_FRAME_D_ID,
    geography_vintage=C2_GEOGRAPHY_VINTAGE_2024,
    names=FRAME_D_NAMES,
    missing=(
        (
            "Frame C Smaller States not printed on Table 3 (except Himachal Pradesh, "
            "which this table does print)"
        ),
        "Frame C Union Territories (including Ladakh and merged DNH–DD)",
        "districts; NSS Natural Division rows (parked)",
    ),
    breaks=(
        "Detailed Table 3 geography as printed (Delhi, not NCT of Delhi). "
        "Do not fill missing UTs from the Bulletin. Crosswalk: none."
    ),
)
FRAME_E_GEOGRAPHY = _printed_frame(
    frame_id=C2_FRAME_E_ID,
    geography_vintage=C2_GEOGRAPHY_VINTAGE_2019,
    names=FRAME_E_NAMES,
    missing=(
        "districts (not in Table 8)",
        "any unit Table 8 does not print — labels are truncated as in the PDF words",
    ),
    breaks=(
        "November 2019 projection map, Census 2011 base. "
        "JAMMU & KASHMIR*(UT) and LADAKH* are printed Table 8 units. "
        "Do not recode onto Frame A or Frame C."
    ),
)

C2_GEOGRAPHIES: dict[str, GeographyVintage] = {
    SERIES_CENSUS_2011_PCA_SD: FRAME_A_GEOGRAPHY,
    SERIES_CENSUS_2011_A02_DECADAL: FRAME_B_GEOGRAPHY,
    SERIES_SRS_BULLETIN_2024: FRAME_C_GEOGRAPHY,
    SERIES_SRS_STATISTICAL_REPORT_2024: FRAME_D_GEOGRAPHY,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: FRAME_E_GEOGRAPHY,
}

C2_CITATIONS: dict[str, Citation] = {
    SERIES_CENSUS_2011_PCA_SD: Citation(
        citation_id=CITE_C2_CARD_1,
        producer=ORGI,
        series=C2_SERIES_BY_ID[SERIES_CENSUS_2011_PCA_SD].name,
        id=(
            "NADA catalog 6191; Reference ID PC11_PCA-SD; file "
            "DDW_PCA0000_2011_Indiastatedist.xlsx sheet Sheet1. Population of "
            "record: TOT_P, TOT_M, TOT_F for Level = India or STATE (not DISTRICT)."
        ),
        reference_period="2011-03-01",
        release_date="unknown",
        url=PCA_URL,
        geography_as_published=(
            "India and States/UTs as labelled in Name where Level = India or STATE; "
            "TRU = Total / Rural / Urban. DISTRICT rows parked."
        ),
        frequency="decennial census",
        licence=ORGI_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "This is a 1 March 2011 count, about fifteen years behind a 2026 reader. "
            "Not a current headcount. Districts parked."
        ),
    ),
    SERIES_CENSUS_2011_A02_DECADAL: Citation(
        citation_id=CITE_C2_CARD_2,
        producer=ORGI,
        series=C2_SERIES_BY_ID[SERIES_CENSUS_2011_A02_DECADAL].name,
        id=(
            "NADA catalog 43333; file 00 A 2-India.xls sheet A-2. India/State/UT "
            "by Census Year; District Code 000. Companion PDF is not the table of record."
        ),
        reference_period="1901-2011",
        release_date="unknown",
        url=A02_XLS_URL,
        geography_as_published=(
            "INDIA and States/UTs as printed (District Code 000). Names keep footnote marks."
        ),
        frequency="decennial",
        licence=ORGI_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "Historical census counts through 2011. N.A. is not zero. Not an SRS rate "
            "and not a 2026 headcount."
        ),
    ),
    SERIES_SRS_BULLETIN_2024: Citation(
        citation_id=CITE_C2_CARD_3,
        producer=ORGI_VSD,
        series=C2_SERIES_BY_ID[SERIES_SRS_BULLETIN_2024].name,
        id=(
            "NADA catalog 47150; SRS_Bulletin_2024_Vol_59_No_1.pdf Table 1: Birth Rate, "
            "Death Rate, Natural Growth Rate and Infant Mortality Rate, Total/Rural/Urban."
        ),
        reference_period="2024",
        release_date=SRS_RELEASE,
        url=SRS_BULLETIN_URL,
        geography_as_published=(
            "India; Bigger States/UTs; Smaller States; Union Territories as printed in "
            "Table 1 (including Telangana, Ladakh, and merged DNH and Daman & Diu)."
        ),
        frequency="annual bulletin for reference year 2024",
        licence=ORGI_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "SRS sample rates for calendar year 2024, not a census stock. No TFR on this card."
        ),
    ),
    SERIES_SRS_STATISTICAL_REPORT_2024: Citation(
        citation_id=CITE_C2_CARD_4,
        producer=ORGI,
        series=C2_SERIES_BY_ID[SERIES_SRS_STATISTICAL_REPORT_2024].name,
        id=(
            "NADA catalog 47152; SRS_STAT_2024.pdf Detailed Table 3 Fertility Indicators, "
            "2024 (including Total Fertility Rate)."
        ),
        reference_period="2024",
        release_date=SRS_RELEASE,
        url=SRS_STAT_URL,
        geography_as_published=(
            "India and bigger States/UTs as printed on Table 3 (Delhi as printed). "
            "Smaller States/UTs missing except where this table prints them."
        ),
        frequency="annual report",
        licence=ORGI_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "SRS fertility including TFR for 2024. Not a census. Do not fill missing "
            "UTs from the Bulletin."
        ),
    ),
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: Citation(
        citation_id=CITE_C2_CARD_5,
        producer=NCP_MOHFW,
        series=C2_SERIES_BY_ID[SERIES_NCP_PROJECTIONS_2011_2036_TABLE8].name,
        id=(
            "Report of the Technical Group on Population Projections, November 2019. "
            "TABLE-8 projected total population by sex as on 1st March 2011–2036, "
            "India, States and Union Territories* ('000). Fetch host nhm.gov.in."
        ),
        reference_period="2011-2036-03-01",
        release_date=NCP_RELEASE,
        url=NCP_TABLE8_URL,
        geography_as_published=(
            "Table 8 stubs as printed, including JAMMU & KASHMIR*(UT), TELANGANA, LADAKH*."
        ),
        frequency="one-off projection report",
        licence=NCP_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "Projection in thousands on 1st March, not a census. A 2026 cell is still "
            "the 2019 report."
        ),
    ),
}

C2_CAVEATS: dict[str, CaveatNote] = {
    SERIES_CENSUS_2011_PCA_SD: CaveatNote(
        caveat_id=CAVEAT_C2_CARD_1,
        concept=(
            "Census of India 2011 PCA SD headcount as published for Level = India or "
            "STATE: persons (TOT_P), males (TOT_M), females (TOT_F), and households "
            "(No_HH) by TRU = Total / Rural / Urban. Census stock on Census day, not "
            "an SRS rate and not a projection."
        ),
        unit="Persons (and households where the column is No_HH). Not thousands. Not a rate.",
        population=(
            "Everyone enumerated in Census 2011 on published India and STATE rows. "
            "Not DISTRICT rows. Not NPR, electoral rolls, or a 2026 usual-resident count."
        ),
        reference_period="00:00 hours, 1 March 2011. Not the NADA catalog date.",
        producer_definition=(
            "TOT_P, TOT_M, TOT_F for Level = India or STATE; TRU = Total / Rural / Urban "
            "(ORGI, Census of India 2011 PCA SD, NADA catalog 6191). India (00) is the "
            "published national total, not a roll-up of STATE rows."
        ),
        comparable_from=(
            "This card is one census vintage. Compare Frame A units only on the 2011 map."
        ),
        breaks=(
            "No Telangana STATE row; no Ladakh UT row; DAMAN & DIU (25) and DADRA & "
            "NAGAR HAVELI (26) are separate. Do not recode onto Frame C or Frame E."
        ),
        lags=(
            "About fifteen years behind a 2026 reader. next_release unknown — delayed. "
            "Census 2021 totals were not published. Census 2027 houselisting is not a count."
        ),
        disagrees_with=(
            "Card 2 A-02 (different table and printed names). Cards 3–4 SRS 2024 rates. "
            "Card 5 Table 8 projections in thousands. UN / World Bank modelled stocks "
            "(charter-out)."
        ),
        do_not=(
            "Do not present TOT_P as how many people live in India now. Do not hide "
            "1 March 2011. Do not chart DISTRICT rows. Do not add SRS rates to invent a "
            "2024 headcount. Do not splice Card 5 onto this line. Do not rank."
        ),
    ),
    SERIES_CENSUS_2011_A02_DECADAL: CaveatNote(
        caveat_id=CAVEAT_C2_CARD_2,
        concept=(
            "Census of India 2011 Table A-02: population by census year 1901–2011 and "
            "variation since the preceding census for INDIA and States/UTs as printed."
        ),
        unit=(
            "Persons, and producer-printed decadal variation (absolute and percentage). "
            "N.A. cells are not zero."
        ),
        population=(
            "Census enumerated population on District Code 000 India/State/UT rows. "
            "Not districts. Missing early years are missing observations, not dropped States."
        ),
        reference_period="Census years on the row (1901 through 2011). 2011 is the last year.",
        producer_definition=(
            "Table A-2 as printed; State rows use District Code 000 (ORGI, NADA catalog "
            "43333, 00 A 2-India.xls). Footnote marks stay on the printed name."
        ),
        comparable_from=(
            "Where the producer prints a number for that census year on that unit. "
            "Pipeline keys State Code, not spelling versus Frame A."
        ),
        breaks=(
            "Same 2011 map holes as Frame A. Do not stitch Card 5 projections onto this "
            "1901–2011 line as one census run."
        ),
        lags="Same Census hole as Card 1: no published census year after 2011 on these cards.",
        disagrees_with="Card 1 PCA. Cards 3–4 SRS 2024. Card 5 projections. CRS (rejected).",
        do_not=(
            "Do not extend the line past 2011 with Table 8 or SRS. Do not chart N.A. as 0. "
            "Do not spelling-merge Frame B names with Frame A. Do not call 2011 current."
        ),
    ),
    SERIES_SRS_BULLETIN_2024: CaveatNote(
        caveat_id=CAVEAT_C2_CARD_3,
        concept=(
            "SRS estimated Birth Rate, Death Rate, Natural Growth Rate, and Infant "
            "Mortality Rate for calendar year 2024, India and States/UTs, Total / Rural / "
            "Urban. Survey estimates, not a census. No TFR on this bulletin."
        ),
        unit="Rates as labelled on Table 1. Not persons. Not a stock.",
        population=(
            "SRS sample for India, Bigger States/UTs, Smaller States, and Union Territories "
            "as printed. Manipur* is one unit (130 SRS units footnote)."
        ),
        reference_period="Calendar year 2024. Not the May 2026 cover.",
        producer_definition=(
            "SRS Bulletin Volume 59 No. 1, May 2026, Table 1 (ORGI Vital Statistics "
            "Division, NADA catalog 47150)."
        ),
        comparable_from="This 2024 bulletin issue. Do not join a 2024 stub to a 2011 Census code.",
        breaks=(
            "2024 map vs Frames A/B: Telangana and Andhra Pradesh distinct; Jammu & Kashmir "
            "and Ladakh distinct; DNH and Daman & Diu merged."
        ),
        lags="2024 rates released May 2026. next_release unknown.",
        disagrees_with="Cards 1–2 census stock. Card 4 (TFR; narrower geography). Card 5 projections.",
        do_not=(
            "Do not add Card 1 population to these rates to invent a 2024 headcount. "
            "Do not use this card for TFR. Do not drop the Manipur* footnote. Do not rank."
        ),
    ),
    SERIES_SRS_STATISTICAL_REPORT_2024: CaveatNote(
        caveat_id=CAVEAT_C2_CARD_4,
        concept=(
            "SRS Statistical Report 2024 fertility indicators as published, including "
            "Crude Birth Rate and Total Fertility Rate. Same SRS family as Card 3, not a "
            "substitute census."
        ),
        unit="Indicators as labelled in Detailed Table 3. Not Census persons. Not Card 5 thousands.",
        population=(
            "India and bigger States/UTs as printed on Table 3. Missing: most Frame C "
            "Smaller States and all Frame C Union Territories. Districts and NSS Natural "
            "Divisions parked."
        ),
        reference_period="Calendar year 2024. Not PDF CreationDate / NADA 20 May 2026.",
        producer_definition=(
            "SRS Statistical Report 2024 Detailed Table 3 Fertility Indicators, 2024 "
            "(ORGI, NADA catalog 47152)."
        ),
        comparable_from=(
            "This 2024 report, Frame D units only. An India TFR must still name missing "
            "smaller States, UTs, and districts."
        ),
        breaks="Narrower geography than Card 3. Do not fill holes from the Bulletin.",
        lags="Same May 2026 vintage as Card 3. next_release unknown.",
        disagrees_with="Card 3 Bulletin. Cards 1–2 census. Card 5 projections. NFHS (not on these cards).",
        do_not=(
            "Do not present TFR as a headcount or as India today. Do not paste Smaller "
            "States / UT rates from the Bulletin into this report. Do not rank."
        ),
    ),
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: CaveatNote(
        caveat_id=CAVEAT_C2_CARD_5,
        concept=(
            "Projected total population by sex as on 1st March, 2011–2036, TABLE-8 of "
            "the Technical Group report. A projection, not a census."
        ),
        unit="Thousands ('000) as printed. Still not Census PCA persons.",
        population="India, States and UTs as labelled on TABLE-8. Not districts.",
        reference_period="Projected years 2011–2036 as on 1st March. Not Table 11 (1st July).",
        producer_definition=(
            "TABLE-8 Projected Total Population by Sex as on 1st March 2011–2036 "
            "(NCP / MoHFW, November 2019). Hosted PDF from nhm.gov.in."
        ),
        comparable_from=(
            "Table 8 columns inside this 2019 report. The 2011 column is a smoothed "
            "projected base, not Card 1 TOT_P."
        ),
        breaks=(
            "Projection map as of November 2019. Jammu & Kashmir*(UT) and Ladakh* are "
            "printed Table 8 units. No successor Technical Group report on these cards."
        ),
        lags=(
            "Report dated November 2019. A 2026 Table-8 cell is still a 2019 projection, "
            "not a new enumeration."
        ),
        disagrees_with="Card 1 PCA. Card 2 A-02. Cards 3–4 SRS rates. TABLE-11 in the same PDF. UN WPP (charter-out).",
        do_not=(
            "Do not present a Table-8 figure as India has X people without naming Table 8, "
            "thousands, 1st March, and that it is a projection. Do not merge Table 8 and "
            "Table 11. Do not paper the missing Census 2021/2027."
        ),
    ),
}
