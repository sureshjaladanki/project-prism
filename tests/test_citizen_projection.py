"""Citizen projection types cannot carry desk fields; denomination integrity holds."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prism.citizen_projection import (
    FORBIDDEN_PROJECTION_FIELD_NAMES,
    NOT_COMPARABLE,
    PROJECTION_TYPES,
    assert_citizen_number_text,
    denomination_from_unit,
    project_citizen_change,
    project_citizen_number,
    scale_for_group,
    to_canonical,
)
from prism.schema import (
    NOT_PUBLISHED,
    AxisToken,
    ChangeDirection,
    CitizenChange,
    CitizenCite,
    CitizenGeography,
    CitizenMethod,
    CitizenNumber,
    Denomination,
    DenominationMagnitude,
    DenominationMeasure,
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
        CitizenNumber: {
            "canonical_value": 4.82,
            "measure": DenominationMeasure.percent,
            "text": "4.82",
            "chart_value": 4.82,
            "axis_label": "",
            "status": ObservationStatus.value,
        },
        CitizenChange: {
            "current": {
                "canonical_value": 4.82,
                "measure": DenominationMeasure.percent,
                "text": "4.82",
                "chart_value": 4.82,
                "axis_label": "",
                "status": ObservationStatus.value,
            },
            "prior": {
                "canonical_value": 4.45,
                "measure": DenominationMeasure.percent,
                "text": "4.45",
                "chart_value": 4.45,
                "axis_label": "",
                "status": ObservationStatus.value,
            },
            "prior_period": "July 2026",
            "direction": ChangeDirection.higher,
            "difference": "0.37",
            "citation_id": "cite-prior",
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


def test_citizen_number_hole_is_null_not_zero() -> None:
    with pytest.raises(ValidationError, match="chart_value null"):
        CitizenNumber(
            canonical_value=None,
            measure=DenominationMeasure.rupees,
            text=NOT_PUBLISHED,
            chart_value=0,
            axis_label="",
            status=ObservationStatus.unknown,
        )
    hole = project_citizen_number(
        value=None,
        denomination=Denomination(
            magnitude=DenominationMagnitude.crore,
            measure=DenominationMeasure.rupees,
        ),
        status=ObservationStatus.unknown,
        axis=AxisToken.L_Cr,
    )
    assert hole.chart_value is None
    assert hole.text == NOT_PUBLISHED


def test_citizen_number_published_requires_chart_value() -> None:
    with pytest.raises(ValidationError, match="requires chart_value"):
        CitizenNumber(
            canonical_value=12.0,
            measure=DenominationMeasure.percent,
            text="12",
            chart_value=None,
            axis_label="",
            status=ObservationStatus.value,
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


def test_citizen_series_label_drops_group_code_and_base() -> None:
    from prism.citizen_projection import citizen_series_label, project_citizen_cite
    from tests.factories import make_citation

    raw = (
        "Consumer Food Price Index (CFPI) — Rural, Urban and Combined; "
        "same values as CPI Group name Food, Group code 01.1 (Base 2024=100)"
    )
    assert citizen_series_label(raw) == (
        "Consumer Food Price Index (CFPI) — Rural, Urban and Combined"
    )
    cite = project_citizen_cite(make_citation(series=raw))
    assert "Group code" not in cite.series
    assert "Base 2024" not in cite.series
    assert cite.series.startswith("Consumer Food Price Index (CFPI)")


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


def test_blueprint_10_revenue_receipts_keep_crore_order() -> None:
    """3526840 ₹ crore → ₹35.27 lakh crore, never 0.35 Cr."""
    denom = Denomination(
        magnitude=DenominationMagnitude.crore, measure=DenominationMeasure.rupees
    )
    canonical = to_canonical(3_526_840.0, denom)
    assert canonical == pytest.approx(3.52684e13)  # 3526840 * 1e7
    axis = scale_for_group((canonical,), compact=True)
    assert axis is AxisToken.L_Cr
    number = project_citizen_number(
        value=3_526_840.0,
        denomination=denom,
        status=ObservationStatus.value,
        axis=axis,
    )
    assert number.text == "₹35.27 lakh crore"
    assert number.chart_value == pytest.approx(35.2684)
    assert not number.text.startswith("₹0.")


def test_blueprint_10_seeded_wrong_magnitude_fails() -> None:
    """A crore column whose canonical forgets ×10^7 fails magnitude integrity."""
    denom = Denomination(
        magnitude=DenominationMagnitude.crore, measure=DenominationMeasure.rupees
    )
    with pytest.raises(ValueError, match="canonical magnitude"):
        from prism.citizen_projection import assert_magnitude_integrity

        assert_magnitude_integrity(
            producer_value=3_526_840.0,
            denomination=denom,
            canonical=3_526_840.0,  # wrong: forgot × 1e7
            text="₹0.35",
        )
    with pytest.raises(ValueError, match="order of magnitude"):
        from prism.citizen_projection import assert_magnitude_integrity

        assert_magnitude_integrity(
            producer_value=3_526_840.0,
            denomination=denom,
            canonical=to_canonical(3_526_840.0, denom),
            text="₹0.35",
        )


def test_blueprint_11_gap_never_plotted_as_zero() -> None:
    from prism.serving import ServeError, assert_hole_never_plotted_as_zero

    with pytest.raises(ServeError, match="must be null|plotted as zero"):
        assert_hole_never_plotted_as_zero(
            {
                "unit": "₹ crore; 8.03 GST Compensation Cess",
                "value": 0,
                "status": ObservationStatus.unknown.value,
            }
        )


def test_headcount_and_projection_use_persons_ladder() -> None:
    persons = denomination_from_unit("persons")
    assert persons.measure is DenominationMeasure.persons
    census = project_citizen_number(
        value=1_210_854_977,
        denomination=persons,
        status=ObservationStatus.value,
        axis=AxisToken.Cr,
    )
    assert census.text == "121.09 crore people"
    projected_unit = "thousands ('000); projected; 1st March"
    projected_denom = denomination_from_unit(projected_unit)
    assert projected_denom.magnitude is DenominationMagnitude.thousand
    axis = scale_for_group(
        (to_canonical(1_423_000.0, projected_denom),),
        compact=True,
    )
    assert axis is AxisToken.Cr
    projected = project_citizen_number(
        value=1_423_000.0,
        denomination=projected_denom,
        status=ObservationStatus.value,
        axis=axis,
    )
    assert projected.text == "142.3 crore people"
    assert "thousand" not in projected.text.lower()


def test_rates_never_compact() -> None:
    rate = project_citizen_number(
        value=4.45,
        denomination=denomination_from_unit("inflation (%)"),
        status=ObservationStatus.value,
        axis=AxisToken.Cr,
    )
    assert rate.text == "4.45"
    assert rate.chart_value == 4.45
    assert rate.axis_label == ""


def test_citizen_change_comparable() -> None:
    denom = denomination_from_unit("inflation (%)")
    change = project_citizen_change(
        current_value=4.82,
        prior_value=4.45,
        denomination=denom,
        current_status=ObservationStatus.value,
        prior_status=ObservationStatus.value,
        prior_period="July 2026",
        prior_citation_id="cite-prior",
        axis=AxisToken.none,
    )
    assert change.direction is ChangeDirection.higher
    assert change.difference == "0.37"
    assert change.prior_period == "July 2026"


def test_citizen_change_break_is_not_comparable() -> None:
    denom = denomination_from_unit("inflation (%)")
    change = project_citizen_change(
        current_value=4.82,
        prior_value=4.45,
        denomination=denom,
        current_status=ObservationStatus.value,
        prior_status=ObservationStatus.value,
        prior_period="July 2026",
        prior_citation_id="cite-prior",
        axis=AxisToken.none,
        comparable=False,
    )
    assert change.difference == NOT_COMPARABLE


def test_forbidden_compact_unit_glue() -> None:
    with pytest.raises(ValueError, match="producer unit word|compact token"):
        assert_citizen_number_text("35.27 L crore")
    with pytest.raises(ValueError, match="producer unit word|compact token"):
        assert_citizen_number_text("14.23 L Thousand")
