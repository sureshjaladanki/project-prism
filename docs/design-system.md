# Design system

UI/UX Developer. Visual contract for citizen pages. Persona: [ui-ux-developer.md](personas/ui-ux-developer.md). How the page **reads** is [editorial-guidelines.md](editorial-guidelines.md) (Content Editor) — this file implements that as type, colour, layout, and chart chrome. UI/UX Developer implements this file and runs the presentation pass against it. Routes, titles, SEO, and preview vs published HTTP: [web-design.md](web-design.md) (Front-end Architect). Integrity stays in [data-contracts.md](data-contracts.md) and [architectural-blueprint.md](architectural-blueprint.md). C1 application: [presentation-charter.md](archive/presentation-charter.md).

Product role, answer-page shape, and newsroom forbids live in the editorial guidelines. Stack (Astro SSG, Vega-Lite) lives in [repo-conventions.md](repo-conventions.md). Current work lives under [Next](#next).

```text
tone:           corporate, professional, minimal, modern
look:           house tokens; not USAFacts magenta, cream, Aeonik, or wordmark
tokens:         CSS custom properties on :root — not in the vintage
fit:            every rule below must hold at 360px and at 1440px
```

## Decision

One quiet visual language for the portrait in [vision.md](vision.md). A citizen should recognise the same house on every slice: large cited numbers, calm type, charts that do not argue.

This system does not restate voice, scan path, or newsroom forbids. Those live in the editorial guidelines. [USAFacts](https://usafacts.org/) is not a look to reproduce: no brand marks, magenta, cream plot, Aeonik, or chart-corner logo. Bound ranks, a house-highlighted fact-lede, fast-facts / featured-slice rails, and an analysis byline use **our** tokens (`--mark`, `--paper`, `--card`).

**A rule that cannot be measured is not in this file.** Earlier versions said "cite chrome in the same view", "the plot fills the card", and "WCAG AA" without a number, and the live desk passed every box while putting the producer below the fold, rendering chart labels at 3.2px on a phone, and colouring holes at 3.09:1. Each rule below carries the measurement that fails it. If you cannot state how a box fails, it is a preference, not a contract.

Do not retune the pipeline for layout. Content Editor names blocks; UI/UX specifies and applies the styles.

## Look we do not copy

Reading craft is in the editorial guidelines. This system forbids the costume:

- Magenta bar, Aeonik, pink/magenta sentence highlight (`span.answer`)
- Purple illustrated heroes; a news-style hottest-topics carousel (scoops, engagement)
- Newsletter, social kits, "get notified", video desk, search box, chat widget
- Cream plot, brand-colour edge rule, magenta download pill, chart-corner logo

A page that would pass for USAFacts with the wordmark swapped has failed this system.

## House chrome we do use

Same desk tokens. Not a second palette.

| Class | Tokens | Job |
|-------|--------|-----|
| `.fact-lede` | `--card` on `--paper`; 3px `--mark` rule; `--ink` type | Optional highlight of the bound fact-lede (number, unit, place, year — then definition). Not magenta. Not a slogan box. |
| `.fast-facts` | `--card`, `--ink` fact, `--muted` labels | Compact slot-bound one-line facts. The fact is body type in `--ink`, never byline grey — a fact desk does not whisper the fact. Not a ticker of unnamed numbers. |
| `.hottest-rail` | `--paper`, `--card`, `--mark` links | Featured citizen questions / slices. Sleeve-appropriate. No scoops, no "get notified." |
| `.analysis-byline` | `--muted` on `--card` | Optional "Analysis by Prism" next to the producer cite. Never instead of the producer. Not a second wordmark. |
| `.cite-strip` | `--card` on `--paper`; hairline `--rule`; `--muted` summary | First-screen citation chrome. A `<details>` whose summary is the producer line and whose open state is the full card. See [Citation chrome](#citation-chrome). |

## Visual encodings

These encode the editorial guidelines as chrome. Do not treat them as a second reading contract.

1. **No performance colour.** Colour and weight never mean better or worse. Order is alphabetical / documented geographic by default. Measure-sort is allowed only when the citizen question is a rank question.
2. **The number is the hero.** Display type is for bound figures, not for slogans. On any page that quotes a figure, the largest non-heading text on the first screen is a bound observation.
3. **Cite chrome in the same view.** Producer, series, reference period, release date, geography vintage, data vintage, caveat. A tooltip is not enough. Measured in [Citation chrome](#citation-chrome), not left to judgement.
4. **Holes stay holes.** `unknown`, `not_comparable`, and `series_break` are encodings, not styling problems to smooth away. A hole is never smaller, lighter, or lower-contrast than the sentence it sits in.
5. **Quiet chrome.** Hairlines, whitespace, one accent. No gradient, shadow, or illustration that the vintage did not earn.
6. **Legible or scrollable, never shrunk.** No text on a citizen page renders below 12px effective size at any viewport. A chart that cannot fit is scrolled, not scaled into a smear.

## Tokens

Implement as CSS custom properties on `:root` in the citizen layout. Do not put them in the vintage schema.

### Colour

Warm stone paper, ink type, navy as the only accent. Navy is already how C1 charts plot a series (`#1F4E79`). It is institutional, not a performance colour.

Contrast is quoted against `--paper`, which is the harder ground for dark marks. A token that passes on paper passes on `--card`.

| Token | Hex | Use | On `--paper` | Needs |
|-------|-----|-----|--------------|-------|
| `--paper` | `#F4F2EE` | Page ground | — | — |
| `--card` | `#FFFFFF` | Stat cell, chart well, citation panel | — | — |
| `--ink` | `#1A1A1A` | Body, headings, figures | 15.6 | 4.5 |
| `--muted` | `#5A5A5A` | Byline, labels, axis labels | 6.2 | 4.5 |
| `--hole` | `#6B6B6B` | Unknown / not published copy | 4.8 | 4.5 |
| `--mark` | `#1F4E79` | Links, focus, chart series 1, header rule | 7.7 | 4.5 |
| `--mark-2` | `#7A542E` | Chart series 2 only (categorical) | 6.0 | 3.0 |
| `--mark-3` | `#4A6670` | Chart series 3 only (slate; not "good") | 5.5 | 3.0 |
| `--mark-4` | `#5C5C5C` | Chart series 4 / residual | 6.0 | 3.0 |
| `--break` | `#333333` | Series-break rule | 11.3 | 3.0 |
| `--rule-strong` | `#8C857A` | Any line that carries meaning: chart axis domain, hole-band edge, a boundary a reader must see | 3.3 | 3.0 |
| `--rule` | `#D6D2CA` | Decorative hairlines and chart grid only | 1.3 | decorative |
| `--hole-band` | `#E3DFD8` | Hole-band fill | 1.2 | decorative; see below |
| `--focus` | `#1F4E79` | Keyboard focus ring | 7.7 | 3.0 |

**Contrast is a token property, not a later check.** `--hole` was `#8A8A8A` and measured **3.09:1** on paper — the honest part of the page was the least legible part of the page. It is now `#6B6B6B` at 4.8.

**A decorative fill is allowed; a decorative meaning is not.** `--rule` and `--hole-band` are below 3:1 and stay there because neither carries the meaning on its own. A hole band is identified by a `--rule-strong` edge **and** a text label; a card hairline separates, it does not inform. The moment a line is the only thing telling a reader something, it is `--rule-strong` or darker. `--hole-band` was `#D9D9D9`, a cool grey in a warm house, and is now in the stone family.

**Forbidden as tokens:** magenta / hot pink; wine used as a USAFacts-style edge; red–green pairs; gold/saffron; saturated "dashboard" blues; the tricolour as brand or as a scale (it reads as the flag, or as a scorecard); party colours or ministry campaign palettes; saffron/green as up/down.

Links are `--mark` plus underline. Visited is the same (this is a record, not a web of explored lore).

### Type

Sans throughout. Corporate and modern; not a literary serif, not a fashion grotesque.

| Role | Face | Notes |
|------|------|--------|
| UI, body, headings, figures | **IBM Plex Sans** | Weights 400 / 500 / 600. Tabular figures on every observation. |
| Identifiers | **IBM Plex Mono** | `vintage_id`, `series_id`, geography codes — not body copy. |
| Later scripts | IBM Plex Sans Devanagari | Pair when a template ships a non-English official name. English is first. |

Self-host under `src/cms/public/fonts/`. Do not hotlink a font CDN at render or at request time. Fallback: `"IBM Plex Sans", "Source Sans 3", "Segoe UI", system-ui, sans-serif`.

Do not use Aeonik (theirs, proprietary). Do not use a serif for body — it reads as a journal, not a desk.

**Scale** (root 16px)

| Style | Size | Weight | Line | Tracking |
|-------|------|--------|------|----------|
| Sleeve | 0.75rem | 500 | 1.3 | 0.08em; uppercase |
| Display figure | `clamp(1.75rem, 14.5cqi, 2.75rem)` | 600 | 1.05 | −0.03em; `font-variant-numeric: tabular-nums` |
| H1 (citizen question) | `clamp(1.75rem, 4vw, 2.25rem)` | 500 | 1.2 | −0.02em |
| H2 (section) | 1.25rem | 500 | 1.3 | 0 |
| Body | 1.0625rem | 400 | 1.55 | 0 |
| Byline / source summary | 0.875rem | 400 | 1.4 | 0 |
| Label / dt | 0.75rem | 500 | 1.3 | 0.04em; uppercase; `--muted` |
| Caption | 0.8125rem | 400 | 1.4 | 0 |
| Hole (inline) | inherits its sentence | 400 italic | inherits | 0; colour `--hole` |

**12px is the floor.** Nothing a citizen reads renders smaller than 0.75rem, including text inside an SVG after any scaling. See [Chart system](#chart-system).

**A hole inherits its sentence.** `.observation-missing` is italic `--hole` at the size of the surrounding text. It was 0.8125rem italic inside 1.0625rem body, which shrank and faded the exact words that keep the page honest. Italic and colour are the encoding; smaller is not.

**The display figure is sized by its cell, not by the viewport.** `cqi` is the inline size of the `.stat` container. See [Fit](#fit).

H1 is a question, not a billboard. The bound figure is the display size.

### Space, line, radius

| Token | Value | Use |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 px | Stacking only these steps |
| `--measure` | 40rem | **Running prose, fact-lede, byline, source-line, one-liners.** Applied, not decorative |
| `--desk` | 68rem | Page frame: stat rows, chart wells, citation cards, header, footer |
| `--radius` | 0 | No rounded marketing cards |
| `--hair` | 1px | Borders |
| `--header-rule` | 3px `--mark` | Top of the viewport only |

No box-shadow. No gradient. Elevation is a hairline on `--card` against `--paper`.

## Fit

The desk holds ten-digit official counts. Layout that only works for `4.82` is not a layout.

**Prose runs at `--measure`, evidence runs at `--desk`.** Running paragraphs, the fact-lede, the byline, the source-line, and fast-facts one-liners cap at 40rem (about 70 characters at body size). Stat rows, chart wells, citation cards, header, and footer keep the full 68rem. Prose at 68rem measured **124 characters per line** on the live desk; that is a reading failure, not a house style. `--measure` already existed and was marked unused. It is now applied.

**Stat cells fit the widest figure the vintage can bind.** Two rules together, both required:

```css
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: var(--space-4);
}
.stat { container-type: inline-size; min-width: 0; }
.stat-figure { font-size: clamp(1.75rem, 14.5cqi, 2.75rem); }
```

`minmax(9.5rem, 1fr)` at a fixed 2.75rem could not hold a ten-digit count: `1210854977` measured 251px inside a 192px cell at a 768px viewport — a 58px bleed into the neighbouring card, on every viewport from about 368px to 929px. `16rem` stops the row from packing cells too narrow; `min(100%, …)` stops the row from overflowing a 360px phone; `14.5cqi` sizes the figure from its own cell so the figure shrinks before the card does. The clamp is set so the widest plausible bound string — ten digits plus four separators, about 6.7em — fits at every cell width the grid can produce.

**Grouping is not decided here.** Whether a figure is written `1,210,854,977` or `1,21,08,54,977` or ungrouped is one convention chosen once and applied at bind, so the lede, the stat cell, the chart label, and the `meta description` are the same string (Front-end ruling R8; Content Editor and bind own the choice). This file guarantees that whichever string arrives **fits**, including the ungrouped form.

**Breakpoints.** One: `48rem`. Below it the desk is a single column and the stat row packs to whatever `auto-fit` allows. Do not add a second breakpoint to solve a fit problem that `clamp`, `min()`, or a container query solves.

**Every rule in this file is checked at 360px and 1440px.** A box that passes at one width and not the other is a failed box.

## Layout primitives

Content Editor may name only these blocks (already in `LAYOUT_BLOCKS` in `src/prism/template_bind.py`). Do not invent a second set of layout tokens in YAML.

| Token | Element | Job |
|-------|---------|-----|
| `hero` | `<header class="hero">` | First screen: sleeve, question, byline, fact-lede that answers the H1, stat row, **cite strip**, first chart, source-line |
| `stat-row` | `<div class="stat-row">` | 2–4 bound figures, equal weight, no winner colour |
| `section` | `<section class="portrait-section">` | One idea; heading; copy; optional stats; one chart; cites |
| `how-this-is-measured` | `<section class="how-measured">` | Method after the record |
| compact source byline | `<details class="citation-card source-byline">` | Summary line visible; full card on open |
| caveat note | `<details class="caveat-note">` | Same rule |

**Section headings are `<h2>`.** The live slices emit `<h3>` for section headings and CSS restyles them to the H2 size, so the page looks like a hierarchy it does not have and a screen-reader user hears a level skipped from H1. The element and the scale must agree. Fix at bind, not with a CSS override.

**Site chrome** (UI/UX Developer, not Content Editor copy). Same tokens. Not a second palette, not a full-bleed marketing bar, not a USAFacts wordmark. Routes and labels: [web-design.md](web-design.md).

| Region | Class | Tokens | Job |
|--------|-------|--------|-----|
| Skip link | `.skip-link` | `--card` fill, `--mark` type, `--hair` `--rule`; 44px hit | First focusable; off-screen until `:focus-visible` |
| Header rule | `body` border-top | `--header-rule` `--mark` | Top of the viewport only |
| Frame | `.site-frame` | `--desk` column; `--space-5` / `--space-8` padding | Header, `main`, footer share it |
| Header | `.site-header` | flex wrap; gap `--space-4` | Lockup + sleeve nav |
| Lockup | `a.site-lockup` | 0.875rem / 500 / 0.04em uppercase; `--ink`; no underline | Links to `/`. Wordmark, not a sleeve link |
| Sleeve nav | `.sleeve-nav a` | `--mark` + underline; min-height 44px | Five sleeves. `aria-current` is weight 600, not a second colour |
| Breadcrumb | `.breadcrumb` | byline 0.875rem; `--muted`; current `--ink`, capped at `--measure` | Hub and slice only. The current crumb repeats the H1 verbatim by IA contract; cap its width so it does not become a second headline |
| Main | `main#main` | `--desk` (via `.site-frame`) | Page type |
| Footer | `.site-footer` | hairline `--rule`; byline size; 44px hits | Sleeves + house. No SDK |
| Fast facts (home) | `.fast-facts` | `--card` cards, `--ink` fact, `--mark` link; grid `repeat(auto-fit, minmax(min(100%, 20rem), 1fr))` | One bound one-liner per catalog slice, side by side at desk width. Not three stacked paragraphs |
| Hottest rail | `.hottest-rail` | already above | Featured questions |
| Sleeve index | `.sleeve-index` | body type; `--mark` + underline; 44px hits | Hub links. Not a tile grid |
| Preview banner | `.preview-banner` | `--card` on `--paper`; `--hair` `--rule`; `vintage_id` in IBM Plex Mono 0.75rem | Serving-only injection (Front-end ruling R5). No link, no control, so the skip link stays the first focusable element. Never in the citizen tree |

No search, subscribe, or social row. No engagement SDK. Home H1 uses the same H1 scale as a citizen question — not display-figure size, not a billboard.

**Grid.** Stat rows, charts, and citation cards share `--desk`. Running prose shares `--measure`. Everything is left-aligned. Do not centre the question.

**First screen (every slice).** Implements the scan path in [editorial-guidelines.md](editorial-guidelines.md). Do not add magenta highlight, unnamed-number ticker, trending-news rail, or "get notified."

1. Sleeve (topic family, not a news kicker).
2. Citizen question as H1 (geography in the words, not a US-style dropdown until a bound geography route exists).
3. Byline: release date (`Asia/Kolkata`), next named release.
4. Fact-lede that answers the H1 (bound number, unit, place, year) then one sentence of definition — optional `.fact-lede` house highlight.
5. Stat row of the comparable published figures, or a `.fast-facts` rail of 3–4 bound one-liners.
6. **Cite strip** for the figures above it — collapsed, but present and above the first chart.
7. The first chart for those figures, then its source-line.

The hottest rail closes the hero; it never sits above the cite strip. "Methodology" is not on screen 1. Charter-outs stay in Methodology, not as a separate closing section.

## Chart system

Vega-Lite in git; SVG at render. `src/cms/src/lib/render-chart.ts` applies the frame. Specs must still encode breaks and holes themselves.

**House look (ours, not theirs).** White well, 1px `--rule` hairline, no coloured left bar, no logo in the corner, no download pill in magenta. Title and subtitle live in HTML `figcaption` above the SVG (`.chart-title` matches section heading 1.25rem / 500; `.chart-subtitle` matches the byline).

**Legibility floor — the rule this system was missing.** A chart is authored at one house `plotWidth` and rendered to SVG at build time. `width: 100%` on that SVG scales the whole drawing, type included. On the live desk a 1056px plot in a 278px phone well rendered its 12px axis labels at **3.2px**; at 1440px it rendered them at 11.5px. The old checklist box ("the plot fills the `--card`") passed while the chart was unreadable. Replace it:

- `fitWidth` equals the actual well content width at `--desk` — **1008px** (68rem frame − 2×`--space-5` frame padding − 2×`--space-4` figure padding). At desk width the SVG renders 1:1 and chart type is exactly the size the scale says.
- The SVG may scale **down to 0.92 and no further** (12px → 11px, the practical floor for axis labels). Below that width, `figure.chart` scrolls horizontally — `overflow-x: auto` is already on the well; it is currently dead because `max-width: 100%` never lets the SVG exceed its box.
- Scrolling a chart is honest: nothing is hidden, nothing is re-rendered, the type stays legible. Scaling to 3px is not.
- The fit pass runs until every chart on a page lands on the **same** `plotWidth`. Today one page carries 1047, 1050, 1056, 1057, 1058, 1061 and 1064 because the pass corrects once and the correction moves the axis labels. Iterate or clamp; mixed intrinsic widths mean mixed effective type sizes on one page.
- A chart that needs 36 categories at `barStep` needs 36 × `barStep` of height. Do not compress the step to make it fit a phone; scroll.

**Categorical bars** are horizontal, house `barStep` so 2 bars and 36 states share thickness, single-series navy only. No extra colour legend when the axis already names the categories.

**Numbers inside a chart match numbers outside it.** Bar value labels and axis labels use the **same** number format, and that format is the one bind applied to the figure in the lede and the stat cell. The live desk prints an axis of `200,000,000` beside a bar labelled `833748852` in the same drawing — one chart, two conventions. The format is one token; `render-chart.ts` does not invent `.2~f` for value labels.

**Series colour** is categorical position, never magnitude:

1. `--mark` navy
2. `--mark-2` ochre (e.g. compiled vs linked)
3. `--mark-3` slate
4. `--mark-4` grey

Single-series bars use navy only. Grid `--rule` at 50% opacity, quantitative axis only (decorative; the values are labelled). Axis domain and any hairline a reader must see use `--rule-strong` or `--ink`. Axis labels `--muted`. Zero line, when the scale includes zero, `--ink` at 1px. Break: dashed `--break` rule plus a labelled band in `--hole-band`. Unknown: `invalid: "break-paths"`; never plot as zero.

**Order.** States/UTs: alphabetical by official English name, or a documented geographic order — the default. When the slice's citizen question is a rank question and the vintage supports it, the chart or list may sort by the published measure. Divisions: producer annex order. Never red–green. Test 8 remains the gate on the default.

**One idea.** If the chart needs a paragraph to explain two encodings, it is two charts. A chart that plots exactly the figures already in the stat row directly above it is a second copy, not evidence — either it earns a dimension the stat row does not have, or the stat row is the chart.

**Screenshot test.** A crop of a chart should still show: title, unit, geography, a source byline, and visible holes, **at readable size**. It should not look like a USAFacts chart (cream field, magenta rail, wordmark). Attribution is the citation card, not a corner logo.

## Citation chrome

Visible on the same view as the number. "Same view" is measured, not judged:

- **The producer name appears within the first 600px of `main`** at 1440×900, so it is above the fold on a 1366×768 laptop. On the live desk the compact source-line sat at 729px and the full card at 4596px on a 5706px page — six screens below the figure it belonged to.
- The first screen carries a `<details class="citation-card source-byline cite-strip">` placed **after the stat row and before the first chart**. `.cite-strip` is the same card, in the hero, with the hero's margins — not a fifth panel style.
- Summary (always visible): `producer · series · reference period · released {date}`. All four, on every slice. C2's source-line omits the release date; a missing field is a failed render, not a shorter line.
- Open: producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, caveat.
- Optional: `.analysis-byline` — "Analysis by Prism" (or house equivalent) in `--muted`, after the producer, never instead of the producer.

Collapsed `<details>` is allowed and is the default. The full cards stay on the page in the bottom `.source-stack` — the strip is a second, earlier view of the same cite, not a replacement (Front-end ruling R7). Empty chrome while the number shows is a failed render. Do not move this into a fly-out that leaves the view.

Caveat notes use the same panel language: hairline, `--card`, summary in `--muted`, no warning-orange "alert" styling (a break is not an emergency).

## States the UI must show

| Status | Surface |
|--------|---------|
| `value` | Tabular figure or mark |
| `unknown` / not published | Em dash or "Not published", italic `--hole`, **at the size of its sentence**; slot stays |
| `series_break` | Break encoding + one prose line |
| `not_comparable` | Not joined on the same line; named |
| Two official numbers | Two stats or two encodings; no pick-a-winner colour |

## Accessibility

WCAG 2.2 AA, checked against the numbers in the [colour table](#colour), not asserted.

- Text contrast 4.5:1 against both `--paper` and `--card`. Meaningful graphics 3:1.
- Do not communicate meaning by colour alone (sector is also a label; a break is also a dash and a sentence).
- Focus: 2px `--focus` outline, 2px offset.
- Heading order does not skip a level. H1 question → H2 section → H3 sub.
- `lang="en"` until a template ships another language.
- Hit targets on `<summary>` and nav links at least 44px tall.
- No text below 12px effective size, including inside a scaled SVG.
- `prefers-reduced-motion`: no optional motion (there should be none yet).

## Interaction

Citizen pages are static. Allowed: in-page `<details>`, hash links, horizontal scroll of a chart well, Vega-Lite hover and chart download from **already-bound** specs. Forbidden: request-time fetch, engagement SDK, A/B, heatmap, live filter that loads another vintage, "get notified." Geography as a pre-rendered route or a client filter over observations from **this** vintage is a later, named piece of work — not a copy of their metro picker.

## Implementation

| Place | What changes |
|-------|----------------|
| `src/cms/src/lib/theme.ts` | Tokens, `fitWidth`, number format, Vega house config. One source. |
| `src/cms/src/styles/desk.css` | Layout primitives and site chrome. Inherit tokens; no hex. |
| `src/cms/src/layouts/SiteShell.astro` | Apply the theme. Shared shell. No page-local palette. |
| `src/cms/src/lib/render-chart.ts` | Apply the theme's Vega frame and the legibility floor. Specs do not restyle. |
| `src/cms/templates/**/*.vl.json` | Encode breaks and holes. No new palettes. |
| `src/prism/template_bind.py` | Layout blocks, heading level, first-screen cite strip. No new block without updating this file |
| `src/prism/cms_site.py` | Catalog fields the chrome reads (one-liner, per-card vintage, rail siblings) |

Do not add Storybook, a token npm package, or a second CSS framework. Pages inherit the desk theme; they do not define one.

## Presentation pass

UI/UX Developer. Run on **preview** before Trust, on **every template that reached Content Editor Proof** — not only when chrome or charts changed. A new template breaks form factor at a new data shape while the house is untouched: C2 and C3 changed no token and no stylesheet, and both shipped a figure bleeding out of its cell. Record `skipped` only when the same template renders the same page at the same vintage.

Gate: this file. Every box below carries how it fails.

- [ ] **Tokens.** Same house tokens on every block. No mixed palettes, no magenta / cream / Aeonik / USAFacts costume. *Fails on:* any hex in `desk.css`, any page-local palette.
- [ ] **Type scale.** H1, H2, byline, figcaption, source-line, labels on the scale. Chart titles in HTML, not Vega. *Fails on:* a heading element whose level and size disagree; a Vega title at 14px beside an H2 at 1.25rem.
- [ ] **Measure.** Running prose, lede, byline, source-line at `--measure`. *Fails on:* any paragraph over 90 characters per line at 1440px.
- [ ] **Stat fit.** *Fails on:* any `.stat-figure` wider than its cell's content box at 360, 480, 768, 1024, or 1440px. Measure it; do not eyeball it.
- [ ] **Chart legibility.** *Fails on:* any SVG text rendering below 12px effective size — intrinsic size × rendered scale — at any of those widths.
- [ ] **One plot width.** *Fails on:* two charts on one page with different intrinsic SVG widths.
- [ ] **Chart wells.** Plot fills the well at desk width; no leftover white field. *Fails on:* reserved label padding wider than the longest label.
- [ ] **Number agreement.** *Fails on:* an axis label and a bar value label in the same chart using different grouping; a stat figure and a lede figure that are different strings.
- [ ] **Bars.** Horizontal; house `barStep` so thickness does not depend on category count. *Fails on:* a two-category chart whose bars are thicker than a thirty-six-category chart's.
- [ ] **Cite proximity.** *Fails on:* the producer name further than 600px from the top of `main` at 1440×900; a first-screen summary missing producer, series, reference period, or release date.
- [ ] **Holes.** *Fails on:* a hole rendered smaller or lower-contrast than its sentence.
- [ ] **Contrast.** *Fails on:* any text under 4.5:1 or meaningful graphic under 3:1 against its actual ground.
- [ ] **Screenshot test.** A crop still shows title, unit, geography, source line, and visible holes at readable size, and does not look like a USAFacts chart.

Fail the pass if any box is open. Fix here. Content Editor Proof hands a named form-factor list; it does not restyle. Hand to Trust only for cites, dates, holes, spin — not for taste.

A new token or primitive is specified in this file first — do not invent it in a one-off template. Tone is quiet, corporate, professional, minimal, modern — not prettier-than-the-record, not a scorecard.

Checklist also lives on the persona: [ui-ux-developer.md](personas/ui-ux-developer.md).

## Out of scope for this system

Pipeline schema, citation *content*, chart *meaning*, voice and copy ([editorial-guidelines.md](editorial-guidelines.md)), routes and slugs ([web-design.md](web-design.md)), Trust ship/block, a public wordmark beyond a text lockup, dark mode, a mobile app, the number-grouping convention (bind, per Front-end ruling R8).

## Next

The preview desk at `localhost:4321` carries the desk home, five hubs, and three bound slices: C1 `/prices/retail-prices`, C2 `/people/population`, C3 `/money/union`. C1 alone is on the citizen pointer; C2 and C3 are preview-only and Charter owns publish.

Preview at `localhost:4321` now implements [ui-ux-change-plan.md](next/ui-ux-change-plan.md) Phases A–D. Do not move `data/pointers/citizen`.
