# Catalog + registry: ingest and pipeline at charter scale

Persona: Platform Architect. Product and serving: [architectural-blueprint.md](../architectural-blueprint.md). Schema: [data-contracts.md](../data-contracts.md). Batch stages: [data-pipeline.md](../data-pipeline.md). Layout and tooling: [repo-conventions.md](../repo-conventions.md).

This is an execution plan, not an implementation. Nothing here changes a definition, a route, a slug, or a line of citizen copy. Slice identity stays exactly as locked in [c1-refresh-contract.md](../archive/c1-refresh-contract.md), [c2-refresh-contract.md](../archive/c2-refresh-contract.md), and [c3-refresh-contract.md](../archive/c3-refresh-contract.md).

---

## 1. Verdict

**Adopt with changes.**

Adopted: one ingest runner and one vintage runner driven by a typed catalog; per-charter templates stay; parsers and mappers register by table **shape**, not by C-number; C1–C3 migrate onto the catalog before C4 starts; ingest and pipeline stay two stages.

Changed, in five places:

1. **The catalog is identity, never instruction.** `MEASURES` in `pipeline/c3.py`, the classifier table in `pipeline/c1.py`, and every column map stay in Python beside their mapper. A catalog field may be an id, a name, a date, a URL, or a path. If reading the field requires an `if`, it is code. This is the line that stops YAML becoming a second programming language.
2. **Ingest is grouped by artifact, not by series.** `ingest_c1` fetches one MoSPI workbook for three series, hard-links the raw bytes, and carries an Annex companion. A per-series runner cannot express that. The catalog needs `artifact_id` (URL + companions) with many series pointing at one artifact.
3. **Named holes become a per-series catalog flag.** `NAMED_HOLE_SERIES_IDS` in `refresh.py` is a global frozenset seeded from C3 alone, and `lineage_blocks_completeness` applies it to every slice. At twenty charters that is a completeness hazard, not a tidy-up.
4. **The multi-slice `citizen_pointer` is a different contract and gets its own track.** Unifying runners does not let C2 ship. Merging C1+C2+C3 into one desk vintage is not the fix and is forbidden by the slice contracts already locked.
5. **Cards move out of Python.** `c1_cards.py` + `c2_cards.py` + `c3_cards.py` are 1,705 lines of Pydantic instances that Source Librarian, Methodologist, and Geography Steward should be able to author. They become validated data files, last, and only on proof of byte-identical payloads.

Rejected: nothing in the parent hypothesis. The hypothesis is right about where the duplication is; it is thin on the artifact-sharing and completeness details above.

---

## 2. Contract gaps

### CC-1 — the citizen pointer cannot hold more than one slice (blocking)

`data/pointers/citizen` holds one `vintage_id`. `bind_pages_for_desk` keeps a page in citizen mode only when its `bound_vintage_id` equals that pointer. A C3 vintage lists eleven series and no C1 series ([c3-refresh-contract.md](../archive/c3-refresh-contract.md): "Do not require C1 or C2 series in a C3 vintage"), so publishing C2 or C3 as citizen unpublishes C1. That is exactly the block [c2-charter-verdict.md](../archive/c2-charter-verdict.md) put on Platform.

The code already half-admits it: `render(data_root, vintage_id, cms_root)` binds the **whole desk** but writes the tree to `data/renders/{vintage_id}/`. The tree key is a desk id wearing one slice's vintage id.

**Decision: the published unit is a desk, and the pointer names a desk.**

```text
desk_id_rule: "desk-" + publish_date_utc (YYYYMMDD) + "-" + 12-hex of desk.json.
 Directory with that id is never overwritten.
data/desks/{desk_id}/desk.json immutable: one (template_id, vintage_id) per slice,
 plus completeness: complete | failed
data/pointers/citizen desk_id (still one line, still temp+rename)
data/renders/{desk_id}/ the Astro tree for that desk
```

Each page still binds exactly one `vintage_id` — blueprint test 6 is untouched and gains teeth. Vintages stay immutable, per-slice, and independently refreshable. Prior desks and prior vintages stay addressable.

