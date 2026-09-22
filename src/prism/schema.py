"""Portrait contract types. Construction fails if required ids are missing."""

from __future__ import annotations

import json
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonEmptyStr = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

NextRelease = date | Literal["unknown"]
ReleaseDate = date | Literal["unknown"]


class ContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class RefreshTrigger(StrEnum):
    schedule = "schedule"
    source_change = "source_change"
    on_demand = "on_demand"


class SourceChanged(StrEnum):
    yes = "yes"
    no = "no"
    first_retrieve = "first_retrieve"


class YesNo(StrEnum):
    yes = "yes"
    no = "no"


class Completeness(StrEnum):
    complete = "complete"
    failed = "failed"


class CodeSystem(StrEnum):
    lgd = "LGD"
    census = "census"
    producer_specific = "producer-specific"
    none = "none"


class ObservationStatus(StrEnum):
    value = "value"
    unknown = "unknown"
    withheld = "withheld"
    delayed = "delayed"
    withdrawn = "withdrawn"
    not_comparable = "not_comparable"
    series_break = "series_break"


class Series(ContractModel):
    series_id: NonEmptyStr
    producer: NonEmptyStr
    name: NonEmptyStr
    frequency: NonEmptyStr
    licence: NonEmptyStr


class Citation(ContractModel):
    citation_id: NonEmptyStr
    producer: NonEmptyStr
    series: NonEmptyStr
    id: NonEmptyStr
    reference_period: NonEmptyStr
    release_date: ReleaseDate
    url: NonEmptyStr
    geography_as_published: NonEmptyStr
    frequency: NonEmptyStr
    licence: NonEmptyStr
    next_release: NextRelease
    caveat_one_line: NonEmptyStr


class GeographyUnit(ContractModel):
    code: NonEmptyStr
    name_en: NonEmptyStr
    geography_vintage: NonEmptyStr


class GeographyRef(ContractModel):
    code: NonEmptyStr
    geography_vintage: NonEmptyStr
    code_system: CodeSystem


class GeographyVintage(ContractModel):
    frame_id: NonEmptyStr
    geography_vintage: NonEmptyStr
    code_system: CodeSystem
    frame: NonEmptyStr
    units_included: tuple[GeographyUnit, ...]
    units_missing: tuple[str, ...]
    breaks: NonEmptyStr
    crosswalk: NonEmptyStr

    @model_validator(mode="after")
    def units_carry_geography_vintage(self) -> Self:
        for unit in self.units_included:
            if unit.geography_vintage != self.geography_vintage:
                raise ValueError(
                    "each unit must store the same geography_vintage as the frame"
                )
        return self


NOT_PUBLISHED = "not published"


class DenominationMagnitude(StrEnum):
    ones = "ones"
    thousand = "thousand"
    lakh = "lakh"
    crore = "crore"


class DenominationMeasure(StrEnum):
    rupees = "rupees"
    persons = "persons"
    percent = "percent"
    rate = "rate"
    index = "index"
    count = "count"


class Denomination(ContractModel):
    """Producer magnitude paired with what is measured. Ingest does not normalise to ones."""

    magnitude: DenominationMagnitude
    measure: DenominationMeasure


class AxisToken(StrEnum):
    """Compact axis / chart token for a declared scale group. Empty string is none."""

    none = ""
    K = "K"
    L = "L"
    Cr = "Cr"
    L_Cr = "L Cr"


class ChangeDirection(StrEnum):
    higher = "higher"
    lower = "lower"
    unchanged = "unchanged"


class CaveatNote(ContractModel):
    caveat_id: NonEmptyStr
    concept: NonEmptyStr
    unit: NonEmptyStr
    population: NonEmptyStr
    reference_period: NonEmptyStr
    producer_definition: NonEmptyStr
    comparable_from: NonEmptyStr
    breaks: NonEmptyStr
    lags: NonEmptyStr
    disagrees_with: NonEmptyStr
    do_not: NonEmptyStr
    citizen_note: NonEmptyStr | None = None


class ObservationLineage(ContractModel):
    raw_path: NonEmptyStr
    derived_path: NonEmptyStr
    checksum: NonEmptyStr


class Observation(ContractModel):
    observation_id: NonEmptyStr
    series_id: NonEmptyStr
    citation_id: NonEmptyStr
    caveat_id: NonEmptyStr
    geography: GeographyRef
    sector: NonEmptyStr
    reference_period: NonEmptyStr
    value: float | None
    unit: NonEmptyStr
    denomination: Denomination
    status: ObservationStatus
    lineage: ObservationLineage

    @model_validator(mode="after")
    def value_status_holds(self) -> Self:
        if self.status is ObservationStatus.value and self.value is None:
            raise ValueError("status value requires a number; blank is not zero")
        return self


class SlotSelector(ContractModel):
    """What a template slot may bind. Never a numeral typed into the page."""

    series_id: NonEmptyStr
    geography_code: NonEmptyStr
    geography_vintage: NonEmptyStr
    code_system: CodeSystem
    sector: NonEmptyStr
    reference_period: NonEmptyStr
    unit: NonEmptyStr
    status: ObservationStatus


class TemplateSlot(ContractModel):
    slot_id: NonEmptyStr
    selector: SlotSelector


class Template(ContractModel):
    template_id: NonEmptyStr
    slots: tuple[TemplateSlot, ...]


