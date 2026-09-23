"""Map NFHS fact-sheet and RHS facility tables into a data vintage."""

from __future__ import annotations

import re

from prism.catalog.registry import MapperSpec, register_mapper
from prism.citizen_projection import denomination_from_unit
from prism.pipeline.errors import PipelineError
from prism.schema import (
    GeographyRef,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
)

MAPPER_VERSION = "c7-health-1.0.0"
NFHS_PERIOD = "2023-24"
RHS_PERIOD = "2021-22"
_SLUG = re.compile(r"[^a-z0-9]+")
_MINUS_PREFIXES = frozenset({"-", "\u2212", "\u2013", "\u2014", "\ufffd"})

NFHS_MEASURES = (
    ("nfhs6_urban", "Urban", "nfhs6"),
    ("nfhs6_rural", "Rural", "nfhs6"),
    ("nfhs6_total", "Total", "nfhs6"),
    ("nfhs5_total", "Total", "nfhs5"),
)
RHS_MEASURES = (
    ("sc_2022", "sc-functioning"),
    ("phc_2022", "phc-functioning"),
    ("chc_2022", "chc-functioning"),
)


def _cell(row: dict[str, str], name: str) -> str:
    value = row.get(name)
    if value is None:
        return ""
    return value.strip()


def _slug(text: str, fallback: str = "unit") -> str:
    ascii_only = text.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG.sub("-", ascii_only.lower()).strip("-")
    if slug == "":
        return fallback
    return slug[:80]


def _number(text: str, *, label: str) -> float | None:
    stripped = text.strip().replace(",", "").replace(" ", "")
    if stripped == "":
        return None
    if stripped.lower() in {".", "..", "...", "…", "n.a.", "na", "n/a"}:
        return None
    stripped = stripped.removesuffix("%")
    stripped = stripped.removeprefix("+")
    if stripped[:1] in _MINUS_PREFIXES:
        stripped = "-" + stripped[1:]
    if stripped == "" or stripped == "-":
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise PipelineError(f"unparseable {label}: {text!r}") from exc


def _names(frame: GeographyVintage) -> dict[str, str]:
    return {unit.code: unit.name_en for unit in frame.units_included}


def _ref(code: str, name: str, frame: GeographyVintage) -> GeographyRef:
    expected = _names(frame).get(code)
    if expected is None:
        raise PipelineError(
            f"producer code {code!r} is not in {frame.frame_id}; not recoding"
        )
    if expected != name:
        raise PipelineError(
            f"producer name {name!r} for code {code} does not match frame "
            f"{expected!r}; not recoding"
        )
    return GeographyRef(
        code=code,
        geography_vintage=frame.geography_vintage,
        code_system=frame.code_system,
    )


def _printed_ref(name: str, frame: GeographyVintage) -> GeographyRef:
    return _ref(_slug(name), name, frame)


def _obs(
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geo: GeographyRef,
    sector: str,
    period: str,
    measure: str,
    value: float | None,
    unit: str,
    lineage: ObservationLineage,
) -> Observation:
    period_token = _slug(period, "period")
    return Observation(
        observation_id=(
            f"obs-{series_id}-{geo.code}-{_slug(sector)}-{period_token}-{measure}"
        ),
        series_id=series_id,
        citation_id=citation_id,
        caveat_id=caveat_id,
        geography=geo,
        sector=sector,
        reference_period=period,
        value=value,
        unit=unit,
        denomination=denomination_from_unit(unit),
        status=ObservationStatus.unknown
        if value is None
        else ObservationStatus.value,
        lineage=lineage,
    )


def _map_nfhs(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        name = _cell(row, "geography")
        indicator = _cell(row, "indicator")
        if name == "" or indicator == "":
            continue
        geo = _printed_ref(name, geography)
        measure = _slug(indicator, f"indicator-{index}")
        for column, sector, round_tag in NFHS_MEASURES:
            obs = _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector=sector,
                period=NFHS_PERIOD if round_tag == "nfhs6" else "2019-21",
                measure=f"{round_tag}-{measure}",
                value=_number(_cell(row, column), label=column),
                unit=f"NFHS fact-sheet indicator as published; {indicator}",
                lineage=lineage,
            )
            if obs.observation_id in seen:
                obs = obs.model_copy(
                    update={"observation_id": f"{obs.observation_id}-{index}"}
                )
            seen.add(obs.observation_id)
            out.append(obs)
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def _map_rhs(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        name = _cell(row, "geography")
        if name == "":
            continue
        geo = _printed_ref(name, geography)
        for column, measure in RHS_MEASURES:
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector="Rural",
                    period=RHS_PERIOD,
                    measure=measure,
                    value=_number(_cell(row, column), label=column),
                    unit=f"RHS facility count as published; {measure}",
                    lineage=lineage,
                )
            )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


register_mapper(
    "nfhs-factsheet-indicators",
    MapperSpec(map_rows=_map_nfhs, version=MAPPER_VERSION),
)
register_mapper(
    "rhs-facility-counts",
    MapperSpec(map_rows=_map_rhs, version=MAPPER_VERSION),
)
