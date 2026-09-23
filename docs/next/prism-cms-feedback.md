# Prism CMS feedback

Desk / Principal notes after the rethink close-out ([prism-cms-rethink.md](prism-cms-rethink.md)) and a USAFacts answer-page comparison. Routes open questions. Does **not** amend standing contracts until Charter names owners and a wave. Preview desk and `citizen_pointer` are out of scope here.

```text
about:          story-shaped how/why/what analysis (USAFacts-shaped); insight
                push; method naming; citations available on demand in a
                side-panel (need not sit on the page); source grouping /
                compact cards; methodology reading width
source:         desk read 2026-09-22 after USAFacts vs Prism comparison;
                live templates C1–C3; design-system v4 `--measure` on method
status:         open — no rulings yet
forbids:        inventing figures; replacing the agency cite; spin / partisan
                scorecard; engagement SDK; amending contracts from this file alone
next_persona:   Charter Editor (triage) → Content Editor / UI/UX / Platform as
                named below
```

Related: [usafacts-profile.md](../usafacts-profile.md), [editorial-guidelines.md](../editorial-guidelines.md), [design-system.md](../design-system.md), archive [cms-system-feedback.md](../archive/cms-system-feedback.md) (ruling 4 on method width).

---

## Open feedback

### F-insight-push — story-shaped how / why / what (USAFacts-shaped)

