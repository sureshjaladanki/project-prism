# Presentation charter

Charter Editor. Apply the standing reading contract to C1 without retuning the pipeline. C1 in/out/source_class unchanged. C1 Trust passed; data-slice ship is [c1-charter-verdict.md](c1-charter-verdict.md). This note is the look contract, not a second Trust.

Governing reading: [editorial-guidelines.md](../editorial-guidelines.md). Governing look: [design-system.md](../design-system.md).

```text
slice:          How should a citizen page look, without weakening the record?
in:             C1 (and later slices) as template + one vintage; editorial-guidelines scan path; compact citation chrome; layout blocks; Content Editor rewrite of copy; Vega-Lite that still shows breaks and holes
out:            pipeline schema changes for layout; Next.js / ISR / request-time fetch; tooltip-only cites; anything editorial-guidelines or the design system forbid; engagement / A/B SDKs
source_class:   (unchanged — this is not a data slice)
next_persona:   ui-ux-developer
block_reason:   none on this charter. Data-slice ship is c1-charter-verdict. UI/UX Developer may flip citizen_pointer to dv-20260916-234e263c8588 after the nine tests.
```

## Decision

**Editorial guidelines govern how the page reads.** This charter does not restate them. Design-system implements them as type, colour, layout, and chart chrome. Do not invent a third reading contract.

**Do not retune the data pipeline for presentation.** Integrity is the spine: cited observations, immutable vintages, one vintage per page. Layout, type, and reading order do not belong in Parquet or `manifest.json`.

**The locked stack does not block a compelling page.** Astro SSG, Markdown/YAML templates, and Vega-Lite can do the scan path in the editorial guidelines. That is a Content Editor + UI/UX job, not a framework swap. Do not add Next.js, ISR, or a request-time producer fetch.

[USAFacts](https://usafacts.org/) remains an inspirational *role* only, as the editorial guidelines already say. Do not paint C1 to resemble that site.

Trust fail #3 and the division-axis order hole are closed on preview. Presentation tokens stay on this vintage. It is not a reason to start C2.

## What is actually missing

The pipeline is doing its job. C1 preview uses desk layout primitives (`src/cms/src/layouts/SiteShell.astro`, `src/cms/templates/c1-prices-people-pay/template.md`). First screen vs Methodology is a Content Editor scan-path job already on this vintage, not a pipeline retune.

Editorial review is not a new ingest step. Passes: [editorial-guidelines.md](../editorial-guidelines.md) (Who writes what). Trust Auditor does not become a style editor. A pretty page that hides a break or a cite still fails.

## Allow / deny for the page

**Allow**

- Layout blocks the template can name: hero question, stat row, section, chart, compact source byline, “how this is measured”.
- House `.fact-lede` highlight; `stat-row` / `.fast-facts`; `.hottest-rail` of featured citizen questions / slices — per [design-system.md](../design-system.md).
- Bound ranks when the slice question is a rank question and the vintage supports the published measure.
- “Analysis by Prism” (`.analysis-byline`) next to the producer cite. It does not replace the agency.
- CSS grid / type / colour that is not a performance scale, per [design-system.md](../design-system.md).
- Geography as pre-rendered routes or a client filter **over observations already bound from one vintage**.
- Vega-Lite hover/download from that bound spec. Breaks and `unknown` stay visible.
- Citation chrome that is compact **and still in the same view**. A collapsed `<details>` on that view is allowed. A tooltip as the only cite is not.

**Deny**

- Moving layout, copy, or UX into ingest, vintage schema, or DuckDB.
- Next.js, ISR, `revalidate`, request-time fetch of MoSPI.
- Client engagement, heatmap, or A/B SDKs.
- Anything [editorial-guidelines.md](../editorial-guidelines.md) forbids (verdicts, partisan report cards, newsroom scoops, 10-K / SEBI LODR metaphors, story infographics, invented figures).
- USAFacts look (magenta, cream plot, Aeonik, wordmark), topics, or media desk. Colour and type forbids: [design-system.md](../design-system.md).
- Prism as the statistical office, or an analysis byline that drops the producer cite.

## Next

Preview is on `dv-20260916-234e263c8588`. C1 data-slice ship is [c1-charter-verdict.md](c1-charter-verdict.md). Do not paint C1 to resemble USAFacts. Do not start C2 from this note.
