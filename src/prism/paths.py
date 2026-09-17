"""Store layout under data/. Paths in records use POSIX (forward slashes)."""

from __future__ import annotations

from pathlib import Path

CAS_DIRNAME = "cas"
VINTAGES_DIRNAME = "vintages"
RENDERS_DIRNAME = "renders"
POINTERS_DIRNAME = "pointers"
RAW_DIRNAME = "raw"
DERIVED_DIRNAME = "derived"
LINEAGE_DIRNAME = "lineage"

CITIZEN_POINTER = "citizen"
PREVIEW_POINTER = "preview"
RENDER_COMPLETE_MARKER = "COMPLETE"

OBSERVATIONS_FILENAME = "observations.parquet"
CITATION_FILENAME = "citation.json"
CAVEAT_FILENAME = "caveat.json"
GEOGRAPHY_FILENAME = "geography.json"
MANIFEST_FILENAME = "manifest.json"
TABLE_FILENAME = "table.csv"
LINEAGE_FILENAME = "lineage.json"
HEADERS_FILENAME = "headers.json"
REPORT_FILENAME = "report.json"

PRODUCER_SLUG_MOSPI = "mospi"


def posix(path: Path) -> str:
    return path.as_posix()


def cas_dir(data_root: Path) -> Path:
    return data_root / CAS_DIRNAME


def cas_path(data_root: Path, sha256_hex: str) -> Path:
    return cas_dir(data_root) / sha256_hex


def vintages_dir(data_root: Path) -> Path:
    return data_root / VINTAGES_DIRNAME


def vintage_dir(data_root: Path, vintage_id: str) -> Path:
    return vintages_dir(data_root) / vintage_id


def series_dir(data_root: Path, vintage_id: str, series_id: str) -> Path:
    return vintage_dir(data_root, vintage_id) / "series" / series_id


def renders_dir(data_root: Path) -> Path:
    return data_root / RENDERS_DIRNAME


def render_dir(data_root: Path, vintage_id: str) -> Path:
    return renders_dir(data_root) / vintage_id


def render_complete_path(data_root: Path, vintage_id: str) -> Path:
    return render_dir(data_root, vintage_id) / RENDER_COMPLETE_MARKER


def pointers_dir(data_root: Path) -> Path:
    return data_root / POINTERS_DIRNAME


def citizen_pointer_path(data_root: Path) -> Path:
    return pointers_dir(data_root) / CITIZEN_POINTER


def preview_pointer_path(data_root: Path) -> Path:
    return pointers_dir(data_root) / PREVIEW_POINTER


def ingest_raw_dir(
    data_root: Path,
    producer_slug: str,
    series_id: str,
    source_vintage: str,
    retrieved_at: str,
) -> Path:
    return data_root / RAW_DIRNAME / producer_slug / series_id / source_vintage / retrieved_at


def ingest_derived_dir(
    data_root: Path,
    producer_slug: str,
    series_id: str,
    source_vintage: str,
) -> Path:
    return data_root / DERIVED_DIRNAME / producer_slug / series_id / source_vintage


def ingest_lineage_dir(
    data_root: Path,
    producer_slug: str,
    series_id: str,
    source_vintage: str,
) -> Path:
    return data_root / LINEAGE_DIRNAME / producer_slug / series_id / source_vintage


def ingest_table_path(
    data_root: Path,
    producer_slug: str,
    series_id: str,
    source_vintage: str,
) -> Path:
    return ingest_derived_dir(data_root, producer_slug, series_id, source_vintage) / TABLE_FILENAME


def ingest_lineage_path(
    data_root: Path,
    producer_slug: str,
    series_id: str,
    source_vintage: str,
) -> Path:
    return ingest_lineage_dir(data_root, producer_slug, series_id, source_vintage) / LINEAGE_FILENAME


def run_report_path(logs_root: Path, run_id: str) -> Path:
    return logs_root / run_id / REPORT_FILENAME
