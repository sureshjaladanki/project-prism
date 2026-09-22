# Prism and CMS rethink

```text
verdict:        accepted — Prism is re-scoped as a civic answer publisher for India
status:         programme closed on preview — phases 1–17 done on
                desk-20260922-1c821625d891; resonance gate passed; phase 17
                done-when met; paused before B3
publish:        none — citizen_pointer untouched this wave (still
                desk-20260916-30d02e4204cd); all rethink work stayed on preview
top_priority:   pause — Catalog B3 (multi-slice citizen publish) is a separate
                Charter question; do not start it from this close-out
tooling:        unchanged by choice — one repo, Python src/prism/, Astro SSG
                src/cms/, DuckDB at render, one vintage_id per page
next_persona:   — (pause); Charter Editor only when opening B3 or a new slice
preview_desk:   desk-20260922-1c821625d891
```

---

## 1. The product after the rethink

### 1.1 What Prism is now

Prism is a **civic answer publisher**: one citizen question per URL, answered out loud from official Indian government statistics, with the producing office standing next to the number.

The thing that changes is not the machine and not the sources. It is **who the page is written for**. Today C1, C2, and C3 are correct and unreadable: they open by teaching the reader what an index is, what a projection is not, and what a Budget Estimate is not. That is a codebook with a question on top. The new product opens with the answer a person would repeat to someone else, shows that the number moved, and puts the teaching below the fold.

House sentence, for every contract that needs one:

> **Prism answers one question at a time, in the words a person would use, with the government's own number and the government's own name on it.**

### 1.2 "Relate and resonate" as a gate a Principal read can fail

The resonance gate is six tests. A Principal citizen read (`docs/personas/principal.md`) runs them against the rendered preview page, in order, and fails the page on the first one that breaks. All six must pass on `/prices/retail-prices`, `/people/population`, and `/money/union` before any lower F-row is worked.

| Id | Test | Fails when |
|----|------|-----------|
| **R1 Spoken thesis** | The first sentence of the page states the answer: a bound number, its unit in citizen words, the place, the period, and the direction. | The first sentence defines an index, names a base year or a producer series, says what the page is *not*, or describes the page instead of answering it. |
| **R2 Movement** | The first screen carries a **prior published period** for the lead figure and what changed between them — both bound. | The first screen holds only one period's levels. A number with no yesterday. |
| **R3 One line of what it is** | Exactly **one** sentence above the first chart says what the number counts for a person. | Two or more definition sentences above the first chart. Zero is also a fail. |
| **R4 No decoder ring above the fold** | Above the first chart there are **zero** occurrences of: base-year notation (`2024=100`), series/annex/group/table ids, `vintage_id`, "not comparable", "this is not X" asides, producer notation beyond a plain phrase. | Any one occurrence. |
| **R5 Evidence that further answers** | Every evidence section opens with a further citizen question and answers it with a figure **and** a movement or a comparison. | A section that opens by restating a stat chip; a section whose main content is an anti-misread aside; a section that is a codebook tour. |
| **R6 Read-aloud** | A reader reads the first screen aloud in under 30 seconds and can then restate the answer, the direction, and who published it, without using a word the page did not say in plain English. | Restating needs a term the page never translated. |

Two further tests are **not** resonance and do not yield to it. They are Trust Auditor's, and they block ship on their own:

- **M1 Magnitude.** The number a reader would say aloud is the producer's magnitude. `0.35 Cr` for a `3526840` ₹ crore figure fails. See §4.2.
- **M2 Hole vs zero.** A published zero and a gap are verbally and visually distinct. The citizen phrase for a gap is **not published**; the schema status stays `unknown` / `withheld`.

### 1.3 Answer-page anatomy

One URL. One vintage. Above the fold is the answer; below it is the evidence; method is last and quiet.

**Above the fold (the answer band)**

