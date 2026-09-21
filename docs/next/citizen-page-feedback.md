# Citizen-page feedback

Charter Editor. Principal notes recorded 2026-09-20 against preview (`localhost:4321`) on `/money/union`, `/people/population`, and `/prices/retail-prices`. This file routes the notes to personas. It does not amend [editorial-guidelines.md](../editorial-guidelines.md), [design-system.md](../design-system.md), or [web-design.md](../web-design.md) until the named owner acts.

Related: first-screen look and column width stay in [ui-ux-feedback.md](ui-ux-feedback.md). Catalog-scale ingest/vintage already has an execution plan: [catalog-ingest-pipeline-plan.md](catalog-ingest-pipeline-plan.md). This file is copy, cite chrome, chart encoding, method, pipeline jargon, geography pages, ingest accuracy, and generic parsers.

```text
about:          preview answer pages vs a citizen who should not need the codebook
wanted:         a story-shaped explainer; cites that lead to the producer; charts that fit; method without desk notes; one ingest/vintage machine
got:            restated .stat-figure numbers; citation field dumps; ingest/desk jargon on the page; holes plotted as zero; per-charter Python parsers
forbids:        newsroom plot; “what this means” as a ministry verdict; hiding a hole or a cite; doorway state pages; a twelfth persona; YAML as a second programming language
status:         routing only; standing contracts not reopened here
next_persona:   content-editor (lead on story and jargon); then methodologist, ui-ux-developer, platform-architect as named below
```

## Charter rulings

These clashes are decided here so owners do not invent a second vision.

1. **Evidence is an explainer, not a recap and not a news piece.** Sections must further answer the H1: bound change from the previous published period, what was counted, who, when, and how the published series got to this point. They must not retype the `.stat-figure` cells. They must not explain *why the government did it*, forecast, or tell the reader what to think. “What it means to the reader” is what the number *is* (a rate is not a headcount; Budget Estimates are not actuals). It is not a takeaway about a ministry.

2. **One citizen method block.** Merge “How to read this series” into Methodology unless Content Editor Development can name a distinct citizen job that Methodology does not already do. Method sits after the record and is quieter than the answer. Desk `do_not` lines stay in [method notes](../archive/c1-method-notes.md), not on the page.

3. **Cite chrome is for the citizen; schema fields stay in the vintage.** The open card shows producer (linked to the citation `url`), series as the producer names it, reference period, release date, and one readable caveat. `geography_vintage` and `vintage_id` stay on the observation and in `data-vintage-id`. They are not citizen labels. A tooltip is still not enough. A closable panel may *mirror* the on-page card; it must not replace it or leave the view (standing [design-system.md](../design-system.md) cite rule).

4. **Ingest keeps the producer’s table. The page does not.** Derived CSV stays replayable against the artifact (sheet, table, cell). Pipeline writes house `series_id` and citizen citation/caveat fields. Content Editor never prints parser names (`table 0`), Frame labels, annex codes, or “Table 8” in running copy. The librarian card may still name the producer table so a stranger can fetch it.

5. **One citizen phrase for a gap: “not published”.** Schema status stays `unknown` / `withheld` / `delayed` / `withdrawn` / `not_comparable` / `series_break`. Running copy and chart labels do not say hole, missing, or unknown. “Named hole” remains desk language in refresh contracts. Unknown is never plotted as zero.

6. **Compact Indian display units are in, at bind.** Lede, `.stat-figure`, and chart axes use one format. Vintage `unit` stays what the producer printed. Compact form (thousands `K`, lakhs `L`, crores `Cr`) is a display token, not a rewrite of Parquet. Two charts of the same concept on one page use the same display unit.

7. **Geography pages are in, later, as full slices.** `/{sleeve}/{slice}/{geo}` is already reserved. Do not ship a number-only doorway. Not in this feedback batch’s first pass. Charter names which slices when Front-end Architect reopens the “now” tree.

8. **No `ingest-auditor` persona.** Accuracy of raw → derived is a required **ingest accuracy gate**, not a twelfth roster member. Ingest Engineer owns golden/fixture tests (derived cells still map to the artifact). Methodologist signs the first parse of a new table shape (`derived_path` is the producer’s table). Trust Auditor may spot-check cells on ship and still requires the raw file; it does not become a second ingest engineer. Do not add `.cursor/agents/ingest-auditor.md`.

