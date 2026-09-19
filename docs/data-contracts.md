# Data contracts

The portrait schema. Every number a citizen can see is an observation inside a data vintage. A float with no citation card is not stored and not served.

This is not the running machine ([architectural-blueprint.md](architectural-blueprint.md)) and not how files are fetched or vintages written ([data-pipeline.md](data-pipeline.md)). Languages and on-disk layout: [repo-conventions.md](repo-conventions.md).

Platform Architect owns these types. A write that cannot satisfy them fails; it does not drop a field so a chart can render.

## Identity rules

- A **geography code without a geography vintage is a bug.** Store them as a pair.
- A **data vintage is immutable** once written. Refresh writes a new id.
- **Unchanged series are not recopied.** A new vintage directory lists every series; files whose payload checksum matches the previous vintage are hard-linked (or the same content-addressed key). Duplicating those bytes is a bug. `manifest.json` is always new.
- **Release date is not the reference period.** Both are stored; charts use the reference period.
- **Status is first-class.** Unknown, withheld, delayed, withdrawn, not comparable, and series break are stored as status, not missing columns that a chart skips.

## Series

The producer’s series, not a nickname.

```text
series_id:          (stable in this platform)
producer:           (office that publishes it)
name:               (name the producer uses)
frequency:
licence:            (from the citation card)
```

## Citation

Source Librarian’s card. Every observation points at one.

```text
citation_id:
producer:
series:
id:                 (round, statement, table, or dataset id)
reference_period:
release_date:
url:
geography_as_published:
frequency:
licence:
next_release:       (date or unknown)
caveat_one_line:
```

## Geography vintage

The map as of the series, not today’s map pasted onto an old table. Geography Steward owns the contents.

```text
geography_vintage:  (year / date the boundaries refer to)
code_system:        LGD | census | producer-specific | none
frame:              Union | state | UT | district | other
units_included:     (code + English name, each with geography_vintage)
units_missing:      (named, not implied)
breaks:             (splits, merges, renames that hit this frame)
crosswalk:          (path, or none — do not recode)
```

## Caveat note

Methodologist’s note. Every series in a vintage carries one.

```text
caveat_id:
concept:
unit:
population:
reference_period:
producer_definition:
comparable_from:
breaks:
lags:
disagrees_with:     (other official series, or none)
do_not:             (joins, ranks, or charts that would lie)
```

## Observation

```text
observation_id:
series_id:
citation_id:        (required)
caveat_id:          (required)
geography:          { code, geography_vintage, code_system }
reference_period:
value:              (number, or null)
unit:
status:             value | unknown | withheld | delayed | withdrawn
                    | not_comparable | series_break
lineage:            { raw_path, derived_path, checksum }
```

If `citation_id`, `caveat_id`, or `geography.geography_vintage` is missing, the write fails. Do not drop the field so a chart can render.

Two official series that disagree are two observations, each with its own citation and caveat. The model does not pick a winner.

## Data vintage

```text
vintage_id:         (see refresh contract in the architectural blueprint; never reused)
created_at:
trigger:            schedule | source_change | on_demand
input_manifest:     written as manifest.json (human-readable) and hashed
                    into vintage_id. Per series: producer, series_id,
                    source_vintage, raw checksum, parser version,
                    lineage_ok, geography vintage, payload checksum,
                    reused: yes | no; plus caveat ids and mapper version.
                    The 12-hex is identity, not the audit trail.
observations:       one Parquet file per series_id; unchanged files are
                    hard-linked / CAS-reused, never byte-copied
citations:
geography_vintages:
caveat_notes:       per series, same reuse rule as observations
completeness:       complete | failed
```

A complete vintage lists every required series. A **named hole** (locked on the slice refresh contract) stays on that list: `lineage_ok: no`, observations `status: unknown` with a citation and caveat, not a reconstructed table, not omitted. Other required series must be `lineage_ok: yes`. Omitting the hole, or `lineage_ok: no` on a series that is not a named hole, cannot be `completeness: complete`.

A failed vintage is retained for diagnosis. It is never the citizen pointer. Do not recopy the ingest audit trail into `lineage.json`; ingest lineage stays per retrieve. The pipeline’s “what ran, changed, failed” record is `logs/{run_id}/report.json`. Do not write a full-portrait snapshot that duplicates unchanged series.

## Template

Content Editor authors copy and chart spec. Slots bind to selectors (series + geography + reference period), not to numerals typed into the page.

```text
template_id:
slots:              (each: selector → observation in the bound vintage)
copy:
chart_spec:         (breaks stay breaks; no default rank sort)
```

Binding (`template_id`, `vintage_id`) is a desk field, not a template field. If the vintage has no matching observation, the slot renders as unknown / not published — not as a remembered figure.

## Pointers

```text
citizen_pointer:    desk_id of the last complete published desk
preview_pointer:    desk_id of the current preview desk (never an alias of citizen)
cms_mode:           citizen | preview
retained_vintages:  prior published vintage_ids stay addressable
retained_desks:     prior published desk_ids stay addressable
```

Two CMS modes, two pointers, same relative paths.

- **citizen** — only slices listed on the citizen desk. Home, hubs, and hottest-rail list those slices only. Each page binds one `vintage_id`.
- **preview** — every slice listed on the preview desk (latest complete vintage per slice, including unpublished slices). Each page still binds one `vintage_id`; the desk may hold C1, C2, and C3 pages from different vintages.

A citizen route reads only `citizen_pointer`. How the pointer is flipped atomically is serving, not schema: [architectural-blueprint.md](architectural-blueprint.md).
