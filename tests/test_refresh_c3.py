"""C3 refresh bindings: eleven series, Card 8 named hole, not mixed with C1/C2."""

from __future__ import annotations

from pathlib import Path

import pytest

from prism.observation_parquet import observations_from_parquet, observations_to_parquet
from prism.paths import OBSERVATIONS_FILENAME, series_dir
from prism.refresh import (
    C1_SERIES_IDS,
    C2_SERIES_IDS,
    C3_BUDGET_SOURCE_VINTAGE,
    C3_CGA_FA_SOURCE_VINTAGE,
    C3_FRAME_A_ID,
    C3_FRAME_C_ID,
    C3_GEOGRAPHY_VINTAGE_2024,
    C3_GEOGRAPHY_VINTAGE_2026,
    C3_LINEAGE_REQUIRED_SERIES_IDS,
    C3_NAMED_HOLE_SERIES_IDS,
    C3_SERIES,
    C3_SERIES_BY_ID,
    C3_SERIES_IDS,
    CAVEAT_C3_CARD_8,
    CITE_C3_CARD_1,
    CITE_C3_CARD_8,
    PRODUCER_SLUG_CGA,
    PRODUCER_SLUG_MOF_BUDGET,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
    SeriesBinding,
    lineage_blocks_completeness,
    lineage_record_blocks_completeness,
    scheduled_series_on,
)
from prism.schema import (
    CodeSystem,
    Completeness,
    LineageRecord,
    Observation,
    ObservationLineage,
    ObservationStatus,
    RefreshTrigger,
    ServedObservation,
    SourceChanged,
    YesNo,
)
from prism.vintage_store import SeriesWrite, VintageStoreError, write_vintage
from tests.factories import (
    CREATED_AT,
    make_caveat,
    make_citation,
    make_geography,
    make_geography_ref,
    make_observation,
    make_series_write,
)


def _c3_write(
    binding: SeriesBinding,
    *,
    lineage_ok: YesNo = YesNo.yes,
    observations_parquet: bytes | None = None,
) -> SeriesWrite:
    payload = (
        observations_parquet
        if observations_parquet is not None
        else f"PARQUET-{binding.series_id}".encode()
    )
    return make_series_write(
        binding.series_id,
        payload,
        source_vintage=binding.source_vintage,
        geography_frame_id=binding.geography_frame_id,
        geography_vintage=binding.geography_vintage,
        caveat_id=binding.caveat_id,
        producer=binding.producer,
        lineage_ok=lineage_ok,
        citation=make_citation(
            citation_id=binding.citation_id,
            next_release="unknown",
            release_date="unknown",
        ),
        caveat=make_caveat(caveat_id=binding.caveat_id),
        geography=make_geography(
            frame_id=binding.geography_frame_id,
            frame="Union",
            geography_vintage=binding.geography_vintage,
            units_included=(
                {
                    "code": "union",
                    "name_en": "Government of India",
                    "geography_vintage": binding.geography_vintage,
                },
            ),
        ),
    )


def _frbm_hole_observation() -> Observation:
    return make_observation(
        observation_id="obs-c3-frbm-statements-union-2026-27-unknown",
        series_id=SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
        citation_id=CITE_C3_CARD_8,
        caveat_id=CAVEAT_C3_CARD_8,
        geography=make_geography_ref(
            code="union",
            geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
            code_system=CodeSystem.none,
        ),
        sector="Union",
        reference_period="2026-27",
        value=None,
        unit="not a table",
        status=ObservationStatus.unknown,
        lineage=ObservationLineage(
            raw_path=(
                "data/raw/mof-budget/budget-2026-27-frbm-statements/"
                "2026-27/20260918T080000Z/frbm1.pdf"
            ),
            derived_path=(
                "data/derived/mof-budget/budget-2026-27-frbm-statements/"
                "2026-27/table.csv"
            ),
            checksum="d" * 64,
        ),
    )


