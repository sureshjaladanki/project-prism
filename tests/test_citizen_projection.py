"""C1: citizen projection types cannot carry desk fields."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prism.citizen_projection import (
    FORBIDDEN_PROJECTION_FIELD_NAMES,
    PROJECTION_TYPES,
)
from prism.schema import (
    NOT_PUBLISHED,
    CitizenCite,
    CitizenGeography,
    CitizenMethod,
    DisplayScale,
    DisplayValue,
    ObservationStatus,
)


def test_projection_types_omit_desk_fields() -> None:
    for model in PROJECTION_TYPES:
        names = set(model.model_fields)
        leak = names & FORBIDDEN_PROJECTION_FIELD_NAMES
        assert not leak, f"{model.__name__} carries desk fields {sorted(leak)}"


def test_projection_types_forbid_extra_desk_keys() -> None:
    payloads: dict[type, dict[str, object]] = {
        CitizenCite: {
            "producer": "NSO",
            "url": "https://www.mospi.gov.in/",
            "series": "CPI General",
            "reference_period": "August 2026",
            "released": "14 September 2026",
            "caveat": "Latest month is Provisional.",
        },
        CitizenMethod: {
            "what_it_counts": "Retail prices of selected goods and services.",
            "coverage": "States and UTs in the CPI collection.",
        },
        DisplayValue: {
            "raw_value": 4.82,
            "unit": "percent",
            "display_scale": DisplayScale.none,
            "display_string": "4.82",
            "status": ObservationStatus.value,
            "chart_value": 4.82,
        },
        CitizenGeography: {
            "geography_label": "Kerala",
            "geography_slug": "kerala",
        },
    }
    for model, base in payloads.items():
        for name in FORBIDDEN_PROJECTION_FIELD_NAMES:
            with pytest.raises(ValidationError):
                model.model_validate({**base, name: "desk"})


def test_display_value_hole_is_null_not_zero() -> None:
    with pytest.raises(ValidationError, match="chart_value null"):
        DisplayValue(
            raw_value=0,
            unit="₹ crore",
            display_scale=DisplayScale.none,
            display_string=NOT_PUBLISHED,
            status=ObservationStatus.unknown,
            chart_value=0,
        )
    hole = DisplayValue(
        raw_value=None,
        unit="₹ crore",
        display_scale=DisplayScale.none,
        display_string=NOT_PUBLISHED,
        status=ObservationStatus.unknown,
        chart_value=None,
    )
    assert hole.chart_value is None
    assert hole.display_string == NOT_PUBLISHED


def test_display_value_published_requires_chart_value() -> None:
    with pytest.raises(ValidationError, match="requires chart_value"):
        DisplayValue(
            raw_value=12.0,
            unit="percent",
            display_scale=DisplayScale.none,
            display_string="12",
            status=ObservationStatus.value,
            chart_value=None,
        )


def test_cite_element_id_splits_when_one_id_covers_two_periods() -> None:
    from prism.citizen_projection import cite_element_id

    citation_id = "cite-c1-cpi-general-base-2024-2026-08"
    one = frozenset({"2026-08"})
    two = frozenset({"2026-07", "2026-08"})
    assert cite_element_id(citation_id, "2026-08", one) == f"cite-{citation_id}"
    assert (
        cite_element_id(citation_id, "2026-08", two) == f"cite-{citation_id}--2026-08"
    )
    assert (
        cite_element_id(citation_id, "2026-07", two) == f"cite-{citation_id}--2026-07"
    )


def test_project_citizen_cite_and_method() -> None:
    from prism.citizen_projection import project_citizen_cite, project_citizen_method
    from tests.factories import make_caveat, make_citation

    cite = project_citizen_cite(make_citation())
    assert cite.released == "14 September 2026"
    assert cite.producer.startswith("National Statistics Office")
    assert "citation_id" not in cite.model_dump()
    method = project_citizen_method(make_caveat())
    assert "do_not" not in method.model_dump()
    assert "CPI General" in method.what_it_counts


def test_project_citizen_cite_rejects_desk_ingest_flags() -> None:
    from prism.citizen_projection import assert_citizen_caveat

    with pytest.raises(ValueError, match="desk language"):
        assert_citizen_caveat(
            "PDF reconstruction (ambiguous=0). Do not collapse. Card 2."
        )
    from prism.citizen_projection import assert_citizen_method_note

    with pytest.raises(ValueError, match="desk language"):
        assert_citizen_method_note("There is no later census total on this desk.")


def test_catalog_citations_project_without_desk_language() -> None:
    from prism.catalog import default_catalog
    from prism.citizen_projection import (
        assert_citizen_caveat,
        assert_citizen_method_note,
        project_citizen_cite,
    )

    catalog = default_catalog()
    for citation in catalog.citations.values():
        assert_citizen_caveat(citation.caveat_one_line)
        cite = project_citizen_cite(citation)
        assert cite.caveat == citation.caveat_one_line
    for note in catalog.caveats.values():
        assert note.citizen_note
        assert_citizen_method_note(note.citizen_note)


def test_citizen_period_label_strips_marks_and_prefixes() -> None:
    from prism.citizen_projection import citizen_period_label

    assert citizen_period_label("1901 $") == "1901"
    assert citizen_period_label("1951 @") == "1951"
    assert citizen_period_label("1981 #") == "1981"
    assert citizen_period_label("1991 +") == "1991"
    assert citizen_period_label("2001 ++") == "2001"
    assert citizen_period_label("2011") == "2011"
    assert citizen_period_label("end-2024-25") == "2024-25"
    assert citizen_period_label("actual-2017-18") == "2017-18"
    assert citizen_period_label("actuals-2024-2025") == "2024-2025"
    assert citizen_period_label("revised-2025-26") == "2025-26"
    assert citizen_period_label("budget-2026-27") == "2026-27"
    assert citizen_period_label("re-2025-26") == "2025-26"
    assert citizen_period_label("be-2026-27") == "2026-27"
    assert citizen_period_label("2026-08") == "2026-08"

    from prism.citizen_projection import (
        project_display_value,
        scale_for_concept,
    )

    assert scale_for_concept((4.82, 5.52), rate_or_index=True) is DisplayScale.none
    assert scale_for_concept((1_210_854_977,), rate_or_index=False) is DisplayScale.Cr
    display = project_display_value(
        raw_value=1_210_854_977,
        unit="persons",
        status=ObservationStatus.value,
        scale=DisplayScale.Cr,
    )
    assert display.display_string == "121.09 Cr"
    assert display.chart_value == pytest.approx(121.0854977)
    rate = project_display_value(
        raw_value=4.45,
        unit="inflation (%)",
        status=ObservationStatus.value,
        scale=DisplayScale.none,
    )
    assert rate.display_string == "4.45"
    assert rate.chart_value == 4.45
    hole = project_display_value(
        raw_value=None,
        unit="₹ crore",
        status=ObservationStatus.unknown,
        scale=DisplayScale.L,
    )
    assert hole.chart_value is None
    assert hole.display_string == NOT_PUBLISHED


def test_display_string_is_whole_citizen_unit() -> None:
    from prism.citizen_projection import (
        assert_display_string,
        concept_key,
        magnitude_for_display,
        project_display_value,
        scale_for_concept,
    )

    money = project_display_value(
        raw_value=3_527_000.0,
        unit="₹ crore; REVENUE RECEIPTS",
        status=ObservationStatus.value,
        scale=DisplayScale.L,
    )
    assert money.display_string == "35.27 L Cr"
    assert "crore" not in money.display_string.lower()

    projected_raw = 1_423_000.0
    persons = magnitude_for_display(
        projected_raw, "thousands ('000); projected; 1st March"
    )
    assert persons == pytest.approx(1_423_000_000.0)
    assert concept_key("ncp", "thousands ('000); projected; 1st March") == "headcount"
    assert concept_key("census", "persons") == "headcount"
    scale = scale_for_concept((1_210_854_977.0, persons), rate_or_index=False)
    assert scale is DisplayScale.Cr
    projected = project_display_value(
        raw_value=projected_raw,
        unit="thousands ('000); projected; 1st March",
        status=ObservationStatus.value,
        scale=scale,
    )
    assert projected.display_string == "142.3 Cr"
    assert "thousand" not in projected.display_string.lower()

    with pytest.raises(ValueError, match="producer unit word"):
        assert_display_string("35.27 L crore")
    with pytest.raises(ValueError, match="producer unit word"):
        assert_display_string("14.23 L Thousand")
