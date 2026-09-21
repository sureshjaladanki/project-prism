"""C3: a hole is never plotted as zero. GST Compensation Cess is the fixture."""

from __future__ import annotations

import pytest

from prism.schema import ObservationStatus, ServedObservation
from prism.serving import (
    GST_COMPENSATION_CESS,
    ServeError,
    assert_hole_never_plotted_as_zero,
    chart_payload,
)
from tests.factories import make_caveat, make_citation, make_observation

CESS_UNIT = f"₹ crore; 8.03 {GST_COMPENSATION_CESS}"


def test_gst_compensation_cess_null_passes_hole_gate() -> None:
    observation = make_observation(
        value=None,
        status=ObservationStatus.unknown,
        unit=CESS_UNIT,
    )
    payload = chart_payload(
        ServedObservation(
            observation=observation,
            citation=make_citation(),
            caveat=make_caveat(),
        )
    )
    payload["head_name"] = GST_COMPENSATION_CESS
    assert payload["value"] is None
    assert payload["unit"] == CESS_UNIT
    assert_hole_never_plotted_as_zero(payload)


def test_gst_compensation_cess_zero_fails_hole_gate() -> None:
    with pytest.raises(ServeError, match="plotted as zero"):
        assert_hole_never_plotted_as_zero(
            {
                "head_name": GST_COMPENSATION_CESS,
                "unit": CESS_UNIT,
                "value": 0,
                "status": ObservationStatus.value.value,
            }
        )


def test_chart_payload_nulls_non_published_zero() -> None:
    observation = make_observation(
        value=0,
        status=ObservationStatus.unknown,
        unit=CESS_UNIT,
    )
    payload = chart_payload(
        ServedObservation(
            observation=observation,
            citation=make_citation(),
            caveat=make_caveat(),
        )
    )
    assert payload["value"] is None
    assert payload["status"] == ObservationStatus.unknown.value
    payload["head_name"] = GST_COMPENSATION_CESS
    assert_hole_never_plotted_as_zero(payload)
