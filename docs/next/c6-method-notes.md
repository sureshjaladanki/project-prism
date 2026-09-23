# C6 method notes

Persona: Methodologist. Sleeve: **People**. Slice: **C6**.

Citizen question: Who is in school, and what does the official record say about schools?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`.

Locked inputs: [`c6-citation-cards.md`](c6-citation-cards.md), [`c6-geography-frame.md`](c6-geography-frame.md). Charter block: [`topic-charters.md`](topic-charters.md) § C6.

**UDISE+ and Census literacy are two records.** Cards 1–2 are UDISE+ Report 2025-26 (NEP Structure). Card 3 is Census 2011 PCA literacy counts. Do not merge literacy into enrolment. Do not invent a “current literacy rate from schools.”

**NEP Structure and Existing Structure are two category frames for the same year.** Cards 1–2 use NEP as primary. Do not stitch NEP and Existing Structure into one table without a break note.

**Release date is not the reference period.** PDF CreationDate 7 July 2026 is not academic year 2025-26. Census reference moment is 1 March 2011, not the NADA catalog date.

**UDISE “ASER” ≠ Pratham ASER.** Table 6.6 Age Specific Enrolment Rate uses the acronym ASER inside the UDISE booklet — enrolment rate, not the NGO learning survey (charter-out as source of record).

**Districts are parked.** National and State/UT only. Say so beside India totals.

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| Schools / enrolment / teachers | Do not stitch NEP + Existing; do not rank states; do not lead with Aadhaar-linked enrolment | UDISE+ stocks for 2025-26 as printed |
| Facilities | Do not invent a facilities index; do not confuse “having” with “functional” | School facility counts/shares as printed |
| Census literacy | Do not merge into UDISE; do not present 2011 as current | Literate counts from Census 2011; lag is the story |

---

## Card 1 — UDISE+ schools, enrolments, teachers (2025-26 NEP)

Binds: citation Card 1. Geography: **Frame A**.

```text
concept:            Stocks of schools, enrolments, and teachers at India and State/UT as published in UDISE+ Report 2025-26 NEP Structure (Tables 1, 2.1, 2.2). Not GER/NER/dropout rates (Section 6 — derived; not this card’s core).
unit:               Counts as labelled (schools; students enrolled; teachers). Zero-enrolment and single-teacher school columns are producer caveats on Table 2.2 — not nulls to fill.
population:         Schools/enrolments/teachers in the UDISE+ administrative record for academic year 2025-26. Not private learning assessments. Not board-exam candidates.
reference_period:   Academic year 2025-26. Not 7 July 2026 PDF CreationDate.
producer_definition: DoSEL UDISE+ Report 2025-26 NEP Structure booklet; companion open-services summarised-stats / edu-highlights for yearId "12". Same vintage, two fetch forms.
comparable_from:    Within UDISE+ NEP Structure for this year. Prior-year booklets are history with possible category-frame breaks — do not silent-stack onto 2025-26.
breaks:             NEP vs Existing Structure category frames (same year — do not merge). Do not recode Frame A onto Frame B. District rows parked.
lags:               Annual; next_release unknown (no 2026-27 booklet on dashboard Downloads list).
disagrees_with:     Card 3 Census 2011 literacy (different concept and decade). Existing Structure booklet (same year, different school-category frame). Pratham ASER (rejected as record).
do_not:             Do not stitch NEP + Existing into one table. Do not rank states. Do not treat Table 6.6 “ASER” as Pratham ASER. Do not lead with Aadhaar-linked enrolment. Do not present as learning outcomes. Do not pull district UDISE.
```

---

## Card 2 — UDISE+ school facilities / infrastructure (2025-26 NEP)

Binds: citation Card 2. Geography: **Frame A**.

```text
concept:            School infrastructure and facilities at India and State/UT (Table 2.5 and Section 7): toilets, drinking water, electricity, library, computers, internet, ramps, CWSN toilets, etc., as published.
unit:               Counts of schools having / functional facility as labelled; national shares in Key Results / Table 1 as printed percentages.
population:         Same UDISE+ school universe as Card 1 for 2025-26.
reference_period:   Academic year 2025-26. Not 7 July 2026.
producer_definition: Same NEP booklet as Card 1; facility fields on schools-summarised-stats / edu-highlights for yearId "12".
comparable_from:    Within this year’s NEP facility tables. “Having” and “functional” columns are different concepts.
breaks:             Having ≠ functional. NEP vs Existing Structure if both used. Do not invent a composite facilities index.
lags:               Same as Card 1.
disagrees_with:     None required among official series on this card; Card 1 is stocks of schools/enrolment/teachers, not facilities.
do_not:             Do not invent a facilities scorecard or rank states. Do not treat “having toilet” as “functional toilet” when both columns exist. Do not pull district facility extracts.
```

---

## Card 3 — Census 2011 PCA literacy counts

Binds: citation Card 3. Geography: **Frame B** (same map as C2 Frame A).

```text
concept:            Literate and illiterate population counts as published on PCA SD (`P_LIT`, `M_LIT`, `F_LIT`, and illiterate companions). Optional citizen rate uses Census definition (typically literates among population aged 7+); Methodologist: if the page shows a rate, cite the denominator columns and the producer formula — do not invent one from UDISE.
unit:               Person counts on the workbook. Rate only if computed from published columns with the Census definition stated.
population:         Census 2011 household population on India/STATE rows (TRU as published). Not school enrolment. Not 2025-26.
reference_period:   Census of India 2011 (00:00 hours, 1 March 2011). Not academic year 2025-26.
producer_definition: Census 2011 PCA SD NADA catalog 6191; literacy columns on Level = India or STATE only. Same file as C2 Card 1 population — literacy fields only for this card.
comparable_from:    2011 PCA only for this stock. No later census literacy totals published (Census 2021 totals not published; Census 2027 houselisting is not a literacy release).
breaks:             2011 map lacks Telangana STATE and Ladakh UT rows; Daman & Diu and Dadra & Nagar Haveli are separate. Do not recode onto Frame A.
lags:               About fifteen years behind 2026 and behind UDISE+ 2025-26 — the lag is the public caveat. next_release unknown (delayed).
disagrees_with:     Cards 1–2 UDISE+ (different concept: schools/enrolment vs literacy). Do not “update” literacy with enrolment.
do_not:             Do not merge into UDISE. Do not present 2011 literacy as current. Do not ingest DISTRICT rows. Do not patch with NSS or international modelled literacy.
```

---

## Named holes (method)

- **UDISE+ 2026-27** — not published; next_release unknown.
- **NSS literacy as current of record** — no clear live MoSPI series URL verified on the citation-card run; Census 2011 remains the named literacy card.
- **District UDISE** — parked by charter.
- **Flash Statistics** as a separate 2025-26 product — not verified; annual product is the UDISE+ Report booklet.

---

## Handoff

Next: Platform Architect (refresh contract) when this slice becomes a product; then Ingest. Geography frames locked. Prefer producer dashboard PDF + open-services; PCA xlsx for Card 3 literacy columns only.
