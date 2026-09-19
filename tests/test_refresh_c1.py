"""C1 refresh triggers and lineage signal."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from prism.paths import PRODUCER_SLUG_MOSPI
from prism.refresh import (
    C1_FRAME_A_ID,
    C1_GEOGRAPHY_VINTAGE,
    C1_SERIES,
    C1_SERIES_BY_ID,
    C1_SERIES_IDS,
    CARD_4_SOURCE_VINTAGE,
    CARDS_1_3_NEXT_RELEASE,
    CARDS_1_3_SOURCE_VINTAGE,
    MOSPI_NSO_PSD,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
    SeriesBinding,
    trigger_from_lineage,
)
from prism.schema import (
    Completeness,
    LineageRecord,
    RefreshTrigger,
    SourceChanged,
    YesNo,
)
from prism.vintage_store import write_vintage
from tests.factories import (
    CREATED_AT,
    make_caveat,
    make_citation,
    make_geography,
    make_series_write,
)


def _lineage(source_changed: SourceChanged) -> LineageRecord:
    citation = make_citation()
    return LineageRecord(
        raw_path="data/raw/mospi/cpi-general-base-2024/2026-08/20260916T080000Z/artifact",
        derived_path="data/derived/mospi/cpi-general-base-2024/2026-08/table.csv",
        checksum="c" * 64,
        retrieved_at="20260916T080000Z",
        parser="c1-unwritten",
        citation_id=citation.citation_id,
        row_count=0,
        nulls="none yet",
        source_changed=source_changed,
        lineage_ok=YesNo.yes,
        flags="none",
    )


def test_source_changed_yes_and_first_retrieve_are_source_change() -> None:
    assert trigger_from_lineage(_lineage(SourceChanged.yes)) is RefreshTrigger.source_change
    assert trigger_from_lineage(_lineage(SourceChanged.first_retrieve)) is RefreshTrigger.source_change
    assert trigger_from_lineage(_lineage(SourceChanged.no)) is None


def test_c1_bindings_lock_producer_slug_and_geography_vintage() -> None:
    general = C1_SERIES_BY_ID[SERIES_CPI_GENERAL_BASE_2024]
    assert isinstance(general, SeriesBinding)
    assert general.producer == MOSPI_NSO_PSD
    assert general.producer_slug == PRODUCER_SLUG_MOSPI
    assert general.geography_frame_id == C1_FRAME_A_ID
    assert general.geography_vintage == C1_GEOGRAPHY_VINTAGE
    back = C1_SERIES_BY_ID[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024]
    assert back.producer_slug == PRODUCER_SLUG_MOSPI
    assert back.geography_vintage == C1_GEOGRAPHY_VINTAGE
    assert all(isinstance(binding, SeriesBinding) for binding in C1_SERIES)


def test_card_4_is_not_on_the_october_schedule() -> None:
    assert CARDS_1_3_NEXT_RELEASE == date(2026, 10, 12)
    assert CARDS_1_3_SOURCE_VINTAGE == "2026-08"
    assert CARD_4_SOURCE_VINTAGE == "2013-2024-linked"
    assert C1_SERIES_BY_ID[SERIES_CPI_BACK_SERIES_LINKED_BASE_2024].next_release == "unknown"


def test_complete_c1_vintage_lists_all_four_series(tmp_path: Path) -> None:
    writes = []
    for binding in C1_SERIES:
        release_date: date | str = "unknown" if binding.card == 4 else date(2026, 9, 14)
        writes.append(
            make_series_write(
                binding.series_id,
                f"PARQUET-{binding.series_id}".encode(),
                source_vintage=binding.source_vintage,
                geography_frame_id=binding.geography_frame_id,
                caveat_id=binding.caveat_id,
                citation=make_citation(
                    citation_id=binding.citation_id,
                    next_release=binding.next_release,
                    release_date=release_date,
                ),
                caveat=make_caveat(caveat_id=binding.caveat_id),
                geography=make_geography(
                    frame_id=binding.geography_frame_id,
                    frame="Union" if binding.card == 4 else "Union | state | UT",
                ),
            )
        )
    manifest = write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=tuple(writes),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=C1_SERIES_IDS,
    )
    assert [entry.series_id for entry in manifest.series] == list(C1_SERIES_IDS)
    assert all(entry.reused.value == "no" for entry in manifest.series)
