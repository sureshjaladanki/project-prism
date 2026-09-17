"""Observation Parquet codec. Columns are the locked schema fields, flattened."""

from __future__ import annotations

import io

import pyarrow as pa  # type: ignore[import-untyped]
import pyarrow.parquet as pq  # type: ignore[import-untyped]

from prism.schema import (
    OBSERVATION_PARQUET_COLUMNS,
    CodeSystem,
    GeographyRef,
    Observation,
    ObservationLineage,
    ObservationStatus,
)

_PARQUET_SCHEMA = pa.schema(
    [
        ("observation_id", pa.string()),
        ("series_id", pa.string()),
        ("citation_id", pa.string()),
        ("caveat_id", pa.string()),
        ("geography_code", pa.string()),
        ("geography_vintage", pa.string()),
        ("geography_code_system", pa.string()),
        ("sector", pa.string()),
        ("reference_period", pa.string()),
        ("value", pa.float64()),
        ("unit", pa.string()),
        ("status", pa.string()),
        ("lineage_raw_path", pa.string()),
        ("lineage_derived_path", pa.string()),
        ("lineage_checksum", pa.string()),
    ]
)


class ObservationParquetError(ValueError):
    pass


def observations_to_parquet(observations: tuple[Observation, ...]) -> bytes:
    if not observations:
        raise ObservationParquetError("a series must have at least one observation")
    ordered = tuple(sorted(observations, key=lambda item: item.observation_id))
    ids = [item.observation_id for item in ordered]
    if len(set(ids)) != len(ids):
        raise ObservationParquetError("observation_id must be unique within a series")
    columns: dict[str, list[object]] = {name: [] for name in OBSERVATION_PARQUET_COLUMNS}
    for item in ordered:
        if not item.citation_id or not item.caveat_id:
            raise ObservationParquetError("citation_id and caveat_id are required")
        if not item.geography.geography_vintage:
            raise ObservationParquetError("geography.geography_vintage is required")
        columns["observation_id"].append(item.observation_id)
        columns["series_id"].append(item.series_id)
        columns["citation_id"].append(item.citation_id)
        columns["caveat_id"].append(item.caveat_id)
        columns["geography_code"].append(item.geography.code)
        columns["geography_vintage"].append(item.geography.geography_vintage)
        columns["geography_code_system"].append(item.geography.code_system.value)
        columns["sector"].append(item.sector)
        columns["reference_period"].append(item.reference_period)
        columns["value"].append(item.value)
        columns["unit"].append(item.unit)
        columns["status"].append(item.status.value)
        columns["lineage_raw_path"].append(item.lineage.raw_path)
        columns["lineage_derived_path"].append(item.lineage.derived_path)
        columns["lineage_checksum"].append(item.lineage.checksum)
    table = pa.table(columns, schema=_PARQUET_SCHEMA)
    buffer = io.BytesIO()
    pq.write_table(
        table,
        buffer,
        compression="none",
        use_dictionary=False,
        write_statistics=False,
        store_schema=True,
    )
    return buffer.getvalue()


def observations_from_parquet(payload: bytes) -> tuple[Observation, ...]:
    table = pq.read_table(io.BytesIO(payload), schema=_PARQUET_SCHEMA)
    names = tuple(table.column_names)
    if names != OBSERVATION_PARQUET_COLUMNS:
        raise ObservationParquetError(
            "unexpected parquet columns: " + ", ".join(names)
        )
    observations: list[Observation] = []
    for row in table.to_pylist():
        observations.append(
            Observation(
                observation_id=row["observation_id"],
                series_id=row["series_id"],
                citation_id=row["citation_id"],
                caveat_id=row["caveat_id"],
                geography=GeographyRef(
                    code=row["geography_code"],
                    geography_vintage=row["geography_vintage"],
                    code_system=CodeSystem(row["geography_code_system"]),
                ),
                sector=row["sector"],
                reference_period=row["reference_period"],
                value=row["value"],
                unit=row["unit"],
                status=ObservationStatus(row["status"]),
                lineage=ObservationLineage(
                    raw_path=row["lineage_raw_path"],
                    derived_path=row["lineage_derived_path"],
                    checksum=row["lineage_checksum"],
                ),
            )
        )
    return tuple(observations)
