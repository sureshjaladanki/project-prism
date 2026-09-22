"""Typed fixtures for contract tests. Not a second schema."""

from __future__ import annotations

from datetime import UTC, date, datetime

from prism.refresh import (
    C1_FRAME_A_ID,
    C1_GEOGRAPHY_VINTAGE,
    C1_LICENCE,
    CAVEAT_C1_CARD_1,
    CITE_C1_CARD_1,
    MOSPI_NSO_PSD,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import (
    CaveatNote,
    Citation,
    CodeSystem,
    GeographyRef,
    GeographyUnit,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
    SlotSelector,
    YesNo,
)
from prism.vintage_store import SeriesWrite

CREATED_AT = datetime(2026, 9, 16, 8, 0, tzinfo=UTC)


def make_citation(**overrides: object) -> Citation:
    payload: dict[str, object] = {
        "citation_id": CITE_C1_CARD_1,
        "producer": MOSPI_NSO_PSD,
        "series": "Consumer Price Index (CPI) General — Rural, Urban and Combined (Base 2024=100)",
        "id": "MoSPI product_id 9; Documents id 315",
        "reference_period": "2026-08",
        "release_date": date(2026, 9, 14),
        "url": "https://www.mospi.gov.in/uploads/documents/productChartTable/1789491098345-Data_August_CPI_2026_14092026.xlsx",
        "geography_as_published": "All India and States/UTs as labelled in State Name",
        "frequency": "monthly",
        "licence": C1_LICENCE,
        "next_release": date(2026, 10, 12),
        "caveat_one_line": "Latest month is Provisional; Combined is a published sector, not a user merge.",
    }
    payload.update(overrides)
    return Citation.model_validate(payload)


def make_caveat(**overrides: object) -> CaveatNote:
    payload: dict[str, object] = {
        "caveat_id": CAVEAT_C1_CARD_1,
        "concept": "CPI General Base 2024=100",
        "unit": "Index points (Base 2024=100)",
        "population": "NSO price collection covering States/UTs; not districts",
        "reference_period": "calendar month on the row",
        "producer_definition": "All India CPI General Base 2024=100 as published",
        "comparable_from": "January 2025",
        "breaks": "Base-year break versus 2012=100",
        "lags": "August 2026 Provisional released 14 September 2026",
        "disagrees_with": "CPI Base 2012=100; WPI; Labour Bureau CPIs",
        "do_not": "Do not stitch 2012=100; do not chart blank inflation as zero",
        "citizen_note": "CPI General is the headline retail price index, Base 2024=100.",
    }
    payload.update(overrides)
    return CaveatNote.model_validate(payload)


def make_geography(**overrides: object) -> GeographyVintage:
    payload: dict[str, object] = {
        "frame_id": C1_FRAME_A_ID,
        "geography_vintage": C1_GEOGRAPHY_VINTAGE,
        "code_system": CodeSystem.producer_specific,
        "frame": "Union | state | UT",
        "units_included": (
            GeographyUnit(
                code="00",
                name_en="All India",
                geography_vintage=C1_GEOGRAPHY_VINTAGE,
            ),
        ),
        "units_missing": ("districts and below (parked)",),
        "breaks": "Base 2024=100 map is post-reorganisation",
        "crosswalk": "none",
    }
    payload.update(overrides)
    return GeographyVintage.model_validate(payload)


def make_geography_ref(**overrides: object) -> GeographyRef:
    payload: dict[str, object] = {
        "code": "00",
        "geography_vintage": C1_GEOGRAPHY_VINTAGE,
        "code_system": CodeSystem.producer_specific,
    }
    payload.update(overrides)
    return GeographyRef.model_validate(payload)


def make_observation(**overrides: object) -> Observation:
    from prism.citizen_projection import denomination_from_unit

    payload: dict[str, object] = {
        "observation_id": "obs-c1-general-00-combined-2026-08-index",
        "series_id": SERIES_CPI_GENERAL_BASE_2024,
        "citation_id": CITE_C1_CARD_1,
        "caveat_id": CAVEAT_C1_CARD_1,
        "geography": make_geography_ref(),
        "sector": "Combined",
        "reference_period": "2026-08",
        "value": 104.82,
        "unit": "index (Base 2024=100)",
        "status": ObservationStatus.value,
        "lineage": ObservationLineage(
            raw_path="data/raw/mospi/cpi-general-base-2024/2026-08/20260916T080000Z/artifact",
            derived_path="data/derived/mospi/cpi-general-base-2024/2026-08/table.csv",
            checksum="a" * 64,
        ),
    }
    payload.update(overrides)
    if "denomination" not in payload:
        unit = str(payload["unit"])
        payload["denomination"] = denomination_from_unit(unit)
    return Observation.model_validate(payload)


def make_selector(**overrides: object) -> SlotSelector:
    payload: dict[str, object] = {
        "series_id": SERIES_CPI_GENERAL_BASE_2024,
        "geography_code": "00",
        "geography_vintage": C1_GEOGRAPHY_VINTAGE,
        "code_system": CodeSystem.producer_specific,
        "sector": "Combined",
        "reference_period": "2026-08",
        "unit": "index (Base 2024=100)",
        "status": ObservationStatus.value,
    }
    payload.update(overrides)
    return SlotSelector.model_validate(payload)


def make_series_write(
    series_id: str, observations_parquet: bytes, **overrides: object
) -> SeriesWrite:
    citation = make_citation()
    caveat = make_caveat()
    geography = make_geography()
    payload: dict[str, object] = {
        "producer": MOSPI_NSO_PSD,
        "series_id": series_id,
        "source_vintage": "2026-08",
        "raw_checksum": "b" * 64,
        "parser_version": "c1-unwritten",
        "lineage_ok": YesNo.yes,
        "geography_vintage": C1_GEOGRAPHY_VINTAGE,
        "geography_frame_id": C1_FRAME_A_ID,
        "caveat_id": caveat.caveat_id,
        "mapper_version": "c1-unwritten",
        "observations_parquet": observations_parquet,
        "citation": citation,
        "caveat": caveat,
        "geography": geography,
    }
    payload.update(overrides)
    return SeriesWrite(**payload)  # type: ignore[arg-type]