Rejected alternative: one desk vintage listing every slice's series. It forces a new `vintage_id` for all twenty charters every time CPI refreshes, rewrites every template binding on every run, and contradicts the locked per-slice vintage contracts.

### CC-2 — `bound_vintage_id` is not in the Template contract

`data-contracts.md` defines a template as `template_id`, `slots`, `copy`, `chart_spec`. `src/cms/templates/*/slots.yaml` adds `bound_vintage_id`, so every refresh needs a git commit against a Content Editor file, times twenty charters. The binding belongs to the desk record, which is a store Platform owns. Removing it returns the template to the locked contract.

### CC-3 — named holes are global, completeness is per-slice

See verdict change 3. Fixed by the catalog; no locked-document change.

### CC-4 — `write_vintage(required_series_ids=C1_SERIES_IDS)` defaults to C1

A slice runner that forgets the keyword is checked against C1's required series. C2 and C3 pass it; C1 relies on the default. Make the keyword required.

### CC-5 — series reuse is keyed on exact tuple order

`latest_manifest_with_series` matches a previous manifest by `tuple(...) == series_ids`. Reordering a catalog file would silently find no previous manifest, mark every series `reused: no`, and duplicate bytes — a blueprint test 9 failure caused by an edit that changed nothing. Compare as a set.

### Follow-up note required

CC-1 and CC-2 change locked text. Do **not** edit the three architecture files ahead of the work. When Track B phase B1 lands, Platform writes `docs/archive/published-desk-contract.md` and amends, in one pass, exactly these lines:

- `architectural-blueprint.md` — Stores table (Render, Pointer rows), "Citizen request" view, Refresh contract block, test 4.
- `data-contracts.md` — Pointers block (`citizen_pointer` / `preview_pointer` name a desk id), Template block (state that binding is not a template field).
- `repo-conventions.md` — `data/renders/{vintage_id}/` → `{desk_id}/`, pointer store lines, and a `data/desks/` row.

Nothing else in those files moves.

---

## 3. Refresh contract

Vintage identity, triggers, sequence, failure, and retention are **unchanged**. Two lines are added for the published desk (CC-1), marked NEW.

```text
vintage_id_rule: "dv-" + run_date_utc (YYYYMMDD) + "-" + 12-hex of
 manifest.json. Directory with that id is never overwritten.
desk_id_rule: NEW. "desk-" + publish_date_utc (YYYYMMDD) + "-" + 12-hex of
 desk.json. Directory with that id is never overwritten.
publish_unit: NEW. a desk: one (template_id, vintage_id) per published slice.
 Each page still binds exactly one vintage_id.
triggers: schedule | source_change | on_demand
sequence: ingest → pipeline (data vintage) → cms render → publish pointer
atomic_publish: yes (citizen-view moves only when render of the new desk is
 complete for every slice the desk lists)
on_fail: keep previous published desk; do not serve a partial
retain_prior: yes (prior desks and prior vintages stay addressable)
```

Triggers keep their locked meaning: `schedule` follows each series' `next_release` in the catalog, not a global clock; `source_change` is the ingest raw checksum; `on_demand` is the same CLI. Request-time producer fetch and in-place regeneration of live citizen routes are not triggers and are not publish.

---

## 4. Serving and store paths

Pipeline and CMS keep using these. Names and helpers stay in `src/prism/paths.py`; nobody builds these strings by hand.

| Store | Path | Change |
|---|---|---|
| Ingest raw / derived / lineage | `data/{raw,derived,lineage}/{producer_slug}/{series_id}/{source_vintage}/…` | none |
| CAS | `data/cas/{sha256}` | none |
| Vintage | `data/vintages/{vintage_id}/manifest.json` + `series/{series_id}/{observations.parquet,citation.json,caveat.json,geography.json}` | none |
| Desk | `data/desks/{desk_id}/desk.json` | **new, Track B** |
| Render | `data/renders/{desk_id}/` + `COMPLETE` | key changes from `vintage_id`, Track B |
| Pointers | `data/pointers/{citizen,preview}` | content becomes a `desk_id`, Track B |
| Run report | `logs/{run_id}/report.json` | none |
| Catalog | `src/prism/catalog/` (in git, package data) | **new, Track A** |

