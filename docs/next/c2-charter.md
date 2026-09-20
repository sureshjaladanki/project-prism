# C2 charter

Charter Editor. Opens Wave 1 slice **C2** for first crew. C1 in/out/source_class unchanged. C1 ship is a separate track ([c1-charter-verdict.md](../archive/c1-charter-verdict.md)). This note does not unpublish C1 and does not ship C2.

Catalogue: [topic-charters.md](topic-charters.md). C1 cards (the gate): [c1-citation-cards.md](c1-citation-cards.md).

```text
slice:          How many people live in India, where, and how is that changing?
in:             Census population at national and state/UT as published; Sample Registration System births, deaths, infant mortality, fertility as published; any official projection the librarian confirms — each series shown as itself. Fetch from official government agencies that can source that dependency (producing office first preference, not the only host). Quote producer, series, date, and fetch source in the sources of the page view.
out:            treating 2011 as current without saying so; a single “India has X people” that hides the lag or blends Census, SRS, and projections; NPR / citizenship registers; electoral rolls; caste politics; district tables (parked even if Census publishes them); World Bank / UN as source of record; NITI scorecards as the record
source_class:   allow — requirement → producing office → official government fetch (producer first, any government office that can source the dependency) → cite on the page. Deny a fetch with no producer named. Deny a number with no cite on the page view.
next_persona:   ingest stays on named cards. Librarian only when a new data requirement needs a producing office named.
block_reason:   none. Do not treat this as a ship of C2. Do not pull district files.
```

## Decision

**Start C2 first crew.** Topic charters already put this slice in Wave 1. The hold was “until C1 has cards.” C1 has cards. Librarian on C2 may run as its own job. Do not wait for C1 to ship.

C2 is a vision spine, not a search spike: the Census lag is the trust test. Show the hole. Do not paper a 2011 count into a current headcount.

Geography Steward joins after the librarian names series that are not all-India. A national total that does not name missing units (including parked districts) does not ship.

Census, SRS, and any official projection are three records. The page shows each as itself. It does not pick a winner or invent a blended “India today” figure.

## How this page gets its numbers

House rule ([topic-charters.md](topic-charters.md), [vision.md](../vision.md)):

1. **Identify the data requirement** — headcount, change over time, births/deaths/IMR/fertility, official projection; national and state/UT; districts parked.
2. **Identify the producing office** — ORGI (Census, SRS); NCP / MoHFW (Technical Group projections). Name it even when the file is fetched elsewhere.
3. **Fetch** from official government agencies that can source that dependency. Producing office first preference. Card 5 already fetches the NCP/MoHFW report from `nhm.gov.in`. Another government office (`data.gov.in`, a ministry, NITI as a host of that table) is in if it supplies the same table.
4. **Quote** producer, series, date, and fetch source in the sources of the C2 page view. Every number on the page still traces to a citation card.

If no official government source can supply a post-2011 census total, that requirement is a hole. Another government office may host the Census/SRS/projection table. It may not put a different series on the page as if it were the census.

## Allow / deny

**Allow**

- Census / ORGI population as published at national and state/UT
- SRS vital rates (births, deaths, infant mortality, fertility) as published at the same geography bar
- Official projections only if the librarian can cite the producing office, the vintage, and the table — labelled as projections, not as a census
- Bound ranks of a published population or rate when the citizen question is a rank question and the vintage can bind them
- Fetch from any official government office that can source the named dependency; producing office first preference

**Deny**

- A retrieve with no producing office
- A number on the page view with no source quote
- NPR, NRC, or citizenship registers
- Electoral rolls as a population count
- International secondary databases as the source of record
- District PCA or any district file this iteration
- One headline number that hides which series and which year
- Caste politics; NITI / composite scorecards / SDG league tables
- Ministry “achievements”, press prose, or a dashboard without a producing series
- Using a different series as if it were the census (UIDAI, rolls, CRS implied population, NITI composites)

## Next

C2 cards already follow this rule. Ingest stays on those artifacts. A new data requirement (a new producer and table, shown as itself) is a librarian job and a charter delta.
