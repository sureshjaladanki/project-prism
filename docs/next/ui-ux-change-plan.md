# UI/UX change plan

UI/UX Developer. Visual review of the preview desk at `localhost:4321` on 2026-09-19, and the plan to fix what it found. Standing contract: [design-system.md](../design-system.md) (**v2**) — replaced 2026-09-20 for the welcome ruling ([ui-ux-feedback.md](ui-ux-feedback.md)). v1 is [design-system-v1.md](../archive/design-system-v1.md). This plan’s Phases A–D implemented v1. **Phase E** implements v2. Do not implement Phase A harder. Routes and slugs are [web-design.md](../web-design.md) (Front-end Architect) and are not reopened here. Copy is [editorial-guidelines.md](../editorial-guidelines.md) (Content Editor). Front-end's remaining-work list is [web-app-execution-plan.md](web-app-execution-plan.md); this plan reorders its phases and says why.

Three words, once. A **sleeve** is one of the five topic families and the first segment of a URL. A **slice** is one citizen question on one stable URL. A **vintage** is one dated snapshot of observations, citations and caveats; a page binds to exactly one.

## Verdict

**The desk is honest and it is unreadable.** Every number is bound, every hole is a hole, no figure is typed in, and nothing on the page argues. Then a phone renders the chart axis labels at **3.2px**, a laptop puts the producer's name below the fold, a tablet bleeds a ten-digit census count **58px out of its own card**, and the token that colours "not published" fails WCAG AA at **3.09:1**. None of that is a taste disagreement. All of it is measurable, and none of it could fail the old presentation pass, because the old contract had no box that measured anything.

That is why this pass rewrites [design-system.md](../design-system.md) rather than amending it. The failures are not places where the desk drifted from the contract; they are places where the desk **obeyed** the contract. "The plot fills the card, SVG `width: 100%`" is the instruction that produces 3.2px labels. "`minmax(9.5rem, 1fr)`" with a fixed 2.75rem display figure is the instruction that produces the bleed. `--hole: #8A8A8A` is the token that fails AA. `--measure: 40rem | Unused for column width` is the line that authorises 124-character prose.

The look is not costumed as USAFacts and does not need rescuing from magenta. It needs to survive its own data.

## 1. Visual verdict against the contract

Measured with the browser at 360, 768 and 1440px on the four first screens. Boxes are the presentation-pass checklist in the rewritten [design-system.md](../design-system.md).

| Box | Home | C1 prices | C2 people | C3 money |
|-----|------|-----------|-----------|----------|
| House tokens, no costume | pass | pass | pass | pass |
| Type scale on headings, byline, figcaption, source-line | pass | fail | fail | fail |
| Measure (≤ 90 chars/line) | fail | fail | fail | fail |
| Stat fit at every width | n/a | pass | **fail** | **fail** |
| Chart legibility (no SVG text under 12px) | n/a | **fail** | **fail** | **fail** |
| One intrinsic plot width per page | n/a | **fail** | **fail** | **fail** |
| Chart well filled, no dead field | n/a | **fail** | **fail** | **fail** |
| Number agreement inside a chart | n/a | pass | **fail** | pass |
| Bars horizontal at house `barStep` | n/a | pass | pass | pass |
| Cite proximity (producer within 600px of `main`) | n/a | **fail** | **fail** | **fail** |
| Holes not shrunk or faded | n/a | **fail** | n/a | **fail** |
| Contrast (text 4.5:1, meaningful graphics 3:1) | pass | **fail** | pass | **fail** |
| Number is the hero | **fail** | pass | pass | pass |
| Screenshot test at readable size | n/a | fail | fail | fail |

What each failure actually is:

**Chart legibility — the worst one.** Charts are authored at ~1056px and the SVG carries `width: 100%`, so the browser scales the entire drawing. At a 360px viewport the well is 278px wide, the scale is 0.263, and every 12px axis label renders at **3.2px**. The C2 first chart becomes a 30px smear of blue lines under a figcaption three times its height. At 1440px the scale is 0.955, so even on a large desktop chart type sits at 11.5px, under the 12px floor the type scale declares. The 36-bar state chart at 360px gives each state row 5.9px. The old checklist box for this read "chart wells fill `--desk`; the plot fills the `--card`" — and it passed.