Unchanged rules: DuckDB reads exactly one `vintage_id` per page at render; nothing serves a bare float; the pointer flip is last, after a complete render and after the nine tests; a failed vintage or desk is retained and never the citizen pointer.

---

## 5. What the catalog owns, what code owns

```text
src/prism/catalog/
 __init__.py Pydantic models + loader + PARSERS / MAPPERS registries
 slices/c1.yaml c2.yaml c3.yaml
 cards/citations/*.yaml (phase A4)
 cards/caveats/*.yaml (phase A4)
 cards/geographies/*.yaml (phase A4)
```

Catalog (identity and wiring):

```yaml
slice_id: c3
charter: C3
template_id: c3-union-money
artifacts:
 - artifact_id: receipt-budget-tr-xlsx
 url: "https://…/tr.xlsx"
 companions: []
series:
 - series_id: budget-2026-27-tax-revenue
 card: 1
 name: "Receipt Budget, 2026-2027 — I. Tax Revenue (major heads as published)"
 producer: "Ministry of Finance, Budget Division, Government of India"
 producer_slug: mof-budget
 source_vintage: "2026-27"
 next_release: unknown
 geography_frame_id: c3-frame-a
 geography_vintage: "2026"
 citation_id: cite-c3-budget-2026-27-tax-revenue
 caveat_id: caveat-c3-budget-2026-27-tax-revenue
 artifact_id: receipt-budget-tr-xlsx
 parser_id: budget-xlsx
 mapper_id: wide-measure-columns/budget-four-year
 named_hole: false
```

Code (anything that must be interpreted): parser functions, mapper functions, column maps, month tables, classifier rules, header offsets, unit-label composition, PDF layout hints. Parameter sets such as `_FOUR_BUDGET` or `_ANNEX1` stay in the mapper module and are referenced from the catalog by name only.

Registries keyed by table shape, not by charter:

- Parsers today: `mospi-cpi-xlsx` (`ingest/xlsx_cpi_period.py`), Census / SRS / NCP (`ingest/census_srs_xlsx_pdf.py`), Budget / CGA (`ingest/budget_cga_xlsx_pdf_html.py`). Layout helpers: `xls_ole_grid.py`, `html_table_expand.py`, `pdf_word_columns.py`.
- Mappers today: `state-sector-period` (`pipeline/c1.py: map_derived_table`), `wide-measure-columns` (`pipeline/c3.py: map_c3_table`), plus whatever `pipeline/c2.py` already implements. Pipeline Engineer names the C2 families by reading that file. Do not invent a fourth family before then.

A new charter that reuses a family is a catalog file. A new layout — PLFS for C4 — is a new parser module plus, if the table shape is genuinely new, a new mapper family. `pipeline/c3.py` is never copied.

CLI shape after the programme:

```text
prism catalog list # slices, series, parser_id, mapper_id
prism catalog validate # CI gate: ids resolve, no orphan artifact/parser/mapper
prism ingest [--slice-id c3] [--series-id …]
prism vintage --slice-id c3
prism render --desk-id desk-… [--set-preview]
prism desk --slice c1=dv-… --slice c2=dv-…
prism publish --desk-id desk-… --citizen
```

---

## 6. Execution plan

Two tracks. They are different contracts and must not share a commit.

- **Track A — runner unification.** Unblocks C4 without copy-paste. Owner: Platform sets A1, Pipeline Engineer and Ingest Engineer execute A2–A5.
- **Track B — published desk.** Unblocks a C2 or C3 citizen ship. Owner: Platform throughout.

Run **B first** if Charter's next decision is shipping C2/C3 to citizens (that is the open block on the record). Run **A first** if the next decision is C4. Do not interleave.

Every phase, without exception: blueprint tests 1–9 (`tests/test_blueprint_contract.py`) pass; `tests/test_pipeline_c1.py`, `test_pipeline_c2.py`, `test_pipeline_c3.py`, `test_ingest_c1.py`, `test_ingest_c2.py`, `test_ingest_c3.py`, `test_ingest_run.py`, `test_refresh_c1.py`, `test_refresh_c2.py`, `test_refresh_c3.py`, `test_cms_modes.py`, `test_pointer_store.py`, `test_citizen_serve.py`, `test_render_c2.py`, `test_render_c3.py` pass; Ruff and mypy clean.

