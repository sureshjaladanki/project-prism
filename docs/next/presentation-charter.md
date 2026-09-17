# Presentation charter

Charter Editor. Dispute: retune the data pipeline vs build a USAFacts-like citizen page. C1 in/out/source_class unchanged. Citizen pointer stays unpublished. Trust fail #3 on C1 is still open — a redesign does not close it.

```text
slice:          How should a citizen page look, without weakening the record?
in:             C1 (and later slices) as template + one vintage; first-screen hierarchy; compact citation chrome; layout blocks; editorial rewrite of copy; Vega-Lite that still shows breaks and holes
out:            pipeline schema changes for layout; Next.js / ISR / request-time fetch; tooltip-only cites; newsroom verdicts; USAFacts topics, newsletter, social, “hottest topics”; ranking or red–green maps; engagement / A/B SDKs
source_class:   (unchanged — this is not a data slice)
next_persona:   cms-engineer
block_reason:   none on this charter. Do not treat this as a ship of C1. Do not flip the citizen pointer.
```

## Decision

**Do not retune the data pipeline for presentation.** Integrity is the spine: cited observations, immutable vintages, one vintage per page. Layout, type, and reading order do not belong in Parquet or `manifest.json`.

**The locked stack does not block a compelling page.** Astro SSG, Markdown/YAML templates, and Vega-Lite can do hero numbers, sectioned layouts, whitespace, and clean charts. USAFacts-looking pages are a Portrait + CMS job, not a framework swap. Do not add Next.js, ISR, or a request-time producer fetch.

C1 is still blocked on Trust fail #3 (July Final Combined bound to the wrong citation month) and the division-axis order hole. Close those on preview. Presentation may proceed on the same preview vintage. It is not a reason to start C2.

## How USAFacts presentation is characterized

Vision takes the *role*, not the American product. USAFacts is characterized as **three things at once**. We take two of them as craft. We do not become the third.

**1. Civic aggregator with disclosure discipline**

Ballmer’s origin story: government data should be as usable as a public company’s annual report. Wired (2017) quotes him: put the data “in an orchestrated way so people can find it and create their own analysis.” Gaps, delays, and revisions are named. That is disclosure, not a scorecard. We already require producer, series, date, geography vintage, and caveat in the same view.

This is **not a 10-K and not SEBI LODR.** Those are company filings. The Union is not an issuer; the citizen is not a shareholder. Money is C3/C5, citing Finance Accounts / CGA / CAG as published — not “India Inc.”

**Closest analogue for a civic reporting desk.** USAFacts’ 10-K is only their *spending* product. The rest of the site (answers, charts) is a statistical fact desk. We copy neither the form nor the newsroom. We copy the desk that already exists in Indian official life, made readable.

| What USAFacts bundled | Closest Indian analogue | Our desk |
|----------------------|-------------------------|----------|
| Government 10-K (spend / revenue / debt as one issuer) | **Finance Accounts** and **Appropriation Accounts** (CGA, certified by CAG); **Combined Finance and Revenue Accounts** when CAG publishes Union-and-state together; CGA monthly accounts; FRBM statements. **Budget at a Glance** tables for aggregates — not its infographic copy | **Public-accounts fact desk** on C3 (Union) then C5 (states). Cite the producer. Do not consolidate. |
| Inflation / people / other “answers” | **NSO / MoSPI dissemination**: press note, annex, Statistical Yearbook, metadata — the same numbers, without a decoder ring | **Statistical fact desk** (Portrait Editor). C1 is this. |
| Independent check | CAG on accounts; Methodologist + Trust Auditor on the page | Trust Auditor. We do not audit the government. |

The desk is **not** a newspaper, SEBI IR shop, or Economic Survey. Journalists are readers. The producing office remains the source.

C1 stays the first page of that fact desk. C3 is the first page of the public-accounts desk. Do not start C3 until C1 can ship.

**2. A visualization system, not a data.gov dump**

Artefact (the launch design studio) and Wired characterize the site as the opposite of bureaucratic portals: one visual language, glanceable charts, type you can actually read, drill from the whole to the part without losing the whole. Charts: sparklines, flow diagrams, annotations, source buttons with agency and date. Later viz system (Artefact 2025): cream ground, magenta edge rule, accessible colour, label standards — charts that survive a screenshot and still look like the same house.

Artefact is explicit: infographics usually *tell a story*; USAFacts charts **must not editorialize**. “We want users to draw their own conclusions, so we let the numbers speak for themselves.” Wired notes the tension: infographics are inherently editorial; their answer is transparency of source, not a verdict in the graphic.

