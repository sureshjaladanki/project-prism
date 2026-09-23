# C7 method notes

Persona: Methodologist. Sleeve: **People**. Slice: **C7**.

Citizen question: How do births, deaths, child survival, and nutrition stand in the official record?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`.

Locked inputs: [`c7-citation-cards.md`](c7-citation-cards.md), [`c7-geography-frame.md`](c7-geography-frame.md). Charter block: [`topic-charters.md`](topic-charters.md) § C7.

**SRS, NFHS, and RHS are three records.** Cards 1–2 are Sample Registration System vital rates (ORGI). Card 3 is NFHS-6 survey fact sheets (IIPS / MoHFW). Card 4 is Rural Health Statistics facility counts (MoHFW Statistics Division). Do not mix them into one “child survival” or “health” number. Do not invent a blended C2+C7 product — Cards 1–2 reuse C2’s SRS artifacts for a different citizen question.

**Release date is not the reference period.** Bulletin/Statistical Report May 2026 → calendar year **2024**. NFHS fact-sheet release May 2026 → fieldwork **May 2023–December 2024**. RHS PDF 2023 → stock **as on 31 March 2022**.

**Survey vs survey vs administrative.** SRS and NFHS are both sample surveys with different designs and indicators. RHS is an administrative facility yearbook. Line them up only with break notes — never as one continuous series.

**NFHS fact sheets do not replace SRS mortality.** The 101 indicators include nutrition and MCH measures; they do **not** print Neonatal / Infant / Under-five mortality rates as SRS does. Do not invent those cells from NFHS-5 DHS hosts or from stunting columns.

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| SRS Bulletin | Do not blend with NFHS; do not treat as census | Birth, death, and infant mortality rates as SRS estimates for 2024 |
| SRS Statistical Report | Do not fill smaller States/UTs from the Bulletin | Fertility and under-five mortality for India and bigger States/UTs |
| NFHS-6 fact sheets | Do not invent IMR/U5MR; do not fill Manipur | Survey indicators including nutrition; Manipur not in this set |
| RHS 2021-22 | Do not use NITI Health Index; do not pull district Section II | Public facility counts as on 31 March 2022; lagged |

---

## Card 1 — SRS Bulletin 2024 (birth, death, IMR)

Binds: citation Card 1. Geography: **Frame A**. Same artifact as C2 Card 3.

```text
concept:            Estimated Birth Rate, Death Rate, Natural Growth Rate, and Infant Mortality Rate for India and States/UTs (Table 1 and related Bulletin tables).
unit:               Rates as labelled (per 1,000 population or per 1,000 live births as printed).
population:         SRS sample population for calendar year 2024. Not a census. Not NFHS.
reference_period:   Calendar year 2024. Not May 2026 release.
producer_definition: SRS Bulletin Volume 59 No. 1 (ORGI Vital Statistics Division). series_id srs-bulletin-2024.
comparable_from:    Within this Bulletin’s 2024 tables. Prior SRS bulletins are history with possible sample/geography breaks.
breaks:             Survey estimates. Do not blend with Card 3. Residence Total/Rural/Urban is not a geography recode. Manipur* sample footnote stays on the stub.
lags:               Published May 2026 for 2024; next_release unknown.
disagrees_with:     Card 3 NFHS (different survey; fact sheets lack matching IMR cells here). Card 2 (same SRS family, more detail / narrower geography for some indicators).
do_not:             Do not mix with NFHS nutrition or MCH indicators into one number. Do not present as census vital registration. Do not pull districts.
```

---

## Card 2 — SRS Statistical Report 2024 (fertility, under-five, neonatal as published)

Binds: citation Card 2. Geography: **Frame B**. Same artifact as C2 Card 4.

```text
concept:            Fertility and mortality indicators as published (CBR, TFR, IMR, neonatal rates, Under-five Mortality Rate, and related Detailed Tables 8–11 / Chapters 3–4).
unit:               Rates and ratios as labelled in the report.
population:         India and bigger States/UTs (population ≥10 million) for the main tables. Not smaller States/UTs on those tables.
reference_period:   Calendar year 2024. Not 20 May 2026 PDF CreationDate.
producer_definition: SRS Statistical Report 2024 (ORGI). series_id srs-statistical-report-2024.
comparable_from:    Within this report’s 2024 tables for Frame B units. Do not extend to Frame A smaller/UT list.
breaks:             Narrower geography than Card 1. NSS Natural Division tables parked. Do not average with Card 3 nutrition.
lags:               Same May 2026 vintage as Card 1; next_release unknown.
disagrees_with:     Card 1 (same family; Bulletin has fuller State/UT list for the four headline rates). Card 3 NFHS.
do_not:             Do not fill missing smaller States/UTs from the Bulletin and call it this report. Do not blend under-five rates with stunting. Do not pull Natural Division rows.
```

---

## Card 3 — NFHS-6 (2023-24) Fact Sheets

Binds: citation Card 3. Geography: **Frame C**.

```text
concept:            101 key indicators on population, health, family planning, maternal and child health, nutrition, and related topics as printed on India and State/UT fact sheets.
unit:               Percents, rates, and counts as labelled on each indicator row.
population:         NFHS-6 surveyed households / eligible respondents for fieldwork May 2023–December 2024. Not SRS sample. Not facility stock.
reference_period:   Survey fieldwork May 2023–December 2024; fact-sheet release May 2026 is not the fieldwork window.
producer_definition: NFHS-6 Fact Sheets PDF (IIPS 2026; MoHFW stewardship). series_id nfhs-6-factsheets-2023-24.
comparable_from:    Within NFHS-6 fact sheets. NFHS-5 comparison columns on the sheets are the producer’s prior round — cite as printed, do not invent a blended NFHS–SRS series.
breaks:             Manipur absent from this set. Fact sheets do not print NMR/IMR/U5MR as SRS Cards 1–2 do — that is a content hole, not a licence to import DHS FR375. District fact sheets parked.
lags:               Fact sheets May 2026; full national report (mortality chapters) not open-fetchable on nfhsiips.in this citation run — named hole. next_release unknown.
disagrees_with:     Cards 1–2 SRS vital rates (different design and indicators). Card 4 RHS (facilities, not survey health).
do_not:             Do not merge with SRS into one child-survival number. Do not invent IMR/U5MR from nutrition cells. Do not fill Manipur from SRS. Do not use NITI Health Index or DHS Program NFHS-5 PDF as the record. Do not pull district fact sheets.
```

---

## Card 4 — Rural Health Statistics 2021-22 (facility counts)

Binds: citation Card 4. Geography: **Frame D**.

```text
concept:            Public health facility counts and related infrastructure / manpower statements (SCs, PHCs, CHCs and related tables) as published in RHS.
unit:               Counts of facilities (and manpower figures where printed) as labelled.
population:         Public facilities in the MoHFW RHS administrative yearbook. Not private hospitals. Not survey respondents.
reference_period:   As on 31 March 2022. Not January 2023 PDF dates.
producer_definition: Rural Health Statistics 2021-22, MoHFW Statistics Division (HMIS fileid 34). series_id rhs-2021-22.
comparable_from:    Within this yearbook’s state-wise statements. Older RHS years on the same menu are history.
breaks:             Stock date is years behind SRS 2024 and NFHS-6 fieldwork. District Section II parked. Do not use CBHI National Health Profile as a silent substitute.
lags:               Latest on HMIS Publications menu this citation run; RHS after 2021-22 not linked — next_release unknown (delayed).
disagrees_with:     Cards 1–3 (rates and survey indicators vs facility counts). NITI Health Index (rejected as record).
do_not:             Do not present as current 2026 facility stock without stating the 31 March 2022 date. Do not pull district Section II. Do not use hospital star-ratings or private insurance tables. Do not use NITI Health Index.
```

---

## Named holes (method)

- **NFHS-6 full national report** (mortality chapters) — not open-fetchable on `nfhsiips.in` this run.
- **NFHS-6 IMR/U5MR on fact sheets** — not printed; mortality of record for this slice stays on SRS Cards 1–2.
- **Manipur** on Frame C — absent from the fact-sheet set.
- **RHS after 2021-22** — not on HMIS Publications menu this run.
- **Districts** — NFHS compendiums and RHS Section II parked.

---

## Handoff

Next: Platform Architect (refresh contract) when this slice becomes a product; then Ingest. Geography frames locked. Fetch the four named PDFs only; keep SRS / NFHS / RHS separate.