9. **One ingest runner and one vintage runner; parsers by format and table shape, not by C-number.** Per-charter Python types (`pipeline/c1.py`, `parse_c2.py`, `parse_c3.py` as the *unit of work*) are out. Catalog YAML wires identity (slice, artifact, `parser_id`, `mapper_id`). Shape families — `xlsx-table`, `html-table`, `pdf-table` — are shared code. A new charter that reuses a shape is a catalog file. A new layout is one new parser/mapper family. YAML does not encode header offsets, merged-cell rules, or “if this charter then”. Stop if the PDF/HTML is ambiguous; do not ship one guess-all parser. Standing plan: [catalog-ingest-pipeline-plan.md](catalog-ingest-pipeline-plan.md).

---

## How to read this file

**Lead** does the pass. **Parties** must act or sign before that item is done. Trust Auditor runs on anything a citizen will see; Charter Editor ships or blocks. Those two are implied on every citizen-facing row and listed only when the fail is already a Trust-class record problem.

---

## By persona

### Content Editor

Standing file: [editorial-guidelines.md](../editorial-guidelines.md). Run Development → Line → Copy → Proof on C1–C3. Several items below are already required by that file and failed on preview.

| Id | Feedback | Also |
|----|----------|------|
| P1 | Answer sections restated `.stat-figure` numbers. Write evidence that further answers the H1: previous published period (bound slot), what the series counts, and what the number is for a citizen. No recap, no verdict, no causal “why” the vintage cannot bind. | Methodologist (comparability of the prior period); Trust (spin) |
| P5 | “Methodology” and “How to read this series” overlap; How-to-read dumps desk notes. One method block after the record. Drop or rewrite every desk sentence (do not fill 2025 blanks; districts parked; HTML table 0). | Methodologist (citizen caveat vs `do_not`) |
| P5.b | Hide desk jargon and naming from the rendered view; run the four editorial passes so the page reads for this desk’s audience. Already the jargon test in the guidelines. Fail if “Table 8”, `table 0`, Frame labels, or `vintage_id` appear in lede, evidence, source-lines, or chart titles. | — |
| S2 | Method must not look as prominent as the answer. Development keeps method after the record; do not restyle type. | UI/UX Developer (type scale) |
| E-money-method | Multiple “How to read this series” sections on `/money/union`. Development: one method, or named citizen jobs — not a codebook tour. | — |
| E-frbm-words | “The FRBM statutory packet for this Budget is unknown / not a table.” Citizen copy: **not published**. Same phrase on every named gap. | Methodologist; Platform Architect (status, not labels) |
| E-table-8 | “Table 8 prints 14,23,435 thousand people…” Producer table ids stay on the librarian card, not in the explainer. | Source Librarian (card `id` unchanged) |
| E-rates-notes | “They are not multiplied by the 2011 headcount” and “Rates are not how many people live in India / this bulletin does not print total fertility.” Fine print in Methodology, not as evidence asides. Do not invent a second chrome type for these sentences. | UI/UX Developer only if Proof names a form-factor for method asides |
| E-all-india-bar | “All India is the national unit above, not a bar here.” Line pass: skip. The States/UTs chart title already says that. | — |
| E-rate-unit | Birth/death/mortality `.stat-figure` values need the slot unit in the cell (per thousand, percent — as published). Do not imply a unit the observation does not have. | UI/UX Developer (stat chrome); Pipeline Engineer if `unit` is missing on the observation |
| E-c2-units | Projection chart in thousands vs census chart in units, same concept on one page. Chart titles and bind display unit must match. | Methodologist (producer units); UI/UX Developer (axis format) |

**Does not:** restyle charts, invent a slug, rewrite ingest parsers, or hide a hole to read friendlier.

### Methodologist

Standing files: slice method notes ([c1-method-notes.md](../archive/c1-method-notes.md), [c2-method-notes.md](../archive/c2-method-notes.md), [c3-method-notes.md](../archive/c3-method-notes.md)).