def _lineage(citation_id: str, lineage_ok: YesNo) -> LineageRecord:
    return LineageRecord(
        raw_path="data/raw/mof-budget/budget-2026-27-tax-revenue/2026-27/20260918T080000Z/artifact",
        derived_path="data/derived/mof-budget/budget-2026-27-tax-revenue/2026-27/table.csv",
        checksum="c" * 64,
        retrieved_at="20260918T080000Z",
        parser="union-c3-1.0.0",
        citation_id=citation_id,
        row_count=0,
        nulls="not parsed",
        source_changed=SourceChanged.first_retrieve,
        lineage_ok=lineage_ok,
        flags="named hole" if citation_id == CITE_C3_CARD_8 else "none",
    )


def test_c3_series_ids_are_eleven_cards_and_disjoint_from_c1_c2() -> None:
    assert C3_SERIES_IDS == (
        "budget-2026-27-tax-revenue",
        "budget-2026-27-non-tax-revenue",
        "budget-2026-27-capital-receipts",
        "budget-2026-27-annex1-trends-receipts",
        "budget-2026-27-expenditure-stat1",
        "budget-2026-27-deficit-statistics",
        "budget-2026-27-liabilities",
        "budget-2026-27-frbm-statements",
        "budget-2026-27-afs",
        "cga-monthly-glance-2026-07",
        "cga-finance-accounts-2024-25-stat1",
    )
    assert set(C3_SERIES_IDS).isdisjoint(C1_SERIES_IDS)
    assert set(C3_SERIES_IDS).isdisjoint(C2_SERIES_IDS)
    assert len(C3_SERIES) == 11
    assert all(binding.next_release == "unknown" for binding in C3_SERIES)
    assert C3_NAMED_HOLE_SERIES_IDS == (SERIES_BUDGET_2026_27_FRBM_STATEMENTS,)
    assert SERIES_BUDGET_2026_27_FRBM_STATEMENTS not in C3_LINEAGE_REQUIRED_SERIES_IDS
    assert len(C3_LINEAGE_REQUIRED_SERIES_IDS) == 10


def test_c3_is_not_on_the_c1_october_schedule() -> None:
    from datetime import date

    from prism.refresh import CARDS_1_3_NEXT_RELEASE

    scheduled = scheduled_series_on(CARDS_1_3_NEXT_RELEASE)
    assert all(binding.series_id not in C3_SERIES_IDS for binding in scheduled)
    assert scheduled_series_on(date(2026, 2, 1)) == ()


def test_c3_bindings_lock_producer_slug_and_geography_vintage() -> None:
    tax = C3_SERIES_BY_ID[SERIES_BUDGET_2026_27_TAX_REVENUE]
    assert tax.producer_slug == PRODUCER_SLUG_MOF_BUDGET
    assert tax.geography_frame_id == C3_FRAME_A_ID
    assert tax.geography_vintage == C3_GEOGRAPHY_VINTAGE_2026
    assert tax.source_vintage == C3_BUDGET_SOURCE_VINTAGE
    fa = C3_SERIES_BY_ID[SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1]
    assert fa.producer_slug == PRODUCER_SLUG_CGA
    assert fa.geography_frame_id == C3_FRAME_C_ID
    assert fa.geography_vintage == C3_GEOGRAPHY_VINTAGE_2024
    assert fa.source_vintage == C3_CGA_FA_SOURCE_VINTAGE


def test_card_8_lineage_ok_no_does_not_block_completeness() -> None:
    assert (
        lineage_blocks_completeness(SERIES_BUDGET_2026_27_FRBM_STATEMENTS, YesNo.no)
        is False
    )
    assert (
        lineage_blocks_completeness(SERIES_BUDGET_2026_27_TAX_REVENUE, YesNo.no) is True
    )
    assert (
        lineage_blocks_completeness(SERIES_BUDGET_2026_27_TAX_REVENUE, YesNo.yes)
        is False
    )
    assert (
        lineage_record_blocks_completeness(_lineage(CITE_C3_CARD_8, YesNo.no)) is False
    )
    assert (
        lineage_record_blocks_completeness(_lineage(CITE_C3_CARD_1, YesNo.no)) is True
    )