1. Sleeve — topic family, not a kicker.
2. **H1** — the citizen question, geography in the words. Unchanged for C1–C3.
3. Byline — release date (`Asia/Kolkata`), next named release.
4. **Thesis** — one sentence, the spoken answer. Bound slots. The answer clause carries a house accent (§2.3). This is the loudest text on the page after H1.
5. **Movement** — one sentence: the prior published period and what changed. Bound slots, or the citizen phrase for a break (§4.3).
6. **What it is** — one sentence. What this number counts, for a person.
7. **Stat row** — 2–4 equal-weight bound figures, each with its unit **in the cell**.
8. **Cite strip** — producer, series as the producer names it (no group codes), reference period, released. Opens the full card in view.
9. **First chart** — the figure the thesis just stated, over time or across the units the question names.

**Below the fold (evidence)**

Each section: a further citizen question as `<h2>`, then a bound figure, then a movement or comparison, then one chart. One idea each. No section whose body is an aside.

**Last (method)**

What was counted, who, when, coverage, breaks, gaps, the "this is not X" lines, dual official series, and the denomination note. Quiet by type, same width as evidence.

### 1.4 The three worked examples

Slots are named jobs, not numbers. Nothing below is a figure to type.

**C1 — `/prices/retail-prices`.** H1 unchanged: *How fast are retail prices rising in India, including food?*

| Block | Job |
|-------|-----|
| Thesis | Retail prices were `{cpi_general_yoy}` percent higher in `{period}` than a year earlier. Food was `{cfpi_yoy}` percent higher. |
| Movement | A month earlier the rate was `{cpi_general_yoy_prior}` percent; a year earlier it was `{cpi_general_yoy_year_ago}` percent. |
| What it is | It is the change in the prices households actually pay, measured on the same basket of goods and services each month. |
| Stat row | General and food rates with `%` in the cell; rural and urban as the other two chips. |
| §1 *Is food rising faster than everything else?* | Food vs general, rural vs urban, each bound, with the gap between them named. Drop the chip recap opener (`F-c1-recap-food`). |
| §2 *When was it last this high?* | Rate over time. The highest and lowest month in a stated, Methodologist-signed window, named as bound facts of the published measure. |
| §3 *Where are prices rising fastest?* | States and UTs. This chart's own caption is a rank question, so this chart may measure-sort (§4.5). Cut the "All India is not a bar here" aside (`F-all-india-aside`). |
| Method | CPI (General), base year, Combined = rural + urban, provisional vs final, Food and beverages vs food index, series names as the producer prints them. |

**C2 — `/people/population`.** H1 unchanged.

| Block | Job |
|-------|-----|
| Thesis | About `{ncp_projection}` people live in India in `{year}`, on the government's official projection. |
| Movement | The last time everyone was counted, in Census 2011, the total was `{census_2011}`; in 2001 it was `{census_2001}`. |
| What it is | A projection is the government's estimate of how many people there are now, carried forward from the last count. |
| Stat row | Projection, Census 2011 Total, decadal growth as published, and one SRS rate — every rate chip carries its producer unit (`F-c2-rates-unit`). |
| §1 *Where do people live?* | States and UTs, alphabetical. No "All India is the unit above" aside. |
| §2 *How fast is that changing?* | Census totals 1901–2011 with plain year ticks, plus the projection path named as projection. |
| §3 *Who is being born, and who is dying?* | SRS birth, death, infant mortality, fertility — each with its unit and its movement against the prior published year. The "rates are not headcount" and "not multiplied by the 2011 headcount" lines move to method (`F-c2-rates-aside`). |
| Method | Projection vs enumeration, the joining-unit note (thousands of persons vs persons), coverage, census footnote marks, what is **not published**. |

**C3 — `/money/union`.** H1 unchanged.

