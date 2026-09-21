# Design system

UI/UX Developer. Visual contract for citizen pages (**v3**). Persona: [ui-ux-developer.md](personas/ui-ux-developer.md). How the page **reads** is [editorial-guidelines.md](editorial-guidelines.md) (Content Editor) — this file implements that as type, colour, layout, and chart chrome. UI/UX Developer implements this file and runs the presentation pass against it. Routes, titles, SEO, and preview vs published HTTP: [web-design.md](web-design.md) (Front-end Architect). Integrity stays in [data-contracts.md](data-contracts.md) and [architectural-blueprint.md](architectural-blueprint.md).

Product role, answer-page shape, and newsroom forbids live in the editorial guidelines. Stack (Astro SSG, Vega-Lite) lives in [repo-conventions.md](repo-conventions.md). Current work lives under [Next](#next).

v1 (quiet desk): [design-system-v1.md](archive/design-system-v1.md). v2 (welcome ruling, read as austere): [design-system-v2.md](archive/design-system-v2.md). Tone: [design-philosophy.md](design-philosophy.md). Direction on v2: [ui-ux-feedback.md](next/ui-ux-feedback.md).

```text
version:        v3
tone:           modern, welcoming, civic publisher, generous
idea:           official record, built for a person — answer first, archive on request
house:          three grounds (paper / card / well); IBM Plex Serif for the record's
                voice (headings, every bound figure), IBM Plex Sans for the desk's
                voice (everything else); navy + clay + slate + graphite as series colour
tokens:         CSS custom properties on :root — not in the vintage
fit:            every rule below must hold at 360px and at 1440px
```

## The house

One house for the portrait in [vision.md](vision.md). A citizen should recognise it on every slice, and want to stay on the first one.

v2 was readable and it was flat: one lift value on every card, one type family carrying both headline and footnote, and a palette read as two greys and a navy. The principal's word for the result was **austere**, not calm. v3 keeps every fit and contrast floor v2 earned — nothing here reopens `--hole` contrast, the ten-digit stat floor, the 12px chart floor, or cite proximity — and rebuilds the house so the answer has somewhere to land.

**What v3 drops from v2, and why:**

- **"One `--lift` token."** A single flat shadow on every card is why nothing on the page felt designed. v3 keeps two tiers — `--lift` (resting: evidence) and `--lift-answer` (the record's answer, once per page) — still no colour, no glow, no stacked marketing shadow.
- **"`--radius` 8px, one value."** v3 adds `--radius-lg` for the same one place `--lift-answer` applies. Everywhere else is still `--radius`. Still not pills, still not 0.
- **"Sans throughout... do not use a serif for body."** Body copy is still sans — that half stays. The other half (no serif anywhere) is dropped: headings and every bound figure now set in IBM Plex Serif. Detail in [Two voices](#two-voices).
- **`.fact-lede` as a lone card, `.stat-row` and `.cite-strip` as separate ones below it.** These three now compose one visual band — [The answer well](#the-answer-well) — because a sentence, a grid of white boxes, and a collapsed footnote reading as three unrelated objects was the "non-intuitive" complaint, not the objects themselves.

**A rule that cannot be measured is not in this file.** Each rule below carries the measurement that fails it.

Do not retune the pipeline for layout. Content Editor names blocks; UI/UX specifies and applies the styles.

### Non-negotiable, regardless of house

Restated here because this pass had "high control" over everything else. These did not move:

1. Tone: modern, welcoming, civic publisher, generous.
2. Official record, built for a person — answer first, archive on request.
3. Not USAFacts costume: no magenta/cream/Aeonik/wordmark, no search/chat/newsletter/"get notified", no performance colour, no wordmark-swap.
4. Do not hide a hole or a cite.
5. One well on the first screen; method is quieter and later.
6. Floors: 12px chart type, stats that fit ten-digit counts, `--hole` ≥ 4.5:1, producer on the first screen, WCAG AA.
7. Tokens live in CSS custom properties, not the vintage.

## Costume we do not copy

- Magenta bar, Aeonik, pink/magenta sentence highlight (`span.answer`)
- Purple illustrated heroes; a news-style hottest-topics carousel (scoops, engagement)
- Newsletter, social kits, "get notified", video desk, search box, chat widget
- Cream plot, brand-colour edge rule, magenta download pill, chart-corner logo

A page that would pass for USAFacts with the wordmark swapped has failed this system.

## Three grounds

The house reads on three planes, not one flat card colour:

| Ground | Token | Carries |
|--------|-------|---------|
| **Paper** | `--paper` | The page. Warm stone — an institution's paper, not a screen's white and not a marketing brand's cream. |
| **Card** | `--card` | Evidence — stats, charts, fast facts, source cards. White, so a number always sits on the same plane its neighbours do. |
| **Well** | `--well` | The answer, once per page. A cool, iso-luminant wash — same lightness as `--paper`, different hue — so the shift is felt as a change of place, not a jump in brightness. Never a verdict; never used for a second thing on the page. |

A citizen who has seen one slice reads the next by ground alone: white box, look for a citation; tinted band, this is what the page is answering.

## House chrome

| Class | Tokens | Job |
|-------|--------|-----|
| `.fact-lede` | Top segment of [the answer well](#the-answer-well); `--well`; `--ink`; serif figures inline | The bound answer as a sentence: number, unit, place, year — then one line of definition. Not a magenta sentence. Not a slogan. |
| `.stat-row` / `.stat` | Middle segment of the well; `.stat` chips are `--card` on `--well`, `--radius`, `--lift` | 2–4 equal-weight bound figures, set apart from the sentence above them like tiles on a tray. No winner colour. |
| `.cite-strip` | Bottom segment of the well; producer `--ink`; rest `--muted` | Source line **next to the number**, closing the well. Open state is the full card. Not a codebook dump. |
| `.fast-facts` | `--card`, `--radius`, `--lift`; fact 1.375rem / 500 / `--ink`, sans | Publisher front: slot-bound one-liners. Never byline grey. Not a ticker of unnamed numbers. |
| `.hottest-rail` | `--paper` background, `--card` chips, `--radius`, `--mark` links | Featured citizen questions / slices. Not scoops, not "hottest topics," no "get notified." |
| `.analysis-byline` | `--muted` | Optional "Analysis by Prism" next to the producer. Never instead of the producer. |

## Visual encodings

Encode the editorial guidelines as chrome. Not a second reading contract.

1. **No performance colour.** Colour and weight never mean better or worse. Alphabetical / documented geographic order by default. Measure-sort only on a rank question.
2. **The answer is a place, not a slogan.** The well is where a citizen lands. Display type is for bound figures, not mission sentences. On any page that quotes a figure, the largest non-heading text on the first screen is a bound observation.
3. **Cite in the same view.** Producer next to the number, inside the same well. A tooltip is not enough. A fly-out that leaves the view is not enough.
4. **Holes stay holes.** Never smaller, lighter, or lower-contrast than the sentence they sit in — same rule for size, colour, **and typeface**: a hole set inside a serif figure stays serif italic, not a demoted sans footnote.
5. **Two tiers of elevation, once each.** The answer well sits higher than its evidence (`--lift-answer` vs `--lift`). That is the only place hierarchy is felt through elevation. Everything else is equal weight.
6. **Generous craft, quiet meaning.** Radius, lift, space, and the well's hue carry "designed." They do not argue. No gradient. No illustration the vintage did not earn.
7. **Legible or scrollable, never shrunk.** Nothing below 12px effective size. At 1440px the first chart fills the well with **no horizontal scroll**. Narrower viewports scroll the figure; they do not shrink type.

## Tokens

CSS custom properties on `:root`. Not in the vintage schema.

### Colour

Warm stone paper, warm ink, navy as the institutional accent, clay and slate as its company. Navy is how C1 already plots (`#1F4E79`) — kept for continuity, not habit.

Contrast is quoted against `--paper` and `--card`; the well is decorative ground and is quoted for legibility of `--ink`/`--mark`/`--muted` printed on it, not for its own contrast against paper (see [Three grounds](#three-grounds) — the shift is hue, not lightness, on purpose).

| Token | Hex | Use | On `--paper` | On `--card` | Needs |
|-------|-----|-----|:---:|:---:|:---:|
| `--paper` | `#F3EEE6` | Page ground | — | — | — |
| `--card` | `#FFFFFF` | Evidence: stats, charts, fast facts, source cards | — | — | — |
| `--well` | `#EAF0F5` | Answer ground, once per page — `.fact-lede`, `.stat-row`, `.cite-strip` | n/a (hue shift, see above) | — | decorative |
| `--ink` | `#1C1A17` | Body, headings, figures, producer | 15.0 | 17.4 | 4.5 |
| `--muted` | `#5B5548` | Byline, labels, axis, cite rest | 6.4 | 7.4 | 4.5 |
| `--hole` | `#6E6656` | Not published | 4.9 | 5.7 | 4.5 |
| `--mark` | `#1F4E79` | Links, focus, series 1, header rule, well top rule | 7.5 | 8.7 | 4.5 |
| `--mark-2` | `#9C5233` | Chart series 2 (clay) | 5.0 | 5.7 | 3.0 |
| `--mark-3` | `#4A6670` | Chart series 3 (slate; not "good") | 5.3 | 6.1 | 3.0 |
| `--mark-4` | `#5C5C5C` | Chart series 4 (graphite) | 5.8 | 6.7 | 3.0 |
| `--break` | `#332E27` | Series-break rule | 11.7 | 13.5 | 3.0 |
| `--rule-strong` | `#8C8370` | Meaning-carrying lines (axis domain, zero line) | 3.3 | 3.8 | 3.0 |
| `--rule` | `#DDD6C9` | Hairlines and chart grid | 1.3 | 1.4 | decorative |
| `--hole-band` | `#E7E0D2` | Hole-band fill | 1.1 | 1.3 | decorative |
| `--focus` | `#1F4E79` | Focus ring | 7.5 | 8.7 | 3.0 |

`--hole` stays at or above 4.5:1. Do not lighten it to look calmer. Every value above is computed (relative-luminance WCAG formula), not eyeballed; recompute before changing a hex.

Text on `--well` is not a separate column above because it is, by design, within 0.05 of the `--paper` figures for every token printed on it: `--ink` 15.1:1, `--muted` 6.4:1, `--mark` 7.5:1, `--hole` 4.9:1. The well is iso-luminant to the paper — the same lightness, a different hue — so nothing that clears AA on paper needs re-checking on the well.

**A decorative fill is allowed; a decorative meaning is not.** `--rule`, `--hole-band`, and `--well` do not carry meaning alone. A hole band needs a `--rule-strong` edge **and** a label. `--well` is a landing field, not a verdict, and appears in exactly one place per page.

**Forbidden as tokens:** magenta / hot pink; wine as a USAFacts-style edge; red–green; gold/saffron; dashboard blues; the tricolour as brand or scale; party colours; ministry campaign palettes; saffron/green as up/down.

Links are `--mark` plus underline. Visited is the same.

### Two voices

The record has a voice for what it states and a voice for what it does. **IBM Plex stays** — expanded, not dropped.

| Voice | Face | Carries |
|-------|------|---------|
| The record | **IBM Plex Serif** | H1, H2, and every bound figure (`.observation-value`, `.stat-figure`, the numbers inline in `.fact-lede`). 500 / 600. The thing the page is asserting. |
| The desk | **IBM Plex Sans** | Body, byline, labels, nav, chart SVG text (axis, bar labels, `figcaption`), fast facts. 400 / 500 / 600. The scaffolding around the assertion. |
| Identifiers | **IBM Plex Mono** | `vintage_id`, `series_id`, geography codes, the preview banner — not body, not a bound figure. |
| Later scripts | IBM Plex Sans Devanagari | When a template ships a non-English official name. English first. |

Chart SVG type is **always** Sans, in every context — the 12px legibility floor is measured on rendered SVG at real scale, and a mismatched serif at that size is the one place "record voice" would cost readability. Fast facts (home, index pages) are Sans throughout, including their numbers — they are navigation, not the answer to a citizen question.

Self-host under `src/cms/public/fonts/`: Sans 400/500/600 (already shipped), Serif 400/500/600 + italic 400 (new), Mono 400 (already shipped). No font CDN at render or request time. Fallback for Serif: `"IBM Plex Serif", Georgia, "Times New Roman", serif`. Fallback for Sans unchanged: `"IBM Plex Sans", "Source Sans 3", "Segoe UI", system-ui, sans-serif`.

Do not use Aeonik. Do not put Serif on body copy, labels, byline, chart SVG, or fast facts — the split is the point; a page that runs Serif everywhere or Sans everywhere has lost it.

**Scale** (root 16px)

| Style | Face | Size | Weight | Line | Tracking |
|-------|------|------|--------|------|----------|
| Sleeve | Sans | 0.75rem | 500 | 1.3 | 0.08em; uppercase |
| H1 (question) | Serif | `clamp(2rem, 4.5vw, 3rem)` | 500 | 1.15 | −0.02em |
| H2 (section) | Serif | 1.5rem | 500 | 1.3 | 0 |
| Bound figure (`.stat-figure`, inline in `.fact-lede`) | Serif | `clamp(1.25rem, 12cqi, 2.75rem)` | 600 | 1.08 | −0.02em; tabular-nums |
| Fast-fact (home, index) | Sans | 1.375rem | 500 | 1.3 | 0; `--ink` |
| Body | Sans | 1.125rem | 400 | 1.65 | 0 |
| Byline / source | Sans | 0.875rem | 400 | 1.45 | 0 |
| Label / dt | Sans | 0.75rem | 500 | 1.3 | 0.04em; uppercase; `--muted` |
| Caption | Sans | 0.875rem | 400 | 1.4 | 0 |
| Hole (inline) | Inherits its sentence's face | Inherits its sentence's size | Italic | Inherits | `--hole` |
| Chart SVG (axis, bar label) | Sans, always | 12px minimum | 400 / 500 | — | tabular-nums |

**12px is the floor.** Nothing a citizen reads, including SVG text after scale.

**A hole inherits its sentence.** Italic, colour, size, **and face** are the encoding; smaller or demoted-to-sans is not.

**The bound figure is sized by its cell.** `cqi` is the `.stat` inline size. `12cqi` and a 1.25rem floor are the measured Serif values that keep a ten-digit count inside the cell at 360px. See [Fit](#fit).

H1 is a citizen question, not a 72px slogan. The bound figure is the climax. Home's welcome is the fact grid at 1.375rem.

### Space, radius, lift

| Token | Value | Use |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 px | Stacking only these steps |
| `--desk` | 68rem | Landing well: hero, stats, charts, header, footer, home facts. Shared left **and** right edge. |
| `--measure` | 40rem | Method prose only (`.how-measured`). Not the hero. Not a section that holds a chart. |
| `--radius` | 12px | Evidence cards: stats, charts, fast-fact tiles, source cards. Not pills. Not 0. |
| `--radius-lg` | 20px | The answer well only — its one exterior shape, top corners of `.fact-lede`, bottom corners of `.cite-strip`. |
| `--lift` | `0 1px 3px rgb(28 26 23 / 0.08)` | Evidence cards (stats, fast-facts, chart well). Resting tier. |
| `--lift-answer` | `0 10px 24px rgb(28 26 23 / 0.10), 0 2px 6px rgb(28 26 23 / 0.06)` | The answer well only. One extra step of elevation, still no colour, no glow, no stacked marketing shadow. |
| `--hair` | 1px | Borders |
| `--header-rule` | 4px `--mark` | Top of the viewport, and the top edge of the answer well |

No gradient. Lift is product elevation, not decoration that argues. `prefers-reduced-motion` does not remove lift (it is static, not an animation).

## Fit

The desk holds ten-digit official counts. Layout that only works for `4.82` is not a layout.

**One width on the composed well.** Lede, stats, cite, and charts in the same view share `--desk`. Content boxes match at 1440px (right edges within 1px). A section that contains a chart is the same well. `--measure` is method only.

Hero copy is short; it may run at `--desk`. Method at 68rem was **124 characters per line** in earlier testing — `.how-measured` stays at `--measure`. Do not fail the hero for exceeding 90 characters per line.

**Stat cells fit the widest figure the vintage can bind.**

```css
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr));
  gap: var(--space-4);
}
.stat { container-type: inline-size; min-width: 0; }
.stat-figure { font-size: clamp(1.25rem, 12cqi, 2.75rem); }
```

`17rem` (up from a Sans-only `16rem`) stops cells packing narrower than a Serif ten-digit string needs; `min(100%, …)` stops overflow at 360px; `cqi` shrinks the figure before the card. Measured on shipped IBM Plex Serif: `1,21,08,54,977` at 1.75rem was 191px in a 184px cell at 360px, so the floor is **1.25rem** and the `cqi` multiplier is **12**. The widest plausible bound string — ten digits plus four separators — must fit at every cell width the grid can produce, including the ungrouped form.

**Grouping is not decided here.** One convention at bind (Front-end ruling R8). This file guarantees the string **fits**.

**Breakpoints.** One: `48rem`. Below it, a single column. Do not add a second breakpoint to solve a fit problem that `clamp`, `min()`, or a container query solves.

**Every rule is checked at 360px and 1440px.**

## Layout primitives

Content Editor may name only these blocks (`LAYOUT_BLOCKS` in `src/prism/template_bind.py`). Do not invent a second set in YAML. **Kept unchanged from v2** — the redesign is in the tokens and in how these blocks are composed visually, not in their keys, tags, or classes; renaming them here would break every template for no reader-facing gain.

| Token | Element | Job |
|-------|---------|-----|
| `hero` | `<header class="hero">` | First screen: sleeve, question, byline, the answer well, cite next to the numbers, first chart. One `--desk` column. |
| `stat-row` | `<div class="stat-row">` | 2–4 bound figures, equal weight — middle segment of the answer well |
| `section` | `<section class="portrait-section">` | One idea; heading; copy; optional stats; one chart. If it holds a chart, the section is `--desk`. |
| `how-this-is-measured` | `<section class="how-measured">` | Method after the record. Prose at `--measure`. Quieter than the answer. |
| compact source byline | `<details class="citation-card source-byline">` | Summary visible; full card on open |
| caveat note | `<details class="caveat-note">` | Same rule |

**Section headings are `<h2>`.** Element and scale agree. Fix at bind, not with a CSS override.

### The answer well

`.fact-lede`, `.stat-row`, and `.cite-strip` are three separate elements in the DOM (Content Editor still writes them as three separate blocks) that read as **one object** on screen: a single tinted band with one exterior radius and one elevation, joined by hairline dividers instead of gaps.

```text
┌─ --radius-lg top corners, 4px --mark top rule ───────┐
│  .fact-lede    sentence, --well ground, serif figures │
│  ─── hairline ───                                      │
│  .stat-row     .stat chips: --card on --well, --lift   │
│  ─── hairline ───                                      │
│  .cite-strip   producer --ink, rest --muted             │
└─ --radius-lg bottom corners ──────────────────────────┘
```

Achieved with adjacent-sibling selectors that zero the joining margins and interior radii (`.fact-lede + .stat-row`, `.stat-row + .cite-strip`) — no new wrapper element, no change to `LAYOUT_BLOCKS`. The well takes `--lift-answer` and `--radius-lg` on its own outer edge only; `.stat` chips inside it keep their own smaller `--radius` and resting `--lift`, like tiles set on a tray. The first chart is **not** part of the well — it is evidence, on `--card`, directly below.

### Site chrome

Same tokens. Not a full-bleed marketing bar. Not a USAFacts wordmark. Routes: [web-design.md](web-design.md).

| Region | Class | Job |
|--------|-------|-----|
| Skip link | `.skip-link` | `--card` fill, `--mark` type; 44px; first focusable |
| Header rule | `body` border-top | `--header-rule` |
| Frame | `.site-frame` | `--desk`; padding-inline `--space-6`; padding-block `--space-6` / `--space-8` |
| Header | `.site-header` | Lockup + sleeve nav; gap `--space-5` |
| Lockup | `a.site-lockup` | 1rem / 500 / 0.04em uppercase; Sans; `--ink`; no underline; links to `/` |
| Sleeve nav | `.sleeve-nav a` | `--mark` + underline; 44px; `aria-current` is weight 600 |
| Breadcrumb | `.breadcrumb` | 0.875rem; Sans; `--muted`; current `--ink`. Wrap; do not cap at `--measure` while H1 is `--desk`. |
| Main | `main#main` | `--desk` via `.site-frame` |
| Footer | `.site-footer` | Hairline; byline size; 44px hits; no SDK |
| Fast facts (home) | `.fast-facts` | Grid `repeat(auto-fit, minmax(min(100%, 20rem), 1fr))`; gap `--space-5`; `--card` tiles, `--radius`, `--lift`. Publisher front. |
| Hottest rail | `.hottest-rail` | Featured questions |
| Sleeve index | `.sleeve-index` | Body type; `--mark` + underline; 44px. Not a tile grid. |
| Preview banner | `.preview-banner` | Serve-only (R5). `--card`, hairline, `vintage_id` in Mono 0.75rem. No control. Never in the citizen tree. |

No search, subscribe, or social row. No engagement SDK.

**Publisher front (home).** H1 is the purpose sentence at H1 scale, Serif. The designed moment is the fact grid — 1.375rem `--ink` Sans one-liners, side by side at `--desk` on `--card` tiles. Then the featured-question rail. Not a mission whisper over grey paragraphs. Not a display-size slogan.

**First screen (every slice).** Editorial scan path as one composed well.

1. Sleeve (topic family, not a news kicker).
2. Citizen question as H1 (geography in the words).
3. Byline: release date (`Asia/Kolkata`), next named release.
4. The answer well: `.fact-lede` sentence, `.stat-row` chips, `.cite-strip` — one band, `--desk` width.
5. First chart, on `--card`, filling the same well.

Hottest rail closes the hero; never above the cite. Methodology is not on screen 1. Left-aligned. Do not centre the question.

## Chart system

Vega-Lite in git; SVG at render. `src/cms/src/lib/render-chart.ts` applies the frame. Specs encode breaks and holes.

**House look.** `--card` well, `--radius`, `--lift`, 1px `--rule` hairline. No coloured left bar, no corner logo, no magenta download pill. Title and subtitle in HTML `figcaption` (`.chart-title` = H2 scale, Serif; `.chart-subtitle` = byline scale, Sans). Plot field is `--card`, not cream.

**Legibility floor.** Authored at one house `plotWidth`. SVG `width: 100%` scales type. Do not roll the 12px floor back to make a well look filled.

- `fitWidth` is the well **content** width at `--desk`: `68rem` (1088px) minus 2× frame padding-inline (`--space-6`, 32px) minus 2× figure padding (`--space-5`, 24px) minus 2× `--hair` (1px) = **974px**. Recalculate if those paddings or the hairline change. At desk width the SVG is 1:1.
- Do not scale the SVG. Below desk width, `figure.chart` scrolls. Authored type stays 12px effective.
- **At 1440px the first-screen chart does not scroll.**
- Every chart on a page: same `plotWidth`.
- Category height is `n × barStep`. Do not compress; scroll.

**Bars.** Horizontal; house `barStep` (26px, up from 22 — a slightly heavier, more confident bar); single-series navy fill by default; **2px corner radius on the bar's outer end** — the one chart-chrome detail this pass adds beyond the legibility floors, matching the house's soft-cornered cards without touching axis, grid, or label rendering. No extra legend when the axis names the categories.

**Numbers agree.** Axis, bar labels, lede, and stat cell use one format from bind. `render-chart.ts` does not invent a format of its own. `valueLabelPad` is derived from the longest formatted label on that chart, not a flat value — a fixed pad leaves dead white field when labels are short and clips them when labels are long.

**Series colour** is categorical position, never magnitude: `--mark`, `--mark-2`, `--mark-3`, `--mark-4`. Grid `--rule` at 50% on the quantitative axis. Domain and meaning-carrying lines: `--rule-strong` or `--ink`. Axis labels `--muted`. Zero line `--ink` 1px. Break: dashed `--break` plus labelled `--hole-band`. Unknown: `invalid: "break-paths"`; never plot as zero.

**Order.** States/UTs alphabetical by official English name, or documented geographic order. Measure-sort only on a rank question. Divisions: producer annex order. Never red–green. Test 8 gates the default.

**One idea.** Two encodings → two charts. A chart that only repeats the stat row is not evidence.

**Screenshot test.** Crop still shows title, unit, geography, source, holes, at readable size. It does not look like a USAFacts chart (cream, magenta rail, wordmark). Attribution is the citation card, not a corner logo.

## Citation chrome

Checkability is proximity, not a field dump.

- Producer within the first **600px** of `main` at 1440×900.
- `<details class="citation-card source-byline cite-strip">` closes [the answer well](#the-answer-well), after the stat chips and **before** the first chart, same `--desk` width.
- Summary: producer `--ink`, then `series · reference period · released {date}` `--muted`. All four, every slice. Missing field fails the render.
- Open: producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, caveat. Same cite as the bottom `.source-stack`, earlier.
- Optional `.analysis-byline` after the producer, never instead.

Collapsed `<details>` is the default. Empty chrome while the number shows fails the render. No fly-out that leaves the view (R7).

Caveats: same panel language; no warning-orange.

## States the UI must show

| Status | Surface |
|--------|---------|
| `value` | Tabular Serif figure or mark |
| `unknown` / not published | Em dash or "Not published", italic `--hole`, inherits its sentence's size and face; slot stays |
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

Static pages. Allowed: `<details>`, hash links, chart scroll when the well is narrower than `fitWidth`, Vega hover and download from **already-bound** specs. Forbidden: request-time fetch, engagement SDK, A/B, heatmap, live filter that loads another vintage, "get notified." Geography routes or a client filter over **this** vintage are later named work — not their metro picker.

## Implementation

Not part of this return — named here so the next pass knows what changes.

| Place | What changes |
|-------|----------------|
| `src/cms/src/lib/theme.ts` | Tokens (`--paper`, `--well`, `--radius`, `--radius-lg`, `--lift`, `--lift-answer`, `--mark-2` hex, type scale, `fitWidth` 974, `minScale` 1, `barStep` 26, bar corner radius), Vega house config. One source. |
| `src/cms/public/fonts/` | Add IBM Plex Serif 400/500/600 + italic 400 (woff2, self-hosted, matching the existing Sans/Mono pattern). |
| `src/cms/src/styles/desk.css` | Publisher layout; the answer-well join (adjacent-sibling selectors on `.fact-lede`, `.stat-row`, `.cite-strip`); Serif applied to H1/H2/`.stat-figure`/`.observation-value`. Inherit tokens; no hex. |
| `src/cms/src/layouts/SiteShell.astro` | Apply the theme. No page-local palette. |
| `src/cms/src/lib/render-chart.ts` | Vega frame + legibility floor + bar corner radius + derived `valueLabelPad`. Specs do not restyle. |
| `src/cms/templates/**/*.vl.json` | Breaks and holes. No new palettes. |
| `src/prism/template_bind.py` | Blocks, heading level, cite strip. No new block without this file — `LAYOUT_BLOCKS` is unchanged by this pass. |
| `src/prism/cms_site.py` | Catalog fields the chrome reads. |

No Storybook, no token npm package, no second CSS framework.

## Token delta

Against the live `src/cms/src/lib/theme.ts` (v2's shipped values, several already ahead of v2's own doc text). Recompute-verified with the WCAG relative-luminance formula, not eyeballed.

| Token | Live (`theme.ts`) | v3 | Why |
|-------|---|---|---|
| `--paper` | `#F4F2EE` | `#F3EEE6` | Warmer, slightly deeper stone — still not cream (higher grey, lower yellow chroma than a marketing cream field). |
| `--card` | `#FFFFFF` | `#FFFFFF` | Unchanged. |
| `--well` *(new)* | — | `#EAF0F5` | New third ground. Decorative, iso-luminant to `--paper` on purpose — see [Three grounds](#three-grounds). Not the same token as v2's undeployed `--mark-soft` (never shipped in `theme.ts`); this replaces that idea with a named, load-bearing ground rather than a wash on a card. |
| `--ink` | `#1A1A1A` | `#1C1A17` | Warmed to sit with the warm paper family. Contrast unaffected (15.0:1 on paper, still miles clear of 4.5). |
| `--muted` | `#5A5A5A` | `#5B5548` | Warmed to match. 6.4:1 on paper, unchanged margin. |
| `--hole` | `#6B6B6B` | `#6E6656` | Warmed. 4.9:1 on paper — still clears 4.5 with the same margin as before; this is a hue shift, not a re-litigation of the v2 AA fix. |
| `--mark` | `#1F4E79` | `#1F4E79` | **Unchanged.** Continuity with already-rendered C1 charts and the reason v2 gave for choosing it in the first place. |
| `--mark-2` | `#7A542E` (brown) | `#9C5233` (clay) | Warmer, more distinct from `--mark-3` at a glance, still an earth tone — not gold/saffron. 5.0:1 on paper. |
| `--mark-3` | `#4A6670` | `#4A6670` | Unchanged. |
| `--mark-4` | `#5C5C5C` | `#5C5C5C` | Unchanged. |
| `--break` | `#333333` | `#332E27` | Warmed to match the ink family. Contrast still >11:1, no functional change. |
| `--rule-strong` | `#8C857A` | `#8C8370` | Slightly darker for margin above the 3.0 floor (was 3.16–3.4 depending on ground; now 3.3–3.8). |
| `--rule` | `#D6D2CA` | `#DDD6C9` | Warmed, decorative only. |
| `--hole-band` | `#E3DFD8` | `#E7E0D2` | Warmed, decorative only. |
| `--focus` | `#1F4E79` | `#1F4E79` | Unchanged. |
| `--radius` | `0` (live code; docs said 8px) | `12px` | Resolves the doc/code mismatch in favour of the more generous value, per this pass's "boring" fix, not a split-the-difference compromise. |
| `--radius-lg` *(new)* | — | `20px` | The answer well's one exterior shape. |
| `--lift` | not in `cssVars` yet | `0 1px 3px rgb(28 26 23 / 0.08)` | First implementation of the v2-documented, never-shipped lift token. |
| `--lift-answer` *(new)* | — | `0 10px 24px rgb(28 26 23 / 0.10), 0 2px 6px rgb(28 26 23 / 0.06)` | Second elevation tier — the dropped "one lift token" rule; see [The house](#the-house). |
| `chart.fitWidth` | `1008` | `974` | Desk content minus frame padding, figure padding, **and** 2× `--hair`. 976 omitted the hairline and rendered chart type at 11.98px at 1440px. |
| `chart.minScale` | `0.92` | `1` | 0.92 × 12px = 11.04px on a phone. Never shrink; scroll. |
| `chart.barStep` | `22` | `26` | Heavier, more confident bar. |
| `chart` bar corner radius | none | `2px` | New — see [Chart system](#chart-system). |
| Type: display-figure clamp | `clamp(1.75rem, 14.5cqi, 2.75rem)`, Sans | `clamp(1.25rem, 12cqi, 2.75rem)`, **Serif** | Face change plus a measured floor: 1.75rem / 13cqi overflowed `1,21,08,54,977` at 360px. |
| Type: H1/H2 face | Sans | Serif | New. |
| Font files | Sans 400/500/600, Mono 400 | + Serif 400/500/600 + italic 400 | New self-hosted family member; same hosting pattern, no CDN. |



## Presentation pass

Run on **preview** before Trust, on **every template that reached Content Editor Proof**. Skip only when the same template renders the same page at the same vintage.

Appeal means **modern, welcoming, civic publisher, generous** — same house. Generous is space, scale, elevation, and the answer well. It is not their kit. Not a scorecard. Not USAFacts magenta. Not unfinished.

Measure at 360px and 1440px. Do not eyeball.

- [ ] **Tokens.** One house, three grounds. `--radius` 12px on evidence, `--radius-lg` 20px on the answer well only. No hex in `desk.css`. No magenta / cream / Aeonik / costume.
- [ ] **Two voices.** Serif on H1, H2, and every bound figure. Sans everywhere else, including all chart SVG text. No page runs one face throughout.
- [ ] **One well.** Lede, stats, cite, first chart: `--desk`; widths match within 1px at 1440px. Hero children not capped at `--measure`.
- [ ] **Method measure.** `.how-measured` prose at `--measure`. *Fails on:* a method paragraph over 90 characters per line at 1440px.
- [ ] **The answer well.** `.fact-lede` + `.stat-row` + `.cite-strip` read as one band: shared `--well` ground, one `--radius-lg` exterior, `--lift-answer`, 4px `--mark` top rule, hairline joins, no visible gap between the three.
- [ ] **Stat fit.** No `.stat-figure` wider than its cell at 360, 480, 768, 1024, or 1440px, in the shipped Serif.
- [ ] **Chart legibility.** No SVG text under 12px effective (intrinsic × scale) at those widths.
- [ ] **Desk chart, no scroll.** First-screen `figure.chart` has no horizontal scrollbar at 1440px.
- [ ] **One plot width.** No mixed intrinsic SVG widths on one page.
- [ ] **Chart wells.** Plot fills the well at desk width; `--radius` on the figure; bar ends carry the 2px corner radius. *Fails on:* label padding wider than the longest label.
- [ ] **Number agreement.** One grouping inside a chart and between lede and stat.
- [ ] **Bars.** Horizontal; house `barStep` (26px).
- [ ] **Cite.** Producer within 600px of `main` at 1440×900, `--ink`, before the first chart; summary has all four fields.
- [ ] **Holes.** Not smaller, lower-contrast, or demoted to Sans inside a Serif context.
- [ ] **Contrast.** Text ≥ 4.5:1; meaningful graphics ≥ 3:1 on the actual ground (paper, card, **or well**).
- [ ] **Screenshot test.** Crop shows title, unit, geography, source, holes at readable size; does not look like a USAFacts chart; reads as Prism without the header rule visible (the well, the clay-and-navy series colour, and the Serif figure are the tell).

Fail the pass if any box is open. Content Editor Proof names form-factor breaks; it does not restyle. Trust gets cites, dates, holes, spin — not taste.

A new token or primitive is specified here first.

Checklist also on the persona: [ui-ux-developer.md](personas/ui-ux-developer.md).

## Out of scope

Pipeline schema, citation *content*, chart *meaning*, voice and copy ([editorial-guidelines.md](editorial-guidelines.md)), routes and slugs ([web-design.md](web-design.md)), Trust ship/block, a public wordmark beyond a text lockup, dark mode, a mobile app, number-grouping (R8). USAFacts costume. Pointer flips.

## Next

Presentation pass **green** on preview `desk-20260916-6328e59eb0d1` (2026-09-21): home, C1 `/prices/retail-prices`, C2 `/people/population`, C3 `/money/union` at 360 and 1440; stat fit also at 480, 768, 1024. `fitWidth` 974, `minScale` 1, display clamp `1.25rem / 12cqi`. Do not move `data/pointers/citizen`.

C1 is on the citizen pointer; C2 and C3 are preview-only. Charter owns publish. Trust next for cites, dates, holes, spin — not taste.
