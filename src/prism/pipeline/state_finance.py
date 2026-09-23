"""Map RBI / CAG state-finance derived tables into a data vintage."""

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

MAPPER_VERSION = "c5-observations-1.0.0"
SECTOR_TOTAL = "Total"
UNIT_CRORE = "₹ crore"
_SLUG = re.compile(r"[^a-z0-9]+")
_WITHHELD = frozenset(
    {"-", "–", "—", "..", "...", "…", ".", "n.a.", "na", "n/a"}
)
_MINUS_PREFIXES = frozenset({"\ufffd", "\u2212", "\u2013", "\u2014"})

MEASURE_COLUMNS = (
    ("accounts_2023_24", "accounts-2023-24"),
    ("re_2024_25", "re-2024-25"),
    ("be_2025_26", "be-2025-26"),
)


def _cell(row: dict[str, str], name: str) -> str:
    value = row.get(name)
    if value is None:
        return ""
    return value.strip()


def _slug(text: str, fallback: str) -> str:
    ascii_only = text.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG.sub("-", ascii_only.lower()).strip("-")
    if slug == "":
        return fallback
    return slug[:80]


def _number(text: str, *, label: str) -> float | None:
    stripped = text.strip().replace(",", "").replace("*", "")
    if stripped == "" or stripped.lower() in _WITHHELD:
        return None
    if set(stripped) <= {".", " "}:
        return None
    if stripped.endswith("%"):
        stripped = stripped[:-1].strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        stripped = "-" + stripped[1:-1].replace("%", "").strip()
    if stripped[:1] in _MINUS_PREFIXES:
        stripped = "-" + stripped[1:]
    if stripped == "":
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise PipelineError(f"unparseable {label}: {text!r}") from exc


def _names(frame: GeographyVintage) -> dict[str, str]:
    return {unit.code: unit.name_en for unit in frame.units_included}


def _ref(name: str, frame: GeographyVintage) -> GeographyRef:
    code = _slug(name, "unit")
    expected = _names(frame).get(code)
    if expected is None:
        raise PipelineError(
            f"producer geography {name!r} is not in {frame.frame_id}; not recoding"
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


def map_state_finance_rows(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    if not rows:
        raise PipelineError(f"{series_id} produced no observations")
    missing = [
        column
        for column, _period in MEASURE_COLUMNS
        if column not in rows[0]
    ]
    if missing:
        raise PipelineError(f"{series_id} missing columns: {', '.join(missing)}")
    observations: list[Observation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        geography_name = _cell(row, "geography")
        if geography_name == "":
            continue
        geo = _ref(geography_name, geography)
        label = _cell(row, "line_label") or "as published"
        slug = _slug(label, f"row-{index}")
        for column, period in MEASURE_COLUMNS:
            value = _number(_cell(row, column), label=column)
            obs_id = f"obs-{series_id}-{geo.code}-{period}-{slug}"
            if obs_id in seen:
                obs_id = f"{obs_id}-{index}"
            seen.add(obs_id)
            unit = f"{UNIT_CRORE}; {label}"
            observations.append(
                Observation(
                    observation_id=obs_id,
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geography=geo,
                    sector=SECTOR_TOTAL,
                    reference_period=period,
                    value=value,
                    unit=unit,
                    denomination=denomination_from_unit(unit),
                    status=ObservationStatus.unknown
                    if value is None
                    else ObservationStatus.value,
                    lineage=lineage,
                )
            )
    if not observations:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(observations)


register_mapper(
    "state-finance/geo-wide",
    MapperSpec(map_rows=map_state_finance_rows, version=MAPPER_VERSION),
)