### Track A

#### A1 — catalog spine (Platform)

**Landed (D4, 2026-09-21).** Catalog package under `src/prism/catalog/`; `slices/{c1,c2,c3}.yaml`; `C1_SERIES` / C2 / C3 are views over the catalog in `refresh.py`. `NAMED_HOLE_SERIES_IDS` is derived from catalog `named_hole`.

- [x] Add `src/prism/catalog/__init__.py`: `CatalogSeries`, `CatalogArtifact`, `CatalogSlice`, `load_catalog()`, `PARSERS`, `MAPPERS`. Pydantic v2, fail fast on an unknown `parser_id` / `mapper_id` / `artifact_id`.
- [x] Add `src/prism/catalog/slices/{c1,c2,c3}.yaml` transcribed from `C1_SERIES` / `C2_SERIES` / `C3_SERIES`, field for field, plus `artifact_id`, `parser_id`, `mapper_id`, `named_hole`.
- [x] `refresh.py` keeps `SeriesBinding`, `vintage_id_for`, triggers, timezones; `C1_SERIES` / `C2_SERIES` / `C3_SERIES` become views over the catalog so no caller changes yet.
- [x] `lineage_blocks_completeness` and `lineage_record_blocks_completeness` read `named_hole` per slice. `NAMED_HOLE_SERIES_IDS` is now derived from the catalog (CC-3), not a C3-seeded frozenset.
- [x] `write_vintage`: `required_series_ids` becomes a required keyword (CC-4). `latest_manifest_with_series` compares sets (CC-5).
- [x] `prism catalog list` / `prism catalog validate`; wire validate into CI.
- [x] Ship the YAML as package data in `pyproject.toml`.

**Out of scope.** Touching parsers, mappers, cards, the CLI's `--slice-id` runners, or anything under `src/cms/`.

**Done when.** `refresh.py` holds no per-series literals; `prism vintage --slice-id c1|c2|c3` still writes a vintage whose every series reports `reused: yes` against the pre-migration manifest and adds no bytes to `data/cas/`; `prism catalog validate` fails on a hand-broken id.

#### A2 — one vintage runner (Pipeline Engineer)

**Goal.** Delete three near-identical `materialise_*` loops.

- [x] Reduce `pipeline/c1.py`, `c2.py`, `c3.py` to mapper families + their parameter sets; register them under `mapper_id`. Rename to shape names once the families are named. **Landed as A-r2:** `state_sector_period.py`, `census_srs_ncp.py`, `wide_measure_columns.py`.
- [ ] Add `src/prism/pipeline/run.py`: `materialise_vintage(data_root, logs_root, *, slice_id, created_at=None)` — load lineage, dispatch `mapper_id`, checksum, write, report. One implementation.
- [ ] `cli.py`: `_VINTAGE_RUNNERS` dict goes; `--slice-id` validates against the catalog.
- [ ] Delete `materialise_c1_vintage` / `_c2_` / `_c3_` and their re-exports in `pipeline/__init__.py`; re-point the slice tests at the one runner.
- [ ] Move `PipelineError`, `observation_count`, `trigger_for_records`, `_write_report` out of `pipeline/c1.py` (C3 imports them from C1 today) into `pipeline/run.py`.

**Out of scope.** Ingest, cards, pointers, templates, any new charter.

**Done when.** `rg "materialise_c" src` is empty; re-running each slice reports `reused: yes` for every series; the run report still names, per series, reused or rewritten.

#### A3 — one ingest runner and parser registry (Ingest Engineer)

**Goal.** One retrieve loop over artifact groups.

- [x] Register parsers by `parser_id` in the catalog registry; family modules renamed to shape names (`xlsx_cpi_period`, `census_srs_xlsx_pdf`, `budget_cga_xlsx_pdf_html`, layout helpers). A-r1 in [citizen-system-change-plan.md](../archive/citizen-system-change-plan.md).
- [ ] Extend `ingest/run.py` to: resolve the requested series → their artifacts, fetch each artifact once, store raw per series (hard-link the shared bytes as `ingest_c1` does today), carry companions, then run each series' registered parser over those bytes.
- [ ] Delete `ingest/c1.py`, `ingest/c2.py`, `ingest/c3.py` once their retrieve behaviour is expressed as artifact groups. Nothing about lineage, `source_changed`, or the `lineage_ok: no` rules changes.
- [ ] Ingest still writes no observations and imports nothing from `prism.pipeline`.

