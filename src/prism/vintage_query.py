"""DuckDB reads of exactly one data vintage. Do not join a second vintage."""

from __future__ import annotations

from pathlib import Path

import duckdb

from prism.observation_parquet import ObservationParquetError
from prism.paths import OBSERVATIONS_FILENAME, series_dir, vintage_dir
from prism.schema import (
    CodeSystem,
    Completeness,
    Denomination,
    DenominationMagnitude,
    DenominationMeasure,
    GeographyRef,
    Observation,
    ObservationLineage,
    ObservationStatus,
)
from prism.vintage_store import load_manifest


class VintageQueryError(ValueError):
    pass


def connect_vintage(data_root: Path, vintage_id: str) -> duckdb.DuckDBPyConnection:
    if not vintage_dir(data_root, vintage_id).exists():
        raise VintageQueryError(f"vintage {vintage_id} does not exist")
    manifest = load_manifest(data_root, vintage_id)
    if manifest.completeness is Completeness.failed:
        raise VintageQueryError("a failed vintage cannot be rendered")
    if manifest.vintage_id != vintage_id:
        raise VintageQueryError("manifest vintage_id does not match the directory")
    paths = [
        (
            series_dir(data_root, vintage_id, entry.series_id) / OBSERVATIONS_FILENAME
        ).resolve()
        for entry in manifest.series
    ]
    missing = [path.as_posix() for path in paths if not path.exists()]
    if missing:
        raise VintageQueryError("missing observations parquet: " + ", ".join(missing))

    connection = duckdb.connect(database=":memory:")
    connection.read_parquet([path.as_posix() for path in paths]).to_table(
        "observations"
    )
    connection.execute("ALTER TABLE observations ADD COLUMN bound_vintage_id VARCHAR")
    connection.execute("UPDATE observations SET bound_vintage_id = ?", [vintage_id])
    ids = connection.execute(
        "SELECT DISTINCT bound_vintage_id FROM observations"
    ).fetchall()
    if ids != [(vintage_id,)]:
        raise VintageQueryError("DuckDB connection mixed more than one vintage_id")
    return connection


def observations_matching(
    connection: duckdb.DuckDBPyConnection,
    vintage_id: str,
    *,
    series_id: str,
    geography_codes: tuple[str, ...],
    geography_vintage: str,
    code_system: CodeSystem,
    sectors: tuple[str, ...],
    reference_periods: tuple[str, ...],
    units: tuple[str, ...],
    statuses: tuple[ObservationStatus, ...],
) -> tuple[Observation, ...]:
    if (
        not geography_codes
        or not sectors
        or not reference_periods
        or not units
        or not statuses
    ):
        raise VintageQueryError("collection query is missing a bound dimension")
    placeholders = {
        "geography": ", ".join("?" for _ in geography_codes),
        "sector": ", ".join("?" for _ in sectors),
        "period": ", ".join("?" for _ in reference_periods),
        "unit": ", ".join("?" for _ in units),
        "status": ", ".join("?" for _ in statuses),
    }
    sql = f"""
        SELECT *
        FROM observations
        WHERE bound_vintage_id = ?
          AND series_id = ?
          AND geography_code IN ({placeholders["geography"]})
          AND geography_vintage = ?
          AND geography_code_system = ?
          AND sector IN ({placeholders["sector"]})
          AND reference_period IN ({placeholders["period"]})
          AND unit IN ({placeholders["unit"]})
          AND status IN ({placeholders["status"]})
    """
    params: list[object] = [
        vintage_id,
        series_id,
        *geography_codes,
        geography_vintage,
        code_system.value,
        *sectors,
        *reference_periods,
        *units,
        *[status.value for status in statuses],
    ]
    return _fetch_observations(connection, sql, params)


def observations_in_period_range(
    connection: duckdb.DuckDBPyConnection,
    vintage_id: str,
    *,
    series_id: str,
    geography_code: str,
    geography_vintage: str,
    code_system: CodeSystem,
    sector: str,
    period_from: str,
    period_to: str,
    unit: str,
    statuses: tuple[ObservationStatus, ...],
) -> tuple[Observation, ...]:
    status_sql = ", ".join("?" for _ in statuses)
    sql = f"""
        SELECT *
        FROM observations
        WHERE bound_vintage_id = ?
          AND series_id = ?
          AND geography_code = ?
          AND geography_vintage = ?
          AND geography_code_system = ?
          AND sector = ?
          AND reference_period >= ?
          AND reference_period <= ?
          AND unit = ?
          AND status IN ({status_sql})
        ORDER BY reference_period
    """
    params: list[object] = [
        vintage_id,
        series_id,
        geography_code,
        geography_vintage,
        code_system.value,
        sector,
        period_from,
        period_to,
        unit,
        *[status.value for status in statuses],
    ]
    return _fetch_observations(connection, sql, params)


def _fetch_observations(
    connection: duckdb.DuckDBPyConnection,
    sql: str,
    params: list[object],
) -> tuple[Observation, ...]:
    result = connection.execute(sql, params)
    if result.description is None:
        raise VintageQueryError("observation query returned no description")
    columns = [column[0] for column in result.description]
    observations: list[Observation] = []
    for tup in result.fetchall():
        row = dict(zip(columns, tup, strict=True))
        observations.append(_observation_from_row(row))
    return tuple(observations)


def _observation_from_row(row: dict[str, object]) -> Observation:
    from prism.citizen_projection import denomination_from_unit

    citation_id = _text(row, "citation_id")
    caveat_id = _text(row, "caveat_id")
    geography_vintage = _text(row, "geography_vintage")
    if not citation_id:
        raise ObservationParquetError("citation_id is required")
    if not caveat_id:
        raise ObservationParquetError("caveat_id is required")
    if not geography_vintage:
        raise ObservationParquetError("geography.geography_vintage is required")
    value = row["value"]
    if value is not None and not isinstance(value, int | float):
        raise VintageQueryError(f"observation value is not a number: {value!r}")
    unit = _text(row, "unit")
    mag = row.get("denomination_magnitude")
    measure = row.get("denomination_measure")
    if isinstance(mag, str) and mag != "" and isinstance(measure, str) and measure != "":
        denomination = Denomination(
            magnitude=DenominationMagnitude(mag),
            measure=DenominationMeasure(measure),
        )
    else:
        # Prior vintages without denomination columns: derive at read; new writes carry it.
        denomination = denomination_from_unit(unit)
    return Observation(
        observation_id=_text(row, "observation_id"),
        series_id=_text(row, "series_id"),
        citation_id=citation_id,
        caveat_id=caveat_id,
        geography=GeographyRef(
            code=_text(row, "geography_code"),
            geography_vintage=geography_vintage,
            code_system=CodeSystem(_text(row, "geography_code_system")),
        ),
        sector=_text(row, "sector"),
        reference_period=_text(row, "reference_period"),
        value=None if value is None else float(value),
        unit=unit,
        denomination=denomination,
        status=ObservationStatus(_text(row, "status")),
        lineage=ObservationLineage(
            raw_path=_text(row, "lineage_raw_path"),
            derived_path=_text(row, "lineage_derived_path"),
            checksum=_text(row, "lineage_checksum"),
        ),
    )


def _text(row: dict[str, object], key: str) -> str:
    value = row[key]
    if not isinstance(value, str) or value == "":
        raise VintageQueryError(f"observation column {key} is empty")
    return value
