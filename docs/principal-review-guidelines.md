# Principal review guidelines

Principal (advisor; outside roster). How a citizen preview read finds fails, how those fails generalize into semantic patterns, and how to apply the patterns across the CMS desk. Charter Editor routes; this file does not amend [editorial-guidelines.md](editorial-guidelines.md), [design-system.md](design-system.md), or [web-design.md](web-design.md).

Seed notes: [citizen-page-feedback.md](archive/citizen-page-feedback.md), [cms-system-feedback.md](archive/cms-system-feedback.md). Programme: [citizen-system-change-plan.md](archive/citizen-system-change-plan.md).

```text
role:           principal (advisor; outside roster)
about:          semantic patterns for a citizen read of preview — not Trust, not a ship gate
seed:           citizen-page-feedback.md + cms-system-feedback.md (C1–C3 answer pages)
outputs:        named fails (path + what a citizen hits) + wants; hand to Charter Editor
forbids:        amending standing contracts; Trust pass/block; rewriting templates from this file
next:           charter-editor
```

---

## How Principal reads

Open preview as a person without the codebook. One question per page. Scan path:

1. **First screen** — Does the H1 get answered before the scroll? Lede, figures, cite within reach.
2. **Evidence sections** — Does each H2 further answer the question, or retype what the chips already said?
3. **Charts next to prose** — Same unit, same period, same concept? Gap visible? Machine marks gone?
4. **Method last** — Quiet, readable, no desk instructions.
5. **Shell** — Home, sleeves, top nav, `/how-this-works`, `/sources`: still a citizen product, not a desk tour.

Prefer concrete path + fail over taste. House rules still bind the advice: official sources only; show, don’t spin; context in, verdicts out. Trust owns the record; Principal names when the page *feels* like a codebook, scorecard, or unfinished printout.

---

## Propagation tests (always run)

When one fail appears, do not stop at that sentence or that chart. Run these four questions before closing the note:

| Test | Question |
|------|----------|
| **A. Same page, other sections** | Does the fail in Page · section B also appear in sections C, D, … on that page? |
| **B. Prose ↔ chart in the same section** | Does the fail in a paragraph also sit on the section’s graph, stat row, or source-line — or does the graph contradict the paragraph? |
| **C. Chart → page readability / look** | Does graph *k* hurt scan, hierarchy, or the page’s calm look? Do other charts on this page share the same waste or leak? |
| **D. Same fail, other pages** | Does Page 1 · section B’s fail also land on `/people/population`, `/prices/retail-prices`, house pages, or shared chrome? |

“Page 1 · section B · graph *k*” is conceptual. Name the real route, heading id, and chart title in the fail note.

A pattern is only a pattern when the same *citizen job* fails more than once — same page, sibling section, sibling encoding, or sibling route.

---

## Semantic patterns

Each pattern: **seed** (how it showed up), **general form**, **propagation**, **further desk hits** from applying the pattern to current C1–C3 templates and house pages. Further hits are Principal notes for Charter — not closed Trust fails and not contract patches.

### 1. Recap instead of answer

**Seed.** Answer sections restated `.stat-figure` numbers (P1). Citizen wanted change from the last published period, what was counted, and what the number *is* — not a second printing of the chip.

**General form.** Anywhere the page repeats a bound magnitude the citizen already saw in the lede, stat row, or prior section, without adding a citizen job (comparability, coverage, concept boundary).

**Propagation.**

- A → Every evidence section under the hottest rail, not only the hero.
- B → Chart that only replots the same cells the paragraph just spoke, with no new cut (sector, state, year run).
- D → Same H2 shape on money, people, and prices.

**Further hits (apply).**

- `/prices/retail-prices` `#food`: restates All India Combined food % already on the first screen.
- `/money/union` `#collect` / `#spend`: some lines correctly add concept (“gross vs net”, “two expenditure totals”); where a sentence only echoes the BE chip, it is the same recap fail.
- `/people/population` `#projection`: restates the 2026 projection already in the fact-lede — keep only the “projection ≠ census / not joined to 1901–2011” job, not the magnitude twice.

