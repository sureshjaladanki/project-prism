# C5 geography frame

Persona: Geography Steward. Slice: **C5** (What do states and UTs collect and spend?).

Input locked: `docs/next/c5-citation-cards.md`. Charter geography: states and UTs as the official compilation publishes them; districts parked; Union Budget / CGA Union accounts stay on **C3**.

Store a row on **the producer’s name as printed on that artifact**. Do not match on spelling alone (Odisha / Orissa, Puducherry / Pondicherry, Delhi / NCT of Delhi / NCT Delhi). Do not join an RBI 2025-26 Study row to a CAG CFRA 2020-21 row because the English looks similar.

Accounts / RE / BE columns are **not** geography. Own tax vs Centre transfers are **not** geography. Local-body accounts are out of frame.

**Districts:** parked. **Crosswalk between frames: none.** RBI Study of Budgets and CAG CFRA are two maps. Neither is a Union Budget map (C3).

Two frames.

---

## Frame A — RBI State Finances: A Study of Budgets of 2025-26 (Cards 1–6)

Binds: Cards 1–6 (deficit/fiscal indicators; revenue receipts; expenditure; capital receipts; GFD financing; outstanding liabilities / market borrowings).

Artifact of record for unit titles: RBI Annual Publications listing dated **23 January 2026**, Appendices I–IV titled **States and Union Territories with Legislature**. File groups on that listing name every unit below (plus an **All States and UTs** aggregate). Statement/appendix table titles also say “State Governments and UTs” — store the row label as printed when Ingest opens the XLSX/PDF.

Key: producer English name as printed (no LGD join licence on these cards). `code_system: producer-specific`.

```text
frame:          state | UT
vintage:        2025-26 Study (listing 23 January 2026; Accounts / RE / BE columns as labelled inside — not geography)
code_system:    producer-specific
units_included:
  states (as titled on Appendices I–IV file groups):
    Andhra Pradesh
    Arunachal Pradesh
    Assam
    Bihar
    Chhattisgarh
    Goa
    Gujarat
    Haryana
    Himachal Pradesh
    Jammu and Kashmir
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
  Union Territories with Legislature (as titled on the same appendices):
    Delhi
    Puducherry
  aggregate row as printed:
    All States and UTs
units_missing:
  Union Territories without legislature (not titled into Appendices I–IV):
    Andaman and Nicobar Islands
    Chandigarh
    Dadra and Nagar Haveli and Daman and Diu
    Ladakh
    Lakshadweep
  districts and below (parked)
  local bodies (charter-out)
  Union Government as a C5 unit (that is C3)
breaks:         Study map as of the 2025-26 edition. Notes for readers, not recodes:
                - Telangana is a titled state unit on this map (post-2014).
                - Jammu and Kashmir appears in the listing’s state file groups; it is a
                  UT with legislature after the 2019 reorganisation — store the printed
                  label, do not invent a pre-2019 state row or a Ladakh twin.
                - Delhi and Puducherry are the UT-with-legislature titles on Appendices
                  I–IV; other UTs are missing (see units_missing).
                - Do not recode these labels onto Frame B (CAG 2020-21) or onto C3.
crosswalk:      none — do not recode
```

**All States and UTs** is the producer’s printed aggregate for this Study’s coverage — not “every UT in India”, and not a roll-up Ingest should invent from state rows. A page that shows it must still say UTs without legislature are missing, and districts are parked.

---

## Frame B — CAG CFRA / Union and State Finances at a Glance 2020-21 (Card 7)

Binds: Card 7 only.

Artifact: CAG glance PDF and CFRA Volumes I–III for **2020-21** (`cag.gov.in` combined-accounts archive). Preface: Union and State Governments / Union Territories with Legislature. Glance revenue-receipt charts list states plus UT Jammu & Kashmir, NCT Delhi, UT Puducherry among others (as printed in the glance extract on the citation card).

```text
frame:          Union | state | UT
vintage:        2020-21 (Accounts); glance preface 6 September 2024
code_system:    producer-specific
units_included:
  Union Government lines as printed in CFRA / glance (for C5 use only state/UT tables —
    do not silent-substitute Union CFRA lines for C3 Budget/CGA cards)
  States and UTs with Legislature as printed in the glance / volumes
    (including Jammu & Kashmir, NCT Delhi, Puducherry where the glance lists them)
units_missing:
  CFRA years after 2020-21 (named hole on the citation card — not on this map)
  UTs without legislature if absent from the opened glance tables
  districts and below (parked)
  local bodies (charter-out)
breaks:         2020-21 audited map. Several years behind Frame A. Do not stitch RBI
                2025-26 Study rows onto CFRA 2020-21 rows. Do not present CFRA Union
                lines as C5 state money or as C3 Budget BE.
crosswalk:      none — do not recode onto Frame A or C3
```

Ingest must confirm the exact printed name strings from the opened glance/volume tables before storing rows. Until then, treat the citation card’s geography note as the coverage claim, not a completed label dump.

---

## Handoff

Next persona: **Methodologist**. Do not ingest until Platform names the refresh contract for this slice. Geography is locked for Frames A–B as above; cell fetch of `rbidocs` may still need a browser-capable path (named hole on the citation cards).
