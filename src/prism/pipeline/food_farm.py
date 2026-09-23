"""Map DES / DFPD / FCI foodgrain derived tables into a data vintage.

Family A (production / procurement / stocks) and Family B (PDS / NFSA delivery)
stay as separate series — never one merged food-security measure.
"""

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

MAPPER_VERSION = "c8-food-farm-1.0.0"
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
    if stripped.lower() in {".", "..", "...", "…", "n.a.", "na", "n/a", "@", "$"}:
        return None
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
    return Observation(
        observation_id=(
            f"obs-{series_id}-{geo.code}-{_slug(sector)}-{_slug(period)}-{measure}"
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


def map_ae_fe_all_india(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    geo = _printed_ref("All India", geography)
    out: list[Observation] = []
    for row in rows:
        crop = _cell(row, "crop")
        season = _cell(row, "season")
        year = _cell(row, "year")
        estimate = _cell(row, "estimate_round")
        if not crop or not season or not year:
            raise PipelineError(f"{series_id} missing crop/season/year")
        value = _number(_cell(row, "production_lakh_tonnes"), label="production")
        out.append(
            _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector=f"{crop}|{season}|{estimate}",
                period=year,
                measure="production",
                value=value,
                unit="lakh tonnes",
                lineage=lineage,
            )
        )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_apy_state(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        state = _cell(row, "state")
        crop = _cell(row, "crop")
        season = _cell(row, "season")
        year = _cell(row, "year")
        if not state or not crop or not season or not year:
            raise PipelineError(f"{series_id} missing state/crop/season/year")
        geo = _printed_ref(state, geography)
        sector = f"{crop}|{season}"
        for column, measure, unit in (
            ("area_thousand_ha", "area", "thousand ha"),
            ("production_thousand_tonnes", "production", "thousand tonnes"),
            ("yield_kg_ha", "yield", "kg/ha"),
        ):
            value = _number(_cell(row, column), label=measure)
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=sector,
                    period=year,
                    measure=measure,
                    value=value,
                    unit=unit,
                    lineage=lineage,
                )
            )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_bulletin_procurement(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        state = _cell(row, "state")
        season = _cell(row, "marketing_season")
        commodity = _cell(row, "commodity")
        if not state or not season or not commodity:
            raise PipelineError(f"{series_id} missing state/season/commodity")
        geo = _printed_ref(state, geography)
        value = _number(_cell(row, "procurement_lmt"), label="procurement")
        out.append(
            _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector=commodity,
                period=season,
                measure="procurement",
                value=value,
                unit="LMT",
                lineage=lineage,
            )
        )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_bulletin_allocation_offtake(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    """Allocation and offtake stay separate measures — never one merged column."""

    out: list[Observation] = []
    for row in rows:
        state = _cell(row, "state")
        period = _cell(row, "period")
        scheme = _cell(row, "scheme")
        if not state or not period or not scheme:
            raise PipelineError(f"{series_id} missing state/period/scheme")
        geo = _printed_ref(state, geography)
        for column, measure in (
            ("allocation_lmt", "allocation"),
            ("offtake_lmt", "offtake"),
        ):
            value = _number(_cell(row, column), label=measure)
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector=scheme,
                    period=period,
                    measure=measure,
                    value=value,
                    unit="LMT",
                    lineage=lineage,
                )
            )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_bulletin_nfsa_coverage_fps(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    for row in rows:
        state = _cell(row, "state")
        table = _cell(row, "table")
        measure = _cell(row, "measure")
        if not state or not table or not measure:
            raise PipelineError(f"{series_id} missing state/table/measure")
        geo = _printed_ref(state, geography)
        value = _number(_cell(row, "value"), label=measure)
        unit = "shops" if measure == "fair_price_shops" else "lakh"
        out.append(
            _obs(
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geo=geo,
                sector=table,
                period="2026-08",
                measure=measure,
                value=value,
                unit=unit,
                lineage=lineage,
            )
        )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_central_pool_stocks(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    out: list[Observation] = []
    period = "2026-09-01"
    for row in rows:
        region = _cell(row, "region")
        if not region:
            raise PipelineError(f"{series_id} missing region")
        geo = _printed_ref(region, geography)
        for column, measure in (
            ("rice_lmt", "rice"),
            ("wheat_lmt", "wheat"),
            ("total_lmt", "total"),
        ):
            value = _number(_cell(row, column), label=measure)
            out.append(
                _obs(
                    series_id=series_id,
                    citation_id=citation_id,
                    caveat_id=caveat_id,
                    geo=geo,
                    sector="central-pool",
                    period=period,
                    measure=measure,
                    value=value,
                    unit="LMT",
                    lineage=lineage,
                )
            )
    if not out:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(out)


def map_named_hole_food(
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
    hole_unit = "not a table"
    return (
        Observation(
            observation_id=(
                f"obs-{series_id}-{unit.code}-companion-{_slug(source_vintage)}-unknown"
            ),
            series_id=series_id,
            citation_id=citation_id,
            caveat_id=caveat_id,
            geography=GeographyRef(
                code=unit.code,
                geography_vintage=geography.geography_vintage,
                code_system=geography.code_system,
            ),
            sector="companion",
            reference_period=source_vintage,
            value=None,
            unit=hole_unit,
            denomination=denomination_from_unit(hole_unit),
            status=ObservationStatus.unknown,
            lineage=lineage,
        ),
    )


register_mapper(
    "food-farm/ae-fe-all-india",
    MapperSpec(map_rows=map_ae_fe_all_india, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/apy-state",
    MapperSpec(map_rows=map_apy_state, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/bulletin-procurement",
    MapperSpec(map_rows=map_bulletin_procurement, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/bulletin-allocation-offtake",
    MapperSpec(map_rows=map_bulletin_allocation_offtake, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/bulletin-nfsa-coverage-fps",
    MapperSpec(map_rows=map_bulletin_nfsa_coverage_fps, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/central-pool-stocks",
    MapperSpec(map_rows=map_central_pool_stocks, version=MAPPER_VERSION),
)
register_mapper(
    "food-farm/named-hole",
    MapperSpec(map_rows=map_named_hole_food, version=MAPPER_VERSION),
)
