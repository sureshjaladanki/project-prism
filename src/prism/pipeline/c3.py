"""Map C3 derived tables into a data vintage. Does not fetch and does not publish."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from prism.catalog.registry import MapperFn, MapperSpec, register_mapper
from prism.pipeline.errors import PipelineError
from prism.schema import (
    CodeSystem,
    GeographyRef,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
)

MAPPER_VERSION = "c3-observations-1.1.0"
SECTOR_UNION = "Union"
UNIT_CRORE = "₹ crore"
_SLUG = re.compile(r"[^a-z0-9]+")
_MINUS_PREFIXES = frozenset({"\ufffd", "\u2212", "\u2013", "\u2014"})


@dataclass(frozen=True)
class MeasureColumn:
    column: str
    reference_period: str
    unit: str


_FOUR_BUDGET = (
    MeasureColumn("actuals_2024_2025", "actuals-2024-2025", UNIT_CRORE),
    MeasureColumn("budget_2025_2026", "budget-2025-2026", UNIT_CRORE),
    MeasureColumn("revised_2025_2026", "revised-2025-2026", UNIT_CRORE),
    MeasureColumn("budget_2026_2027", "budget-2026-2027", UNIT_CRORE),
)
_STAT1 = tuple(
    MeasureColumn(f"{year}_{split}", f"{year.replace('_', '-')}-{split}", UNIT_CRORE)
    for year in (
        "actuals_2024_2025",
        "budget_2025_2026",
        "revised_2025_2026",
        "budget_2026_2027",
    )
    for split in ("revenue", "capital", "total")
)
_ANNEX1 = (
    MeasureColumn("actual_2017_18", "actual-2017-18", UNIT_CRORE),
    MeasureColumn("actual_2018_19", "actual-2018-19", UNIT_CRORE),
    MeasureColumn("actual_2019_20", "actual-2019-20", UNIT_CRORE),
    MeasureColumn("actual_2020_21", "actual-2020-21", UNIT_CRORE),
    MeasureColumn("actual_2021_22", "actual-2021-22", UNIT_CRORE),
    MeasureColumn("actual_2022_23", "actual-2022-23", UNIT_CRORE),
    MeasureColumn("actual_2023_24", "actual-2023-24", UNIT_CRORE),
    MeasureColumn("actual_2024_25", "actual-2024-25", UNIT_CRORE),
    MeasureColumn("re_2025_26", "re-2025-26", UNIT_CRORE),
    MeasureColumn("be_2026_27", "be-2026-27", UNIT_CRORE),
)
_LIABILITIES = (
    MeasureColumn("end_1950_51", "end-1950-51", UNIT_CRORE),
    MeasureColumn("end_2021_2022", "end-2021-2022", UNIT_CRORE),
    MeasureColumn("end_2022_2023", "end-2022-2023", UNIT_CRORE),
    MeasureColumn("end_2023_24", "end-2023-24", UNIT_CRORE),
    MeasureColumn("end_2024_25", "end-2024-25", UNIT_CRORE),
    MeasureColumn("revised_2025_26", "revised-2025-26", UNIT_CRORE),
    MeasureColumn("budget_2026_27", "budget-2026-27", UNIT_CRORE),
)
_FA = (
    MeasureColumn("actuals_2024_2025", "actuals-2024-2025", UNIT_CRORE),
    MeasureColumn("actuals_2023_2024", "actuals-2023-2024", UNIT_CRORE),
)
_CGA_MONTHLY = (
    MeasureColumn("be_2026_2027", "budget-2026-2027", UNIT_CRORE),
    MeasureColumn("actuals_upto_july_2026", "actuals-upto-july-2026", UNIT_CRORE),
    MeasureColumn("pct_current", "pct-of-be-current", "% of BE"),
    MeasureColumn("pct_coppy", "pct-of-be-coppy", "% of BE (COPPY)"),
)

MEASURE_SETS: dict[str, tuple[MeasureColumn, ...]] = {
    "budget-four-year": _FOUR_BUDGET,
    "annex1": _ANNEX1,
    "stat1": _STAT1,
    "liabilities": _LIABILITIES,
    "cga-monthly": _CGA_MONTHLY,
    "finance-accounts": _FA,
}


def _cell(row: dict[str, str], name: str) -> str:
    value = row.get(name)
    if value is None:
        return ""
    return value.strip()


def _number(text: str, *, label: str) -> float | None:
    stripped = text.strip().replace(",", "").replace("*", "")
    if stripped == "":
        return None
    if stripped.endswith("%"):
        stripped = stripped[:-1].strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        stripped = stripped[1:-1].replace("%", "").strip()
    if stripped[:1] in _MINUS_PREFIXES:
        # Finance Accounts PDF minus often lands as U+FFFD / unicode dash.
        stripped = "-" + stripped[1:]
    if stripped == "":
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise PipelineError(f"unparseable {label}: {text!r}") from exc


def _slug(text: str, fallback: str) -> str:
    ascii_only = text.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG.sub("-", ascii_only.lower()).strip("-")
    if slug == "":
        return fallback
    return slug[:80]


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def map_c3_table(
    *,
    series_id: str,
    rows: list[dict[str, str]],
    citation_id: str,
    caveat_id: str,
    geography_code: str,
    geography_vintage: str,
    code_system: CodeSystem,
    lineage: ObservationLineage,
    measures: tuple[MeasureColumn, ...] | None = None,
) -> tuple[Observation, ...]:
    if measures is None:
        from prism.catalog import default_catalog

        mapper_id = default_catalog().series(series_id).mapper_id
        _, key = mapper_id.split("/", 1)
        measures = MEASURE_SETS[key]
    if not rows:
        raise PipelineError(f"{series_id} produced no observations")
    missing = [measure.column for measure in measures if measure.column not in rows[0]]
    if missing:
        raise PipelineError(f"{series_id} missing columns: {', '.join(missing)}")
    observations: list[Observation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = _cell(row, "line_label")
        if label == "":
            continue
        slug = _slug(label, f"row-{index}")
        geo = GeographyRef(
            code=geography_code,
            geography_vintage=geography_vintage,
            code_system=code_system,
        )
        for measure in measures:
            value = _number(_cell(row, measure.column), label=measure.column)
            obs_id = f"obs-{series_id}-{geo.code}-{measure.reference_period}-{slug}"
            if obs_id in seen:
                obs_id = f"{obs_id}-{index}"
            seen.add(obs_id)
            observations.append(
                Observation(
                    observation_id=obs_id,
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geography=geo,
                    sector=SECTOR_UNION,
                    reference_period=measure.reference_period,
                    value=value,
                    unit=f"{measure.unit}; {label}",
                    status=ObservationStatus.unknown
                    if value is None
                    else ObservationStatus.value,
                    lineage=lineage,
                )
            )
    if not observations:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(observations)


def map_named_hole_union(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    del rows
    from prism.catalog import default_catalog

    source_vintage = default_catalog().series(series_id).source_vintage
    unit = geography.units_included[0]
    return (
        Observation(
            observation_id=(
                f"obs-{series_id}-{unit.code}-union-{source_vintage}-unknown"
            ),
            series_id=series_id,
            citation_id=citation_id,
            caveat_id=caveat_id,
            geography=GeographyRef(
                code=unit.code,
                geography_vintage=geography.geography_vintage,
                code_system=geography.code_system,
            ),
            sector=SECTOR_UNION,
            reference_period=source_vintage,
            value=None,
            unit="not a table",
            status=ObservationStatus.unknown,
            lineage=lineage,
        ),
    )


def _wide_map(set_name: str) -> MapperFn:
    columns = MEASURE_SETS[set_name]

    def map_rows(
        rows: list[dict[str, str]],
        series_id: str,
        citation_id: str,
        caveat_id: str,
        geography: GeographyVintage,
        lineage: ObservationLineage,
    ) -> tuple[Observation, ...]:
        unit = geography.units_included[0]
        return map_c3_table(
            series_id=series_id,
            rows=rows,
            citation_id=citation_id,
            caveat_id=caveat_id,
            geography_code=unit.code,
            geography_vintage=geography.geography_vintage,
            code_system=geography.code_system,
            lineage=lineage,
            measures=columns,
        )

    return map_rows


def _register_c3_mappers() -> None:
    for name in MEASURE_SETS:
        register_mapper(
            f"wide-measure-columns/{name}",
            MapperSpec(map_rows=_wide_map(name), version=MAPPER_VERSION),
        )
    register_mapper(
        "named-hole-union",
        MapperSpec(map_rows=map_named_hole_union, version=MAPPER_VERSION),
    )


_register_c3_mappers()
