# Design system v2

Superseded 2026-09-21 by [design-system.md](../design-system.md) (**v3**). v2 was the welcome ruling — one well on the first screen, `--hole` at AA, fit floors — done with a single flat lift token, no display serif, and a two-colour-family palette that the principal read as quiet and austere. v3 keeps every fit and contrast floor from this file and rebuilds the house around them. Do not implement from this file.

UI/UX Developer. Visual contract for citizen pages (**v2**). Persona: [ui-ux-developer.md](../personas/ui-ux-developer.md). How the page **reads** is [editorial-guidelines.md](../editorial-guidelines.md) (Content Editor) — this file implements that as type, colour, layout, and chart chrome. UI/UX Developer implements this file and runs the presentation pass against it. Routes, titles, SEO, and preview vs published HTTP: [web-design.md](../web-design.md) (Front-end Architect). Integrity stays in [data-contracts.md](../data-contracts.md) and [architectural-blueprint.md](../architectural-blueprint.md).

Product role, answer-page shape, and newsroom forbids live in the editorial guidelines. Stack (Astro SSG, Vega-Lite) lives in [repo-conventions.md](../repo-conventions.md). Current work lives under [Next](#next).

v1 (quiet desk): [design-system-v1.md](design-system-v1.md). Tone: [design-philosophy.md](../design-philosophy.md). Direction: [ui-ux-feedback.md](ui-ux-feedback.md).

```text
version:        v2
tone:           modern, welcoming, civic publisher, generous
idea:           official record, built for a person — answer first, archive on request
look:           house tokens, generous craft; not USAFacts magenta, cream, Aeonik, or wordmark
tokens:         CSS custom properties on :root — not in the vintage
fit:            every rule below must hold at 360px and at 1440px
```

## Decision

One house for the portrait in [vision.md](../vision.md). A citizen should recognise it on every slice.

This system does not restate voice, scan path, or newsroom forbids. Bound ranks, a house-highlighted fact-lede, fast-facts / featured-slice rails, and an analysis byline use **our** tokens (`--mark`, `--paper`, `--card`).

**A rule that cannot be measured is not in this file.** Each rule below carries the measurement that fails it. Floors we keep from v1: chart type under 12px, bleeding stats, `--hole` under 4.5:1, producer off the first screen.

Do not retune the pipeline for layout. Content Editor names blocks; UI/UX specifies and applies the styles.

## Costume we do not copy

- Magenta bar, Aeonik, pink/magenta sentence highlight (`span.answer`)
- Purple illustrated heroes; a news-style hottest-topics carousel (scoops, engagement)
- Newsletter, social kits, "get notified", video desk, search box, chat widget
- Cream plot, brand-colour edge rule, magenta download pill, chart-corner logo

A page that would pass for USAFacts with the wordmark swapped has failed this system.

## House chrome

| Class | Tokens | Job |
|-------|--------|-----|
| `.fact-lede` | `--card` on `--paper`; `--radius`; `--lift`; padding `--space-6`; 4px `--mark` top rule; `--ink`; width `--desk` | Landing on the bound answer (number, unit, place, year — then definition). Full well. Not a magenta sentence. Not a slogan. |
| `.fast-facts` | `--card`, `--radius`, `--lift`; fact 1.5rem / 500 / `--ink`; `--muted` labels | Publisher front: slot-bound one-liners. Never byline grey. Not a ticker of unnamed numbers. |
| `.hottest-rail` | `--paper`, `--card`, `--radius`, `--mark` links | Featured citizen questions / slices. Not scoops, not “hottest topics,” no “get notified.” |
| `.stat` | `--card`, `--radius`, `--lift`; padding `--space-5` | Equal-weight bound figures. No winner colour. |
| `.analysis-byline` | `--muted` | Optional "Analysis by Prism" next to the producer. Never instead of the producer. |
| `.cite-strip` | same well as the numbers; no extra card chrome; producer `--ink`; rest `--muted` | Source line **next to the number**. Open state is the full card. Not a codebook dump. |

## Visual encodings

Encode the editorial guidelines as chrome. Not a second reading contract.

1. **No performance colour.** Colour and weight never mean better or worse. Alphabetical / documented geographic order by default. Measure-sort only on a rank question.
2. **The answer is the landing.** Display type is for bound figures, not slogans. On any page that quotes a figure, the largest non-heading text on the first screen is a bound observation.
3. **Cite in the same view.** Producer next to the number. A tooltip is not enough. A fly-out that leaves the view is not enough.
4. **Holes stay holes.** Never smaller, lighter, or lower-contrast than the sentence they sit in.
5. **Generous craft, quiet meaning.** Radius, lift, and space make it a product. They do not argue. No gradient. No illustration the vintage did not earn.
6. **Legible or scrollable, never shrunk.** Nothing below 12px effective size. At 1440px the first chart fills the well with **no horizontal scroll**. Below 0.92 scale, scroll.

## Tokens

CSS custom properties on `:root`. Not in the vintage schema.

### Colour

Warm stone paper, ink type, navy as the only accent. Navy is how C1 already plots (`#1F4E79`). Institutional, not performance colour.

Contrast is quoted against `--paper`. A token that passes on paper passes on `--card`.

| Token | Hex | Use | On `--paper` | Needs |
|-------|-----|-----|--------------|-------|
| `--paper` | `#F7F5F1` | Page ground | — | — |
| `--card` | `#FFFFFF` | Landing, stats, charts, facts | — | — |
| `--ink` | `#1A1A1A` | Body, headings, figures, facts, producer | 16.0 | 4.5 |
| `--muted` | `#5A5A5A` | Byline, labels, axis, cite rest | 6.4 | 4.5 |
| `--hole` | `#6B6B6B` | Not published | 5.0 | 4.5 |
| `--mark` | `#1F4E79` | Links, focus, series 1, header rule, lede rule | 8.0 | 4.5 |
| `--mark-soft` | `#E8EEF4` | Landing wash behind `.fact-lede` only (navy at ~8% on card) | — | decorative |
| `--mark-2` | `#7A542E` | Chart series 2 | 6.2 | 3.0 |
| `--mark-3` | `#4A6670` | Chart series 3 (slate; not "good") | 5.7 | 3.0 |
| `--mark-4` | `#5C5C5C` | Chart series 4 | 6.2 | 3.0 |
| `--break` | `#333333` | Series-break rule | 11.6 | 3.0 |
| `--rule-strong` | `#8C857A` | Meaning-carrying lines | 3.4 | 3.0 |
| `--rule` | `#D6D2CA` | Hairlines and chart grid | 1.3 | decorative |
| `--hole-band` | `#E3DFD8` | Hole-band fill | 1.2 | decorative |
| `--focus` | `#1F4E79` | Focus ring | 8.0 | 3.0 |

`--hole` stays at or above 4.5:1. Do not lighten it to look calmer.

**A decorative fill is allowed; a decorative meaning is not.** `--rule`, `--hole-band`, and `--mark-soft` do not carry meaning alone. A hole band needs a `--rule-strong` edge **and** a label. `--mark-soft` is a landing field, not a verdict.

**Forbidden as tokens:** magenta / hot pink; wine as a USAFacts-style edge; red–green; gold/saffron; dashboard blues; the tricolour as brand or scale; party colours; ministry campaign palettes; saffron/green as up/down.

Links are `--mark` plus underline. Visited is the same.

### Type

Sans throughout. Civic publisher; not a literary serif, not a fashion grotesque.

| Role | Face | Notes |
|------|------|--------|
| UI, body, headings, figures | **IBM Plex Sans** | 400 / 500 / 600. Tabular figures on every observation. |
| Identifiers | **IBM Plex Mono** | `vintage_id`, `series_id`, geography codes — not body. |
| Later scripts | IBM Plex Sans Devanagari | When a template ships a non-English official name. English first. |

Self-host under `src/cms/public/fonts/`. No font CDN at render or request time. Fallback: `"IBM Plex Sans", "Source Sans 3", "Segoe UI", system-ui, sans-serif`.

Do not use Aeonik. Do not use a serif for body.

**Scale** (root 16px)

| Style | Size | Weight | Line | Tracking |
|-------|------|--------|------|----------|
| Sleeve | 0.75rem | 500 | 1.3 | 0.08em; uppercase |
| Display figure | `clamp(2rem, 16cqi, 3.25rem)` | 600 | 1.05 | −0.03em; tabular-nums |
| H1 (question) | `clamp(2rem, 4.5vw, 2.75rem)` | 500 | 1.15 | −0.02em |
| H2 (section) | 1.375rem | 500 | 1.3 | 0 |
| Fast-fact | 1.5rem | 500 | 1.3 | 0; `--ink` |
| Body | 1.125rem | 400 | 1.6 | 0 |
| Byline / source | 0.875rem | 400 | 1.45 | 0 |
| Label / dt | 0.75rem | 500 | 1.3 | 0.04em; uppercase; `--muted` |
| Caption | 0.875rem | 400 | 1.4 | 0 |
| Hole (inline) | inherits its sentence | 400 italic | inherits | `--hole` |

**12px is the floor.** Nothing a citizen reads, including SVG text after scale.

**A hole inherits its sentence.** Italic and colour are the encoding; smaller is not.

**The display figure is sized by its cell.** `cqi` is the `.stat` inline size. Short rates may reach 3.25rem; ten-digit counts shrink before they bleed. See [Fit](#fit).

H1 is a citizen question, not a 72px slogan. The bound figure is the climax. Home’s welcome is the fact grid at 1.5rem.

### Space, radius, lift

| Token | Value | Use |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 px | Stacking only these steps |
| `--desk` | 68rem | Landing well: hero, stats, charts, header, footer, home facts. Shared left **and** right edge. |
| `--measure` | 40rem | Method prose only (`.how-measured`). Not the hero. Not a section that holds a chart. |
| `--radius` | 8px | Cards, lede, stats, charts, fact tiles. Not pills. Not 0. |
| `--lift` | `0 1px 3px rgb(26 26 26 / 0.08)` | Landing cards only (lede, stats, fast-facts, chart well). One token. No glow, no stacked marketing shadow. |
| `--hair` | 1px | Borders |
| `--header-rule` | 4px `--mark` | Top of the viewport |

No gradient. `--lift` is product elevation, not decoration that argues. `prefers-reduced-motion` does not remove lift (it is static).

## Fit

The desk holds ten-digit official counts. Layout that only works for `4.82` is not a layout.

**One width on the composed well.** Lede, stats, cite, and charts in the same view share `--desk`. Content boxes match at 1440px (right edges within 1px). A section that contains a chart is the same well. `--measure` is method only.

Hero copy is short; it may run at `--desk`. Method at 68rem was **124 characters per line** — `.how-measured` stays at `--measure`. Do not fail the hero for exceeding 90 characters per line.

**Stat cells fit the widest figure the vintage can bind.**

```css
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: var(--space-5);
}
.stat { container-type: inline-size; min-width: 0; }
.stat-figure { font-size: clamp(2rem, 16cqi, 3.25rem); }
```

`16rem` stops cells packing too narrow; `min(100%, …)` stops overflow at 360px; `cqi` shrinks the figure before the card. The widest plausible bound string — ten digits plus four separators, about 6.7em — must fit at every cell width the grid can produce, including the ungrouped form.

**Grouping is not decided here.** One convention at bind (Front-end ruling R8). This file guarantees the string **fits**.

**Breakpoints.** One: `48rem`. Below it, a single column. Do not add a second breakpoint to solve a fit problem that `clamp`, `min()`, or a container query solves.

**Every rule is checked at 360px and 1440px.**

## Layout primitives

Content Editor may name only these blocks (`LAYOUT_BLOCKS` in `src/prism/template_bind.py`). Do not invent a second set in YAML.

| Token | Element | Job |
|-------|---------|-----|
| `hero` | `<header class="hero">` | First screen: sleeve, question, byline, fact-lede, stat row, cite next to the numbers, first chart. One `--desk` column. |
| `stat-row` | `<div class="stat-row">` | 2–4 bound figures, equal weight |
| `section` | `<section class="portrait-section">` | One idea; heading; copy; optional stats; one chart. If it holds a chart, the section is `--desk`. |
| `how-this-is-measured` | `<section class="how-measured">` | Method after the record. Prose at `--measure`. Quieter than the answer. |
| compact source byline | `<details class="citation-card source-byline">` | Summary visible; full card on open |
| caveat note | `<details class="caveat-note">` | Same rule |

**Section headings are `<h2>`.** Element and scale agree. Fix at bind, not with a CSS override.

### Site chrome

Same tokens. Not a full-bleed marketing bar. Not a USAFacts wordmark. Routes: [web-design.md](../web-design.md).

| Region | Class | Job |
|--------|-------|-----|
| Skip link | `.skip-link` | `--card` fill, `--mark` type; 44px; first focusable |
| Header rule | `body` border-top | `--header-rule` |
| Frame | `.site-frame` | `--desk`; padding-inline `--space-6`; padding-block `--space-6` / `--space-8` |
| Header | `.site-header` | Lockup + sleeve nav; gap `--space-5` |
| Lockup | `a.site-lockup` | 1rem / 500 / 0.04em uppercase; `--ink`; no underline; links to `/` |
| Sleeve nav | `.sleeve-nav a` | `--mark` + underline; 44px; `aria-current` is weight 600 |
| Breadcrumb | `.breadcrumb` | 0.875rem; `--muted`; current `--ink`. Wrap; do not cap at `--measure` while H1 is `--desk`. |
| Main | `main#main` | `--desk` via `.site-frame` |
| Footer | `.site-footer` | Hairline; byline size; 44px hits; no SDK |
| Fast facts (home) | `.fast-facts` | Grid `repeat(auto-fit, minmax(min(100%, 20rem), 1fr))`; gap `--space-5`. Publisher front. |
| Hottest rail | `.hottest-rail` | Featured questions |
| Sleeve index | `.sleeve-index` | Body type; `--mark` + underline; 44px. Not a tile grid. |
| Preview banner | `.preview-banner` | Serve-only (R5). `--card`, hairline, `vintage_id` in Mono 0.75rem. No control. Never in the citizen tree. |

No search, subscribe, or social row. No engagement SDK.

**Publisher front (home).** H1 is the purpose sentence at H1 scale. The designed moment is the fact grid — 1.5rem `--ink` one-liners, side by side at `--desk`. Then the featured-question rail. Not a mission whisper over grey paragraphs. Not a display-size slogan.

**First screen (every slice).** Editorial scan path as one composed well.

1. Sleeve (topic family, not a news kicker).
2. Citizen question as H1 (geography in the words).
3. Byline: release date (`Asia/Kolkata`), next named release.
4. `.fact-lede` landing at `--desk`.
5. Stat row, or a `.fast-facts` rail of 3–4 bound one-liners.
6. Cite strip next to those numbers — producer `--ink`, before the first chart.
7. First chart, filling the same well.

Hottest rail closes the hero; never above the cite. Methodology is not on screen 1. Left-aligned. Do not centre the question.

## Chart system

Vega-Lite in git; SVG at render. `src/cms/src/lib/render-chart.ts` applies the frame. Specs encode breaks and holes.

**House look.** `--card` well, `--radius`, `--lift`, 1px `--rule` hairline. No coloured left bar, no corner logo, no magenta download pill. Title and subtitle in HTML `figcaption` (`.chart-title` = H2; `.chart-subtitle` = byline). Plot field is `--card`, not cream.

**Legibility floor.** Authored at one house `plotWidth`. SVG `width: 100%` scales type. Do not roll the 12px floor back to make a well look filled.

- `fitWidth` is the well **content** width at `--desk`: `68rem` minus 2× frame padding-inline (`--space-6`) minus 2× figure padding (`--space-5`) = **976px**. Recalculate if those paddings change. At desk width the SVG is 1:1.
- Scale down to **0.92** and no further. Then `figure.chart` scrolls.
- **At 1440px the first-screen chart does not scroll.**
- Every chart on a page: same `plotWidth`.
- Category height is `n × barStep`. Do not compress; scroll.

**Bars.** Horizontal; house `barStep`; single-series navy only. No extra legend when the axis names the categories.

**Numbers agree.** Axis, bar labels, lede, and stat cell use one format from bind. `render-chart.ts` does not invent `.2~f`.

**Series colour** is categorical position, never magnitude: `--mark`, `--mark-2`, `--mark-3`, `--mark-4`. Grid `--rule` at 50% on the quantitative axis. Domain and meaning-carrying lines: `--rule-strong` or `--ink`. Axis labels `--muted`. Zero line `--ink` 1px. Break: dashed `--break` plus labelled `--hole-band`. Unknown: `invalid: "break-paths"`; never plot as zero.

**Order.** States/UTs alphabetical by official English name, or documented geographic order. Measure-sort only on a rank question. Divisions: producer annex order. Never red–green. Test 8 gates the default.

**One idea.** Two encodings → two charts. A chart that only repeats the stat row is not evidence.

**Screenshot test.** Crop still shows title, unit, geography, source, holes, at readable size. It does not look like a USAFacts chart (cream, magenta rail, wordmark). Attribution is the citation card, not a corner logo.

## Citation chrome

Checkability is proximity, not a field dump.

- Producer within the first **600px** of `main` at 1440×900.
- `<details class="citation-card source-byline cite-strip">` after lede and stats, **before** the first chart, same `--desk` width.
- Summary: producer `--ink`, then `series · reference period · released {date}` `--muted`. All four, every slice. Missing field fails the render.
- Open: producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, caveat. Same cite as the bottom `.source-stack`, earlier.
- Optional `.analysis-byline` after the producer, never instead.

Collapsed `<details>` is the default. Empty chrome while the number shows fails the render. No fly-out that leaves the view (R7).

Caveats: same panel language; no warning-orange.

## States the UI must show

| Status | Surface |
|--------|---------|
| `value` | Tabular figure or mark |
| `unknown` / not published | Em dash or "Not published", italic `--hole`, sentence size; slot stays |
| `series_break` | Break encoding + one prose line |
| `not_comparable` | Not joined on the same line; named |
| Two official numbers | Two stats or two encodings; no winner colour |

## Accessibility

WCAG 2.2 AA, against the [colour table](#colour).

- Text 4.5:1 on `--paper` and `--card`. Meaningful graphics 3:1.
- Meaning is never colour alone.
- Focus: 2px `--focus`, 2px offset.
- Heading order does not skip. H1 → H2 → H3.
- `lang="en"` until a template ships another language.
- Hits on `<summary>` and nav ≥ 44px.
- No text below 12px effective size.
- `prefers-reduced-motion`: no optional motion.

## Interaction

Static pages. Allowed: `<details>`, hash links, chart scroll below 0.92, Vega hover and download from **already-bound** specs. Forbidden: request-time fetch, engagement SDK, A/B, heatmap, live filter that loads another vintage, “get notified.” Geography routes or a client filter over **this** vintage are later named work — not their metro picker.

## Implementation

| Place | What changes |
|-------|----------------|
| `src/cms/src/lib/theme.ts` | Tokens (`--paper`, `--radius`, `--lift`, `--mark-soft`, type scale, `fitWidth` 976), Vega house config. One source. |
| `src/cms/src/styles/desk.css` | Publisher layout. Inherit tokens; no hex. |
| `src/cms/src/layouts/SiteShell.astro` | Apply the theme. No page-local palette. |
| `src/cms/src/lib/render-chart.ts` | Vega frame + legibility floor. Specs do not restyle. |
| `src/cms/templates/**/*.vl.json` | Breaks and holes. No new palettes. |
| `src/prism/template_bind.py` | Blocks, heading level, cite strip. No new block without this file. |
| `src/prism/cms_site.py` | Catalog fields the chrome reads. |

No Storybook, no token npm package, no second CSS framework.

## Presentation pass

Run on **preview** before Trust, on **every template that reached Content Editor Proof**. Skip only when the same template renders the same page at the same vintage.

Appeal means **modern, welcoming, civic publisher, generous** — same house. Generous is space, scale, and product cards. It is not their kit. Not a scorecard. Not USAFacts magenta. Not unfinished.

Measure at 360px and 1440px. Do not eyeball.

- [ ] **Tokens.** One house. `--radius` 8px and `--lift` on landing cards. No hex in `desk.css`. No magenta / cream / Aeonik / costume.
- [ ] **Type.** Scale as tabled. Fast-facts 1.5rem / 500 / `--ink`. Chart titles in HTML, not Vega. Heading element and size agree.
- [ ] **One well.** Lede, stats, cite, first chart: `--desk`; widths match within 1px at 1440px. Hero children not capped at `--measure`.
- [ ] **Method measure.** `.how-measured` prose at `--measure`. *Fails on:* a method paragraph over 90 characters per line at 1440px.
- [ ] **Landing.** `.fact-lede` is `--card` + `--mark-soft` wash, `--desk`, padding-block ≥ `--space-6` (32px), 4px `--mark` top rule, `--radius`, `--lift`, `--ink`.
- [ ] **Stat fit.** No `.stat-figure` wider than its cell at 360, 480, 768, 1024, or 1440px.
- [ ] **Chart legibility.** No SVG text under 12px effective (intrinsic × scale) at those widths.
- [ ] **Desk chart, no scroll.** First-screen `figure.chart` has no horizontal scrollbar at 1440px.
- [ ] **One plot width.** No mixed intrinsic SVG widths on one page.
- [ ] **Chart wells.** Plot fills the well at desk width; `--radius` on the figure. *Fails on:* label padding wider than the longest label.
- [ ] **Number agreement.** One grouping inside a chart and between lede and stat.
- [ ] **Bars.** Horizontal; house `barStep`.
- [ ] **Cite.** Producer within 600px of `main` at 1440×900, `--ink`, before the first chart; summary has all four fields.
- [ ] **Holes.** Not smaller or lower-contrast than their sentence.
- [ ] **Contrast.** Text ≥ 4.5:1; meaningful graphics ≥ 3:1 on the actual ground.
- [ ] **Screenshot test.** Crop shows title, unit, geography, source, holes at readable size; does not look like a USAFacts chart.

Fail the pass if any box is open. Content Editor Proof names form-factor breaks; it does not restyle. Trust gets cites, dates, holes, spin — not taste.

A new token or primitive is specified here first.

Checklist also on the persona: [ui-ux-developer.md](../personas/ui-ux-developer.md).

## Out of scope

Pipeline schema, citation *content*, chart *meaning*, voice and copy ([editorial-guidelines.md](../editorial-guidelines.md)), routes and slugs ([web-design.md](../web-design.md)), Trust ship/block, a public wordmark beyond a text lockup, dark mode, a mobile app, number-grouping (R8). USAFacts costume. Pointer flips.

## Next

Preview at `localhost:4321` still carries the v1 layout until [ui-ux-change-plan.md](ui-ux-change-plan.md) **Phase E** lands this file. Do not move `data/pointers/citizen`.

C1 `/prices/retail-prices` is on the citizen pointer; C2 `/people/population` and C3 `/money/union` are preview-only. Charter owns publish.