**Stat fit.** `1210854977` measures 251px at 2.75rem. At a 768px viewport `auto-fit` packs three 224px cells with 192px of content, so the figure bleeds 58px into its neighbour. The overflow exists on every viewport from about 368px to 929px — phones in landscape, every tablet, and small laptop windows. It only clears at 1440px, which is where the contract was written and checked. C3 has the same problem with `5347314.81`.

**Cite proximity.** No slice puts a citation card in the hero. The one-line `.source-line` sits at 729px on C2, below the fold on a 1366×768 laptop, and it arrives *after* the chart rather than with the figures. The full card — producer, series, reference period, release date, geography vintage, data vintage, caveat — sits at **4596px** on a 5706px page. The contract said "cite chrome in the same view" and "a tooltip is not enough", and then had no way to fail a page that put the cite six screens down. C2's source-line also omits the release date that C1's carries, so the compact line is not even the same four fields across slices.

**Contrast and holes.** `--hole: #8A8A8A` is 3.09:1 on `--paper` and 3.45:1 on `--card` — it fails AA for normal text, and it is the colour of the words that keep the page honest ("not published (no rural market in Chandigarh)", "unknown / not a table"). Worse, the scale renders a hole at 0.8125rem italic *inside* a 1.0625rem sentence, so the hole is smaller and fainter than the claim around it. The contract's own principle is "holes stay holes"; its own type table smooths them away. `--hole-band: #D9D9D9` is 1.28:1 and is also a cool grey in a warm stone house.

**Measure.** Running prose renders 1040px wide — **124 characters per line** at 1440px; the fact-lede is 119. `--measure: 40rem` has existed in the tokens since the beginning, explicitly marked "Unused for column width". Applying the token that is already there fixes this.

**Number agreement.** Inside the single C2 hero chart, the axis reads `200,000,000` and the bar beside it is labelled `833748852`. That is one drawing with two conventions, and it is independent of which convention the desk eventually picks: `render-chart.ts` hardcodes `format: ".2~f"` for bar value labels while the axis inherits Vega's default grouping.

**Type scale and heading order.** Section headings on all three slices are `<h3>`, restyled by CSS to the H2 size of 1.25rem. The page looks like a hierarchy it does not have, and a screen-reader user hears H1 jump to H3 with no H2 until "Methodology" at the very bottom.

**Plot widths.** C1 carries intrinsic widths 1050, 1056, 1057, 1058 and 1061 on one page; C3 carries 1056 through 1064; C2 carries 1047 and 1056. The fit pass in `render-chart.ts` corrects once, and correcting moves the axis labels, which moves the width. Because each SVG then scales by a slightly different factor into the same well, chart type sits at a slightly different size in each figure on the same page.

**Dead wells.** Every bar chart on all three slices reserves `valueLabelPad: 96` on the right whether the longest value label is `4.82` or `1210854977`. Measured unused right-hand space: 102–112px on C1, 99–120px on C2, 113–125px on C3 — about a tenth of every bar well is white field the chart never reaches. Line charts, which skip `applyBarPadding`, come in at 4–48px and are fine.

**Home fails "the number is the hero".** The desk home leads with a 36px mission sentence and then three full-width cards whose facts are set in `--muted` byline grey at 14px — the quietest style in the house. The grid has no `grid-template-columns`, so three cards stack as three paragraph blocks down a 1088px column. A fact desk is whispering its facts under a headline that contains no facts. This is the one place the live desk drifts toward a marketing homepage, and the fix is tokens, not copy.

**What passes and should be protected.** Navy `--mark` and the stone palette read institutional, not partisan. Chart titles are in HTML `figcaption`, not baked into Vega. Bars are horizontal at a house `barStep` that does not fatten with few categories. There is no magenta, no cream plot, no Aeonik, no wordmark, no search, no newsletter, no chat, no engagement SDK, no red–green, no league table on a non-rank slice. Every figure on every page carries `data-observation-id` and `data-vintage-id`. Holes render as holes. The skip link is the first focusable element. `--muted`, `--mark` and `--ink` all clear AA comfortably.

## 2. Decision: rewrite

