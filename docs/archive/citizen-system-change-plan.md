# Citizen system change plan

Charter Editor. Adopted 2026-09-21 from a packed architectural, web-design, and UI/UX review (Claude Opus; judgment only, no code). Gaps: [citizen-page-feedback.md](citizen-page-feedback.md). Tone: [design-philosophy.md](../design-philosophy.md). Machine: [architectural-blueprint.md](../architectural-blueprint.md). IA: [web-design.md](../web-design.md). House: [design-system.md](../design-system.md).

This is the standing programme for those gaps. It coordinates; it does not replace [catalog-ingest-pipeline-plan.md](../next/catalog-ingest-pipeline-plan.md) or [web-app-execution-plan.md](../next/web-app-execution-plan.md). Closed look work stays in [ui-ux-change-plan.md](ui-ux-change-plan.md).

```text
verdict:        Track A signed; F-rows closed (2026-09-21); stop before B3
tone_source:    docs/design-philosophy.md (never edited in this programme)
publish:        none — do not flip citizen_pointer
next_persona:   stop
```

One persona per parent pass. Trust Auditor and Source Librarian launch as Cursor agents; do not play them in the parent.

---

## 0. Verdict

**Keep the machine.** Ingest → vintage → render → publish, vintage immutability, the desk pointer, Astro SSG, and the nine tests stay. Nothing the principal recorded traces to that spine.

**One architectural move: a citizen projection at bind.** Today `src/prism/template_bind.py` holds the full librarian citation and the full caveat note, so every citizen improvement is a subtraction in Python — and it re-leaks on the next slice. Typed page-facing records (`CitizenCite`, `CitizenMethod`, `DisplayValue`, `CitizenGeography`) make the renderer *incapable* of printing a desk field.

**Why the page still reads as a codebook** (not a look problem):

1. Bind sees the archive. `_caveat_block_html` dumps every `CaveatNote` field, including `do_not`, under “How to read this series”.
2. Two sources of gap copy: `_slot_html` hardcodes `"unknown / not a table"` while `miss_copy` already defaults to `"not published"`.
3. Compact K / L / Cr (Charter ruling 6) has no home in the contract. `format_bound_number` groups Indian-style and stops.
4. `CITE_BLOCKS` is per-template identity living in Python. The catalog plan recorded it and deferred it; at twenty charters it is the bottleneck.

**Not a re-architecture.** Catalog Track A remaining (shape-named parsers/mappers, A5 accuracy gate) stays in its own plan and runs in parallel. Catalog B1/B2 (desk pointer, desk owns binding) have largely landed in code; this programme only ticks the plan file. Catalog B3 (multi-slice citizen publish) is out of scope. Geography pages stay reserved, not built.

---

## 1. System architecture (Platform Architect)

### Stay

Two stages. Python batch under `src/prism/`, Astro under `src/cms/`. DuckDB only at render against exactly one vintage. Citizen HTTP is static files. Desk is the publish unit: one `(template_id, vintage_id)` per slice; each page one vintage. One vintage runner (`materialise_vintage`) and one ingest runner already exist. Cards are YAML under `src/prism/catalog/cards/`. Nine tests stay nine; new assertions sit beside them.

### Change (contracts)

Projections are built at bind from a vintage. They are not stored as a second vintage. Vintage records stay complete.

```text
CitizenCite          projection of Citation
  producer           office, linked via url
  series             as the producer names it
  reference_period
  released           human date (Asia/Kolkata)
  caveat             one readable paragraph
  absent:            citation id, geography_as_published, geography_vintage,
                     vintage_id, next_release, parser name, table/frame label

CitizenMethod        projection of CaveatNote; one block per page
  what_it_counts
  coverage
  break_note         optional
  lag_note           optional
  absent:            do_not and every other desk field

CaveatNote           vintage record, one new field
  citizen_note       NEW — Methodologist, in catalog caveat YAML
  do_not             stays; desk only; no projection carries it

DisplayValue         bind-time, ruling 6 + cms ruling 1
  raw_value          as published
  unit               producer-printed, unchanged
  display_scale      none | K | L | Cr — once per (page, concept)
  display_string     only citizen number string (scale + Cr when unit is crore);
                     never "L crore" / "L Thousand"; or "not published"
  status             Observation.status; non-published → chart value null
  chart_value        scaled magnitude; null when not published

CitizenGeography     land now so S3 needs no schema change later
  geography_label    "India", "Kerala"
  geography_slug     reserved for /{sleeve}/{slice}/{geo}
  geography_vintage  desk-only; the geography-vintage test stays
```

Scale is chosen per concept per page from the largest magnitude in the bound set. Rates and indices take `display_scale: none`. Chart axes use the same scale as the stat row.

