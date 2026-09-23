# Topic charters

Charter Editor catalogue of slices the portrait should run. It is a menu and a run order, not a partisan report card.

Product: [vision.md](../vision.md). Sleeves: [team.md](../team.md). First crew on each slice: Charter Editor → Source Librarian → Methodologist. Geography Steward as soon as a number is not national.

## Iteration 1 geography

We say **national**. Citation cards keep the producer’s own label if they print “all-India”.

**In:** national, states, Union Territories — as the producer publishes them.

**Parked:** districts (and below). The vision still names districts; this iteration does not ship them. If a series is district-only, do not use it to fake a state number. If a series has districts, stop at state/UT.

A slice that is national or Union-only must still say which units are missing, including districts.

## How a topic got on this list

A charter is in only if it passes all three:

1. **Citizens ask it.** Kitchen-table search: prices, jobs, tax, school, hospital, ration, power, air, safety — not cricket, bills of the week, or “how do I file”.
2. **The audience expects it.** Citizens first; then journalists, students, researchers, and people in public life who need the same official number, cited.
3. **The vision needs it.** What the state **collects**, **spends**, and **delivers**, and **how people live**. Not one national average pretending to be the country. Iteration 1 geography is Union / national, states, and UTs; districts are parked.

If it fails (1) but is required by (3), it still runs — with a note that it is a spine, not a search spike. If it passes (1) but has no official series, it does not run.

## How a number gets on a page view

Charter Editor source class ([charter-editor.md](../personas/charter-editor.md)). Every figure on a citizen page follows this, in order:

1. **Identify the data requirement** — the citizen question, geography bar, and years the slice must answer.
2. **Identify the producing office** — who published that series. Name it even when the file is fetched elsewhere.
3. **Fetch** from official government agencies that can source that dependency. Producing office first preference; any other government office (`*.gov.in`, `data.gov.in`, line ministries, NITI as a host of that table) is in if it supplies the same dependency. Not locked to the producer’s website.
4. **Quote** producer, series, date, and fetch source in the sources of that page view.

A NITI scorecard, news write-up, or international secondary database is not a government source of the dependency. When two official series both answer the requirement, the page shows both and cites both. If no official government source can supply the dependency, the page shows the hole.

If a named card cannot be extracted as spreadsheet cells and cannot be reconstructed from PDF or HTML without guessing, it does **not** block the story-shaped explainer when the remaining lineage-ok cards still answer the citizen question. Keep the card on the catalogue. Show the hole. Do not skip a card that *can* be reconstructed. Do not invent a table.

## What we take from USAFacts (role, not topics)

