# CMS system feedback

Charter Editor. Trust Auditor notes from Track C preview (2026-09-21), after C7, plus principal notes the same day against preview `http://localhost:4333` on `/money/union` and `/people/population`. Principal follow-up (2026-09-22): top-nav UI/UX, and who reviews chart layout vs copy vs look. Desk read (2026-09-22) after C6–C9 re-run: money magnitudes on `/money/union` wrong by orders (`0.35 Cr` for Budget BE revenue already stored as ₹ crore). This file routes them. It does not amend [editorial-guidelines.md](../editorial-guidelines.md), [content-editor.md](../personas/content-editor.md), [web-design.md](../web-design.md), [design-system.md](../design-system.md), or [data-contracts.md](../data-contracts.md) until the named owner acts.

Earlier batch: [citizen-page-feedback.md](citizen-page-feedback.md). Programme: [citizen-system-change-plan.md](citizen-system-change-plan.md). Charter rulings 1–9 in that file stand; compact Indian display is still ruling 6 — **reopened** by this-batch ruling 7 (`F-unit-system` / `F-money-crore-scale`).

```text
about:          preview desk C1–C3 vs desk tokens on the citizen method; numbering, cite chrome, method measure, C2 lede; top-nav ownership; chart review owners; house unit system (ingest→vintage→render)
source:         Trust C8 (four audits, last pass) + C9 accept-on-preview in citizen-system-change-plan.md; principal 2026-09-21 localhost:4333; principal 2026-09-22 nav + chart review; desk read 2026-09-22 money scale (desk-20260922-6dd1f6bafd5e)
forbids:        amending standing contracts from this file; flipping citizen_pointer
status:         F-unit-system / F-money-crore-scale open; F-site-header-nav open; F-chart-review-owners routed; stop before B3; citizen_pointer untouched
```

## Failure notes (from C8 / C9)

Quoted from [citizen-system-change-plan.md](citizen-system-change-plan.md). Routing only. `T-cite-period` is closed.

**C8 first audit** ([Trust audit](83437b7d-b1aa-4312-b07e-c5a616818c08)), desk of that pass. **block.** Closed on later vintages, not on `dv-20260918-846e99d0ca57`.

| Id | Fail (verbatim topic) | Status |
|----|-----------------------|--------|
| T-cess-zero | GST Compensation Cess on `dv-20260918-846e99d0ca57` is status `value` with value `0.0` | Closed: C3 mapper `c3-observations-1.2.0`; vintage `dv-20260921-1fa96ad12e48` is `unknown` / null; no bar. Do not mutate the blocked vintage. Pipeline Engineer. |
| T-cite-desk-caveat | Cite cards print desk `caveat_one_line` (ingest flags, Card N, do not…) | Closed as dump: librarian `caveat_one_line`; projector does not dump ingest flags. Still fail if a card reprints them (`T-c8-surface`). Source Librarian; Platform Architect. |

**C8 re-audit after C3 vintage + librarian + C7** ([Trust audit](d5097240-d303-4c1f-b8ba-2d1684e42310)), `desk-20260921-2f93be5c9ccc`. **block.**

| Id | Fail (verbatim topic) | Status |
|----|-----------------------|--------|
| T-lags-slot | `/people/population` Methodology prints vintage lags (`next_release unknown — delayed…`) via slot `caveat-pca-lags` | Closed on `desk-20260921-c4bb12ee6821`. Content Editor; Platform Architect. |
| T-this-desk | Same page Method details: “There is no later census total on this desk.” from `citizen_note` | Closed on that desk (`citizen_note` is “There is no later census total.”). Methodologist. |

Notes on that pass (not extra fails): C3 tax-by-major-head keeps GST Compensation Cess as unknown / not published (no bar); **IGST is a printed zero**; FRBM gap is “not published”; cites are producer URLs.

**C8 re-audit after C1 cite-period split** ([Trust audit](23f4cc09-5642-4597-851c-41e66fb8d70a)), live preview bind (desk `desk-20260921-c4bb12ee6821` identity; vintages C1 `dv-20260921-6a5d23d42462`, C2 `dv-20260921-617d0e9cf03f`, C3 `dv-20260921-1fa96ad12e48`). **pass.** C9 accepted Track C on preview. `citizen_pointer` does not move.