### 2. Desk voice on a citizen surface

**Seed.** “How to read” / Methodology dumped desk notes (P5, P5.b): `table 0`, “Table 8”, Frame labels, `vintage_id`, “do not fill 2025 blanks”, “districts parked”. Later: “on this desk”, `lags` / `next_release` prose, Card N (T-this-desk, T-lags-slot, T-parked, T-c8-surface).

**General form.** Any string a citizen cannot use without knowing how the desk works — parser state, catalog tokens, roster talk, internal card ids — printed in lede, evidence, source-line, chart title/tick, cite card, method, or byline.

**Propagation.**

- A → Method *and* every evidence aside that “explains the chart.”
- B → Chart title or y-axis that still says producer table code or “thousands” as desk talk.
- D → House pages (`/how-this-works`) and bylines that print the same tokens.

**Further hits (apply).**

- C1 / C2 method and evidence still say **hole** (“a hole, not zero”). Citizen phrase is **not published** (ruling 5); “hole” is desk.
- `/how-this-works`: “A hole is not filled with a remembered figure” — same desk word on a house page.
- C1 / C3 byline binds `next_release` in running chrome. Same family as closed method leaks: catalog timing on the citizen surface unless Charter names byline as an allowed quiet field.
- C2 projection `.source-line`: “projected population, **thousands**” — producer unit word on citizen chrome (family of F-c2-lakh-thousand).
- C2 `#births-deaths` / `#fertility` still carry codebook asides in evidence (“not multiplied by the 2011 headcount”; “does not print total fertility” was split — fertility section exists, but the “not × headcount” line remains evidence, not method).

### 3. One gap, many words — or a quiet lie

**Seed.** FRBM “unknown / not a table” (E-frbm-words) → one citizen phrase: **not published**. GST Compensation Cess plotted as zero (E-cess-zero / T-cess-zero). CPI 2013 “unpublished” on a source-line vs method “hole.”

**General form.** Named absence must (1) use one citizen phrase everywhere, and (2) never encode as a plotted numeric zero. Published zero and gap must stay visually and verbally distinct.

**Propagation.**

- A → Every named gap on the page (FRBM, cess, Chandigarh Rural, missing fertility geos, 2013 inflation).
- B → Chart encoding of that gap (no bar / break / label), not only the sentence beside it.
- D → Same phrase on money, people, prices, and house “when incomplete” copy.

**Further hits (apply).**

- Templates mix **hole**, **missing**, **blank**, **unpublished**, **not published**. Propagate ruling 5 to every surface, including chart captions and `/how-this-works`.
- C2 `#fertility`: “Smaller States… and districts are **missing** here” — same gap job; prefer **not published**.
- C3 method: “States… and districts are **missing**” — same.
- Trust note: IGST printed zero is a *published* zero — Principal still asks: can a citizen tell that bar from a former cess-as-zero failure without reading method? If not, the chart needs a clearer gap treatment elsewhere on the same page for contrast teaching.

### 4. Magnitude and unit must agree across encodings

**Seed.** Projection chart in thousands vs census in persons (E-c2-units). `35.27 L crore` and `14.23 L Thousand` (F-indic-unit, F-c2-lakh-thousand). Compact K / L / Cr is the whole citizen unit (cms ruling 1).

**General form.** One concept on one page → one display scale in lede, `.stat-figure`, prose observation, and chart axes. Scale token must not sit beside a leftover producer unit word. Indian grouping is part of the same job.

**Propagation.**

- B → Lede ↔ stat ↔ chart y-axis in the same section; then every other chart of that concept on the page.
- C → Overflowing ticks, rotated labels, or leftover well space often co-travel with uncompacted magnitudes (P4).
- D → Budget rupees and population headcounts are the same *display* pattern even when producers differ.

