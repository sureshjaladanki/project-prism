"""Citizen projections at bind.

Types live in ``schema``. Bind calls ``project_*``; HTML chrome is C5.
"""

from __future__ import annotations

from datetime import date

from prism.schema import (
    NOT_PUBLISHED,
    CaveatNote,
    Citation,
    CitizenCite,
    CitizenGeography,
    CitizenMethod,
    ContractModel,
    DisplayScale,
    DisplayValue,
    ObservationStatus,
)

PROJECTION_TYPES: tuple[type[ContractModel], ...] = (
    CitizenCite,
    CitizenMethod,
    DisplayValue,
    CitizenGeography,
)

FORBIDDEN_PROJECTION_FIELD_NAMES = frozenset(
    {
        "do_not",
        "id",
        "citation_id",
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
    }
)

THOUSAND = 1_000.0
LAKH = 100_000.0
CRORE = 10_000_000.0

_RATE_MARKERS = (
    "%",
    "inflation",
    "index",
    "rate",
    "tfr",
    "per thousand",
    "per 1,000",
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
        series=citation.series,
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


def concept_key(series_id: str, unit: str) -> str:
    if is_rate_or_index(unit):
        return f"{series_id}::none"
    return f"{series_id}::magnitude"


def is_rate_or_index(unit: str) -> bool:
    lower = unit.lower()
    return any(marker in lower for marker in _RATE_MARKERS)


def scale_for_concept(values: tuple[float, ...], *, rate_or_index: bool) -> DisplayScale:
    if rate_or_index or not values:
        return DisplayScale.none
    peak = max(abs(item) for item in values)
    if peak >= CRORE:
        return DisplayScale.Cr
    if peak >= LAKH:
        return DisplayScale.L
    if peak >= THOUSAND:
        return DisplayScale.K
    return DisplayScale.none


def project_display_value(
    *,
    raw_value: float | None,
    unit: str,
    status: ObservationStatus | str,
    scale: DisplayScale,
) -> DisplayValue:
    if not isinstance(status, ObservationStatus):
        status = ObservationStatus(status)
    published = status is ObservationStatus.value
    if not published:
        return DisplayValue(
            raw_value=raw_value,
            unit=unit,
            display_scale=scale,
            display_string=NOT_PUBLISHED,
            status=status,
            chart_value=None,
        )
    if raw_value is None:
        raise ValueError("status value requires raw_value")
    chart_value = apply_scale(raw_value, scale)
    return DisplayValue(
        raw_value=raw_value,
        unit=unit,
        display_scale=scale,
        display_string=display_string(chart_value, scale),
        status=status,
        chart_value=chart_value,
    )


def apply_scale(value: float, scale: DisplayScale) -> float:
    if scale is DisplayScale.Cr:
        return value / CRORE
    if scale is DisplayScale.L:
        return value / LAKH
    if scale is DisplayScale.K:
        return value / THOUSAND
    return value


def display_string(chart_value: float, scale: DisplayScale) -> str:
    shown = chart_value if scale is DisplayScale.none else round(chart_value, 2)
    grouped = indian_grouped(shown)
    if scale is DisplayScale.none:
        return grouped
    return f"{grouped} {scale.value}"


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