| Block | Job |
|-------|-----|
| Thesis | The Union government plans to collect `{be_revenue_receipts}` and spend `{be_total_expenditure}` in `{year}`. |
| Movement | The last year with final accounts, `{actuals_year}`, it collected `{actuals_revenue}` and spent `{actuals_expenditure}`. |
| What it is | These are Budget Estimates — the plan printed in this year's Budget. |
| Stat row | Receipts, expenditure, one liabilities figure, one tax figure — all in Indian numbering (§4.2). |
| §1 *Where does the money come from?* | Tax, non-tax, capital receipts, each against the last published Actuals. |
| §2 *Where does it go?* | Major expenditure heads, same treatment. |
| §3 *What does the Union owe?* | Outstanding liabilities, its own scale group, plain year ticks. |
| §4 *Plan, revised plan, final accounts* | BE / RE / Actuals as three records — one cite control per observation, each period matching its chip (`F-three-records-cite`). |
| Method | BE is not Actuals; the headline receipts figure is not the sum of the statements below; GST Compensation Cess is **not published** while IGST is a published zero (`F-igst-gap-contrast`). |

---

## 2. USAFacts: adopt, adapt, refuse

The standing veto is lifted. Reference: `docs/usafacts-profile.md` (observation 2026-09-17, not a contract).

| Move | Ruling | What we do |
|------|--------|-----------|
| **Answer voice** — declarative, short, no hedging | **Adopt** | Spoken sentences. Calm, adult, specific. We do not adopt "insights", "Now what?", advocacy copy, or their open-letter register. |
| **Thesis lede as the product** — highlighted answer sentence | **Adopt** | The thesis clause is the designed object, visibly marked. Ours is a house accent, not magenta `span.answer`. `QAPage.acceptedAnswer` already carries it. |
| **Giant display figures under the lede** | **Adopt** | Already the stat row. Add the unit in the cell. |
| **Fast facts** | **Adopt and extend** | Home and sleeve one-liners stay, and now carry the movement clause so a teaser cannot go stale against the hero (`F-home-teaser`, ruling 9). |
| **Ranks and league tables** | **Adapt** | Bound rank order is allowed per **chart**, governed by that chart's own caption being a rank question — not by the page H1 (§4.5). Extrema of one published series over a stated window are bound facts. Refused: "best/worst", "lowest-performing", performance nicknames, podium palettes, red–green. |
| **Evidence payoff** — prior period, what changed, what it is | **Adopt** | This is R2 and R5. It is the core of the rethink. |
| **Scan path** — question → answer → evidence → method | **Adopt** | Already ours; now enforced by R1–R6 rather than by shape alone. |
| **Geography pages** (`/{slice}/{geo}`) | **Adapt, later** | Stays reserved in `docs/web-design.md`. A geography page is a full slice with its own question and cite, never a doorway. Not this wave. |
| **Articles / guides desk** | **Refuse** | We are not a media desk. Sub-questions stay hashes on the slice. |
| **Government 10-K** | **Refuse** | The Union is not an issuer. Unchanged. |
| **Chat / "Ask the data"** | **Refuse** | Static citizen HTTP; no request-time inference over the record. |
| **Search** | **Refuse this wave, reopenable** | Three slices and five hubs do not need an index. Front-end Architect may reopen at eight or more published slices. |
| **Newsletter, social, "get notified", engagement SDK** | **Refuse** | We do not collect the reader. |
| **"Insights" as a genre** | **Refuse as a genre, adopt as a clause** | No essay that tells the reader what it means. The bound "what changed" sentence is the whole of it. |
| **Chart download from bound specs** | **Keep** | Already allowed; specs are bound at render. |
| **MCP / connectors / API** | **Refuse this wave** | Not a non-goal forever; out of this programme. |
| **Look and chrome** | **Adapt — this is the reopen** | See §2.2–2.3. |

### 2.1 What happens to the "wordmark swapped" lines

They are **struck**. They are shape vetoes dressed as integrity rules, and ruling 0 says shape is not the problem. The following lines are removed by the persona who owns each file, in the phase named in §5:

