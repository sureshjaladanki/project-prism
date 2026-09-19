"""One vintage runner. Mapper families stay in c1/c2/c3 modules."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from prism.catalog import Catalog, CatalogSeries, default_catalog
from prism.catalog.registry import MAPPERS
from prism.observation_parquet import observations_from_parquet, observations_to_parquet
from prism.paths import ingest_lineage_path, ingest_table_path, run_report_path
from prism.pipeline.errors import PipelineError
from prism.refresh import (
    SeriesBinding,
    ensure_utc,
    lineage_blocks_completeness,
    trigger_from_lineage,
)
from prism.schema import (
    Completeness,
    LineageRecord,
    ObservationLineage,
    RefreshTrigger,
    VintageManifest,
    YesNo,
)
from prism.vintage_store import SeriesWrite, latest_manifest_with_series, write_vintage


def observation_count(item: SeriesWrite) -> int:
    return len(observations_from_parquet(item.observations_parquet))


def trigger_for_records(records: tuple[LineageRecord, ...]) -> RefreshTrigger:
    if any(
        trigger_from_lineage(record) is RefreshTrigger.source_change
        for record in records
    ):
        return RefreshTrigger.source_change
    return RefreshTrigger.on_demand


def _write_report(logs_root: Path, run_id: str, payload: dict[str, object]) -> Path:
    path = run_report_path(logs_root, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_lineage(data_root: Path, binding: SeriesBinding) -> LineageRecord:
    path = ingest_lineage_path(
        data_root, binding.producer_slug, binding.series_id, binding.source_vintage
    )
    if not path.exists():
        raise PipelineError(f"missing lineage for {binding.series_id}")
    return LineageRecord.model_validate_json(path.read_bytes())


def map_catalog_series(
    data_root: Path,
    entry: CatalogSeries,
    lineage: LineageRecord,
    catalog: Catalog,
) -> SeriesWrite:
    citation = catalog.citations[entry.citation_id]
    caveat = catalog.caveats[entry.caveat_id]
    geography = catalog.geographies[entry.series_id]
    if citation.citation_id != entry.citation_id:
        raise PipelineError("citation_id does not match the locked card")
    if caveat.caveat_id != entry.caveat_id:
        raise PipelineError("caveat_id does not match the locked note")
    if lineage.citation_id != entry.citation_id:
        raise PipelineError(
            f"{entry.series_id} lineage citation_id {lineage.citation_id} "
            f"does not match {entry.citation_id}"
        )
    spec = MAPPERS.get(entry.mapper_id)
    if spec is None:
        raise PipelineError(f"unknown mapper_id: {entry.mapper_id}")
    obs_lineage = ObservationLineage(
        raw_path=lineage.raw_path,
        derived_path=lineage.derived_path,
        checksum=lineage.checksum,
    )
    if entry.named_hole and lineage.lineage_ok is YesNo.no:
        rows: list[dict[str, str]] = []
    elif lineage_blocks_completeness(entry.series_id, lineage.lineage_ok):
        raise PipelineError(
            f"{entry.series_id} lineage_ok={lineage.lineage_ok.value}; not building a vintage"
        )
    else:
        table_path = ingest_table_path(
            data_root, entry.producer_slug, entry.series_id, entry.source_vintage
        )
        if not table_path.exists():
            raise PipelineError(f"missing derived table for {entry.series_id}")
        rows = _read_rows(table_path)
    observations = spec.map_rows(
        rows,
        entry.series_id,
        citation.citation_id,
        caveat.caveat_id,
        geography,
        obs_lineage,
    )
    return SeriesWrite(
        producer=entry.producer,
        series_id=entry.series_id,
        source_vintage=entry.source_vintage,
        raw_checksum=lineage.checksum,
        parser_version=lineage.parser,
        lineage_ok=lineage.lineage_ok,
        geography_vintage=geography.geography_vintage,
        geography_frame_id=entry.geography_frame_id,
        caveat_id=caveat.caveat_id,
        mapper_version=spec.version,
        observations_parquet=observations_to_parquet(observations),
        citation=citation,
        caveat=caveat,
        geography=geography,
    )


def materialise_vintage(
    data_root: Path,
    logs_root: Path,
    *,
    slice_id: str,
    created_at: datetime | None = None,
    catalog: Catalog | None = None,
) -> tuple[VintageManifest, dict[str, object]]:
    """Write a new vintage for one catalog slice. Does not move pointers."""

    loaded = catalog if catalog is not None else default_catalog()
    slice_ = loaded.slice(slice_id)
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
        for entry in slice_.series:
            binding = SeriesBinding(
                card=entry.card,
                series_id=entry.series_id,
                name=entry.name,
                producer=entry.producer,
                producer_slug=entry.producer_slug,
                next_release=entry.next_release,
                geography_frame_id=entry.geography_frame_id,
                geography_vintage=entry.geography_vintage,
                source_vintage=entry.source_vintage,
                citation_id=entry.citation_id,
                caveat_id=entry.caveat_id,
            )
            lineage = load_lineage(data_root, binding)
            records.append(lineage)
            item = map_catalog_series(data_root, entry, lineage, loaded)
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
        series_ids = tuple(entry.series_id for entry in slice_.series)
        previous = latest_manifest_with_series(data_root, series_ids)
        manifest = write_vintage(
            data_root,
            created_at=moment,
            trigger=trigger,
            series=tuple(writes),
            completeness=Completeness.complete,
            previous=previous,
            required_series_ids=series_ids,
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
