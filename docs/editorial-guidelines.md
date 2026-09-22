# Editorial guidelines

Content Editor. Standing reading contract for every citizen template. What the portrait is for: [vision.md](vision.md). The record: [data-contracts.md](data-contracts.md). Movement and denomination signs: [citizen-movement-denomination.md](citizen-movement-denomination.md).

This file governs copy, scan path, voice, and chart *meaning*. [design-system.md](design-system.md) implements the look — UI/UX Developer owns that file.

```text
role:           civic answer publisher — one question, one spoken answer, official name on the number
craft:          thesis → movement → what-it-is → evidence → method
gate:           resonance R1–R6 (Principal citizen read); Trust holds M1 magnitude and M2 hole-vs-zero
```

## Stance

A shared, checkable picture of India from official government statistics — and nothing else. High or low, good or bad: the reader decides.

Prism adapts freely from how [USAFacts](https://usafacts.org/) answers a question — voice, thesis-first lede, fast facts, evidence payoff, scan path, look — into our house for India. The record is India's official statistics; the producing office keeps its name on every number. Resemblance in shape, voice, or scan path is not a failure. House look rules are H1–H7 in [design-philosophy.md](design-philosophy.md) and [design-system.md](design-system.md).

**House sentence.** Prism answers one question at a time, in the words a person would use, with the government's own number and the government's own name on it.

## Resonance gate (R1–R6)

A Principal citizen read ([principal.md](personas/principal.md)) runs these in order against the rendered preview page and fails on the first break. All six must pass on `/prices/retail-prices`, `/people/population`, and `/money/union` before lower F-rows are worked.

| Id | Test | Fails when |
|----|------|-----------|
| **R1 Spoken thesis** | The first sentence of the page states the answer: a bound number, its unit in citizen words, the place, the period, and the direction. | The first sentence defines an index, names a base year or a producer series, says what the page is *not*, or describes the page instead of answering it. |
| **R2 Movement** | The first screen carries a **prior published period** for the lead figure and what changed between them — both bound. | The first screen holds only one period's levels. A number with no yesterday. |
| **R3 One line of what it is** | Exactly **one** sentence above the first chart says what the number counts for a person. | Two or more definition sentences above the first chart. Zero is also a fail. |
| **R4 No decoder ring above the fold** | Above the first chart: zero base-year notation (`2024=100`), series/annex/group/table ids, `vintage_id`, "not comparable", "this is not X" asides, producer notation beyond a plain phrase. | Any one occurrence. |
| **R5 Evidence that further answers** | Every evidence section opens with a further citizen question and answers it with a figure **and** a movement or a comparison. | A section that opens by restating a stat chip; a section whose main content is an anti-misread aside; a section that is a codebook tour. |
| **R6 Read-aloud** | A reader reads the first screen aloud in under 30 seconds and can restate the answer, the direction, and who published it, without using a word the page did not say in plain English. | Restating needs a term the page never translated. |

Trust Auditor (not this gate) still blocks on **M1** magnitude integrity and **M2** hole vs zero.

## Data integrity

The page is a window on one **data vintage**. It is not reporting. Prism may analyze official series and say so. It does not become the statistical office and does not replace the citation.

- **Official sources only.** Cite the producer, the series, and the date. The producer stays the agency.
- **Slots, not typed figures.** Copy binds to observations at render. Missing observation → **not published** — never a remembered number. Bound figures use `CitizenNumber.text` (Indian grouping / house ladder) so the thesis, the stat cell, and the `meta description` share one string.
- **Cite in the same view.** Producer, series (as the producer names it for a person — no group codes in the strip), reference period, release date (`Asia/Kolkata`) sit with the number. Full card on this page. “Analysis by Prism” may sit next to that cite — never instead of it.
- **Citizen names, producer cards.** Running copy uses ordinary names. Series teaching, anti-misread asides, and “this is not X” are **method-only**.
- **Name derived work.** Ranks, comparable periods, and movement (`CitizenChange`) already in the vintage may be named as Prism analysis.
- **Trust the method.** Breaks, lags, holes, and two official numbers stay visible. Do not pick a winner or smooth a hole.
- **India as it is governed.** Name missing units. An All India figure is not “the whole country” when large populations are out of sample.
- **Context in, verdicts out.** What was counted, who, when. Not what it proves about a ministry.

## Story-shaped explainer

A page is **question → thesis → movement → what-it-is → evidence → method**.

Inside `.fact-lede` (unchanged layout block): three sentences — **thesis** (spoken answer, bound slots, house accent on the answer clause), **movement** (prior period and what changed, or the break phrase), **what it is** (exactly one definition for a person). Then the stat row (units **in the cell**), cite strip, first chart.

Evidence sections: further citizen question as `<h2>`, bound figure, movement or comparison, one chart. No section whose body is an aside. Method is last and quiet: teaching, dual series, denomination notes, gaps.

| In | Out |
|----|-----|
| Spoken thesis answering the H1 from slots | Opening with a definition, “this is not X”, or a page description |
| Movement with a prior published period | One period’s levels alone above the fold |
| Exactly one what-it-is sentence | Codebook tour or two definition sentences above the first chart |
| Bound ranks when **that chart’s caption** is a rank question | Judging words; red–green; inventing a scorecard; measure-sort from the page H1 alone |
| Fast facts with a movement clause so teasers cannot go stale | Ticker of unnamed numbers; engagement SDK |
| Method after the record | Opinion, forecast, partisan report card |

## Data visualization focus

- **One idea per chart.**
- **The number is the hero.** Display size is for bound figures, not slogans.
- **No performance colour.** Default order alphabetical / documented geographic. Measure-sort only when the chart caption is a rank question and the template declares it.
- **Holes stay holes.** Gap phrase **not published**; never plot a gap as zero. Published zero looks and reads differently.
- **Source on the figure’s view.** Attribution is the citation card, not a corner logo.

## High scannability

1. Sleeve — topic family, not a kicker
2. H1 — citizen question, geography in the words
3. Byline — release date (`Asia/Kolkata`), next named release
4. Thesis / movement / what-it-is (`.fact-lede`)
5. Stat row — 2–4 equal-weight bound figures, unit in the cell
6. Cite strip — producer, series as named for a person, period, released
7. First chart — the figure the thesis just stated

Then: one section, one idea, one chart. Methodology after the record.

## Voice

Calm, specific, adult. Spoken sentences. No hedging that empties the answer.

**Forbidden.** Judging words; nicknames that smuggle a verdict; party names as causes; `laggard` / `best` / `worst` as a score; forecasts.

**Allowed rank words** when the **chart caption** is a rank question and the vintage binds the measure: `highest`, `lowest`, `led`, `ranked last`, `top five`.

**Surface.** House accent marks only the bound answer clause in the thesis — never a definition or a section title. No magenta `span.answer`. No engagement SDK.

```text
# ❌ BAD
The Consumer Price Index (General), Base 2024=100, is a measure of…
This page is not a forecast.

# ✅ GOOD (slots in the template)
Retail prices were {cpi_general_yoy} percent higher in {period} than a year earlier.
A month earlier the rate was {cpi_general_yoy_prior} percent.
It is the change in the prices households actually pay, measured on the same basket each month.
```

## Content Editor passes

Run **in order**. Three tests every pass: **integrity** (cited slots; holes and dual series visible); **resonance** (R1–R6 shape); **jargon** (page still reads if annex tokens are stripped).

1. **Development** — Keep or drop sections. Shape: question, thesis/movement/what-it-is, evidence that further answers, method. Cut codebook tours and aside-led sections. Rank charts only when the caption is a rank question.
2. **Line** — Thesis first; movement; one what-it-is. Skip annex tokens above the fold. Chart titles are citizen questions or plain names — not lectures.
3. **Copy** — Slots only. Units in chips. Movement via signed comparable periods. Asides and series teaching → method.
4. **Proof** — On the rendered page, **read it aloud** first (R6). Fail on the first R1–R6 break. Then scan path and form-factor list for UI/UX — naming a break is not fixing it.

Then UI/UX presentation pass → Trust (cites, dates, holes, spin, M1, M2) → Principal resonance read (advisor) → Charter.

## Who writes what

| Job | Who |
|-----|-----|
| Citizen template: development → line → copy → proof | Content Editor (this file) |
| Type, colour, layout, chart chrome; presentation pass | UI/UX Developer — [design-system.md](design-system.md) |
| Routes, `<title>`, meta, preview HTTP | Front-end Architect — [web-design.md](web-design.md) |
| Cites, dates, holes, spin, M1, M2 | Trust Auditor |
| Resonance R1–R6 on preview (advisor) | Principal → notes to Charter |
| Ship or block | Charter Editor |

Do not skip Trust Auditor on anything a citizen will see.
