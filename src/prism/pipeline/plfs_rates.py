"""Map PLFS state × sector × sex derived tables into a data vintage."""

from __future__ import annotations

import csv
import re
from pathlib import Path

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

MAPPER_VERSION = "plfs-observations-1.0.0"
PUBLISHED_SECTORS = frozenset({"rural", "urban", "rural + urban"})
PUBLISHED_SEX = frozenset({"male", "female", "person"})
_SLUG = re.compile(r"[^a-z0-9]+")
_WITHHELD = frozenset({".", "..", "...", "…", "-", "n.a.", "na", "n/a"})


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
    stripped = text.strip().replace(",", "")
    if stripped == "" or stripped.lower() in _WITHHELD:
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


def _geography_ref(name: str, frame: GeographyVintage) -> GeographyRef:
    code = _slug(name)
    expected = _names(frame).get(code)
    if expected is None:
        raise PipelineError(
            f"producer geography {name!r} (code {code!r}) is not in "
            f"{frame.frame_id}; not recoding"
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


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def map_plfs_state_sector_sex(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    if not citation_id or not caveat_id:
        raise PipelineError("citation_id and caveat_id are required")
    if not geography.geography_vintage:
        raise PipelineError("geography.geography_vintage is required")
    observations: list[Observation] = []
    for row in rows:
        name = _cell(row, "geography")
        sector = _cell(row, "sector")
        sex = _cell(row, "sex")
        measure = _cell(row, "measure")
        period = _cell(row, "reference_period")
        unit = _cell(row, "unit")
        age_group = _cell(row, "age_group")
        if name == "" or sector == "" or sex == "" or measure == "" or period == "":
            raise PipelineError(f"row missing required PLFS fields for {series_id}")
        if sector not in PUBLISHED_SECTORS:
            raise PipelineError(f"unpublished sector {sector!r}; not inventing")
        if sex not in PUBLISHED_SEX:
            raise PipelineError(f"unpublished sex {sex!r}; not inventing")
        if unit == "":
            raise PipelineError(f"missing unit for {series_id}")
        geo = _geography_ref(name, geography)
        value = _number(_cell(row, "value"), label="value")
        age_token = _slug(age_group, "no-age") if age_group else "no-age"
        obs_id = (
            f"obs-{series_id}-{geo.code}-{_slug(sector)}-{_slug(period, 'period')}"
            f"-{_slug(measure)}-{_slug(sex)}-{age_token}"
        )
        observations.append(
            Observation(
                observation_id=obs_id,
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
        )
    if not observations:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(observations)


register_mapper(
    "plfs-state-sector-sex",
    MapperSpec(map_rows=map_plfs_state_sector_sex, version=MAPPER_VERSION),
)

__all__ = [
    "MAPPER_VERSION",
    "map_plfs_state_sector_sex",
]