**Further hits (apply).**

- After Platform closed display_string: re-scan **source-lines and chart titles** for leftover “thousand”, “crore of rupees”, “lakh” words — C2 projection source-line still carries “thousands.”
- C2 `#births-deaths`: rates need the slot unit in the cell (E-rate-unit). Same pattern on any future rate chip (TFR is a rate — confirm unit chrome matches birth/death/IMR).
- Any new chart that joins two producer units without a method note fails this pattern even if each encoding is locally consistent.

### 5. Cite chrome is citizen, not schema

**Seed.** Citation card as field dump; geography/data vintage as labels (P2). Cite period July vs August answer (T-cite-period). Strip / source-line → panel; stack stays complete (cms rulings 2–3).

**General form.** Every cite control shows producer (linked), series as named, period, release, one readable caveat — and the period on the card must be the period of the bound figure. Machine ids stay off labels. One interaction family (panel), not three.

**Propagation.**

- A → First-screen strip, every chart `.source-line`, every stack card.
- B → In-text cite next to a number vs the chart source-line under that number’s figure.
- D → All three answer pages; `/sources` stays house index, not a per-slice dump.

**Further hits (apply).**

- C1 `#rate-over-time` source-line period cue (“2013 unpublished”) vs stack cards for the linked series — period language must still match what the chart encodes.
- C3 `#three-records` one source-line for three producers (“each record as labelled”) — citizen may not know which card the panel would open; pattern asks for one control per observation or an explicit multi-cite affordance, not a vague line.
- Re-open any card that still reads as a `<dl>` dump or repeats summary and body.

### 6. Method is one quiet block after the record

**Seed.** Methodology vs “How to read this series” overlap; multiple how-tos on `/money/union` (P5, E-money-method). Method type quieter; same `--desk` width (S2, F-method-fineprint). Fine print and rate asides shoved into evidence (E-rates-notes).

**General form.** One method region. It does not compete with the answer for weight. Evidence asides that only teach “how not to misread” belong in method unless Line can name a distinct in-section job.

**Propagation.**

- A → Count method-like H2s and “do not join / do not treat as” paragraphs in evidence.
- B → Chart footnotes living as axis marks instead of method (F-census-axis-marks).
- D → Every answer template’s `{{how-this-is-measured}}` and any leftover how-to block.

**Further hits (apply).**

- C1 `#states`: “All India is the national unit… Chandigarh Rural this month…” — national-unit line was Line-cut on an earlier pass (E-all-india-bar); Chandigarh Rural aside is method-grade.
- C2 `#where`: “India Total is the national unit above, not a bar here” — same Line candidate as prices.
- C2 `#change` / `#births-deaths`: hole and “not a headcount” sentences — method job still sitting in evidence.
- C3 `#deficit` FRBM paragraph and `#liabilities` “not debt as defined in the FRBM Act” — keep concept boundary, but long FRBM teaching may overweight method inside the answer column; check scan against ruling “method after the record.”

### 7. First screen answers “what is it *now*?” without lying about the record

**Seed.** C2 fact-lede led with Census 2011 in a 2026 read (F-c2-lede-year). Alignment of lede/prose vs graphs/stats (S1). Inline numbers at body size (F-lede-inline-type).

**General form.** The first viewport answers the H1 for a reader of *this year*, names the nature of the lead figure (projection, BE, provisional), and keeps the last hard record on the same screen when that is the honest pair. Composition shares one edge; prose numbers do not cosplay stat chips.

**Propagation.**

- A → Byline, lede, stat row, first chart, first source-lines — one composition.
- B → First chart must not contradict the lede’s concept (projection chart vs census chips without labels).
- D → Every answer hero; home fast-facts one-liners that preview a slice.

**Further hits (apply).**