**Wanted.** Answer pages may need to **analyze the how, why, and what of the stats** and present that analysis **story-shaped** the way [usafacts.org](https://usafacts.org/) does on answer pages — not a codebook dump and not a chip recap.

| Layer | Job on the page |
|-------|-----------------|
| **What** | The spoken answer and the bound figure (already R1 / thesis + stats) |
| **How** | How the number moves, compares, or breaks down (evidence sections with further citizen questions, charts that further answer) |
| **Why** | Why the reader is looking at *this* cut of the record — short, bound insight clauses (composition, drivers named only when the producer series supports them; never party- or ministry-causal spin) |

**Insight-forward evidence.** Section heads and short clauses that land a takeaway (“headline was higher than core”; “food led the basket”), as USAFacts often does, bound to official series. Still not a ministry verdict, partisan scorecard, or newsroom essay genre.

**Tension with the rethink.** [prism-cms-rethink.md](prism-cms-rethink.md) §2 refused “insights” *as a genre* and adopted only the bound “what changed” sentence. This item **reopens** that refuse for Charter: allow story-shaped how/why/what analysis and insight *clauses* on evidence sections (and optionally one short closing line after the well) while keeping advocacy, “Now what?”, and unbound narrative out. Reference shape: [usafacts-profile.md](../usafacts-profile.md).

**Does this mean more ingest / more data points?**

| Case | Need new ingest? | Who |
|------|------------------|-----|
| Reframe already-bound slots (movement, food vs general, rural vs urban, extrema already in the vintage) | **No** — Content Editor + Methodologist wording; same vintage | Content Editor |
| Story beat needs a comparison the page cannot bind today (extra period, dual series, a series not on the charter, a derived table not in the vintage) | **Yes** — Charter names the dependency; Source Librarian cites; Ingest / Pipeline extend the vintage; then Content binds | Charter → Librarian → Ingest → Pipeline |
| Rank / “led” / top-five when the chart caption is a rank question | Only if the measure-order or extrema are **not** already in the vintage | Methodologist signs; Pipeline if missing |

**Default answer for this wave:** start with story-shaped how/why/what on **existing** C1–C3 slots (no blanket ingest expansion). Open a data dependency only when a named story beat fails because the observation is missing — not because the sentence is soft.

| Owner | Job |
|-------|-----|
| Charter Editor | Reopen or hold the rethink “insights as genre” refuse; ship/block how/why/what scope |
| Content Editor | Draft story-shaped sections and insight clauses that stay slot-bound; keep R1–R6 and no decoder ring above the fold |
| Methodologist | Sign comparability; block causal “why” the series cannot support |
| Trust Auditor | Spin / invented figures / hole-vs-zero before citizen see |

---

### F-method-name — “method” vs “Methodology”

**Observation.** Contracts and philosophy say **method** (last, quiet). Templates and the citizen H2 say **Methodology**. The layout token is `how-this-is-measured` / `.how-measured`. Three names for one block.

**Question.** Is that confusing or redundant for the reader (and for the crew)?

**Provisional read (not a ruling).** For the citizen, one label is enough. Prefer **Methodology** as the on-page H2 (matches USAFacts and ordinary expectation) **or** **How this is measured** (matches the layout token and house page language) — not both “method” in chrome and “Methodology” as H2 without a glossary. Crew docs can keep “method” as the short internal word for that block.

| Owner | Job |
|-------|-----|
| Content Editor | One citizen heading string on C1–C3 |
| Front-end Architect / UI/UX | Align layout token docs with the chosen H2; no second section |
| Charter Editor | Close when the string is one |

---

### F-source-stack — group by office, compact cards, side-panel (not required on-page)

**Concept.** A citation must be **available when someone needs to see it**. It need **not** sit as a card already on the answer page. Opening the citation card in a **side-panel** is enough, as long as every bound number can reach its cite from that view (cite-strip, chart source-line, or a sources control).

**Wanted.**

1. **Group by producing office** so the sources list has fewer entries (e.g. one NSO / MoSPI group covering CPI General + CFPI + linked run, not five near-duplicate cards).
2. **Compact citations** — the trigger / summary carries what a person needs; the panel body does **not** re-print the same producer / series / period already visible in that summary.
3. **Side-panel as the cite home** — full citation cards live in the panel, not as a mandatory bottom dump of every card on the page. An optional compact “Sources” index that opens the same panel is fine; an on-page stack of full cards is **not** required.

**Reopens.** Prior “source-stack stays on the page / complete list of cards in the DOM” lines (archive cms-system rulings 2–3; design-system Interaction that keeps `.source-stack` cards on-page). Completeness becomes **reachable**, not **already rendered in the reading column**.

**Still required.** Agency remains the producer. No invented figures. No replacing the cite with “Analysis by Prism.” Trust can still open every observation’s citation. Prefer no separate `/cite` URL if the panel is on this slice; if Charter later allows a fragment or house route, the concept still holds — available on demand, not inline by default.

**Open design choices (Charter + Platform + UI/UX).**

| Choice | Lean |
|--------|------|
| Group key | Producer office (and maybe one series family), not one card per `citation_id` |
| Where the card lives | Side-panel (or equivalent closable panel) — **not** required in the page body |
| Trigger | Cite-strip, chart `.source-line`, and/or one “Sources” control → same panel payload |
| Card body | Unique fields only: URL, release notes, caveat not already on the strip |
| Bottom of page | Optional compact grouped index; omit the full on-page card stack |

| Owner | Job |
|-------|-----|
| Charter Editor | Confirm “available when needed” over “must be on the page”; reopen stack-on-page rulings |
| Platform Architect | Cite projection / grouping; panel payload per office group |
| UI/UX Developer | Side-panel chrome; compact triggers; no redundant summary/detail |
| Front-end Architect | Panel on this slice URL; no new page type unless Charter names one |
| Source Librarian | Producer naming when groups merge series |
| Trust Auditor | Every bound observation still opens its cite; producer not replaced |

---

### F-method-width — Methodology narrower than the reading pane

**Observation.** Evidence sections run at `--desk`. Methodology (`.how-measured` / `data-cite-view="how-this-is-measured"`) is capped at `--measure` (40rem) in [design-system.md](../design-system.md) and `desk.css`, so the block does not share the full reading width of other sections.

**Prior ruling.** Archive [cms-system-feedback.md](../archive/cms-system-feedback.md) ruling 4: method is quiet by **type**, not by a second column; same `--desk` left/right edge; `--measure` on `.how-measured` yields.

**Wanted.** Methodology extends to the same width as other sections. Quietness stays smaller type and placement after the record — not a narrow column.

| Owner | Job |
|-------|-----|
| UI/UX Developer | Drop or stop applying `--measure` on method; presentation pass; amend design-system Method quieter |
| Charter Editor | Confirm ruling 4 still stands post-rethink |

---

## Suggested sequence (when opened)

1. **F-method-width** — smallest fix; visual consistency; no copy risk.
2. **F-method-name** — one H2 string.
3. **F-source-stack** — Platform + UI/UX design pass before Content rewrites cards.
4. **F-insight-push** — Charter reopen of rethink §2 (story-shaped how/why/what); then Content on existing slots; ingest only for named missing comparisons.

---

## Out of scope here

Flipping `citizen_pointer`; Catalog B3; search / newsletter / chat; USAFacts magenta / Aeonik; inventing figures for a softer insight.
