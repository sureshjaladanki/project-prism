# Principal review feedback

Principal (advisor; outside roster). Citizen preview read of the CMS desk. Method: [principal-review-guidelines.md](../principal-review-guidelines.md). Charter Editor routes. This file does not amend standing contracts.

```text
role:           principal (advisor; outside roster)
preview:        http://localhost:4333/ · desk-20260921-2f93be5c9ccc
routes:         / · /people · /people/population · /money · /money/union · /prices · /prices/retail-prices · /work · /delivery · /how-this-works · /sources
read:           2026-09-22
patterns:       principal-review-guidelines.md (1–11)
next:           charter-editor
```

**Verdict for Charter.** A citizen without the codebook can open three answer pages and see real producers and real magnitudes — but the desk still reads like a **half-decoded codebook**: mixed scale words (`L crore of rupees`), desk words (`hole`, `parked`, `next_release`), machine axis keys (`end-`, `actual-`), a 2011-led population answer in 2026, and hero numbers that shout inside the sentence. Several items marked closed in [cms-system-feedback.md](cms-system-feedback.md) are **still live on this desk id**. Trust still owns record pass/block; these notes are the citizen job.

---

## Fails

Each fail uses the pattern id from the guidelines. Propagation A–D was run before filing.

### Shell and home

| Id | Pattern | Where | Citizen hit | Propagate | Want |
|----|---------|-------|-------------|-----------|------|
| PR-home-unit | 4 · unit agreement | `/` fast-facts · money teaser | Teaser prints `35.27 L crore of rupees` — compact `L` plus leftover “crore of rupees.” | D → same string on `/money/union` lede, spend prose, liabilities prose, chart axis title `Crore of rupees`. | One Indian `display_string` on home teasers and answer pages (`35.27 L Cr` or equivalent; no leftover producer unit word). |
| PR-home-census | 7 · first-screen honesty | `/` · people teaser; `/people` sleeve blurb | Home and People hub lead with Census 2011 Total as the answer to “how many people live in India.” | D → `/people/population` hero still 2011-led on this desk. | Teaser and sleeve one-liner match the honest 2026 lead (projection named as projection; 2011 kept as last census). |
| PR-empty-sleeve | 11 · shell | `/work`, `/delivery` | Sleeve is only the H1 and footer — blank body. Reads broken, not a calm “not yet” invitation. | D → both empty sleeves. | One quiet sentence that topics are not in this snapshot (no desk jargon). |
| PR-nav-look | 11 · shell | `.site-header` all routes | Header works (Prism + five sleeves, ~44px). Still thin institutional chrome; no strong house presence beyond the wordmark. | C → whole desk shares it. | Front-end signs IA; UI/UX presentation on header tokens/type (open `F-site-header-nav`). Not a second nav tree. |

### `/money/union`

| Id | Pattern | Where | Citizen hit | Propagate | Want |
|----|---------|-------|-------------|-----------|------|
| PR-money-l-crore | 4 | hero lede · `#spend` · `#liabilities` · chart axis titles | `35.27 L crore of rupees`, `43.57 L crore…`, `1.66 Cr crore of rupees`. Stat chips say `35.27 L` / `1.66 Cr` without a complete citizen unit; axes still title `Crore of rupees` beside `L`/`Cr` ticks. | A/B/C/D — every money encoding + home teaser. | Whole-string compact unit; drop leftover “crore of rupees”; axis title matches ticks. |
| PR-money-inline-type | 7 / 9 | `.fact-lede .observation-value` | Bound numbers in the lede render ~44px inside the paragraph — shout over the sentence; chips repeat the same magnitudes immediately below. | D → same on `/people/population` and `/prices/retail-prices` heroes. | Prose observations at body size (weight/underline); large type only on `.stat-figure`. |
| PR-money-hole-word | 2 / 3 | `#collect` prose; chart subtitle “A blank is not zero” | “GST Compensation Cess on this chart is a **hole**…” Desk word on the answer. | A → method “districts are **missing**”; D → people/prices “hole.” | Say **not published**; keep the “not zero” teaching without “hole.” |
| PR-money-cess-zero | 3 | chart *Tax by major head, Budget Estimates 2026-27* | Category **GST Compensation Cess** is listed; a bare **`0`** sits on the scale. Prose says blank≠zero. Citizen cannot tell published IGST zero from a smoothed gap. | B (prose↔chart); Trust for status. | Gap not plotted as numeric zero; published zero visually distinct from **not published**. |
| PR-money-axis-keys | 8 | *Outstanding liabilities…*; *Revenue receipts in this Budget book* | X ticks: `end-2021-2022`, `revised-2025-26`, `actual-2017-18`, `be-2026-27`. | A both multi-year charts; D if other slices gain period keys. | Citizen year / BE·RE·Actuals phrases only. |
| PR-money-chart-left | 9 | *Tax by major head…* (and sibling bar charts) | Long categorical labels eat ~⅓ of the well; plot starts late; truncated “Income tax other than corporatio…”. | C → spend/deficit bars; D → state bars on other pages. | Plot fills the card; labels fit or wrap without starving the marks. |
| PR-money-recap | 1 | hero chips vs lede; parts of `#spend` | Lede magnitudes repeated as chips without a new citizen job on the first screen. | A evidence sections that only restate BE chips. | First screen: one designed answer; chips may carry the same figures if lede does the concept job — but do not enlarge lede numbers into a second chip row in prose. |
| PR-money-three-records | 5 / 10 | `#three-records` source-line | One line: “Ministry… · Controller General… · each record as labelled” for three different producers. | B — three chips, one vague cite control. | One cite control per observation (or clear multi-cite), periods matching each chip. |
| PR-money-method-missing | 2 / 3 | Methodology | “districts are **missing**”; FRBM labels “**missing** as a table.” | D gap vocabulary desk-wide. | **not published** (or “not on this page” only when that is the citizen job). |

