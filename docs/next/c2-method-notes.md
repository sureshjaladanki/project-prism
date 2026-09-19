# C2 method notes

Persona: Methodologist. Sleeve: **People**. Slice: **C2**.

Citizen question: How many people live in India, where, and how is that changing?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`. Schema for caveats already exists in [`docs/data-contracts.md`](../data-contracts.md) (`caveat_id`, `concept`, `unit`, `population`, `reference_period`, `producer_definition`, `comparable_from`, `breaks`, `lags`, `disagrees_with`, `do_not`). This pass writes the notes, not the store. When the slice becomes a product, Platform Architect still owns CMS and the refresh contract.

Locked inputs: [`c2-citation-cards.md`](c2-citation-cards.md), [`c2-geography-frame.md`](c2-geography-frame.md). Charter: [`c2-charter.md`](c2-charter.md).

**Census, SRS, and official projections are three records.** Cards 1–2 are Census of India 2011 stock (and its own historical census table). Cards 3–4 are Sample Registration System (SRS) **rates** for calendar year 2024. Card 5 is the National Commission on Population / MoHFW Technical Group **projection**, November 2019. Do not pick a winner. Do not invent a blended “India today” figure. Do not multiply a 2011 headcount by an SRS rate to make a 2024 stock.

Census of record on these cards: **Census 2011** (00:00 hours, 1 March 2011). As of **18 September 2026** there is no published Census 2021 or Census 2027 headcount. Census 2027 houselisting (notified 1 April 2026–30 September 2026) is not a population total. **The lag is the trust test** ([`docs/vision.md`](../vision.md): when series break, lag, or disagree, say so). Do not paper a 2011 count into a current headcount.

**Release date is not the reference period.** NADA catalog dates, PDF CreationDate, and “May 2026” on the SRS cover are releases. Census day, calendar year 2024, and Table 8’s 1st March projected year are the reference periods.

**No crosswalk.** Frames A–E stay separate. Do not recode 2011 `JAMMU & KASHMIR` onto 2024 Jammu & Kashmir + Ladakh; 2011 `ANDHRA PRADESH` onto Andhra Pradesh + Telangana; or 2011 codes `25` + `26` onto merged Dadra & Nagar Haveli and Daman & Diu.

---

## Card 1 — Census 2011 PCA SD (India and STATE totals)

Binds: citation Card 1. Geography: **Frame A** (Union | state | UT; Census 2011 codes `00`–`35` as printed; TRU is not geography).

```text
concept:            Census of India 2011 Primary Census Abstract (PCA SD) headcount as published for Level = India or STATE: persons (TOT_P), males (TOT_M), females (TOT_F), and households (No_HH) by TRU = Total / Rural / Urban. This is a census stock on Census day, not an SRS rate and not a projection.
unit:               Persons (and households where the column is No_HH), as printed. Not thousands. Not a rate per 1,000.
population:         Everyone enumerated in Census 2011 on the published India and STATE rows. Not DISTRICT rows (1,920 in the same workbook — parked). Not a 2024 or 2026 usual-resident count. Not NPR, electoral rolls, or citizenship registers.
reference_period:   00:00 hours, 1 March 2011 (Census of India 2011). Not the NADA catalog date 19 January 2021. Not 18 September 2026.
producer_definition: Population of record on this card: columns TOT_P, TOT_M, TOT_F for Level = India or STATE (not DISTRICT); TRU = Total / Rural / Urban as published (ORGI, Census of India 2011 PCA SD, NADA catalog 6191, file DDW_PCA0000_2011_Indiastatedist.xlsx Sheet1). India (`00`) is the published national total, not a roll-up Ingest should compute from STATE rows.
comparable_from:    This card is one census vintage. Compare Frame A units only on the 2011 map (codes `00`–`35` as printed). Rural / Urban / Total are three published TRU lines, not a user merge. Do not treat this as a time series beyond 1 March 2011.
breaks:             2011 Census map: no Telangana STATE row; no Ladakh UT row (Leh(Ladakh) and Kargil are DISTRICT under 01 — parked); DAMAN & DIU (`25`) and DADRA & NAGAR HAVELI (`26`) are separate. Later splits/merges are not on this sheet — do not recode onto Frame C or Frame E. Sheets Sheet2 and Sheet3 are empty in this file — not extra totals.
lags:               About fifteen years behind a 2026 reader (cards dated 18 September 2026). next_release: unknown — delayed. Census 2021 population totals were not published. Census 2027 houselisting is not a count. Status of a later census total: delayed / not published — not “use 2011 as current.”
disagrees_with:     Card 2 A-02 (same Census 2011 family, different table and printed names; historical years and footnote marks). Card 3–4 SRS 2024 rates (sample estimates, different year, different map). Card 5 Table 8 (projections in thousands on a smoothed 2011 base; 2011 column is not this PCA). UN / World Bank modelled stocks (charter-out; not a second official Indian census).
do_not:             Do not present TOT_P as “how many people live in India now.” Do not hide the 2011 reference date. Do not ingest or chart DISTRICT rows this iteration. Do not recode 01 / 28 / 25+26 onto 2024 labels. Do not spelling-merge Frame A names with Frame B. Do not add SRS rates to this stock to invent a 2024 headcount. Do not splice Card 5 projected years onto this line. Do not treat India (`00`) as every district or as 2026 India. Do not rank States/UTs (citizen question is not a rank question). Do not use NPR, electoral rolls, or international databases as a patch. Do not forecast or interpolate missing census years as fact.
```

---

## Card 2 — Census 2011 A-02 (decadal variation 1901–2011)

Binds: citation Card 2. Geography: **Frame B** (same 2011 codes `00`–`35` as Frame A; **printed names differ**, including footnote marks).

```text
concept:            Census of India 2011 Table A-02: population by census year 1901–2011 (Persons, Males, Females) and variation since the preceding census (absolute and percentage) for INDIA and States/UTs as printed. Historical census counts, not an SRS rate and not a 2026 headcount.
unit:               Persons, and producer-printed decadal variation (absolute persons and percentage) as labelled. Early years printed N.A. are not zero.
population:         Census enumerated population on District Code `000` India/State/UT rows in this India artifact. Not districts. Not SRS sample units. Some included units have no figure in early years (e.g. Arunachal Pradesh before 1961) — missing observation, not a dropped State.
reference_period:   Census years on the row (1901 through 2011). 2011 is the last year in the table. Not NADA catalog 1 June 2022. Not a 2026 stock.
producer_definition: Table A-2 as printed: India/State/Union Territory by Census Year, Persons, variation since the preceding census (absolute and percentage), Males, Females; State rows use District Code 000 (ORGI, Census of India 2011, NADA catalog 43333, `00 A 2-India.xls` / companion PDF). Footnote marks on names or years (*, ^, $$, ##, @@, $, @, #, + as listed on Frame B) are producer breaks — keep them on the printed name; do not strip them to join Frame A.
comparable_from:    Where the producer prints a number for that census year on that unit. N.A. cells are holes. 2011 is comparable to Card 1 only as two Census 2011 tables on the same code list — still two printed-name frames; Pipeline may key on State Code, not on spelling.
breaks:             Same 2011 map holes as Frame A (no Telangana; no Ladakh UT; Daman & Diu and DNH separate). Producer footnotes are breaks in comparability (territory, coverage, or definition as the PDF states — quote the footnote, do not guess). Do not stitch post-2011 projections (Card 5) onto this 1901–2011 line as one census run.
lags:               Same Census hole as Card 1: no published census year after 2011 on these cards; next_release unknown — delayed.
disagrees_with:     Card 1 PCA (2011 stock on different Name strings; PCA is not a 1901–2011 series). Cards 3–4 (SRS 2024). Card 5 (projections 2011–2036). Civil Registration System (rejected; completeness, not this table).
do_not:             Do not extend the line past 2011 with Table 8 or SRS. Do not chart N.A. as 0. Do not spelling-merge Frame B `Jammu & Kashmir` / `NCT OF Delhi` / `Andhra Pradesh @@` with Frame A names. Do not recode onto Frame C. Do not present decadal variation as an SRS natural growth rate. Do not rank, forecast, interpolate missing census years, or call 2011 “current.”
```

---

## Card 3 — SRS Bulletin 2024 Vol. 59 No. 1 (birth, death, IMR)

Binds: citation Card 3. Geography: **Frame C** (2024 map as printed: Telangana, Ladakh, merged DNH–DD; no state-code column).

```text
concept:            Sample Registration System estimated vital rates for calendar year 2024: Birth Rate, Death Rate, Natural Growth Rate, and Infant Mortality Rate, India and States/UTs, Total / Rural / Urban as published in Tables 1–6. Survey estimates, not a census headcount. This bulletin does not publish TFR (Card 4).
unit:               Rates as labelled on the printed tables (take the denominator from the table header/notes in the PDF). Not persons. Not a stock that can be added to Census TOT_P.
population:         SRS sample for India; Bigger States/Union Territories (producer: population more than 10 million as per Census 2011); Smaller States; Union Territories — labels as in Table 1. Residence (Total / Rural / Urban) is not geography. Not districts. Manipur* is the Manipur unit; the asterisk is a sample footnote (estimates based on 130 SRS units), not a second geography.
reference_period:   Calendar year 2024. Not the cover/release May 2026. Not NADA 20 May 2026. Table 5 note: Smaller States/UTs IMR by sex and residence uses three-year period 2022–24 — that is a different reference period on those cells, not a missing UT.
producer_definition: SRS Bulletin — estimated Birth Rate, Death Rate, Natural Growth Rate and Infant Mortality Rate; Table 1 is the four rates for India and States/UTs, Total / Rural / Urban (ORGI Vital Statistics Division, SRS Bulletin Volume 59 No. 1, May 2026, NADA catalog 47150). Bigger States/UTs: population more than 10 million as per Census 2011. Manipur: estimates based on 130 SRS units (producer footnote).
comparable_from:    This card is the 2024 bulletin issue. Compare Frame C units as printed for 2024. Do not join a 2024 stub to a 2011 Census code because the English looks similar. Do not fill Card 4’s missing smaller States/UTs from this bulletin and call the result the Statistical Report.
breaks:             2024 map vs Frames A/B: Telangana and Andhra Pradesh distinct; Jammu & Kashmir and Ladakh distinct; DNH and Daman & Diu merged as one UT. Table 5 three-year IMR (2022–24) vs calendar-year 2024 rates on Table 1 — show the period, do not blend. Manipur* sample restriction is a method note on that unit, not a recode.
lags:               2024 rates released May 2026. next_release unknown (no date on this bulletin for reference year 2025).
disagrees_with:     Cards 1–2 (census stock, 2011, different map). Card 4 (same SRS family and year; TFR and bigger-State-only fertility tables live there; coverage is narrower). Card 5 (projected stock). CRS (rejected). International modelled vital rates (charter-out).
do_not:             Do not add Card 1 population to these rates to invent a 2024 headcount. Do not present a rate as “how many people live in India.” Do not recode Frame A/B `01` / `28` / `25`+`26` onto these rows. Do not drop the Manipur* footnote. Do not chart Table 5’s 2022–24 IMR as if it were 2024 annual. Do not use this card for TFR. Do not rank States/UTs. Do not forecast, nowcast, or interpolate 2025. Do not treat India as every district.
```

---

## Card 4 — SRS Statistical Report 2024 (fertility including TFR)

Binds: citation Card 4. Geography: **Frame D** (India and **bigger States/UTs only**; smaller States and UTs missing from the main tables).

```text
concept:            SRS Statistical Report 2024 fertility and mortality indicators as published, including Crude Birth Rate and Total Fertility Rate (TFR) for calendar year 2024. Same SRS family as Card 3, not a substitute census. TFR and other fertility measures live here, not in the Bulletin.
unit:               Indicators as labelled in Chapter 3 / Detailed Table 3 and mortality tables as published (take TFR’s unit from the printed table). Not Census persons. Not Card 5 thousands.
population:         India and bigger States/UTs (population of 10 million and above), rural and urban, as the preface states — the Bigger States/Union Territories list on Frame C, plus India. **Missing:** all Frame C Smaller States and all Frame C Union Territories (including Ladakh and merged DNH–DD). NSS Natural Division maps/tables in the same PDF are below the charter bar — parked. Districts not in this report as a district file.
reference_period:   Calendar year 2024. Not PDF CreationDate / NADA 20 May 2026.
producer_definition: Sample Registration System Statistical Report 2024 — fertility and mortality indicators as published (including Crude Birth Rate and Total Fertility Rate); Fertility: Chapter 3 and Detailed Table 3 “Fertility Indicators, 2024”; Figures at a Glance, India — 2024 in the front matter; preface: India and bigger States/UTs (population of 10 million and above), rural and urban (ORGI, NADA catalog 47152, SRS_STAT_2024.pdf).
comparable_from:    This 2024 report, Frame D units only. An India TFR on this card must still name missing smaller States, UTs, and districts. Do not borrow those units from Card 3.
breaks:             Narrower geography than Card 3. Same 2024 bigger-state map as Frame C’s bigger block (Telangana and Andhra Pradesh distinct; Jammu & Kashmir in the bigger list; Ladakh not on this frame). Do not fill holes from the Bulletin. Parked NSS Natural Division rows are not State/UT observations.
lags:               Same May 2026 vintage as Card 3. next_release unknown (no date in the preface for the 2025 report).
disagrees_with:     Card 3 (Bulletin has the full Table 1 State/UT list and does not publish TFR). Cards 1–2 (census stock). Card 5 (projections). NFHS or other survey fertility (not on these cards; do not import to patch Frame D). International modelled TFR (charter-out).
do_not:             Do not present TFR as a headcount or as “India today.” Do not blend with Card 1 or Card 5. Do not paste Smaller States / UT rates from the Bulletin into this report’s tables. Do not recode 2011 Andhra Pradesh or Jammu & Kashmir onto these bigger-state rows. Do not chart parked Natural Division tables. Do not rank, forecast, or interpolate missing States/UTs as if they were in this book.
```

---

## Card 5 — NCP/MoHFW Technical Group projections 2011–2036, Table 8

Binds: citation Card 5. Geography: **Frame E** (Table 8 row labels as printed; including Jammu & Kashmir*(UT) and Telangana as the librarian named them).

```text
concept:            Projected total population by sex as on 1st March, 2011–2036, India, States and Union Territories*, in thousands — TABLE-8 of the Technical Group report. A projection, not a census. A Table-8 figure for a year after 2011 is not an enumerated headcount.
unit:               Thousands ('000) as printed. Multiply-by-1,000 is a unit conversion the producer already labelled — still not Census PCA persons, and still not a licence to drop “projected.”
population:         India, States and UTs as labelled on TABLE-8. Not districts. Do not copy Frame C’s list onto Table 8. Other tables in the same PDF that exclude Goa or combine North-East States excluding Assam are not this series. Input tables in Appendix 1 are assumptions, not published projected stock.
reference_period:   Projected years 2011–2036 as on **1st March** in Table 8. Not the report date November 2019. Not PDF CreationDate 21 November 2019. TABLE-11 in the same PDF is as on **1st July** — same report, different reference day; not this series.
producer_definition: TABLE-8 “Projected Total Population by Sex as on 1st March - 2011 - 2036 : India, States and Union Territories* ('000)” (National Commission on Population, Ministry of Health & Family Welfare, Report of the Technical Group on Population Projections, November 2019). Base is Census 2011 (smoothed), not a 2019 count. Hosted PDF from nhm.gov.in; not an ORGI census table.
comparable_from:    Table 8 columns as published inside this one 2019 report. The 2011 column is still a projection on a smoothed Census 2011 base — not Card 1 TOT_P. Later years are not comparable to a census that was not taken.
breaks:             Projection map as of November 2019, Census 2011 base. Jammu & Kashmir*(UT) is the printed Table 8 unit — not Frame A `01` and not Frame C’s pair (Jammu & Kashmir + Ladakh) unless Table 8 itself prints Ladakh. Table 8 vs Table 11 (1st March vs 1st July). Not a 2011 PCA row and not a 2024 SRS row. No successor Technical Group report found on these cards (search 18 September 2026).
lags:               Report dated November 2019. next_release unknown. Does not close the Census 2021/2027 hole: a 2026 Table-8 cell is still a 2019 projection, not a new enumeration.
disagrees_with:     Card 1 PCA (enumerated persons, 1 March 2011, different unit and map). Card 2 A-02. Cards 3–4 (SRS rates, 2024). TABLE-11 (1st July) in the same PDF. Superseded projection reports (1996–2016, 1981–2001 — rejected). UN World Population Prospects (charter-out).
do_not:             Do not present a Table-8 figure as “India has X people” without naming Table 8, thousands, 1st March, and that it is a projection. Do not merge Table 8 and Table 11. Do not stitch Table 8 onto A-02 as a census continuation. Do not recode thousands or 1st March into another frame. Do not treat Appendix 1 assumptions as stock. Do not use this card to paper the missing Census 2021/2027. Do not rank, nowcast, or blend with SRS. Do not invent English names from Frame C.
```

---

## Do not chart (Content Editor)

A chart that does any of the following is a lie for this slice:

1. **One “India today” headcount** that hides series and year, or blends Census, SRS, and Table 8.
2. **Census 2011 as current** without saying 1 March 2011 and the unpublished later census.
3. **Census stock, SRS rates, and projections as one line** (persons vs rates vs thousands; 2011 vs 2024 vs projected years).
4. **Card 1 × Card 3** (or any rate × stock) as a homemade 2024 population.
5. **A-02 1901–2011 stitched to Table 8 2011–2036** as one census run. Break after 2011. Table 8’s 2011 column is not PCA.
6. **Table 8 and Table 11** as one series (1st March vs 1st July).
7. **Frame A/B recoded onto Frame C/D/E:** 2011 Jammu & Kashmir → 2024 J&K + Ladakh; 2011 Andhra Pradesh → Andhra + Telangana; 25+26 → merged DNH–DD.
8. **Frame B names spelling-merged with Frame A** (footnote marks stripped).
9. **Card 4 India TFR (or other indicator) as the whole country** without naming missing smaller States, UTs, and districts.
10. **Card 3 Table 5 IMR 2022–24** drawn as calendar year 2024.
11. **N.A. / blank as zero.**
12. **District dots or maps** from PCA DISTRICT rows (parked).
13. **NPR, electoral rolls, caste, NITI scorecards, World Bank/UN** as source of record.
14. **Ranks** (this citizen question is not a rank question).
15. **Forecasts, nowcasts, or interpolated census years as fact.** Census 2027 houselisting is not a point on the population line.

Content Editor may show the three records as three records; 2011 stock beside the named lag; SRS 2024 rates beside (not instead of) that stock; Table 8 labelled projected, in thousands, 1st March; Frame A India beside named missing units (districts parked; Telangana and Ladakh not on the 2011 STATE list).

---

## Holes (Trust Auditor)

Named holes. None require Charter Editor to shrink C2: the charter already parks districts, rejects a blended “India today,” NPR/rolls/caste, and international modelled stocks, and requires each series as itself.

| Hole | Where | What to show |
|------|--------|----------------|
| No Census 2021/2027 headcount | Cards 1–2 | 2011 is the census of record; lag is the point; houselisting ≠ count |
| ~15-year lag to a 2026 reader | Card 1 | Say 1 March 2011; do not treat as current |
| Districts parked | Card 1 (1,920 DISTRICT rows); all frames | India is not every district |
| No Telangana / Ladakh UT / merged DNH–DD | Frames A/B | 2011 map; do not recode |
| Frame A vs B printed names | Cards 1–2 | Same codes; different strings and footnote marks |
| A-02 footnotes and N.A. years | Card 2 | Producer breaks; N.A. is not 0 |
| SRS is a sample rate, not a stock | Cards 3–4 | Do not mint a 2024 headcount |
| Manipur* 130 SRS units | Card 3 | Keep the sample footnote |
| Smaller States/UTs IMR 2022–24 | Card 3 Table 5 | Different period than 2024 Table 1 |
| No TFR in the Bulletin | Card 3 vs 4 | Two products; TFR is Card 4 |
| Smaller States and UTs missing | Frame D / Card 4 | Do not fill from Card 3 |
| Table 8 is a projection in thousands | Card 5 | Not a census; name 1st March and '000 |
| Table 8 2011 ≠ PCA 2011 | Cards 5 vs 1 | Smoothed/projected base vs enumerated stock |
| Table 11 1st July | Same PDF as Card 5 | Other series; do not merge |
| No successor projection report | Card 5 | 2019 vintage; unknown next |
| Three maps, no crosswalk | Frames A–E | Show disagreement; do not join |
| International modelled “India today” | Charter-out | Not on the page |

No stretch of definition was used to make a chart work. Caveat fields fit the existing schema; nothing to hand to Platform for a missing field.

---

## Handoff

First crew memo for **C2** is complete (Charter Editor → Source Librarian → Geography Steward → Methodologist).

**Do not ingest into `data/`.** Do not fetch. Do not start a citizen page in this pass.

Next when this slice becomes a product: **Platform Architect** (CMS + refresh contract), then Ingest, Pipeline, Content Editor, UI/UX, Trust — [`docs/team.md`](../team.md) First crew.