class CitizenCite(ContractModel):
    """Page-facing citation. Built at bind; not stored as a vintage record."""

    producer: NonEmptyStr
    url: NonEmptyStr
    series: NonEmptyStr
    reference_period: NonEmptyStr
    released: NonEmptyStr
    caveat: NonEmptyStr


class CitizenMethod(ContractModel):
    """One method block per page. Desk fields including do_not never appear."""

    what_it_counts: NonEmptyStr
    coverage: NonEmptyStr
    break_note: NonEmptyStr | None = None
    lag_note: NonEmptyStr | None = None


class CitizenNumber(ContractModel):
    """Bind-time citizen figure. Record value/unit/denomination stay on the observation."""

    canonical_value: float | None
    measure: DenominationMeasure
    text: NonEmptyStr
    chart_value: float | None
    axis_label: str
    status: ObservationStatus

    @model_validator(mode="after")
    def status_owns_the_hole(self) -> Self:
        published = self.status is ObservationStatus.value
        if published:
            if self.canonical_value is None:
                raise ValueError("status value requires canonical_value")
            if self.chart_value is None:
                raise ValueError("status value requires chart_value")
            return self
        if self.chart_value is not None:
            raise ValueError("non-published status requires chart_value null")
        if self.text != NOT_PUBLISHED:
            raise ValueError('gap text must be "not published"')
        return self


class CitizenChange(ContractModel):
    """Bind-time movement between two observations of the same series in one vintage."""

    current: CitizenNumber
    prior: CitizenNumber
    prior_period: NonEmptyStr
    direction: ChangeDirection
    difference: NonEmptyStr
    citation_id: NonEmptyStr


class CitizenGeography(ContractModel):
    """Reserved for /{sleeve}/{slice}/{geo}. geography_vintage stays on the vintage."""

    geography_label: NonEmptyStr
    geography_slug: NonEmptyStr


class ServedObservation(ContractModel):
    """Charts and APIs take this. A bare float is not a served observation."""

    observation: Observation
    citation: Citation
    caveat: CaveatNote

    @model_validator(mode="after")
    def cards_match_observation(self) -> Self:
        if self.observation.citation_id != self.citation.citation_id:
            raise ValueError("served observation citation_id does not match the card")
        if self.observation.caveat_id != self.caveat.caveat_id:
            raise ValueError("served observation caveat_id does not match the note")
        return self


class LineageRecord(ContractModel):
    """Ingest output. Refresh reads source_changed; Pipeline reads the rest."""

    raw_path: NonEmptyStr
    derived_path: NonEmptyStr
    checksum: NonEmptyStr
    retrieved_at: NonEmptyStr
    parser: NonEmptyStr
    citation_id: NonEmptyStr
    row_count: int = Field(ge=0)
    nulls: NonEmptyStr
    source_changed: SourceChanged
    lineage_ok: YesNo
    flags: NonEmptyStr


class SeriesManifestEntry(ContractModel):
    producer: NonEmptyStr
    series_id: NonEmptyStr
    source_vintage: NonEmptyStr
    raw_checksum: NonEmptyStr
    parser_version: NonEmptyStr
    lineage_ok: YesNo
    geography_vintage: NonEmptyStr
    geography_frame_id: NonEmptyStr
    payload_checksum: NonEmptyStr
    reused: YesNo
    caveat_id: NonEmptyStr
    mapper_version: NonEmptyStr


class InputManifest(ContractModel):
    """Hashed into vintage_id. Does not include vintage_id or completeness."""

    created_at: datetime
    trigger: RefreshTrigger
    series: tuple[SeriesManifestEntry, ...]


class VintageManifest(ContractModel):
    vintage_id: NonEmptyStr
    created_at: datetime
    trigger: RefreshTrigger
    series: tuple[SeriesManifestEntry, ...]
    completeness: Completeness


OBSERVATION_PARQUET_COLUMNS: tuple[str, ...] = (
    "observation_id",
    "series_id",
    "citation_id",
    "caveat_id",
    "geography_code",
    "geography_vintage",
    "geography_code_system",
    "sector",
    "reference_period",
    "value",
    "unit",
    "denomination_magnitude",
    "denomination_measure",
    "status",
    "lineage_raw_path",
    "lineage_derived_path",
    "lineage_checksum",
)


def canonical_json_bytes(model: ContractModel) -> bytes:
    return json.dumps(
        model.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def contract_json_schema() -> dict[str, object]:
    """Source for generated TypeScript later. Do not hand-maintain a parallel schema."""

    return {
        "Series": Series.model_json_schema(),
        "Citation": Citation.model_json_schema(),
        "CaveatNote": CaveatNote.model_json_schema(),
        "GeographyRef": GeographyRef.model_json_schema(),
        "GeographyVintage": GeographyVintage.model_json_schema(),
        "Observation": Observation.model_json_schema(),
        "SlotSelector": SlotSelector.model_json_schema(),
        "Template": Template.model_json_schema(),
        "ServedObservation": ServedObservation.model_json_schema(),
        "CitizenCite": CitizenCite.model_json_schema(),
        "CitizenMethod": CitizenMethod.model_json_schema(),
        "CitizenNumber": CitizenNumber.model_json_schema(),
        "CitizenChange": CitizenChange.model_json_schema(),
        "CitizenGeography": CitizenGeography.model_json_schema(),
        "Denomination": Denomination.model_json_schema(),
        "LineageRecord": LineageRecord.model_json_schema(),
        "VintageManifest": VintageManifest.model_json_schema(),
        "InputManifest": InputManifest.model_json_schema(),
    }
