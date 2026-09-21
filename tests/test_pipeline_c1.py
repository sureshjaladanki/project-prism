"""C1 pipeline: derived tables → immutable vintage. Does not publish."""

from __future__ import annotations

import csv
import hashlib
import io
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from prism.catalog import (
    names_by_code,
    slice_caveats,
    slice_citations,
    slice_geographies,
)
from prism.ingest.xlsx_cpi_period import (
    parse_cpi_back_series,
    parse_cpi_cfpi,
    parse_cpi_division_group,
    parse_cpi_general,
)
from prism.observation_parquet import observations_from_parquet
from prism.paths import (
    PRODUCER_SLUG_MOSPI,
    cas_path,
    citizen_pointer_path,
    ingest_lineage_path,
    ingest_table_path,
    preview_pointer_path,
    series_dir,
)
from prism.pipeline.state_sector_period import (
    MAPPER_VERSION,
    PipelineError,
    map_derived_table,
)
from prism.pipeline.run import materialise_vintage
from prism.refresh import (
    C1_SERIES,
    C1_SERIES_IDS,
    CARD_4_SOURCE_VINTAGE,
    CARDS_1_3_SOURCE_VINTAGE,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import (
    CodeSystem,
    Completeness,
    LineageRecord,
    ObservationLineage,
    ObservationStatus,
    RefreshTrigger,
    SourceChanged,
    YesNo,
)
from prism.vintage_store import load_manifest, payload_checksum
from tests.cpi_xlsx_fixtures import back_series_bytes, monthly_workbook_bytes
from tests.factories import CREATED_AT

C1_CAVEATS = slice_caveats("c1")
C1_CITATIONS = slice_citations("c1")
C1_GEOGRAPHIES = slice_geographies("c1")
FRAME_A_NAME_BY_CODE = names_by_code(SERIES_CPI_GENERAL_BASE_2024)
FRAME_B_NAME_BY_CODE = names_by_code(SERIES_CPI_BACK_SERIES_LINKED_BASE_2024)
FRAME_A_GEOGRAPHY = C1_GEOGRAPHIES[SERIES_CPI_GENERAL_BASE_2024]

LATER = datetime(2026, 9, 16, 10, 0, tzinfo=UTC)


def _csv(series_id: str) -> str:
    monthly = monthly_workbook_bytes()
    if series_id == SERIES_CPI_GENERAL_BASE_2024:
        return parse_cpi_general(monthly).csv_text
    if series_id == SERIES_CPI_CFPI_BASE_2024:
        return parse_cpi_cfpi(monthly).csv_text
    if series_id == SERIES_CPI_DIVISION_GROUP_BASE_2024:
        return parse_cpi_division_group(monthly).csv_text
    return parse_cpi_back_series(back_series_bytes()).csv_text


def _seed_c1(data_root: Path, *, lineage_ok: YesNo = YesNo.yes) -> None:
    for binding in C1_SERIES:
        table = ingest_table_path(
            data_root, PRODUCER_SLUG_MOSPI, binding.series_id, binding.source_vintage
        )
        table.parent.mkdir(parents=True, exist_ok=True)
        table.write_text(_csv(binding.series_id), encoding="utf-8", newline="\n")
        lineage_path = ingest_lineage_path(
            data_root, PRODUCER_SLUG_MOSPI, binding.series_id, binding.source_vintage
        )
        lineage_path.parent.mkdir(parents=True, exist_ok=True)
        record = LineageRecord(
            raw_path=f"data/raw/mospi/{binding.series_id}/{binding.source_vintage}/20260916T090713Z/artifact.xlsx",
            derived_path=f"data/derived/mospi/{binding.series_id}/{binding.source_vintage}/table.csv",
            checksum="c" * 64,
            retrieved_at="20260916T090713Z",
            parser="mospi-cpi-xlsx-1.0.0",
            citation_id=binding.citation_id,
            row_count=1,
            nulls="none",
            source_changed=SourceChanged.first_retrieve,
            lineage_ok=lineage_ok,
            flags="none",
        )
        lineage_path.write_text(
            record.model_dump_json(indent=2) + "\n", encoding="utf-8"
        )


def _lineage() -> ObservationLineage:
    return ObservationLineage(
        raw_path="data/raw/mospi/cpi-general-base-2024/2026-08/20260916T090713Z/artifact.xlsx",
        derived_path="data/derived/mospi/cpi-general-base-2024/2026-08/table.csv",
        checksum="a" * 64,
    )


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def test_mapper_does_not_invent_chandigarh_rural() -> None:

    observations = map_derived_table(
        series_id=SERIES_CPI_GENERAL_BASE_2024,
        rows=_rows(_csv(SERIES_CPI_GENERAL_BASE_2024)),
        citation_id=C1_CITATIONS[SERIES_CPI_GENERAL_BASE_2024].citation_id,
        caveat_id=C1_CAVEATS[SERIES_CPI_GENERAL_BASE_2024].caveat_id,
        geography=C1_GEOGRAPHIES[SERIES_CPI_GENERAL_BASE_2024],
        names=FRAME_A_NAME_BY_CODE,
        lineage=_lineage(),
    )
    chandigarh_rural = [
        item
        for item in observations
        if item.geography.code == "04" and item.sector == "Rural"
    ]
    assert chandigarh_rural == []
    chandigarh = [item for item in observations if item.geography.code == "04"]
    assert {item.sector for item in chandigarh} == {"Urban", "Combined"}


def test_combined_is_a_published_sector_not_geography() -> None:

    observations = map_derived_table(
        series_id=SERIES_CPI_GENERAL_BASE_2024,
        rows=_rows(_csv(SERIES_CPI_GENERAL_BASE_2024)),
        citation_id=C1_CITATIONS[SERIES_CPI_GENERAL_BASE_2024].citation_id,
        caveat_id=C1_CAVEATS[SERIES_CPI_GENERAL_BASE_2024].caveat_id,
        geography=C1_GEOGRAPHIES[SERIES_CPI_GENERAL_BASE_2024],
        names=FRAME_A_NAME_BY_CODE,
        lineage=_lineage(),
    )
    combined = [item for item in observations if item.sector == "Combined"]
    assert combined
    assert all(item.geography.code != "Combined" for item in combined)
    assert any(item.geography.code == "00" for item in combined)


def test_blank_inflation_is_unknown_not_zero() -> None:

    observations = map_derived_table(
        series_id=SERIES_CPI_GENERAL_BASE_2024,
        rows=_rows(_csv(SERIES_CPI_GENERAL_BASE_2024)),
        citation_id=C1_CITATIONS[SERIES_CPI_GENERAL_BASE_2024].citation_id,
        caveat_id=C1_CAVEATS[SERIES_CPI_GENERAL_BASE_2024].caveat_id,
        geography=C1_GEOGRAPHIES[SERIES_CPI_GENERAL_BASE_2024],
        names=FRAME_A_NAME_BY_CODE,
        lineage=_lineage(),
    )
    inflation = [
        item
        for item in observations
        if item.geography.code == "01"
        and item.sector == "Rural"
        and item.unit == "inflation (%)"
    ]
    assert len(inflation) == 1
    assert inflation[0].value is None
    assert inflation[0].status is ObservationStatus.unknown


def test_card_4_is_not_stitched_into_card_1() -> None:

    observations = map_derived_table(
        series_id=SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
        rows=_rows(_csv(SERIES_CPI_BACK_SERIES_LINKED_BASE_2024)),
        citation_id=C1_CITATIONS[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024].citation_id,
        caveat_id=C1_CAVEATS[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024].caveat_id,
        geography=C1_GEOGRAPHIES[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024],
        names=FRAME_B_NAME_BY_CODE,
        lineage=_lineage(),
    )
    assert {item.series_id for item in observations} == {
        SERIES_CPI_BACK_SERIES_LINKED_BASE_2024
    }
    assert {item.geography.code for item in observations} == {"00"}
    assert all(item.geography.geography_vintage == "2024" for item in observations)


def test_map_fails_without_citation_id() -> None:

    with pytest.raises(PipelineError, match="citation_id"):
        map_derived_table(
            series_id=SERIES_CPI_GENERAL_BASE_2024,
            rows=_rows(_csv(SERIES_CPI_GENERAL_BASE_2024)),
            citation_id="",
            caveat_id=C1_CAVEATS[SERIES_CPI_GENERAL_BASE_2024].caveat_id,
            geography=C1_GEOGRAPHIES[SERIES_CPI_GENERAL_BASE_2024],
            names=FRAME_A_NAME_BY_CODE,
            lineage=_lineage(),
        )


def test_all_india_is_published_unit() -> None:

    codes = {unit.code for unit in FRAME_A_GEOGRAPHY.units_included}
    assert "00" in codes
    assert FRAME_A_GEOGRAPHY.code_system is CodeSystem.producer_specific


def test_lineage_ok_no_does_not_write_vintage(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c1(data_root, lineage_ok=YesNo.no)
    with pytest.raises(PipelineError, match="lineage_ok"):
        materialise_vintage(data_root, logs_root, slice_id="c1", created_at=CREATED_AT)
    assert not (data_root / "vintages").exists() or not any(
        (data_root / "vintages").iterdir()
    )


def test_first_vintage_rewrites_all_four_and_leaves_pointers(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c1(data_root)
    manifest, report = materialise_vintage(
        data_root, logs_root, slice_id="c1", created_at=CREATED_AT
    )
    assert manifest.completeness is Completeness.complete
    assert manifest.trigger is RefreshTrigger.source_change
    assert [entry.series_id for entry in manifest.series] == list(C1_SERIES_IDS)
    assert all(entry.reused is YesNo.no for entry in manifest.series)
    assert all(entry.mapper_version == MAPPER_VERSION for entry in manifest.series)
    assert report["pointers"] == "untouched"
    assert not citizen_pointer_path(data_root).exists()
    assert not preview_pointer_path(data_root).exists()
    for entry in manifest.series:
        parquet = (
            series_dir(data_root, manifest.vintage_id, entry.series_id)
            / "observations.parquet"
        )
        digest = hashlib.sha256(parquet.read_bytes()).hexdigest()
        cas = cas_path(data_root, digest)
        assert os.path.samefile(parquet, cas)


def test_second_vintage_hard_links_unchanged_series(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c1(data_root)
    first, _report_a = materialise_vintage(
        data_root, logs_root, slice_id="c1", created_at=CREATED_AT
    )
    second, report_b = materialise_vintage(
        data_root, logs_root, slice_id="c1", created_at=LATER
    )
    assert first.vintage_id != second.vintage_id
    assert all(entry.reused is YesNo.yes for entry in second.series)
    assert all(row["rewritten"] == "no" for row in report_b["series"])  # type: ignore[index]
    series_id = SERIES_CPI_GENERAL_BASE_2024
    path_a = series_dir(data_root, first.vintage_id, series_id) / "observations.parquet"
    path_b = (
        series_dir(data_root, second.vintage_id, series_id) / "observations.parquet"
    )
    digest = hashlib.sha256(path_a.read_bytes()).hexdigest()
    cas = cas_path(data_root, digest)
    assert os.path.samefile(path_a, cas)
    assert os.path.samefile(path_b, cas)
    assert os.stat(cas).st_nlink >= 3
    loaded = load_manifest(data_root, second.vintage_id)
    assert loaded.series[0].payload_checksum == first.series[0].payload_checksum


def test_card_3_units_keep_division_and_group_distinct() -> None:

    observations = map_derived_table(
        series_id=SERIES_CPI_DIVISION_GROUP_BASE_2024,
        rows=_rows(_csv(SERIES_CPI_DIVISION_GROUP_BASE_2024)),
        citation_id=C1_CITATIONS[SERIES_CPI_DIVISION_GROUP_BASE_2024].citation_id,
        caveat_id=C1_CAVEATS[SERIES_CPI_DIVISION_GROUP_BASE_2024].caveat_id,
        geography=C1_GEOGRAPHIES[SERIES_CPI_DIVISION_GROUP_BASE_2024],
        names=FRAME_A_NAME_BY_CODE,
        lineage=_lineage(),
    )
    units = {item.unit for item in observations}
    assert any(
        unit.startswith("index (Base 2024=100); Division code ") for unit in units
    )
    assert any(unit.startswith("index (Base 2024=100); Group code ") for unit in units)
    assert "index (Base 2024=100); Division code 12" not in units


def test_payload_checksum_matches_cas_parts(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c1(data_root)
    manifest, _report = materialise_vintage(
        data_root, logs_root, slice_id="c1", created_at=CREATED_AT
    )
    from prism.paths import CAVEAT_FILENAME, CITATION_FILENAME, GEOGRAPHY_FILENAME
    from prism.schema import CaveatNote, Citation, GeographyVintage

    for entry in manifest.series:
        folder = series_dir(data_root, manifest.vintage_id, entry.series_id)
        observations = folder / "observations.parquet"
        citation = Citation.model_validate_json(
            (folder / CITATION_FILENAME).read_bytes()
        )
        caveat = CaveatNote.model_validate_json((folder / CAVEAT_FILENAME).read_bytes())
        geography = GeographyVintage.model_validate_json(
            (folder / GEOGRAPHY_FILENAME).read_bytes()
        )
        assert (
            payload_checksum(observations.read_bytes(), citation, caveat, geography)
            == entry.payload_checksum
        )
        loaded = observations_from_parquet(observations.read_bytes())
        assert loaded
        assert all(item.citation_id == citation.citation_id for item in loaded)
        assert all(item.caveat_id == caveat.caveat_id for item in loaded)
        assert all(
            item.geography.geography_vintage == geography.geography_vintage
            for item in loaded
        )


def test_source_vintages_stay_split() -> None:
    assert CARDS_1_3_SOURCE_VINTAGE == "2026-08"
    assert CARD_4_SOURCE_VINTAGE == "2013-2024-linked"
