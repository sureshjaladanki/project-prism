# Design system

UI/UX Developer. Visual contract for citizen pages. Persona: [ui-ux-developer.md](personas/ui-ux-developer.md). How the page **reads** is [editorial-guidelines.md](editorial-guidelines.md) (Content Editor) — this file implements that as type, colour, layout, and chart chrome. UI/UX Developer implements this file and runs the presentation pass against it. Routes, titles, SEO, and preview vs published HTTP: [web-design.md](web-design.md) (Front-end Architect). Integrity stays in [data-contracts.md](data-contracts.md) and [architectural-blueprint.md](architectural-blueprint.md). C1 application: [presentation-charter.md](next/presentation-charter.md).

Product role, answer-page shape, and newsroom forbids live in the editorial guidelines. Stack (Astro SSG, Vega-Lite) lives in [repo-conventions.md](repo-conventions.md). C1 pointer work lives under [Next](#next).

```text
tone:           corporate, professional, minimal, modern
look:           house tokens; not USAFacts magenta, cream, Aeonik, or wordmark
tokens:         CSS custom properties on :root — not in the vintage
```

## Decision

One quiet visual language for the portrait in [vision.md](vision.md). A citizen should recognise the same house on every slice: large cited numbers, calm type, charts that do not argue.

This system does not restate voice, scan path, or newsroom forbids. Those live in the editorial guidelines. [USAFacts](https://usafacts.org/) is not a look to reproduce: no brand marks, magenta, cream plot, Aeonik, or chart-corner logo. Bound ranks, a house-highlighted fact-lede, fast-facts / featured-slice rails, and an analysis byline use **our** tokens (`--mark`, `--paper`, `--card`).

Do not retune the pipeline for layout. Content Editor names blocks; UI/UX specifies and applies the styles.

## Look we do not copy

Reading craft is in the editorial guidelines. This system forbids the costume:

- Magenta bar, Aeonik, pink/magenta sentence highlight (`span.answer`)
- Purple illustrated heroes; a news-style hottest-topics carousel (scoops, engagement)
- Newsletter, social kits, “get notified”, video desk
- Cream plot, brand-colour edge rule, magenta download pill, chart-corner logo

A page that would pass for USAFacts with the wordmark swapped has failed this system.

## House chrome we do use

Same desk tokens. Not a second palette.

| Class | Tokens | Job |
|-------|--------|-----|
| `.fact-lede` | `--card` on `--paper`; 3px `--mark` rule; `--ink` type | Optional highlight of the bound fact-lede (number, unit, place, year — then definition). Not magenta. Not a slogan box. |
| `.fast-facts` | `--card`, `--ink`, `--muted` labels | Compact 3–4 slot-bound one-line facts. May be the `stat-row`. Not a ticker of unnamed numbers. |
| `.hottest-rail` | `--paper`, `--card`, `--mark` links | Featured citizen questions / slices. Sleeve-appropriate. No scoops, no “get notified.” |
| `.analysis-byline` | `--muted` on `--card` | Optional “Analysis by Prism” next to the producer cite. Never instead of the producer. Not a second wordmark. |

## Visual encodings

These encode the editorial guidelines as chrome. Do not treat them as a second reading contract.

1. **No performance colour.** Colour and weight never mean better or worse. Order is alphabetical / documented geographic by default. Measure-sort is allowed only when the citizen question is a rank question.
2. **The number is the hero.** Display type is for bound figures, not for slogans.
3. **Cite chrome in the same view.** Producer, series, date, geography vintage, data vintage, caveat. A tooltip is not enough. Optional `.analysis-byline` sits beside the producer — it does not replace the agency.
4. **Holes stay holes.** `unknown`, `not_comparable`, and `series_break` are encodings, not styling problems to smooth away.
5. **Quiet chrome.** Hairlines, whitespace, one accent. No gradient, shadow, or illustration that the vintage did not earn.

## Tokens

Implement as CSS custom properties on `:root` in the citizen layout. Do not put them in the vintage schema.

### Colour

Warm stone paper, ink type, navy as the only accent. Navy is already how C1 charts plot a series (`#1f4e79`). It is institutional, not a performance colour.

| Token | Hex | Use |
|-------|-----|-----|
| `--paper` | `#F4F2EE` | Page ground |
| `--card` | `#FFFFFF` | Stat cell, chart well, citation panel |
| `--ink` | `#1A1A1A` | Body, headings, figures |
| `--muted` | `#5A5A5A` | Byline, labels, axis titles (AA on paper) |
| `--rule` | `#D6D2CA` | Hairline borders, grid |
| `--mark` | `#1F4E79` | Links, focus, chart series 1, quiet header rule |
| `--mark-2` | `#7A542E` | Chart series 2 only (categorical) |
| `--mark-3` | `#4A6670` | Chart series 3 only (slate; not “good”) |
| `--mark-4` | `#5C5C5C` | Chart series 4 / residual |
| `--hole` | `#8A8A8A` | Unknown / not published copy |
| `--focus` | `#1F4E79` | Keyboard focus ring |

**Forbidden as tokens:** magenta / hot pink; wine used as a USAFacts-style edge; red–green pairs; gold/saffron; saturated “dashboard” blues; the tricolour as brand or as a scale (it reads as the flag, or as a scorecard); party colours or ministry campaign palettes; saffron/green as up/down.

Links are `--mark` plus underline. Visited is the same (this is a record, not a web of explored lore).

### Type

Sans throughout. Corporate and modern; not a literary serif, not a fashion grotesque.

| Role | Face | Notes |
|------|------|--------|
| UI, body, headings, figures | **IBM Plex Sans** | Weights 400 / 500 / 600. Tabular figures on every observation. |
| Identifiers | **IBM Plex Mono** | `vintage_id`, `series_id`, geography codes — not body copy. |
| Later scripts | IBM Plex Sans Devanagari | Pair when a template ships a non-English official name. English is first. |

Self-host under `src/cms/public/fonts/`. Do not hotlink a font CDN at render or at request time. Fallback: `"IBM Plex Sans", "Source Sans 3", "Segoe UI", system-ui, sans-serif`.

Do not use Aeonik (theirs, proprietary). Do not keep Source Serif 4 as body (current layout) — it reads as a journal, not a desk.

**Scale** (root 16px)

| Style | Size | Weight | Line | Tracking |
|-------|------|--------|------|----------|
| Sleeve | 0.75rem | 500 | 1.3 | 0.08em; uppercase |
| Display figure | 2.75rem | 600 | 1.05 | −0.03em; `font-variant-numeric: tabular-nums` |
| H1 (citizen question) | 2rem / 2.25rem | 500 | 1.2 | −0.02em |
| H2 (section) | 1.25rem | 500 | 1.3 | 0 |
| Body | 1.0625rem | 400 | 1.55 | 0 |
| Byline / source summary | 0.875rem | 400 | 1.4 | 0 |
| Label / dt | 0.75rem | 500 | 1.3 | 0.04em; uppercase; `--muted` |
| Caption / hole | 0.8125rem | 400 italic for holes | 1.4 | 0 |

H1 is a question, not a billboard. The bound figure is the display size.

### Space, line, radius

| Token | Value | Use |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 px | Stacking only these steps |
| `--measure` | 40rem | Unused for column width |
| `--desk` | 68rem | Page column (prose, stats, charts) |
| `--radius` | 0 | No rounded marketing cards |
| `--hair` | 1px | Borders |
| `--header-rule` | 3px `--mark` | Top of the viewport only |

No box-shadow. No gradient. Elevation is a hairline on `--card` against `--paper`.

## Layout primitives

Content Editor may name only these blocks (already in `LAYOUT_BLOCKS` in `src/prism/template_bind.py`). Do not invent a second set of layout tokens in YAML.

| Token | Element | Job |
|-------|---------|-----|
| `hero` | `<header class="hero">` | First screen: sleeve, question, byline, fact-lede that answers the H1, stat row, first chart, cites for those numbers |
| `stat-row` | `<div class="stat-row">` | 2–4 bound figures, equal weight, no winner colour |
| `section` | `<section class="portrait-section">` | One idea; heading; copy; optional stats; one chart; cites |
| `how-this-is-measured` | `<section class="how-measured">` | Method after the record |
| compact source byline | `<details class="citation-card source-byline">` | Summary line visible; full card on open |
| caveat note | `<details class="caveat-note">` | Same rule |

**Site chrome** (UI/UX Developer, not Content Editor copy). Same tokens. Not a second palette, not a full-bleed marketing bar, not a USAFacts wordmark. Routes and labels: [web-design.md](web-design.md).

| Region | Class | Tokens | Job |
|--------|-------|--------|-----|
| Skip link | `.skip-link` | `--card` fill, `--mark` type, `--hair` `--rule`; 44px hit | First focusable; off-screen until `:focus-visible` |
| Header rule | `body` border-top | `--header-rule` `--mark` | Top of the viewport only |
| Frame | `.site-frame` | `--desk` column; `--space-5` / `--space-8` padding | Header, `main`, footer share it |
| Header | `.site-header` | flex wrap; gap `--space-4` | Lockup + sleeve nav |
| Lockup | `a.site-lockup` | 0.875rem / 500 / 0.04em uppercase; `--ink`; no underline | Links to `/`. Wordmark, not a sleeve link |
| Sleeve nav | `.sleeve-nav a` | `--mark` + underline; min-height 44px | Five sleeves. `aria-current` is weight 600, not a second colour |
| Breadcrumb | `.breadcrumb` | byline 0.875rem; `--muted`; current `--ink` | Hub and slice only |
| Main | `main#main` | `--desk` (via `.site-frame`) | Page type |
| Footer | `.site-footer` | hairline `--rule`; byline size; 44px hits | Sleeves + house. No SDK |
| Fast facts (home) | `.fast-facts` | `--card`, `--ink`, `--mark` links | One bound one-liner per catalog slice |
| Hottest rail | `.hottest-rail` | already above | Featured questions |
| Sleeve index | `.sleeve-index` | body type; `--mark` + underline; 44px hits | Five hub links. Not a tile grid |

No search, subscribe, or social row. No engagement SDK. Home H1 uses the same H1 scale as a citizen question — not display-figure size, not a billboard.

**Grid.** `stat-row` is CSS grid, `minmax(9.5rem, 1fr)`, gap `--space-4`. Charts and running prose share `--desk` width, left-aligned. Do not centre the question.

**First screen (C1 and every later slice).** Implements the scan path in [editorial-guidelines.md](editorial-guidelines.md). Do not add magenta highlight, unnamed-number ticker, trending-news rail, or “get notified.”

1. Sleeve (topic family, not a news kicker).
2. Citizen question as H1 (geography in the words, not a US-style dropdown until a bound geography route exists).
3. Byline: release date (`Asia/Kolkata`), next named release, data vintage.
4. Fact-lede that answers the H1 (bound number, unit, place, year) then one sentence of definition — optional `.fact-lede` house highlight.
5. Stat row of the comparable published figures (fast facts), or a `.fast-facts` rail of 3–4 bound one-liners.
6. The first chart for those figures.
7. Citation and caveat for everything on this view, compact. Optional `.analysis-byline` next to the producer.

“Methodology” is not on screen 1. Charter-outs stay in Methodology, not as a separate closing section.

## Chart system

Vega-Lite in git; SVG at render. `src/cms/src/lib/render-chart.ts` applies the frame. Specs must still encode breaks and holes themselves.

**House look (ours, not theirs).** White well, 1px `--rule` hairline, no coloured left bar, no logo in the corner, no download pill in magenta. Title and subtitle live in HTML `figcaption` above the SVG (`.chart-title` matches section heading 1.25rem / 500; `.chart-subtitle` matches the byline). The plot fills the card: one house `plotWidth`, SVG `width: 100%`.

**Categorical bars** are horizontal, house `barStep` so 2 bars and 36 states share thickness, single-series navy only. No extra colour legend when the axis already names the categories.

**Series colour** is categorical position, never magnitude:

1. `--mark` navy  
2. `--mark-2` ochre (e.g. compiled vs linked)  
3. `--mark-3` slate  
4. `--mark-4` grey  

Single-series bars use navy only. Grid `--rule` at 50% opacity, quantitative axis only. Axis labels `--muted`. Zero line, when the scale includes zero, `--ink` at 1px. Break: dashed rule `#333333` plus a labelled band — already C1 practice. Unknown: `invalid: "break-paths"`; never plot as zero.

**Order.** States/UTs: alphabetical by official English name, or a documented geographic order — the default. When the slice’s citizen question is a rank question and the vintage supports it, the chart or list may sort by the published measure. Divisions: producer annex order. Never red–green. Test 8 remains the gate on the default.

**One idea.** If the chart needs a paragraph to explain two encodings, it is two charts.

**Screenshot test.** A crop of a chart should still show: title, unit, geography, a source byline, and visible holes. It should **not** look like a USAFacts chart (cream field, magenta rail, wordmark). Attribution is the citation card, not a corner logo.

## Citation chrome

Visible on the same view as the number:

- Summary: `series · reference period · released {date}`
- Open: producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, caveat
- Optional: `.analysis-byline` — “Analysis by Prism” (or house equivalent) in `--muted`, after the producer, never instead of the producer

Collapsed `<details>` is allowed. Empty chrome while the number shows is a failed render. Do not move this into a fly-out that leaves the view.

Caveat notes use the same panel language: hairline, `--card`, summary in `--muted`, no warning-orange “alert” styling (a break is not an emergency).

## States the UI must show

| Status | Surface |
|--------|---------|
| `value` | Tabular figure or mark |
| `unknown` / not published | Em dash or “Not published”, italic `--hole`; slot stays |
| `series_break` | Break encoding + one prose line |
| `not_comparable` | Not joined on the same line; named |
| Two official numbers | Two stats or two encodings; no pick-a-winner colour |

## Accessibility

WCAG 2.2 AA on text and on chart colour against `--card` and `--paper`. Do not communicate meaning by colour alone (sector is also a label; a break is also a dash and a sentence). Focus: 2px `--focus` outline, 2px offset. `lang="en"` until a template ships another language. Hit targets on `<summary>` at least 44px tall. Prefers-reduced-motion: no optional motion (there should be none yet).

## Interaction

Citizen pages are static. Allowed: in-page `<details>`, hash links, Vega-Lite hover and chart download from **already-bound** specs. Forbidden: request-time fetch, engagement SDK, A/B, heatmap, live filter that loads another vintage, “get notified.” Geography as a pre-rendered route or a client filter over observations from **this** vintage is a later, named piece of work — not a copy of their metro picker.

## Implementation

| Place | What changes |
|-------|----------------|
| `src/cms/src/lib/theme.ts` | Tokens. CSS custom properties and Vega house config. One source. |
| `src/cms/src/styles/desk.css` | Layout primitives and site chrome. Inherit tokens; no hex. |
| `src/cms/src/layouts/SiteShell.astro` | Apply the theme. Shared shell. No page-local palette. |
| `src/cms/src/lib/render-chart.ts` | Apply the theme’s Vega frame. Specs do not restyle. |
| `src/cms/templates/**/*.vl.json` | Encode breaks and holes. No new palettes. |
| `src/prism/template_bind.py` | No new layout blocks without updating this file |

Do not add Storybook, a token npm package, or a second CSS framework. Pages inherit the desk theme; they do not define one.

## Presentation pass

UI/UX Developer. Run on **preview** after chrome or charts change, before Trust. Gate: this file — [layout primitives](#layout-primitives) and [chart system](#chart-system). Not a fifth Content Editor writing pass. Not Trust. A new token or primitive is specified in this file first — do not invent it in a one-off template.

**Done when** the preview is the same house: desk tokens; type scale on headings, byline, figcaption, source-line; plots at `--desk`; `--card` wells filled (no leftover white); categorical bars at house `barStep`; titles in HTML matching H2 / byline. Fail mixed plot widths, dead wells, bars that fatten with category count, Vega titles at 14px vs H2 at 1.25rem, magenta/cream/USAFacts costume. Tone is quiet, corporate, professional, minimal, modern — not prettier-than-the-record, not a scorecard.

Checklist: [ui-ux-developer.md](personas/ui-ux-developer.md).

## Out of scope for this system

Pipeline schema, citation *content*, chart *meaning*, voice and copy ([editorial-guidelines.md](editorial-guidelines.md)), Trust ship/block, a public wordmark beyond a text lockup, dark mode, a mobile app.

## Next

Site chrome and C1 at `/prices/retail-prices` (`dv-20260916-234e263c8588`). Charter ships this vintage. Do not start C2 from this file.
