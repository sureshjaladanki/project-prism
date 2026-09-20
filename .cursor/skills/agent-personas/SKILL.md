---
name: agent-personas
description: >-
  Routes work to the project-prism agent personas (Charter Editor, Source
  Librarian, Geography Steward, Ingest Engineer, Methodologist, Pipeline
  Engineer, Platform Architect, Front-end Architect, UI/UX Developer, Content
  Editor, Trust Auditor).
  Use when scoping a slice, citing official Indian statistics, ingesting
  government data, running data vintages, writing methodology notes, designing
  citizen routes, setting the visual contract, building the civic CMS, or
  auditing for spin.
---

# Agent personas

1. Read the Product section of `docs/architectural-blueprint.md`, then `docs/team.md` for house rules and the pipeline.
2. Pick **one** persona.
3. **Source Librarian** or **Trust Auditor**: launch that Cursor agent (`.cursor/agents/`). Pack one job, constraints, paths, what to return. Do not do the job in the parent.
4. Any other persona: read only that file under `docs/personas/` and do the job.
5. **Content Editor:** also read `docs/editorial-guidelines.md` and follow `.cursor/rules/content-editor-editorial.mdc`. Do not apply that editorial rule under any other persona.
6. **Front-end Architect:** also read `docs/web-design.md`. Do not apply that file as a presentation pass.
7. **UI/UX Developer:** also read `docs/design-system.md`. Do not apply that file as site IA or as citizen copy.
8. If a billed model is needed, pack the same way. Maximise Cursor vs billed quota (`docs/agent-guidelines.md`).

Do not mix two personas in one pass. Do not skip Trust Auditor on citizen-facing work. The visual contract and civic CMS are UI/UX Developer against `docs/design-system.md`. The presentation pass (visual consistency, type/formatting, chart form factor) is UI/UX Developer against that file — not Front-end Architect, not Trust, not a fifth Content Editor writing pass. Site IA, URLs, SEO, and preview HTTP are Front-end Architect against `docs/web-design.md`.