**Observation status into the chart.** Bound chart data emits `value: null` for any non-published status. Vega `invalid: "break-paths"` is necessary and insufficient: if bind hands a zero, the chart draws a zero. New test: a hole is never plotted as zero (GST Compensation Cess is the fixture).

**Cite identity.** `CITE_BLOCKS` moves to `src/prism/catalog/slices/{slice}.yaml` as a list of cite ids — identity, never instruction. Bind resolves catalog id → vintage citation → `CitizenCite`. Adding a fourth slice needs no Python edit. This is the deferred item from catalog B2’s out-of-scope note, not catalog B2 itself (B2 is desk binding, already in code).

**Ingest accuracy gate.** Stays with Ingest Engineer (ruling 8). Golden fixtures under `tests/`. Catalog plan A5. Runs at ingest, offline, never at render.

### Do not change

Vintage immutability. `desk_id_rule`. Two stages. No request-time fetch. Catalog YAML as identity only. No twelfth persona. No merged desk vintage.

---

## 2. Web design (Front-end Architect)

The standing shape holds and follows the philosophy: sleeve → slice, one question one URL, scan path is region order on that URL (no `/how-it-is-measured` split). Home is the glance (Purpose sentence + `.fast-facts`). Cite chrome is not a route. No new page types.

### Amend `docs/web-design.md` (phase D1)

| Stale line | Yields to |
|------------|-----------|
| Inclusion table: citizen slice bind uses `bound_vintage_id` as the citizen pointer | Blueprint: binding is a desk field; pointer names a `desk_id` |
| On-disk tree `data/renders/{vintage_id}/` (also Published vs preview) | Blueprint: `data/renders/{desk_id}/` |
| (keep) Home `.hottest-rail` forbid | Standing; design-system must not re-specify |

DuckDB may still alias a query column `bound_vintage_id` as the page vintage. That is a query alias, not a template field. Say so or stop naming it.

### Geography reservation (ruling 7, now)

One contract sentence, no folders: `/{sleeve}/{slice}/{geo}` is a full slice (own question, fact-lede, cite), never a doorway; `{geo}` is `CitizenGeography.geography_slug`. Geography Steward signs; no build this wave.

### Still owed, not this programme

`robots.txt` and sitemap on the citizen prefix wait for a second published slice ([web-app-execution-plan.md](../next/web-app-execution-plan.md) Phase 4). This programme does not flip the pointer.

---

## 3. UI/UX (UI/UX Developer)

v3 already delivers the house: three grounds, two voices, answer band, cite within 600px of `main`, `theme.ts` tokens (`fitWidth` 974, `minScale` 1, `barStep` 26). Phase E of the archived UI/UX plan is closed. Do not redo it.

### Clash A — well vs first chart

“Well” was doing two jobs. Philosophy guideline 5 is **alignment**: lede, stats, cite, and the first chart share a left and right edge. Design-system v3 is **ground**: the answer band sits on `--well`; evidence sits on `--card`. Both survive.

**Ruling: the well is a ground, not a column.** The first chart shares the answer column’s edges (`--desk`) and sits on `--card` below the band. `docs/design-system.md` takes one sentence. `docs/design-philosophy.md` does not change.

### Remaining presentation work (not a new house)

- Cite dump was schema. `_citizen_citation_dl` is already the five citizen fields. Close `_caveat_block_html`; do not restyle the leak.
- Compact units arrive as `DisplayValue.display_string`. This file only guarantees the string fits.
- GST zero is observation status, not a Vega restyle.
- Method quieter: answer H2 ≥ 1.4× method H2; method never uses `--well`; method prose at `--measure`. Keep method heading in Serif (two voices).
- Remove `chart.titleSize` / `subtitleSize` (14 / 11) from `theme.ts`. Titles live in HTML figcaption; SVG text stays ≥ 12px.
- In-text `popover` already matches Interaction. Test: every `in-text-cite` target resolves to an on-page card with the same id. It must not replace the card.

Measurable boxes for compact units: axis ticks ≥ 12px, ≤ 9 characters, no truncation, no rotation at `fitWidth` 974; same `display_scale` on axis and stat row.

---

## 4. Clash rulings (Charter)

`docs/design-philosophy.md` wins on tone and idea and is **never edited**. `docs/architectural-blueprint.md` wins on the batch contract.