**Rewrite, in place, this pass.** [design-system.md](../design-system.md) is still the only look file; there is no second memo and no parallel file.

The palette, the face, the tone and the forbids survive — the tokens still serve the vision. What changed:

- **A new opening rule: a rule that cannot be measured is not in this file.** Every presentation-pass box now names how it fails, with a number.
- **`--hole` `#8A8A8A` → `#6B6B6B`** (3.09 → 4.8 on paper). **`--hole-band` `#D9D9D9` → `#E3DFD8`**, warm. **New `--rule-strong` `#8C857A`** at 3.3 for any line that carries meaning; `--rule` stays light and is now explicitly decorative-only. The colour table carries a measured contrast column and a required minimum, so a reviewer can check the claim instead of trusting it.
- **A new `Fit` section.** Prose caps at `--measure` 40rem; stat rows, charts and cards keep `--desk`. `.stat` becomes a container query and the display figure becomes `clamp(1.75rem, 14.5cqi, 2.75rem)`, sized by its own cell, with `minmax(min(100%, 16rem), 1fr)` on the row. The clamp is derived so the widest plausible bound string — ten digits plus four separators — fits at every cell width the grid can produce, **including the ungrouped form**. One breakpoint at 48rem; no second breakpoint to solve a fit problem that `clamp` and `min()` solve.
- **A chart legibility floor.** `fitWidth` becomes 1008px, the real well width at `--desk`, so charts render 1:1 on a desktop. Below a 0.92 scale the well scrolls horizontally instead of shrinking type. Scrolling hides nothing and re-renders nothing; scaling to 3px hides everything.
- **Cite proximity becomes a number**: the producer name within 600px of the top of `main` at 1440×900, carried by a `.cite-strip` after the stat row and before the first chart, with all four summary fields required.
- **Holes inherit their sentence's size**; italic and colour are the whole encoding.
- **Heading order** is named: section headings are `<h2>`, fixed at bind, not with a CSS override.
- **Presentation pass runs on every template that reached Proof**, not only when chrome changed — because C2 and C3 changed no token and no stylesheet and both shipped a bleeding stat cell.
- **New primitives documented before use**: `.cite-strip` and `.preview-banner`.
- **The `Next` section is current.** It named three slices, said C1 is the only published one, and stopped telling a reader not to start C2.

## 3. Vision and the USAFacts role

The vision is "a shared, checkable picture of India that does not belong to a party, a ministry, or a news cycle."

**Where the look carries it.** *Shared* is served by one house on every slice — the same paper, the same navy, the same card. *Not belonging to a party* is served by refusing the tricolour, saffron/green, red–green, and any performance colour; a citizen cannot read approval or disapproval out of this page, because nothing on it is coloured by whether a number is good. *Not a news cycle* is served by the absence of scoops, a trending rail, engagement, and a byline that pretends to be reporting.

**Where the look breaks it.** *Checkable* is the word the desk currently fails. A picture is only checkable if the reader can see who published it while looking at the number, and today the producer is below the fold and the full provenance is six screens down. And *shared* fails on a phone: an Indian citizen reading on a 360px screen gets a chart they physically cannot read. A portrait that only resolves on a 1440px monitor is not shared.

**The USAFacts role, taken.** Question as H1, a bound fact-lede that answers it, then stats and charts, then method — the live tree has that shape and this plan does not touch it. Fast facts as one-liners and featured questions as rails are role, not costume, and both stay. An analysis byline beside the producer stays allowed.

**The role, not taken — and one place we accidentally took the wrong half.** No magenta, cream, Aeonik, wordmark, search, newsletter, chat, media desk, scoops. But the desk home currently takes the *shape* of a marketing homepage — a large mission statement over three cards — while dropping the thing that makes their homepage work as a fact desk: the fast fact is a **fact**, short and prominent. Ours is a full paragraph in the quietest grey in the house. The fix is to make the fact `--ink` body type in a real card grid, and to shorten it to one line (Front-end ruling R3, at bind). That is taking more of the role and none of the costume. A page that would pass for USAFacts with the wordmark swapped still fails; a page that whispers its facts fails differently.

## 4. Change plan

Owner is UI/UX Developer unless a handoff is named. Nothing here invents a URL, a slug, a title formula, or a preview-HTTP rule. Nothing here moves `data/pointers/citizen`.