| Id | Fail (verbatim topic) | Status |
|----|-----------------------|--------|
| T-cite-period | One catalog cite printed 2026-07 while the bound answer is August 2026 (Provisional) | Closed: two `CitizenCite` cards (`--2026-08` and `--2026-07`); in-text and strip are August. Platform Architect. |

C9: Track C accepted on preview. Catalog B3 still out. F- rows below remain.

## Charter rulings (this batch)

1. **One Indian display string, no leftover producer unit.** Compact K / L / Cr (ruling 6) is the *whole* citizen unit. Fail `"35.27 L crore"` and `"14.23 L Thousand"`: the scale token must not sit next to the vintage `unit` word. Population counts on that page use **Cr**, same concept, same scale. Grouping is Indian (12,34,56,789 or compact Cr/L/K). Vintage `unit` stays as printed.

2. **Cite line opens a panel; the card stays on the page.** First-screen cite and every chart `.source-line` may look like the compact source-line. The control opens the existing in-text cite `popover` (P3). `.source-stack` still holds the full cards. Do not add `/cite`. Do not leave the view. Do not drop a producer that is not already named next to a figure.

3. **Source-stack is the complete list.** “Sources on this page” may list **every** cite the answer-page uses, including those already named in the fact-lede or immediately after a chart. Completeness at the bottom is in. Do not treat an earlier in-text or chart source-line as a reason to omit the card from the stack. Those lines are the same panel control.

4. **Method is quiet by type, not by a second column.** Fine-print (smaller than answer body). Same `--desk` left/right edge as other sections. `--measure` on `.how-measured` yields. Quietness is size and placement after the record, not a narrower well.

5. **C2 fact-lede for a 2026 reader.** The first number answers “how many people live in India” with the official **projection for the current year, named as a projection**. Census 2011 stays on the same first screen as the last enumerated Total (stat row or the next sentence). Do not treat the projection as a census count. Do not treat 2011 as today. Methodologist signs the wording.

6. **Axis ticks are citizen period labels.** Census years are years (1901…2011), not producer footnote marks (`$`, `@`, `#`, `+`). Budget charts do not print machine prefixes (`end-`, `actual-`). Footnotes and BE/RE/Actuals live in method or the cite, not in the tick.

7. **One house unit system; drop `DisplayScale`.** Ingest, vintage, and render must share one **standard Indian numbering** contract (ones / thousand / lakh / crore as magnitudes of the *same* base). Observation `value` + denomination are the record; render **formats** for display (Indian digit grouping, compact K / L / Cr labels) and must not re-interpret magnitude by guessing a second scale from page peaks. **`DisplayScale` / `scale_for_concept` / `apply_scale` that divide already-crore (or already-thousand) values as if they were ones are out.** Fail `/money/union` showing Budget BE revenue as `0.35 Cr` when the vintage holds `~3.5e6` ₹ crore. Vintage `unit` stays as the producer printed it; citizen chrome never reprints leftover “crore of rupees” beside a scale token (ruling 1 still). Platform Architect owns the contract; Pipeline and Ingest keep denomination honest; Methodologist signs denomination notes; Trust fails wrong order-of-magnitude on ship.

## By persona

### Content Editor