| Id | Clash | Ruling | Changes | Yields |
|----|-------|--------|---------|--------|
| A | Well vs first chart | Well is a ground, not a column. Chart is edge-aligned on `--card`. | [design-system.md](../design-system.md) | design-system wording → philosophy guideline 5 |
| B | Home featured-question rail | Standing forbid holds. Home = Purpose + `.fast-facts`. Rail is slice-only. | [design-system.md](../design-system.md) Publisher front | design-system → [web-design.md](../web-design.md) |
| C | Vintage labels on collapsed card | Ruling 3: producer (linked), series, period, released, one caveat. `geography_vintage` / `vintage_id` are not citizen labels. The geography-vintage **test** stays. | [editorial-guidelines.md](../editorial-guidelines.md) line 25 | editorial → ruling 3 and design-system |
| D | `bound_vintage_id` / `renders/{vintage_id}` | Blueprint wins. | [web-design.md](../web-design.md) | web-design → blueprint |
| E | Gap copy | Ruling 5: one phrase, **not published**. `miss_copy` is the only source. | `template_bind.py` `_slot_html`; design-system names the primitive | hardcoded `"unknown / not a table"` |
| F | Caveat blob with `do_not` | Ruling 2: one `CitizenMethod` block. Desk notes never reach bind. | `schema.py`, data-contracts, `_caveat_block_html` | field-dump helper; `do_not` stays on the caveat card |
| G | Compact K/L/Cr unspecified | Ruling 6: bind, per concept per page; vintage `unit` untouched; rates/indices `none`. | data-contracts (`DisplayValue`); design-system (fit/axis) | neither; both gain text |
| H | Stale catalog checkboxes | Code is the truth. A1, A4, B1, B2 largely landed. Cite-identity is this programme (deferred from B2 out-of-scope). | [catalog-ingest-pipeline-plan.md](../next/catalog-ingest-pipeline-plan.md) | plan file → code |

Charter rulings 1–9 in [citizen-page-feedback.md](citizen-page-feedback.md) stand. This file does not invent a second vision.

---

## 5. Execution

Different contracts do not share a commit. One owner per phase; parties sign or act, they do not co-write.

| Track | Contract | Relation to existing plans |
|-------|----------|----------------------------|
| **D** | Doc amendments recording §4 | New, first, so later phases quote true files |
| **C** | Citizen surface (projection, bind, chrome, copy, audit) | New |
| **A** | Ingest/vintage machine remaining | Continues catalog Track A in parallel with C |
| **B** | Desk publish | B1/B2 landed (tick in D4). B3 out of scope. Cite-identity deferred item runs as C4 |

### Order (why it differs from the feedback file)

Feedback order was Methodologist → Platform → Ingest/Pipeline → Content → UI/UX → Trust.

1. **Track D first** — three later phases quote files that are currently wrong.
2. **Platform’s empty shape before Methodologist writes** — otherwise citizen caveats are rewritten to fit a field they never saw.
3. **UI/UX twice** — primitives before Content (C5), presentation pass after real copy (C7). Not one restyle sandwiching the writer.

Trust after any citizen-facing preview. Charter ship/block last. **No pointer flip.**

---

### Track D — contract amendments

#### D1 — Desk contract in web design

- **Owner:** Front-end Architect
- **Signs:** Platform Architect, Geography Steward, Charter Editor
- **Files:** `docs/web-design.md`
- **Done when:** inclusion table names desk binding and the `desk_id` pointer; on-disk tree is `data/renders/{desk_id}/`; no line claims `bound_vintage_id` is the citizen pointer; geography reservation names `geography_slug` and “full slice, never a doorway”.
- **Depends on:** nothing
- **Out of scope:** routes, 404 body, robots, sitemap, any new page type
- **Size:** S
- **Covers:** S3, S3-frame (reservation)

#### D2 — Design system v3.1

- **Owner:** UI/UX Developer
- **Signs:** Front-end Architect, Charter Editor
- **Files:** `docs/design-system.md`
- **Done when:** Publisher-front rail sentence is gone (B); first chart is edge-aligned to `--desk` on `--card` (A); compact-unit fit and same-scale-on-axis rules exist (G); not-published primitive is named (E); chart titles live in HTML figcaption with 12px SVG floor; method-quieter box is written (answer H2 ≥ 1.4× method H2; method never on `--well`; prose at `--measure` ≤ 68ch).
- **Depends on:** D1 (must not re-specify the home-rail forbid or 404)
- **Out of scope:** new tokens for taste; Phase E; re-specifying 404
- **Size:** S
- **Covers:** S1, S2-type

#### D3 — Editorial cite surface

- **Owner:** Content Editor (also `.cursor/rules/content-editor-editorial.mdc`)
- **Signs:** Charter Editor, Methodologist
- **Files:** `docs/editorial-guidelines.md`
- **Done when:** line 25 no longer places geography vintage or data vintage on the collapsed card; citizen cite surface matches ruling 3; gap phrase “not published” is house copy.
- **Depends on:** D2
- **Out of scope:** rewriting template copy (C6)
- **Size:** S
- **Covers:** clash C