**Reordered against [web-app-execution-plan.md](web-app-execution-plan.md), on purpose.** That plan runs the rail and the one-liner first (its items 3 and 5) and treats the first screen as Phase 2, on the reasoning that a presentation pass should run once against a structure that has stopped moving. I agree with the reasoning and disagree with the order. The rail and the one-liner change how the desk *connects*; fit, legibility and contrast decide whether any of it can be **read**. A sibling link from a chart nobody can see is not progress. So Phase A below is fit and legibility, and the Front-end items follow. No item is dropped and no ruling is refused.

### Phase A — Make the desk readable (UI/UX Developer)

Blocking. Nothing else is worth checking until these pass.

| # | Change | Files |
|---|--------|-------|
| A1 | `--hole` → `#6B6B6B`; `--hole-band` → `#E3DFD8`; add `--rule-strong` `#8C857A`; add `--break` to `cssVars` (it exists in `color` but never reaches `:root`) | `theme.ts` |
| A2 | `.observation-missing` inherits its sentence's size; keep italic and `--hole`. Drop the 0.8125rem override | `desk.css` |
| A3 | `.stat { container-type: inline-size; min-width: 0 }`; `.stat-figure { font-size: clamp(1.75rem, 14.5cqi, 2.75rem) }`; `.stat-row` → `repeat(auto-fit, minmax(min(100%, 16rem), 1fr))` | `desk.css` |
| A4 | Apply `--measure` to running prose, `.fact-lede p`, `.byline`, `.source-line`, `.fast-facts` one-liners and the current breadcrumb crumb. Keep `--desk` on `.stat-row`, `figure.chart`, `.citation-card`, header and footer. **Superseded 2026-09-20:** `--measure` is method prose only; hero is one `--desk` well (Phase E). Do not re-apply A4. | `desk.css` |
| A5 | `chart.fitWidth` 1056 → **1008**; iterate the fit pass until every chart on a page converges on one intrinsic width | `theme.ts`, `render-chart.ts` |
| A6 | Chart legibility floor: SVG keeps its intrinsic width down to a 0.92 scale, then `figure.chart` scrolls. `overflow-x: auto` is already there and is dead today because `max-width: 100%` never lets the SVG exceed the box | `desk.css`, `render-chart.ts` |
| A7 | One number format for axis labels and bar value labels, read from a single token — replace the hardcoded `format: ".2~f"` in `addBarValueLabels` | `theme.ts`, `render-chart.ts` |
| A8 | Derive `valueLabelPad` from the longest formatted label instead of a flat 96px, which leaves 99–125px of dead white on every bar well today | `render-chart.ts` |
| A9 | Axis domain and any meaningful line move from `--rule` to `--rule-strong`; grid stays `--rule` and stays decorative | `theme.ts` |

Acceptance: at 360, 480, 768, 1024 and 1440px — no `.stat-figure` wider than its cell's content box; no SVG text under 12px effective size; method paragraphs over 90 characters (hero is `--desk`, not this box); every chart on a page at one intrinsic width; `--hole` at 4.8:1.

### Phase B — Make the first screen checkable (UI/UX Developer, R7)

| # | Change | Files |
|---|--------|-------|
| B1 | Emit the first-screen cite as a `<details class="citation-card source-byline cite-strip">` inside `hero`, after the stat row and before the first chart. The templates already carry the `cite-view: first-screen` contract as a comment; this makes it a rendered element | `template_bind.py`, templates |
| B2 | Summary is always producer · series · reference period · released {date}. A missing field fails the render — C2's line omits the release date today | `template_bind.py` |
| B3 | `.cite-strip` styling: same well as the numbers, hero margins, 44px summary hit, producer `--ink`, rest `--muted`. Not a fifth panel style. **Amended 2026-09-20:** not an all-`--muted` codebook strip (Phase E). | `desk.css` |
| B4 | Section headings `<h3>` → `<h2>`; delete the `article.portrait > .cite-view h3` size override that was papering over it | `template_bind.py`, `desk.css` |

Acceptance: the producer name is within 600px of the top of `main` at 1440×900 on all three slices; the full cards are still in the bottom `.source-stack`; no new route, fragment or `/sources` per-slice page (R7).

