"""C3 ingest: Union Budget / CGA artifacts. Stop at the producer table."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import httpx

from prism.ingest.parse import ParsedTable
from prism.ingest.parse_c3 import (
    PARSER,
    parse_afs_pdf,
    parse_annex1_pdf,
    parse_cga_finance_accounts_pdf,
    parse_cga_monthly_html,
    parse_deficit_statistics_xlsx,
    parse_expenditure_stat1_xlsx,
    parse_frbm_statements_pdf,
    parse_liabilities_pdf,
    parse_receipt_xlsx,
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
    C3_SERIES_BY_ID,
    C3_SERIES_IDS,
    SERIES_BUDGET_2026_27_AFS,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
    SERIES_BUDGET_2026_27_LIABILITIES,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
    SERIES_CGA_MONTHLY_GLANCE_2026_07,
)
from prism.schema import LineageRecord, SourceChanged, YesNo

TAX_URL = "https://www.indiabudget.gov.in/doc/rec/tr.xlsx"
NON_TAX_URL = "https://www.indiabudget.gov.in/doc/rec/ntr.xlsx"
CAPITAL_URL = "https://www.indiabudget.gov.in/doc/rec/ctr.xlsx"
ANNEX1_URL = "https://www.indiabudget.gov.in/doc/rec/annex1.pdf"
STAT1_URL = "https://www.indiabudget.gov.in/doc/eb/stat1.xlsx"
BAG_URL = "https://www.indiabudget.gov.in/doc/Budget_at_Glance/budget_at_a_glance.xlsx"
LIABILITIES_URL = "https://www.indiabudget.gov.in/doc/rec/annex91.pdf"
FRBM_URL = "https://www.indiabudget.gov.in/doc/frbm1.pdf"
AFS_URL = "https://www.indiabudget.gov.in/doc/AFS/allafs.pdf"
CGA_MONTHLY_URL = "https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.htm"
CGA_FA_URL = "https://cga.gov.in/writereaddata/file/Fin20242025Statement1.pdf"

_KIND = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: "xlsx",
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: "xlsx",
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: "xlsx",
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: "pdf",
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: "xlsx",
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: "xlsx",
    SERIES_BUDGET_2026_27_LIABILITIES: "pdf",
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: "pdf",
    SERIES_BUDGET_2026_27_AFS: "pdf",
    SERIES_CGA_MONTHLY_GLANCE_2026_07: "html",
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: "pdf",
}

_URL = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: TAX_URL,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: NON_TAX_URL,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: CAPITAL_URL,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: ANNEX1_URL,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: STAT1_URL,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: BAG_URL,
    SERIES_BUDGET_2026_27_LIABILITIES: LIABILITIES_URL,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: FRBM_URL,
    SERIES_BUDGET_2026_27_AFS: AFS_URL,
    SERIES_CGA_MONTHLY_GLANCE_2026_07: CGA_MONTHLY_URL,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: CGA_FA_URL,
}

_PARSERS = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: parse_receipt_xlsx,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: parse_receipt_xlsx,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: parse_receipt_xlsx,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: parse_annex1_pdf,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: parse_expenditure_stat1_xlsx,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: parse_deficit_statistics_xlsx,
    SERIES_BUDGET_2026_27_LIABILITIES: parse_liabilities_pdf,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: parse_frbm_statements_pdf,
    SERIES_BUDGET_2026_27_AFS: parse_afs_pdf,
    SERIES_CGA_MONTHLY_GLANCE_2026_07: parse_cga_monthly_html,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: parse_cga_finance_accounts_pdf,
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
    binding = C3_SERIES_BY_ID[series_id]
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


def ingest_c3(
    data_root: Path,
    *,
    client: httpx.Client | None = None,
    retrieved_at: datetime | None = None,
    series_ids: tuple[str, ...] | None = None,
) -> tuple[LineageRecord, ...]:
    requested = C3_SERIES_IDS if series_ids is None else series_ids
    unknown = [series_id for series_id in requested if series_id not in C3_SERIES_BY_ID]
    if unknown:
        raise IngestError("unknown series_id: " + ", ".join(unknown))
    wanted = tuple(series_id for series_id in C3_SERIES_IDS if series_id in requested)
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
