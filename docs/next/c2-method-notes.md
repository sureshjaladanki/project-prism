# C2 method notes — citizen vs desk

Persona: Methodologist. Desk fields unchanged: [c2-method-notes.md](../archive/c2-method-notes.md).

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| Census 2011 PCA | Do not present as how many people live in India now | Enumerated persons on 1 March 2011; last published census Total; not today |
| Census A-02 | Do not chart N.A. as 0; do not extend past 2011 | Population by census year 1901–2011; N.A. is not zero |
| SRS bulletin | Do not invent a 2024 headcount | Sample rates (birth, death, IMR), not a stock |
| SRS statistical report | Do not present TFR as a headcount | Fertility rates including TFR; bigger States/UTs only |
| NCP Table 8 | Do not present a projection as a census | 2019 projection as on 1 March; later year still that report; not a census |

## F-c2-lede-year — signed wording (2026-09-21)

Charter this-batch ruling 5. Methodologist sign. Content Editor applies slots; does not invent a pasted 2026 figure.

**Must say**

1. The first number on the fact-lede is the official **projection** for the current year (slot `india-projected-persons-2026`, period `projection_2026`), named as a projection.
2. That figure is **not** a census enumeration.
3. Census 2011 Total (slot `india-total-persons-2011`) stays on the **same first screen** as the last enumerated Total (stat row and/or the next sentence).
4. Do not treat 2011 as today. Do not treat the projection as a census count.

**Approved citizen sentences (use or tighten; do not soften)**

Byline (first screen):

> Official projection as on {{period.projection_2026.label}}. Latest published census Total: {{period.census_2011.label}}.

Fact-lede:

> As on {{period.projection_2026.label}}, the official projection for India, Persons, is {{slot:india-projected-persons-2026}}. That is a National Commission on Population projection from the 2019 Technical Group report, not a census count. Census 2011 enumerated {{slot:india-total-persons-2011}} people in India, Total, as of {{period.census_2011.label}} — the latest published census Total.

Stat row on the first screen: keep India Total / Rural / Urban from Census 2011 (slots already bound).

**Unit note (F-c2-lakh-thousand, method)**

Producer Table 8 is thousands of persons. Bind shows compact Cr beside census persons. Methodology must still say they are different records (projection vs enumeration) and must not read as one continuous headcount line.

**Out**

- Leading the page with 2011 as the answer to “how many people live in India” in 2026.
- Calling a 2026 Table 8 cell a census or “India has X people” without “projection”.
- Dropping 2011 from the first screen.
