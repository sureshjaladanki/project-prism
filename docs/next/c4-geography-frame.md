# C4 geography frame

Persona: Geography Steward. Slice: **C4** (How many people are working, seeking work, and what do they earn?).

Input locked: `docs/next/c4-citation-cards.md`. Charter geography: national and states/UTs as published; **districts parked** (including PLFS Selected Districts snapshot — do not ingest for C4). PLFS only — not CMIE, not MGNREGA (C9).

Store a row on **the producer’s name as printed on that artifact**. Do not match on spelling alone (`Delhi` ≠ `NCT of Delhi`; `Andaman & N. Island` ≠ `Andaman & Nicobar Islands`). Do not join a quarterly “selected States” row to an annual State/UT row because the English looks similar.

Sector (rural / urban / rural+urban), gender, and age group are **not** geography. Usual status (ps+ss) vs CWS is **not** geography.

**Districts:** parked. **Crosswalk between frames: none.** Monthly all-India, quarterly selected States, and annual State/UT are three maps.

Three frames.

---

## Frame A — PLFS Monthly Bulletin, all-India only (Card 1)

Binds: Card 1 — LFPR, WPR, UR in CWS (August 2026 Bulletin and later months of the same series).

```text
frame:          Union
vintage:        monthly CWS reference month (Card 1: August 2026)
code_system:    none
units_included:
  All India (as printed; by sector rural / urban / rural+urban — sector is not a State)
units_missing:
  all States and UTs as own rows (not in the Monthly Bulletin)
  districts and below (parked)
breaks:         Post-January-2025 monthly design. Do not invent State rows from Frame B or C
                and call them Monthly Bulletin geography.
crosswalk:      none — do not recode
```

A national monthly figure must still say States/UTs and districts are missing from **this** bulletin.

---

## Frame B — PLFS Quarterly Bulletin, selected States (Card 2)

Binds: Card 2 — Appendix A Tables 2–5 (and companions) for April–June 2026 and later quarterly bulletins under the same “selected States” rule.

Artifact labels on Table 2 (April–June 2026) as on the citation card:

```text
frame:          Union | state | UT
vintage:        April–June 2026 (and later quarters as labelled; CWS)
code_system:    producer-specific
units_included:
  all-India
  Andhra Pradesh
  Assam
  Bihar
  Chhattisgarh
  Delhi
  Gujarat
  Haryana
  Himachal Pradesh
  Jharkhand
  Karnataka
  Kerala
  Madhya Pradesh
  Maharashtra
  Odisha
  Punjab
  Rajasthan
  Tamil Nadu
  Telangana
  Uttarakhand
  Uttar Pradesh
  West Bengal
  Jammu & Kashmir
units_missing:
  all other States/UTs not on Appendix A (e.g. smaller States and remaining UTs —
    publisher omission, not a Prism withhold; do not fill from Frame C)
  districts and below (parked)
breaks:         Selected-States map only. Pre-2025 urban-only quarterly series is a
                different design — do not silent-stitch. Do not recode onto Frame C.
crosswalk:      none — do not recode
```

---

## Frame C — PLFS Annual Report 2025, each State/UT (Cards 3–4)

Binds: Card 3 (LFPR/WPR/UR usual ps+ss and CWS); Card 4 (earnings Tables 38–40). Same `State/UT` column labels.

Labels on Table 16.0 as on the citation card:

```text
frame:          Union | state | UT
vintage:        January–December 2025 (calendar year; first annual under revamped design)
code_system:    producer-specific
units_included:
  all India
  Andhra Pradesh
  Arunachal Pradesh
  Assam
  Bihar
  Chhattisgarh
  Delhi
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
  Uttarakhand
  Uttar Pradesh
  West Bengal
  Andaman & N. Island
  Chandigarh
  Dadra & Nagar Haveli & Daman & Diu
  Jammu & Kashmir
  Ladakh
  Lakshadweep
  Puducherry
units_missing:
  districts and below (parked; do not ingest Selected Districts snapshot for C4)
breaks:         Printed stubs use Delhi (not NCT of Delhi); Andaman & N. Island;
                Dadra & Nagar Haveli & Daman & Diu as one merged UT string.
                Calendar-year 2025 annual vs earlier July–June annuals is a design /
                reference-period break (Methodologist). Do not fill Frame B holes
                from this list and call them quarterly.
crosswalk:      none — do not recode onto Frame B or other slices’ maps
```

---

## Handoff

Next persona: **Methodologist** (usual vs CWS; January 2025 design break; three earnings concepts). Do not ingest until Platform names the refresh contract. Refresh MoSPI hashed upload paths via product 69 listing when re-fetching.