#### D4 — Reconcile the catalog plan with code

- **Owner:** Platform Architect
- **Signs:** Charter Editor
- **Files:** `docs/next/catalog-ingest-pipeline-plan.md`
- **Done when:** A1, A4, B1, B2 are ticked with a one-line note of what landed; a note points cite-identity (`CITE_BLOCKS`) at C4 in this file; no third plan is created.
- **Depends on:** nothing
- **Out of scope:** rewriting the catalog plan; opening Track B3
- **Size:** S
- **Covers:** clash H

---

### Track C — citizen surface

#### C1 — Define the projection

- **Owner:** Platform Architect
- **Signs:** Methodologist, UI/UX Developer
- **Files:** `docs/data-contracts.md`, `src/prism/schema.py` (generated TS types follow)
- **Done when:** `CitizenCite`, `CitizenMethod`, `DisplayValue`, `CitizenGeography` exist as in §1; `CaveatNote` gains `citizen_note` and keeps `do_not`; a test asserts no projection type can carry `do_not`, a citation `id`, `geography_vintage`, `vintage_id`, a parser name, a frame label, or a table label; observation `status` is the only source of a hole, with chart value null.
- **Landed (2026-09-21).** `CitizenCite`, `CitizenMethod`, `DisplayValue`, `CitizenGeography` in `schema.py` / data-contracts; `CaveatNote.citizen_note`; projector types cannot carry `do_not`.
- **Follow-up (2026-09-21).** T-cite-period: bind emits one `CitizenCite` per `(citation_id, observation period)`. Same catalog id for July Final and August Provisional is two cards / two HTML ids (`cite-{id}--{period}`). In-text cites target the citation’s own `reference_period` (August on C1). `observation_slots` on C1 latest blocks. `citizen_pointer` untouched.
- **Depends on:** D1, D2, D3
- **Out of scope:** mutating `Observation`; vintage immutability; desk record; renderer HTML in this commit
- **Covers:** P2-schema, P5.a-contract, S3-catalog, E-table-8 (forbidden by type)

#### C2 — Author citizen caveats

- **Owner:** Methodologist
- **Signs:** Charter Editor
- **Files:** `src/prism/catalog/cards/caveats/*.yaml` (add `citizen_note` beside existing `do_not`; keys today: `caveat_id`, `concept`, `unit`, `population`, `reference_period`, `producer_definition`, `comparable_from`, `breaks`, `lags`, `disagrees_with`, `do_not`); method notes in `docs/next/c{1,2,3}-method-notes.md` (archive copies exist if next copies are desk-only)
- **Done when:** every caveat card used by C1–C3 has a `citizen_note` a person can read; `do_not` text is unchanged; the rule “a citizen caveat says what the number is, never what a ministry should do” is written once; method notes mark citizen vs desk sentences.
- **Depends on:** C1
- **Out of scope:** rewriting `do_not`; writing page copy; filling FRBM from a non-table
- **Size:** M
- **Covers:** P2-caveat, P5-leak (source split), P1-compare (comparability in `citizen_note`), E-frbm, E-c2-units (producer unit note)

#### C3 — Vintage status and units

- **Owner:** Pipeline Engineer
- **Signs:** Platform Architect, UI/UX Developer, Trust Auditor (on the new test)
- **Files:** mapper modules `src/prism/pipeline/c1.py`, `c2.py`, `c3.py` (until A-r2 renames them); chart bind path that currently can emit a numeric zero for a gap
- **Done when:** a gap observation has non-published `status` and `value` null, never `0`; every bound stat carries `unit` from the observation; the new “hole is never plotted as zero” test fails a GST Compensation Cess zero and passes a null; existing “blank is not zero” and “no bare float” tests still pass.
- **Landed (2026-09-21).** Mapper `c3-observations-1.2.0`: GST Compensation Cess BE 2026-27 is `0.0` in `tr.xlsx`; mapped to `unknown` / null. Vintage `dv-20260921-1fa96ad12e48`. Do not mutate `dv-20260918-846e99d0ca57`. Also rematerialised C1 `dv-20260921-6a5d23d42462` and C2 `dv-20260921-a5acccd33f2e` after librarian cards. Pointers untouched.
- **Depends on:** C1
- **Out of scope:** HTML/CSS; compact display strings (C4); renaming modules (A-r2)
- **Size:** M
- **Covers:** P5.a-vintage, E-cess-zero, E-cess-status, E-unit, E-rate-unit (unit on the observation)

#### C4 — Projector at bind; retire `CITE_BLOCKS`