That is **data visualization focus**. C1’s codebook column is the bureaucratic portal they designed against. Layout blocks, hero numbers, and one idea per chart are in. Rank colour, homemade merges, and “story” infographics are out.

**3. A later media desk (we are not this)**

USAFacts also runs as a content organization: “answers,” articles, Viz Lab, newsletters, Ad Fontes media ratings, a press page that sells “sharp analysis and compelling narratives,” a Shorty Awards write-up of ~10 articles a week with a five-person edit (writing, edits, data check, viz). That is **data journalism as a newsroom**. Our vision: not a newsroom, not a news cycle. Journalists are an *audience*. We do not ship scoops, hottest-topics carousels, or narrative arcs.

**Informative presentation** is the craft those articles borrowed: citizen question, short lede, large number, one chart, method at the back. That craft is in. The newsroom is out.

Their inflation answer page (closest analogue to C1) is that craft, not a codebook:

1. Sleeve label + citizen question as the title (geography in the question).
2. Updated date and refresh cadence near the top.
3. A short lede, then **large numbers** (headline / core) with a one-line source.
4. One idea per section: a factual heading, a chart, a download. Sources sit in a panel, not a wall of definition lists before the first chart.
5. Methodology at the bottom. Related questions after the record.

“Dynamic” there is mostly: geography as a route or picker, client charts from already-loaded series, collapsible source panels. It is not a live scrape.

Take those habits. Do not take: hottest-topics carousels, newsletters, social kits, city search we cannot cite, ranking language, “analysis by us” as a second producer, or a combined-government 10-K.

## Three phrases, in or out

Integrity stays the spine. These are *how the page reads*, not a pipeline retune.

| Phrase | In (craft) | Out (product) |
|--------|------------|----------------|
| Data journalism (informative presentation) | Question page; lede; first screen vs method; calm copy; editorial passes (developmental, line, copy); proof of cites | Newsroom, news cycle, “compelling narrative,” scoops, hottest topics |
| Data visualization focus | Unified chart language; glanceable stats; one idea per chart; breaks and holes visible; source on the figure | Infographic that tells the reader what to think; red–green performance; rank sort |
| Corporate-style civic reporting | Named source, date, comparable period, stated holes; C3/C5 accounts as the producer prints them | Product called 10-K or SEBI LODR; homemade Union+states firm; risk factors; ROI or listed-issuer metaphor |

USAFacts themselves *combine* federal, state, and local and standardize for the 10-K. We do not. India as it is governed: Union, states, and UTs as published, missing units named. Two official numbers stay two numbers.

## What is actually missing

The pipeline is doing its job. The citizen page is a single 46rem column of method prose, full citation cards, and charts of equal weight (`src/cms/src/layouts/PortraitPage.astro`, `src/cms/templates/c1-prices-people-pay/template.md`). Portrait Editor already owns “first screen vs how this is measured.” That split is not on the page.

Editorial review is not a new ingest step:

| Pass | Who |
|------|-----|
| Developmental (what is on screen 1) | Portrait Editor |
| Line and copy (calm, specific, adult) | Portrait Editor |
| Visual system (stat, section, byline, chart frame) | CMS Engineer |
| Proof of cites, dates, holes | Trust Auditor (existing) |

Trust Auditor does not become a style editor. A pretty page that hides a break or a cite still fails.

## Allow / deny for the page

**Allow**

- Layout blocks the template can name: hero question, stat row, section, chart, compact source byline, “how this is measured”.
- CSS grid / type / colour that is not a performance scale.
- Geography as pre-rendered routes or a client filter **over observations already bound from one vintage**.
- Vega-Lite hover/download from that bound spec. Breaks and `unknown` stay visible.
- Citation chrome that is compact **and still in the same view** (producer, series, date, geography vintage, data vintage, caveat). A collapsed `<details>` on that view is allowed. A tooltip as the only cite is not.

**Deny**

- Moving layout, copy, or UX into ingest, vintage schema, or DuckDB.
- Next.js, ISR, `revalidate`, request-time fetch of MoSPI.
- Client engagement, heatmap, or A/B SDKs.
- Verdict words, state ranks, red–green maps.
- USAFacts chapters that are not India’s official spine.

## Next

Preview is on `dv-20260916-234e263c8588` for review of the first screen (CMS bind + layout primitives; Portrait rewrite). Loop CMS + Portrait until that screen is good enough.

Hold Trust Auditor and Charter Editor ship/block until that review. Do not start C2. Do not flip `citizen_pointer`.
