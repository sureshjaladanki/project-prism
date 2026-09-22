"""Map state × sector × period derived tables into a data vintage."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from prism.catalog.registry import MapperSpec, register_mapper
from prism.citizen_projection import denomination_from_unit
from prism.pipeline.errors import PipelineError
from prism.refresh import (
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
)
from prism.schema import (
    GeographyRef,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
)

MAPPER_VERSION = "c1-observations-1.0.0"
UNIT_INDEX = "index (Base 2024=100)"
UNIT_INFLATION = "inflation (%)"
PUBLISHED_SECTORS = frozenset({"Rural", "Urban", "Combined"})
MEASURE_INDEX = "index"
MEASURE_INFLATION = "inflation"
MONTH_NUMBERS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
    "1": "01",
    "01": "01",
    "2": "02",
    "02": "02",
    "3": "03",
    "03": "03",
    "4": "04",
    "04": "04",
    "5": "05",
    "05": "05",
    "6": "06",
    "06": "06",
    "7": "07",
    "07": "07",
    "8": "08",
    "08": "08",
    "9": "09",
    "09": "09",
    "10": "10",
    "11": "11",
    "12": "12",
}


@dataclass(frozen=True)
class Classifier:
    kind: str
    code: str

    def token(self) -> str:
        if self.kind in {"general", "cfpi"}:
            return self.kind
        prefix = "div" if self.kind == "division" else "grp"
        return f"{prefix}-{self.code}"

    def unit_for(self, measure_unit: str) -> str:
        if self.kind in {"general", "cfpi"}:
            return measure_unit
        label = "Division code" if self.kind == "division" else "Group code"
        return f"{measure_unit}; {label} {self.code}"


def _cell(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value is None:
            continue
        text = value.strip()
        if text != "":
            return text
    return ""


def _state_code(value: str) -> str:
    if value.isdigit() and len(value) <= 2:
        return value.zfill(2)
    return value


def _month_number(value: str) -> str:
    key = value.strip().lower()
    number = MONTH_NUMBERS.get(key)
    if number is None:
        raise PipelineError(f"unrecognised month: {value!r}")
    return number


def _reference_period(year: str, month: str) -> str:
    year_text = year.strip()
    if not year_text.isdigit() or len(year_text) != 4:
        raise PipelineError(f"unrecognised year: {year!r}")
    return f"{year_text}-{_month_number(month)}"


def _number(text: str, *, label: str) -> float | None:
    if text == "" or text.strip().lower() in {".", "..", "...", "…", "-", "n.a.", "na"}:
        return None
    try:
        return float(text)
    except ValueError as exc:
        raise PipelineError(f"unparseable {label}: {text!r}") from exc


def _producer_status(text: str) -> str:
    if text == "":
        return ""
    if text in {"F", "P"}:
        return text
    raise PipelineError(f"unrecognised producer status: {text!r}")


def _observation_status(value: float | None) -> ObservationStatus:
    if value is None:
        return ObservationStatus.unknown
    return ObservationStatus.value


def _geography_ref(
    code: str,
    name: str,
    frame: GeographyVintage,
    names: dict[str, str],
) -> GeographyRef:
    expected = names.get(code)
    if expected is None:
        raise PipelineError(
            f"producer code {code!r} is not in {frame.frame_id}; not recoding"
        )
    if expected != name:
        raise PipelineError(
            f"producer name {name!r} for code {code} does not match frame "
            f"{expected!r}; not recoding"
        )
    if not frame.geography_vintage:
        raise PipelineError("geography.geography_vintage is required")
    return GeographyRef(
        code=code,
        geography_vintage=frame.geography_vintage,
        code_system=frame.code_system,
    )


def _observation_id(
    series_id: str,
    code: str,
    sector: str,
    period: str,
    classifier: Classifier,
    measure: str,
    producer_status: str,
) -> str:
    parts = [series_id, code, sector, period, classifier.token(), measure]
    if producer_status:
        parts.append(producer_status)
    return "obs-" + "-".join(parts)


def _classifier_for_row(series_id: str, row: dict[str, str]) -> Classifier:
    if series_id == SERIES_CPI_GENERAL_BASE_2024:
        return Classifier("general", "")
    if series_id == SERIES_CPI_CFPI_BASE_2024:
        group_code = _cell(row, "Group code")
        group_name = _cell(row, "Group Name")
        if group_code != "01.1" or group_name != "Food":
            raise PipelineError(
                "CFPI row is not Group Food 01.1; not substituting Division 01"
            )
        return Classifier("cfpi", "01.1")
    if series_id == SERIES_CPI_DIVISION_GROUP_BASE_2024:
        div_code = _cell(row, "Division code")
        grp_code = _cell(row, "Group code")
        if div_code and grp_code:
            raise PipelineError("row has both Division and Group codes; not stitching")
        if div_code:
            if div_code == "12":
                raise PipelineError(
                    "Division 12 is not a published series on this slice"
                )
            return Classifier("division", div_code)
        if grp_code:
            return Classifier("group", grp_code)
        raise PipelineError("row has neither Division nor Group code")
    if series_id == SERIES_CPI_BACK_SERIES_LINKED_BASE_2024:
        group = _cell(row, "Group")
        if group != "General":
            raise PipelineError(
                f"Card 4 Group {group!r} is not General; not stitching into Card 1"
            )
        return Classifier("general", "")
    raise PipelineError(f"unknown series_id: {series_id}")


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def map_derived_table(
    *,
    series_id: str,
    rows: list[dict[str, str]],
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    names: dict[str, str],
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    if not citation_id or not caveat_id:
        raise PipelineError("citation_id and caveat_id are required")
    if not geography.geography_vintage:
        raise PipelineError("geography.geography_vintage is required")
    observations: list[Observation] = []
    for row in rows:
        code = _state_code(_cell(row, "State Code", "State code"))
        name = _cell(row, "State Name", "State name")
        sector = _cell(row, "Sector")
        if code == "" or name == "":
            raise PipelineError(f"row missing producer geography for {series_id}")
        if sector not in PUBLISHED_SECTORS:
            raise PipelineError(
                f"unpublished sector {sector!r}; not inventing Combined"
            )
        geo = _geography_ref(code, name, geography, names)
        period = _reference_period(
            _cell(row, "year", "Year"),
            _cell(row, "month", "Month"),
        )
        producer_status = _producer_status(_cell(row, "status"))
        classifier = _classifier_for_row(series_id, row)
        measures = (
            (
                MEASURE_INDEX,
                UNIT_INDEX,
                _number(_cell(row, "index", "Index"), label="index"),
            ),
            (
                MEASURE_INFLATION,
                UNIT_INFLATION,
                _number(
                    _cell(row, "inflation (%)", "Inflation (%)"), label="inflation"
                ),
            ),
        )
        for measure, measure_unit, value in measures:
            unit = classifier.unit_for(measure_unit)
            observations.append(
                Observation(
                    observation_id=_observation_id(
                        series_id,
                        geo.code,
                        sector,
                        period,
                        classifier,
                        measure,
                        producer_status,
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
            )
    if not observations:
        raise PipelineError(f"{series_id} produced no observations")
    return tuple(observations)


def map_state_sector_period(
    rows: list[dict[str, str]],
    series_id: str,
    citation_id: str,
    caveat_id: str,
    geography: GeographyVintage,
    lineage: ObservationLineage,
) -> tuple[Observation, ...]:
    names = {unit.code: unit.name_en for unit in geography.units_included}
    return map_derived_table(
        series_id=series_id,
        rows=rows,
        citation_id=citation_id,
        caveat_id=caveat_id,
        geography=geography,
        names=names,
        lineage=lineage,
    )


register_mapper(
    "state-sector-period",
    MapperSpec(map_rows=map_state_sector_period, version=MAPPER_VERSION),
)

__all__ = [
    "MAPPER_VERSION",
    "UNIT_INDEX",
    "UNIT_INFLATION",
    "PipelineError",
    "map_derived_table",
    "map_state_sector_period",
]
