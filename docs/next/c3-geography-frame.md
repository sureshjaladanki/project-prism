# C3 geography frame

Persona: Geography Steward. Slice: **C3** (What does the Union collect, and what does it spend it on?).

Input locked: `docs/next/c3-citation-cards.md`. Charter geography: **Union-only until C5**. Keep the producer’s printed label (`Government of India` / `Central Government` / `Union Government` / `Union budget heads`). Do not treat a Union total as the country’s public money.

Store a row on **the producer’s geography string as printed on that artifact**. Do not merge `Government of India`, `Central Government`, and `Union Government` because the English looks similar. Do not match on spelling alone.

BE / RE / Actuals, fiscal year, and monthly “upto July” are **not** geography. Transfers to States, tax assignment, and “Receipts of Union Territories” as **Union budget heads** are **not** a State/UT finance map.

**States and UTs as own governments:** out of frame (C5). **Districts:** parked. Do not ingest Receipt Budget Annex 4 / 4A / 4B or BAG transfers-to-States as if they were C5. **Crosswalk between frames: none.** Budget statements, CGA monthly accounts, and Finance Accounts are three records.

Three frames (Cards 1–9 share the Budget 2026-27 Union map, with each card’s printed label).

---

## Frame A — Union Budget 2026-27 (Cards 1–9)

Binds:

- Card 1 — Receipt Budget I. Tax Revenue (`Government of India` / Union)
- Card 2 — Receipt Budget II. Non-Tax Revenue (same; “Receipts of Union Territories” is a Union head)
- Card 3 — Receipt Budget III. Capital Receipts (same; not state borrowings)
- Card 4 — Annex-1 Trends in Receipts (`Government of India`)
- Card 5 — Expenditure Profile Statement 1 (`Union budget heads`)
- Card 6 — BAG Deficit Statistics (`Government of India`)
- Card 7 — Statement of Liabilities (`Central Government` / `Government of India`)
- Card 8 — FRBM statements (`Central Government`)
- Card 9 — Annual Financial Statement (`Central Government` / Consolidated Fund of India, Contingency Fund, Public Account)

Artifacts: `indiabudget.gov.in` Budget 2026-27 statements named on those cards (xlsx fetch for Cards 1, 2, 3, 5, 6; PDF for Cards 4, 7, 8, 9). No state-code column on the Union totals of record. Format change is not a new map.

```text
frame:          Union
vintage:        2026
code_system:    none
units_included:
  one Union government unit as labelled on that card
  (Government of India | Central Government | Union Government |
   Union budget heads | Consolidated Fund of India as printed)
units_missing:
  all States as own governments:
    Andhra Pradesh
    Arunachal Pradesh
    Assam
    Bihar
    Chhattisgarh
    Goa
    Gujarat
    Haryana
    Himachal Pradesh
    Jharkhand
    Karnataka
    Kerala
    Madhya Pradesh
    Maharashtra
    Manipur
    Meghalaya
    Mizoram
    Nagaland
    Odisha
    Punjab
    Rajasthan
    Sikkim
    Tamil Nadu
    Telangana
    Tripura
    Uttar Pradesh
    Uttarakhand
    West Bengal
  all Union Territories as own governments:
    Andaman and Nicobar Islands
    Chandigarh
    Dadra and Nagar Haveli and Daman and Diu
    NCT of Delhi (legislature)
    Jammu and Kashmir (legislature)
    Ladakh
    Lakshadweep
    Puducherry (legislature)
  districts and below (parked; not in these Union statements as a district series)
  local-body accounts
breaks:         Union accounts for Budget 2026-27 as laid 1 February 2026.
                Not a state Finance Accounts vintage. Not CGA monthly (Frame B)
                and not Finance Accounts 2024-25 (Frame C).
                Card 9 “Receipts and Expenditure of Union Territories without
                Legislature” stays inside Union accounts — it does not fill
                missing UT finance units.
                Card 5 Transfers (Centrally Sponsored Schemes, Finance Commission
                Transfers, Other Transfers) are Union outgo as printed — not C5.
crosswalk:      none — do not recode
```

A Union figure on this frame must still say **states, UTs, and districts are missing**.

---

## Frame B — CGA monthly Accounts at a Glance (Card 10)

Binds: Card 10 — Union Government Accounts at a Glance as at the end of July 2026.

Artifact: `https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.htm`. Geography as printed: Government of India / Union Government.

```text
frame:          Union
vintage:        2026
code_system:    none
units_included:
  Union Government as printed on DATA2627.htm
units_missing:
  same States, UTs as own governments, districts, and local bodies as Frame A
breaks:         Intra-year unaudited Union accounts for FY 2026-27 up to July 2026.
                Not Budget BE/RE/Actuals (Frame A) and not Finance Accounts
                2024-25 Actuals (Frame C). Do not recode onto Frame A labels.
crosswalk:      none — do not recode
```

---

## Frame C — CGA Finance Accounts 2024-25 Statement No. 1 (Card 11)

Binds: Card 11 — Finance Accounts, Union Government, 2024-2025, No. 1 Summary of Transactions.

Artifact: `https://cga.gov.in/writereaddata/file/Fin20242025Statement1.pdf`. Geography as printed: Union Government. Annexure to Statement 1 (proceeds assigned to States) is Union tax assignment, not C5.

```text
frame:          Union
vintage:        2024
code_system:    none
units_included:
  Union Government as printed on Statement No. 1
units_missing:
  same States, UTs as own governments, districts, and local bodies as Frame A
  (the Statement 1 annexure does not make those units included)
breaks:         Annual Actuals for FY 2024-25. Not Budget 2026-27 (Frame A) and
                not July 2026 monthly (Frame B). Do not recode proceeds assigned
                to States into a state finance row.
crosswalk:      none — do not recode
```

---

## Do not recode (standing)

| From | To | Why not |
|------|----|---------|
| Frame A `Government of India` | Frame B `Union Government` | Budget vs unaudited monthly |
| Frame A BE/RE/Actuals | Frame C Finance Accounts Actuals | Different producer table even when the year overlaps |
| Frame A Card 5 Transfers | C5 state receipts | Union outgo, not state accounts |
| Frame A Card 2 UT receipts head | UT Finance Accounts | Union budget head |
| Frame C annexure assigned to States | C5 | Union tax assignment |
| Any of the above | LGD “current” India | Not this vintage |
| Any of the above | a per-person India | Charter-out |

---

## Ingest / Pipeline keys

| Field | Store as |
|-------|----------|
| Frame A geography key | printed Union label on that card (no state code) |
| Frame B geography key | printed Union Government string on DATA2627.htm |
| Frame C geography key | printed Union Government string on Statement No. 1 |
| BE / RE / Actuals / month | observation status / period; not a geography unit |
| States, UTs as governments, districts | out of frame on every card |
| Frame | A Cards 1–9; B Card 10; C Card 11 |

Do not invent English names. Do not hide missing states, UTs, or districts inside a Union figure. Do not rank jurisdictions.

---

## Handoff

Geography Steward done for C3: Ingest can store a Union row without guessing a State, and without treating Union transfers as C5. Content Editor cannot present Union money as the whole country’s public money.

**No re-run after the 18 September 2026 re-card.** Printed Union labels and the Union-only missing-units list are unchanged. Cards 1, 2, 3, 5, 6 now fetch producing-office xlsx of the same statements; that is not a new geography.

Next persona: **Methodologist** (xlsx is the same statement as the printed book). Then Ingest on the named card URLs.
