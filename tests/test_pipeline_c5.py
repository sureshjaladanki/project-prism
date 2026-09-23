"""C5 pipeline mapper: geography × Accounts/RE/BE columns."""

from __future__ import annotations

from prism.catalog import default_catalog
from prism.pipeline.state_finance import map_state_finance_rows
from prism.schema import ObservationLineage, ObservationStatus


def test_state_finance_mapper_emits_three_periods() -> None:
    catalog = default_catalog()
    series_id = "rbi-sf-2025-26-deficit-indicators"
    entry = catalog.series(series_id)
    geography = catalog.geographies[series_id]
    rows = [
        {
            "geography": "Andhra Pradesh",
            "line_label": "Gross Fiscal Deficit",
            "accounts_2023_24": "1000",
            "re_2024_25": "1100",
            "be_2025_26": "",
        }
    ]
    lineage = ObservationLineage(
        raw_path="data/raw/example.xlsx",
        derived_path="data/derived/example.csv",
        checksum="abc",
    )
    observations = map_state_finance_rows(
        rows,
        series_id,
        entry.citation_id,
        entry.caveat_id,
        geography,
        lineage,
    )
    assert len(observations) == 3
    by_period = {obs.reference_period: obs for obs in observations}
    assert by_period["accounts-2023-24"].value == 1000.0
    assert by_period["re-2024-25"].value == 1100.0
    assert by_period["be-2025-26"].status is ObservationStatus.unknown
    assert by_period["accounts-2023-24"].geography.code == "andhra-pradesh"