| Id | Feedback | Also |
|----|----------|------|
| T-lags-slot | `/people/population` Methodology printed desk `lags` via slot `caveat-pca-lags` (“About fifteen years behind a 2026 reader. next_release unknown — delayed…”). Do not bind CaveatNote desk fields (`lags`, `do_not`, codebook `concept`, Frame, Card N, parser flags) into method or running copy. Write citizen sentences. | Platform Architect (projection); Methodologist |
| T-this-desk | Method details printed “There is no later census total on this desk.” from `citizen_note`. Citizen copy must not say “this desk”, “on this desk”, `next_release`, or catalog tokens. | Methodologist (`citizen_note`) |
| T-parked | Method said “Districts are parked.” Catalog talk. Same as P5 desk sentences. | Methodologist (`do_not` stays desk) |
| T-c8-surface | C8 done-when: no desk field, parser name, Frame label, or `do_not` on the page. Cite cards must not dump ingest flags, Card N, or `do_not`. | Platform Architect (projection) |
| T-cite-period | `/prices/retail-prices`: source-stack cards `cite-c1-cpi-general-base-2024-2026-08` and `cite-c1-cpi-cfpi-base-2024-2026-08` print 2026-07 while the bound answer is August 2026 (Provisional). Closed: two cards; slot still must not name a month the card does not carry. | Platform Architect (projection) |
| F-indic-unit | `/money/union` fact-lede printed `35.27 L crore of rupees` (compact L plus leftover “crore”). Template must not append vintage `unit` after `DisplayValue.display_string`. Same fail on “What liabilities are outstanding?” `.stat-row` and the liabilities chart. Indian grouping / one compact scale, ruling 6 and this-batch ruling 1. | **Closed as string dump (Platform, 2026-09-21).** Magnitude integrity reopened as `F-money-crore-scale` / `F-unit-system` (ruling 7). |
| F-money-crore-scale | `/money/union` on `desk-20260922-6dd1f6bafd5e`: Budget BE revenue receipts **`~3.5e6` ₹ crore** in the vintage display as **`0.35 Cr`**. Liabilities peak (`~2.1e7` ₹ crore) forces shared `money-crore` concept onto `DisplayScale.Cr`, then `apply_scale` divides by `1e7` as if values were ones. Ingest is not wrong. Fail any page that shrinks already-denominated magnitudes by a second scale. | Platform Architect (drop `DisplayScale`); Pipeline Engineer; Methodologist; Trust Auditor |
| F-unit-system | Establish one **Indian numbering** unit system every stage understands: ingest writes denomination with the value; vintage stores it; render formats only (grouping / compact label). Do not invent a bind-time scale enum that re-bases producer crore or thousand amounts. Replace `DisplayScale` / peak-driven `scale_for_concept` with that contract. | Platform Architect (lead); Ingest Engineer; Pipeline Engineer; Methodologist; UI/UX (chrome only); Trust Auditor |
| F-c2-lakh-thousand | `/people/population` “What does the official projection print?” stats and the following chart y-axis as `14.23 L Thousand`. Same concept as the census counts: display **Cr**, Indian numbering, no “Lakh Thousands”. Do not leave producer “thousand” next to scale L. | **Closed (Platform, 2026-09-21):** thousands → persons before scale; shared `headcount` concept with census → **Cr**; template dropped `thousand people`. Method note for joining units still Methodologist. |
| F-c2-lede-year | `/people/population` fact-lede still leads with Census 2011 Total in 2026. This-batch ruling 5: lead with the official projection for the current year, **named as a projection**; keep 2011 on the same first screen as the last enumerated Total. Slots, not a pasted 2026 figure. | **Closed (Content Editor, 2026-09-21):** lede leads with NCP 2026 projection named as projection; 2011 Total remains on first screen. |
| F-census-axis-marks | Chart “India Total, census years 1901 to 2011” x-axis carries producer footnote marks (`1901 $`, `1951 @`, `1981 #`, `1991 +`, `2001 ++`). Tick text is the year. Spec `sort` must not be those marks. Footnotes belong in method / the cite. | **Closed (Pipeline + UI/UX, 2026-09-21):** `period_label` on chart rows; VL `sort` is plain years; marks stay on `reference_period` for bind. |
| F-axis-period-prefix | `/money/union` “Outstanding liabilities, Central Government” x-axis `end-[year1-year2]`; “Revenue receipts in this Budget book” `actual-[year1-year2]`. Citizen ticks are the year labels. Prefixes are period keys. | **Closed (Pipeline + Platform + UI/UX, 2026-09-21):** `citizen_period_label` / `period_label`; liabilities and receipts charts encode `period_label`. |
| F-method-fineprint | Methodology: quieter copy after the record. Do not restyle; do not reopen a second “How to read” block. Type and width are UI/UX (this-batch ruling 4). | **Closed (UI/UX, 2026-09-21):** method body 0.9375rem `--muted` at `--measure`; H2 already 1.4× quieter. |
| F-chart-review-owners | Chart **content** on answer pages: titles, axis meaning in citizen words, what the figure answers, first-screen vs method. Layout, type size, real-estate, and visual appeal are not this pass — hand those to UI/UX. Do not restyle. | UI/UX Developer (presentation); Methodologist (breaks / meaning) |

### Methodologist

