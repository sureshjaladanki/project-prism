# C4 method notes

Persona: Methodologist. Sleeve: **Work**. Slice: **C4**.

Citizen question: How many people are working, seeking work, and what do they earn?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`.

Locked inputs: [`c4-citation-cards.md`](c4-citation-cards.md), [`c4-geography-frame.md`](c4-geography-frame.md). Charter block: [`topic-charters.md`](topic-charters.md) § C4.

**PLFS only.** Not CMIE. Not MGNREGA (C9). Do not mix person-days with unemployment rates.

**Usual status (ps+ss) ≠ Current Weekly Status (CWS).** Both appear on Card 3. Never merge into one rate. Cards 1–2 are CWS only.

**January 2025 design break.** Monthly/quarterly series and the calendar-year 2025 annual sit under the revamped design (`PLFS_Changes-in-2025_rev.pdf`). Do not stitch pre-2025 urban-only quarterlies or July–June annuals as continuous without a break note.

**Release date is not the reference period.** Press note 15 September 2026 is not August CWS. Press note 27 March 2026 is not calendar year 2025.

**Three earnings concepts on Card 4.** Regular wage/salary, casual labour per day, and self-employment gross earnings have different reference periods — not one “average wage.”

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| Monthly CWS | Do not invent State rows; do not stitch pre-2025 | All-India LFPR, WPR, UR for the month (CWS) |
| Quarterly CWS | Do not fill missing States from the annual | CWS rates for all-India and selected States |
| Annual LFPR/WPR/UR | Do not merge usual and CWS | Calendar-year 2025 rates; usual and CWS both published |
| Annual earnings | Do not invent one wage across statuses; not MGNREGA | Regular, casual, and self-employment earnings as defined |

---

## Card 1 — PLFS Monthly Bulletin (CWS, all-India)

Binds: citation Card 1. Geography: **Frame A**.

```text
concept:            Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), and Unemployment Rate (UR) in Current Weekly Status (CWS) for all-India, by sector / gender / broad age as published.
unit:               Rates as labelled (percent).
population:         Persons in the PLFS monthly sample under CWS (7-day reference). Not usual status. Not State/UT rows.
reference_period:   Calendar month of the bulletin (August 2026 on this card). Not 15 September 2026 release.
producer_definition: PLFS Monthly Bulletin (NSO/MoSPI product 69). Post-January-2025 monthly series (this card: seventeenth bulletin from April 2025).
comparable_from:    Within post-January-2025 monthly CWS bulletins. Break vs any pre-2025 monthly product.
breaks:             CWS only — usual status not on this card. No State/UT. No companion XLSX on this release (PDF statements). Design revamp January 2025.
lags:               next_release 15 October 2026 (Sep 2026 bulletin) per ARC 2026-27.
disagrees_with:     Card 3 usual status (different concept). Card 2 (selected States, quarterly). CMIE (rejected).
do_not:             Do not invent State/UT rows. Do not merge with usual status. Do not mix MGNREGA. Do not use CMIE. Do not pull districts.
```

---

## Card 2 — PLFS Quarterly Bulletin (CWS, selected States)

Binds: citation Card 2. Geography: **Frame B**.

```text
concept:            LFPR, WPR, UR (and related CWS worker-distribution tables) for all-India and selected States, rural and urban.
unit:               Rates as labelled; absolute worker counts if used are derived with MoHFW projected population — cite that dependency.
population:         PLFS quarterly CWS sample; publisher “selected States” only on Appendix A.
reference_period:   Quarter as labelled (April–June 2026 on this card). Not 10 August 2026 bulletin date.
producer_definition: PLFS Quarterly Bulletin (NSO/MoSPI); Appendix A Excel Tables 1–5.
comparable_from:    Within post-January-2025 rural+urban quarterly bulletins for the published State list.
breaks:             Selected States only — missing States/UTs are not published here. Pre-2025 urban-only quarterlies are a different series. Do not fill holes from Card 3.
lags:               next_release 10 November 2026 (July–Sep 2026) per ARC.
disagrees_with:     Card 1 (monthly, all-India only). Card 3 (annual, all State/UT, includes usual status).
do_not:             Do not fill missing States from the annual report. Do not merge with usual status. Do not mix MGNREGA/CMIE. Do not pull districts.
```

---

## Card 3 — PLFS Annual Report: LFPR, WPR, UR (usual ps+ss and CWS)

Binds: citation Card 3. Geography: **Frame C**.

```text
concept:            LFPR, WPR, UR in usual status (ps+ss) and in CWS; related employment-status tables as published for calendar year 2025.
unit:               Rates as labelled.
population:         PLFS annual sample; each State/UT as in Appendix A. Absolute counts using MoHFW projections are derived — cite if used.
reference_period:   January–December 2025. Not 27 March 2026 press note.
producer_definition: Annual Report PLFS 2025 (NSO/MoSPI); Appendix A Tables 16.0/17.0/18.0 (usual) and 30/31/32 (CWS).
comparable_from:    Within calendar-year 2025 annual under revamped design. Break vs earlier July–June PLFS annuals.
breaks:             Usual status ≠ CWS — publish both, never average into one. First calendar-year annual under new design.
lags:               Next annual on ARC for calendar year 2026 (detailed report + unit level — unit level is Category B, not this card’s path).
disagrees_with:     Cards 1–2 (CWS frequency/geography). Card 4 (earnings, same publication).
do_not:             Do not merge usual and CWS. Do not stitch to pre-2025 July–June annuals without a break. Do not use to fill Card 2’s missing States as if quarterly. Do not pull microdata or districts for this path.
```

---

## Card 4 — PLFS Annual Report: wages and earnings

Binds: citation Card 4. Geography: **Frame C**.

```text
concept:            Average earnings from (1) regular wage/salaried employment, (2) casual labour (other than public works), and (3) self-employment — as defined in the Annual Report.
unit:               Rupees as labelled for each table (monthly / per day / last 30 days gross — follow the table).
population:         Earners in each status as defined; State/UT and sector as in Tables 38–40. Cell 0 can mean no sample observation (Table 38 note).
reference_period:   Calendar year 2025 survey; earnings windows differ by status (regular: preceding calendar month in CWS; casual: per day in the week; self-employed: last 30 days gross).
producer_definition: Appendix A Tables 38–40; Annual Report Section Four (*Earnings from employment*).
comparable_from:    Within each earnings table separately. Not across statuses as one wage.
breaks:             Three concepts, three reference windows. Public works / MGNREGA wages are not this card (C9).
lags:               Same annual cycle as Card 3.
disagrees_with:     CMIE wage series (rejected). MGNREGA wage notifications (C9).
do_not:             Do not invent a single average wage across statuses. Do not chart MGNREGA as PLFS earnings. Do not use CMIE. Do not treat 0 as a real zero wage without the producer note.
```

---

## Named holes (method)

- **Monthly has no State/UT** — high-frequency state picture is Card 2 (selected) or Card 3 (annual).
- **Quarterly selected States only** — do not fill from Card 3.
- **January 2025 design break** — state explicitly on any long run.
- **Hashed MoSPI upload paths** — re-resolve via product 69 when refreshing.
- **No monthly Excel** on Card 1 this release — PDF only.
- **Districts** — Selected Districts snapshot parked.

---

## Handoff

Next: Platform Architect (refresh contract) when this slice becomes a product; then Ingest. Geography frames locked. PLFS aggregates only (GSDD Category A); no Category B unit-level for this path.