| File | Line | Action |
|------|------|--------|
| `docs/vision.md` | "It is not a copy of that site, its topics, or its American frame." | Replace with the adapt sentence (§3). |
| `docs/editorial-guidelines.md` | "A page that would pass for USAFacts with the wordmark swapped has failed these guidelines." | Strike. Replaced by the resonance gate. |
| `docs/design-system.md` | "A page that would pass for USAFacts with the wordmark swapped has failed this system."; the "Costume we do not copy" section; non-negotiable 3; the two "does not look like a USAFacts chart" checklist boxes | Strike and replace with house rules H1–H7. |
| `docs/design-philosophy.md` | "not USAFacts magenta, cream, Aeonik, or wordmark"; "not a passionate-nerd costume" | Rewrite as H1. |
| `docs/web-design.md` | "Do not paint the desk to resemble USAFacts." | Strike; the tone paragraph is rewritten to point at H1–H7. |

Resemblance in shape, voice, scan path, or product move is no longer a failure condition. Trust Auditor does not block on "this reads like USAFacts" — that is restated in the Trust row of `docs/archive/cms-system-feedback.md` and stands.

### 2.2 House rules that replace "not USAFacts costume"

These are the standing look/chrome rules. They are positive identity plus a short forbid list, and they are what UI/UX writes into `docs/design-philosophy.md` and `docs/design-system.md`.

- **H1 — Prism is its own publication.** Own text lockup, own tokens, own typefaces. We do not use another publisher's wordmark, brand colour, or licensed typeface — Aeonik and the USAFacts magenta stay out because they are theirs, not because the shape is theirs.
- **H2 — The answer is the loudest thing on the page, and it is a bound observation.** Display weight never lands on a slogan, a mission line, or a section title.
- **H3 — Colour never means better or worse.** No red–green, no podium palette, no party or ministry palette, no tricolour as brand or scale, no saffron/green as up/down. Series colour is categorical position.
- **H4 — A gap is visible and named.** The citizen phrase is **not published**, italic, same size and face as its sentence. A published zero must look and read differently from a gap.
- **H5 — The producer sits with the number, in view.** Cite strip on the first screen, full card on this page, complete list at the bottom. "Analysis by Prism" beside the producer, never instead.
- **H6 — No chrome that collects the reader.** No search (this wave), chat, newsletter, social row, "get notified", A/B, heatmap, or engagement SDK.
- **H7 — No decoration the vintage did not earn.** No illustration that asserts a fact, no gradient that implies direction, no icon standing in for a number.

Still forbidden, independent of look: spin and judging words; a partisan report card; hidden holes; a missing or replaced producer cite; invented figures; forecasts and private polls as the record; picking a winner between two disagreeing official series.

### 2.3 The one visual move this reopen buys

The thesis clause may carry a **house accent mark** — a marked answer clause, the way the highlighted lede is the product on an answer page. UI/UX specifies the token in `docs/design-system.md` v4 from the existing warm/navy family. It is not magenta, it is not a link colour, and it marks only the bound answer clause, never a definition or a section title.

---

## 3. Contracts: keep, amend, replace