### Phase C — Front-end's Phase 1, after the desk can be read

| # | Change | Owner | Files |
|---|--------|-------|-------|
| C1 | Hottest-rail siblings from `site.json` (R1): author hashes first, then up to three catalog siblings in charter order, current slice excluded, no empty group when there is no sibling | UI/UX | `cms_site.py` |
| C2 | Fast-facts and hub cards (R3/R4): `.fast-facts` gets a real grid, `repeat(auto-fit, minmax(min(100%, 20rem), 1fr))`; the one-liner becomes `--ink` body type, not `--muted` byline; per-card `data-vintage-id` from the card's own catalog entry | UI/UX | `desk.css`, `cms_site.py`, `index.astro`, `[sleeve]/index.astro` |
| C3 | 404 body (R2): one sentence, link to `/`, five sleeve links from `site.json`. Keeps `noindex`, keeps no `data-prism-path` | **Content Editor writes the sentence**, UI/UX implements | `404.astro` |
| C4 | `how-measured` (R10): the section renders today via `.cite-view[data-cite-view="how-this-is-measured"]`, so the styling is already right, but the `how-this-is-measured` layout token in `LAYOUT_BLOCKS` is never used and the documented `<section class="how-measured">` never appears. Make the contract and the DOM agree on one of them | UI/UX | `template_bind.py`, templates, `desk.css` |

Acceptance: as in the Front-end plan, plus the home fast-fact reads as a fact and not as a byline.

### Phase D — Named handoffs, not blocking

| # | Item | Owner |
|---|------|-------|
| D1 | Number grouping convention, Indian or Western, applied at bind so lede, stat cell, chart label and `meta description` are one string (R8). Phase A3 and A7 guarantee whichever string fits and stays consistent; they do not choose | Content Editor + bind |
| D2 | C2's "Updated not printed" byline wording (R11) | Content Editor, then Methodologist |
| D3 | Slot spacing artefacts — "the death rate was 6.4 ." — a space before the full stop after a bound slot on C2 | Content Editor + bind |
| D4 | C2's hero chart plots exactly the three figures in the stat row above it, with the same labels. Either it earns a dimension the stat row does not have, or the stat row is the chart | Content Editor (chart meaning), UI/UX (form factor) |
| D5 | Fold R1, R3, R4 into `web-design.md` as contract text | Front-end Architect |
| D6 | Preview banner (R5). Tokens specified in `design-system.md`: `.preview-banner`, `--card` on `--paper`, hairline `--rule`, `Preview · not published` plus the tree `vintage_id` in IBM Plex Mono 0.75rem, no link and no control inside it so the skip link stays the first focusable element, injected at serve and never in the citizen tree | Platform Architect |

### Phase E — Welcome ruling (UI/UX Developer)

Blocking on first-screen width and tone. Do not reopen A1–A3, A5–A9, or hole contrast. Direction: [ui-ux-feedback.md](ui-ux-feedback.md). Contract: [design-system.md](../design-system.md).

| # | Change | Files |
|---|--------|-------|
| E1 | First screen is one `--desk` well. Remove `--measure` from `.fact-lede`, `.byline`, `.source-line`, `.cite-strip`, `.fast-facts .fact`, and the current breadcrumb crumb. Shared left **and** right edge with `.stat-row` and `figure.chart`. | `desk.css` |
| E2 | `--measure` only on `.how-measured` running prose (and other method-only copy). A `.portrait-section` that contains a chart stays `--desk`. | `desk.css` |
| E3 | `.fact-lede` is the landing: `--card` at `--desk`, padding-block at least `--space-5`, 3px `--mark` **top** rule (not a narrow left-rule column), `--ink` type. | `desk.css` |
| E4 | `.cite-strip` sits after lede and stats, before the first chart, same width. Summary: producer `--ink`, rest `--muted`. Not a muted dump. | `desk.css`, `template_bind.py` if order differs |
| E5 | `.fast-facts .fact` is 1.25rem / 500 / `--ink`. Home’s designed moment is the fact grid, not a display-size H1. | `desk.css` |
| E6 | At 1440px the first-screen `figure.chart` must not show a horizontal scrollbar. Scroll remains the fallback below 0.92 scale. | `desk.css`, `render-chart.ts` if the well still shrinks type at desk width |

