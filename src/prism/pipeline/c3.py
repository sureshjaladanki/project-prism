"""Map C3 derived tables into a data vintage. Does not fetch and does not publish."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from prism.observation_parquet import observations_to_parquet
from prism.paths import ingest_lineage_path, ingest_table_path, run_report_path
from prism.pipeline.c1 import PipelineError, observation_count, trigger_for_records
from prism.pipeline.c3_cards import C3_CAVEATS, C3_CITATIONS, C3_GEOGRAPHIES
from prism.refresh import (
    C3_SERIES,
    C3_SERIES_IDS,
    NAMED_HOLE_SERIES_IDS,
    SERIES_BUDGET_2026_27_AFS,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
    SERIES_BUDGET_2026_27_LIABILITIES,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
    SERIES_CGA_MONTHLY_GLANCE_2026_07,
    SeriesBinding,
    ensure_utc,
    lineage_blocks_completeness,
)
from prism.schema import (
    CodeSystem,
    Completeness,
    GeographyRef,
    LineageRecord,
    Observation,
    ObservationLineage,
    ObservationStatus,
    VintageManifest,
    YesNo,
)
from prism.vintage_store import SeriesWrite, latest_manifest_with_series, write_vintage

MAPPER_VERSION = "c3-observations-1.1.0"
SECTOR_UNION = "Union"
UNIT_CRORE = "₹ crore"
_SLUG = re.compile(r"[^a-z0-9]+")
_MINUS_PREFIXES = frozenset({"\ufffd", "\u2212", "\u2013", "\u2014"})


@dataclass(frozen=True)
class MeasureColumn:
    column: str
    reference_period: str
    unit: str


_FOUR_BUDGET = (
    MeasureColumn("actuals_2024_2025", "actuals-2024-2025", UNIT_CRORE),
    MeasureColumn("budget_2025_2026", "budget-2025-2026", UNIT_CRORE),
    MeasureColumn("revised_2025_2026", "revised-2025-2026", UNIT_CRORE),
    MeasureColumn("budget_2026_2027", "budget-2026-2027", UNIT_CRORE),
)
_STAT1 = tuple(
    MeasureColumn(f"{year}_{split}", f"{year.replace('_', '-')}-{split}", UNIT_CRORE)
    for year in (
        "actuals_2024_2025",
        "budget_2025_2026",
        "revised_2025_2026",
        "budget_2026_2027",
    )
    for split in ("revenue", "capital", "total")
)
_ANNEX1 = (
    MeasureColumn("actual_2017_18", "actual-2017-18", UNIT_CRORE),
    MeasureColumn("actual_2018_19", "actual-2018-19", UNIT_CRORE),
    MeasureColumn("actual_2019_20", "actual-2019-20", UNIT_CRORE),
    MeasureColumn("actual_2020_21", "actual-2020-21", UNIT_CRORE),
    MeasureColumn("actual_2021_22", "actual-2021-22", UNIT_CRORE),
    MeasureColumn("actual_2022_23", "actual-2022-23", UNIT_CRORE),
    MeasureColumn("actual_2023_24", "actual-2023-24", UNIT_CRORE),
    MeasureColumn("actual_2024_25", "actual-2024-25", UNIT_CRORE),
    MeasureColumn("re_2025_26", "re-2025-26", UNIT_CRORE),
    MeasureColumn("be_2026_27", "be-2026-27", UNIT_CRORE),
)
_LIABILITIES = (
    MeasureColumn("end_1950_51", "end-1950-51", UNIT_CRORE),
    MeasureColumn("end_2021_2022", "end-2021-2022", UNIT_CRORE),
    MeasureColumn("end_2022_2023", "end-2022-2023", UNIT_CRORE),
    MeasureColumn("end_2023_24", "end-2023-24", UNIT_CRORE),
    MeasureColumn("end_2024_25", "end-2024-25", UNIT_CRORE),
    MeasureColumn("revised_2025_26", "revised-2025-26", UNIT_CRORE),
    MeasureColumn("budget_2026_27", "budget-2026-27", UNIT_CRORE),
)
_FA = (
    MeasureColumn("actuals_2024_2025", "actuals-2024-2025", UNIT_CRORE),
    MeasureColumn("actuals_2023_2024", "actuals-2023-2024", UNIT_CRORE),
)
_CGA_MONTHLY = (
    MeasureColumn("be_2026_2027", "budget-2026-2027", UNIT_CRORE),
    MeasureColumn("actuals_upto_july_2026", "actuals-upto-july-2026", UNIT_CRORE),
    MeasureColumn("pct_current", "pct-of-be-current", "% of BE"),
    MeasureColumn("pct_coppy", "pct-of-be-coppy", "% of BE (COPPY)"),
)

MEASURES: dict[str, tuple[MeasureColumn, ...]] = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: _FOUR_BUDGET,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: _FOUR_BUDGET,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: _FOUR_BUDGET,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: _ANNEX1,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: _STAT1,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: _FOUR_BUDGET,
    SERIES_BUDGET_2026_27_LIABILITIES: _LIABILITIES,
    SERIES_BUDGET_2026_27_AFS: _FOUR_BUDGET,
    SERIES_CGA_MONTHLY_GLANCE_2026_07: _CGA_MONTHLY,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: _FA,
}


def _cell(row: dict[str, str], name: str) -> str:
    value = row.get(name)
    if value is None:
        return ""
    return value.strip()


def _number(text: str, *, label: str) -> float | None:
    stripped = text.strip().replace(",", "").replace("*", "")
    if stripped == "":
        return None
    if stripped.endswith("%"):
        stripped = stripped[:-1].strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        stripped = stripped[1:-1].replace("%", "").strip()
    if stripped[:1] in _MINUS_PREFIXES:
        # Finance Accounts PDF minus often lands as U+FFFD / unicode dash.
        stripped = "-" + stripped[1:]
    if stripped == "":
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise PipelineError(f"unparseable {label}: {text!r}") from exc


def _slug(text: str, fallback: str) -> str:
    ascii_only = text.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG.sub("-", ascii_only.lower()).strip("-")
    if slug == "":
        return fallback
    return slug[:80]


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_c3_lineage(data_root: Path, binding: SeriesBinding) -> LineageRecord:
    path = ingest_lineage_path(
        data_root, binding.producer_slug, binding.series_id, binding.source_vintage
    )
    if not path.exists():
        raise PipelineError(f"missing lineage for {binding.series_id}")
    return LineageRecord.model_validate_json(path.read_bytes())


def map_c3_table(
    *,
    series_id: str,
    rows: list[dict[str, str]],
    citation_id: str,
    caveat_id: str,
    geography_code: str,
    geography_vintage: str,
    code_system: CodeSystem,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    measures = MEASURES[series_id]
    if not rows:
        raise PipelineError(f"{series_id} produced no observations")
    missing = [measure.column for measure in measures if measure.column not in rows[0]]
    if missing:
        raise PipelineError(f"{series_id} missing columns: {', '.join(missing)}")
    observations: list[Observation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = _cell(row, "line_label")
        if label == "":
            continue
        slug = _slug(label, f"row-{index}")
        geo = GeographyRef(
            code=geography_code,
            geography_vintage=geography_vintage,
            code_system=code_system,
        )
        for measure in measures:
            value = _number(_cell(row, measure.column), label=measure.column)
            obs_id = f"obs-{series_id}-{geo.code}-{measure.reference_period}-{slug}"
            if obs_id in seen:
                obs_id = f"{obs_id}-{index}"
            seen.add(obs_id)
            observations.append(
                Observation(
                    observation_id=obs_id,
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geography=geo,
                    sector=SECTOR_UNION,
                    reference_period=measure.reference_period,
                    value=value,
                    unit=f"{measure.unit}; {label}",
                    status=ObservationStatus.unknown
                    if value is None
                    else ObservationStatus.value,
                    lineage=lineage,
                )
            )
    if not observations:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(observations)


def _hole_observation(
    binding: SeriesBinding, lineage: LineageRecord
) -> tuple[Observation, ...]:
    geography = C3_GEOGRAPHIES[binding.series_id]
    citation = C3_CITATIONS[binding.series_id]
    caveat = C3_CAVEATS[binding.series_id]
    unit = geography.units_included[0]
    return (
        Observation(
            observation_id=(
                f"obs-{binding.series_id}-{unit.code}-union-"
                f"{binding.source_vintage}-unknown"
            ),
            series_id=binding.series_id,
            citation_id=citation.citation_id,
            caveat_id=caveat.caveat_id,
            geography=GeographyRef(
                code=unit.code,
                geography_vintage=geography.geography_vintage,
                code_system=geography.code_system,
            ),
            sector=SECTOR_UNION,
            reference_period=binding.source_vintage,
            value=None,
            unit="not a table",
            status=ObservationStatus.unknown,
            lineage=ObservationLineage(
                raw_path=lineage.raw_path,
                derived_path=lineage.derived_path,
                checksum=lineage.checksum,
            ),
        ),
    )


def map_c3_series(
    data_root: Path, binding: SeriesBinding, lineage: LineageRecord
) -> SeriesWrite:
    citation = C3_CITATIONS[binding.series_id]
    caveat = C3_CAVEATS[binding.series_id]
    geography = C3_GEOGRAPHIES[binding.series_id]
    if citation.citation_id != binding.citation_id:
        raise PipelineError("citation_id does not match the locked card")
    if caveat.caveat_id != binding.caveat_id:
        raise PipelineError("caveat_id does not match the locked note")
    if lineage.citation_id != binding.citation_id:
        raise PipelineError(
            f"{binding.series_id} lineage citation_id {lineage.citation_id} "
            f"does not match {binding.citation_id}"
        )
    obs_lineage = ObservationLineage(
        raw_path=lineage.raw_path,
        derived_path=lineage.derived_path,
        checksum=lineage.checksum,
    )
    if binding.series_id in NAMED_HOLE_SERIES_IDS and lineage.lineage_ok is YesNo.no:
        observations = _hole_observation(binding, lineage)
    elif lineage_blocks_completeness(binding.series_id, lineage.lineage_ok):
        raise PipelineError(
            f"{binding.series_id} lineage_ok={lineage.lineage_ok.value}; not building a vintage"
        )
    else:
        table_path = ingest_table_path(
            data_root, binding.producer_slug, binding.series_id, binding.source_vintage
        )
        if not table_path.exists():
            raise PipelineError(f"missing derived table for {binding.series_id}")
        unit = geography.units_included[0]
        observations = map_c3_table(
            series_id=binding.series_id,
            rows=_read_rows(table_path),
            citation_id=citation.citation_id,
            caveat_id=caveat.caveat_id,
            geography_code=unit.code,
            geography_vintage=geography.geography_vintage,
            code_system=geography.code_system,
            lineage=obs_lineage,
        )
    return SeriesWrite(
        producer=binding.producer,
        series_id=binding.series_id,
        source_vintage=binding.source_vintage,
        raw_checksum=lineage.checksum,
        parser_version=lineage.parser,
        lineage_ok=lineage.lineage_ok,
        geography_vintage=geography.geography_vintage,
        geography_frame_id=binding.geography_frame_id,
        caveat_id=caveat.caveat_id,
        mapper_version=MAPPER_VERSION,
        observations_parquet=observations_to_parquet(observations),
        citation=citation,
        caveat=caveat,
        geography=geography,
    )


def _write_report(logs_root: Path, run_id: str, payload: dict[str, object]) -> Path:
    path = run_report_path(logs_root, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def materialise_c3_vintage(
    data_root: Path,
    logs_root: Path,
    *,
    created_at: datetime | None = None,
) -> tuple[VintageManifest, dict[str, object]]:
    """Write a new C3 vintage. Does not move preview or citizen pointers."""

    moment = ensure_utc(created_at if created_at is not None else datetime.now(UTC))
    run_id = moment.strftime("%Y%m%dT%H%M%SZ")
    series_rows: list[dict[str, object]] = []
    report: dict[str, object] = {
        "run_id": run_id,
        "vintage_id": None,
        "trigger": None,
        "completeness": Completeness.failed.value,
        "series": series_rows,
        "flags": "none",
        "pointers": "untouched",
    }
    try:
        records: list[LineageRecord] = []
        writes: list[SeriesWrite] = []
        for binding in C3_SERIES:
            lineage = load_c3_lineage(data_root, binding)
            records.append(lineage)
            item = map_c3_series(data_root, binding, lineage)
            writes.append(item)
            series_rows.append(
                {
                    "series_id": item.series_id,
                    "observation_count": observation_count(item),
                    "lineage_ok": item.lineage_ok.value,
                    "source_vintage": item.source_vintage,
                    "reused": None,
                    "rewritten": None,
                }
            )
        trigger = trigger_for_records(tuple(records))
        report["trigger"] = trigger.value
        previous = latest_manifest_with_series(data_root, C3_SERIES_IDS)
        manifest = write_vintage(
            data_root,
            created_at=moment,
            trigger=trigger,
            series=tuple(writes),
            completeness=Completeness.complete,
            previous=previous,
            required_series_ids=C3_SERIES_IDS,
        )
        reused_by_id = {entry.series_id: entry.reused for entry in manifest.series}
        for row in series_rows:
            reused = reused_by_id[str(row["series_id"])]
            row["reused"] = reused.value
            row["rewritten"] = (
                YesNo.no.value if reused is YesNo.yes else YesNo.yes.value
            )
        report["vintage_id"] = manifest.vintage_id
        report["completeness"] = manifest.completeness.value
        _write_report(logs_root, run_id, report)
        return manifest, report
    except Exception as exc:
        report["flags"] = str(exc)
        _write_report(logs_root, run_id, report)
        raise
