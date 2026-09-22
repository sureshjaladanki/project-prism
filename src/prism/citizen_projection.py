"""Citizen projections at bind.

Types live in ``schema``. Bind calls ``project_*``; HTML chrome is C5.
"""

from __future__ import annotations

import re
from datetime import date

from prism.schema import (
    NOT_PUBLISHED,
    AxisToken,
    CaveatNote,
    ChangeDirection,
    Citation,
    CitizenChange,
    CitizenCite,
    CitizenGeography,
    CitizenMethod,
    CitizenNumber,
    ContractModel,
    Denomination,
    DenominationMagnitude,
    DenominationMeasure,
    ObservationStatus,
)

PROJECTION_TYPES: tuple[type[ContractModel], ...] = (
    CitizenCite,
    CitizenMethod,
    CitizenNumber,
    CitizenChange,
    CitizenGeography,
)

FORBIDDEN_PROJECTION_FIELD_NAMES = frozenset(
    {
        "do_not",
        "id",
        "caveat_id",
        "geography_vintage",
        "vintage_id",
        "parser",
        "parser_name",
        "parser_version",
        "frame_label",
        "table_label",
        "geography_as_published",
        "next_release",
        "display_scale",
        "concept_key",
    }
)

THOUSAND = 1_000.0
LAKH = 100_000.0
CRORE = 10_000_000.0
LAKH_CRORE = 1_000_000_000_000.0

_MAGNITUDE_TO_ONES: dict[DenominationMagnitude, float] = {
    DenominationMagnitude.ones: 1.0,
    DenominationMagnitude.thousand: THOUSAND,
    DenominationMagnitude.lakh: LAKH,
    DenominationMagnitude.crore: CRORE,
}

_AXIS_DIVISOR: dict[AxisToken, float] = {
    AxisToken.none: 1.0,
    AxisToken.K: THOUSAND,
    AxisToken.L: LAKH,
    AxisToken.Cr: CRORE,
    AxisToken.L_Cr: LAKH_CRORE,
}

_AXIS_PROSE: dict[AxisToken, str] = {
    AxisToken.none: "",
    AxisToken.K: "thousand",
    AxisToken.L: "lakh",
    AxisToken.Cr: "crore",
    AxisToken.L_Cr: "lakh crore",
}

_RATE_MARKERS = (
    "%",
    "inflation",
    "index",
    "rate",
    "tfr",
    "per thousand",
    "per 1,000",
)

# Producer unit words wrongly glued after a compact token (ruling 1).
_FORBIDDEN_COMPACT_UNIT = re.compile(
    r"\b(?:[KL]|Cr|L Cr)\s+(?:crore|crores|thousand|thousands|lakh|lakhs)\b",
    re.IGNORECASE,
)

DESK_CITE_MARKERS = (
    "pdf reconstruction",
    "ambiguous=0",
    "html reconstruction",
    "named hole",
    "do not ",
    "card 1",
    "card 2",
    "card 3",
    "cards 1",
    "cards 6",
)

DESK_METHOD_MARKERS = (
    "on this desk",
    "this desk",
    "next_release",
    "pdfplumber",
)

NOT_COMPARABLE = "not comparable"


