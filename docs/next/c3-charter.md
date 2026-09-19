# C3 charter

Charter Editor. Wave 1 slice **C3**. C1 ship is a separate track ([c1-charter-verdict.md](c1-charter-verdict.md)). C2 product stop remains ingest ([c2-refresh-contract.md](c2-refresh-contract.md)); this note does not unblock C2 and does not ship C3.

Catalogue: [topic-charters.md](topic-charters.md). Cards: [c3-citation-cards.md](c3-citation-cards.md). Method: [c3-method-notes.md](c3-method-notes.md).

```text
slice:          What does the Union collect, and what does it spend it on?
in:             Union receipts (tax, non-tax, borrowings as published); expenditure by the budget’s own heads; deficit and debt as the producer defines them; a run of years. Fetch from official government agencies that can source that dependency (producing office first preference, not the only host). Quote producer, series, date, and fetch source in the sources of the page view.
out:            state finances (that is C5); scheme report cards; “waste / welfare” verdicts; Economic Survey prose; per-person rankings; districts; SEBI LODR; a US 10-K or USAFacts “four missions” frame; World Bank / IMF / credit-rating tables as the source of record; NITI scorecards as the record
source_class:   allow — requirement → producing office → official government fetch (producer first, any government office that can source the dependency) → cite on the page. Deny a fetch with no producer named. Deny a number with no cite on the page view.
next_persona:   platform-architect (named-hole completeness for Card 8), then ingest on reconstructable cards
block_reason:   none. Do not treat this as a ship of C3. Do not pull district files. Do not ingest state Finance Accounts. Do not invent a Card 8 table.
```

## Decision

**Move the collect/spend explainer on the cards that have a table. Keep Card 8 as a named hole.**

The citizen question is still answerable without reconstructing Card 8 as a grid. Do not shrink the eleven series: Card 8 stays on the catalogue and on the page as unknown / not a table. Do not drop reconstructable cards (xlsx or unambiguous PDF/HTML) to go faster.

House rule (also in [topic-charters.md](topic-charters.md)): if a named card cannot be extracted as spreadsheet cells and cannot be reconstructed from PDF or HTML without guessing, that card does **not** block the story-shaped explainer when the remaining lineage-ok cards still answer the H1. The hole stays visible. Reconstructable cards are not skipped.

On C3 that means:

| Need for the H1 | Cards | Status for the explainer |
|-----------------|-------|--------------------------|
| What the Union collects | 1, 2, 3, 4 | Tables of record (xlsx or reconstructed PDF) |
| What it spends | 5, 9 | Tables of record (xlsx or reconstructed PDF) |
| Deficit and debt as printed | 6, 7 | Tables of record (xlsx or reconstructed PDF) |
| Run of years | 4 | Reconstructed PDF |
| Three records (Budget / monthly / Finance Accounts) | 9–11 with 10 | Reconstructed PDF/HTML |
| FRBM statutory packet | 8 | **Hole.** Prose, not a grid. Not a block. |

Missing if Card 8 stays unrestored: Macro-Economic Framework; Medium-term Fiscal Policy / Fiscal Policy Strategy; deviation statement; FRBM labels as printed (3% / 40% / 60% wording, producer % of GDP as statement text). Not missing: collect, spend, deficit statistics, outstanding liabilities.

Do not print page 9 “Economic Performance at a Glance” as Card 8. Do not turn FRBM wording into a Prism grade. Do not wait for C2 ingest to unblock.

This is not a ship. Platform must let a C3 vintage proceed when Card 8 is a named hole and the H1 cards above are `lineage_ok: yes`. Ingest still lands those reconstructable tables. Content Editor still names the hole. Trust still runs before citizen-view.

## How this page gets its numbers

House rule ([topic-charters.md](topic-charters.md), [vision.md](../vision.md)):

1. **Identify the data requirement** — Union receipts (tax, non-tax, borrowings), expenditure by the budget’s own heads, deficit and debt as the producer defines them, a run of years; Union-only; states/UTs/districts missing.
2. **Identify the producing office** — Ministry of Finance, Budget Division (Union Budget); Controller General of Accounts (monthly accounts and Union Finance Accounts). Name it even when the file is fetched elsewhere.
3. **Fetch** from official government agencies that can source that dependency. Producing office first preference. Another government office (`data.gov.in`, a ministry, CAG as a host of the Union Finance Accounts table, NITI as a host of that table, RBI only if it is the named table of record) is in if it supplies the **same** table.
4. **Quote** producer, series, date, and fetch source in the sources of the C3 page view. Every number on the page still traces to a citation card.

A companion xlsx on `indiabudget.gov.in` is in when it is the **same** Budget 2026-27 statement (same heads, same year columns). Unambiguous PDF/HTML reconstruction of the **same** table is in when no spreadsheet of that vintage exists. It is not a substitute for a different table, a stale year workbook (`allafs.xlsx`), or a 404 `.xls`. If the artifact cannot be read as cells without guessing, the card stays a named hole.

RBI Handbook / DBIE Union fiscal tables are allowed only if named as the table of record for that requirement. They are not a silent substitute when the Budget or CGA file exists but is not cell-mapped.

## Allow / deny

**Allow**

- Union Budget / Controller General of Accounts / Controller of Accounts figures the librarian can cite as the producing series
- A producing-office spreadsheet or CSV of the **same** statement already on the cards
- Unambiguous reconstruction of that same PDF/HTML table (ingest stops if a number could sit in two columns)
- Another official government host of that same table (`*.gov.in`, `data.gov.in`, CAG as host of Union Finance Accounts)
- RBI compilation of Union fiscal aggregates only if the librarian names it as the source of record for that table (not as a substitute when the Budget/CGA file is late or not cell-mapped)
- Finance Accounts / CAG statistical annexes for Union only, if they are the producer’s table of record
- Deficit and debt as the producer defines them (FRBM labels as printed — not a Prism score)
- Bound ranks of a published Union series only when the citizen question is a rank question and the vintage can bind them (this slice is not a state rank)
- Moving the explainer with Card 8 as a named hole, once the H1 cards have tables

**Deny**

- A retrieve with no producing office
- A number on the page view with no source quote
- Inventing a Card 8 receipts/expenditure/deficit/debt grid
- Skipping a reconstructable card because Card 8 is hard
- State / UT finances (C5)
- Local-body accounts
- District tables
- Scheme MIS report cards and ministry “achievements” pages
- Economic Survey narrative (tables they reprint only if the producing Budget/CGA series is cited)
- “Waste / welfare” verdicts; per-person rankings
- SEBI LODR; USAFacts mission chapters; a government 10-K form
- World Bank / IMF / credit-rating tables as the source of record
- NITI scorecards / composite league tables
- Using a different series, year, or table as if it were the named Budget/CGA statement

## Next

**Platform Architect** on C3 refresh completeness: a named unreconstructable hole (Card 8) must not fail the slice vintage when the H1 series are `lineage_ok: yes`. The vintage still lists all eleven; Card 8 is unknown / not a table, not omitted. Do not move `citizen_pointer`.

**Ingest Engineer** lands tables for Cards 1–7 and 9–11. Card 8 stays `lineage_ok: no` with the FRBM prose flag.

Geography Steward waits unless printed Union labels change. Content Editor after a bindable vintage — name the Card 8 hole in method; do not fake a table. Trust Auditor before anything a citizen sees.