- **Owner:** Platform Architect
- **Signs:** Charter Editor, Source Librarian, Pipeline Engineer
- **Files:** new projector module under `src/prism/` (name in the C1 pass); `src/prism/template_bind.py`; `src/prism/catalog/slices/{c1,c2,c3}.yaml`
- **Landed (2026-09-21).** `project_*` in `src/prism/citizen_projection.py`; cite ids on slice YAML; bind emits `CitizenCite` / `DisplayValue` (and validates `CitizenMethod`); `CITE_BLOCKS` removed. Cite caveat is only `citation.caveat_one_line` (no desk `CaveatNote.reference_period` override). `assert_citizen_caveat` gates catalog YAML. Librarian cards rewrote C1–C3 `caveat_one_line`.
- **Done when:** bind emits `CitizenCite`, `CitizenMethod`, `DisplayValue` (scale once per page-concept; rates/indices `none`; same scale on stats and axes); `rg CITE_BLOCKS` is empty; cite ids live in slice YAML as identity; adding a fourth slice needs no Python edit; unresolved cite id fails the build.
- **Depends on:** C1, C2, C3
- **Out of scope:** YAML instruction; changing producer urls (Source Librarian’s own card work); HTML chrome (C5)
- **Size:** L
- **Covers:** P2-schema, P3 (panel bind `citation_id`), P6, P6-mappers (display leaves mappers), E-c2-units, E-compact (computation)

#### C5 — Citizen chrome

- **Owner:** UI/UX Developer
- **Signs:** Front-end Architect, Platform Architect
- **Files:** `src/prism/template_bind.py` (`_caveat_block_html`, `_slot_html`, `format_bound_number`), `src/cms/src/styles/desk.css`, `src/cms/src/lib/theme.ts`
- **Landed (2026-09-21).** Method HTML is `CitizenMethod`; holes use `miss_copy`; Vega `titleSize`/`subtitleSize` gone; method H2 1.0625rem on `--paper`; in-text `popovertarget` is `cite-{citation_id}`.
- **Done when:** method block renders `CitizenMethod` only — no caveat schema field, no “Do not”, no “How to read this series” codebook; `_slot_html` hardcode gone, “not published” from `miss_copy` alone; compact strings fit (axis ≥ 12px, ≤ 9 characters, no rotation at 974); `chart.titleSize` / `subtitleSize` removed; answer H2 ≥ 1.4× method H2; method not on `--well`; every `in-text-cite` target resolves to an on-page card with the same id.
- **Depends on:** C4, D2
- **Out of scope:** writing copy; inventing slugs; new tokens for taste; redoing Phase E
- **Size:** L
- **Covers:** P2-chrome, P3, P4, P5.b (chrome), S1, S2, S2-type, E-compact (render), E-money-method (primitive)

#### C6 — Content Editor four passes

- **Owner:** Content Editor (editorial rule)
- **Signs:** Charter Editor, Methodologist
- **Files:** `src/cms/templates/*/template.md` for C1–C3
- **Landed (2026-09-22), re-run.** C1: `#food` opens on Food and beverages vs CFPI / rural–urban (no Combined-food chip recap); cut All-India-not-a-bar; gap phrase **not published**. C2: cut All-India aside; rate “how not to misread” → Methodology; fertility gaps without desk imperative; projection source-line drops “thousands”. C3: spend leads with BE vs Actuals / central vs transfers; cess and FRBM wording **not published**. Proof form-factor list for C7: inline lede type still shouty; rate chips may lack unit in cell; bar left-gap / axis keys unchanged (bind/UI — not this pass).
- **Done when:** Development → Line → Copy → Proof on each slice. Evidence further answers the H1 (not a recap of `.stat-figure`, not a ministry verdict). One method block after the record. No parser name, Frame label, “Table 8”, or `vintage_id` in lede, evidence, source-lines, or chart titles. Chart titles name the thing in citizen words. Four passes, one phase — not a restyle.
- **Depends on:** C5, D3
- **Out of scope:** CSS, tokens, routes, a fifth pass
- **Size:** L
- **Covers:** P1, P5, P5.b, E-money-method, E-frbm-words, E-table-8, E-rates-notes, E-all-india-bar (cut)

#### C7 — Presentation pass on preview

