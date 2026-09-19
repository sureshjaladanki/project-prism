"""C2 refresh bindings: five series, no calendar, not mixed with C1."""

from __future__ import annotations

from pathlib import Path

from prism.refresh import (
    C1_SERIES_IDS,
    C2_CARD_5_SOURCE_VINTAGE,
    C2_FRAME_A_ID,
    C2_FRAME_E_ID,
    C2_GEOGRAPHY_VINTAGE_2011,
    C2_GEOGRAPHY_VINTAGE_2019,
    C2_SERIES,
    C2_SERIES_BY_ID,
    C2_SERIES_IDS,
    PRODUCER_SLUG_NCP_MOHFW,
    PRODUCER_SLUG_ORGI,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
    scheduled_series_on,
)
from prism.schema import Completeness, RefreshTrigger
from prism.vintage_store import write_vintage
from tests.factories import (
    CREATED_AT,
    make_caveat,
    make_citation,
    make_geography,
    make_series_write,
)


def test_c2_series_ids_are_five_cards_and_disjoint_from_c1() -> None:
    assert C2_SERIES_IDS == (
        "census-2011-pca-sd",
        "census-2011-a02-decadal",
        "srs-bulletin-2024",
        "srs-statistical-report-2024",
        "ncp-projections-2011-2036-table8",
    )
    assert set(C2_SERIES_IDS).isdisjoint(C1_SERIES_IDS)
    assert len(C2_SERIES) == 5
    assert all(binding.next_release == "unknown" for binding in C2_SERIES)


def test_c2_is_not_on_the_c1_october_schedule() -> None:
    from datetime import date

    from prism.refresh import CARDS_1_3_NEXT_RELEASE

    scheduled = scheduled_series_on(CARDS_1_3_NEXT_RELEASE)
    assert all(binding.series_id not in C2_SERIES_IDS for binding in scheduled)
    assert scheduled_series_on(date(2011, 3, 1)) == ()


def test_c2_bindings_lock_producer_slug_and_geography_vintage() -> None:
    pca = C2_SERIES_BY_ID[SERIES_CENSUS_2011_PCA_SD]
    assert pca.producer_slug == PRODUCER_SLUG_ORGI
    assert pca.geography_frame_id == C2_FRAME_A_ID
    assert pca.geography_vintage == C2_GEOGRAPHY_VINTAGE_2011
    assert pca.source_vintage == "2011"
    table8 = C2_SERIES_BY_ID[SERIES_NCP_PROJECTIONS_2011_2036_TABLE8]
    assert table8.producer_slug == PRODUCER_SLUG_NCP_MOHFW
    assert table8.geography_frame_id == C2_FRAME_E_ID
    assert table8.geography_vintage == C2_GEOGRAPHY_VINTAGE_2019
    assert table8.source_vintage == C2_CARD_5_SOURCE_VINTAGE


def test_complete_c2_vintage_lists_all_five_series(tmp_path: Path) -> None:
    writes = []
    for binding in C2_SERIES:
        writes.append(
            make_series_write(
                binding.series_id,
                f"PARQUET-{binding.series_id}".encode(),
                source_vintage=binding.source_vintage,
                geography_frame_id=binding.geography_frame_id,
                geography_vintage=binding.geography_vintage,
                caveat_id=binding.caveat_id,
                producer=binding.producer,
                citation=make_citation(
                    citation_id=binding.citation_id,
                    next_release="unknown",
                    release_date="unknown",
                ),
                caveat=make_caveat(caveat_id=binding.caveat_id),
                geography=make_geography(
                    frame_id=binding.geography_frame_id,
                    frame="Union | state | UT",
                    geography_vintage=binding.geography_vintage,
                    units_included=(
                        {
                            "code": "00",
                            "name_en": "India",
                            "geography_vintage": binding.geography_vintage,
                        },
                    ),
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
        required_series_ids=C2_SERIES_IDS,
    )
    assert [entry.series_id for entry in manifest.series] == list(C2_SERIES_IDS)
    assert all(entry.reused.value == "no" for entry in manifest.series)