| Id | Feedback | Also |
|----|----------|------|
| T-this-desk | `citizen_note` on caveat-c2-census-2011-pca-sd said “on this desk.” Citizen note says what the number is, never the desk. | Content Editor |
| F-c2-lede-year | Sign citizen wording that a 2026 NCP figure is a **projection**, not a census headcount, and that 2011 is the last enumerated Total. Content Editor cannot put the projection in the lede without that note. | **Signed (2026-09-21).** See [c2-method-notes.md](c2-method-notes.md). Content Editor; Trust Auditor |
| F-c2-lakh-thousand | Producer unit of the projection series is thousands of persons. Display compact Cr is bind, not a new observation. Do not join census persons and projection thousands without the unit note in method. | Content Editor; Platform Architect; UI/UX Developer |
| F-census-axis-marks | Census 2011 A-02 footnote marks on selected years stay on the desk / citizen caveat, not as axis text. | Content Editor; Pipeline Engineer |
| F-unit-system | Sign denomination vocabulary for the house unit system (ones / thousand / lakh / crore of what — persons vs ₹). Citizen method may name producer denomination; it must not invent a second magnitude. | Platform Architect; Pipeline Engineer |
| F-money-crore-scale | Budget ₹ crore columns stay crore of rupees as printed. Compact citizen form is Indian numbering of that crore amount (e.g. lakh crore), never a second ÷10⁷ on the crore figure. | Platform Architect |

### UI/UX Developer

| Id | Feedback | Also |
|----|----------|------|
| F-lede-inline-type | Bound numbers inside running `<p>` (fact-lede and evidence) at **body size**, highlighted (weight; underline only if it cannot look like a link). Do not enlarge `.observation-value` in prose to `.stat-figure`. No magenta `span.answer`. Stat chips stay large. | **Closed (UI/UX, 2026-09-21):** prose `.observation-value` inherits body size; `.stat-figure` keeps clamp. |
| F-cite-line-panel | First-screen citation-card should match other source-line chrome: one line, control opens the cite `popover`. On-page `.source-stack` cards remain (this-batch ruling 2, P3). Amend Interaction in [design-system.md](../design-system.md) if the strip’s open state moves from `<details>` to the panel. No fly-out that leaves the view. | **Closed (UI/UX, 2026-09-21):** cite-strip is a button → `popover`; `data-citation-id` on the control; stack cards stay `<details>`. |
| F-source-line-panel | Every `.source-line` immediately after a chart is the same panel control for that observation’s card. | **Closed (UI/UX, 2026-09-21):** source-lines that carry a cite open the same panel; lines without a cite stay `<p>`. |
| F-source-stack | On-page `.source-stack` lists every cite the answer-page uses (this-batch ruling 3). Same panel control as the strip and chart source-lines. Do not invent a third cite chrome. | Front-end Architect |
| F-method-fineprint | Method as fine-print: smaller than answer body; method H2 already 1.4× quieter. Same `--desk` width as other sections (this-batch ruling 4). Amend [design-system.md](../design-system.md) `--measure` on `.how-measured`. | **Closed (UI/UX, 2026-09-21):** see Charter Editor table. |
| F-indic-unit | Lede, `.stat-row`, and chart axes: one Indian `display_string`. Presentation pass fails mixed `L` + “crore” and ungrouped ten-digit rupees. Compact-units box still: ticks ≤ 9 characters, same scale as the stat row. | Platform Architect; Content Editor |
| F-unit-system | After Platform names the house unit formatters: presentation fails ticks/labels that still assume `DisplayScale` peak logic or leftover producer unit words. Do not invent denomination. | Platform Architect |
| F-c2-lakh-thousand | Projection chart y-axis in Cr, same as the page’s population counts. Fail “Lakh Thousands”. | Content Editor; Platform Architect |
| F-census-axis-marks | Census line chart: x-axis years, no special-symbol ticks. | **Closed:** see Charter Editor table. |
| F-axis-period-prefix | Drop `end-` / `actual-` from axis ticks. | **Closed:** see Charter Editor table. |
| F-chart-left-gap | `/money/union` “Tax by major head, Budget Estimates 2026-27” and “What the Union collects and spends, Budget Estimates 2026-27”: unused white field to the **left** of the plot. Plot fills the card (`valueLabelPad` / well filled). Same as P4. | **Closed (UI/UX, 2026-09-21):** dropped oversized `labelLimit`; categorical axis `maxExtent` capped so the plot fills the card. |
| F-site-header-nav | Principal: work the look of the top navigation bar. After Front-end signs IA (or confirms the standing sleeve header), run presentation on `.site-header` / `.sleeve-nav` against [design-system.md](../design-system.md) (tokens, type, 44px hits, header rule, `--desk` shell). Do not invent a second nav tree. | Front-end Architect (IA first) |
| F-chart-review-owners | Principal: who reviews answer-page charts for layout, font, real-estate, visual appeal? **This persona** — named presentation pass against [design-system.md](../design-system.md) (chart wells fill `--desk`, plot fills `--card`, 12px SVG floor, one `plotWidth`, house type). Not Trust taste. Not Front-end inventing chrome. Content stays Content Editor. | Content Editor (titles / labels); Methodologist (breaks) |