- **Owner:** UI/UX Developer
- **Signs:** Front-end Architect
- **Files:** template CSS and `theme.ts` only
- **Landed (2026-09-21).** Preview `http://127.0.0.1:4333` desk `desk-20260921-2f93be5c9ccc`. No `desk.css` / `theme.ts` edit. Measured C1–C3 at 1440 and 360 against v3.1: one well (gap 0, `--radius-lg` 20px, 4px `--mark`), first chart `--card` 1024 / SVG 974, method 17px vs answer 24px (1.41×) at `--measure` ≤65ch, numeric ticks ≤9 chars / 12px, contrast ≥4.5:1, stat figures fit at 360. Do not treat port 4321 as this desk. Front-end Architect sign: routes unchanged (`/prices/retail-prices`, `/people/population`, `/money/union`). Compact-unit axis ticks pass; long category names may ellipsize (not a tick-string fail).
- **Landed (2026-09-22), re-run after C6.** Preview `http://127.0.0.1:4333` desk `desk-20260922-6dd1f6bafd5e`. No `desk.css` / `theme.ts` edit — C6 was copy/chart-subtitle only; house tokens already match v3.1 (inline `.fact-lede` figures inherit body size; method quieter). Routes unchanged. Proof leftovers that are not CSS (rate unit in cell, axis period keys, bar left-gap) stay Platform/Pipeline/later F-rows — not this pass.
- **Done when:** preview passes design-system v3.1 end to end with C6 copy — one well per page, two voices, first chart edge-aligned on `--card`, cropped chart still shows title, unit, geography, source, holes; method quieter; AA at 360 and 1440.
- **Depends on:** C6
- **Out of scope:** copy edits, schema, bind logic
- **Size:** M
- **Covers:** P4, S1, S2, E-all-india-bar (form factor)

#### C8 — Trust audit of the preview desk

- **Owner:** Trust Auditor — launch `.cursor/agents/trust-auditor.md`; do not play this in the parent
- **Signs:** none (independent)
- **Files:** none; writes a verdict note into this plan
- **Landed (2026-09-21), first audit.** Independent agent [Trust audit](83437b7d-b1aa-4312-b07e-c5a616818c08). **block** (cess zero; desk `caveat_one_line`). Not played in the parent.
- **Landed (2026-09-21), re-audit after C3 vintage + librarian + C7.** Independent agent [Trust audit](d5097240-d303-4c1f-b8ba-2d1684e42310). **block.** Not played in the parent.
- **Landed (2026-09-21), re-audit after C2 method leak.** Independent agent [Trust audit](6345d775-a7d8-488a-8a87-7d8e7cbfa476). **block.** Not played in the parent.

- **Landed (2026-09-21), re-audit after C1 cite-period split.** Independent agent [Trust audit](23f4cc09-5642-4597-851c-41e66fb8d70a). **pass.** Not played in the parent.

- **Landed (2026-09-22), re-audit after C6–C7 re-run.** Independent agent [Trust audit](8fe25feb-4f3e-472d-abd5-860d110726de). **pass.** Not played in the parent.

```text
verdict:  pass
slice:    desk-20260922-6dd1f6bafd5e Track C C8 (C1/C2/C3 preview)
fails:    none
notes:    Pointer and desk vintages match. C1 dual cite panels
          --2026-08/--2026-07 with August strip/lede; Cess unknown/null;
          FRBM not published; no desk leak; no default rank, red–green,
          or spin. citizen_pointer untouched.
next:     charter-editor
```
- **Done when:** every cite opens the producer page for that series; dates match the vintage; no hole plotted as zero (including GST Compensation Cess); no desk field, parser name, Frame label, or `do_not` on the page; no default rank, no red–green; no spin. Taste is out.
- **Depends on:** C7
- **Out of scope:** style, layout, wording preference
- **Size:** M
- **Covers:** P2-chrome verification, E-cess-zero, E-table-8, E-frbm, P5-leak on the page

#### C9 — Ship or block

- **Owner:** Charter Editor
- **Signs:** Platform Architect
- **Files:** this plan (verdict block)
- **Prior verdict (2026-09-21).** First Trust block (cess zero; desk cites). Then C2 method leak. Then T-cite-period. Pointer did not move.
- **Verdict (2026-09-21).** [Trust audit](23f4cc09-5642-4597-851c-41e66fb8d70a) after the C1 cite-period split. No override of Trust. Track C is **accepted on the preview bind**. **`citizen_pointer` does not move.**
- **Verdict (2026-09-22), C6–C9 re-run.** [Trust audit](8fe25feb-4f3e-472d-abd5-860d110726de) after Content Editor C6 (P1 explainer) + C7 presentation (no CSS). No override of Trust. Track C **preview bind accepted** on `desk-20260922-6dd1f6bafd5e`. **`citizen_pointer` does not move.**

```text
slice:          Track C citizen surface (C1–C3 templates + bind projection)
in:             C6 explainer evidence; C8 pass on desk-20260922-6dd1f6bafd5e;
                C1 dual cites; C3 cess hole; not-published FRBM
out:            citizen_pointer flip; catalog B3; geography folders this wave
source_class:   unchanged
next_persona:   platform-architect
```