**Out of scope.** New URLs, new producers, re-parsing anything, changing a derived table.

**Done when.** `prism ingest` and `prism ingest --series-id …` produce the same `lineage.json` fields and the same derived CSV bytes as before, including the Annex companion flag and the shared-workbook hard-link note.

#### A4 — cards as data (Platform contract, Pipeline Engineer executes)

**Landed (D4, 2026-09-21).** Cards live under `src/prism/catalog/cards/{citations,caveats,geographies}/`. `pipeline/c*_cards.py` are gone.

- [x] Move `C1_CITATIONS` / `C1_CAVEATS` / `C1_GEOGRAPHIES` and the C2 and C3 equivalents to `src/prism/catalog/cards/**.yaml`, one file per card, validated into the locked Pydantic types at load.
- [x] Delete `pipeline/c1_cards.py`, `c2_cards.py`, `c3_cards.py`. Name lookup tables that mappers use (`FRAME_A_NAME_BY_CODE`) derive from the geography card, not a second literal.
- [x] Loader asserts the card ids match the series entry's `citation_id` / `caveat_id` — the check `map_c3_series` does by hand today.

**Out of scope.** Editing any card's content. This phase is a move; a changed value is a Source Librarian or Methodologist decision, not a refactor.

**Done when.** Every series payload checksum is unchanged — a re-run reports `reused: yes` across all twenty series and `data/cas/` gains nothing (blueprint test 9 proves the move); `rg "Citation\(|CaveatNote\(|GeographyVintage\(" src/prism/pipeline` is empty.

#### A5 — guards, then stop (Platform)

**Landed (accuracy gate A-r3, 2026-09-21; import/catalog guards already in `tests/test_catalog.py`).**

- [x] Test: a fixture slice with a fake producer runs ingest → vintage end to end through the generic runners, touching no C1/C2/C3 module. This is the proof that "a new charter is a catalog file".
- [x] Test: `prism.pipeline` imports no `httpx` and nothing from `prism.ingest.retrieve`; `prism.ingest` imports no `Observation`. The two stages stay two stages.
- [x] Test: a catalog entry with an unknown `parser_id`, a duplicate `series_id`, or a missing `citation_id` fails `prism catalog validate`.
- [x] Ingest accuracy gate: `tests/fixtures/ingest/` + `tests/test_ingest_accuracy_gate.py` (citizen plan A-r3).

**Done when.** All three pass. C4 is then a separate programme with its own charter, cards, and method notes — not this one.

### Track B

#### B1 — desk record and desk pointer (Platform)

**Landed (D4, 2026-09-21).** `desk_store.py`, pointers name a `desk_id`, render trees at `data/renders/{desk_id}/`. Locked-doc amendments: [published-desk-contract.md](../archive/published-desk-contract.md).

- [x] `src/prism/desk_store.py`: `DeskRecord` (desk_id, created_at, slices `[(template_id, vintage_id)]`, completeness), `write_desk`, `load_desk`, `latest_desk`. Immutable directory, same temp+rename discipline as `write_vintage`.
- [x] `paths.py`: `desks_dir`, `desk_dir`, `desk_path`; `render_dir` and `render_complete_path` key on `desk_id`.
- [x] `refresh.py`: `DESK_ID_PATTERN`, `desk_id_for(publish_date_utc, record)`.
- [x] `pointer_store.py`: pointers hold a `desk_id`; `_require_publishable` checks the desk exists, is `complete`, has a `COMPLETE` render, and that every listed vintage exists and is complete. Atomic write, publish lock, and the citizen rollback path are unchanged.
- [x] `render.py`: `render(data_root, desk_id, cms_root, *, cms_mode)`; required-pages set for `_mark_complete` comes from the desk's slice list, not a Python constant.
- [x] `prism desk` and `prism publish` commands; `prism render --vintage-id` becomes `--desk-id`.
- [x] Migration: mint a one-slice desk for the live C1 citizen vintage `dv-20260916-234e263c8588`, render it, flip the pointer. The C1 page must be byte-identical.