| Id | Feedback | Also |
|----|----------|------|
| P1-compare | Say whether the previous recorded period is comparable (provisional vs final, BE vs RE vs actuals, base-year break). Content Editor cannot bind a change the caveat forbids. | Content Editor; Pipeline Engineer (slots) |
| P2-caveat | Caveat on the citizen card is one comprehensible paragraph (concept, unit, coverage, the live break). Not disconnected `do_not` phrases. Split the note: **citizen caveat** vs **desk `do_not`**. Only the first may render. | Content Editor; Platform Architect if the schema cannot store two surfaces |
| P5-leak | Desk instructions leaked onto `/prices/retail-prices` and `/money/union` (do not fill 2025 blanks; table 0). Those stay in `do_not`. Rewrite the citizen caveat so Pipeline is not forced to attach parser talk. | Ingest Engineer (stop putting parser state in derived comments that Pipeline copies); Pipeline Engineer |
| P7-signoff | First parse of a new table shape: open `derived_path` against the raw artifact and sign that it is the producer’s table (Ingest Engineer “done when”). Not a standing extra agent. | Ingest Engineer |
| E-frbm | Card 8 / FRBM remains a named gap. Citizen wording is **not published**, not “unknown / not a table.” | Content Editor; Charter (ruling 5) |
| E-c2-units | Producer unit of each C2 population series (thousands vs persons). Do not join them as one line without a unit note. Display compact form is bind, not a new observation. | Content Editor; UI/UX Developer |

**Does not:** forecast why prices rose; fill FRBM from a non-table; smooth GST Compensation Cess.

### UI/UX Developer

Standing file: [design-system.md](../design-system.md). Presentation pass on every template that reached Proof. First-screen width and welcome tone: [ui-ux-feedback.md](ui-ux-feedback.md) — do not duplicate that work here.

| Id | Feedback | Also |
|----|----------|------|
| P2-chrome | `.citation-card` is a field dump: summary repeats the `<dl>`; Geography vintage and Data vintage shown as citizen rows. Open state: producer (link), series, period, released, caveat. No duplicate fields. No vintage ids as labels. | Platform Architect (which citation fields bind to chrome); Content Editor (caveat prose) |
| P3 | In-text cites open that observation’s card in a closable panel, same bound fields. The on-page card / `.source-stack` stays. No request-time fetch. Amend Interaction in the design system if a panel is added; do not replace `<details>` with a fly-out that leaves the view. | Front-end Architect only if this becomes a new page type (it must not) |
| P4 | Chart wells waste width: vertical tick labels, uncompacted large numbers, leftover field. Axis ticks horizontal where they fit; compact K / L / Cr per ruling 6; plot fills the card. Standing boxes: well filled, 12px floor, one `plotWidth`, number agreement. | Content Editor (format convention at bind) |
| S1 | `.fact-lede` and body `<p>` do not share an edge with graphs and `.stat-row`. Same item as [ui-ux-feedback.md](ui-ux-feedback.md) “one width on the first screen.” Fix there. | — |
| S2-type | Methodology type is quieter than answer H2 / fact-lede. Not a second house. | Content Editor (scan path) |
| E-cess-zero | `/money/union` — GST Compensation Cess is a gap, plotted as zero. **Never plot `unknown` as zero** (already in the design system). Fail the presentation pass. | Pipeline Engineer (observation `status`); Trust Auditor |
| E-compact | Population and Budget figures: compact display in lede, stat, and axes. Stat cells must still fit. | Content Editor (convention); Platform Architect if bind format is unspecified |

**Does not:** write the explainer, invent geography slugs, or pass the record on taste.

### Front-end Architect

Standing file: [web-design.md](../web-design.md).

| Id | Feedback | Also |
|----|----------|------|
| S3 | Vintages with Union and state rows should also generate state-specific pages (USAFacts role, not costume). Geography slice is already **later**: `/{sleeve}/{slice}/{geo}`, same template bound to one unit, no doorway pages, no LGD code in the path. Reopen the “now” tree only when Charter names the slices. | Charter Editor; Geography Steward; Content Editor; Platform Architect; UI/UX Developer (implement after the contract) |

**Does not:** run the presentation pass, write citizen questions, or add `/answers/`.

### Platform Architect

Standing files: [data-contracts.md](../data-contracts.md), [architectural-blueprint.md](../architectural-blueprint.md).