def citizen_series_label(series: str) -> str:
    """Citizen series name: drop base-year and group-code decoder text (F-c1-group-code)."""
    text = re.sub(r"\s*\(Base\s+\d{4}\s*=\s*100\)", "", series, flags=re.IGNORECASE)
    text = re.sub(
        r";?\s*same values as CPI Group name Food,\s*Group code\s*[0-9.]+",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r",\s*COICOP\s+2018\s*\([^)]*\)", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", text).strip(" —;,")


def project_citizen_cite(
    citation: Citation,
    *,
    reference_period: str | None = None,
    caveat: str | None = None,
) -> CitizenCite:
    text = caveat if caveat is not None else citation.caveat_one_line
    return CitizenCite(
        producer=citation.producer,
        url=citation.url,
        series=citizen_series_label(citation.series),
        reference_period=reference_period or citation.reference_period,
        released=_released(citation.release_date),
        caveat=text,
    )


def cite_element_id(
    citation_id: str,
    reference_period: str,
    periods_for_citation: frozenset[str],
) -> str:
    """HTML id for a CitizenCite. Split when one catalog id covers two periods."""
    if len(periods_for_citation) <= 1:
        return f"cite-{citation_id}"
    return f"cite-{citation_id}--{reference_period}"


def assert_citizen_caveat(text: str) -> None:
    lowered = text.lower()
    for marker in DESK_CITE_MARKERS:
        if marker in lowered:
            raise ValueError(f"CitizenCite.caveat carries desk language: {marker!r}")


def assert_citizen_method_note(text: str) -> None:
    lowered = text.lower()
    for marker in DESK_METHOD_MARKERS:
        if marker in lowered:
            raise ValueError(f"CitizenMethod note carries desk language: {marker!r}")


def project_citizen_method(caveat: CaveatNote) -> CitizenMethod:
    note = caveat.citizen_note
    if note is None or note.strip() == "":
        raise ValueError(f"{caveat.caveat_id} missing citizen_note")
    assert_citizen_method_note(note)
    first, _, rest = note.partition(". ")
    coverage = first if rest == "" else first + "."
    return CitizenMethod(
        what_it_counts=note,
        coverage=coverage,
        break_note=None,
        lag_note=None,
    )


def project_citizen_geography(*, label: str, slug: str) -> CitizenGeography:
    return CitizenGeography(geography_label=label, geography_slug=slug)


def denomination_from_unit(unit: str) -> Denomination:
    """Infer denomination from the producer unit string. Pipeline should set it explicitly."""
    if is_rate_or_index(unit):
        lower = unit.lower()
        if "%" in lower or "inflation" in lower or "percent" in lower:
            measure = DenominationMeasure.percent
        elif "index" in lower:
            measure = DenominationMeasure.index
        else:
            measure = DenominationMeasure.rate
        return Denomination(magnitude=DenominationMagnitude.ones, measure=measure)
    lower = unit.lower()
    if "crore" in lower:
        return Denomination(
            magnitude=DenominationMagnitude.crore, measure=DenominationMeasure.rupees
        )
    if "lakh" in lower:
        return Denomination(
            magnitude=DenominationMagnitude.lakh, measure=DenominationMeasure.rupees
        )
    if "thousand" in lower or "'000" in lower:
        return Denomination(
            magnitude=DenominationMagnitude.thousand,
            measure=DenominationMeasure.persons,
        )
    if any(
        token in lower
        for token in ("person", "male", "female", "household", "tot_p", "tot_m", "tot_f")
    ):
        return Denomination(
            magnitude=DenominationMagnitude.ones, measure=DenominationMeasure.persons
        )
    if "₹" in unit or "rs" in lower or "rupee" in lower:
        return Denomination(
            magnitude=DenominationMagnitude.ones, measure=DenominationMeasure.rupees
        )
    return Denomination(
        magnitude=DenominationMagnitude.ones, measure=DenominationMeasure.count
    )


def is_rate_or_index(unit: str) -> bool:
    lower = unit.lower()
    return any(marker in lower for marker in _RATE_MARKERS)


def never_compacts(denomination: Denomination) -> bool:
    return denomination.measure in {
        DenominationMeasure.percent,
        DenominationMeasure.rate,
        DenominationMeasure.index,
    }


def to_canonical(value: float, denomination: Denomination) -> float:
    """Convert producer value × denomination to base units (rupees, persons, or as published)."""
    if never_compacts(denomination):
        return value
    return value * _MAGNITUDE_TO_ONES[denomination.magnitude]


def scale_for_group(
    canonical_values: tuple[float, ...], *, compact: bool
) -> AxisToken:
    """Pick one axis token for a template-declared scale group from canonical peaks."""
    if not compact or not canonical_values:
        return AxisToken.none
    peak = max(abs(item) for item in canonical_values)
    if peak >= LAKH_CRORE:
        return AxisToken.L_Cr
    if peak >= CRORE:
        return AxisToken.Cr
    if peak >= LAKH:
        return AxisToken.L
    if peak >= THOUSAND:
        return AxisToken.K
    return AxisToken.none


def project_citizen_number(
    *,
    value: float | None,
    denomination: Denomination,
    status: ObservationStatus | str,
    axis: AxisToken,
) -> CitizenNumber:
    if not isinstance(status, ObservationStatus):
        status = ObservationStatus(status)
    published = status is ObservationStatus.value
    if not published:
        return CitizenNumber(
            canonical_value=None if value is None else to_canonical(value, denomination),
            measure=denomination.measure,
            text=NOT_PUBLISHED,
            chart_value=None,
            axis_label=axis.value,
            status=status,
        )
    if value is None:
        raise ValueError("status value requires value")
    canonical = to_canonical(value, denomination)
    if never_compacts(denomination):
        axis = AxisToken.none
    chart_value = canonical / _AXIS_DIVISOR[axis]
    shown = chart_value if axis is AxisToken.none else round(chart_value, 2)
    text = format_citizen_text(shown, axis, measure=denomination.measure)
    assert_citizen_number_text(text)
    assert_magnitude_integrity(
        producer_value=value,
        denomination=denomination,
        canonical=canonical,
        text=text,
    )
    return CitizenNumber(
        canonical_value=canonical,
        measure=denomination.measure,
        text=text,
        chart_value=chart_value,
        axis_label=axis.value,
        status=status,
    )


def format_citizen_text(
    shown: float, axis: AxisToken, *, measure: DenominationMeasure
) -> str:
    grouped = indian_grouped(shown)
    prose = _AXIS_PROSE[axis]
    if measure is DenominationMeasure.rupees:
        if prose == "":
            return f"₹{grouped}"
        return f"₹{grouped} {prose}"
    if measure is DenominationMeasure.persons:
        if prose == "":
            return f"{grouped} people"
        return f"{grouped} {prose} people"
    return grouped


def assert_citizen_number_text(text: str) -> None:
    if text == NOT_PUBLISHED:
        return
    if _FORBIDDEN_COMPACT_UNIT.search(text):
        raise ValueError(
            f"citizen text must not glue a compact token to a producer unit word: {text!r}"
        )


def assert_magnitude_integrity(
    *,
    producer_value: float,
    denomination: Denomination,
    canonical: float,
    text: str,
) -> None:
    """Blueprint test 10: citizen magnitude must match the producer's published magnitude."""
    expected = to_canonical(producer_value, denomination)
    if abs(canonical - expected) > max(1e-9, abs(expected) * 1e-12):
        raise ValueError(
            f"canonical magnitude {canonical} differs from producer "
            f"{producer_value} × {denomination.magnitude.value}"
        )
    if never_compacts(denomination):
        return
    # Fail the known wrong-order pattern: crore column shown as a fraction of a crore.
    if (
        denomination.magnitude is DenominationMagnitude.crore
        and denomination.measure is DenominationMeasure.rupees
        and producer_value >= 1_000_000
        and text.startswith("₹0.")
    ):
        raise ValueError(f"citizen text loses crore order of magnitude: {text!r}")


def project_citizen_change(
    *,
    current_value: float | None,
    prior_value: float | None,
    denomination: Denomination,
    current_status: ObservationStatus | str,
    prior_status: ObservationStatus | str,
    prior_period: str,
    prior_citation_id: str,
    axis: AxisToken,
    comparable: bool = True,
) -> CitizenChange:
    current = project_citizen_number(
        value=current_value,
        denomination=denomination,
        status=current_status,
        axis=axis,
    )
    prior = project_citizen_number(
        value=prior_value,
        denomination=denomination,
        status=prior_status,
        axis=axis,
    )
    if (
        not comparable
        or current.status is not ObservationStatus.value
        or prior.status is not ObservationStatus.value
        or current.canonical_value is None
        or prior.canonical_value is None
    ):
        if prior.status is not ObservationStatus.value:
            difference = NOT_PUBLISHED
            direction = ChangeDirection.unchanged
        else:
            difference = NOT_COMPARABLE
            direction = ChangeDirection.unchanged
    else:
        delta = current.canonical_value - prior.canonical_value
        if abs(delta) < 1e-12:
            direction = ChangeDirection.unchanged
        elif delta > 0:
            direction = ChangeDirection.higher
        else:
            direction = ChangeDirection.lower
        diff_number = project_citizen_number(
            value=abs(delta) / _MAGNITUDE_TO_ONES[denomination.magnitude]
            if not never_compacts(denomination)
            else abs(delta),
            denomination=denomination,
            status=ObservationStatus.value,
            axis=axis,
        )
        difference = diff_number.text
    return CitizenChange(
        current=current,
        prior=prior,
        prior_period=prior_period,
        direction=direction,
        difference=difference,
        citation_id=prior_citation_id,
    )


def indian_grouped(value: float) -> str:
    text = format(value, ".12g")
    if "e" in text.lower():
        text = format(value, ".12f").rstrip("0").rstrip(".")
    sign = ""
    if text.startswith("-"):
        sign = "-"
        text = text[1:]
    if "." in text:
        integer, fraction = text.split(".", 1)
        return f"{sign}{_indian_group_integer(integer)}.{fraction}"
    return f"{sign}{_indian_group_integer(text)}"


_CENSUS_YEAR_MARKS = re.compile(r"\s*[$@#+\u2020\u2021].*$")
_PERIOD_KEY_PREFIX = re.compile(
    r"^(end|actuals?|budget|revised|re|be)-",
    re.IGNORECASE,
)


def citizen_period_label(reference_period: str) -> str:
    """Axis / tick label. Year only — no producer footnote marks or machine prefixes."""
    text = reference_period.strip()
    text = _CENSUS_YEAR_MARKS.sub("", text).strip()
    text = text.rstrip("+").strip()
    text = _PERIOD_KEY_PREFIX.sub("", text).strip()
    return text if text else reference_period


def _indian_group_integer(digits: str) -> str:
    if len(digits) <= 3:
        return digits
    last_three = digits[-3:]
    rest = digits[:-3]
    groups: list[str] = []
    while rest:
        groups.append(rest[-2:])
        rest = rest[:-2]
    return ",".join(reversed(groups)) + "," + last_three


def _released(value: date | str) -> str:
    if value == "unknown":
        return "not printed"
    if isinstance(value, date):
        return f"{value.day} {value.strftime('%B %Y')}"
    return str(value)