[USAFacts](https://usafacts.org/) is the *role* in the vision: make official data usable; do not tell people what to think. Useful habits: citizen questions, government money next to how people live, and a public note when a series is late. Live portrait of that site (not a Prism contract): [usafacts-profile.md](../usafacts-profile.md).

We do **not** copy its American chapters (immigration enforcement, Medicare/Social Security, firearms, homeland security, foreign aid, a Constitution-preamble “four missions”, a government **10-K form**). Do not substitute **SEBI LODR** as the Indian equivalent: LODR is listing disclosure for companies, not a civic filing. India’s frame is how India is governed. Union and state **accounts** (receipts, expenditure, deficit, debt as published) are C3 and C5 — Finance Accounts / CGA / CAG / FRBM, not a US form and not a stock-exchange code.

## Topic families (Indian frame)

These families sit on the five sleeves. Each family is many slices, not one page.

| Family | Sleeve | Citizen / audience pull | Vision spine |
|--------|--------|-------------------------|--------------|
| Prices in the market | Prices and production | Inflation, food, fuel, EMI context | How people live |
| People | People | Census, “how many of us”, births and deaths | How people live |
| Work and pay | Work | Jobs, unemployment, wages, public works | How people live |
| Union and state money | Money | Tax, GST, budget, deficit, debt | Collects and spends |
| School | People | Enrolment, teachers, what schools have | Live + deliver |
| Health and survival | People | Child survival, nutrition, facilities | Live + deliver |
| Food and farm | Prices and production + Delivery | Food prices, grain, PDS, harvest | Live + deliver |
| What the state delivers | Delivery | Ration, work days, power, roads, water, housing | Delivers |
| Size of the economy | Prices and production | GDP, industry — journalists and public life | Context for money and work |
| Recorded crime | Delivery (admin record) | Safety searches; NCRB is a record of cases, not a feeling | How people live (as recorded) |
| Air, water, forest | Delivery / People | AQI, forests | How people live |

## Out (do not charter)

- NITI / SDG league tables as the source of record, “best state” verdicts, partisan report cards
- News, legislation explainers, elections, party scorecards
- Forecasts, “will inflation fall”, private polls
- World Bank, IMF, UNDP, CMIE, ASER, or news tables as the source of record
- How-to services (passport, ITR filing, exam results portals)
- USAFacts-shaped topics with no Indian official spine: border enforcement, Medicare-style insurance chapters, firearms
- Defence or foreign aid as a patriotic chapter (Union defence *spend* may appear later as a budget line inside Union money)
- Ministry “achievements” pages and Economic Survey narrative (tables they reprint may be in, if the producing series is cited)

When two official series disagree, the slice shows both. It does not pick a winner.

---

## Wave 1 — prove the method

Run these three. They cover live / collect-spend, and they force honesty about geography and lag. **Run first: prices.**

### C1. Prices people pay (run first)

```text
slice:          How fast are retail prices rising in India, including food?
in:             CPI (headline and group), food index; national and states/UTs as published; recent years plus a longer comparable run if the series allows
out:            forecasts; “cheap/expensive” verdicts; city rankings; petrol pump prices that are not the CPI series; districts (parked)
source_class:   allow (MoSPI price statistics) — librarian names the exact series
next_persona:   source-librarian
```

Why: highest kitchen-table search that official statistics can answer; journalists need it on release day; states exist so the slice is not national-only.

### C2. People of India

```text
slice:          How many people live in India, where, and how is that changing?
in:             Census population at national and state/UT; Sample Registration System births, deaths, infant mortality, fertility; any official projection the librarian confirms — each shown as itself
out:            treating 2011 as current without saying so; a single “India has X people” that hides the lag; NPR / citizenship registers; caste politics; district tables (parked even if Census publishes them)
source_class:   allow — requirement → producing office → official government fetch (producer first, any government office that can source the dependency) → cite on the page ([c2-charter.md](../archive/c2-charter.md); [charter-editor.md](../personas/charter-editor.md))
next_persona:   source-librarian
```

Why: vision spine; students and public life expect it; the Census lag is a trust test — show the hole.

Geography Steward joins this slice for states/UTs. A national total that does not name missing units (including parked districts) does not ship.

### C3. Union money

```text
slice:          What does the Union collect, and what does it spend it on?
in:             Union receipts (tax, non-tax, borrowings as published); expenditure by the budget’s own heads; deficit and debt as the producer defines them; a run of years
out:            state finances (that is C5); scheme report cards; “waste / welfare” verdicts; Economic Survey prose; per-person rankings; districts
source_class:   allow — requirement → producing office → official government fetch (producer first, any government office that can source the dependency) → cite on the page
next_persona:   source-librarian
```

Why: vision “collects and spends”; journalists and public life expect it; this is the USAFacts *role* analogue, not a copy of US missions.

This slice is Union-only until C5. The page must say states, UTs, and districts are missing (districts stay missing for this iteration). Card 8 (FRBM statutory packet) is a named hole, not a block of the collect/spend explainer ([c3-charter.md](../archive/c3-charter.md)).

---

## Wave 2 — kitchen table and the states

Run after Wave 1 has citation cards and method notes. **First crew in parallel:** C4–C8 may each run Charter → Source Librarian → Methodologist (and Geography Steward when the number is not national) at the same time. There is no “run first” inside this wave. Keep slice boundaries: do not fold C5 into C3, do not mix PLFS with MGNREGA (C9), do not merge SRS and NFHS into one figure, and do not wait on C2/C3 *citizen* ship to start these cards. Product stops (catalog ingest machine, Platform refresh, preview) stay per-slice and may still serialise on shared engineering — that is not a charter serial order.

Several of these are not national. Stop at state/UT; do not ingest district files.

### C4. Work and pay

```text
slice:          How many people are working, seeking work, and what do they earn?
in:             Periodic Labour Force Survey employment, labour force, unemployment as defined; usual vs current status if both are published; wages/earnings as published; national and states/UTs
out:            CMIE; “jobless growth” verdicts; mixing PLFS with MGNREGA as if they were one unemployment rate; districts
source_class:   allow — PLFS Monthly (CWS all-India), Quarterly (CWS selected States), Annual 2025 (usual + CWS State/UT), earnings Tables 38–40. Jan 2025 design break. Thirteen series per [c4-series-expansion.md](c4-series-expansion.md). ([c4-citation-cards.md](c4-citation-cards.md); [c4-geography-frame.md](c4-geography-frame.md); [c4-method-notes.md](c4-method-notes.md); [c4-refresh-contract.md](c4-refresh-contract.md)). Vintage `dv-20260922-985274aa0a45` complete (13/13 lineage_ok).
next_persona:   content-editor
```

### C5. State money

```text
slice:          What do states and UTs collect and spend?
in:             State/UT receipts, expenditure, deficit/debt as in the official state-finance compilation the librarian names
out:            ranking states by “fiscal virtue”; treating Union grants as if they were own tax; local-body accounts; districts
source_class:   allow — RBI State Finances Study of Budgets 2025-26 (Cards 1–6); CAG CFRA glance 2020-21 (Card 7, lagged). Own tax ≠ Centre transfers. ([c5-citation-cards.md](c5-citation-cards.md); [c5-geography-frame.md](c5-geography-frame.md); [c5-method-notes.md](c5-method-notes.md); [c5-refresh-contract.md](c5-refresh-contract.md)). Catalog + parsers landed; **all 7 lineage_ok=no** (rbidocs WAF HTML; CAG glance headers not uniquely mappable). No C5 vintage until an approved fetch yields real XLSX/PDF cells.
next_persona:   ingest-engineer
```

### C6. School

```text
slice:          Who is in school, and what does the official record say about schools?
in:             UDISE (or successor) enrolment, teachers, school facilities at national and state/UT; Census/NSS literacy if cited separately
out:            ASER as source of record; board-exam result portals; “learning crisis” verdicts; ranking states; district UDISE (parked)
source_class:   allow — UDISE+ Report 2025-26 NEP (Cards 1–2); Census 2011 PCA literacy counts separate (Card 3). Still named UDISE+; no successor rename. ([c6-citation-cards.md](c6-citation-cards.md); [c6-geography-frame.md](c6-geography-frame.md); [c6-method-notes.md](c6-method-notes.md); [c6-refresh-contract.md](c6-refresh-contract.md)). Vintage `dv-20260922-37718de3c4fc` complete.
next_persona:   content-editor
```

### C7. Health and survival

```text
slice:          How do births, deaths, child survival, and nutrition stand in the official record?
in:             SRS vital rates; NFHS health and nutrition indicators at national and state/UT as published; facility counts from the health statistical system the librarian names, same geography bar
out:            mixing SRS and NFHS into one number; hospital star-ratings; private insurance products; NITI health index as the record; districts
source_class:   allow — SRS Bulletin + Statistical Report 2024 (Cards 1–2, same artifacts as C2); NFHS-6 fact sheets (Card 3, Manipur absent); RHS 2021-22 facilities (Card 4). Three records. ([c7-citation-cards.md](c7-citation-cards.md); [c7-geography-frame.md](c7-geography-frame.md); [c7-method-notes.md](c7-method-notes.md); [c7-refresh-contract.md](c7-refresh-contract.md)). Vintage `dv-20260922-06858699984f` complete (4/4 lineage_ok).
next_persona:   content-editor
```

### C8. Food and farm

```text
slice:          What does the official record say about foodgrain, and what does the public food system deliver?
in:             Agricultural production/procurement at national and state/UT as published; PDS / NFSA administrative series the librarian can cite at the same geography; keep farm output and ration delivery on separate charts
out:            a hunger index; FAO/UN as source of record; MSP as a farmer-income verdict; districts
source_class:   allow — Family A: DES AE/FE/APY + DFPD procurement + FCI stocks (Cards A1–A6); Family B: DFPD offtake/coverage + NFSA dashboard (Cards B1–B4). Separate charts. ([c8-citation-cards.md](c8-citation-cards.md); [c8-geography-frame.md](c8-geography-frame.md); [c8-method-notes.md](c8-method-notes.md); [c8-refresh-contract.md](c8-refresh-contract.md)). Vintage `dv-20260922-f095e54660d9` complete (A1–A3, A5–A6, B1–B2 lineage_ok; A4/B3/B4 named holes).
next_persona:   content-editor
```

---

## Wave 3 — delivery and the rest of living

Each is a slice, not a ministry home page. Source class is `needs librarian` until a citation card exists. Geography bar is the same: national and state/UT; districts parked.

| ID | Slice (citizen question) | Sleeve | Notes |
|----|--------------------------|--------|--------|
| C9 | How much public works employment is provided? | Delivery | MGNREGA administrative series; not a poverty verdict |
| C10 | What does the official record say about electricity? | Delivery | Generation, capacity, households as published — not a “power for all” slogan |
| C11 | What does the official record say about roads and rail? | Delivery | Transport statistics as published |
| C12 | What does the official record say about drinking water and sanitation? | Delivery | Administrative coverage series; say what “household tap” means |
| C13 | How do people live in their houses? | People + Delivery | Census housing plus any housing-scheme administrative series; show both |
| C14 | What crimes are recorded? | Delivery | NCRB is recorded crime, not “how safe”; no women-safety ranking |
| C15 | What does the official record say about air and forests? | Delivery | CPCB / forest survey as librarian cites; “AQI near me” is a product, not this slice |
| C16 | How large is the economy, and what is industry producing? | Prices and production | GDP/GVA, IIP; journalist spine; not the citizen homepage hero |
| C17 | What taxes do people and firms pay into the Union? | Money | Income tax and GST *receipts* as published; not filing advice or slab explainers |
| C18 | What does the banking system report about deposits and credit? | Money | RBI monetary and banking statistics |
| C19 | How many establishments exist, and of what kind? | Work | Economic Census; if delayed, the slice is the delay |
| C20 | How do people move inside India? | People | Census/NSS migration; not a border-security chapter |

---

## Later, only with a fresh charter

Do not start these until Wave 1–2 are shipping:

- **Districts** (parked for this iteration) — Census, UDISE, NCRB, scheme MIS, and any other district file. Needs Geography Steward before Ingest.
- Disability, age structure, urbanisation (Census/SRS detail)
- SC/ST tables as published Census/ministry statistics — facts, not a campaign
- Defence spend as a line inside Union money, not a chapter
- Disasters, monsoon as climatology if IMD/NDMA publish a series we can cite
- Pensions and social-security *administrative* counts
- Local governments (rural/urban local bodies) if a comparable official series exists

## Search spikes we will not chase

| People search | We run | We do not run |
|---------------|--------|----------------|
| Inflation, tomato, petrol | C1 | Price tips, forecasts |
| Naukri, unemployment | C4, C9 | Job portals, “sarkari naukri” lists |
| ITR, GST, tax slab | C3, C17 | Filing how-to |
| GDP, fiscal deficit | C3, C5, C16 | “Is the economy good” |
| Census, population | C2 | NPR/citizenship politics |
| School, results | C6 | Exam portals |
| Hospital, vaccine, stunting | C7 | Hospital ads, rankings |
| Ration, Atta, PDS | C8 | Entitlement calculators |
| AQI near me | C15 (national / state record) | Live pin-map; district AQI |
| Crime, women safety | C14 | Vigilante lists, ranking “safest city” |
| Waqf bill, elections, IPL | — | News and sport |

## Next

C1 has cards ([c1-citation-cards.md](../archive/c1-citation-cards.md)). C1 Trust passed; Charter ships the preview vintage — see [c1-charter-verdict.md](../archive/c1-charter-verdict.md).

C2 cards exist ([c2-citation-cards.md](../archive/c2-citation-cards.md)); C2 product stop is ingest (see [c2-refresh-contract.md](../archive/c2-refresh-contract.md)). Do not unblock C2 from this file.

C3 cards exist ([c3-citation-cards.md](../archive/c3-citation-cards.md)). Charter: proceed with reconstructable cards; Card 8 stays a named hole ([c3-charter.md](../archive/c3-charter.md)). Product stop is Platform completeness + ingest of those tables — not “wait for FRBM as a grid.” Do not unblock C3 citizen-view from this file.

Wave 2 machine path (catalog → ingest → vintage): **C4, C6, C7, C8 complete**; **C5 catalog+parsers landed but no vintage** (rbidocs WAF; CAG glance headers). Vintages: C4 `dv-20260922-985274aa0a45`, C6 `dv-20260922-37718de3c4fc`, C7 `dv-20260922-06858699984f`, C8 `dv-20260922-f095e54660d9`. Next per complete slice: Content Editor templates — **stop before** UI/UX citizen chrome, Trust, and `citizen_pointer`. Do not start Wave 3 until Charter opens that gate.



