# CMS system feedback

Charter Editor. Trust Auditor notes from Track C preview (2026-09-21), after C7, plus principal notes the same day against preview `http://localhost:4333` on `/money/union` and `/people/population`. This file routes them. It does not amend [editorial-guidelines.md](../editorial-guidelines.md), [content-editor.md](../personas/content-editor.md), or [design-system.md](../design-system.md) until the named owner acts.

Earlier batch: [citizen-page-feedback.md](citizen-page-feedback.md). Programme: [citizen-system-change-plan.md](citizen-system-change-plan.md). Charter rulings 1–9 in that file stand; compact Indian display is still ruling 6.

```text
about:          preview desk C1–C3 vs desk tokens on the citizen method; numbering, cite chrome, method measure, C2 lede
source:         Trust C8 (four audits, last pass) + C9 accept-on-preview in citizen-system-change-plan.md; principal 2026-09-21 localhost:4333
forbids:        amending standing contracts from this file; flipping citizen_pointer
status:         routing only; T-cite-period closed
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

## By persona

### Content Editor

| Id | Feedback | Also |
|----|----------|------|
| T-lags-slot | `/people/population` Methodology printed desk `lags` via slot `caveat-pca-lags` (“About fifteen years behind a 2026 reader. next_release unknown — delayed…”). Do not bind CaveatNote desk fields (`lags`, `do_not`, codebook `concept`, Frame, Card N, parser flags) into method or running copy. Write citizen sentences. | Platform Architect (projection); Methodologist |
| T-this-desk | Method details printed “There is no later census total on this desk.” from `citizen_note`. Citizen copy must not say “this desk”, “on this desk”, `next_release`, or catalog tokens. | Methodologist (`citizen_note`) |
| T-parked | Method said “Districts are parked.” Catalog talk. Same as P5 desk sentences. | Methodologist (`do_not` stays desk) |
| T-c8-surface | C8 done-when: no desk field, parser name, Frame label, or `do_not` on the page. Cite cards must not dump ingest flags, Card N, or `do_not`. | Platform Architect (projection) |
| T-cite-period | `/prices/retail-prices`: source-stack cards `cite-c1-cpi-general-base-2024-2026-08` and `cite-c1-cpi-cfpi-base-2024-2026-08` print 2026-07 while the bound answer is August 2026 (Provisional). Closed: two cards; slot still must not name a month the card does not carry. | Platform Architect (projection) |
| F-indic-unit | `/money/union` fact-lede printed `35.27 L crore of rupees` (compact L plus leftover “crore”). Template must not append vintage `unit` after `DisplayValue.display_string`. Same fail on “What liabilities are outstanding?” `.stat-row` and the liabilities chart. Indian grouping / one compact scale, ruling 6 and this-batch ruling 1. | Platform Architect (`DisplayValue`); UI/UX Developer (axes and stat chrome); Pipeline Engineer (`unit` on the observation) |
| F-c2-lakh-thousand | `/people/population` “What does the official projection print?” stats and the following chart y-axis as `14.23 L Thousand`. Same concept as the census counts: display **Cr**, Indian numbering, no “Lakh Thousands”. Do not leave producer “thousand” next to scale L. | Methodologist (producer unit); Platform Architect (scale per concept); UI/UX Developer (axis); Pipeline Engineer |
| F-c2-lede-year | `/people/population` fact-lede still leads with Census 2011 Total in 2026. This-batch ruling 5: lead with the official projection for the current year, **named as a projection**; keep 2011 on the same first screen as the last enumerated Total. Slots, not a pasted 2026 figure. | Methodologist (projection ≠ count); Charter Editor (ruling 5); Trust Auditor |
| F-census-axis-marks | Chart “India Total, census years 1901 to 2011” x-axis carries producer footnote marks (`1901 $`, `1951 @`, `1981 #`, `1991 +`, `2001 ++`). Tick text is the year. Spec `sort` must not be those marks. Footnotes belong in method / the cite. | Methodologist; Pipeline Engineer (citizen period label); UI/UX Developer (axis) |
| F-axis-period-prefix | `/money/union` “Outstanding liabilities, Central Government” x-axis `end-[year1-year2]`; “Revenue receipts in this Budget book” `actual-[year1-year2]`. Citizen ticks are the year labels. Prefixes are period keys. | Pipeline Engineer; Platform Architect (citizen period); UI/UX Developer |
| F-method-fineprint | Methodology: quieter copy after the record. Do not restyle; do not reopen a second “How to read” block. Type and width are UI/UX (this-batch ruling 4). | UI/UX Developer |