| File | Ruling | Written by |
|------|--------|-----------|
| `docs/vision.md` | **Amend.** Add the reader sentence from ruling 0 — citizens first, a page a person without the codebook can relate to. Replace the "not a copy of that site" line with: *we adapt freely from how USAFacts answers a question; the record is India's official statistics and the producing office keeps its name on every number.* Every "how we work" bullet stands unchanged. | Charter Editor |
| `docs/design-philosophy.md` | **Replace.** New idea line: *an answer a person can say out loud, with the government's name on it.* Carries H1–H7 as the tone contract. Drops the costume framing and the "austere vs generous" argument with v2. | UI/UX Developer |
| `docs/editorial-guidelines.md` | **Replace.** The resonance gate R1–R6 becomes the spine. Thesis / movement / what-it-is replaces "fact-lede then one sentence of definition". Evidence sections must further answer with a figure and a movement. Series teaching, anti-misread asides, and "this is not X" are method-only. The four passes stay, in order, with a new first test in Proof: read it aloud. | Content Editor |
| `docs/design-system.md` | **Amend to v4.** Answer band gains the thesis accent and a movement line; stat cells carry units; gap encoding distinct from published zero; compact-unit fit rewritten against the new number contract (§4.2); `LAYOUT_BLOCKS` unchanged. Every fit, contrast, and legibility floor from v3.1 carries forward untouched. | UI/UX Developer |
| `docs/web-design.md` | **Amend.** Quiet-empty hubs carry one citizen invitation line (`F-empty-sleeve`); header nav IA signed or confirmed before any look pass (`F-site-header-nav`); search named as refused-this-wave with the reopen condition; geography routes stay reserved; home-rail forbid stands. | Front-end Architect |
| `docs/architectural-blueprint.md` | **Amend.** Spine unchanged and restated as a choice (§4.1). Test 8 amended to chart-level rank questions. Two tests added: test 10 (denomination integrity / order of magnitude), test 11 (published zero is not a gap, and a gap is never plotted as zero). Nine tests become eleven. | Platform Architect |
| `docs/data-contracts.md` | **Amend.** `DisplayValue` is replaced by `CitizenNumber`; observations carry `denomination`; a new `CitizenChange` projection carries movement. Citizen projection and Pointers sections rewritten accordingly. Pointer semantics unchanged. | Platform Architect |
| `docs/team.md` | **Amend, lightly.** Add one step to "how work moves": a Principal citizen read against the resonance gate runs after the presentation pass and before Charter's verdict on any template that changed voice. Principal stays an outside-roster advisor and is still not a ship gate. | Charter Editor |
| `docs/next/topic-charters.md` | **Keep.** Districts stay parked. No new sleeves, no new charters this wave. | — |
| `docs/repo-conventions.md` | **Keep.** Tooling lock reaffirmed as a choice, not deference (§4.1). | — |

`docs/archive/cms-system-feedback.md` holds the F-row routing from the prior wave. `docs/archive/citizen-system-change-plan.md` is the closed predecessor programme (superseded by this file).

---

## 4. The machine

### 4.1 What stays, as a choice

Ingest → immutable vintage → bind/render → atomic pointer **stays**. Astro SSG stays. DuckDB at render, one `vintage_id` per page, stays. Two pointers, same relative paths, stays. Static citizen HTTP stays.

This is a choice, not deference. Resonance is a voice, binding, and typography problem. Nothing in R1–R6 needs a server: the movement clause is a second observation from the same vintage, and the thesis is a template sentence with slots. What the immutable vintage buys us is exactly what ruling 0 cannot be allowed to cost us — "no invented figures" is checkable because every figure on a page is traceable to one snapshot, and a page cannot silently change under a reader. Adding ISR or a request-time producer fetch would buy freshness we do not need and lose the property the whole trust argument rests on.

So: no Next.js, no ISR, no request-time fetch, no API, no second CSS framework, no new top-level folder.

### 4.2 The unit system — one Indian numbering contract

`DisplayScale`, `scale_for_concept`, `concept_key`, and `apply_scale` are **removed**. Peak-driven, concept-lumped scaling is the direct cause of `0.35 Cr` and of `14.23 L Thousand`. It is replaced by a denomination contract that runs ingest → vintage → render.

**Owner:** Platform Architect (contract and the one formatter). Ingest Engineer and Pipeline Engineer keep denomination honest on the way in. Methodologist signs denomination vocabulary. UI/UX only guarantees the string fits. Trust Auditor fails wrong order of magnitude on ship.

**On the observation.** Add `denomination`: the magnitude the producer printed (`ones` | `thousand` | `lakh` | `crore`) paired with what is being measured (`rupees` | `persons` | `percent` | `rate` | `index` | …). `value` and `unit` stay exactly as the producer printed them; `unit` remains the string the cite card shows. Ingest does not normalise to ones. A ₹ crore column stays `crore` of `rupees`. A thousands-of-persons column stays `thousand` of `persons`.