### Front-end Architect

| Id | Feedback | Also |
|----|----------|------|
| F-cite-line-panel | Cite chrome is not a route ([web-design.md](../web-design.md)). Panel mirrors the on-page card. Sign only if IA would otherwise be invented — it must not. | UI/UX Developer |
| F-source-line-panel | Same: in-page panel, not `/cite`. | UI/UX Developer |
| F-source-stack | `/sources` stays the house producer index, never a per-slice dump. The complete slice cite list stays on the slice URL (this-batch ruling 3). | UI/UX Developer |
| F-site-header-nav | Principal: should we work UI/UX of the top nav? **IA first.** Header architecture (Prism lockup → `/`, five sleeve links, wrap, hub quiet-empty) lives in [web-design.md](../web-design.md). Sign whether the standing shell is enough or needs an IA change. Do not invent tokens or chart chrome. Hand look of `.site-header` to UI/UX only after that sign. | UI/UX Developer |

### Source Librarian

| Id | Feedback | Also |
|----|----------|------|
| T-cite-desk-caveat | Closed as dump: citizen `caveat_one_line` is one readable paragraph, not ingest flags, Card N, or `do_not`. Still fail a reprint (`T-c8-surface`). | Platform Architect |

### Platform Architect

| Id | Feedback | Also |
|----|----------|------|
| T-lags-slot | `caveat_field` must not project desk fields (`lags`, `do_not`, Frame, parser flags) onto the page. | Content Editor (do not name those slots) |
| T-cite-period | Closed: one catalog id, two `CitizenCite` periods. Still fail if one HTML id stands for July and August. | Content Editor (which cite id the slot names) |
| F-indic-unit | `DisplayValue.display_string` is the only citizen number string. Bind must not concatenate scale + vintage `unit`. One `display_scale` per (page, concept). | **Landed as string dump (2026-09-21).** Peak-driven `DisplayScale` still wrong for money — see `F-money-crore-scale` / `F-unit-system`. |
| F-money-crore-scale | Open: shared `money-crore` + `scale_for_concept` peak ≥ `CRORE` (1e7) from liabilities → `DisplayScale.Cr` → `apply_scale` ÷1e7 on already-₹-crore values → BE revenue `0.35 Cr`. Evidence: vintage `dv-20260921-1fa96ad12e48` holds `3526840` ₹ crore; intended compact form is Indian numbering of that crore amount (e.g. `35.27 L Cr`), not a second crore conversion. | Pipeline Engineer; Methodologist; Trust Auditor |
| F-unit-system | **Lead.** Name one house unit system (Indian numbering) ingest + vintage + render share. Remove `DisplayScale` / `scale_for_concept` / `apply_scale` re-basing. Observation keeps producer magnitude + denomination; render formats only. Amend [data-contracts.md](../data-contracts.md) when the contract lands. Do not flip `citizen_pointer` from this file. | Ingest Engineer; Pipeline Engineer; Methodologist; UI/UX Developer; Trust Auditor |
| F-c2-lakh-thousand | Projection and census headcount are one concept on `/people/population`: one scale, **Cr**. Producer thousands stay on `unit`. | **Landed (2026-09-21).** Shared `headcount` concept; thousands → persons at bind. Revisit under `F-unit-system` so headcount and money use the same numbering rules without peak cross-talk. |
| F-cite-line-panel | Control carries `citation_id` so the `popover` mirrors `CitizenCite`. No request-time fetch. | UI/UX Developer |
| F-axis-period-prefix | Citizen period label on chart rows is the year (or BE/RE/Actuals phrase), not the vintage period key. | Pipeline Engineer; UI/UX Developer |

### Ingest Engineer

| Id | Feedback | Also |
|----|----------|------|
| F-unit-system | Derived cells keep the producer’s magnitude and denomination (₹ crore stays crore of rupees; thousands stay thousands). Do not “normalize to ones” at ingest unless Methodologist signs a new observation. Accuracy gate still: hole ≠ zero. | Platform Architect; Pipeline Engineer; Methodologist |

### Pipeline Engineer