| Id | Feedback | Also |
|----|----------|------|
| P2-schema | Citation chrome is dumping internal fields because the bind treats every card field as citizen. Name a **citizen citation surface** (producer, series, url, reference period, release date, caveat prose) vs machine fields (`citation_id`, `geography_vintage`, `vintage_id`). Do not drop required fields from the vintage. | UI/UX Developer; Source Librarian (url already on the card) |
| P5.a-contract | Ingest output stays producer-shaped. Vintage citizen fields do not carry parser names. If caveat currently has one blob, split citizen vs `do_not` so Pipeline cannot attach desk notes to the page. | Methodologist; Pipeline Engineer |
| S3-catalog | Geography routes are a catalog of bound units from **this** vintage, completeness still atomic, no thin pages. Refresh contract before anyone builds folders. | Front-end Architect; Pipeline Engineer |
| P6 | Avoid per-charter Python types (C1, C2, C3). One ingest module, one vintage module. Generic YAML / html-to-table / pdf-to-table / xls-table parsers for every charter. **In:** one runner each; catalog YAML as identity; parsers registered by format + table shape and reused across slices. **Out:** `C1Page` types; copying `pipeline/c3.py` for C4; YAML that needs an `if` to mean anything; one PDF parser that guesses every ministry layout. Execute [catalog-ingest-pipeline-plan.md](catalog-ingest-pipeline-plan.md); do not open a second plan. | Ingest Engineer (shape parsers); Pipeline Engineer (shape mappers); Charter Editor (ruling 9) |

**Does not:** author copy or chart chrome. Does not write a second catalog plan.

### Ingest Engineer

Standing file: [data-pipeline.md](../data-pipeline.md) Stage 1.

| Id | Feedback | Also |
|----|----------|------|
| P5.a-ingest | Do **not** rewrite the derived table into citizen nicknames. Keep producer columns, sheet/table mapping, and lineage so a retrieve can replay. Stop leaking parser state (`table 0`, merged-cell reconstruction notes) into anything Pipeline might copy onto a caveat. Put that in lineage/flags, not in a citizen-bound field. | Pipeline Engineer; Methodologist |
| P7 | Do we need an ingest-auditor who verifies raw → derived? **No new persona.** Own the **ingest accuracy gate**: fixture bytes in `tests/` must still equal the derived cells; `lineage.flags` on mismatched totals / ambiguous pages; stop rather than guess. Register parsers by shape under the one ingest runner (P6), not as `parse_c2.py` forever. | Methodologist (first-layout sign-off); Platform Architect (runner); Trust Auditor (spot-check on ship, not a cell-by-cell second parse) |

**Does not:** hide the producer’s table names; that would break replay. Does not invent `ingest-auditor`.

### Pipeline Engineer

Standing file: [data-pipeline.md](../data-pipeline.md) Stage 2.

| Id | Feedback | Also |
|----|----------|------|
| P5.a-vintage | Map derived tables to house `series_id` and citizen citation/caveat fields. Do not copy ingest parser jargon, Frame labels, or sheet indexes into rendered caveat text. | Ingest Engineer; Methodologist |
| P6-mappers | One vintage runner. Register mappers by table shape (`state-sector-period`, `wide-measure-columns`, …), not `pipeline/c1.py` as the charter. A reused shape is a catalog `mapper_id`. | Platform Architect; Ingest Engineer |
| E-cess-status | If GST Compensation Cess is a gap, the observation `status` must not be a numeric zero. Charts follow status. | UI/UX Developer; Trust Auditor |
| E-unit | Every bound stat carries `unit` from the observation. Rates are not unitless. | Content Editor |

**Does not:** change a definition or impute the FRBM packet.

### Source Librarian

Launch the Cursor agent. Do not play this role in the parent.

| Id | Feedback | Also |
|----|----------|------|
| P2-url | Citation cards already carry `url`. Confirm each live card’s url is the producer page or artifact a citizen can open — not an internal path. Do not rewrite series names for tone. | UI/UX Developer (link in chrome) |
| E-table-8 | Keep producer table ids on the card (`id`). They must not migrate into template copy. | Content Editor |

### Geography Steward

| Id | Feedback | Also |
|----|----------|------|
| S3-frame | When Charter opens geography pages, the unit list and English kebab names come from the existing geography frames — not from today’s map pasted onto an old table. | Front-end Architect; Pipeline Engineer |