**Out of scope.** Publishing C2 or C3. Any route, slug, nav, or copy change. Any change to what a vintage is.

**Done when.** Test 4 reads "the pointer does not move if any slice in the desk failed to render"; test 5 and test 6 pass unchanged; `data/pointers/citizen` holds a `desk_id`; the prior render tree and all prior vintages are still addressable.

#### B2 — the desk owns the binding (Platform contract, Pipeline Engineer executes)

**Landed (D4, 2026-09-21).** `bind_pages_for_desk` reads the desk; `bound_vintage_id` is gone from template `slots.yaml`.

- [x] `bind_page` takes the vintage from the desk record; `bind_pages_for_desk(cms_mode)` reads the citizen or preview desk instead of comparing against a pointer string.
- [x] Drop `bound_vintage_id` from `src/cms/templates/*/slots.yaml`. Coordinate with UI/UX Developer and Content Editor: this removes one machine field, nothing else in those files.
- [x] Preview desk is built, not hand-bound: latest complete vintage per slice, including unpublished slices. Preview still may hold slices from different vintages and is never an alias of citizen.
- [x] `bind_c1_page` / `bind_c2_page` / `bind_c3_page` stay test-only wrappers or go; production stays `bind_pages_for_desk` → `bind_page`.

**Cite-identity (C4, 2026-09-21).** `cite_blocks` live on `src/prism/catalog/slices/{c1,c2,c3}.yaml`. Bind projects catalog id → vintage citation → `CitizenCite`. `CITE_BLOCKS` is gone from Python.

**Done when.** A refresh of one slice requires no edit under `src/cms/templates/`; `test_cms_modes.py` still shows preview binding three slices at three vintages.

#### B3 — publish a multi-slice citizen desk (Platform, after Trust)

**Goal.** C1 and C2 (and C3 when Trust passes) on the citizen pointer at once.

- [ ] Build the desk, render it, run the nine tests, flip last.
- [ ] Citizen home, hubs, and hottest rail list exactly the desk's slices.
- [ ] Test: a desk that adds C2 does not drop C1 — the block from [c2-charter-verdict.md](../archive/c2-charter-verdict.md), encoded.

**Out of scope.** Deciding *whether* C2 or C3 ships. That is Charter Editor after Trust Auditor. Platform only makes it possible.

**Done when.** `prices/retail-prices` and `people/population` serve from one citizen desk, each page binding its own single `vintage_id`, and C1 was never unpublished.

---

## 7. Non-goals

- **YAML as a parser.** No column maps, header offsets, regexes, pivot rules, or conditionals in the catalog. A new table shape is a Python module.
- **Collapsing ingest and pipeline.** Ingest never writes observations; pipeline never fetches. A5 encodes this as an import test.
- **One merged desk vintage.** C1+C2+C3 series in one vintage is not how more than one slice shares a pointer, and the slice refresh contracts forbid requiring another slice's series.
- **ISR, Next.js, SSR, request-time producer fetch.** Not triggers, not publish.
- **New top-level folders.** No `apps/`, `packages/`, `web/`. The catalog is package data under `src/prism/`.
- **A job runner.** Twenty series exist but they are not twenty independent schedules — C1 has one cadence and every C2/C3 `next_release` is `unknown`. Airflow, Dagster, and Spark stay out until the locked trigger for them is actually met.
- **Starting C4–C20.** No PLFS retrieve, no new citation cards, no new templates in this programme.
- **Rewriting C1–C3 and starting a new charter in the same pass.**
- **Per-charter page types.** No `C1Page` / `C3Page`. One `BoundPage`, one `Observation`.

## 8. Done when

Pipeline can add a charter that reuses a known table shape by writing one catalog file and no Python; a genuinely new layout costs one parser and at most one mapper family; a citizen desk can carry more than one slice without unpublishing another; and the nine blueprint tests still fail on a missing cite, a missing geography vintage, a torn publish, or a duplicated byte.