### Methodologist

| Id | Feedback | Also |
|----|----------|------|
| T-this-desk | `citizen_note` on caveat-c2-census-2011-pca-sd said “on this desk.” Citizen note says what the number is, never the desk. | Content Editor |
| F-c2-lede-year | Sign citizen wording that a 2026 NCP figure is a **projection**, not a census headcount, and that 2011 is the last enumerated Total. Content Editor cannot put the projection in the lede without that note. | Content Editor; Trust Auditor |
| F-c2-lakh-thousand | Producer unit of the projection series is thousands of persons. Display compact Cr is bind, not a new observation. Do not join census persons and projection thousands without the unit note in method. | Content Editor; Platform Architect; UI/UX Developer |
| F-census-axis-marks | Census 2011 A-02 footnote marks on selected years stay on the desk / citizen caveat, not as axis text. | Content Editor; Pipeline Engineer |

### UI/UX Developer

| Id | Feedback | Also |
|----|----------|------|
| F-lede-inline-type | Bound numbers inside running `<p>` (fact-lede and evidence) at **body size**, highlighted (weight; underline only if it cannot look like a link). Do not enlarge `.observation-value` in prose to `.stat-figure`. No magenta `span.answer`. Stat chips stay large. | Content Editor (Proof names the break; does not restyle) |
| F-cite-line-panel | First-screen citation-card should match other source-line chrome: one line, control opens the cite `popover`. On-page `.source-stack` cards remain (this-batch ruling 2, P3). Amend Interaction in [design-system.md](../design-system.md) if the strip’s open state moves from `<details>` to the panel. No fly-out that leaves the view. | Front-end Architect (refuse a new page type); Platform Architect (`citation_id` on the control); Content Editor (which cite the strip names) |
| F-source-line-panel | Every `.source-line` immediately after a chart is the same panel control for that observation’s card. | Front-end Architect (not a route); Platform Architect |
| F-source-stack | On-page `.source-stack` lists every cite the answer-page uses (this-batch ruling 3). Same panel control as the strip and chart source-lines. Do not invent a third cite chrome. | Front-end Architect |
| F-method-fineprint | Method as fine-print: smaller than answer body; method H2 already 1.4× quieter. Same `--desk` width as other sections (this-batch ruling 4). Amend [design-system.md](../design-system.md) `--measure` on `.how-measured`. | Content Editor (placement) |
| F-indic-unit | Lede, `.stat-row`, and chart axes: one Indian `display_string`. Presentation pass fails mixed `L` + “crore” and ungrouped ten-digit rupees. Compact-units box still: ticks ≤ 9 characters, same scale as the stat row. | Platform Architect; Content Editor |
| F-c2-lakh-thousand | Projection chart y-axis in Cr, same as the page’s population counts. Fail “Lakh Thousands”. | Content Editor; Platform Architect |
| F-census-axis-marks | Census line chart: x-axis years, no special-symbol ticks. | Content Editor; Pipeline Engineer |
| F-axis-period-prefix | Drop `end-` / `actual-` from axis ticks. | Pipeline Engineer; Content Editor |
| F-chart-left-gap | `/money/union` “Tax by major head, Budget Estimates 2026-27” and “What the Union collects and spends, Budget Estimates 2026-27”: unused white field to the **left** of the plot. Plot fills the card (`valueLabelPad` / well filled). Same as P4. | — |

### Front-end Architect

| Id | Feedback | Also |
|----|----------|------|
| F-cite-line-panel | Cite chrome is not a route ([web-design.md](../web-design.md)). Panel mirrors the on-page card. Sign only if IA would otherwise be invented — it must not. | UI/UX Developer |
| F-source-line-panel | Same: in-page panel, not `/cite`. | UI/UX Developer |
| F-source-stack | `/sources` stays the house producer index, never a per-slice dump. The complete slice cite list stays on the slice URL (this-batch ruling 3). | UI/UX Developer |

### Source Librarian

| Id | Feedback | Also |
|----|----------|------|
| T-cite-desk-caveat | Closed as dump: citizen `caveat_one_line` is one readable paragraph, not ingest flags, Card N, or `do_not`. Still fail a reprint (`T-c8-surface`). | Platform Architect |

### Platform Architect

