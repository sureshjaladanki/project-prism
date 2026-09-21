# C1 method notes

Persona: Methodologist. Sleeve: **Prices and production**. Slice: **C1**.

Citizen question: How fast are retail prices rising in India, including food?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`. Schema for caveats already exists in [`docs/data-contracts.md`](../data-contracts.md) (`caveat_id`, `concept`, `unit`, `population`, `reference_period`, `producer_definition`, `comparable_from`, `breaks`, `lags`, `disagrees_with`, `do_not`). This pass writes the notes, not the store. When the slice becomes a product, Platform Architect still owns CMS and the refresh contract.

Locked inputs: [`c1-citation-cards.md`](c1-citation-cards.md), [`c1-geography-frame.md`](c1-geography-frame.md).

Producer for all four cards: National Statistics Office (NSO), Price Statistics Division, Ministry of Statistics and Programme Implementation (MoSPI). CPI here is a **price index from a price-collection system**, not a census of every shop and not an administrative tax or pump-price register. The August 2026 press note states: “Real time price data are collected from selected 1407 urban Markets (including online markets) and 1465 villages covering all States/UTs through personal visits by field staff of Field Operations Division of NSO, MoSPI on a weekly roster.” That is the producer’s collection description. Do not invent a sample-design essay beyond it.

**Release date is not the reference period.** The 14 September 2026 press note is the release. The month on the row (for example August 2026) is the reference period.

---

## Card 1 — CPI General (Rural, Urban, Combined), Base 2024=100

Binds: citation Card 1. Geography: **Frame A** (Union | state | UT; `00` All India plus 36 States/UTs; sector is not geography).

```text
concept:            All-India and State/UT Consumer Price Index (CPI) General — the producer’s headline retail price index of selected goods and services, Base 2024=100. Published as three sectors: Rural, Urban, and Combined. Combined is a published sector in the same tables, not a user merge of Rural and Urban.
unit:               Index points (Base 2024=100) and, where the producer prints it, year-on-year inflation (%) — August 2026 over August 2025 in the latest press table. Status F/P as printed. Do not treat a blank inflation cell as 0.
population:         Prices from the NSO Field Operations Division collection: selected 1407 urban markets (including online markets) and 1465 villages covering all States/UTs (August 2026 press note). Not a census of all transactions. Not districts. Not a city ranking of the 1407/1465 collection points.
reference_period:   Calendar month named on the row (latest on these cards: August 2026 Provisional and July 2026 Final). Not the press date 14 September 2026.
producer_definition: “Year-on-year inflation rate based on All India Consumer Price Index (CPI) with base year 2024 for the month of August, 2026 over August, 2025 is 4.82%(Provisional). Corresponding inflation rates for rural and urban are 5.23% and 4.31%, respectively.” Same note prints CPI (General) Index and Inflation for Rural, Urban and Combined in one Key Statistics table (July 2026 Final beside August 2026 Provisional). Collection: selected 1407 urban markets and 1465 villages covering all States/UTs, weekly roster (NSO/MoSPI, Press Release of Consumer Price Index on Base 2024=100 for August, 2026, 14 September 2026). Annexure-III footnote: “*: No rural market in Chandigarh”. Rounding: “Indices at all levels and inflation rates are compiled using the actual index values without rounding off. However, the indices published are rounded off to two decimal places.”
comparable_from:    Independently compiled Base 2024=100 General index: January 2025 onward (time-series workbooks and Annexure-IV). Year-on-year inflation (%) on this base: January 2026 onward in Annexure-IV (Jan–Dec 2025 inflation cells are blank because there is no prior year on this base). Do not use Card 4 to fill those 2025 blanks.
breaks:             Base-year break versus CPI 2012=100 (and 2010=100 remnants): show a break, never a blended line. Linked back series (Card 4) is not this card. Sector Combined is not a geography break. Frame A already uses current units (Telangana 36 / Andhra Pradesh 28; Jammu And Kashmir 01 / Ladakh 37; DNH&DD 25). Chandigarh (04) Rural is withheld (dash / no Rural row); Combined equals Urban on that row — not a missing UT. Code 26 unused. `00` All India is a published national unit, not a roll-up of State/UT Combined.
lags:               August 2026 figures released 14 September 2026; next release 12 October 2026 (CPI for September 2026). Latest month is Provisional until the producer prints Final (here July 2026 Final sits beside August 2026 Provisional). Status P and F are different observations, not one smoothed number.
disagrees_with:     CPI Base 2012=100 (previous series; still appears on some product-9 files — not this line). National Metadata Structure PDF on the MoSPI site still describes older grouping (NSS 68th round weights / six groups) while live 2024=100 releases use COICOP 2018 — cite the live workbook, not the stale metadata PDF, as the grouping of record. Out of this slice but official and not the same number: WPI (DPIIT wholesale); Labour Bureau CPI-IW and CPI-AL/RL (different populations and baskets). Division 01 “Food and beverages” (Card 3) is not this General index. CFPI (Card 2) is not this General index. Pump prices (PPAC) are not this series (press note: petrol, diesel and LPG price reference is the 15th of the month inside the CPI collection — that is not a PPAC overlay).
do_not:             Do not average Rural and Urban to invent Combined. Do not present `00` All India as “the whole country” (districts parked; Chandigarh Rural withheld; All India is not a sum of State/UT Combined). Do not recode State Codes. Do not join Frame A State/UT rows to Card 4 (Card 4 has none). Do not stitch 2012=100 onto this series. Do not chart a continuous line from Card 4 linked indexes into this compiled series as if they were one independently compiled run — state the break at January 2025. Do not chart blank inflation (%) as zero. Do not replace Provisional with Final or blend them. Do not rank States/UTs or cities; press “top five States” tables are not a series. Do not overlay petrol pump prices. Do not issue cheap/expensive or forecast copy. Do not recompute higher-level indexes from rounded published figures and treat the difference as a revision.
```

---

## Card 2 — Consumer Food Price Index (CFPI) / CPI Group Food (01.1)

Binds: citation Card 2. Geography: **Frame A**. Same workbook family as Card 1. CFPI Combined values match Group code **01.1** name **Food** — not Division **01**.

```text
concept:            Consumer Food Price Index (CFPI): the producer’s named food price index, Base 2024=100, Rural / Urban / Combined. Same figures as CPI Group “Food”, Group code 01.1. Not Division 01 “Food and beverages”.
unit:               Index points (Base 2024=100) and year-on-year inflation (%) as printed. Blank inflation is not zero. Status Provisional / Final as printed.
population:         Same price-collection system as Card 1 (1407 urban markets including online; 1465 villages; all States/UTs). Food as Group 01.1, not every item a household buys.
reference_period:   Calendar month on the row (August 2026 Provisional and July 2026 Final on these cards). Not 14 September 2026.
producer_definition: “Year-on-year inflation rate based on All India Consumer Food Price Index (CFPI) for the month of August, 2026 over August, 2025 is 5.95% (Provisional). Corresponding inflation rates for rural and urban are 6.13% and 5.64%, respectively.” Key Statistics prints CFPI Index and Inflation beside CPI (General) (NSO/MoSPI press note, 14 September 2026). Annexure-II row Group code 01.1 Food Combined inflation 5.95% matches that CFPI figure. Annexure-I Division 01 Food and beverages Combined inflation is 5.66% — a different published number (Division 01 also includes Group 01.2 Beverages and Group 01.3 Services for processing primary goods for food).
comparable_from:    Same as Card 1 for this base: Group 01.1 / CFPI index from January 2025; year-on-year inflation on this base from January 2026 where the producer prints it. Card 4 has Group = General only — no CFPI back series in that file.
breaks:             Same base-year break versus 2012=100. Same Frame A geography notes as Card 1 (including Chandigarh Rural withheld). Do not treat Division 01 as a continuation of CFPI.
lags:               Same monthly calendar as Card 1 (August 2026 Provisional in the 14 September 2026 release; July 2026 Final in the same book).
disagrees_with:     Division 01 Food and beverages (Card 3) — same producer, same month, different basket (food plus beverages and food-processing services). Headline CPI General (Card 1). CPI 2012=100 food groupings. WPI food articles (wholesale, different office). Labour Bureau food components of CPI-IW / CPI-AL/RL. Stale National Metadata Structure six-group description versus live COICOP 2018 Group 01.1.
do_not:             Do not chart Division 01 as “food” or as CFPI. Do not mix 01.1 with 01.2 or 01.3 into a homemade food index. Do not use Card 4 for food. Do not rank states or cities by food inflation. Do not overlay tomato/onion item spikes as the food index (item tables are out of this slice; press also warns some item indices use thin samples). Same geography and status do-nots as Card 1: no All-India-as-whole-country, no Rural/Urban merge, no blank-as-zero, no Provisional/Final blend, no pump prices, no cheap/expensive, no forecast.
```

---

## Card 3 — CPI Division and Group indexes (COICOP 2018), Base 2024=100

Binds: citation Card 3. Geography: **Frame A**. Same monthly and time-series workbooks. Not city rankings. Not item/subclass for this slice.

```text
concept:            CPI Division indexes (COICOP 2018, 12 Divisions as named) and CPI Group indexes (43 Groups as named), Rural / Urban / Combined, Base 2024=100. Headline General is Card 1. Food-only is Card 2 (Group 01.1 / CFPI). Division 01 is “Food and beverages”.
unit:               Index points (Base 2024=100) and year-on-year inflation (%) as printed. Blank inflation is not zero. Status Provisional / Final as printed.
population:         Same collection system as Card 1. Each Division/Group is the producer’s COICOP 2018 aggregate, not a user basket.
reference_period:   Calendar month on the row (August 2026 Provisional and July 2026 Final on these cards). Not 14 September 2026.
producer_definition: Annexure-I title: “All India General (Rural, Urban and Combined) division wise indices and inflation for August, 2026 (Provisional)”; Division 01 Food and beverages is one row among twelve named divisions; a bottom “All India” row is General (Card 1), not Division 01 (NSO/MoSPI press note, 14 September 2026). Annexure-II title: group wise indices; first row is 01.1 Food. Live 2024=100 grouping is COICOP 2018 (product-9 metadata and these annexes). Division names as printed for August 2026: Food and beverages; Paan, tobacco and intoxicants; Clothing and footwear; Housing, water, electricity, gas and other fuels; Furnishings, household equipment and routine household maintenance; Health; Transport; Information and communication; Recreation, sport and culture; Education services; Restaurants and accommodation services; Personal care, social protection and miscellaneous goods and services.
comparable_from:    January 2025 for Division/Group indexes on Base 2024=100. Year-on-year inflation where printed with a prior year on this base (from January 2026 for All India General lookback; do not invent missing Group YoY). Card 4 does not carry Division/Group back series.
breaks:             Base-year break versus 2012=100 (old six-group structure is not these Divisions). Same Frame A geography notes as Card 1. Annexure-I prints Division codes 01–11 then 13 as on the sheet — use printed names and codes; do not invent a Division 12 series for this slice.
lags:               Same as Card 1.
disagrees_with:     National Metadata Structure PDF (older NSS 68th / six groups) versus these COICOP 2018 Divisions/Groups. Group 01.1 / CFPI (Card 2) versus Division 01. Item/Subclass sheets in the same workbook (out of slice; press: “State-level item indices available on the portal should be interpreted and used with caution, as the indices for some items may have been compiled using thin samples of price quotations.”). CPI 2012=100 group files. WPI and Labour Bureau CPIs (different concepts).
do_not:             Do not label Division 01 as food. Do not use Item or Subclass sheets to rank cities or to thicken a Division chart. Do not treat press “top five key items” tables as this series. Do not chart Housing or Transport as petrol pump prices. Same geography, rank, forecast, Combined-merge, blank-as-zero, and 2012=100 do-nots as Card 1. Do not join these rows to Card 4.
```

---

## Card 4 — CPI Back Series Index and Inflation (Base 2024=100, linked)

Binds: citation Card 4. Geography: **Frame B** (Union only; `00` All India; all 36 States/UTs missing). General only.

```text
concept:            Producer-linked CPI General back series expressed on Base 2024=100 — not independently compiled 2024-basket observations before the new series. Rural, Urban and Combined sectors as published. Group = General only.
unit:               Index points (linked onto Base 2024=100) and year-on-year inflation (%) where the cell is filled. Early Inflation (%) cells are blank (None) — that is not zero.
population:         All India (`00`) only in this file. Sectors Rural / Urban / Combined. Not States/UTs. Not districts. Same national CPI family as Card 1, but linked/back-cast rather than the current compiled run.
reference_period:   Calendar month on the row. File rows run January 2013–December 2024 (opened Sheet1). This file’s own release date is not printed on the sheet — do not use 14 September 2026 as this series’ reference period or as a substitute release date.
producer_definition: Workbook title as cited: CPI Back Series Index Inflation Based on Base Year 2024; columns Base Year, State code, State name, Sector, Year, Month, Group, Index, Inflation (%). Opened rows: State name = All India, State code = 00, Group = General (citation Card 4). First rows: January 2013 Rural/Urban/Combined indexes with Inflation (%) blank; first non-blank inflation is January 2014. Last opened rows: December 2024. This is the producer’s own linked series, not a user splice of 2012=100.
comparable_from:    Linked General index: January 2013 onward in this file (All India). Linked year-on-year inflation (%): January 2014 onward (2013 inflation blank). File ends December 2024. Independently compiled 2024=100 months are Card 1 from January 2025 — not this card.
breaks:             Linked / back-cast versus independently compiled Base 2024=100 (Cards 1–3 from January 2025): show a break, not one blended line. Do not stitch this file to CPI 2012=100 as if they were one. Frame B has no State/UT map (Telangana, J&K/Ladakh, DNH&DD reorganisation do not appear as changing units here). Do not recode Frame A rows onto this card.
lags:               Not a monthly press product; next_release unknown; no date on the sheet. Do not imply it updates with the August 2026 press note.
disagrees_with:     Cards 1–3 compiled 2024-basket General/Division/Group from January 2025 (different compilation status). CPI 2012=100 as originally published. WPI and Labour Bureau CPIs. No State/UT official CPI in this file to disagree with Frame A — the hole is missing geography, not a second state series.
do_not:             Do not present these indexes as independently compiled 2024-basket prices before 2025. Do not stitch to 2012=100. Do not join to Frame A State/UT rows (there are none). Do not chart State-level history from this card. Do not chart inflation (%) for 2013 (or any blank cell) as zero. Do not use this card for CFPI, Division, or Group food. Do not hide the January 2025 compiled-series start as a smooth continuation. Do not rank, forecast, overlay pumps, or call All India the whole country (States, UTs, and districts are missing here).
```

---

## Do not chart (Content Editor)

A chart that does any of the following is a lie for this slice:

1. **Headline Combined as a homemade merge** of Rural and Urban. Combined is published. Chandigarh Combined = Urban on the printed row; Chandigarh Rural is withheld (“No rural market in Chandigarh”).
2. **Division 01 “Food and beverages” labelled as food.** Food is CFPI / Group 01.1 (Card 2). August 2026 Combined: CFPI 5.95% vs Division 01 5.66%.
3. **Provisional and Final as one smoothed month.** August 2026 is Provisional; July 2026 is Final in the same book.
4. **2012=100 and 2024=100 as one continuous line.** Base-year break. Card 4 is linked back series only — still not 2012=100, and still not Cards 1–3.
5. **Card 4 linked General into Card 1 compiled General as one independently compiled run.** Break at January 2025. Card 4 stops December 2024, All India only.
6. **Card 4 State/UT history** (none) joined to Frame A.
7. **All India (`00`) as the whole country.** It is a published national unit, not a roll-up of State/UT Combined, not every district. Districts are parked. Do not recode.
8. **Blank `inflation (%)` as zero** — Card 4 year 2013; Card 1 Annexure-IV Jan–Dec 2025 inflation cells.
9. **Cheap / expensive verdicts; city or state rankings; press “top five States” or “top five items” as a ranking product.**
10. **Petrol / diesel / LPG pump prices (PPAC) overlaid on CPI.** Fuel in the CPI basket is not the pump series; press reference for those items is the 15th of the month.
11. **Item / Subclass / eSankhyiki thin-sample item indexes** as this slice; **districts**; **WPI, CPI-IW, CPI-AL/RL, CPI UNME**.
12. **Forecasts, nowcasts, or interpolated holes.**
13. **Recomputed higher-level indexes from rounded published figures** treated as a producer revision.

Content Editor may show Rural, Urban, and Combined as three published series; CFPI next to (not instead of, not relabelled as) Division 01; index and inflation as separate series so blank inflation is a hole, not a dip to zero; All India beside named missing units (districts parked; on Card 4, all 36 States/UTs missing).

---

## Holes (Trust Auditor)

Named holes. None require Charter Editor to shrink C1: the charter already parks districts, rejects ranks/pumps/forecasts, and allows a longer run only if the series allows (Card 4 is All India linked General, not State/UT compiled food).

| Hole | Where | What to show |
|------|--------|----------------|
| Latest month Provisional | Cards 1–3 | Status P, not blended with Final |
| YoY inflation blank on current base until 12-month lookback | Card 1 Annexure-IV Jan–Dec 2025 | Index yes; inflation hole, not zero |
| Linked back series, not 2024-basket compilation | Card 4 | Break vs Cards 1–3 at Jan 2025 |
| Inflation blank in 2013 | Card 4 | Do not chart as 0; first filled YoY is Jan 2014 |
| No State/UT on Card 4 | Frame B | All 36 States/UTs missing; do not join Frame A |
| Chandigarh Rural withheld | Frame A unit `04` | Dash / omitted Rural row; Combined = Urban |
| Districts | All cards | Parked; All India is not “every district” |
| CFPI ≠ Division 01 | Cards 2 vs 3 | Two official numbers; do not pick a winner |
| Stale metadata PDF (six groups / NSS 68) vs live COICOP 2018 | Product 9 vs annexes | Live workbook/annex is grouping of record |
| Card 4 has no printed release date | Card 4 | Do not borrow 14 Sep 2026 |
| Rounding of published indexes | Press note | Do not treat user-recomputed drift as a revision |
| Thin-sample item indexes | Press warning | Out of slice |
| Other official price series | WPI, CPI-IW, CPI-AL/RL, pumps | Out of slice; different concept |

No stretch of definition was used to make a chart work.

---

## Handoff

First crew memo for **C1** is complete (Charter Editor → Source Librarian → Geography Steward → Methodologist).

**Do not fetch. Do not start C2–C20. Do not ingest into `data/`.**

Next when this slice becomes a product: **Platform Architect** (CMS + refresh contract), then Ingest, Pipeline, Content Editor, UI/UX, Trust — [`docs/team.md`](../team.md) First crew.