**At bind, once.** A single function converts `value × denomination` to a **canonical** amount in base units — rupees, persons — for money and headcount. Percent, rates, and indices have denomination `ones` and are never converted and never compacted.

**At render, formatting only.** One formatter produces the citizen string from the canonical amount, on the Indian ladder:

| Magnitude | Prose token | Axis token |
|-----------|-------------|-----------|
| 10³ | thousand | `K` |
| 10⁵ | lakh | `L` |
| 10⁷ | crore | `Cr` |
| 10¹² | lakh crore | `L Cr` |

Worked: `3526840` ₹ crore → canonical `3.52684e12` rupees → **₹35.27 lakh crore**. Liabilities `2.1e7` ₹ crore → canonical `2.1e14` → **₹210 lakh crore**. Projection `1,42,39,xxx` thousand persons → canonical `~1.42e9` persons → **142 crore people**. The token is the entire unit; the producer's `unit` word never sits beside it (ruling 1 stands: `35.27 L crore` and `14.23 L Thousand` both fail).

**No cross-talk.** Scale is chosen per **scale group**, and a scale group is *declared by the template* — a chart axis and the chips that quote that chart. Never inferred from a page-wide concept bucket. Liabilities cannot set the scale for revenue receipts; a chart and its own axis agree, and nothing else is forced to agree with them.

**`DisplayValue` becomes `CitizenNumber`:**

```text
CitizenNumber
  canonical_value    base units (rupees, persons) or the published rate/index
  measure            rupees | persons | percent | rate | index | count
  text               the only citizen number string — or "not published"
  chart_value        the value plotted, in the chart's declared scale group
  axis_label         the compact token for that group
  status             Observation.status
  absent             display_scale, concept_key, producer unit word
```

`raw_value`, `unit`, and `denomination` stay on the observation and on the cite card. They are the record; `CitizenNumber.text` is the page.

**Blueprint test 10 (new).** A rendered citizen figure whose canonical magnitude differs from the producer's published magnitude fails the build. This does not wait behind voice work.

### 4.3 Movement, as a bound object

New bind-time projection, `CitizenChange`, so R2 is bindable rather than written:

```text
CitizenChange
  current            CitizenNumber (this period)
  prior              CitizenNumber (prior published period, same series)
  prior_period       citizen period label
  direction          higher | lower | unchanged
  difference         formatted difference, or "not comparable"
  citation_id        the prior observation's own cite
```

Rules: both sides are observations of the **same series** in the **same vintage**. The only arithmetic is subtraction (and, where Methodologist signs it, a published ratio). If a `series_break` or `not_comparable` status lies between the two, `difference` renders the citizen phrase for a break and the template shows both figures without joining them. If the prior observation is absent, the slot renders **not published** — never a remembered number. Prism may name this as analysis beside the producer cite; the producer stays the producer.

### 4.4 Templates, charts, and chrome

- `LAYOUT_BLOCKS` in `src/prism/template_bind.py` is **unchanged**. The thesis, movement, and what-it-is sentences all live inside the existing `.fact-lede` block, which gains a three-sentence job. No new block keys, no new Astro route, no new page type.
- Chart system stays Vega-Lite in git, SVG at render, one `plotWidth` per page, 12px floor. What changes: a gap is encoded as an explicit labelled absence, never a numeric zero, and a published zero must be visibly distinguishable from it (test 11).
- Axis ticks are citizen period labels — plain years, plain BE/RE/Actuals phrases. No producer footnote marks, no `end-` / `actual-` prefixes.
- Citizen cite series text uses the producer's name for a person; table, group, and COICOP codes stay on the librarian card (`F-c1-group-code`).

### 4.5 Rank order, amended

Blueprint test 8 currently gates measure-sort on the **slice's** question. Amended: a chart may measure-sort when **that chart's own caption is a rank question** and the template declares it on the chart spec. Default everywhere else remains alphabetical by official English name or a documented geographic order. Red–green, diverging performance scales, and podium palettes stay forbidden under H3. Trust checks that the declared caption really is a question about order — not that the page H1 was one.

