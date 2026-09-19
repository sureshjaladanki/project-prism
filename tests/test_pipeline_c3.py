"""C3 pipeline: derived tables → immutable vintage. Card 8 stays a named hole."""

from __future__ import annotations

import csv
import hashlib
import io
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from prism.ingest.parse_c3 import (
    AFS_COLUMNS,
    ANNEX1_COLUMNS,
    FA_COLUMNS,
    LIABILITIES_COLUMNS,
    PARSER,
    parse_cga_monthly_html,
    parse_deficit_statistics_xlsx,
    parse_expenditure_stat1_xlsx,
    parse_receipt_xlsx,
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
from prism.pipeline.c1 import materialise_c1_vintage
from prism.pipeline.c3 import (
    MAPPER_VERSION,
    PipelineError,
    map_c3_table,
    materialise_c3_vintage,
)
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
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
    SERIES_BUDGET_2026_27_LIABILITIES,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
    SERIES_CGA_MONTHLY_GLANCE_2026_07,
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
from tests.c3_ingest_fixtures import (
    cga_monthly_html_bytes,
    deficit_statistics_bytes,
    expenditure_stat1_bytes,
    receipt_workbook_bytes,
)
from tests.factories import CREATED_AT
from tests.test_pipeline_c1 import _seed_c1

LATER = datetime(2026, 9, 19, 10, 0, tzinfo=UTC)
AFTER_C1 = datetime(2026, 9, 20, 8, 0, tzinfo=UTC)

_PDF_SEED: dict[str, tuple[tuple[str, ...], str]] = {
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: (ANNEX1_COLUMNS, "Tax Revenue"),
    SERIES_BUDGET_2026_27_LIABILITIES: (LIABILITIES_COLUMNS, "Total Liabilities"),
    SERIES_BUDGET_2026_27_AFS: (AFS_COLUMNS, "Revenue Receipts"),
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: (FA_COLUMNS, "Revenue Receipts"),
}


def _one_row_csv(columns: tuple[str, ...], label: str) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerow(
        {name: label if name == "line_label" else "100" for name in columns}
    )
    return buffer.getvalue()


def _csv_for(series_id: str) -> str:
    if series_id in {
        SERIES_BUDGET_2026_27_TAX_REVENUE,
        SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
        SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
    }:
        return parse_receipt_xlsx(receipt_workbook_bytes()).csv_text
    if series_id == SERIES_BUDGET_2026_27_EXPENDITURE_STAT1:
        return parse_expenditure_stat1_xlsx(expenditure_stat1_bytes()).csv_text
    if series_id == SERIES_BUDGET_2026_27_DEFICIT_STATISTICS:
        return parse_deficit_statistics_xlsx(deficit_statistics_bytes()).csv_text
    if series_id == SERIES_CGA_MONTHLY_GLANCE_2026_07:
        return parse_cga_monthly_html(cga_monthly_html_bytes()).csv_text
    columns, label = _PDF_SEED[series_id]
    return _one_row_csv(columns, label)


def _seed_c3(
    data_root: Path,
    *,
    lineage_ok_by_id: dict[str, YesNo] | None = None,
) -> None:
    overrides = lineage_ok_by_id or {}
    for binding in C3_SERIES:
        lineage_ok = overrides.get(binding.series_id, YesNo.yes)
        if binding.series_id in NAMED_HOLE_SERIES_IDS:
            lineage_ok = overrides.get(binding.series_id, YesNo.no)
        table = ingest_table_path(
            data_root, binding.producer_slug, binding.series_id, binding.source_vintage
        )
        if binding.series_id not in NAMED_HOLE_SERIES_IDS:
            table.parent.mkdir(parents=True, exist_ok=True)
            table.write_text(_csv_for(binding.series_id), encoding="utf-8", newline="\n")
        lineage_path = ingest_lineage_path(
            data_root, binding.producer_slug, binding.series_id, binding.source_vintage
        )
        lineage_path.parent.mkdir(parents=True, exist_ok=True)
        derived = (
            f"data/derived/{binding.producer_slug}/{binding.series_id}/"
            f"{binding.source_vintage}/table.csv"
        )
        record = LineageRecord(
            raw_path=(
                f"data/raw/{binding.producer_slug}/{binding.series_id}/"
                f"{binding.source_vintage}/20260918T110000Z/artifact"
            ),
            derived_path=derived,
            checksum="c" * 64,
            retrieved_at="20260918T110000Z",
            parser=PARSER,
            citation_id=binding.citation_id,
            row_count=1,
            nulls="none",
            source_changed=SourceChanged.first_retrieve,
            lineage_ok=lineage_ok,
            flags=(
                "statutory FRBM prose, not a reconstructable grid"
                if binding.series_id in NAMED_HOLE_SERIES_IDS
                else "none"
            ),
        )
        lineage_path.write_text(record.model_dump_json(indent=2) + "\n", encoding="utf-8")


def _lineage() -> ObservationLineage:
    return ObservationLineage(
        raw_path="data/raw/mof-budget/budget-2026-27-tax-revenue/2026-27/20260918T110000Z/tr.xlsx",
        derived_path="data/derived/mof-budget/budget-2026-27-tax-revenue/2026-27/table.csv",
        checksum="a" * 64,
    )


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def test_locked_ids_match_bindings() -> None:
    assert set(C3_CITATIONS) == set(C3_SERIES_IDS)
    assert set(C3_CAVEATS) == set(C3_SERIES_IDS)
    assert set(C3_GEOGRAPHIES) == set(C3_SERIES_IDS)
    for binding in C3_SERIES:
        assert C3_CITATIONS[binding.series_id].citation_id == binding.citation_id
        assert C3_CAVEATS[binding.series_id].caveat_id == binding.caveat_id
        geography = C3_GEOGRAPHIES[binding.series_id]
        assert geography.frame_id == binding.geography_frame_id
        assert geography.geography_vintage == binding.geography_vintage
        assert geography.code_system is CodeSystem.none


def test_blank_budget_cell_is_unknown_not_zero() -> None:
    observations = map_c3_table(
        series_id=SERIES_BUDGET_2026_27_TAX_REVENUE,
        rows=_rows(_csv_for(SERIES_BUDGET_2026_27_TAX_REVENUE)),
        citation_id=C3_CITATIONS[SERIES_BUDGET_2026_27_TAX_REVENUE].citation_id,
        caveat_id=C3_CAVEATS[SERIES_BUDGET_2026_27_TAX_REVENUE].caveat_id,
        geography_code="government-of-india",
        geography_vintage="2026",
        code_system=CodeSystem.none,
        lineage=_lineage(),
    )
    blank = [
        item
        for item in observations
        if item.observation_id.endswith("-cgst") and item.reference_period == "budget-2025-2026"
    ]
    assert len(blank) == 1
    assert blank[0].value is None
    assert blank[0].status is ObservationStatus.unknown


def test_be_re_actuals_are_reference_periods_not_geography() -> None:
    observations = map_c3_table(
        series_id=SERIES_BUDGET_2026_27_TAX_REVENUE,
        rows=_rows(_csv_for(SERIES_BUDGET_2026_27_TAX_REVENUE)),
        citation_id=C3_CITATIONS[SERIES_BUDGET_2026_27_TAX_REVENUE].citation_id,
        caveat_id=C3_CAVEATS[SERIES_BUDGET_2026_27_TAX_REVENUE].caveat_id,
        geography_code="government-of-india",
        geography_vintage="2026",
        code_system=CodeSystem.none,
        lineage=_lineage(),
    )
    corporation = [item for item in observations if item.observation_id.endswith("-corporation-tax")]
    assert {item.geography.code for item in corporation} == {"government-of-india"}
    assert {item.sector for item in corporation} == {"Union"}
    assert {item.unit for item in corporation} == {"₹ crore; Corporation Tax"}
    assert {item.reference_period for item in corporation} == {
        "actuals-2024-2025",
        "budget-2025-2026",
        "revised-2025-2026",
        "budget-2026-2027",
    }


def test_empty_line_label_is_skipped() -> None:
    rows = [
        {"line_label": "", "actuals_2024_2025": "1", "budget_2025_2026": "2",
         "revised_2025_2026": "3", "budget_2026_2027": "4"},
        {"line_label": "Fiscal Deficit", "actuals_2024_2025": "(4.8%)",
         "budget_2025_2026": "5", "revised_2025_2026": "6", "budget_2026_2027": "7"},
    ]
    observations = map_c3_table(
        series_id=SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
        rows=rows,
        citation_id=C3_CITATIONS[SERIES_BUDGET_2026_27_DEFICIT_STATISTICS].citation_id,
        caveat_id=C3_CAVEATS[SERIES_BUDGET_2026_27_DEFICIT_STATISTICS].caveat_id,
        geography_code="government-of-india",
        geography_vintage="2026",
        code_system=CodeSystem.none,
        lineage=_lineage(),
    )
    assert all(item.observation_id.endswith("-fiscal-deficit") for item in observations)
    actuals = [item for item in observations if item.reference_period == "actuals-2024-2025"]
    assert actuals[0].value == 4.8


def test_pdf_replacement_minus_is_negative() -> None:
    rows = [
        {
            "line_label": "Refunds",
            "actuals_2024_2025": "\ufffd32482.83",
            "actuals_2023_2024": "\u22124850.43",
        }
    ]
    observations = map_c3_table(
        series_id=SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
        rows=rows,
        citation_id=C3_CITATIONS[SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1].citation_id,
        caveat_id=C3_CAVEATS[SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1].caveat_id,
        geography_code="union-government",
        geography_vintage="2024",
        code_system=CodeSystem.none,
        lineage=_lineage(),
    )
    by_period = {item.reference_period: item for item in observations}
    assert by_period["actuals-2024-2025"].value == -32482.83
    assert by_period["actuals-2023-2024"].value == -4850.43


def test_cga_percent_of_be_strips_percent_and_parens() -> None:
    observations = map_c3_table(
        series_id=SERIES_CGA_MONTHLY_GLANCE_2026_07,
        rows=_rows(_csv_for(SERIES_CGA_MONTHLY_GLANCE_2026_07)),
        citation_id=C3_CITATIONS[SERIES_CGA_MONTHLY_GLANCE_2026_07].citation_id,
        caveat_id=C3_CAVEATS[SERIES_CGA_MONTHLY_GLANCE_2026_07].caveat_id,
        geography_code="union-government",
        geography_vintage="2026",
        code_system=CodeSystem.none,
        lineage=_lineage(),
    )
    by_period = {item.reference_period: item for item in observations}
    assert by_period["pct-of-be-current"].value == 35.9
    assert by_period["pct-of-be-coppy"].value == 31.1
    assert by_period["pct-of-be-current"].unit == "% of BE; Revenue Receipts"
    assert by_period["pct-of-be-coppy"].unit == "% of BE (COPPY); Revenue Receipts"


def test_h1_lineage_ok_no_does_not_write_vintage(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c3(
        data_root,
        lineage_ok_by_id={SERIES_BUDGET_2026_27_TAX_REVENUE: YesNo.no},
    )
    with pytest.raises(PipelineError, match="lineage_ok"):
        materialise_c3_vintage(data_root, logs_root, created_at=CREATED_AT)
    assert not (data_root / "vintages").exists() or not any(
        (data_root / "vintages").iterdir()
    )


def test_first_vintage_lists_eleven_names_card_8_hole_and_leaves_pointers(
    tmp_path: Path,
) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c3(data_root)
    manifest, report = materialise_c3_vintage(data_root, logs_root, created_at=CREATED_AT)
    assert manifest.completeness is Completeness.complete
    assert manifest.trigger is RefreshTrigger.source_change
    assert [entry.series_id for entry in manifest.series] == list(C3_SERIES_IDS)
    assert all(entry.reused is YesNo.no for entry in manifest.series)
    assert all(entry.mapper_version == MAPPER_VERSION for entry in manifest.series)
    hole = next(
        entry for entry in manifest.series if entry.series_id == SERIES_BUDGET_2026_27_FRBM_STATEMENTS
    )
    assert hole.lineage_ok is YesNo.no
    parquet = (
        series_dir(data_root, manifest.vintage_id, SERIES_BUDGET_2026_27_FRBM_STATEMENTS)
        / "observations.parquet"
    )
    loaded = observations_from_parquet(parquet.read_bytes())
    assert len(loaded) == 1
    assert loaded[0].status is ObservationStatus.unknown
    assert loaded[0].value is None
    assert loaded[0].unit == "not a table"
    assert loaded[0].citation_id == C3_CITATIONS[SERIES_BUDGET_2026_27_FRBM_STATEMENTS].citation_id
    assert report["pointers"] == "untouched"
    assert not citizen_pointer_path(data_root).exists()
    assert not preview_pointer_path(data_root).exists()
    for entry in manifest.series:
        path = series_dir(data_root, manifest.vintage_id, entry.series_id) / "observations.parquet"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert os.path.samefile(path, cas_path(data_root, digest))


def test_second_vintage_hard_links_unchanged_series(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c3(data_root)
    first, _report_a = materialise_c3_vintage(data_root, logs_root, created_at=CREATED_AT)
    second, report_b = materialise_c3_vintage(data_root, logs_root, created_at=LATER)
    assert first.vintage_id != second.vintage_id
    assert all(entry.reused is YesNo.yes for entry in second.series)
    assert all(row["rewritten"] == "no" for row in report_b["series"])  # type: ignore[index]
    series_id = SERIES_BUDGET_2026_27_TAX_REVENUE
    path_a = series_dir(data_root, first.vintage_id, series_id) / "observations.parquet"
    path_b = series_dir(data_root, second.vintage_id, series_id) / "observations.parquet"
    digest = hashlib.sha256(path_a.read_bytes()).hexdigest()
    cas = cas_path(data_root, digest)
    assert os.path.samefile(path_a, cas)
    assert os.path.samefile(path_b, cas)
    assert os.stat(cas).st_nlink >= 3
    loaded = load_manifest(data_root, second.vintage_id)
    assert loaded.series[0].payload_checksum == first.series[0].payload_checksum


def test_c1_vintage_is_not_previous_for_c3_reuse(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c3(data_root)
    _seed_c1(data_root)
    first, _report_a = materialise_c3_vintage(data_root, logs_root, created_at=CREATED_AT)
    materialise_c1_vintage(data_root, logs_root, created_at=LATER)
    second, _report_b = materialise_c3_vintage(data_root, logs_root, created_at=AFTER_C1)
    assert first.vintage_id != second.vintage_id
    assert [entry.series_id for entry in second.series] == list(C3_SERIES_IDS)
    assert all(entry.reused is YesNo.yes for entry in second.series)


def test_payload_checksum_matches_cas_parts(tmp_path: Path) -> None:
    data_root = tmp_path / "data"
    logs_root = tmp_path / "logs"
    _seed_c3(data_root)
    manifest, _report = materialise_c3_vintage(data_root, logs_root, created_at=CREATED_AT)
    from prism.paths import CAVEAT_FILENAME, CITATION_FILENAME, GEOGRAPHY_FILENAME
    from prism.schema import CaveatNote, Citation, GeographyVintage

    for entry in manifest.series:
        folder = series_dir(data_root, manifest.vintage_id, entry.series_id)
        observations = folder / "observations.parquet"
        citation = Citation.model_validate_json((folder / CITATION_FILENAME).read_bytes())
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
            item.geography.geography_vintage == geography.geography_vintage for item in loaded
        )
        assert all(item.sector == "Union" for item in loaded)
