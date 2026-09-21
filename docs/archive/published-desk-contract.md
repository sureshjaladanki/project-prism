# Published desk contract

Persona: Platform Architect. Product: [architectural-blueprint.md](../architectural-blueprint.md). Schema: [data-contracts.md](../data-contracts.md). Layout: [repo-conventions.md](../repo-conventions.md). Execution plan: [catalog-ingest-pipeline-plan.md](../next/catalog-ingest-pipeline-plan.md).

The published unit is a **desk**. Pointers name a `desk_id`. Each page still binds exactly one `vintage_id`. Vintages stay immutable, per-slice, and independently refreshable.

```text
desk_id_rule: "desk-" + publish_date_utc (YYYYMMDD) + "-" + 12-hex of
 desk.json (hashed without desk_id). Directory with that id is never overwritten.
publish_unit: a desk: one (template_id, vintage_id) per published slice.
atomic_publish: yes (citizen-view moves only when render of the new desk is
 complete for every slice the desk lists)
on_fail: keep previous published desk; do not serve a partial
retain_prior: yes (prior desks and prior vintages stay addressable)
```

## Stores

| Store | Path |
|---|---|
| Desk | `data/desks/{desk_id}/desk.json` |
| Render | `data/renders/{desk_id}/` + `COMPLETE` |
| Pointers | `data/pointers/{citizen,preview}` — one `desk_id` each |

Template files do not carry `bound_vintage_id`. Binding is a desk field.

## Locked-document amendments (this landing)

These lines in the architecture files now match this contract. Nothing else in those files moved.

- `architectural-blueprint.md` — Stores table (Render, Pointer), Citizen request view, Refresh contract, test 4.
- `data-contracts.md` — Pointers block; Template block (binding is not a template field).
- `repo-conventions.md` — `data/renders/{desk_id}/`, pointer store lines, `data/desks/` row.
