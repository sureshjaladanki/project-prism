# Editorial guidelines

Content Editor. Standing reading contract for every citizen template. What the portrait is for: [vision.md](vision.md). The record: [data-contracts.md](data-contracts.md).

This file governs copy, scan path, voice, and chart *meaning*. [presentation-charter.md](next/presentation-charter.md) applies it to C1; it does not replace it. [design-system.md](design-system.md) implements the look (type, colour, layout, chart chrome) — UI/UX Developer owns and implements that file.

```text
role:           civic fact desk — official numbers, readable, no verdict
craft:          story-shaped explainer; visual-first; no newsroom
reference:      USAFacts answer-page shape — not the product, magenta look, or media desk
```

## Stance

A shared, checkable picture of India from official government statistics — and nothing else. High or low, good or bad: the reader decides.

[USAFacts](https://usafacts.org/) is an inspirational *role*: make government data usable; do not tell people what to think. Take the **answer-page shape** (citizen question, fact-lede, evidence, method). Bound ranks, a house-highlighted fact-lede, fast-facts / featured-slice rails, and named analysis of official series are in — in our tokens, as slots. Do not copy that site, its topics, its American frame, its media desk, or its look (magenta, cream plot, Aeonik, wordmark). A page that would pass for USAFacts with the wordmark swapped has failed these guidelines.

## Data integrity

The page is a window on one **data vintage**. It is not reporting. Prism may analyze official series and say so. It does not become the statistical office and does not replace the citation.

- **Official sources only.** Union and state statistical systems, the Census, the Reserve Bank of India, and other mandated public series. Cite the producer, the series, and the date. The producer stays the agency.
- **Slots, not typed figures.** Copy binds to observations at render. If the vintage has no observation, the page reads as unknown or not published — never as a remembered number. Do not invent figures.
- **Cite in the same view.** Producer, series, reference period, release date (`Asia/Kolkata`), geography vintage, data vintage, and caveat sit with the number. A tooltip is not enough. An “Analysis by Prism” byline may sit next to that cite — never instead of it. Those fields live on the **collapsed card**, not in the byline or the fact-lede.
- **Citizen names, producer cards.** Running copy, labels, and chart titles use ordinary names (food, Food and beverages). Distinguishing two official series does not mean teaching annex codes, `vintage_id`, or base-year notation (2024=100). The card still prints the series as the producer prints it.
- **Name derived work.** Ranks, comparable periods, standardized frames, and derived tables already in the vintage may be named as Prism analysis. They are still slots on that vintage.
- **Trust the method.** Breaks, lags, holes, and two official numbers stay visible. Do not pick a winner, smooth a hole, or draw a continuous line across a break.
- **India as it is governed.** Union, states, and Union Territories as published. Name missing units. An All India figure is not “the whole country” when districts or large populations are out of sample.
- **Context in, verdicts out.** What was counted, who was counted, when. Not what it proves about a ministry or a mandate.

A pretty page that hides a break or a cite still fails.

## Corporate-style civic reporting

Write like a calm public fact desk — the numbers a ministry already publishes, without a decoder ring. Not a newspaper, not a brochure, not a company filing.

**In:** named source; comparable period; stated coverage; named holes; equal weight on comparable published figures; adult, specific, unhurried; named analysis of official series already in the vintage.

**Out:** calling the product a 10-K or SEBI LODR; consolidating Union and states into one “issuer”; ROI, risk factors, or listed-company metaphors; achievement copy; Prism as the statistical office; invented figures; replacing the agency cite.

The Union is not a company. The citizen is not a shareholder. Money pages cite Finance Accounts / CGA / CAG as printed. Statistical pages cite NSO / MoSPI / Census / RBI as printed.

## Story-shaped explainer

A page is **question → fact-lede → evidence → method**. That is the USAFacts answer-page shape. It is not a newsroom story and not their look.

The fact-lede must answer the H1 with bound slots: number, unit, place, and year. Then one sentence of definition. It may be visually highlighted in house chrome (see [design-system.md](design-system.md) `.fact-lede`). Evidence sections are further answers to that same question — not a plot (setup, conflict, payoff). Sub-questions may be section headings if they are citizen questions the vintage can answer. A numbered list sorted by the published measure is in only when the H1 is a rank question.

| In | Out |
|----|-----|
| One citizen question as the title | Scoops, news-cycle tickers, “get notified” |
| Fact-lede answering the H1 from slots, then the figures; house highlight of that lede | Magenta `<span class="answer">`; slogan; “what this means” about a ministry |
| Bound ranks when the vintage supports them and the question is a rank question: highest/lowest, led, ranked last, top five, numbered list sorted by the published measure | Judging words; party names as causes; red–green performance colour; inventing a scorecard |
| Fast facts: compact row of bound one-line facts (the stat row, or a named rail of 3–4 slot-bound facts). Hottest rails: featured citizen questions / slices | Ticker of unnamed numbers; trending news; engagement SDK |
| Named analysis of official series already in the vintage; “Analysis by Prism” beside the producer cite | Prism as MoSPI / Census / RBI; invented figures; dropping the agency cite |
| One idea per section, same question; sub-questions only if the vintage can answer them | Narrative arc; league table on a non-rank slice; spin |
| Method after the record | Opinion, forecast, partisan report card, press-release recap, Economic Survey voice |

Journalists are readers. We do not ship a reporter’s piece. We do ship an explainer with that shape.

## Data visualization focus

Charts carry the record. Copy labels them. Neither argues.

- **One idea per chart.** If it needs a paragraph to explain two encodings, split it.
- **The number is the hero.** Display size is for bound figures, not slogans.
- **No performance colour.** Colour and weight never mean better or worse. States and UTs default to alphabetical by official English name, or a documented geographic order. Sort by the published measure only when the citizen question is a rank question and the vintage can bind that order. No red–green maps, no podium palette.
- **Holes stay holes.** `unknown`, `not_comparable`, and `series_break` are encodings. A footnote is not a licence to stitch a line.
- **Source on the figure’s view.** Compact citation chrome. Attribution is the citation card, not a corner logo.
- **Screenshot test.** A crop still shows title, unit, geography, a source line, and visible holes. It does not look like a USAFacts chart.

Infographics that tell the reader what to think are out. Chart chrome: [design-system.md](design-system.md).

## High scannability and visual-first

The first screen is the page. Method sits behind it, not in front of it.

**Scan path**

1. Sleeve (topic family — not a news kicker)
2. Citizen question as H1 (geography in the words)
3. Byline: release date (`Asia/Kolkata`), next named release. Data vintage is internal — collapsed citation cards, not the byline.
4. Fact-lede: answers the H1 with bound number, unit, place, and year — then one sentence of definition. House highlight (`.fact-lede`) is allowed. Still true if you only read the caveat. Not a slogan.
5. Stat row / fast facts: comparable published figures (2–4, equal weight), or a named rail of 3–4 slot-bound one-line facts — not a ticker of unnamed numbers
6. The first chart for those figures
7. Citation and caveat for everything on this view, compact. Optional “Analysis by Prism” next to the producer — not instead of it.

Then: one section, one idea, one chart. Methodology after the record. Charter-outs sit in Methodology, not as a separate “Not on this page”.

**Do**

- Lead with the fact the question asked: number, unit, place, year. Then the definition.
- Prefer a labelled figure and a short sentence over a codebook column before the first chart.
- Keep running prose short. Put coverage, holes, and dual series next to the chart they belong to.
- Collapse full citation cards behind a visible summary line; never hide them off this view.

**Don’t**

- Front-load annex codes, methodology, or definition lists before the first figure.
- Use a ticker of unnamed numbers, a trending-news rail, or “get notified.”
- Highlight a sentence to smuggle a slogan or “what this means.” House `.fact-lede` on the bound answer is in.
- Invent a scorecard, call a laggard, or paint red–green rank colour. Measure-sort only on a rank question.

## Voice

Calm, specific, adult. A journalist and a sceptical uncle should recognise the same fact. Neither should think you told them how to vote.

**Forbidden.** Judging words (`impressive`, `failed`, `despite`, `thanks to`). Nicknames that smuggle a verdict (`burden`, `miracle`, `crisis`). Party names as causal agents. Verdict rank talk (`laggard`, `best`, `worst` as a score). Forecasts and speculation.

**Allowed rank words** when the H1 is a rank question and the vintage binds the measure: `highest`, `lowest`, `led`, `ranked last`, `top five`. Alphabetical / documented geographic order remains the default on every other slice.

**Surface.** Chrome can smuggle a takeaway. House highlight of the fact-lede is allowed (`.fact-lede`, `--mark` / `--card` / `--paper`) — still slots, still true if you only read the caveat. Fast facts and hottest rails are desk chrome: bound one-liners and featured citizen questions, not a newsroom. An analysis byline is desk chrome beside the producer cite, not a second office. No magenta `span.answer`. No engagement SDK. UI/UX must not smuggle tone through decoration. Token forbids that encode this (tricolour as brand or scale; party palettes; saffron/green as up/down) live in [design-system.md](design-system.md).

**When the series is incomplete.** Say so in the same view. Do not fill a hole with a plot or a remembered figure.

```text
# ❌ BAD
Kerala leads the country on literacy as southern states pull ahead.

# ✅ GOOD (rendered page — in the template the rate is a slot)
In Census 2011, 94.0% of people aged 7 and above in Kerala were recorded as
literate. The Census definition counts anyone who can read and write with
understanding in any language. States are listed here in alphabetical order.
Census 2011 is the latest census with released literacy tables.
```

## Content Editor passes

Content Editor runs these **in order** on every template. They are not extra personas. Stop after each. A later pass must not put back what an earlier pass cut.

Three tests, every pass: **integrity** (cited slots, holes and dual series still visible); **explainer** (each kept section further answers the H1 — not metrics restated as headings); **jargon** (the page still reads if you strip every annex token). Integrity is not the same as teaching the codebook.

1. **Development** — Keep or drop whole sections. Shape: citizen question, fact-lede, evidence that further answers that question, Methodology. Not a plot. Not a codebook tour. If the question is not a rank question, no league table — alphabetical / documented geographic order. Do not write sentences yet. Completeness (including data vintage) stays in collapsed citation/caveat chrome — not on the byline, not as method on screen 1. Copy and proof may not restore a dropped section.
2. **Line** — Keep, skip, or rephrase sentences, paragraphs, and words. Fact-lede: bound answer, then what was counted / who / when — not producer notation. Skip any word the reader does not need to understand the number (`vintage_id`, base-year equals, Division/Group codes). Chart titles and labels name the thing in citizen words; they do not argue and they do not lecture the annex. Do not add a section Development dropped.
3. **Copy** — Slots, not typed figures. Forbidden judging words out. Rank words only when Development kept a rank question. Two official numbers stay two numbers, named as the citizen already speaks (food vs Food and beverages) — not as annex codes. Named analysis does not replace the producer cite. Coverage, holes, and dual series sit next to the chart they belong to, in one short sentence.
4. **Proof** — On the rendered page, read as a citizen first. Fail if the H1 is not answered; if a section is a codebook recap; if annex tokens, vintage ids, or base-year notation appear in the byline, lede, evidence, source-lines, or chart titles the reader sees (cards may still print the producer series). Then chrome as a scan, not art direction: scan path; house `.fact-lede`; source-line in view; full cards collapsed once with the numbers; no codebook before the first figure; hottest rail is featured slices; analysis byline beside the agency cite. If Proof sees a form-factor break (mixed plot widths, leftover white in a `--card` well, bars that fatten with few categories, Vega titles instead of HTML H2/byline), hand to UI/UX Developer. Content Editor does not restyle charts.

Then, if chrome or charts changed, UI/UX Developer runs the **presentation pass** against [design-system.md](design-system.md). Then Trust Auditor (cites, dates, holes, spin). Not a fifth Content Editor writing pass. Trust does not become a style editor; Content Editor does not print codebook tokens to pre-empt Trust.

## Who writes what

| Job | Who |
|-----|-----|
| Citizen template: development → line → copy → proof | Content Editor (this file) |
| Type, colour, layout blocks, chart chrome; render; presentation pass | UI/UX Developer — [design-system.md](design-system.md) |
| Routes, `<title>`, meta, preview vs published HTTP | Front-end Architect — [web-design.md](web-design.md); question and fact-lede copy stay Content Editor; UI/UX implements the route |
| Cites, dates, holes, spin | Trust Auditor |
| Ship or block | Charter Editor |

Do not skip Trust Auditor on anything a citizen will see.
