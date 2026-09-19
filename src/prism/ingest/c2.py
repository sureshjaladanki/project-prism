"""C2 ingest: Census / ORGI / NCP artifacts. Stop at the producer table."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import httpx

from prism.ingest.parse import ParsedTable
from prism.ingest.parse_c2 import (
    PARSER,
    parse_census_2011_a02_xls,
    parse_census_2011_pca_sd,
    parse_ncp_projections_table8,
    parse_srs_bulletin_2024,
    parse_srs_statistical_report_2024,
)
from prism.ingest.retrieve import (
    IngestError,
    RetrievedArtifact,
    new_client,
    retrieve_artifact,
    retrieved_at_stamp,
    write_raw_artifact,
)
from prism.paths import ingest_lineage_path, ingest_raw_dir, ingest_table_path, posix
from prism.refresh import (
    C2_SERIES_BY_ID,
    C2_SERIES_IDS,
    SERIES_CENSUS_2011_A02_DECADAL,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
    SERIES_SRS_BULLETIN_2024,
    SERIES_SRS_STATISTICAL_REPORT_2024,
)
from prism.schema import LineageRecord, SourceChanged, YesNo

PCA_URL = (
    "https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/"
    "DDW_PCA0000_2011_Indiastatedist.xlsx"
)
A02_XLS_URL = (
    "https://censusindia.gov.in/nada/index.php/catalog/43333/download/47001/"
    "00%20A%202-India.xls"
)
SRS_BULLETIN_URL = (
    "https://censusindia.gov.in/nada/index.php/catalog/47150/download/51394/"
    "SRS_Bulletin_2024_Vol_59_No_1.pdf"
)
SRS_STAT_URL = (
    "https://censusindia.gov.in/nada/index.php/catalog/47152/download/51396/"
    "SRS_STAT_2024.pdf"
)
NCP_TABLE8_URL = (
    "https://nhm.gov.in/New_Updates_2018/Report_Population_Projection_2019.pdf"
)

_KIND = {
    SERIES_CENSUS_2011_PCA_SD: "xlsx",
    SERIES_CENSUS_2011_A02_DECADAL: "xls",
    SERIES_SRS_BULLETIN_2024: "pdf",
    SERIES_SRS_STATISTICAL_REPORT_2024: "pdf",
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: "pdf",
}

_URL = {
    SERIES_CENSUS_2011_PCA_SD: PCA_URL,
    SERIES_CENSUS_2011_A02_DECADAL: A02_XLS_URL,
    SERIES_SRS_BULLETIN_2024: SRS_BULLETIN_URL,
    SERIES_SRS_STATISTICAL_REPORT_2024: SRS_STAT_URL,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: NCP_TABLE8_URL,
}

_PARSERS = {
    SERIES_CENSUS_2011_PCA_SD: parse_census_2011_pca_sd,
    SERIES_CENSUS_2011_A02_DECADAL: parse_census_2011_a02_xls,
    SERIES_SRS_BULLETIN_2024: parse_srs_bulletin_2024,
    SERIES_SRS_STATISTICAL_REPORT_2024: parse_srs_statistical_report_2024,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: parse_ncp_projections_table8,
}


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


def _failed_record(
    *,
    data_root: Path,
    binding_citation_id: str,
    retrieved_at: str,
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
        citation_id=binding_citation_id,
        row_count=0,
        nulls="not parsed",
        source_changed=_source_changed(previous, checksum),
        lineage_ok=YesNo.no,
        flags=flags,
    )


def _ingest_series(
    data_root: Path,
    series_id: str,
    retrieved_at: str,
    artifact: RetrievedArtifact,
) -> LineageRecord:
    binding = C2_SERIES_BY_ID[series_id]
    lineage_path = ingest_lineage_path(
        data_root, binding.producer_slug, series_id, binding.source_vintage
    )
    derived_path = ingest_table_path(
        data_root, binding.producer_slug, series_id, binding.source_vintage
    )
    previous = _load_previous(lineage_path)
    raw_dir = ingest_raw_dir(
        data_root,
        binding.producer_slug,
        series_id,
        binding.source_vintage,
        retrieved_at,
    )
    try:
        artifact_path, _how = write_raw_artifact(
            raw_dir, artifact, kind=_KIND[series_id]
        )
    except IngestError as exc:
        record = _failed_record(
            data_root=data_root,
            binding_citation_id=binding.citation_id,
            retrieved_at=retrieved_at,
            raw_path=raw_dir / artifact.filename,
            derived_path=derived_path,
            checksum=artifact.checksum,
            flags=str(exc),
            previous=previous,
        )
        _write_lineage(lineage_path, record)
        return record

    parsed = _PARSERS[series_id](artifact.content)
    record = LineageRecord(
        raw_path=_record_path(data_root, artifact_path),
        derived_path=_record_path(data_root, derived_path),
        checksum=artifact.checksum,
        retrieved_at=retrieved_at,
        parser=PARSER,
        citation_id=binding.citation_id,
        row_count=parsed.row_count,
        nulls=parsed.nulls,
        source_changed=_source_changed(previous, artifact.checksum),
        lineage_ok=parsed.lineage_ok,
        flags=parsed.flags,
    )
    _write_derived(derived_path, parsed, previous_exists=derived_path.exists())
    _write_lineage(lineage_path, record)
    return record


def ingest_c2(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    requested = C2_SERIES_IDS if series_ids is None else series_ids
    unknown = [series_id for series_id in requested if series_id not in C2_SERIES_BY_ID]
    if unknown:
        raise IngestError("unknown series_id: " + ", ".join(unknown))
    wanted = tuple(series_id for series_id in C2_SERIES_IDS if series_id in requested)
    stamp = retrieved_at_stamp(retrieved_at)
    own_client = client is None
    http = client if client is not None else new_client()
    records: list[LineageRecord] = []
    try:
        for series_id in wanted:
            url = _URL[series_id]
            artifact = retrieve_artifact(
                url,
                client=http,
                retrieved_at=stamp,
                filename=unquote(url.rstrip("/").rsplit("/", 1)[-1]),
            )
            records.append(_ingest_series(data_root, series_id, stamp, artifact))
    finally:
        if own_client:
            http.close()
    return tuple(records)