- **Done when:** a recorded verdict exists. **`citizen_pointer` does not move.** Publishing a multi-slice desk is catalog B3 with its own named scope after this programme.
- **Depends on:** C8
- **Out of scope:** flipping the pointer; opening geography folders
- **Size:** S

---

### Track A — ingest and vintage machine (parallel with C)

#### A-r1 — Rename parser families

- **Owner:** Ingest Engineer
- **Signs:** Platform Architect
- **Files:** `src/prism/ingest/xlsx_cpi_period.py`, `census_srs_xlsx_pdf.py`, `budget_cga_xlsx_pdf_html.py`, `xls_ole_grid.py`, `html_table_expand.py`, `pdf_word_columns.py`; shared `parsed_table.py`; `ingest/run.py` stays the single runner
- **Landed (2026-09-21).** Modules renamed off C-numbers to format + table-shape names. `parser_id` registry and lineage `PARSER` strings unchanged. Runner still selects via catalog `parser_id` → `PARSERS`. No parse behaviour change.
- **Signed (2026-09-21), Platform Architect.** Shape names + one runner; registries still keyed by `parser_id`; no guess-all parser; refresh contract untouched.
- **Done when:** no parser module name contains a C-number; each name states format + table shape; runner selects by declared shape; no behaviour change in the rename commit.
- **Depends on:** D4
- **Out of scope:** guess-all PDF parser; changing parse behaviour
- **Size:** M
- **Covers:** P6 (structure), P7, P5.a-ingest (structure)

#### A-r2 — Rename mapper families

- **Owner:** Pipeline Engineer
- **Signs:** Platform Architect
- **Files:** `src/prism/pipeline/state_sector_period.py`, `census_srs_ncp.py`, `wide_measure_columns.py`; `materialise_vintage` stays the single entry in `pipeline/run.py`
- **Landed (2026-09-21).** Modules renamed off C-numbers to shape names matching catalog `mapper_id` families. `MAPPER_VERSION` strings and map behaviour unchanged.
- **Signed (2026-09-21), Platform Architect.** Shape modules + `materialise_vintage` single entry; `mapper_id` registry unchanged; no mapping behaviour in the rename.
- **Done when:** no mapper module name contains a C-number; `materialise_vintage` stays the single entry; no mapping behaviour in the rename commit.
- **Depends on:** A-r1, C3 (status/unit work lands before the same files churn)
- **Out of scope:** changing mapping behaviour
- **Size:** M
- **Covers:** P6-mappers, P7

#### A-r3 — Ingest accuracy gate (catalog A5)

- **Owner:** Ingest Engineer
- **Signs:** Charter Editor, Methodologist
- **Files:** `tests/fixtures/ingest/{xlsx_cpi_period,xlsx_census_pca,xls_census_a02,pdf_srs_bulletin,xlsx_budget_receipt,html_cga_monthly}/`, `tests/test_ingest_accuracy_gate.py`
- **Landed (2026-09-21).** Six producer shapes with licence-safe raw + hand-verified `expected.csv`. Gate runs in the normal pytest suite. Corrupt raw fails (`lineage_ok: no` or parser raises). CPI withheld inflation and Budget blank/`...` cells stay empty in derived CSV — never `"0"`. No `ingest-auditor` persona.
- **Signed (2026-09-21), Charter Editor + Methodologist.** Ruling 8 stands (no twelfth persona). Offline gate covers the six shapes; holes stay empty, not fabricated zeros. Methodologist: first-layout bar for these shapes is met — withheld/`...`/blank cells must not become numeric zeros at ingest. Charter: Track A accepted; source class unchanged; do not flip `citizen_pointer`; B3 stays out.
- **Done when:** each producer file shape has a small licence-safe sample and a hand-verified derived table; gate runs offline in the normal test run; a corrupted fixture fails it; a hole in the raw file arrives as non-published status, never a zero. No `ingest-auditor` persona (ruling 8).
- **Depends on:** A-r1
- **Out of scope:** network in tests; a new persona; render-time assertions (those are C3/C8)
- **Size:** M
- **Covers:** P7, P7-signoff, P5.a-ingest

Source Librarian (launch the agent, not the parent): confirm live card `url`s are producer pages a citizen can open — pack as a job before C8. Geography Steward: no build this wave; sign D1.

#### Track A — closed

```text
slice:          Track A ingest/vintage machine (A-r1..A-r3)
in:             shape-named parsers/mappers; offline ingest accuracy gate;
                catalog A5 guards already in tests
out:            citizen_pointer flip; B3; guess-all parser; ingest-auditor
source_class:   unchanged
next_persona:   platform-architect
```

