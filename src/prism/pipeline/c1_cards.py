"""C1 citation cards, caveat notes, and geography frames — attached, not rewritten."""

from __future__ import annotations

from datetime import date

from prism.refresh import (
    C1_FRAME_A_ID,
    C1_FRAME_B_ID,
    C1_GEOGRAPHY_VINTAGE,
    C1_LICENCE,
    C1_SERIES_BY_ID,
    CARDS_1_3_NEXT_RELEASE,
    CAVEAT_C1_CARD_1,
    CAVEAT_C1_CARD_2,
    CAVEAT_C1_CARD_3,
    CAVEAT_C1_CARD_4,
    CITE_C1_CARD_1,
    CITE_C1_CARD_2,
    CITE_C1_CARD_3,
    CITE_C1_CARD_4,
    MOSPI_NSO_PSD,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import (
    CaveatNote,
    Citation,
    CodeSystem,
    GeographyUnit,
    GeographyVintage,
)

MONTHLY_URL = (
    "https://www.mospi.gov.in/uploads/documents/productChartTable/"
    "1789491098345-Data_August_CPI_2026_14092026.xlsx"
)
BACK_SERIES_URL = (
    "https://www.mospi.gov.in/uploads/documents/CPI/"
    "CPI_2024-Back-Series-Index-Inflation.xlsx"
)

FRAME_A_UNITS: tuple[tuple[str, str], ...] = (
    ("00", "All India"),
    ("01", "Jammu And Kashmir"),
    ("02", "Himachal Pradesh"),
    ("03", "Punjab"),
    ("04", "Chandigarh"),
    ("05", "Uttarakhand"),
    ("06", "Haryana"),
    ("07", "NCT of Delhi"),
    ("08", "Rajasthan"),
    ("09", "Uttar Pradesh"),
    ("10", "Bihar"),
    ("11", "Sikkim"),
    ("12", "Arunachal Pradesh"),
    ("13", "Nagaland"),
    ("14", "Manipur"),
    ("15", "Mizoram"),
    ("16", "Tripura"),
    ("17", "Meghalaya"),
    ("18", "Assam"),
    ("19", "West Bengal"),
    ("20", "Jharkhand"),
    ("21", "Odisha"),
    ("22", "Chhattisgarh"),
    ("23", "Madhya Pradesh"),
    ("24", "Gujarat"),
    ("25", "The Dadra And Nagar Haveli And Daman And Diu"),
    ("27", "Maharashtra"),
    ("28", "Andhra Pradesh"),
    ("29", "Karnataka"),
    ("30", "Goa"),
    ("31", "Lakshadweep"),
    ("32", "Kerala"),
    ("33", "Tamil Nadu"),
    ("34", "Puducherry"),
    ("35", "Andaman And Nicobar Islands"),
    ("36", "Telangana"),
    ("37", "Ladakh"),
)

FRAME_A_NAME_BY_CODE = {code: name for code, name in FRAME_A_UNITS}
FRAME_B_NAME_BY_CODE = {"00": "All India"}

FRAME_A_GEOGRAPHY = GeographyVintage(
    frame_id=C1_FRAME_A_ID,
    geography_vintage=C1_GEOGRAPHY_VINTAGE,
    code_system=CodeSystem.producer_specific,
    frame="Union | state | UT",
    units_included=tuple(
        GeographyUnit(code=code, name_en=name, geography_vintage=C1_GEOGRAPHY_VINTAGE)
        for code, name in FRAME_A_UNITS
    ),
    units_missing=(
        "districts and below (not in these artifacts; parked — do not pull, do not recode)",
        "city / centre geographies (charter-out; not this frame)",
        (
            "Chandigarh Rural: not a missing UT. Unit 04 Chandigarh is included. "
            "Workbook General: Urban and Combined rows only (no Rural row). "
            "Annexure-III prints Chandigarh* with Rural cells blank; footnote "
            "*: No rural market in Chandigarh. Combined equals Urban on that row. "
            "Do not recode; do not treat Combined as a missing unit."
        ),
        (
            "No current State or UT is absent from State Name "
            "(28 states + 8 UTs + All India = 37 labels)."
        ),
        "Code 26 is unused; it is not a missing published unit.",
    ),
    breaks=(
        "This Base 2024=100 map is post-reorganisation throughout the comparable "
        "run (January 2025 onward). Hits that already sit on the sheet as separate "
        "current units: 2014 Telangana (36) and Andhra Pradesh (28) are distinct; "
        "undivided Andhra Pradesh is not a unit here. 2019 Jammu And Kashmir (01) "
        "and Ladakh (37) are distinct UTs; undivided Jammu & Kashmir state is not "
        "a unit here. 2020 Dadra and Nagar Haveli and Daman and Diu are one UT "
        "(25); former separate UTs and census-style code 26 are not published. "
        "Do not recode 2012=100 (or earlier) geographies onto these rows. "
        "State/UT Combined is not comparable to a user average of districts: "
        "districts are not on the map. `00` All India is a published national "
        "unit, not a roll-up of State/UT Combined."
    ),
    crosswalk="none",
)

FRAME_B_GEOGRAPHY = GeographyVintage(
    frame_id=C1_FRAME_B_ID,
    geography_vintage=C1_GEOGRAPHY_VINTAGE,
    code_system=CodeSystem.producer_specific,
    frame="Union",
    units_included=(
        GeographyUnit(
            code="00", name_en="All India", geography_vintage=C1_GEOGRAPHY_VINTAGE
        ),
    ),
    units_missing=(
        (
            "all 36 States and Union Territories published on Frame A "
            "(Jammu And Kashmir through Ladakh / The Dadra And Nagar Haveli "
            "And Daman And Diu — none appear as rows in this file)"
        ),
        "districts and below (parked)",
        "city / centre geographies (charter-out; not this frame)",
    ),
    breaks=(
        "File does not carry a State/UT map, so Telangana, J&K reorganisation, "
        "Ladakh, and the DNH–DD merger do not appear as changing units here. "
        "Linked national All India only; do not treat this as a state-level "
        "historical map. Do not recode Frame A State/UT rows onto Card 4."
    ),
    crosswalk="none",
)

C1_CITATIONS: dict[str, Citation] = {
    SERIES_CPI_GENERAL_BASE_2024: Citation(
        citation_id=CITE_C1_CARD_1,
        producer=MOSPI_NSO_PSD,
        series=C1_SERIES_BY_ID[SERIES_CPI_GENERAL_BASE_2024].name,
        id=(
            "MoSPI product_id 9; latestRelease id 170 Press release of CPI for the "
            "month of August 2026; Documents id 315 CPI Data - August 2026 Based "
            "on Base Year 2024 file Data_August_CPI_2026_14092026.xlsx sheet "
            "General; companion Annex.xlsx sheet Annexure-III (State/UT wise "
            "general). Time series of record for Jan 2025–Dec 2025: "
            "CPI_2024-Jan2025-Dec2025.xlsx sheet General; for Jan 2026: "
            "CPI_2024-Jan2026.xlsx sheet General."
        ),
        reference_period="2026-08",
        release_date=date(2026, 9, 14),
        url=MONTHLY_URL,
        geography_as_published=(
            "All India and States/UTs as labelled in State Name "
            "(37 labels including All India); Sector = Rural / Urban / Combined "
            "as published. Not districts."
        ),
        frequency="monthly",
        licence=C1_LICENCE,
        next_release=CARDS_1_3_NEXT_RELEASE,
        caveat_one_line=(
            "Latest month is Provisional; Combined is a published sector, not a "
            "user merge. Chandigarh Rural is withheld (dash) in Annexure-III. "
            "Base-year break vs 2012=100. Districts are not in this file."
        ),
    ),
    SERIES_CPI_CFPI_BASE_2024: Citation(
        citation_id=CITE_C1_CARD_2,
        producer=MOSPI_NSO_PSD,
        series=C1_SERIES_BY_ID[SERIES_CPI_CFPI_BASE_2024].name,
        id=(
            "Same monthly workbook as Card 1, sheet Group, Group Name = Food / "
            "Group code 01.1; press note Key Statistics table CFPI; Annex.xlsx "
            "sheet Annexure-II row 01.1 Food. Time series: "
            "CPI_2024-Jan2025-Dec2025.xlsx and CPI_2024-Jan2026.xlsx sheet Group."
        ),
        reference_period="2026-08",
        release_date=date(2026, 9, 14),
        url=MONTHLY_URL,
        geography_as_published=(
            "All India and States/UTs as in State Name; Sector = Rural / Urban / "
            "Combined. Not districts."
        ),
        frequency="monthly",
        licence=C1_LICENCE,
        next_release=CARDS_1_3_NEXT_RELEASE,
        caveat_one_line=(
            "CFPI is not the same as Division Food and beverages (01), which also "
            "includes beverages and food-processing services. Use Group Food 01.1 "
            "/ the press CFPI table for the named food index. Latest month Provisional."
        ),
    ),
    SERIES_CPI_DIVISION_GROUP_BASE_2024: Citation(
        citation_id=CITE_C1_CARD_3,
        producer=MOSPI_NSO_PSD,
        series=C1_SERIES_BY_ID[SERIES_CPI_DIVISION_GROUP_BASE_2024].name,
        id=(
            "Same monthly workbook as Card 1, sheets Division and Group; press "
            "Annexure-I (division) and Annexure-II (group); Documents id 314 "
            "Annex.xlsx. Time series: CPI_2024-Jan2025-Dec2025.xlsx and "
            "CPI_2024-Jan2026.xlsx sheets Division and Group."
        ),
        reference_period="2026-08",
        release_date=date(2026, 9, 14),
        url=MONTHLY_URL,
        geography_as_published=(
            "All India and States/UTs as in State Name; Sector = Rural / Urban / "
            "Combined. Not districts. Not city/centre rankings."
        ),
        frequency="monthly",
        licence=C1_LICENCE,
        next_release=CARDS_1_3_NEXT_RELEASE,
        caveat_one_line=(
            "Division 01 is Food and beverages; food-only is Card 2. Item and "
            "Subclass sheets exist in the same workbook — do not use them to rank "
            "cities. Some item indices on eSankhyiki are thin-sample (press note "
            "warning); this slice uses Division/Group/General as published."
        ),
    ),
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024: Citation(
        citation_id=CITE_C1_CARD_4,
        producer=MOSPI_NSO_PSD,
        series=C1_SERIES_BY_ID[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024].name,
        id=(
            "Documents id 290; file CPI_2024-Back-Series-Index-Inflation.xlsx "
            "sheet Sheet1; columns Base Year, State code, State name, Sector, "
            "Year, Month, Group, Index, Inflation (%)"
        ),
        reference_period="2013-01 to 2024-12",
        release_date="unknown",
        url=BACK_SERIES_URL,
        geography_as_published=(
            "All India only in the opened rows (State name = All India, State "
            "code 00); Sector = Rural / Urban / Combined; Group = General"
        ),
        frequency="monthly",
        licence=C1_LICENCE,
        next_release="unknown",
        caveat_one_line=(
            "Linked / back-cast onto 2024=100 — not independently compiled "
            "2024-basket observations before the new series. Do not stitch this "
            "to the 2012=100 series as if they were one. All India only in this "
            "file; no State/UT rows in the previewed sheet. Inflation (%) is "
            "blank on early rows."
        ),
    ),
}

C1_CAVEATS: dict[str, CaveatNote] = {
    SERIES_CPI_GENERAL_BASE_2024: CaveatNote(
        caveat_id=CAVEAT_C1_CARD_1,
        concept=(
            "All-India and State/UT Consumer Price Index (CPI) General — the "
            "producer’s headline retail price index of selected goods and "
            "services, Base 2024=100. Published as three sectors: Rural, Urban, "
            "and Combined. Combined is a published sector in the same tables, "
            "not a user merge of Rural and Urban."
        ),
        unit=(
            "Index points (Base 2024=100) and, where the producer prints it, "
            "year-on-year inflation (%) — August 2026 over August 2025 in the "
            "latest press table. Status F/P as printed. Do not treat a blank "
            "inflation cell as 0."
        ),
        population=(
            "Prices from the NSO Field Operations Division collection: selected "
            "1407 urban markets (including online markets) and 1465 villages "
            "covering all States/UTs (August 2026 press note). Not a census of "
            "all transactions. Not districts. Not a city ranking of the "
            "1407/1465 collection points."
        ),
        reference_period=(
            "Calendar month named on the row (latest on these cards: August 2026 "
            "Provisional and July 2026 Final). Not the press date 14 September 2026."
        ),
        producer_definition=(
            "Year-on-year inflation rate based on All India Consumer Price Index "
            "(CPI) with base year 2024 for the month of August, 2026 over August, "
            "2025 is 4.82%(Provisional). Corresponding inflation rates for rural "
            "and urban are 5.23% and 4.31%, respectively. Same note prints CPI "
            "(General) Index and Inflation for Rural, Urban and Combined in one "
            "Key Statistics table (July 2026 Final beside August 2026 Provisional). "
            "Collection: selected 1407 urban markets and 1465 villages covering "
            "all States/UTs, weekly roster (NSO/MoSPI, Press Release of Consumer "
            "Price Index on Base 2024=100 for August, 2026, 14 September 2026). "
            "Annexure-III footnote: *: No rural market in Chandigarh. Rounding: "
            "Indices at all levels and inflation rates are compiled using the "
            "actual index values without rounding off. However, the indices "
            "published are rounded off to two decimal places."
        ),
        comparable_from=(
            "Independently compiled Base 2024=100 General index: January 2025 "
            "onward (time-series workbooks and Annexure-IV). Year-on-year "
            "inflation (%) on this base: January 2026 onward in Annexure-IV "
            "(Jan–Dec 2025 inflation cells are blank because there is no prior "
            "year on this base). Do not use Card 4 to fill those 2025 blanks."
        ),
        breaks=(
            "Base-year break versus CPI 2012=100 (and 2010=100 remnants): show a "
            "break, never a blended line. Linked back series (Card 4) is not this "
            "card. Sector Combined is not a geography break. Frame A already uses "
            "current units (Telangana 36 / Andhra Pradesh 28; Jammu And Kashmir "
            "01 / Ladakh 37; DNH&DD 25). Chandigarh (04) Rural is withheld (dash "
            "/ no Rural row); Combined equals Urban on that row — not a missing "
            "UT. Code 26 unused. `00` All India is a published national unit, "
            "not a roll-up of State/UT Combined."
        ),
        lags=(
            "August 2026 figures released 14 September 2026; next release 12 "
            "October 2026 (CPI for September 2026). Latest month is Provisional "
            "until the producer prints Final (here July 2026 Final sits beside "
            "August 2026 Provisional). Status P and F are different observations, "
            "not one smoothed number."
        ),
        disagrees_with=(
            "CPI Base 2012=100 (previous series; still appears on some product-9 "
            "files — not this line). National Metadata Structure PDF on the MoSPI "
            "site still describes older grouping (NSS 68th round weights / six "
            "groups) while live 2024=100 releases use COICOP 2018 — cite the live "
            "workbook, not the stale metadata PDF, as the grouping of record. Out "
            "of this slice but official and not the same number: WPI (DPIIT "
            "wholesale); Labour Bureau CPI-IW and CPI-AL/RL (different populations "
            "and baskets). Division 01 Food and beverages (Card 3) is not this "
            "General index. CFPI (Card 2) is not this General index. Pump prices "
            "(PPAC) are not this series (press note: petrol, diesel and LPG price "
            "reference is the 15th of the month inside the CPI collection — that "
            "is not a PPAC overlay)."
        ),
        do_not=(
            "Do not average Rural and Urban to invent Combined. Do not present "
            "`00` All India as the whole country (districts parked; Chandigarh "
            "Rural withheld; All India is not a sum of State/UT Combined). Do not "
            "recode State Codes. Do not join Frame A State/UT rows to Card 4 "
            "(Card 4 has none). Do not stitch 2012=100 onto this series. Do not "
            "chart a continuous line from Card 4 linked indexes into this compiled "
            "series as if they were one independently compiled run — state the "
            "break at January 2025. Do not chart blank inflation (%) as zero. Do "
            "not replace Provisional with Final or blend them. Do not rank "
            "States/UTs or cities; press top five States tables are not a series. "
            "Do not overlay petrol pump prices. Do not issue cheap/expensive or "
            "forecast copy. Do not recompute higher-level indexes from rounded "
            "published figures and treat the difference as a revision."
        ),
    ),
    SERIES_CPI_CFPI_BASE_2024: CaveatNote(
        caveat_id=CAVEAT_C1_CARD_2,
        concept=(
            "Consumer Food Price Index (CFPI): the producer’s named food price "
            "index, Base 2024=100, Rural / Urban / Combined. Same figures as CPI "
            "Group Food, Group code 01.1. Not Division 01 Food and beverages."
        ),
        unit=(
            "Index points (Base 2024=100) and year-on-year inflation (%) as "
            "printed. Blank inflation is not zero. Status Provisional / Final as "
            "printed."
        ),
        population=(
            "Same price-collection system as Card 1 (1407 urban markets including "
            "online; 1465 villages; all States/UTs). Food as Group 01.1, not every "
            "item a household buys."
        ),
        reference_period=(
            "Calendar month on the row (August 2026 Provisional and July 2026 "
            "Final on these cards). Not 14 September 2026."
        ),
        producer_definition=(
            "Year-on-year inflation rate based on All India Consumer Food Price "
            "Index (CFPI) for the month of August, 2026 over August, 2025 is "
            "5.95% (Provisional). Corresponding inflation rates for rural and "
            "urban are 6.13% and 5.64%, respectively. Key Statistics prints CFPI "
            "Index and Inflation beside CPI (General) (NSO/MoSPI press note, 14 "
            "September 2026). Annexure-II row Group code 01.1 Food Combined "
            "inflation 5.95% matches that CFPI figure. Annexure-I Division 01 "
            "Food and beverages Combined inflation is 5.66% — a different "
            "published number (Division 01 also includes Group 01.2 Beverages and "
            "Group 01.3 Services for processing primary goods for food)."
        ),
        comparable_from=(
            "Same as Card 1 for this base: Group 01.1 / CFPI index from January "
            "2025; year-on-year inflation on this base from January 2026 where "
            "the producer prints it. Card 4 has Group = General only — no CFPI "
            "back series in that file."
        ),
        breaks=(
            "Same base-year break versus 2012=100. Same Frame A geography notes "
            "as Card 1 (including Chandigarh Rural withheld). Do not treat "
            "Division 01 as a continuation of CFPI."
        ),
        lags=(
            "Same monthly calendar as Card 1 (August 2026 Provisional in the 14 "
            "September 2026 release; July 2026 Final in the same book)."
        ),
        disagrees_with=(
            "Division 01 Food and beverages (Card 3) — same producer, same month, "
            "different basket (food plus beverages and food-processing services). "
            "Headline CPI General (Card 1). CPI 2012=100 food groupings. WPI food "
            "articles (wholesale, different office). Labour Bureau food components "
            "of CPI-IW / CPI-AL/RL. Stale National Metadata Structure six-group "
            "description versus live COICOP 2018 Group 01.1."
        ),
        do_not=(
            "Do not chart Division 01 as food or as CFPI. Do not mix 01.1 with "
            "01.2 or 01.3 into a homemade food index. Do not use Card 4 for food. "
            "Do not rank states or cities by food inflation. Do not overlay "
            "tomato/onion item spikes as the food index (item tables are out of "
            "this slice; press also warns some item indices use thin samples). "
            "Same geography and status do-nots as Card 1: no All-India-as-whole-"
            "country, no Rural/Urban merge, no blank-as-zero, no Provisional/Final "
            "blend, no pump prices, no cheap/expensive, no forecast."
        ),
    ),
    SERIES_CPI_DIVISION_GROUP_BASE_2024: CaveatNote(
        caveat_id=CAVEAT_C1_CARD_3,
        concept=(
            "CPI Division indexes (COICOP 2018, 12 Divisions as named) and CPI "
            "Group indexes (43 Groups as named), Rural / Urban / Combined, Base "
            "2024=100. Headline General is Card 1. Food-only is Card 2 (Group "
            "01.1 / CFPI). Division 01 is Food and beverages."
        ),
        unit=(
            "Index points (Base 2024=100) and year-on-year inflation (%) as "
            "printed. Blank inflation is not zero. Status Provisional / Final as "
            "printed."
        ),
        population=(
            "Same collection system as Card 1. Each Division/Group is the "
            "producer’s COICOP 2018 aggregate, not a user basket."
        ),
        reference_period=(
            "Calendar month on the row (August 2026 Provisional and July 2026 "
            "Final on these cards). Not 14 September 2026."
        ),
        producer_definition=(
            "Annexure-I title: All India General (Rural, Urban and Combined) "
            "division wise indices and inflation for August, 2026 (Provisional); "
            "Division 01 Food and beverages is one row among twelve named "
            "divisions; a bottom All India row is General (Card 1), not Division "
            "01 (NSO/MoSPI press note, 14 September 2026). Annexure-II title: "
            "group wise indices; first row is 01.1 Food. Live 2024=100 grouping "
            "is COICOP 2018 (product-9 metadata and these annexes). Division names "
            "as printed for August 2026: Food and beverages; Paan, tobacco and "
            "intoxicants; Clothing and footwear; Housing, water, electricity, gas "
            "and other fuels; Furnishings, household equipment and routine "
            "household maintenance; Health; Transport; Information and "
            "communication; Recreation, sport and culture; Education services; "
            "Restaurants and accommodation services; Personal care, social "
            "protection and miscellaneous goods and services."
        ),
        comparable_from=(
            "January 2025 for Division/Group indexes on Base 2024=100. Year-on-"
            "year inflation where printed with a prior year on this base (from "
            "January 2026 for All India General lookback; do not invent missing "
            "Group YoY). Card 4 does not carry Division/Group back series."
        ),
        breaks=(
            "Base-year break versus 2012=100 (old six-group structure is not "
            "these Divisions). Same Frame A geography notes as Card 1. Annexure-I "
            "prints Division codes 01–11 then 13 as on the sheet — use printed "
            "names and codes; do not invent a Division 12 series for this slice."
        ),
        lags="Same as Card 1.",
        disagrees_with=(
            "National Metadata Structure PDF (older NSS 68th / six groups) versus "
            "these COICOP 2018 Divisions/Groups. Group 01.1 / CFPI (Card 2) versus "
            "Division 01. Item/Subclass sheets in the same workbook (out of slice; "
            "press: State-level item indices available on the portal should be "
            "interpreted and used with caution, as the indices for some items may "
            "have been compiled using thin samples of price quotations.). CPI "
            "2012=100 group files. WPI and Labour Bureau CPIs (different concepts)."
        ),
        do_not=(
            "Do not label Division 01 as food. Do not use Item or Subclass sheets "
            "to rank cities or to thicken a Division chart. Do not treat press "
            "top five key items tables as this series. Do not chart Housing or "
            "Transport as petrol pump prices. Same geography, rank, forecast, "
            "Combined-merge, blank-as-zero, and 2012=100 do-nots as Card 1. Do "
            "not join these rows to Card 4."
        ),
    ),
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024: CaveatNote(
        caveat_id=CAVEAT_C1_CARD_4,
        concept=(
            "Producer-linked CPI General back series expressed on Base 2024=100 "
            "— not independently compiled 2024-basket observations before the new "
            "series. Rural, Urban and Combined sectors as published. Group = "
            "General only."
        ),
        unit=(
            "Index points (linked onto Base 2024=100) and year-on-year inflation "
            "(%) where the cell is filled. Early Inflation (%) cells are blank "
            "(None) — that is not zero."
        ),
        population=(
            "All India (`00`) only in this file. Sectors Rural / Urban / Combined. "
            "Not States/UTs. Not districts. Same national CPI family as Card 1, "
            "but linked/back-cast rather than the current compiled run."
        ),
        reference_period=(
            "Calendar month on the row. File rows run January 2013–December 2024 "
            "(opened Sheet1). This file’s own release date is not printed on the "
            "sheet — do not use 14 September 2026 as this series’ reference period "
            "or as a substitute release date."
        ),
        producer_definition=(
            "Workbook title as cited: CPI Back Series Index Inflation Based on "
            "Base Year 2024; columns Base Year, State code, State name, Sector, "
            "Year, Month, Group, Index, Inflation (%). Opened rows: State name = "
            "All India, State code = 00, Group = General (citation Card 4). First "
            "rows: January 2013 Rural/Urban/Combined indexes with Inflation (%) "
            "blank; first non-blank inflation is January 2014. Last opened rows: "
            "December 2024. This is the producer’s own linked series, not a user "
            "splice of 2012=100."
        ),
        comparable_from=(
            "Linked General index: January 2013 onward in this file (All India). "
            "Linked year-on-year inflation (%): January 2014 onward (2013 "
            "inflation blank). File ends December 2024. Independently compiled "
            "2024=100 months are Card 1 from January 2025 — not this card."
        ),
        breaks=(
            "Linked / back-cast versus independently compiled Base 2024=100 "
            "(Cards 1–3 from January 2025): show a break, not one blended line. "
            "Do not stitch this file to CPI 2012=100 as if they were one. Frame B "
            "has no State/UT map (Telangana, J&K/Ladakh, DNH&DD reorganisation do "
            "not appear as changing units here). Do not recode Frame A rows onto "
            "this card."
        ),
        lags=(
            "Not a monthly press product; next_release unknown; no date on the "
            "sheet. Do not imply it updates with the August 2026 press note."
        ),
        disagrees_with=(
            "Cards 1–3 compiled 2024-basket General/Division/Group from January "
            "2025 (different compilation status). CPI 2012=100 as originally "
            "published. WPI and Labour Bureau CPIs. No State/UT official CPI in "
            "this file to disagree with Frame A — the hole is missing geography, "
            "not a second state series."
        ),
        do_not=(
            "Do not present these indexes as independently compiled 2024-basket "
            "prices before 2025. Do not stitch to 2012=100. Do not join to Frame A "
            "State/UT rows (there are none). Do not chart State-level history from "
            "this card. Do not chart inflation (%) for 2013 (or any blank cell) as "
            "zero. Do not use this card for CFPI, Division, or Group food. Do not "
            "hide the January 2025 compiled-series start as a smooth continuation. "
            "Do not rank, forecast, overlay pumps, or call All India the whole "
            "country (States, UTs, and districts are missing here)."
        ),
    ),
}

C1_GEOGRAPHIES: dict[str, GeographyVintage] = {
    SERIES_CPI_GENERAL_BASE_2024: FRAME_A_GEOGRAPHY,
    SERIES_CPI_CFPI_BASE_2024: FRAME_A_GEOGRAPHY,
    SERIES_CPI_DIVISION_GROUP_BASE_2024: FRAME_A_GEOGRAPHY,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024: FRAME_B_GEOGRAPHY,
}
