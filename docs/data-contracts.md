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
do_not:             (joins, ranks, or charts that would lie — desk only)
citizen_note:       (what the number is, for the citizen method block)
```

`do_not` never projects. `citizen_note` is Methodologist copy; bind reads it into `CitizenMethod`. Prior vintages may omit `citizen_note`; a new catalog card must set it.

## Observation

```text
observation_id:
series_id:
citation_id:        (required)
caveat_id:          (required)
geography:          { code, geography_vintage, code_system }
reference_period:
value:              (number, or null) — as the producer printed it
unit:               (string the cite card shows — as the producer printed it)
denomination:       magnitude the producer printed, paired with the measure:
                    magnitude: ones | thousand | lakh | crore
                    measure:   rupees | persons | percent | rate | index | count | …
status:             value | unknown | withheld | delayed | withdrawn
                    | not_comparable | series_break
lineage:            { raw_path, derived_path, checksum }
```

If `citation_id`, `caveat_id`, `geography.geography_vintage`, or `denomination` is missing, the write fails. Do not drop the field so a chart can render.

`value` and `unit` stay exactly as the producer printed them. Ingest does not normalise to ones. A ₹ crore column stays `crore` of `rupees`. A thousands-of-persons column stays `thousand` of `persons`. Percent, rates, and indices carry magnitude `ones` and are never converted.

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

Binding (`template_id`, `vintage_id`) is a desk field, not a template field. If the vintage has no matching observation, the slot renders **not published** — not as a remembered figure.

## Citizen projection (bind-time)

Built at bind from a vintage. Not stored as a second vintage. Projector: `src/prism/citizen_projection.py`. Bind calls `project_*`. The renderer must not receive a desk field.

At bind, once: a single function converts `value × denomination` to a **canonical** amount in base units (rupees, persons) for money and headcount. Percent, rates, and indices have denomination magnitude `ones` and are never converted and never compacted. At render, one formatter produces the citizen string from the canonical amount on the Indian ladder: thousand / `K`, lakh / `L`, crore / `Cr`, lakh crore / `L Cr`. The token is the entire unit; the producer's `unit` word never sits beside it.

Scale is chosen per **scale group** declared by the template — a chart axis and the chips that quote that chart. Never inferred from a page-wide concept bucket. Liabilities cannot set the scale for revenue receipts.

```text
CitizenCite          projection of Citation
  producer           office, linked via url
  url
  series             as the producer names it (no group / table / COICOP codes)
  reference_period   observation period on this card; one catalog citation
                     used for two months is two CitizenCite records
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

CitizenNumber        bind-time citizen figure (replaces DisplayValue)
  canonical_value    base units (rupees, persons) or the published rate/index
  measure            rupees | persons | percent | rate | index | count
  text               the only citizen number string — or "not published"
  chart_value        the value plotted, in the chart's declared scale group
  axis_label         the compact token for that group (K | L | Cr | L Cr | …)
  status             Observation.status
  absent:            display_scale, concept_key, producer unit word

  Record fields stay on the observation and the cite card: raw `value`,
  `unit`, and `denomination`. CitizenNumber.text is the page.

CitizenChange        bind-time movement between two observations
  current            CitizenNumber (this period)
  prior              CitizenNumber (prior published period, same series)
  prior_period       citizen period label
  direction          higher | lower | unchanged
  difference         formatted difference, or "not comparable"
  citation_id        the prior observation's own cite

  Both sides are observations of the same series in the same vintage.
  The only arithmetic is subtraction (and, where Methodologist signs it,
  a published ratio). If a series_break or not_comparable status lies
  between them, difference is the citizen phrase for a break and the
  template shows both figures without joining them. If the prior
  observation is absent, the slot renders "not published" — never a
  remembered number. Prism may name this as analysis beside the
  producer cite; the producer stays the producer.

CitizenGeography     reserved for /{sleeve}/{slice}/{geo}
  geography_label    "India", "Kerala"
  geography_slug     kebab English name
  absent:            geography_vintage (desk / vintage GeographyRef only)
```

Observation `status` is the only source of a hole. A published zero (`status: value`, `value: 0`) and a gap (`unknown` / `withheld`) are verbally and visually distinct; the citizen phrase for a gap is **not published**.

`DisplayScale`, `scale_for_concept`, `concept_key`, and `apply_scale` are removed. Peak-driven, concept-lumped scaling is not part of this contract.

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