Open citizen gaps after Track C + Track A: [cms-system-feedback.md](cms-system-feedback.md) F- rows — **closed 2026-09-21** (compact unit, C2 lede, axis ticks, cite chrome, method fine-print, bar left-gap). Not B3. `citizen_pointer` untouched.

---

### Feedback coverage

Every id in [citizen-page-feedback.md](citizen-page-feedback.md) maps to at least one phase.

| Id | Feedback (verbatim topic) | Phase |
|----|---------------------------|-------|
| P1 | Evidence restates `.stat-figure`; write explainer | C6 |
| P1-compare | Prior period comparable? | C2 |
| P2-chrome | Citation card is a field dump; no vintage labels | C5, C8 |
| P2-schema | Name a citizen citation surface vs machine fields | C1, C4 |
| P2-caveat | One comprehensible citizen caveat vs `do_not` | C2, C1 |
| P2-url | Card `url` is a producer page | Source Librarian before C8 |
| P3 | In-text cite → closable panel; card stays | C4 (bind), C5, C8 |
| P4 | Chart wells, ticks, compact units, fill | C5, C7 |
| P5 | One method block; drop desk sentences | C2, C5, C6 |
| P5-leak | Desk `do_not` / parser talk on the page | C2, C5, C8 |
| P5.a-contract | Ingest producer-shaped; vintage citizen fields; split caveat | C1 |
| P5.a-ingest | Parser state in lineage/flags, not citizen fields | A-r1, A-r3 |
| P5.a-vintage | Map to house fields; do not copy parser jargon | C3, C4 |
| P5.b | Hide desk jargon; four editorial passes | C6, C5 |
| P6 | Compact K / L / Cr at bind | C1, C4, C5 |
| P6-mappers | Mappers by table shape, not C-number | C4, A-r2 |
| P7 | Ingest accuracy gate; parsers by shape; no new persona | A-r1, A-r3 |
| P7-signoff | First parse of a new table shape | A-r3; C9 citizen half |
| S1 | Lede/prose vs chart/stat alignment | D2, C5, C7 |
| S2 | Method after the record; not as prominent | C6 (placement), C5/C7 (type) |
| S2-type | Methodology type quieter | D2, C5 |
| S3 | Geography pages later, full slices | D1 reservation; no build |
| S3-catalog | Geography catalog of bound units; atomic completeness | C1 fields; D1 |
| S3-frame | Units and kebab names from geography frames | Geography Steward signs D1 |
| E-money-method | Several “How to read” on `/money/union` | C5 primitive, C6 copy |
| E-frbm-words / E-frbm | FRBM “unknown / not a table” → **not published** | C2, C6, C8 |
| E-table-8 | “Table 8 prints…” | C1, C6, C8 |
| E-rates-notes | Rates ≠ headcount; TFR aside → Methodology | C2, C6 |
| E-all-india-bar | “All India is not a bar” — Line skip | C6, C7 |
| E-rate-unit | Rate `.stat-figure` needs slot unit | C3, C5 |
| E-c2-units | Same concept, same display unit | C2, C4 |
| E-cess-zero / E-cess-status | GST Compensation Cess gap drawn as zero | C3, C8 |
| E-compact | Compact display in lede, stat, axes | C4, C5 |
| E-unit | Every bound stat carries `unit` | C3, C5 |

---

## 6. Non-goals

- A second catalog or ingest plan.
- An `ingest-auditor` persona, or any twelfth persona.
- A guess-all PDF/HTML parser. YAML as parser instruction.
- Doorway geography pages, or generating `/{sleeve}/{slice}/{geo}` this wave.
- ISR, Next.js, request-time producer fetch, search, chat, newsletter, `/answers/`, `/cite`, `/how-it-is-measured`.
- USAFacts costume (magenta, cream, Aeonik, wordmark). Role stays; kit stays out.
- Flipping `citizen_pointer`. Catalog B3 is a later named programme.
- Rewriting v3 tokens for taste, or redoing archived UI/UX Phase E.
- A fifth Content Editor writing pass.
- Deleting or renumbering the nine locked tests.
- Printing `geography_vintage` or `vintage_id` as citizen labels (keep the tests).
- Blending personas inside a phase.
- Editing `docs/design-philosophy.md`.

---

## How a later parent runs this

1. Pick **one** phase. Read only that owner’s persona file.
2. Do not start C while D1–D3 are open if the phase quotes those contracts.
3. Track A may run beside Track C after D4.
4. Launch Trust Auditor and Source Librarian as Cursor agents. Pack one job.
5. Stop at C9 with a verdict. Do not publish.

```text
next_persona:   stop
phase:          F-rows closed; do not open B3; citizen_pointer stays put
plan:           docs/archive/cms-system-feedback.md
```