def test_complete_c3_vintage_lists_all_eleven_series(tmp_path: Path) -> None:
    writes = tuple(_c3_write(binding) for binding in C3_SERIES)
    manifest = write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=writes,
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=C3_SERIES_IDS,
    )
    assert [entry.series_id for entry in manifest.series] == list(C3_SERIES_IDS)
    assert all(entry.reused.value == "no" for entry in manifest.series)


def test_complete_c3_vintage_allows_card_8_named_hole(tmp_path: Path) -> None:
    hole = _frbm_hole_observation()
    writes = []
    for binding in C3_SERIES:
        if binding.series_id == SERIES_BUDGET_2026_27_FRBM_STATEMENTS:
            writes.append(
                _c3_write(
                    binding,
                    lineage_ok=YesNo.no,
                    observations_parquet=observations_to_parquet((hole,)),
                )
            )
            continue
        writes.append(_c3_write(binding))
    manifest = write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=tuple(writes),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=C3_SERIES_IDS,
    )
    assert manifest.completeness is Completeness.complete
    by_id = {entry.series_id: entry for entry in manifest.series}
    assert list(by_id) == list(C3_SERIES_IDS)
    assert by_id[SERIES_BUDGET_2026_27_FRBM_STATEMENTS].lineage_ok is YesNo.no
    assert all(
        by_id[series_id].lineage_ok is YesNo.yes
        for series_id in C3_LINEAGE_REQUIRED_SERIES_IDS
    )
    stored = observations_from_parquet(
        (
            series_dir(
                tmp_path, manifest.vintage_id, SERIES_BUDGET_2026_27_FRBM_STATEMENTS
            )
            / OBSERVATIONS_FILENAME
        ).read_bytes()
    )
    assert stored == (hole,)
    served = ServedObservation(
        observation=hole,
        citation=make_citation(
            citation_id=CITE_C3_CARD_8,
            next_release="unknown",
            release_date="unknown",
        ),
        caveat=make_caveat(caveat_id=CAVEAT_C3_CARD_8),
    )
    assert served.observation.status is ObservationStatus.unknown
    assert served.observation.value is None


def test_complete_c3_vintage_cannot_omit_card_8(tmp_path: Path) -> None:
    writes = tuple(
        _c3_write(binding)
        for binding in C3_SERIES
        if binding.series_id != SERIES_BUDGET_2026_27_FRBM_STATEMENTS
    )
    with pytest.raises(VintageStoreError, match="missing required series"):
        write_vintage(
            tmp_path,
            created_at=CREATED_AT,
            trigger=RefreshTrigger.on_demand,
            series=writes,
            completeness=Completeness.complete,
            previous=None,
            required_series_ids=C3_SERIES_IDS,
        )


def test_complete_c3_vintage_requires_h1_lineage_ok(tmp_path: Path) -> None:
    writes = []
    for binding in C3_SERIES:
        if binding.series_id == SERIES_BUDGET_2026_27_TAX_REVENUE:
            writes.append(_c3_write(binding, lineage_ok=YesNo.no))
            continue
        if binding.series_id == SERIES_BUDGET_2026_27_FRBM_STATEMENTS:
            writes.append(_c3_write(binding, lineage_ok=YesNo.no))
            continue
        writes.append(_c3_write(binding))
    with pytest.raises(VintageStoreError, match="lineage_ok"):
        write_vintage(
            tmp_path,
            created_at=CREATED_AT,
            trigger=RefreshTrigger.on_demand,
            series=tuple(writes),
            completeness=Completeness.complete,
            previous=None,
            required_series_ids=C3_SERIES_IDS,
        )