- C2 hero stat row still shows **only 2011** Total/Rural/Urban while the lede leads with 2026 projection — citizen may think the big chips are “today.” Pattern: first-screen stats should include the lead answer’s magnitude or clearly label the chips as last census.
- C1 lede answers inflation *now* well; confirm provisional vs final sentence does not bury the lead.
- C3 lede correctly names Budget Estimates — apply the same “name the nature of the figure” test whenever Actuals and BE share a page.

### 8. Chart ticks and labels are citizen period / category text

**Seed.** Census years with `$` `@` `#` `+` (F-census-axis-marks). Budget ticks `end-` / `actual-` (F-axis-period-prefix).

**General form.** Axis text is what a person says aloud: year, BE/RE/Actuals phrase, state name. Producer footnote marks and machine period keys stay in caveat or lineage.

**Propagation.**

- B → Title, axis, tooltip, and data label for the same chart.
- C → Crowded or rotated ticks often hide leftover producer strings.
- D → Every multi-year or categorical chart on all slices.

**Further hits (apply).**

- Re-scan C1 state/UT and division charts for truncated or codebook category strings.
- C3 `#three-records` has no chart — if one is added later, period labels must distinguish Budget Actuals / monthly / Finance Accounts without machine prefixes.
- Any `sort` or category field that still equals a footnote-laden `reference_period` fails this pattern again.

### 9. Chart well is part of the page’s calm look

**Seed.** Vertical ticks, uncompacted numbers, leftover field (P4). Left gap on bar charts (F-chart-left-gap). Principal ask: who owns layout / font / real-estate / appeal → UI/UX presentation pass (F-chart-review-owners).

**General form.** Plot fills the card; ticks readable; same width language as the desk; no empty theatre to the left or under rotated labels. Content of titles/labels stays Content; breaks stay Methodologist; holes/cites/spin stay Trust.

**Propagation.**

- A → Every chart on the page, not the first bar chart only.
- C → One wasteful well makes the whole scroll feel unfinished.
- D → Same VL / well primitives on money, people, prices.

**Further hits (apply).**

- After left-gap fix on two money charts: run the same fill test on C1 state bars, C1 division bars, C2 state bars, C2 census line, C2 projection line, C3 deficit / liabilities / receipts.
- Long categorical labels (tax heads, CPI divisions, state names) are the usual regress — treat label overflow as the same pattern, not a new taste note.
- Top nav look (`F-site-header-nav`) is the shell cousin of this pattern: shared chrome real-estate after Front-end signs IA.

### 10. Concept boundary: do not join what the producer keeps apart

**Seed.** Rates ≠ headcount; projection ≠ census; BE ≠ Actuals; Combined ≠ desk average; gross tax ≠ tax net of States’ share; FRBM debt ≠ liabilities statement.

**General form.** Where two official numbers sit on one page, the citizen must see they are different records — in lede, section openers, chart titles, and method — without a newsroom “what it means.”

**Propagation.**

- A → Every section that could be misread as a continuation of the previous chart.
- B → Chart that draws two series as one line, or one axis that implies commensurability.
- D → Cross-slice vocabulary (“All India”, “Total”, “Combined”) must stay producer-true.

**Further hits (apply).**

- C3 `#receipts-over-time` correctly warns net vs gross — confirm the tax-heads chart title cannot be read as the same total as Annex-1.
- C2 `#change` vs `#projection`: copy says not joined; charts must stay visually separate (no shared axis implying one series).
- C1 provisional vs final months: evidence sentence is good; ensure no chart title collapses them into “latest.”

### 11. Shared chrome and house pages are in scope

**Seed.** Top-nav UI/UX (F-site-header-nav). Chart review ownership (F-chart-review-owners). Geography pages later, not thin doorways (S3).

**General form.** A citizen lands through home, sleeve, header, and how-this-works. Those surfaces can fail the same semantic patterns (desk voice, unclear answer, weak hierarchy) even when answer pages were patched.

**Propagation.**

