"""One ingest runner: fetch each catalog artifact once, parse per series."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import httpx

from prism.catalog import Catalog, CatalogArtifact, CatalogSeries, default_catalog
from prism.catalog.registry import PARSERS, RETRIEVERS
from prism.ingest.parsed_table import ParsedTable
from prism.ingest.retrieve import (
    IngestError,
    RetrievedArtifact,
    new_client,
    retrieve_artifact,
    retrieved_at_stamp,
    write_raw_artifact,
)
from prism.paths import ingest_lineage_path, ingest_raw_dir, ingest_table_path, posix
from prism.schema import LineageRecord, SourceChanged, YesNo


def _record_path(data_root: Path, path: Path) -> str:
    return posix(path.relative_to(data_root.parent))


def _load_previous(path: Path) -> LineageRecord | None:
    if not path.exists():
        return None
    return LineageRecord.model_validate_json(path.read_bytes())


def _source_changed(previous: LineageRecord | None, checksum: str) -> SourceChanged:
    if previous is None:
        return SourceChanged.first_retrieve
    if previous.checksum == checksum:
        return SourceChanged.no
    return SourceChanged.yes


def _write_lineage(path: Path, record: LineageRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(record.model_dump_json(indent=2) + "\n", encoding="utf-8")


def _write_derived(path: Path, parsed: ParsedTable, previous_exists: bool) -> None:
    if parsed.lineage_ok is YesNo.yes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(parsed.csv_text, encoding="utf-8", newline="\n")
        return
    if previous_exists:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def _combine_flags(*parts: str) -> str:
    kept = [part for part in parts if part and part != "none"]
    return "; ".join(kept) if kept else "none"


def _failed_record(
    *,
    data_root: Path,
    retrieved_at: str,
    citation_id: str,
    raw_path: Path,
    derived_path: Path,
    checksum: str,
    flags: str,
    previous: LineageRecord | None,
    parser: str,
) -> LineageRecord:
    return LineageRecord(
        raw_path=_record_path(data_root, raw_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=checksum,
        retrieved_at=retrieved_at,
        parser=parser,
        citation_id=citation_id,
        row_count=0,
        nulls="not parsed",
        source_changed=_source_changed(previous, checksum),
        lineage_ok=YesNo.no,
        flags=flags,
    )


def _companion_note(annex: RetrievedArtifact) -> str:
    if annex.http_status != 200:
        return f"companion_annex_http_{annex.http_status}"
    return f"companion_annex={annex.filename} sha256={annex.checksum}"


def _store_artifact(
    data_root: Path,
    entry: CatalogSeries,
    retrieved_at: str,
    artifact: RetrievedArtifact,
    spec_kind: str,
    catalog_artifact: CatalogArtifact,
    companion_fetched: tuple[RetrievedArtifact, ...],
    link_from: Path | None,
) -> tuple[Path, str, str]:
    dest = ingest_raw_dir(
        data_root,
        entry.producer_slug,
        entry.series_id,
        entry.source_vintage,
        retrieved_at,
    )
    artifact_path, how = write_raw_artifact(
        dest, artifact, link_from=link_from, kind=spec_kind
    )
    annex_flag = "none"
    for companion, fetched in zip(
        catalog_artifact.companions, companion_fetched, strict=True
    ):
        if fetched.http_status != 200:
            continue
        annex_link = None if link_from is None else link_from.parent / fetched.filename
        if annex_link is not None and not annex_link.exists():
            annex_link = None
        try:
            write_raw_artifact(
                dest,
                fetched,
                link_from=annex_link,
                headers_name=companion.headers_name,
                kind=catalog_artifact.kind,
            )
        except IngestError as exc:
            annex_flag = f"companion_annex_store_failed:{exc}"
    return artifact_path, how, annex_flag


def _ingest_series(
    data_root: Path,
    entry: CatalogSeries,
    retrieved_at: str,
    artifact: RetrievedArtifact,
    catalog_artifact: CatalogArtifact,
    companion_fetched: tuple[RetrievedArtifact, ...],
    companion_note: str,
    link_from: Path | None,
) -> tuple[LineageRecord, Path]:
    spec = PARSERS[entry.parser_id]
    lineage_path = ingest_lineage_path(
        data_root, entry.producer_slug, entry.series_id, entry.source_vintage
    )
    derived_path = ingest_table_path(
        data_root, entry.producer_slug, entry.series_id, entry.source_vintage
    )
    previous = _load_previous(lineage_path)
    raw_dir = ingest_raw_dir(
        data_root,
        entry.producer_slug,
        entry.series_id,
        entry.source_vintage,
        retrieved_at,
    )
    try:
        artifact_path, how, annex_store_flag = _store_artifact(
            data_root,
            entry,
            retrieved_at,
            artifact,
            spec.kind,
            catalog_artifact,
            companion_fetched,
            link_from,
        )
    except IngestError as exc:
        record = _failed_record(
            data_root=data_root,
            retrieved_at=retrieved_at,
            citation_id=entry.citation_id,
            raw_path=raw_dir / artifact.filename,
            derived_path=derived_path,
            checksum=artifact.checksum,
            flags=str(exc),
            previous=previous,
            parser=spec.lineage_name,
        )
        _write_lineage(lineage_path, record)
        return record, raw_dir / artifact.filename

    parsed = spec.parse(artifact.content)
    flags = parsed.flags
    if catalog_artifact.share_note:
        share_note = f"{catalog_artifact.share_note}:{how}"
        companion = companion_note if companion_note else "companion_annex_absent"
        flags = _combine_flags(parsed.flags, share_note, companion, annex_store_flag)
    if artifact.tls_mode != "verify":
        flags = _combine_flags(flags, f"tls_mode={artifact.tls_mode}")
    record = LineageRecord(
        raw_path=_record_path(data_root, artifact_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=artifact.checksum,
        retrieved_at=retrieved_at,
        parser=spec.lineage_name,
        citation_id=entry.citation_id,
        row_count=parsed.row_count,
        nulls=parsed.nulls,
        source_changed=_source_changed(previous, artifact.checksum),
        lineage_ok=parsed.lineage_ok,
        flags=flags,
    )
    _write_derived(derived_path, parsed, previous_exists=derived_path.exists())
    _write_lineage(lineage_path, record)
    return record, artifact_path


def ingest(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
    catalog: Catalog | None = None,
) -> tuple[LineageRecord, ...]:
    loaded = catalog if catalog is not None else default_catalog()
    known = loaded.series_ids()
    if series_ids is not None:
        unknown = [series_id for series_id in series_ids if series_id not in known]
        if unknown:
            raise IngestError("unknown series_id: " + ", ".join(unknown))
        wanted_ids = series_ids
    else:
        wanted_ids = known
    wanted = [loaded.series(series_id) for series_id in wanted_ids]
    stamp = retrieved_at_stamp(retrieved_at)
    own_client = client is None
    http = client if client is not None else new_client()
    records: list[LineageRecord] = []
    try:
        remaining = list(wanted)
        while remaining:
            first = remaining[0]
            artifact = loaded.slice_for_series(first.series_id).artifact(
                first.artifact_id
            )
            group = [
                entry for entry in remaining if entry.artifact_id == first.artifact_id
            ]
            remaining = [
                entry for entry in remaining if entry.artifact_id != first.artifact_id
            ]
            if artifact.retrieve_id:
                retriever = RETRIEVERS.get(artifact.retrieve_id)
                if retriever is None:
                    raise IngestError(
                        f"unknown retrieve_id: {artifact.retrieve_id}"
                    )
                fetched = retriever.retrieve(
                    http, stamp, artifact.url
                )
            else:
                raw_name = artifact.filename or unquote(
                    artifact.url.rstrip("/").rsplit("/", 1)[-1]
                )
                raw_name = raw_name.split("?", 1)[0].split("#", 1)[0]
                if not raw_name or "." not in raw_name:
                    raw_name = f"{artifact.artifact_id}.{artifact.kind}"
                fetched = retrieve_artifact(
                    artifact.url,
                    client=http,
                    retrieved_at=stamp,
                    filename=raw_name,
                )
            companion_fetched: list[RetrievedArtifact] = []
            companion_note = ""
            annex_ok: list[RetrievedArtifact] = []
            for companion in artifact.companions:
                item = retrieve_artifact(
                    companion.url,
                    client=http,
                    retrieved_at=stamp,
                    filename=unquote(companion.url.rstrip("/").rsplit("/", 1)[-1]),
                )
                companion_fetched.append(item)
                companion_note = _companion_note(item)
                if item.http_status == 200:
                    annex_ok.append(item)
            link_from: Path | None = None
            for entry in group:
                record, artifact_path = _ingest_series(
                    data_root,
                    entry,
                    stamp,
                    fetched,
                    artifact,
                    tuple(companion_fetched),
                    companion_note,
                    link_from,
                )
                records.append(record)
                if artifact_path.exists():
                    link_from = artifact_path
    finally:
        if own_client:
            http.close()
    return tuple(records)


def ingest_c1(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    catalog = default_catalog()
    owned = tuple(entry.series_id for entry in catalog.slice("c1").series)
    if series_ids is None:
        selected = owned
    else:
        unknown = [series_id for series_id in series_ids if series_id not in owned]
        if unknown:
            raise IngestError("unknown series_id: " + ", ".join(unknown))
        selected = tuple(series_id for series_id in owned if series_id in series_ids)
    return ingest(
        data_root, client=client, retrieved_at=retrieved_at, series_ids=selected
    )


def ingest_c2(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    catalog = default_catalog()
    owned = tuple(entry.series_id for entry in catalog.slice("c2").series)
    if series_ids is None:
        selected = owned
    else:
        unknown = [series_id for series_id in series_ids if series_id not in owned]
        if unknown:
            raise IngestError("unknown series_id: " + ", ".join(unknown))
        selected = tuple(series_id for series_id in owned if series_id in series_ids)
    return ingest(
        data_root, client=client, retrieved_at=retrieved_at, series_ids=selected
    )


def ingest_c3(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    catalog = default_catalog()
    owned = tuple(entry.series_id for entry in catalog.slice("c3").series)
    if series_ids is None:
        selected = owned
    else:
        unknown = [series_id for series_id in series_ids if series_id not in owned]
        if unknown:
            raise IngestError("unknown series_id: " + ", ".join(unknown))
        selected = tuple(series_id for series_id in owned if series_id in series_ids)
    return ingest(
        data_root, client=client, retrieved_at=retrieved_at, series_ids=selected
    )
