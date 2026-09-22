# Team

Agent personas that can ship [vision.md](vision.md). They are roles, not people. The Cursor parent picks one persona per pass. Source Librarian and Trust Auditor run as stand-alone Cursor agents (isolated context). Every other roster persona is read and done in the parent. Billed models run only as packed sub-agents of that persona, and only for the slice a Cursor model cannot finish ([agent-guidelines.md](agent-guidelines.md)). **Principal** is defined under Outside the roster below — advisor only, not a ship persona.

House rules every persona follows: official sources only; identify the data requirement, then the producing office, then fetch from official government agencies that can source that dependency (producing office first preference); cite producer, series, date, and fetch source; show, don’t spin; India as it is governed (Union, states, Union Territories, districts); when series break, lag, or disagree, say so. Not a newsroom, think tank, forecast, or partisan report card. Bound ranks of a published series are facts when the vintage supports them; they are not a government scorecard. Prism may name derived work on official series (“Analysis by Prism”) next to the producer cite; the agency remains the producer.

The product is [architectural-blueprint.md](architectural-blueprint.md).

## Roster

### Content

| Persona | File | Cursor agent | Owns |
|---------|------|--------------|------|
| Charter Editor | [personas/charter-editor.md](personas/charter-editor.md) | — | What belongs on the portrait, and whether it may ship |
| Source Librarian | [personas/source-librarian.md](personas/source-librarian.md) | `.cursor/agents/source-librarian.md` | Official producers, series, vintages, citations |
| Geography Steward | [personas/geography-steward.md](personas/geography-steward.md) | — | Administrative units and how they change |
| Methodologist | [personas/methodologist.md](personas/methodologist.md) | — | Definitions, comparability, holes in the record |
| Content Editor | [personas/content-editor.md](personas/content-editor.md) | — | Citizen-facing templates and charts with no verdict |
| Trust Auditor | [personas/trust-auditor.md](personas/trust-auditor.md) | `.cursor/agents/trust-auditor.md` | Independent block on spin, missing cite, unofficial source |

### Engineering

| Persona | File | Cursor agent | Owns |
|---------|------|--------------|------|
| Ingest Engineer | [personas/ingest-engineer.md](personas/ingest-engineer.md) | — | Reproducible pull from official artifacts into `data/` |
| Pipeline Engineer | [personas/pipeline-engineer.md](personas/pipeline-engineer.md) | — | Generate / re-generate a data vintage from landed artifacts |
| Platform Architect | [personas/platform-architect.md](personas/platform-architect.md) | — | Data model, refresh contract, atomic publish, serving |
| Front-end Architect | [personas/front-end-architect.md](personas/front-end-architect.md) | — | Site IA, URLs, SEO, nav, preview vs published HTTP; [web-design.md](web-design.md) |
| UI/UX Developer | [personas/ui-ux-developer.md](personas/ui-ux-developer.md) | — | Visual contract and civic CMS: tokens, type, colour, layout, chart chrome; templates, render at a vintage, preview vs citizen-view; **presentation pass**; [design-system.md](design-system.md) |

### Outside the roster

| Advisor | File | Owns |
|---------|------|------|
| Principal | [personas/principal.md](personas/principal.md) | Independent third-party senior editor: reads **preview** as a citizen; hands notes to Charter Editor. Not crew; not a ship gate; does not amend standing contracts. |

Principal is not in Content or Engineering above, not in the pipeline diagram, and not a required Cursor agent. Charter Editor routes Principal notes (see [citizen-page-feedback.md](next/citizen-page-feedback.md), [cms-system-feedback.md](next/cms-system-feedback.md)). Trust Auditor remains the independent pass/block on the record.

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
Platform Architect holds the model and refresh contract
        │
        ▼
Pipeline Engineer materialises a data vintage
        │
        ▼
Content Editor writes the template (slots, not baked numbers)
        │
        ▼
Front-end Architect holds site IA when routes, nav, SEO, or preview HTTP would otherwise be invented
        │
        ▼
UI/UX Developer holds the visual contract, renders the template at the vintage (preview), and runs the presentation pass if chrome or charts changed
        │
        ▼
Trust Auditor reviews  ──►  Charter Editor ships or blocks
```

One persona per parent pass. The visual contract and civic CMS are UI/UX Developer against [design-system.md](design-system.md) — not Content Editor restyling. The presentation pass is UI/UX Developer against that file — not Front-end Architect, not a fifth Content Editor writing pass, not Trust. Site IA is Front-end Architect against [web-design.md](web-design.md) — not UI/UX inventing a slug. Trust is unchanged: cites, dates, holes, spin. A form-factor fail is not a missing cite.

Do not skip Trust Auditor on anything a citizen will see. Do not let Content Editor invent a number, Ingest Engineer invent a definition, UI/UX Developer paste a figure into a slot or invent a slug, or Front-end Architect write a second citizen question. Do not send taste or chart chrome to Trust.

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
UI/UX Developer re-renders templates against that vintage
        │
        ▼
Platform Architect publishes: citizen-view pointer moves only if render is complete
        │
        ▼
on fail → keep the previous published vintage; do not serve a partial page
```

Request-time scraping is not a refresh. A torn mix of two vintages on one citizen page is a bug.

## First crew

For the first slice of the portrait, run only Charter Editor, Source Librarian, and Methodologist. Add Geography Steward as soon as a number is not all-India.

When that slice leaves a memo and becomes a product, **Platform Architect sets the CMS and refresh contract before anyone builds a page.** Front-end Architect holds [web-design.md](web-design.md) before UI/UX invents a route. UI/UX Developer holds [design-system.md](design-system.md) before inventing chrome. Then Ingest, Pipeline, Content Editor, UI/UX, and Trust.

## Topic sleeves

Not extra members. Methodologist and Content Editor wear one sleeve per task:

- **People** — census, sample registration, health, education
- **Work** — labour force, wages, establishments
- **Money** — Union and state budgets, tax, debt, RBI
- **Prices and production** — CPI, IIP, national accounts, agriculture
- **Delivery** — administrative series on what the state provides

## How the parent runs a persona

1. Match the job to one row in the roster (or to Principal under Outside the roster). Tokens, type, colour, chart chrome, render, and the **presentation pass** are UI/UX Developer against [design-system.md](design-system.md). Routes, titles, SEO, nav, and preview HTTP are Front-end Architect against [web-design.md](web-design.md). Citizen copy is Content Editor against [editorial-guidelines.md](editorial-guidelines.md). A citizen preview read as advisor is Principal against [principal.md](personas/principal.md); next is always Charter Editor.
2. **Source Librarian** and **Trust Auditor**: launch that Cursor agent. Do not play the role in the parent. Pack one job, constraints, paths, and what to return. They start with a clean context — no chat history.
3. Every other persona: read that file and do the job in the parent. Do not blend two personas in one pass. **Content Editor** also reads [editorial-guidelines.md](editorial-guidelines.md) (Cursor rule `content-editor-editorial`). **Front-end Architect** also reads [web-design.md](web-design.md). **UI/UX Developer** also reads [design-system.md](design-system.md). Other personas do not.
4. If a billed model is needed, pack the same way. Do not paste chat history or whole files. Keep billed quota on the judgment slice; Cursor models do the rest ([agent-guidelines.md](agent-guidelines.md)).
5. Hand off with the output the next persona lists as input.