| Id | Feedback | Also |
|----|----------|------|
| T-cess-zero | Closed on `dv-20260921-1fa96ad12e48`: GST Compensation Cess BE 2026-27 is `unknown` / null, never plotted as `0.0`. Do not mutate `dv-20260918-846e99d0ca57`. IGST printed zero is a published zero, not this hole. | Trust Auditor |
| F-indic-unit | Observation `unit` stays as the producer printed it. Display scale is bind, not a rewritten Parquet unit. | Platform Architect |
| F-money-crore-scale | Confirm Budget / CGA / Finance Accounts ₹ crore columns map as crore-denominated values (not rupees). Do not rewrite Parquet to “fix” display. | Platform Architect; Ingest Engineer |
| F-unit-system | Mapper families emit denomination with the value so render never guesses. Shape-named mappers; no C-number unit specials. | Platform Architect; Ingest Engineer; Methodologist |
| F-c2-lakh-thousand | Projection series unit (thousands of persons) on the observation so bind can scale to Cr without guessing. | Methodologist; Platform Architect |
| F-census-axis-marks | Chart category / `reference_period` for the citizen row is the census year, not `1901 $`. Footnote flags stay in lineage or the caveat, not the tick. | Methodologist; Content Editor |
| F-axis-period-prefix | Do not copy `end-2024-25` / `actual-2024-25` keys into bound chart labels. | Platform Architect; UI/UX Developer |

### Trust Auditor

C8 done-when still: dates match the vintage; no desk field, parser name, Frame label, or `do_not` on the page; no hole plotted as zero; cites open producer URLs.

Closed on live preview bind (C8 pass): C1 July vs August (`T-cite-period`); C2 method leak (`T-lags-slot`, `T-this-desk`); cess hole (`T-cess-zero`); desk cite dump (`T-cite-desk-caveat`). Notes, not fails: IGST printed zero; FRBM **not published**; producer URLs; no default rank, no red–green, no spin.

Next citizen-facing preview: fail wrong **order of magnitude** on money or headcount (`F-money-crore-scale` — e.g. Budget crore amounts shown as `0.35 Cr`); fail `L crore` / `L Thousand` string dumps (`F-indic-unit`, `F-c2-lakh-thousand`). Form-factor (inline type, method fine-print, left-gap on bars, source-line chrome, chart real-estate, header chrome) is **not** Trust. Unit-system redesign (`F-unit-system`) is Platform’s contract — Trust fails the citizen wrong number, not the enum name.

## Multi-party items (this batch, lead first)

| Item | Lead | Parties |
|------|------|---------|
| C1 cite period matches the observation (or two cards); no July card for August | Closed (C8 pass / C9) | Content Editor, Trust Auditor |
| One Indian `display_string`; no L+crore / Lakh Thousands; population in Cr | Platform Architect | Content Editor, UI/UX Developer, Pipeline Engineer, Methodologist, Trust Auditor |
| House unit system (Indian numbering); drop `DisplayScale`; money crore scale (`F-unit-system`, `F-money-crore-scale`) | Platform Architect | Ingest Engineer, Pipeline Engineer, Methodologist, UI/UX Developer, Trust Auditor, Charter Editor (ruling 7) |
| Inline `<p>` numbers at body size, highlighted | UI/UX Developer | Content Editor |
| Cite-strip and chart source-lines → panel; card remains | UI/UX Developer | Front-end Architect, Platform Architect, Content Editor |
| Source-stack lists every cite used on the answer-page | UI/UX Developer | Front-end Architect |
| Method fine-print, `--desk` width | UI/UX Developer | Content Editor, Charter Editor (ruling 4) |
| C2 lede: current-year projection, named; 2011 still on first screen | Content Editor | Methodologist, Charter Editor (ruling 5), Trust Auditor |
| Census year ticks without footnote marks | Pipeline Engineer | Content Editor, Methodologist, UI/UX Developer |
| Budget axis without `end-` / `actual-` | Pipeline Engineer | Platform Architect, UI/UX Developer, Content Editor |
| Bar charts: fill leftover left field | UI/UX Developer | — |
| Top nav: IA then look (`F-site-header-nav`) | Front-end Architect | UI/UX Developer |
| Answer charts: content vs form-factor (`F-chart-review-owners`) | UI/UX Developer (layout / font / real-estate / appeal) | Content Editor (titles / labels); Methodologist (breaks); Trust Auditor (cites / holes / spin only) |