### `/people/population`

| Id | Pattern | Where | Citizen hit | Propagate | Want |
|----|---------|-------|-------------|-----------|------|
| PR-c2-lede-2011 | 7 | hero byline + fact-lede + stat row | H1 asks how many people live in India; first screen answers with **Census 2011** (`121.09 Cr`) and “not today,” but never leads with the 2026 projection. | D home/sleeve teasers. | Lead with official **projection for the current year, named as projection**; keep 2011 Total on the same first screen. |
| PR-c2-lakh-thousand | 4 | `#projection` prose · chart title · y-axis · source-line | `14.23 L thousand people`; chart “Projected India population… **thousands**”; axis title **Thousands**; source-line “projected population, **thousands**.” Same page’s census concept is **Cr**. | B all projection encodings; D money `L crore` family. | One headcount display (**Cr**); producer thousands stay off citizen chrome. |
| PR-c2-axis-marks | 8 | chart *India Total, census years 1901 to 2011* | Ticks: `1901 $`, `1951 @`, `1981 #`, `1991 +`, `2001 ++`. | B title says years; axis says footnotes. | Year only; footnotes in method/cite. |
| PR-c2-desk-method | 2 | Methodology | `next_release unknown — delayed`; “**Districts are parked**”; “STATE rows / DISTRICT rows” codebook caps. | A evidence “Do not fill those **holes**”; D prices “hole.” | Citizen sentences only; desk fields stay off the page. |
| PR-c2-hole-do-not | 2 / 3 / 6 | `#change`, `#fertility` evidence | “a **hole**, not zero”; “districts are **missing**”; “**Do not fill** those holes from the bulletin above.” | A method; D money/prices. | **not published**; drop desk imperative from evidence (method if needed). |
| PR-c2-rates-unit | 4 | `#births-deaths` / `#fertility` stats | Chips `18.3`, `6.4`, `24`, `1.9` with **no unit in the cell**; prose does not say per thousand / per woman. | B chart *India Total rates, 2024*. | Slot unit on every rate chip and axis. |
| PR-c2-rates-aside | 6 | `#births-deaths` openers | “They are not multiplied by the 2011 headcount…” and “Rates are not how many people live in India” sit in evidence. | A fertility “missing” teaching. | Keep short concept line if needed; long “how not to misread” → Methodology. |
| PR-c2-all-india-aside | 1 / 6 | `#where` | “India Total is the national unit above, not a bar here.” Chart title already implies state list. | D prices `#states` same line. | Line: cut or one short clause; not a standing aside. |
| PR-c2-inline-type | 7 | fact-lede | `121.09 Cr` at ~44px inside the sentence. | D money/prices heroes. | Body-size prose observations. |
| PR-c2-cite-strip | 5 | first-screen cite control | Opens as a long producer·series dump line (PCA SD, table codes). Card body is better (producer / series / period / release / caveat) once expanded. | D money/prices strips. | Compact source-line chrome; panel/card carries detail (cms rulings 2–3). |

### `/prices/retail-prices`