Acceptance: at 1440px, computed content widths of `.fact-lede`, `.stat-row`, `.cite-strip`, and the first `figure.chart` match within 1px; `.how-measured` paragraphs ≤ 90 characters; producer in `--ink` within 600px of `main`; no 12px-floor or stat-bleed regressions at 360 / 768 / 1440px.

## 5. Editorial visual-review gate

The gate was not real. Proof *mentioned* form factor in a trailing clause, and the sentence after it made the presentation pass conditional on "if chrome or charts changed". C2 and C3 changed no chrome and no chart code — they are new templates over the same house — so the pass was legitimately skippable, and it was skipped, and a bleeding stat cell and a 3.2px chart reached preview. The condition was wrong because form factor breaks at a new **data shape**, not at a new stylesheet.

Applied in this pass, inside the Content Editor passes section only:

- **[editorial-guidelines.md](../editorial-guidelines.md), pass 4 (Proof)** — the citizen read, the fail conditions and the copy forbids are untouched. The trailing clause becomes a required output: Proof *closes by naming* every form-factor break it saw, as a list handed to UI/UX Developer, and the sentence "naming a break is not fixing it" is made explicit — Content Editor does not restyle a chart, change a token, or reword a figure to make it fit. A chart whose labels are unreadable at the width you are reading is added to the examples, because that is the break the old list could not name.
- **[editorial-guidelines.md](../editorial-guidelines.md), the sentence after Proof** — the presentation pass becomes a required gate on every template that reaches Proof, recorded as skipped only when the same template renders the same page at the same vintage. It answers Proof's list and the design-system checklist and explicitly does not reopen sections, wording, or voice. Trust still follows, and still does not become a style editor.

Voice, scan-path *meaning*, and the copy forbids were not touched. Nothing outside lines 127–139 was touched.

Matching edits:

- **[design-system.md](../design-system.md) Presentation pass** — same trigger, plus a checklist where every box states how it fails.
- **[personas/ui-ux-developer.md](../personas/ui-ux-developer.md) Presentation pass** — same trigger and the expanded boxes; the output line now reads `skipped (same template, same page, same vintage)`.

## 6. Out of scope

Routes, slugs, `<title>` formulas, sitemap, `robots.txt`, canonical and preview-HTTP rules — Front-end Architect, [web-design.md](../web-design.md). Citizen questions, fact-ledes, chart titles, the 404 sentence, the "not printed" byline — Content Editor. The number-grouping convention — Content Editor and bind. Cites, dates, holes, spin, ship or block — Trust Auditor and Charter Editor; a visual failure is a house-look fail, not a missing cite, and this pass does not pass or block the record. Magenta, cream, Aeonik, a wordmark beyond the text lockup, search, newsletter, chat, social, an engagement SDK, dark mode, a mobile app — forbidden, not deferred. Pointer flips and `CITIZEN_ORIGIN` — Platform Architect. `data/pointers/citizen` is not touched by anything in this plan.

## 7. Output

```text
contract:            docs/design-system.md
tokens:              changed  (--hole #8A8A8A→#6B6B6B; --hole-band #D9D9D9→#E3DFD8;
                               + --rule-strong #8C857A; --measure applied; display figure
                               → clamp(1.75rem, 14.5cqi, 2.75rem); fitWidth 1056→1008)
primitives:          changed  (+ .cite-strip, + .preview-banner; .stat-row regrid;
                               .fast-facts regrid; section headings h3→h2)
template:            none bound this pass (plan + contract only)
vintage_id:          preview tree dv-20260919-87b702f1fd66
                     (C1 dv-20260916-234e263c8588 · C3 dv-20260918-846e99d0ca57)
preview:             localhost:4321 (unpublished desk)
published:           no (do not flip citizen_pointer)
cite_bound:          n/a this pass
refresh:             no
presentation_pass:   fail  (live desk: chart text at 3.2px on 360px; stat figure 58px
                            outside its cell at 768px; producer below the fold;
                            --hole at 3.09:1; prose at 124 characters)
next_persona:        ui-ux-developer (Phase E), then trust-auditor on preview
```