Not in the first pass of this batch.

### Trust Auditor

Launch the Cursor agent on the next citizen-facing preview after the owners above act. Extra fail notes from this feedback (already on the checklist):

- GST Compensation Cess plotted as zero (smoothed hole).
- Desk `do_not` and parser talk on the page (page is not a published method note; it reads as if the desk were the statistical office).
- Verdict or causal “why” if Content Editor overshoots P1.
- Spot-check: a bound figure still matches the producer cell in the kept raw artifact. Fail the parse back to Ingest Engineer. Do not become ingest-auditor.

A form-factor fail (whitespace, alignment, method type size) is **not** Trust. A missing golden test for a new parser is **not** Trust — that is the ingest accuracy gate.

---

## Multi-party items (lead first)

| Item | Lead | Parties |
|------|------|---------|
| Story-shaped evidence, not a recap | Content Editor | Methodologist, Trust Auditor, Charter Editor (ruling 1) |
| Citation card: producer link, no vintage labels, readable caveat | UI/UX Developer | Platform Architect, Methodologist, Source Librarian, Content Editor |
| In-text cite → closable panel, card remains on page | UI/UX Developer | Platform Architect (bind citation_id), Front-end Architect (only if IA is invented — refuse) |
| Compact K / L / Cr + horizontal ticks + filled wells | UI/UX Developer | Content Editor (convention), Methodologist (producer unit), Pipeline Engineer (unit on observation) |
| One method block; no desk notes on the page | Content Editor | Methodologist, Pipeline Engineer, Ingest Engineer |
| Hide source/desk jargon by layer | Charter Editor (ruling 4) | Ingest Engineer (keep producer table), Pipeline Engineer (house fields), Content Editor (rendered view) |
| Gap language = “not published”; never plot as zero | Methodologist | Content Editor, Platform Architect, UI/UX Developer, Pipeline Engineer, Trust Auditor |
| Same concept, same display unit (C2 population charts) | Content Editor | Methodologist, UI/UX Developer |
| Method quieter than the answer | Content Editor (placement) | UI/UX Developer (type) |
| Lede/prose vs chart/stat alignment | UI/UX Developer | see [ui-ux-feedback.md](ui-ux-feedback.md) |
| Union + state pages | Front-end Architect | Charter Editor, Geography Steward, Platform Architect, Content Editor, UI/UX Developer, Pipeline Engineer |
| Ingest accuracy (raw → derived) without a new persona | Ingest Engineer | Methodologist (first-layout sign-off), Trust Auditor (spot-check on ship), Charter Editor (ruling 8) |
| One ingest + one vintage runner; shape parsers (YAML / HTML / PDF / XLS) | Platform Architect | Ingest Engineer, Pipeline Engineer, Charter Editor (ruling 9) |

---

## Trace from the principal’s list

### Primary

| # | Ask | Route |
|---|----------------|--------|
| 1 | Analyze data into a meaningful story (why now, how we got here, change from last period, what it means) | **Content Editor** + **Methodologist**; Charter ruling 1 clips newsroom “why” and verdict “means” |
| 2 | Citation card is an internal dump; duplicate summary/`<dl>`; vintage ids; link the producer; caveat must read as prose | **UI/UX Developer** + **Platform Architect** + **Methodologist** + **Source Librarian** |
| 3 | Data cites open the citation card as a closable side-panel | **UI/UX Developer**; card stays on the page |
| 4 | Chart whitespace; axis orientation; K / L / Cr | **UI/UX Developer** + **Content Editor** |
| 5 | Methodology vs How to read; desk internals on the page | **Content Editor** + **Methodologist** |
| 5.a | Hide source jargon from later pipeline stages | **Ingest Engineer** (do not rename the producer table) + **Pipeline Engineer** (do not copy parser names into the vintage citizen fields) + **Platform Architect** |
| 5.b | Content Editor hides desk jargon and runs Development + Line + Copy + Proof + Visual | **Content Editor** (four writing passes) + **UI/UX Developer** (presentation / visual pass — not a fifth writing pass) |
| 6 | Ingest-auditor persona to verify raw → derived | **Ingest Engineer** (accuracy gate) + **Methodologist** + **Trust Auditor** (spot-check). Charter ruling 8: **no new persona** |
| 7 | Avoid per-charter Python types; one ingest and one vintage module; generic YAML / html-to-table / pdf-to-table / xls-table parsers | **Platform Architect** ([catalog-ingest-pipeline-plan.md](catalog-ingest-pipeline-plan.md)) + **Ingest Engineer** + **Pipeline Engineer**. Charter ruling 9 |

