"""Map C2 derived tables into a data vintage. Does not fetch and does not publish."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from prism.catalog.registry import MapperSpec, register_mapper
from prism.pipeline.errors import PipelineError
from prism.refresh import (
    SERIES_CENSUS_2011_A02_DECADAL,
    SERIES_CENSUS_2011_PCA_SD,
    SERIES_NCP_PROJECTIONS_2011_2036_TABLE8,
    SERIES_SRS_BULLETIN_2024,
    SERIES_SRS_STATISTICAL_REPORT_2024,
)
from prism.schema import (
    GeographyRef,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
)

MAPPER_VERSION = "c2-observations-1.1.0"
PCA_PERIOD = "2011-03-01"
SRS_PERIOD = "2024"
PCA_TRU = frozenset({"Total", "Rural", "Urban"})
PCA_MEASURES = (
    ("TOT_P", "persons", "tot-p"),
    ("TOT_M", "males", "tot-m"),
    ("TOT_F", "females", "tot-f"),
    ("No_HH", "households", "no-hh"),
)
A02_MEASURES = (
    ("persons", "persons", "persons"),
    ("males", "males", "males"),
    ("females", "females", "females"),
    ("variation_absolute", "persons (decadal variation)", "variation-absolute"),
    ("variation_percentage", "percentage (decadal variation)", "variation-percentage"),
)
BULLETIN_MEASURES = (
    ("birth_total", "Total", "birth-rate"),
    ("birth_rural", "Rural", "birth-rate"),
    ("birth_urban", "Urban", "birth-rate"),
    ("death_total", "Total", "death-rate"),
    ("death_rural", "Rural", "death-rate"),
    ("death_urban", "Urban", "death-rate"),
    ("ngr_total", "Total", "natural-growth-rate"),
    ("ngr_rural", "Rural", "natural-growth-rate"),
    ("ngr_urban", "Urban", "natural-growth-rate"),
    ("imr_total", "Total", "infant-mortality-rate"),
    ("imr_rural", "Rural", "infant-mortality-rate"),
    ("imr_urban", "Urban", "infant-mortality-rate"),
)
TABLE3_MEASURES = (
    ("total", "Total"),
    ("rural", "Rural"),
    ("urban", "Urban"),
)
TABLE8_MEASURES = (
    ("persons", "Persons"),
    ("male", "Male"),
    ("females", "Females"),
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


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        observation_id=f"obs-{series_id}-{geo.code}-{_slug(sector)}-{period_token}-{measure}",
        series_id=series_id,
        citation_id=citation_id,
        caveat_id=caveat_id,
        geography=geo,
        sector=sector,
        reference_period=period,
        value=value,
        unit=unit,
        status=_observation_status(value),
        lineage=lineage,
    )


def _map_pca(
    rows: list[dict[str, str]],
    *,
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
            raise PipelineError("pca row missing State/Name; not recoding")
        if sector not in PCA_TRU:
            raise PipelineError(
                f"pca unpublished TRU {sector!r}; not inventing Combined"
            )
        geo = _ref(code, name, frame)
        for column, unit, measure in PCA_MEASURES:
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


def _fill_a02(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    filled: list[dict[str, str]] = []
    state_code = ""
    district = ""
    name = ""
    for row in rows:
        if (
            _cell(row, "state_code")
            or _cell(row, "name")
            or _cell(row, "district_code")
        ):
            state_code = _cell(row, "state_code")
            district = _cell(row, "district_code")
            name = _cell(row, "name")
        merged = dict(row)
        merged["state_code"] = state_code
        merged["district_code"] = district
        merged["name"] = name
        filled.append(merged)
    return filled


def _map_a02(
    rows: list[dict[str, str]],
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    seen: set[str] = set()
    for row in _fill_a02(rows):
        year = _cell(row, "census_year")
        if year == "":
            continue
        district = _cell(row, "district_code")
        if district not in {"", "000"}:
            raise PipelineError(
                "a02 district row reached pipeline; districts are parked"
            )
        code = _cell(row, "state_code")
        if code.isdigit():
            code = code.zfill(2)
        name = _cell(row, "name")
        geo = _ref(code, name, frame)
        for column, unit, measure in A02_MEASURES:
            obs = _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector="Total",
                period=year,
                measure=measure,
                value=_number(_cell(row, column), label=column),
                unit=unit,
                lineage=lineage,
            )
            if obs.observation_id in seen:
                raise PipelineError(f"duplicate a02 observation {obs.observation_id}")
            seen.add(obs.observation_id)
            out.append(obs)
    return tuple(out)


def _map_bulletin(
    rows: list[dict[str, str]],
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        label = _cell(row, "line_label")
        values = [_cell(row, column) for column, _sector, _measure in BULLETIN_MEASURES]
        if not any(values):
            continue
        geo = _printed_ref(label, frame)
        for column, sector, measure in BULLETIN_MEASURES:
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=sector,
                    period=SRS_PERIOD,
                    measure=measure,
                    value=_number(_cell(row, column), label=column),
                    unit=f"SRS rate as published; {measure.replace('-', ' ')}",
                    lineage=lineage,
                )
            )
    return tuple(out)


def _map_table3(
    rows: list[dict[str, str]],
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = _cell(row, "line_label")
        name = _cell(row, "geography")
        if label == "" or name == "":
            continue
        geo = _printed_ref(name, frame)
        measure = _slug(label, f"indicator-{index}")
        for column, sector in TABLE3_MEASURES:
            obs = _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector=sector,
                period=SRS_PERIOD,
                measure=measure,
                value=_number(_cell(row, column), label=column),
                unit=f"SRS indicator as published; {label}",
                lineage=lineage,
            )
            if obs.observation_id in seen:
                obs = obs.model_copy(
                    update={"observation_id": f"{obs.observation_id}-{index}"}
                )
            seen.add(obs.observation_id)
            out.append(obs)
    return tuple(out)


def _map_table8(
    rows: list[dict[str, str]],
    *,
    series_id: str,
    citation_id: str,
    caveat_id: str,
    frame: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        name = _cell(row, "geography")
        year = _cell(row, "year")
        if name == "" or year == "":
            continue
        geo = _printed_ref(name, frame)
        for column, sector in TABLE8_MEASURES:
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=sector,
                    period=year,
                    measure="projected-population",
                    value=_number(_cell(row, column), label=column),
                    unit="thousands ('000); projected; 1st March",
                    lineage=lineage,
                )
            )
    return tuple(out)


_FAMILY = {
    "census-pca-tru": _map_pca,
    "census-a02-decadal": _map_a02,
    "srs-bulletin-rates": _map_bulletin,
    "srs-table3-indicators": _map_table3,
    "ncp-table8-projections": _map_table8,
}


def _wrap(
    mapper_id: str,
    fn: Any,
) -> None:
    def map_rows(
        rows: list[dict[str, str]],
        series_id: str,
        citation_id: str,
        caveat_id: str,
        geography: GeographyVintage,
        lineage: ObservationLineage,
    ) -> tuple[Observation, ...]:
        observations = fn(
            rows,
            series_id=series_id,
            citation_id=citation_id,
            caveat_id=caveat_id,
            frame=geography,
            lineage=lineage,
        )
        if not observations:
            raise PipelineError(f"{series_id} produced no observations")
        return tuple(observations)

    register_mapper(mapper_id, MapperSpec(map_rows=map_rows, version=MAPPER_VERSION))


for _mapper_id, _fn in _FAMILY.items():
    _wrap(_mapper_id, _fn)


def map_c2_table(
    *,
    series_id: str,
    rows: list[dict[str, str]],
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    by_series = {
        SERIES_CENSUS_2011_PCA_SD: "census-pca-tru",
        SERIES_CENSUS_2011_A02_DECADAL: "census-a02-decadal",
        SERIES_SRS_BULLETIN_2024: "srs-bulletin-rates",
        SERIES_SRS_STATISTICAL_REPORT_2024: "srs-table3-indicators",
        SERIES_NCP_PROJECTIONS_2011_2036_TABLE8: "ncp-table8-projections",
    }
    mapper_id = by_series.get(series_id)
    if mapper_id is None:
        raise PipelineError(f"unknown C2 series_id: {series_id}")
    from prism.catalog.registry import MAPPERS

    return MAPPERS[mapper_id].map_rows(
        rows, series_id, citation_id, caveat_id, geography, lineage
    )