### 4.6 Preview, and the rows marked closed on 2026-09-21

Every phase that touches copy, numbers, or chrome **rebinds and re-renders the preview desk**. This programme does not assume a later desk and does not trust a row closed against `desk-20260921-2f93be5c9ccc`.

The principal read of that desk still saw several rows that were marked closed. Ruling: **a row is closed when it is absent from the newest preview desk, not when a pass reported it fixed.** At the Trust phase, the auditor re-checks the closed rows in `docs/archive/cms-system-feedback.md` — inline type, method fine-print, chart left-gap, census axis marks, budget axis prefixes, cite-strip panel, source-line panel — against the new desk and reopens any that reappear. No re-argument, just the new desk.

`citizen_pointer` does not move in this programme.

---

## 5. Phases

One persona per phase. Implementation is not assigned here — each phase names the persona and the files, and that persona decides the edit in its own pass.

Two tracks run inside the order below: **Track U** (units and movement — phases 2–5) and **Track V** (voice and look — phases 6–11). They converge at phase 12. `depends-on` is the real constraint; a parent may run a Track U phase and a Track V phase in either order where no dependency exists.

| # | Goal | Persona | Files | Depends on | Done when | A citizen would notice |
|---|------|---------|-------|------------|-----------|------------------------|
| 1 | Reader-first vision; strike the copy veto | Charter Editor | `docs/vision.md` | this file | Vision carries the citizens-first resonance sentence and the adapt sentence; the "not a copy" line is gone; every sources/spin bullet is unchanged | nothing |
| 2 | Name the unit system and the movement object | Platform Architect | `docs/data-contracts.md` | 1 | `denomination` on the observation; `CitizenNumber` replaces `DisplayValue`; `CitizenChange` specified; `DisplayScale` removed from the contract | nothing |
| 3 | Integrity tests for magnitude and gaps | Platform Architect | `docs/architectural-blueprint.md` | 2 | Test 8 amended to chart-level rank; tests 10 and 11 written; spine restated as a choice | nothing |
| 4 | Land the number contract in the spine | Platform Architect | `src/prism/` schema, projection, bind | 3 | One formatter; declared scale groups; no `scale_for_concept` / `apply_scale`; tests 10 and 11 fail on a seeded wrong magnitude and a zero-plotted gap | nothing yet |
| 5 | Denomination honest on the way in; gap status correct | Pipeline Engineer | mappers, vintages for C1–C3 | 4 | Every C1/C2/C3 series carries denomination; ₹ crore stays crore; rate and index series carry their unit; GST Compensation Cess stays `unknown`, IGST stays a published zero | money and population figures read at the right size |
| 6 | Sign what may be bound as movement, denomination, and gap wording | Methodologist | a new note under `docs/` | 2 | Signed: which prior periods are comparable for C1/C2/C3; the C1 extremum window; denomination vocabulary; the citizen gap wording | nothing |
| 7 | The reading contract | Content Editor | `docs/editorial-guidelines.md` | 1, 6 | R1–R6 are the contract; thesis/movement/what-it-is replaces the old lede rule; asides and series teaching are method-only; the wordmark-swap line is gone | nothing |
| 8 | Tone and house rules | UI/UX Developer | `docs/design-philosophy.md` | 7 | New idea line; H1–H7 carried; costume framing gone | nothing |
| 9 | Visual contract v4 | UI/UX Developer | `docs/design-system.md` | 8, 2 | Thesis accent token; movement line; units in stat cells; gap-vs-zero encoding; compact-unit fit rewritten against `CitizenNumber`; all v3.1 floors intact; `LAYOUT_BLOCKS` unchanged | nothing |
| 10 | IA for the gaps the principal found | Front-end Architect | `docs/web-design.md` | 8 | Quiet-empty hub invitation is IA-signed; header nav signed or confirmed; search refused-this-wave with a named reopen condition; geography still reserved | nothing |
| 11 | Rewrite C1, C2, C3 | Content Editor | the three templates under `src/cms/templates/` | 5, 7, 6 | Each page has a thesis, a movement, one what-it-is line, units in chips, and evidence sections that further answer; asides moved to method; recap openers cut | the pages start with an answer instead of a definition |
| 12 | Implement v4 and render preview | UI/UX Developer | `src/cms/` theme, styles, render; new preview desk | 9, 11 | New preview desk renders complete; thesis accent, movement line, unit-bearing chips, gap encoding all live | the answer band looks like an answer |
| 13 | Presentation pass | UI/UX Developer | preview desk | 12 | v4 checklist clean at 360px and 1440px; header nav look done after the phase-10 sign; chart wells fill; no mixed plot widths | polish |
| 14 | Record pass or block | Trust Auditor (Cursor agent) | preview desk | 13 | Cites, dates, holes, spin clean; M1 magnitude and M2 hole-vs-zero pass; the 2026-09-21 closed rows re-checked on this desk and reopened if present | nothing |
| 15 | Citizen resonance read | Principal (advisor) | preview desk | 14 | R1–R6 run in order on all three slices; result handed to Charter as pass or first-fail | nothing |
| 16 | Verdict and routing | Charter Editor | `docs/next/prism-cms-rethink.md`, `docs/archive/cms-system-feedback.md` | 15 | Gate passed or the failing phase is re-run; remaining F-rows sequenced | nothing |
| 17 | Lower F-rows, gated behind 16 | per row, one persona per pass | per row | 16 | `F-empty-sleeve` copy, `F-home-teaser`, `F-gap-phrase` on house pages, `F-c1-group-code`, `F-three-records-cite`, `F-site-header-nav` look, `F-chart-review-owners` all closed on a fresh desk | small corrections across home, hubs, and cites |

