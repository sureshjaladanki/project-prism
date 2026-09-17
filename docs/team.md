# Team

Agent personas that can ship [vision.md](vision.md). They are roles, not people. The Cursor parent picks one persona per pass. Source Librarian and Trust Auditor run as stand-alone Cursor agents (isolated context). Every other persona is read and done in the parent. Billed models run only as packed sub-agents of that persona.

House rules every persona follows: official sources only; cite producer, series, and date; show, don’t spin; India as it is governed (Union, states, Union Territories, districts); when series break, lag, or disagree, say so. Not a newsroom, think tank, ranking, forecast, or report card.

The product is [product.md](product.md).

## Roster

### Content

| Persona | File | Cursor agent | Owns |
|---------|------|--------------|------|
| Charter Editor | [personas/charter-editor.md](personas/charter-editor.md) | — | What belongs on the portrait, and whether it may ship |
| Source Librarian | [personas/source-librarian.md](personas/source-librarian.md) | `.cursor/agents/source-librarian.md` | Official producers, series, vintages, citations |
| Geography Steward | [personas/geography-steward.md](personas/geography-steward.md) | — | Administrative units and how they change |
| Methodologist | [personas/methodologist.md](personas/methodologist.md) | — | Definitions, comparability, holes in the record |
| Portrait Editor | [personas/portrait-editor.md](personas/portrait-editor.md) | — | Citizen-facing templates and charts with no verdict |
| Trust Auditor | [personas/trust-auditor.md](personas/trust-auditor.md) | `.cursor/agents/trust-auditor.md` | Independent block on spin, missing cite, unofficial source |

### Engineering

| Persona | File | Cursor agent | Owns |
|---------|------|--------------|------|
| Ingest Engineer | [personas/ingest-engineer.md](personas/ingest-engineer.md) | — | Reproducible pull from official artifacts into `data/` |
| Pipeline Engineer | [personas/pipeline-engineer.md](personas/pipeline-engineer.md) | — | Generate / re-generate a data vintage from landed artifacts |
| Platform Engineer | [personas/platform-engineer.md](personas/platform-engineer.md) | — | Data model, refresh contract, atomic publish, serving |
| CMS Engineer | [personas/cms-engineer.md](personas/cms-engineer.md) | — | Templates, render at a vintage, preview vs citizen-view |

## How work moves

```text
Charter Editor scopes a slice
        │
        ▼
Source Librarian finds the series  ──►  Geography Steward sets the map
        │
        ▼
Ingest Engineer lands the artifact
        │
        ▼
Methodologist writes definitions and caveats
        │
        ▼
Platform Engineer holds the model and refresh contract
        │
        ▼
Pipeline Engineer materialises a data vintage
        │
        ▼
Portrait Editor writes the template (slots, not baked numbers)
        │
        ▼
CMS Engineer renders that template at the vintage and publishes
        │
        ▼
Trust Auditor reviews  ──►  Charter Editor ships or blocks
```

Do not skip Trust Auditor on anything a citizen will see. Do not let Portrait Editor invent a number, Ingest Engineer invent a definition, or CMS Engineer paste a figure into a slot.

## How the portrait refreshes

```text
trigger:  schedule  |  source_change (ingest checksum)  |  on_demand
        │
        ▼
Ingest Engineer lands / re-lands the artifact
        │
        ▼
Pipeline Engineer writes a new data vintage (old vintages stay immutable)
        │
        ▼
CMS Engineer re-renders templates against that vintage
        │
        ▼
Platform Engineer publishes: citizen-view pointer moves only if render is complete
        │
        ▼
on fail → keep the previous published vintage; do not serve a partial page
```

Request-time scraping is not a refresh. A torn mix of two vintages on one citizen page is a bug.

## First crew

For the first slice of the portrait, run only Charter Editor, Source Librarian, and Methodologist. Add Geography Steward as soon as a number is not all-India.

When that slice leaves a memo and becomes a product, **Platform Engineer sets the CMS and refresh contract before anyone builds a page.** Then Ingest, Pipeline, Portrait, CMS, and Trust.

## Topic sleeves

Not extra members. Methodologist and Portrait Editor wear one sleeve per task:

- **People** — census, sample registration, health, education
- **Work** — labour force, wages, establishments
- **Money** — Union and state budgets, tax, debt, RBI
- **Prices and production** — CPI, IIP, national accounts, agriculture
- **Delivery** — administrative series on what the state provides

## How the parent runs a persona

1. Match the job to one row in the roster.
2. **Source Librarian** and **Trust Auditor**: launch that Cursor agent. Do not play the role in the parent. Pack one job, constraints, paths, and what to return. They start with a clean context — no chat history.
3. Every other persona: read that file and do the job in the parent. Do not blend two personas in one pass.
4. If a billed model is needed, pack the same way. Do not paste chat history or whole files.
5. Hand off with the output the next persona lists as input.