| Id | Feedback | Also |
|----|----------|------|
| T-lags-slot | `caveat_field` must not project desk fields (`lags`, `do_not`, Frame, parser flags) onto the page. | Content Editor (do not name those slots) |
| T-cite-period | Closed: one catalog id, two `CitizenCite` periods. Still fail if one HTML id stands for July and August. | Content Editor (which cite id the slot names) |
| F-indic-unit | `DisplayValue.display_string` is the only citizen number string. Bind must not concatenate scale + vintage `unit`. One `display_scale` per (page, concept). | UI/UX Developer; Content Editor; Pipeline Engineer |
| F-c2-lakh-thousand | Projection and census headcount are one concept on `/people/population`: one scale, **Cr**. Producer thousands stay on `unit`. | Methodologist; Content Editor; UI/UX Developer |
| F-cite-line-panel | Control carries `citation_id` so the `popover` mirrors `CitizenCite`. No request-time fetch. | UI/UX Developer |
| F-axis-period-prefix | Citizen period label on chart rows is the year (or BE/RE/Actuals phrase), not the vintage period key. | Pipeline Engineer; UI/UX Developer |

### Pipeline Engineer

| Id | Feedback | Also |
|----|----------|------|
| T-cess-zero | Closed on `dv-20260921-1fa96ad12e48`: GST Compensation Cess BE 2026-27 is `unknown` / null, never plotted as `0.0`. Do not mutate `dv-20260918-846e99d0ca57`. IGST printed zero is a published zero, not this hole. | Trust Auditor |
| F-indic-unit | Observation `unit` stays as the producer printed it. Display scale is bind, not a rewritten Parquet unit. | Platform Architect |
| F-c2-lakh-thousand | Projection series unit (thousands of persons) on the observation so bind can scale to Cr without guessing. | Methodologist; Platform Architect |
| F-census-axis-marks | Chart category / `reference_period` for the citizen row is the census year, not `1901 $`. Footnote flags stay in lineage or the caveat, not the tick. | Methodologist; Content Editor |
| F-axis-period-prefix | Do not copy `end-2024-25` / `actual-2024-25` keys into bound chart labels. | Platform Architect; UI/UX Developer |

### Trust Auditor

C8 done-when still: dates match the vintage; no desk field, parser name, Frame label, or `do_not` on the page; no hole plotted as zero; cites open producer URLs.

Closed on live preview bind (C8 pass): C1 July vs August (`T-cite-period`); C2 method leak (`T-lags-slot`, `T-this-desk`); cess hole (`T-cess-zero`); desk cite dump (`T-cite-desk-caveat`). Notes, not fails: IGST printed zero; FRBM **not published**; producer URLs; no default rank, no red–green, no spin.

Next citizen-facing preview after the F- rows: fail a 2011 lede that reads as today, or a 2026 projection that reads as a census count (`F-c2-lede-year`); fail `L crore` / `L Thousand` as a magnitude (`F-indic-unit`, `F-c2-lakh-thousand`). Form-factor (inline type, method fine-print, left-gap on bars, source-line chrome) is **not** Trust.

## Multi-party items (this batch, lead first)

| Item | Lead | Parties |
|------|------|---------|
| C1 cite period matches the observation (or two cards); no July card for August | Closed (C8 pass / C9) | Content Editor, Trust Auditor |
| One Indian `display_string`; no L+crore / Lakh Thousands; population in Cr | Platform Architect | Content Editor, UI/UX Developer, Pipeline Engineer, Methodologist, Trust Auditor |
| Inline `<p>` numbers at body size, highlighted | UI/UX Developer | Content Editor |
| Cite-strip and chart source-lines → panel; card remains | UI/UX Developer | Front-end Architect, Platform Architect, Content Editor |
| Source-stack lists every cite used on the answer-page | UI/UX Developer | Front-end Architect |
| Method fine-print, `--desk` width | UI/UX Developer | Content Editor, Charter Editor (ruling 4) |
| C2 lede: current-year projection, named; 2011 still on first screen | Content Editor | Methodologist, Charter Editor (ruling 5), Trust Auditor |
| Census year ticks without footnote marks | Pipeline Engineer | Content Editor, Methodologist, UI/UX Developer |
| Budget axis without `end-` / `actual-` | Pipeline Engineer | Platform Architect, UI/UX Developer, Content Editor |
| Bar charts: fill leftover left field | UI/UX Developer | — |
