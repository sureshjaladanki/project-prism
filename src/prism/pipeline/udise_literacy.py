"""Map UDISE+ stocks/facilities and Census PCA literacy into a data vintage."""

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

MAPPER_VERSION = "c6-observations-1.0.0"
UDISE_PERIOD = "2025-26"
PCA_PERIOD = "2011-03-01"
UDISE_SECTOR = "Total"
PCA_TRU = frozenset({"Total", "Rural", "Urban"})

SCHOOLS_ENROL_TEACHERS_MEASURES = (
    ("schools", "schools", "schools"),
    ("enrolments", "students enrolled", "enrolments"),
    ("teachers", "teachers", "teachers"),
)
FACILITY_MEASURES = (
    ("tot_sch_b_toilet", "schools having boys toilet", "boys-toilet"),
    ("tot_sch_g_toilet", "schools having girls toilet", "girls-toilet"),
    ("tot_sch_library", "schools having library", "library"),
    ("tot_sch_electricity", "schools having electricity", "electricity"),
    ("tot_sch_drinkwater", "schools having drinking water", "drinkwater"),
    ("tot_sch_handwash", "schools having hand wash", "handwash"),
    ("tot_sch_medical", "schools having medical check-up", "medical"),
    ("tot_sch_ramp", "schools having ramp", "ramp"),
)
LITERACY_MEASURES = (
    ("P_LIT", "persons (literate)", "p-lit"),
    ("M_LIT", "males (literate)", "m-lit"),
    ("F_LIT", "females (literate)", "f-lit"),
    ("P_ILL", "persons (illiterate)", "p-ill"),
    ("M_ILL", "males (illiterate)", "m-ill"),
    ("F_ILL", "females (illiterate)", "f-ill"),
    ("TOT_P", "persons", "tot-p"),
    ("TOT_M", "males", "tot-m"),
    ("TOT_F", "females", "tot-f"),
)

_SLUG = re.compile(r"[^a-z0-9]+")
_MINUS_PREFIXES = frozenset({"-", "\u2212", "\u2013", "\u2014", "\ufffd"})


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


def _observation_status(value: float | None) -> ObservationStatus:
    if value is None:
        return ObservationStatus.unknown
    return ObservationStatus.value


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
        status=_observation_status(value),
        lineage=lineage,
    )


def _map_udise_region_measures(
    rows: list[dict[str, str]],
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
    measures: tuple[tuple[str, str, str], ...],
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        code = _cell(row, "region_code")
        name = _cell(row, "region_name")
        if code == "" or name == "":
            raise PipelineError("udise row missing region_code/region_name; not recoding")
        geo = _ref(code, name, frame)
        for column, unit, measure in measures:
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=UDISE_SECTOR,
                    period=UDISE_PERIOD,
                    measure=measure,
                    value=_number(_cell(row, column), label=column),
                    unit=unit,
                    lineage=lineage,
                )
            )
    return tuple(out)


def map_udise_schools_enrolment_teachers(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    return _map_udise_region_measures(
        rows,
        series_id=series_id,
        citation_id=citation_id,
        caveat_id=caveat_id,
        frame=frame,
        lineage=lineage,
        measures=SCHOOLS_ENROL_TEACHERS_MEASURES,
    )


def map_udise_facilities(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    return _map_udise_region_measures(
        rows,
        series_id=series_id,
        citation_id=citation_id,
        caveat_id=caveat_id,
        frame=frame,
        lineage=lineage,
        measures=FACILITY_MEASURES,
    )


def map_census_pca_literacy(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        code = (
            _cell(row, "State").zfill(2)
            if _cell(row, "State").isdigit()
            else _cell(row, "State")
        )
        name = _cell(row, "Name")
        sector = _cell(row, "TRU")
        if code == "" or name == "":
            raise PipelineError("pca literacy row missing State/Name; not recoding")
        if sector not in PCA_TRU:
            raise PipelineError(
                f"pca literacy unpublished TRU {sector!r}; not inventing Combined"
            )
        geo = _ref(code, name, frame)
        for column, unit, measure in LITERACY_MEASURES:
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=sector,
                    period=PCA_PERIOD,
                    measure=measure,
                    value=_number(_cell(row, column), label=column),
                    unit=unit,
                    lineage=lineage,
                )
            )
    return tuple(out)


register_mapper(
    "udise-schools-enrol-teachers",
    MapperSpec(map_rows=map_udise_schools_enrolment_teachers, version=MAPPER_VERSION),
)
register_mapper(
    "udise-facilities",
    MapperSpec(map_rows=map_udise_facilities, version=MAPPER_VERSION),
)
register_mapper(
    "census-pca-literacy-tru",
    MapperSpec(map_rows=map_census_pca_literacy, version=MAPPER_VERSION),
)
