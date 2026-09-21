"""C2 pipeline: derived tables → immutable vintage. Does not publish."""

from __future__ import annotations

import csv
import hashlib
import io
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from prism.catalog import slice_caveats, slice_citations, slice_geographies
from prism.ingest.census_srs_xlsx_pdf import (
    PARSER,
    parse_census_2011_a02_xls,
    parse_census_2011_pca_sd,
    parse_ncp_projections_table8,
    parse_srs_bulletin_2024,
    parse_srs_statistical_report_2024,
)
from prism.observation_parquet import observations_from_parquet
from prism.paths import (
    cas_path,
    citizen_pointer_path,
    ingest_lineage_path,
    ingest_table_path,
    preview_pointer_path,
    series_dir,
)
from prism.pipeline.census_srs_ncp import (
    MAPPER_VERSION,
    PipelineError,
    map_c2_table,
)
from prism.pipeline.run import materialise_vintage
from prism.refresh import (
    C2_SERIES,
    C2_SERIES_IDS,
    SERIES_CENSUS_2011_A02_DECADAL,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
    SERIES_SRS_BULLETIN_2024,
    SERIES_SRS_STATISTICAL_REPORT_2024,
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
from tests.c2_ingest_fixtures import (
    a02_workbook_bytes,
    bulletin_table1_pdf_bytes,
    pca_workbook_bytes,
    table3_fertility_pdf_bytes,
    table8_projection_pdf_bytes,
)
from tests.factories import CREATED_AT
from tests.test_pipeline_c1 import _seed_c1

C2_CAVEATS = slice_caveats("c2")
C2_CITATIONS = slice_citations("c2")
C2_GEOGRAPHIES = slice_geographies("c2")

LATER = datetime(2026, 9, 19, 12, 0, tzinfo=UTC)


def _csv(series_id: str) -> str:
    if series_id == SERIES_CENSUS_2011_PCA_SD:
        return parse_census_2011_pca_sd(pca_workbook_bytes()).csv_text
    if series_id == SERIES_CENSUS_2011_A02_DECADAL:
        return parse_census_2011_a02_xls(a02_workbook_bytes()).csv_text
    if series_id == SERIES_SRS_BULLETIN_2024:
        return parse_srs_bulletin_2024(bulletin_table1_pdf_bytes()).csv_text
    if series_id == SERIES_SRS_STATISTICAL_REPORT_2024:
        return parse_srs_statistical_report_2024(table3_fertility_pdf_bytes()).csv_text
    return parse_ncp_projections_table8(table8_projection_pdf_bytes()).csv_text


def _seed_c2(data_root: Path, *, lineage_ok: YesNo = YesNo.yes) -> None:
    for binding in C2_SERIES:
        table = ingest_table_path(
            data_root, binding.producer_slug, binding.series_id, binding.source_vintage
        )
        table.parent.mkdir(parents=True, exist_ok=True)
        table.write_text(_csv(binding.series_id), encoding="utf-8", newline="\n")
        lineage_path = ingest_lineage_path(
            data_root, binding.producer_slug, binding.series_id, binding.source_vintage
        )
        lineage_path.parent.mkdir(parents=True, exist_ok=True)
        record = LineageRecord(
            raw_path=(
                f"data/raw/{binding.producer_slug}/{binding.series_id}/"
                f"{binding.source_vintage}/20260919T080000Z/artifact"
            ),
            derived_path=(
                f"data/derived/{binding.producer_slug}/{binding.series_id}/"
                f"{binding.source_vintage}/table.csv"
            ),
            checksum="c" * 64,
            retrieved_at="20260919T080000Z",
            parser=PARSER,
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
        raw_path="data/raw/orgi/census-2011-pca-sd/2011/20260919T080000Z/pca.xlsx",
        derived_path="data/derived/orgi/census-2011-pca-sd/2011/table.csv",
        checksum="a" * 64,
    )


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def test_locked_ids_match_bindings() -> None:
    assert set(C2_CITATIONS) == set(C2_SERIES_IDS)
    assert set(C2_CAVEATS) == set(C2_SERIES_IDS)
    assert set(C2_GEOGRAPHIES) == set(C2_SERIES_IDS)
    for binding in C2_SERIES:
        assert C2_CITATIONS[binding.series_id].citation_id == binding.citation_id
        assert C2_CAVEATS[binding.series_id].caveat_id == binding.caveat_id
        geography = C2_GEOGRAPHIES[binding.series_id]
        assert geography.frame_id == binding.geography_frame_id
        assert geography.geography_vintage == binding.geography_vintage


def test_pca_india_is_2011_census_day_not_current() -> None:
    observations = map_c2_table(
        series_id=SERIES_CENSUS_2011_PCA_SD,
        rows=_rows(_csv(SERIES_CENSUS_2011_PCA_SD)),
        citation_id=C2_CITATIONS[SERIES_CENSUS_2011_PCA_SD].citation_id,
        caveat_id=C2_CAVEATS[SERIES_CENSUS_2011_PCA_SD].caveat_id,
        geography=C2_GEOGRAPHIES[SERIES_CENSUS_2011_PCA_SD],
        lineage=_lineage(),
    )
    india_total = [
        item
        for item in observations
        if item.geography.code == "00"
        and item.sector == "Total"
        and item.observation_id.endswith("-tot-p")
    ]
    assert len(india_total) == 1
    assert india_total[0].value == 100
    assert india_total[0].reference_period == "2011-03-01"
    assert india_total[0].unit == "persons"
    assert {item.unit for item in observations if item.geography.code == "00"} == {
        "persons",
        "males",
        "females",
        "households",
    }
    assert india_total[0].geography.code_system is CodeSystem.census
    assert india_total[0].geography.geography_vintage == "2011"


def test_a02_blank_variation_is_unknown_not_zero() -> None:
    observations = map_c2_table(
        series_id=SERIES_CENSUS_2011_A02_DECADAL,
        rows=_rows(_csv(SERIES_CENSUS_2011_A02_DECADAL)),
        citation_id=C2_CITATIONS[SERIES_CENSUS_2011_A02_DECADAL].citation_id,
        caveat_id=C2_CAVEATS[SERIES_CENSUS_2011_A02_DECADAL].caveat_id,
        geography=C2_GEOGRAPHIES[SERIES_CENSUS_2011_A02_DECADAL],
        lineage=_lineage(),
    )
    blank = [
        item
        for item in observations
        if item.geography.code == "00"
        and item.reference_period == "1901 $"
        and item.observation_id.endswith("-variation-absolute")
    ]
    assert len(blank) == 1
    assert blank[0].value is None
    assert blank[0].status is ObservationStatus.unknown


def test_table8_keeps_thousands_and_projection_unit() -> None:
    observations = map_c2_table(
        series_id=SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
        rows=_rows(_csv(SERIES_NCP_PROJECTIONS_2011_2036_TABLE8)),
        citation_id=C2_CITATIONS[SERIES_NCP_PROJECTIONS_2011_2036_TABLE8].citation_id,
        caveat_id=C2_CAVEATS[SERIES_NCP_PROJECTIONS_2011_2036_TABLE8].caveat_id,
        geography=C2_GEOGRAPHIES[SERIES_NCP_PROJECTIONS_2011_2036_TABLE8],
        lineage=_lineage(),
    )
    india_2011 = [
        item
        for item in observations
        if item.geography.code == "india"
        and item.reference_period == "2011"
        and item.sector == "Persons"
    ]
    assert len(india_2011) == 1
    assert india_2011[0].value == 1210855
    assert "projected" in india_2011[0].unit
    assert india_2011[0].geography.code_system is CodeSystem.none


def test_lineage_ok_no_does_not_write_vintage(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c2(data_root, lineage_ok=YesNo.no)
    with pytest.raises(PipelineError, match="lineage_ok"):
        materialise_vintage(data_root, logs_root, slice_id="c2", created_at=CREATED_AT)
    assert not (data_root / "vintages").exists() or not any(
        (data_root / "vintages").iterdir()
    )


def test_first_vintage_lists_five_series_and_leaves_pointers(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c2(data_root)
    manifest, report = materialise_vintage(
        data_root, logs_root, slice_id="c2", created_at=CREATED_AT
    )
    assert manifest.completeness is Completeness.complete
    assert manifest.trigger is RefreshTrigger.source_change
    assert [entry.series_id for entry in manifest.series] == list(C2_SERIES_IDS)
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
        assert os.path.samefile(parquet, cas_path(data_root, digest))


def test_c2_vintage_does_not_list_c1_series(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c1(data_root)
    _seed_c2(data_root)
    c1, _ = materialise_vintage(
        data_root, logs_root, slice_id="c1", created_at=CREATED_AT
    )
    c2, _ = materialise_vintage(data_root, logs_root, slice_id="c2", created_at=LATER)
    assert {entry.series_id for entry in c1.series}.isdisjoint(C2_SERIES_IDS)
    assert {entry.series_id for entry in c2.series} == set(C2_SERIES_IDS)
    observations = observations_from_parquet(
        (
            series_dir(data_root, c2.vintage_id, SERIES_CENSUS_2011_PCA_SD)
            / "observations.parquet"
        ).read_bytes()
    )
    assert all(item.series_id == SERIES_CENSUS_2011_PCA_SD for item in observations)
