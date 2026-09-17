"""C1 ingest: MoSPI CPI Base 2024=100. Stop at the producer table."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import httpx

from prism.ingest.parse import (
    PARSER,
    ParsedTable,
    parse_cpi_back_series,
    parse_cpi_cfpi,
    parse_cpi_division_group,
    parse_cpi_general,
)
from prism.ingest.retrieve import (
    IngestError,
    RetrievedArtifact,
    new_client,
    retrieve_artifact,
    retrieved_at_stamp,
    write_raw_artifact,
)
from prism.paths import (
    PRODUCER_SLUG_MOSPI,
    ingest_lineage_path,
    ingest_raw_dir,
    ingest_table_path,
    posix,
)
from prism.refresh import (
    C1_SERIES_BY_ID,
    C1_SERIES_IDS,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import LineageRecord, SourceChanged, YesNo

MONTHLY_URL = (
    "https://www.mospi.gov.in/uploads/documents/productChartTable/"
    "1789491098345-Data_August_CPI_2026_14092026.xlsx"
)
ANNEX_URL = (
    "https://www.mospi.gov.in/uploads/documents/productChartTable/"
    "1789491131821-Annex.xlsx"
)
BACK_SERIES_URL = (
    "https://www.mospi.gov.in/uploads/documents/CPI/"
    "CPI_2024-Back-Series-Index-Inflation.xlsx"
)

MONTHLY_SERIES_IDS: tuple[str, ...] = (
    SERIES_CPI_GENERAL_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
)

_PARSERS = {
    SERIES_CPI_GENERAL_BASE_2024: parse_cpi_general,
    SERIES_CPI_CFPI_BASE_2024: parse_cpi_cfpi,
    SERIES_CPI_DIVISION_GROUP_BASE_2024: parse_cpi_division_group,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024: parse_cpi_back_series,
}


@dataclass(frozen=True)
class CompanionNote:
    filename: str
    checksum: str
    http_status: int
    flags: str


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
    series_id: str,
    source_vintage: str,
    retrieved_at: str,
    citation_id: str,
    raw_path: Path,
    derived_path: Path,
    checksum: str,
    flags: str,
    previous: LineageRecord | None,
) -> LineageRecord:
    return LineageRecord(
        raw_path=_record_path(data_root, raw_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=checksum,
        retrieved_at=retrieved_at,
        parser=PARSER,
        citation_id=citation_id,
        row_count=0,
        nulls="not parsed",
        source_changed=_source_changed(previous, checksum),
        lineage_ok=YesNo.no,
        flags=flags,
    )


def _store_shared_raw(
    data_root: Path,
    series_id: str,
    source_vintage: str,
    retrieved_at: str,
    monthly: RetrievedArtifact,
    annex: RetrievedArtifact | None,
    link_from: Path | None,
) -> tuple[Path, str, str]:
    dest = ingest_raw_dir(
        data_root, PRODUCER_SLUG_MOSPI, series_id, source_vintage, retrieved_at
    )
    artifact_path, how = write_raw_artifact(dest, monthly, link_from=link_from)
    annex_flag = "none"
    if annex is not None:
        annex_link = None if link_from is None else link_from.parent / annex.filename
        if annex_link is not None and not annex_link.exists():
            annex_link = None
        try:
            write_raw_artifact(
                dest,
                annex,
                link_from=annex_link,
                headers_name="annex_headers.json",
            )
        except IngestError as exc:
            annex_flag = f"companion_annex_store_failed:{exc}"
    return artifact_path, how, annex_flag


def _ingest_monthly_series(
    data_root: Path,
    series_id: str,
    retrieved_at: str,
    monthly: RetrievedArtifact,
    annex: RetrievedArtifact | None,
    companion: CompanionNote | None,
    link_from: Path | None,
) -> tuple[LineageRecord, Path]:
    binding = C1_SERIES_BY_ID[series_id]
    lineage_path = ingest_lineage_path(
        data_root, PRODUCER_SLUG_MOSPI, series_id, binding.source_vintage
    )
    derived_path = ingest_table_path(
        data_root, PRODUCER_SLUG_MOSPI, series_id, binding.source_vintage
    )
    previous = _load_previous(lineage_path)
    raw_dir = ingest_raw_dir(
        data_root,
        PRODUCER_SLUG_MOSPI,
        series_id,
        binding.source_vintage,
        retrieved_at,
    )
    try:
        artifact_path, how, annex_store_flag = _store_shared_raw(
            data_root,
            series_id,
            binding.source_vintage,
            retrieved_at,
            monthly,
            annex,
            link_from,
        )
    except IngestError as exc:
        record = _failed_record(
            data_root=data_root,
            series_id=series_id,
            source_vintage=binding.source_vintage,
            retrieved_at=retrieved_at,
            citation_id=binding.citation_id,
            raw_path=raw_dir / monthly.filename,
            derived_path=derived_path,
            checksum=monthly.checksum,
            flags=str(exc),
            previous=previous,
        )
        _write_lineage(lineage_path, record)
        return record, raw_dir / monthly.filename

    parsed = _PARSERS[series_id](monthly.content)
    share_note = f"shared_monthly_xlsx:{how}"
    companion_note = companion.flags if companion is not None else "companion_annex_absent"
    flags = _combine_flags(parsed.flags, share_note, companion_note, annex_store_flag)
    record = LineageRecord(
        raw_path=_record_path(data_root, artifact_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=monthly.checksum,
        retrieved_at=retrieved_at,
        parser=PARSER,
        citation_id=binding.citation_id,
        row_count=parsed.row_count,
        nulls=parsed.nulls,
        source_changed=_source_changed(previous, monthly.checksum),
        lineage_ok=parsed.lineage_ok,
        flags=flags,
    )
    _write_derived(derived_path, parsed, previous_exists=derived_path.exists())
    _write_lineage(lineage_path, record)
    return record, artifact_path


def _ingest_back_series(
    data_root: Path,
    retrieved_at: str,
    back: RetrievedArtifact,
) -> LineageRecord:
    series_id = SERIES_CPI_BACK_SERIES_LINKED_BASE_2024
    binding = C1_SERIES_BY_ID[series_id]
    lineage_path = ingest_lineage_path(
        data_root, PRODUCER_SLUG_MOSPI, series_id, binding.source_vintage
    )
    derived_path = ingest_table_path(
        data_root, PRODUCER_SLUG_MOSPI, series_id, binding.source_vintage
    )
    previous = _load_previous(lineage_path)
    raw_dir = ingest_raw_dir(
        data_root,
        PRODUCER_SLUG_MOSPI,
        series_id,
        binding.source_vintage,
        retrieved_at,
    )
    try:
        artifact_path, _how = write_raw_artifact(raw_dir, back)
    except IngestError as exc:
        record = _failed_record(
            data_root=data_root,
            series_id=series_id,
            source_vintage=binding.source_vintage,
            retrieved_at=retrieved_at,
            citation_id=binding.citation_id,
            raw_path=raw_dir / back.filename,
            derived_path=derived_path,
            checksum=back.checksum,
            flags=str(exc),
            previous=previous,
        )
        _write_lineage(lineage_path, record)
        return record

    parsed = parse_cpi_back_series(back.content)
    record = LineageRecord(
        raw_path=_record_path(data_root, artifact_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=back.checksum,
        retrieved_at=retrieved_at,
        parser=PARSER,
        citation_id=binding.citation_id,
        row_count=parsed.row_count,
        nulls=parsed.nulls,
        source_changed=_source_changed(previous, back.checksum),
        lineage_ok=parsed.lineage_ok,
        flags=parsed.flags,
    )
    _write_derived(derived_path, parsed, previous_exists=derived_path.exists())
    _write_lineage(lineage_path, record)
    return record


def _companion_note(annex: RetrievedArtifact) -> CompanionNote:
    if annex.http_status != 200:
        return CompanionNote(
            filename=annex.filename,
            checksum=annex.checksum,
            http_status=annex.http_status,
            flags=f"companion_annex_http_{annex.http_status}",
        )
    return CompanionNote(
        filename=annex.filename,
        checksum=annex.checksum,
        http_status=annex.http_status,
        flags=f"companion_annex={annex.filename} sha256={annex.checksum}",
    )


def ingest_c1(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    requested = C1_SERIES_IDS if series_ids is None else series_ids
    unknown = [series_id for series_id in requested if series_id not in C1_SERIES_BY_ID]
    if unknown:
        raise IngestError("unknown series_id: " + ", ".join(unknown))
    wanted = tuple(series_id for series_id in C1_SERIES_IDS if series_id in requested)
    stamp = retrieved_at_stamp(retrieved_at)
    own_client = client is None
    http = client if client is not None else new_client()
    records: list[LineageRecord] = []
    try:
        monthly_wanted = tuple(
            series_id for series_id in wanted if series_id in MONTHLY_SERIES_IDS
        )
        if monthly_wanted:
            monthly = retrieve_artifact(MONTHLY_URL, client=http, retrieved_at=stamp)
            annex_retrieved = retrieve_artifact(
                ANNEX_URL, client=http, retrieved_at=stamp
            )
            companion = _companion_note(annex_retrieved)
            annex: RetrievedArtifact | None = (
                annex_retrieved if annex_retrieved.http_status == 200 else None
            )
            link_from: Path | None = None
            for series_id in monthly_wanted:
                record, artifact_path = _ingest_monthly_series(
                    data_root,
                    series_id,
                    stamp,
                    monthly,
                    annex,
                    companion,
                    link_from,
                )
                records.append(record)
                if artifact_path.exists():
                    link_from = artifact_path
        if SERIES_CPI_BACK_SERIES_LINKED_BASE_2024 in wanted:
            back = retrieve_artifact(BACK_SERIES_URL, client=http, retrieved_at=stamp)
            records.append(_ingest_back_series(data_root, stamp, back))
    finally:
        if own_client:
            http.close()
    return tuple(records)
