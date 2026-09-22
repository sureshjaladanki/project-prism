# Citizen movement, denomination, and gaps

Persona: Methodologist. Signed for the Prism CMS rethink ([prism-cms-rethink.md](next/prism-cms-rethink.md) phase 6). Bind may use these rulings; Content Editor must not invent a prior period or a denomination.

**Citizen gap phrase (house-wide):** **not published**. Schema status stays `unknown` or `withheld`. Never “unknown / not a table”, never a blank that reads as zero, never a remembered figure. A published zero (`status: value`, `value: 0`) is a different fact — say zero; do not use the gap phrase.

**Break phrase (when joining is refused):** **not comparable**. Used only when a `series_break` or `not_comparable` status lies between two observations, or when this note refuses the join. Show both figures; do not subtract them.

---

## Denomination vocabulary

| Producer print | `denomination.magnitude` | `denomination.measure` | Citizen ladder |
|----------------|--------------------------|------------------------|----------------|
| ₹ crore (Budget, CGA, liabilities) | `crore` | `rupees` | thousand / lakh / crore / lakh crore of **rupees** |
| thousands of persons / `'000` (NCP Table 8) | `thousand` | `persons` | same ladder of **persons** |
| persons (Census PCA, A-02) | `ones` | `persons` | same |
| inflation (%), % of BE, rates | `ones` | `percent` or `rate` | never compacted |
| index (Base …=100) | `ones` | `index` | never compacted |
| SRS birth/death/IMR/TFR as published | `ones` | `rate` | never compacted; unit stays on the chip |

Ingest and Pipeline write denomination with the observation. Bind converts `value × magnitude` to canonical base units once. Render formats only. Do not re-base crore or thousand amounts as if they were ones.

---

## C1 — `/prices/retail-prices`

### Movement (same series, same vintage)

| Lead figure | Prior period (comparable) | Year-ago (comparable) |
|-------------|---------------------------|------------------------|
| CPI General Combined YoY inflation, latest Provisional month | Previous calendar month, same series/sector (Final when published for that month) | Same calendar month one year earlier on the **Base 2024=100** General series |
| CFPI Combined YoY | Same rule on the CFPI series | Same |

**Refuse as movement:** stitching a 2012=100 month to a 2024=100 month; Rural vs Urban as “prior”; Division 01 as prior to CFPI; linked back-series blanks as zero change.

### Extremum window ( forevidence “when was it last this high?”)

Bound highest and lowest **monthly Combined YoY inflation** on CPI General, Base 2024=100, for the months the vintage publishes on that series after the base change — do not silently extend into the linked back series. Name the window in method as the months present in the vintage for that series. Extrema are facts of the published measure; they are not a verdict.

---

## C2 — `/people/population`

### Movement

| Lead figure | Comparable prior | Refuse |
|-------------|------------------|--------|
| NCP projection for the current projection year | Census 2011 Total and Census 2001 Total as **separate** published counts (movement sentence may name them; do not subtract projection − census as a continuous change rate without “Analysis by Prism” and a method note that they are different records) | Treating projection − 2011 as a producer-published change; multiplying SRS rates by 2011 headcount |
| SRS rates (birth, death, IMR, TFR) | Prior **published SRS year** for the same indicator on the same bulletin/report series | Inventing a headcount from a rate |

Projection and census stay verbally distinct on the first screen. Thousands-of-persons (projection) and persons (census) share the persons ladder after canonical conversion; they remain different records.

---

## C3 — `/money/union`

### Movement

| Lead figure | Comparable prior | Refuse |
|-------------|------------------|--------|
| Budget Estimates receipts / expenditure for the Budget year | Last year with **Actuals** on the same annex/statement line (e.g. Actuals 2024-25 against BE 2026-27) | Joining BE → RE → Actuals as one continuous change; treating CGA April–July as an annual prior |
| Tax / non-tax / capital / expenditure heads | Same head’s last published Actuals | Collapsing BE/RE/Actuals; GST Compensation Cess gap as zero; IGST published zero as a gap |

BE, RE, and Actuals are three records. Movement is BE (or the on-screen plan) against the last Actuals for that line — never a single slope through all three.

**Gap vs zero:** GST Compensation Cess stays **not published** (`unknown`). IGST may be a published **zero**. Say both plainly in method; never plot the cess gap as 0.

---

## What Content Editor may bind

- `CitizenChange` only for pairs this note marks comparable (or with `comparable=False` → **not comparable**).
- Gap slots → citizen phrase **not published**.
- Denomination from the observation; do not invent a second scale in copy.

## What stays desk / method-only

Base-year notation, series/annex/group codes, “this is not X” asides, dual-series teaching, joining-unit notes, BE≠Actuals — method block, not above the fold.