| Id | Pattern | Where | Citizen hit | Propagate | Want |
|----|---------|-------|-------------|-----------|------|
| PR-c1-recap-food | 1 | `#food` | Restates All India Combined food **5.95%** already on the first screen; adds Food and beverages / rural / urban — keep those; drop the pure recap sentence. | A other sections that restate hero chips. | Further the H2 (wider basket, sectors), don’t reprint the hero food rate as the opener. |
| PR-c1-stat-unit | 4 | hero + rural/urban `.stat-figure` | Chips show `4.82`, `5.95`, `5.23`, `4.31` with **no %** in the cell; lede says “percent.” | B first chart labels. | Unit in the cell (percent), same as money needs complete scale. |
| PR-c1-hole | 2 / 3 | `#rate-over-time` chart subtitle + prose + method | “2013 is not published — a **hole**, not zero”; method “blank inflation cell is a **hole**.” | D people/money. | **not published**; never “hole.” |
| PR-c1-all-india-aside | 6 | `#states` | “All India is the national unit above, not a bar here.” | D people `#where`. | Cut (title already lists States/UTs). Chandigarh Rural **not published** line can stay. |
| PR-c1-group-code | 2 / 5 | source-stack cite for CFPI | Series text includes **Group code 01.1** — codebook on the citizen card. | D other cites with annex/table codes in the *citizen* series line. | Producer series name in plain words; codes on librarian card only if Charter keeps them off the strip. |
| PR-c1-inline-type | 7 | fact-lede | `4.82` / `5.95` at ~44px in prose. | D other heroes. | Body-size inline observations. |
| PR-c1-july-cards | 5 | source-stack | Stack includes July 2026 Final cards beside August Provisional answer. | Trust/Platform if one HTML id ever meant two months; here two cards may be intentional. | Citizen must not open a July card thinking it is the August figure; strip/in-text must bind August. |

### House pages

| Id | Pattern | Where | Citizen hit | Propagate | Want |
|----|---------|-------|-------------|-----------|------|
| PR-how-hole | 2 / 3 | `/how-this-works` · When the record is incomplete | “A **hole** is not filled with a remembered figure.” | D answer-page gap vocabulary. | Same citizen phrase as answer pages (**not published** / named absence). |
| PR-sources | — | `/sources` | Clear house index; “How to read a cite” is usable. | — | No fail. Keep as the producer index, not a per-slice dump. |

---

## Wants (summary for Charter)

1. **One citizen magnitude string** everywhere (home → lede → chip → axis): no `L crore` / `L thousand` / axis `Crore of rupees` beside `L`.
2. **One gap phrase: not published** — retire hole / missing / parked / do-not fill from citizen surfaces; never plot a gap as `0`.
3. **Population first screen for a 2026 reader** — projection named as projection; 2011 as last census on the same screen; fix home/sleeve teasers to match.
4. **Citizen axis labels** — years and BE/RE/Actuals phrases; no `$` `@` `#` or `end-` / `actual-` keys.
5. **Prose numbers at body size**; method quieter than the answer; evidence that further answers, not chip recaps or codebook asides.
6. **Empty sleeves** get one calm invitation sentence; header presentation after Front-end IA sign.

---

## Out of scope (do not expand here)

- Trust pass/block on producer URLs, spin, or cell spot-checks (including whether IGST `0` is the published zero).
- Whether this preview should be rebound to a later desk id that already closed F-rows — Platform / publish pointer; Principal only reports **this** URL.
- Contract patches to editorial-guidelines, design-system, or web-design.
- Geography doorway pages; ingest runner redesign.

---

## Cleared on this pass (citizen job OK enough)

- Answer pages name producers; FRBM gap on money uses **not published** in the deficit section.
- Money cite *card* fields (producer, series, period, release, caveat) read as a citizen card once open — strip chrome still fails density.
- `/sources` house framing is sound.
- Concept boundaries on money (BE ≠ Actuals, gross ≠ net, three records) are mostly present — density and cite wiring still hurt.

---

## Handoff

```text
role:           principal (advisor; outside roster)
preview:        http://localhost:4333/ · desk-20260921-2f93be5c9ccc
routes:         / · /people · /people/population · /money/union · /prices/retail-prices · /work · /delivery · /how-this-works · /sources
fails:          PR-home-unit, PR-home-census, PR-empty-sleeve, PR-nav-look; PR-money-* (unit, inline-type, hole, cess-zero, axis-keys, chart-left, recap, three-records, method-missing); PR-c2-* (lede-2011, lakh-thousand, axis-marks, desk-method, hole-do-not, rates-unit, rates-aside, all-india-aside, inline-type, cite-strip); PR-c1-* (recap-food, stat-unit, hole, all-india-aside, group-code, inline-type, july-cards); PR-how-hole
wants:          one display string; not published; 2026 population lead; citizen ticks; body-size prose; quiet empty sleeves
out_of_scope:   Trust record audit; desk rebind; contract edits
next:           charter-editor
```

Method reference: [principal-review-guidelines.md](../principal-review-guidelines.md). Earlier routed batches: [citizen-page-feedback.md](citizen-page-feedback.md), [cms-system-feedback.md](cms-system-feedback.md).
