"""What a template or chart may bind. Nothing serves a bare float."""

from __future__ import annotations

from pathlib import Path

from prism.paths import render_complete_path, render_dir
from prism.pointer_store import read_citizen_pointer, read_preview_pointer
from prism.schema import (
    CaveatNote,
    Citation,
    Observation,
    ServedObservation,
    SlotSelector,
)


class BindError(ValueError):
    pass


class ServeError(ValueError):
    pass


PREVIEW_HEADERS = {
    "X-Robots-Tag": "noindex, nofollow",
    "Cache-Control": "private, no-store",
}


DEFAULT_STATE_ORDER = "alphabetical_official_english_name"


def observation_matches(observation: Observation, selector: SlotSelector) -> bool:
    geography = observation.geography
    return (
        observation.series_id == selector.series_id
        and geography.code == selector.geography_code
        and geography.geography_vintage == selector.geography_vintage
        and geography.code_system == selector.code_system
        and observation.sector == selector.sector
        and observation.reference_period == selector.reference_period
        and observation.unit == selector.unit
        and observation.status == selector.status
    )


def bind_observation(
    observation: Observation,
    citation: Citation,
    caveat: CaveatNote,
    selector: SlotSelector,
) -> ServedObservation:
    if not observation_matches(observation, selector):
        raise BindError("no matching observation in the bound vintage")
    return ServedObservation(observation=observation, citation=citation, caveat=caveat)


def chart_payload(served: ServedObservation) -> dict[str, object]:
    observation = served.observation
    return {
        "observation_id": observation.observation_id,
        "series_id": observation.series_id,
        "value": observation.value,
        "unit": observation.unit,
        "status": observation.status.value,
        "reference_period": observation.reference_period,
        "sector": observation.sector,
        "geography": observation.geography.model_dump(mode="json"),
        "citation": served.citation.model_dump(mode="json"),
        "caveat_id": served.caveat.caveat_id,
        "data_vintage_bound": True,
    }


def _require_complete_render(data_root: Path, vintage_id: str) -> Path:
    dest = render_dir(data_root, vintage_id)
    if not render_complete_path(data_root, vintage_id).exists():
        raise ServeError(f"render is not complete for {vintage_id}")
    if not (dest / "index.html").exists():
        raise ServeError(f"required template failed to render for {vintage_id}")
    return dest


def resolve_citizen_render(data_root: Path) -> Path:
    vintage_id = read_citizen_pointer(data_root)
    if vintage_id is None:
        raise ServeError("citizen route cannot read a non-published vintage")
    return _require_complete_render(data_root, vintage_id)


def resolve_preview_render(data_root: Path) -> Path:
    vintage_id = read_preview_pointer(data_root)
    if vintage_id is None:
        raise ServeError("no preview pointer")
    return _require_complete_render(data_root, vintage_id)


def citizen_may_read(data_root: Path, vintage_id: str) -> bool:
    return read_citizen_pointer(data_root) == vintage_id


def preview_response_headers() -> dict[str, str]:
    return dict(PREVIEW_HEADERS)