### Secondary

| # | Ask | Route |
|---|----------------|--------|
| 1 | Fact-lede and `<p>` alignment vs graphs and `.stat-row` | **UI/UX Developer** ([ui-ux-feedback.md](ui-ux-feedback.md)) |
| 2 | Methodology less prominent than answer paragraphs | **Content Editor** + **UI/UX Developer** |
| 3 | Union pages plus state-specific pages | **Front-end Architect** + **Charter Editor** + **Geography Steward** + **Platform Architect** + **Content Editor** + **UI/UX Developer** |

### Examples (map to the page that carries them)

Principal listed some C2 items under `/money/union`. They are routed by what the page actually prints.

| Example | Page | Route |
|---------|------|--------|
| Large counts in K / L / Cr (Budget figures; also population counts) | `/money/union`, `/people/population` | UI/UX Developer, Content Editor |
| Birth/death/mortality figures without a unit | `/people/population` | Content Editor, Pipeline Engineer |
| Tax by major head — GST Compensation Cess as a gap, drawn as zero | `/money/union` | UI/UX Developer, Pipeline Engineer, Trust Auditor |
| How to read this series — several sections | `/money/union` (and C1/C2 if repeated) | Content Editor |
| FRBM “unknown / not a table” — many words for one gap | `/money/union` | Content Editor, Methodologist (ruling 5) |
| “Table 8 prints…” | `/people/population` | Content Editor; Source Librarian keeps Table 8 on the card |
| Rates not × 2011 headcount; rates are not headcount; no TFR | `/people/population` | Content Editor → Methodology |
| Projection chart in thousands vs census chart in units | `/people/population` | Content Editor, Methodologist, UI/UX Developer |
| “All India is not a bar here” | `/prices/retail-prices` | Content Editor Line (cut) |
| Do not fill 2025 blanks; districts parked | `/prices/retail-prices` | Methodologist `do_not`; Content Editor drops from the page |
| Monthly accounts reconstructed from HTML table 0 | `/money/union` | Ingest Engineer lineage; Pipeline/Content drop from the page |

---

## Order of work

One persona per parent pass.

1. **Methodologist** — citizen caveat vs `do_not`; C2 units; FRBM as not published; C1/C3 leaked notes pulled off the citizen surface.
2. **Platform Architect** — citizen citation surface; optional split caveat fields; compact format at bind (if not already a theme token). Parallel track: one ingest/vintage runner and shape parsers ([catalog-ingest-pipeline-plan.md](catalog-ingest-pipeline-plan.md)); do not start a third plan.
3. **Ingest Engineer** then **Pipeline Engineer** — parser talk in lineage/flags only; `status` not zero for gaps; house fields on the vintage; ingest accuracy gate (fixtures, not a new agent).
4. **Content Editor** — four passes on C1–C3 (P1, P5, P5.b, examples).
5. **UI/UX Developer** — cite chrome, in-text panel, charts, method type; plus [ui-ux-feedback.md](ui-ux-feedback.md) alignment. Presentation pass.
6. **Trust Auditor** — then Charter Editor ship or block.

**S3 geography pages** wait for a separate Charter slice after Front-end Architect amends [web-design.md](../web-design.md). They are not a gate on the rows above.

## Out of this file

- USAFacts costume, search, chat, ISR.
- Causal policy stories and “what this means” as a score.
- Renaming producer tables at ingest.
- A new `ingest-auditor` persona or Cursor agent.
- One guess-all PDF/HTML parser; YAML as parser instruction.
- Shipping thin state URLs.
- Flipping `citizen_pointer`.
- Rewriting [design-system.md](../design-system.md) for welcome/alignment — done 2026-09-20; implementation is [ui-ux-change-plan.md](ui-ux-change-plan.md) Phase E.