If phase 15 fails, the parent re-runs the failing phase only — 11 for a voice fail, 12 or 13 for a chrome fail, 5 for a number fail — then 13, 14, 15 again. Phases 16 and 17 do not start on a failed gate.

---

## 6. Non-goals this wave

- Flipping `citizen_pointer`. Nothing here publishes.
- Catalog B3 (multi-slice citizen publish). Stays out; it is a separate Charter question after the gate passes.
- Districts and geography routes. Districts stay parked (`docs/next/topic-charters.md`); `/{sleeve}/{slice}/{geo}` stays reserved and unbuilt.
- New charters. C4–C20 get no template, no slug, no sleeve change.
- Search, chat, newsletter, social, articles, guides, a 10-K, an API, MCP, connectors, `og:image`, dark mode, a mobile app, another language.
- Any framework change: no Next.js, no ISR, no request-time producer fetch, no server at citizen request time, no second CSS framework, no new top-level folder.
- Rewriting past vintages. `dv-20260918-846e99d0ca57` and every other written vintage stay immutable; wrong numbers are fixed forward in a new vintage.
- A partisan report card, forecasts, private polls, a winner between two disagreeing official series.

---

## 7. First parent pass

**Persona:** Charter Editor. **File:** `docs/vision.md`. **Nothing else.**

Three edits:

1. In *Who it is for*, or as a new sentence in the opening, carry ruling 0's reader clause: a citizen without the codebook must be able to relate to and resonate with the answer page — citizens first, then journalists, students, researchers, and public life.
2. In *What this is*, replace "It is not a copy of that site, its topics, or its American frame." with the adapt sentence: Prism adapts freely from how USAFacts answers a question — voice, thesis-first lede, fast facts, evidence payoff, scan path, look — into our house for India; the record is India's official statistics and the producing office keeps its name on every number.
3. Leave every *How we work* bullet exactly as written. Official sources only, show don't spin, name the derivation, order is not a verdict, India as it is governed, trust the method — none of them move.

Do not touch `docs/editorial-guidelines.md`, `docs/design-system.md`, any template, or any code in that pass. Phase 2 is Platform Architect on `docs/data-contracts.md`.