- D → Always include `/`, sleeve indexes, header, `/how-this-works`, `/sources` in a full desk read.
- C → Header and answer wells share `--desk`; misaligned shell breaks the portrait’s one-house feel.

**Further hits (apply).**

- `/how-this-works` “hole” language (pattern 2 / 3).
- Home fast-facts: one-line teaser must not outpace the slice’s honest lead figure (e.g. imply a 2026 census).
- Sleeve hubs quiet-empty: still invitation, not a codebook empty state.

---

## Pattern → fail note (how to write it)

For Charter, each Principal fail should carry enough to route without a second read:

```text
pattern:    (id + name from this file)
where:      (route · heading id or hero · encoding: lede | p | stat | chart title | axis | source-line | cite | method | shell)
citizen:    (what they hit in one sentence)
propagate:  (A/B/C/D checks run; sibling hits listed or “cleared”)
want:       (optional; what would clear the fail)
not:        (Trust / Platform / etc. if out of Principal lane)
```

Do not open a second vision document from a Principal pass. Do not amend standing contracts here.

---

## Desk checklist (one Principal pass)

Use against preview. Mark fail only with path + pattern.

**Every answer page**

- [ ] First screen answers H1 for a reader of this year; nature of the lead figure is named (7)
- [ ] Evidence sections further the H1; no chip recap (1)
- [ ] No desk / catalog / parser voice on any citizen surface (2)
- [ ] Gaps say **not published**; never look like plotted zero (3)
- [ ] Same concept → same display unit across lede / stat / chart (4)
- [ ] Cite period matches bound figure; chrome is citizen fields (5)
- [ ] One quiet method block; method-grade asides not living in evidence (6)
- [ ] Chart ticks are citizen labels (8)
- [ ] Chart wells fill; page still looks calm (9)
- [ ] Adjacent records stay visibly distinct (10)

**Across the desk**

- [ ] Run A–D on every new fail before filing
- [ ] Compare `/money/union`, `/people/population`, `/prices/retail-prices` for shared patterns
- [ ] Shell: header, home, `/how-this-works`, `/sources` (11)

**Hand off**

```text
role:           principal (advisor; outside roster)
preview:        (base URL or desk id)
routes:         (paths read)
fails:          (pattern + where + citizen hit)
wants:          (optional)
out_of_scope:   (Trust / Platform / …)
next:           charter-editor
```

---

## Trace: seeds → patterns

| Seed (feedback id) | Pattern |
|--------------------|---------|
| P1 story / recap | 1 Recap instead of answer |
| P5, P5.b, T-this-desk, T-lags-slot, T-parked, T-c8-surface, E-table-8 | 2 Desk voice |
| E-frbm-words, E-cess-zero, T-cess-zero, ruling 5 | 3 One gap phrase / no fake zero |
| E-c2-units, E-rate-unit, F-indic-unit, F-c2-lakh-thousand, ruling 6 | 4 Magnitude & unit agreement |
| P2, P3, T-cite-period, cms rulings 2–3 | 5 Cite chrome |
| P5, E-money-method, S2, E-rates-notes, F-method-fineprint | 6 One quiet method |
| F-c2-lede-year, S1, F-lede-inline-type | 7 First screen honesty & composition |
| F-census-axis-marks, F-axis-period-prefix | 8 Citizen axis labels |
| P4, F-chart-left-gap, F-chart-review-owners | 9 Chart well / look |
| E-rates-notes, F-c2-lede-year, C3 gross/net & BE/Actuals copy | 10 Concept boundary |
| F-site-header-nav, S3, house pages | 11 Shared chrome & house |

---

## Out of this file

- Trust pass/block, cite URL audits, cell spot-checks.
- Contract patches to editorial, design-system, or web-design.
- Scheduling (see [citizen-system-change-plan.md](archive/citizen-system-change-plan.md)).
- Inventing geography doorways or a twelfth persona.
