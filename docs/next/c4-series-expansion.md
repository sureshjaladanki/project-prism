# C4 series expansion (Platform note)

Persona: Platform Architect. Amends [`c4-refresh-contract.md`](c4-refresh-contract.md) for the catalog ingest machine.

**Why.** `ParserSpec` takes one artifact’s bytes. PLFS Appendix A publishes one XLSX per rate table. Keep one tidy series per file so Ingest does not guess across workbooks.

## Stable series ids (complete C4 vintage)

| Card family | `series_id` | Artifact |
|-------------|-------------|----------|
| 1 Monthly CWS | `plfs-monthly-lfpr-wpr-ur-cws` | Monthly Bulletin PDF |
| 2 Quarterly LFPR | `plfs-quarterly-lfpr-cws` | Table_2.xlsx |
| 2 Quarterly WPR | `plfs-quarterly-wpr-cws` | Table_3.xlsx |
| 2 Quarterly UR | `plfs-quarterly-ur-cws` | Table_5.xlsx |
| 3 Annual usual LFPR | `plfs-annual-usual-lfpr-2025` | Table__16.0.xlsx |
| 3 Annual usual WPR | `plfs-annual-usual-wpr-2025` | Table__17.0.xlsx |
| 3 Annual usual UR | `plfs-annual-usual-ur-2025` | Table__18.0.xlsx |
| 3 Annual CWS LFPR | `plfs-annual-cws-lfpr-2025` | Table__30.xlsx |
| 3 Annual CWS WPR | `plfs-annual-cws-wpr-2025` | Table__31.xlsx |
| 3 Annual CWS UR | `plfs-annual-cws-ur-2025` | Table__32.xlsx |
| 4 Regular earnings | `plfs-annual-earnings-regular-2025` | Table__38.xlsx |
| 4 Casual earnings | `plfs-annual-earnings-casual-2025` | Table__39.xlsx |
| 4 Self-employment | `plfs-annual-earnings-self-2025` | Table__40.xlsx |

A complete C4 vintage **lists all thirteen**. Unchanged series reuse via CAS. Citizen charts may still show “quarterly rates” as one visual family — that is Content/UI binding, not one `series_id`.

Frames: monthly → `c4-frame-a`; quarterly → `c4-frame-b`; annual rates + earnings → `c4-frame-c`.
