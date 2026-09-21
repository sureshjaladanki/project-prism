"""Bind Portrait slots to one vintage. Never type a numeral into the page."""

from __future__ import annotations

import copy
import html
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import markdown
import yaml

from prism.catalog import CatalogCiteBlock, default_catalog
from prism.citizen_projection import (
    cite_element_id,
    concept_key,
    indian_grouped,
    is_rate_or_index,
    magnitude_for_display,
    project_citizen_cite,
    project_citizen_method,
    project_display_value,
    scale_for_concept,
    tick_scale_label,
)
from prism.cms_site import plain_fact_lede, sleeve_path
from prism.paths import (
    CAVEAT_FILENAME,
    CITATION_FILENAME,
    GEOGRAPHY_FILENAME,
    series_dir,
    vintage_dir,
)
from prism.schema import (
    CaveatNote,
    Citation,
    CitizenCite,
    CitizenMethod,
    CodeSystem,
    DisplayScale,
    DisplayValue,
    GeographyVintage,
    Observation,
    ObservationStatus,
    ServedObservation,
    SlotSelector,
    contract_json_schema,
)
from prism.serving import (
    assert_hole_never_plotted_as_zero,
    bind_observation,
    chart_payload,
)
from prism.vega_lite_gates import assert_generated_spec
from prism.vintage_query import (
    connect_vintage,
    observations_in_period_range,
    observations_matching,
)
from prism.vintage_store import load_manifest

C1_TEMPLATE_ID = "c1-prices-people-pay"
C1_TEMPLATE_DIRNAME = "c1-prices-people-pay"
C2_TEMPLATE_ID = "c2-people-of-india"
C2_TEMPLATE_DIRNAME = "c2-people-of-india"
C3_TEMPLATE_ID = "c3-union-money"
C3_TEMPLATE_DIRNAME = "c3-union-money"


LAYOUT_BLOCKS: dict[str, tuple[str, str]] = {
    "hero": ("header", "hero"),
    "stat-row": ("div", "stat-row"),
    "section": ("section", "portrait-section"),
    "how-this-is-measured": ("section", "how-measured"),
}

SLOT_RE = re.compile(r"\{\{slot:([^}]+)\}\}")
STAT_RE = re.compile(r"\{\{stat:([^}|]+)(?:\|([^}]+))?\}\}")
CITE_BLOCK_RE = re.compile(r"\{\{cite-block:([^}]+)\}\}")
CAVEAT_BLOCK_RE = re.compile(r"\{\{caveat-block:([^}]+)\}\}")
CHART_RE = re.compile(r"\{\{chart:([^}]+)\}\}")
CITE_FIELD_RE = re.compile(r"\{\{cite:([^.}]+)\.([^}]+)\}\}")
PERIOD_RE = re.compile(r"\{\{period\.([^.}]+)\.([^}]+)\}\}")
LEFTOVER_MUSTACHE_RE = re.compile(r"\{\{[^}]+\}\}")
CITE_VIEW_COMMENT_RE = re.compile(
    r"<!--\s*cite-view:\s*([A-Za-z0-9_-]+)", re.IGNORECASE
)
CITE_VIEW_OPEN_RE = re.compile(
    r'<section class="(?:cite-view|how-measured)(?:\s[^"]*)?"(?:\s+data-cite-view="([^"]+)")?\s*>',
    re.IGNORECASE,
)
HOW_MEASURED_RE = re.compile(
    r'<section class="how-measured"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE,
)
STAT_ROW_OPEN = '<div class="stat-row">'
SLOT_VALUE_PUNCT_RE = re.compile(
    r'(<span class="observation-value">[^<]*</span></span>)\s+([.,;:])'
)
SLOT_MISSING_PUNCT_RE = re.compile(
    r'(<span class="observation observation-missing"[^>]*>[^<]*</span>)\s+([.,;:])'
)
BOUND_NUMBER_RE = re.compile(r'class="observation"[^>]*data-observation-id="[^"]+"')
REQUIRED_CARD_MARKERS: tuple[tuple[str, str], ...] = (
    ("citation-card", 'class="citation-card'),
    ("caveat-note", 'class="caveat-note'),
    ("producer", "<dt>Producer</dt>"),
    ("series", "<dt>Series</dt>"),
    ("reference period", "<dt>Reference period</dt>"),
    ("release date", "<dt>Release date</dt>"),
    ("caveat", "<dt>Caveat</dt>"),
    ("data vintage", "data-vintage-id="),
)


class RenderError(ValueError):
    pass


@dataclass(frozen=True)
class BoundCopy:
    text: str


@dataclass(frozen=True)
class BoundPage:
    template_id: str
    vintage_id: str
    sleeve: str
    slug: str
    path: str
    charter: str
    citizen_question: str
    fact_lede: str
    body_html: str
    charts: dict[str, dict[str, Any]]


def templates_dir(cms_root: Path) -> Path:
    return cms_root / "templates"


def c1_template_dir(cms_root: Path) -> Path:
    return templates_dir(cms_root) / C1_TEMPLATE_DIRNAME


def c2_template_dir(cms_root: Path) -> Path:
    return templates_dir(cms_root) / C2_TEMPLATE_DIRNAME


def c3_template_dir(cms_root: Path) -> Path:
    return templates_dir(cms_root) / C3_TEMPLATE_DIRNAME


def bind_c1_page(data_root: Path, vintage_id: str, cms_root: Path) -> BoundPage:
    return bind_page(data_root, vintage_id, c1_template_dir(cms_root))


def bind_c2_page(data_root: Path, vintage_id: str, cms_root: Path) -> BoundPage:
    return bind_page(data_root, vintage_id, c2_template_dir(cms_root))


def bind_c3_page(data_root: Path, vintage_id: str, cms_root: Path) -> BoundPage:
    return bind_page(data_root, vintage_id, c3_template_dir(cms_root))


def _template_folders(cms_root: Path) -> tuple[Path, ...]:
    root = templates_dir(cms_root)
    if not root.is_dir():
        raise RenderError("CMS templates directory is missing")
    return tuple(
        folder
        for folder in sorted(root.iterdir())
        if folder.is_dir() and (folder / "slots.yaml").exists()
    )


def _slice_series_ids(template_id: str) -> set[str]:
    from prism.catalog import CatalogError, default_catalog

    try:
        item = default_catalog().slice_for_template(template_id)
    except CatalogError as exc:
        raise RenderError(f"unknown template_id {template_id}") from exc
    return {entry.series_id for entry in item.series}


def _assert_vintage_matches_template(
    data_root: Path, vintage_id: str, template_id: str
) -> None:
    if not vintage_dir(data_root, vintage_id).exists():
        raise RenderError(
            f"template is bound to {template_id}; refusing to mix vintage {vintage_id}"
        )
    manifest = load_manifest(data_root, vintage_id)
    found = {entry.series_id for entry in manifest.series}
    expected = _slice_series_ids(template_id)
    if found != expected:
        raise RenderError(
            f"template is bound to {template_id}; refusing to mix vintage {vintage_id}"
        )


def bind_pages_for_vintage(
    data_root: Path, vintage_id: str, cms_root: Path
) -> tuple[BoundPage, ...]:
    pages: list[BoundPage] = []
    if not vintage_dir(data_root, vintage_id).exists():
        raise RenderError(f"no template bound at vintage {vintage_id}")
    manifest = load_manifest(data_root, vintage_id)
    found = {entry.series_id for entry in manifest.series}
    for folder in _template_folders(cms_root):
        spec = _load_yaml(folder / "slots.yaml")
        template_id = str(spec["template_id"])
        if _slice_series_ids(template_id) != found:
            continue
        pages.append(bind_page(data_root, vintage_id, folder))
    if not pages:
        raise RenderError(f"no template bound at vintage {vintage_id}")
    return tuple(pages)


def bind_pages_for_desk(
    data_root: Path,
    cms_root: Path,
    *,
    cms_mode: str,
    desk_id: str | None = None,
) -> tuple[BoundPage, ...]:
    """Bind each slice the desk lists. cms_mode selects the pointer when desk_id is omitted."""
    if cms_mode not in {"preview", "citizen"}:
        raise RenderError(f"unknown cms_mode {cms_mode}")
    from prism.desk_store import load_desk
    from prism.pointer_store import read_citizen_pointer, read_preview_pointer

    if desk_id is None:
        desk_id = (
            read_citizen_pointer(data_root)
            if cms_mode == "citizen"
            else read_preview_pointer(data_root)
        )
    if desk_id is None:
        raise RenderError(f"no template bound for cms_mode {cms_mode}")
    record = load_desk(data_root, desk_id)
    pages: list[BoundPage] = []
    root = templates_dir(cms_root)
    for binding in record.slices:
        folder = root / binding.template_id
        pages.append(bind_page(data_root, binding.vintage_id, folder))
    if not pages:
        raise RenderError(f"no template bound for cms_mode {cms_mode}")
    return tuple(pages)


def bind_page(data_root: Path, vintage_id: str, template_dir: Path) -> BoundPage:
    slots_path = template_dir / "slots.yaml"
    copy_path = template_dir / "template.md"
    spec = _load_yaml(slots_path)
    template_id = str(spec["template_id"])
    _assert_vintage_matches_template(data_root, vintage_id, template_id)
    manifest = load_manifest(data_root, vintage_id)
    if manifest.vintage_id != vintage_id:
        raise RenderError("one page cannot bind slots from two vintage_ids")

    cards = _load_cards(
        data_root, vintage_id, tuple(entry.series_id for entry in manifest.series)
    )
    connection = connect_vintage(data_root, vintage_id)
    try:
        bound_slots = _bind_observation_slots(connection, vintage_id, spec, cards)
        charts = _bind_charts(
            connection, vintage_id, spec, cards, template_dir, bound_slots
        )
    finally:
        connection.close()

    scales = _display_scales(bound_slots, charts)
    _apply_chart_displays(charts, scales)
    displays = _slot_displays(bound_slots, scales)
    cite_blocks = default_catalog().slice_for_template(template_id).cite_block_by_id()
    miss_copies = {
        str(slot["slot_id"]): str(slot.get("miss_copy", "not published"))
        for slot in spec["slots"]
    }

    front_matter, markdown_copy = _parse_front_matter(
        copy_path.read_text(encoding="utf-8")
    )
    if front_matter.get("template_id") != template_id:
        raise RenderError("unexpected template_id")
    sleeve = str(front_matter.get("sleeve") or "")
    slug = str(front_matter.get("slug") or "")
    charter = str(front_matter.get("charter") or "")
    citizen_question = str(front_matter.get("citizen_question") or "").strip()
    if charter == "":
        raise RenderError("template front matter is missing charter")
    if citizen_question == "":
        raise RenderError("citizen_question is missing")
    path = sleeve_path(sleeve, slug)
    expanded = _expand_copy(
        markdown_copy,
        vintage_id,
        spec,
        bound_slots,
        cards,
        charts,
        displays,
        cite_blocks,
        miss_copies,
        _periods_by_citation(
            tuple(CITE_BLOCK_RE.findall(markdown_copy)),
            cite_blocks,
            bound_slots,
            cards,
        ),
    )
    body_html = wrap_cite_views(
        markdown.markdown(expanded, extensions=["extra", "md_in_html"])
    )
    leftover = LEFTOVER_MUSTACHE_RE.search(body_html)
    if leftover is not None:
        raise RenderError(f"unbound template token: {leftover.group(0)}")
    body_html = _tidy_slot_punctuation(body_html)
    body_html = _inject_cite_strip(body_html)
    body_html = _wire_source_lines(body_html)
    assert_cite_views_complete(body_html)
    fact_lede = plain_fact_lede(body_html)
    return BoundPage(
        template_id=template_id,
        vintage_id=vintage_id,
        sleeve=sleeve,
        slug=slug,
        path=path,
        charter=charter,
        citizen_question=citizen_question,
        fact_lede=fact_lede,
        body_html=body_html,
        charts=charts,
    )


def write_contract_schema(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(contract_json_schema(), indent=2, sort_keys=True, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )


def wrap_cite_views(html_text: str) -> str:
    rest, measured = _peel_how_measured(html_text)
    wrapped = _wrap_h2_cite_views(rest)
    if measured is None:
        return wrapped
    return wrapped + _ensure_how_measured_named(measured)


def _peel_how_measured(html_text: str) -> tuple[str, str | None]:
    match = HOW_MEASURED_RE.search(html_text)
    if match is None:
        return html_text, None
    rest = html_text[: match.start()] + html_text[match.end() :]
    return rest, match.group(0)


def _ensure_how_measured_named(html_text: str) -> str:
    if "data-cite-view=" in html_text:
        return html_text
    return html_text.replace(
        '<section class="how-measured"',
        '<section class="how-measured" data-cite-view="how-this-is-measured"',
        1,
    )


def _wrap_h2_cite_views(html_text: str) -> str:
    parts = re.split(r"(<h2[^>]*>)", html_text, flags=re.IGNORECASE)
    if len(parts) == 1:
        return _cite_view_section(html_text, _cite_view_name(html_text))
    groups: list[tuple[str | None, str]] = []
    current_html = parts[0]
    current_name = _cite_view_name(parts[0])
    for index in range(1, len(parts), 2):
        heading = parts[index]
        body = parts[index + 1] if index + 1 < len(parts) else ""
        chunk = f"{heading}{body}"
        name = _cite_view_name(chunk)
        if name is None:
            current_html += chunk
            continue
        if current_html:
            groups.append((current_name, current_html))
        current_html = chunk
        current_name = name
    if current_html:
        groups.append((current_name, current_html))
    rebuilt: list[str] = []
    for index, (name, inner) in enumerate(groups):
        if index == 0 and name is None and BOUND_NUMBER_RE.search(inner) is None:
            rebuilt.append(inner)
            continue
        rebuilt.append(_cite_view_section(inner, name))
    return "".join(rebuilt)


def _cite_view_name(html_text: str) -> str | None:
    match = CITE_VIEW_COMMENT_RE.search(html_text)
    if match is None:
        return None
    return match.group(1)


def _cite_view_section(inner: str, name: str | None) -> str:
    if name == "how-this-is-measured":
        return (
            f'<section class="how-measured" data-cite-view="{html.escape(name)}">'
            f"{inner}</section>"
        )
    if name is None:
        return f'<section class="cite-view">{inner}</section>'
    return f'<section class="cite-view" data-cite-view="{html.escape(name)}">{inner}</section>'


def iter_cite_views(html_text: str) -> tuple[tuple[str | None, str], ...]:
    matches = list(CITE_VIEW_OPEN_RE.finditer(html_text))
    views: list[tuple[str | None, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(html_text)
        views.append((match.group(1), html_text[start:end]))
    return tuple(views)


def assert_cite_views_complete(html_text: str) -> None:
    """Fail closed: a bound number needs producer, series, date, and caveat in that same view."""

    for name, section_html in iter_cite_views(html_text):
        if BOUND_NUMBER_RE.search(section_html) is None:
            continue
        missing = [
            label
            for label, needle in REQUIRED_CARD_MARKERS
            if needle not in section_html
        ]
        if not missing:
            continue
        label = name or "unnamed"
        raise RenderError(
            f"cite-view {label} bound a number without "
            + " and ".join(missing)
            + "; fail closed"
        )


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RenderError("slots.yaml must be a mapping")
    return loaded


def _parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        raise RenderError("template.md is missing front matter")
    end = text.find("\n---", 3)
    if end == -1:
        raise RenderError("template.md front matter is not closed")
    loaded = yaml.safe_load(text[3:end])
    if not isinstance(loaded, dict):
        raise RenderError("template front matter is not a mapping")
    return loaded, text[end + 4 :].lstrip("\n")


def _load_cards(
    data_root: Path, vintage_id: str, series_ids: tuple[str, ...]
) -> dict[str, tuple[Citation, CaveatNote, GeographyVintage]]:
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]] = {}
    for series_id in series_ids:
        folder = series_dir(data_root, vintage_id, series_id)
        citation = Citation.model_validate_json(
            (folder / CITATION_FILENAME).read_bytes()
        )
        caveat = CaveatNote.model_validate_json((folder / CAVEAT_FILENAME).read_bytes())
        geography = GeographyVintage.model_validate_json(
            (folder / GEOGRAPHY_FILENAME).read_bytes()
        )
        cards[series_id] = (citation, caveat, geography)
    return cards


def _citation_by_id(
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]], citation_id: str
) -> Citation:
    for citation, _caveat, _geography in cards.values():
        if citation.citation_id == citation_id:
            return citation
    raise RenderError(f"citation {citation_id} is not in this vintage")


def _caveat_by_id(
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]], caveat_id: str
) -> CaveatNote:
    for _citation, caveat, _geography in cards.values():
        if caveat.caveat_id == caveat_id:
            return caveat
    raise RenderError(f"caveat {caveat_id} is not in this vintage")


def _cards_for_series(
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]], series_id: str
) -> tuple[Citation, CaveatNote, GeographyVintage]:
    try:
        return cards[series_id]
    except KeyError as exc:
        raise RenderError(f"series {series_id} is not in this vintage") from exc


def _bind_observation_slots(
    connection: Any,
    vintage_id: str,
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> dict[str, ServedObservation | BoundCopy | str]:
    bound: dict[str, ServedObservation | BoundCopy | str] = {}
    for slot in spec["slots"]:
        kind = slot["kind"]
        slot_id = slot["slot_id"]
        if kind == "observation":
            bound[slot_id] = _bind_one_observation(connection, vintage_id, slot, cards)
        elif kind == "caveat_field":
            caveat = _caveat_by_id(cards, slot["caveat_id"])
            bound[slot_id] = BoundCopy(text=_caveat_field(caveat, slot["field"]))
        elif kind == "collection":
            continue
        else:
            raise RenderError(f"unknown slot kind {kind}")
    return bound


def _bind_one_observation(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> ServedObservation | str:
    selector = _selector_from_mapping(slot["selector"])
    matches = observations_matching(
        connection,
        vintage_id,
        series_id=selector.series_id,
        geography_codes=(selector.geography_code,),
        geography_vintage=selector.geography_vintage,
        code_system=selector.code_system,
        sectors=(selector.sector,),
        reference_periods=(selector.reference_period,),
        units=(selector.unit,),
        statuses=(selector.status,),
    )
    if len(matches) > 1:
        raise RenderError(f"slot {slot['slot_id']} matched more than one observation")
    if len(matches) == 0:
        if slot.get("required", False):
            raise RenderError(
                f"required slot {slot['slot_id']} has no observation; not pasting a remembered figure"
            )
        return str(slot.get("miss_copy", "not published"))
    citation, caveat, _geography = _cards_for_series(cards, selector.series_id)
    if (
        citation.citation_id != slot["citation_id"]
        or caveat.caveat_id != slot["caveat_id"]
    ):
        raise RenderError(
            f"slot {slot['slot_id']} citation or caveat does not match the vintage"
        )
    served = bind_observation(matches[0], citation, caveat, selector)
    _assert_cite_complete(served)
    return served


def _assert_cite_complete(served: ServedObservation) -> None:
    observation = served.observation
    if not observation.citation_id or not observation.caveat_id:
        raise RenderError("a number cannot render without citation_id and caveat_id")
    if not observation.geography.geography_vintage:
        raise RenderError("a number cannot render without geography vintage")
    if served.citation.producer == "" or served.citation.series == "":
        raise RenderError("citation card is missing producer or series")


_CITIZEN_CAVEAT_FIELDS = {
    "population": lambda caveat: caveat.population,
    "citizen_note": lambda caveat: caveat.citizen_note or "",
    "unit": lambda caveat: caveat.unit,
    "reference_period": lambda caveat: caveat.reference_period,
}


def _caveat_field(caveat: CaveatNote, field: str) -> str:
    try:
        return _CITIZEN_CAVEAT_FIELDS[field](caveat)
    except KeyError as exc:
        raise RenderError(f"desk caveat field {field} is not a citizen slot") from exc


def _selector_from_mapping(selector: dict[str, Any]) -> SlotSelector:
    return SlotSelector(
        series_id=selector["series_id"],
        geography_code=str(selector["geography_code"]),
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sector=selector["sector"],
        reference_period=str(selector["reference_period"]),
        unit=selector["unit"],
        status=ObservationStatus(selector["status"]),
    )


def _bind_charts(
    connection: Any,
    vintage_id: str,
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
    template_dir: Path,
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
) -> dict[str, dict[str, Any]]:
    datasets: dict[str, list[dict[str, object]]] = {}
    for slot in spec["slots"]:
        if slot["kind"] != "collection":
            continue
        datasets[slot["slot_id"]] = _bind_collection(
            connection, vintage_id, slot, spec, cards, bound_slots
        )

    charts: dict[str, dict[str, Any]] = {}
    for chart_id, relpath in spec["charts"].items():
        spec_path = (template_dir / relpath).resolve()
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
        bound_spec = _fill_named_datasets(raw, datasets)
        assert_generated_spec(bound_spec)
        charts[chart_id] = bound_spec
    return charts


def _iter_chart_rows(node: Any) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if isinstance(node, dict):
        data = node.get("data")
        if isinstance(data, dict) and isinstance(data.get("values"), list):
            rows.extend(item for item in data["values"] if isinstance(item, dict))
        for value in node.values():
            rows.extend(_iter_chart_rows(value))
    elif isinstance(node, list):
        for item in node:
            rows.extend(_iter_chart_rows(item))
    return rows


def _display_scales(
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    charts: dict[str, dict[str, Any]],
) -> dict[str, DisplayScale]:
    buckets: dict[str, list[float]] = {}
    rate_by_key: dict[str, bool] = {}

    def add(
        series_id: str, unit: str, raw: float | None, status: ObservationStatus
    ) -> None:
        key = concept_key(series_id, unit)
        rate_by_key[key] = is_rate_or_index(unit)
        if status is ObservationStatus.value and raw is not None:
            buckets.setdefault(key, []).append(magnitude_for_display(raw, unit))

    for bound in bound_slots.values():
        if isinstance(bound, ServedObservation):
            observation = bound.observation
            add(
                observation.series_id,
                observation.unit,
                observation.value,
                observation.status,
            )
    for spec in charts.values():
        for row in _iter_chart_rows(spec):
            series_id = row.get("series_id")
            unit = row.get("unit")
            status_raw = row.get("status")
            if not isinstance(series_id, str) or not isinstance(unit, str):
                continue
            if not isinstance(status_raw, str):
                continue
            status = ObservationStatus(status_raw)
            raw = row.get("value") if status is ObservationStatus.value else None
            add(
                series_id,
                unit,
                float(raw) if isinstance(raw, (int, float)) else None,
                status,
            )
    return {
        key: scale_for_concept(tuple(buckets.get(key, ())), rate_or_index=rate)
        for key, rate in rate_by_key.items()
    }


def _apply_chart_displays(
    charts: dict[str, dict[str, Any]],
    scales: dict[str, DisplayScale],
) -> None:
    for spec in charts.values():
        for row in _iter_chart_rows(spec):
            series_id = row.get("series_id")
            unit = row.get("unit")
            status_raw = row.get("status")
            if not isinstance(series_id, str) or not isinstance(unit, str):
                continue
            if not isinstance(status_raw, str):
                continue
            status = ObservationStatus(status_raw)
            scale = scales.get(concept_key(series_id, unit), DisplayScale.none)
            raw = row.get("value") if status is ObservationStatus.value else None
            display = project_display_value(
                raw_value=float(raw) if isinstance(raw, (int, float)) else None,
                unit=unit,
                status=status,
                scale=scale,
            )
            row["value"] = display.chart_value
            row["display_scale"] = scale.value
            row["tick_scale"] = tick_scale_label(scale, unit)
            row["display_string"] = display.display_string


def _slot_displays(
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    scales: dict[str, DisplayScale],
) -> dict[str, DisplayValue]:
    displays: dict[str, DisplayValue] = {}
    for slot_id, bound in bound_slots.items():
        if not isinstance(bound, ServedObservation):
            continue
        observation = bound.observation
        scale = scales.get(
            concept_key(observation.series_id, observation.unit),
            DisplayScale.none,
        )
        displays[slot_id] = project_display_value(
            raw_value=observation.value,
            unit=observation.unit,
            status=observation.status,
            scale=scale,
        )
    return displays


def _bind_collection(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
) -> list[dict[str, object]]:
    if "members" in slot:
        return _member_rows(slot, bound_slots)
    selector = slot["selector"]
    period = selector.get("reference_period")
    if (
        selector.get("geography_codes") == "state_ut_order"
        or "exclude_geography_codes" in slot
    ):
        return _state_rows(connection, vintage_id, slot, spec, cards)
    if isinstance(period, dict) and "from" in period:
        return _range_rows(connection, vintage_id, slot, cards)
    if "units" in selector:
        label_key = slot.get("labels")
        if label_key and "unit" in spec[label_key][0]:
            return _labelled_unit_rows(connection, vintage_id, slot, spec, cards)
        return _division_rows(connection, vintage_id, slot, spec, cards)
    return _collection_rows(connection, vintage_id, slot, spec, cards)


def _labelled_unit_rows(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> list[dict[str, object]]:
    selector = slot["selector"]
    units = tuple(str(item) for item in selector["units"])
    statuses = tuple(ObservationStatus(item) for item in _as_tuple(selector["status"]))
    observations = observations_matching(
        connection,
        vintage_id,
        series_id=selector["series_id"],
        geography_codes=(str(selector["geography_code"]),),
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sectors=(selector["sector"],),
        reference_periods=_as_tuple(selector["reference_period"]),
        units=units,
        statuses=statuses,
    )
    by_unit = {item.unit: item for item in observations}
    names = {item["unit"]: item["name"] for item in spec[slot["labels"]]}
    rows: list[dict[str, object]] = []
    for unit in units:
        observation = by_unit.get(unit)
        if observation is None:
            raise RenderError(
                f"collection {slot['slot_id']} missing unit {unit}; not inventing a figure"
            )
        rows.append(_row(_serve(observation, cards), {"head_name": names[unit]}))
    return rows


def _serve(
    observation: Observation,
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> ServedObservation:
    citation, caveat, _geography = _cards_for_series(cards, observation.series_id)
    if (
        observation.citation_id != citation.citation_id
        or observation.caveat_id != caveat.caveat_id
    ):
        raise RenderError(
            "observation cards do not match the series files in this vintage"
        )
    selector = SlotSelector(
        series_id=observation.series_id,
        geography_code=observation.geography.code,
        geography_vintage=observation.geography.geography_vintage,
        code_system=observation.geography.code_system,
        sector=observation.sector,
        reference_period=observation.reference_period,
        unit=observation.unit,
        status=observation.status,
    )
    served = bind_observation(observation, citation, caveat, selector)
    _assert_cite_complete(served)
    return served


def _row(
    served: ServedObservation, extra: dict[str, object] | None = None
) -> dict[str, object]:
    payload = chart_payload(served)
    if extra:
        payload.update(extra)
    assert_hole_never_plotted_as_zero(payload)
    return payload


def _collection_rows(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> list[dict[str, object]]:
    selector = slot["selector"]
    sectors = _as_tuple(selector["sector"])
    periods = _as_tuple(selector["reference_period"])
    statuses = tuple(ObservationStatus(item) for item in _as_tuple(selector["status"]))
    observations = observations_matching(
        connection,
        vintage_id,
        series_id=selector["series_id"],
        geography_codes=(str(selector["geography_code"]),),
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sectors=sectors,
        reference_periods=tuple(str(item) for item in periods),
        units=(selector["unit"],),
        statuses=statuses,
    )
    by_key = {(item.sector, item.reference_period): item for item in observations}
    rows: list[dict[str, object]] = []
    sector_order = [str(item) for item in spec.get("sector_order", [])]
    ordered_sectors = [item for item in sector_order if item in sectors] or list(
        sectors
    )
    for sector in ordered_sectors:
        for period in periods:
            observation = by_key.get((sector, str(period)))
            if observation is None:
                raise RenderError(
                    f"collection {slot['slot_id']} missing {sector} {period}; not inventing a figure"
                )
            rows.append(_row(_serve(observation, cards)))
    return rows


def _range_rows(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> list[dict[str, object]]:
    selector = slot["selector"]
    period = selector["reference_period"]
    statuses = tuple(ObservationStatus(item) for item in _as_tuple(selector["status"]))
    observations = observations_in_period_range(
        connection,
        vintage_id,
        series_id=selector["series_id"],
        geography_code=str(selector["geography_code"]),
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sector=selector["sector"],
        period_from=str(period["from"]),
        period_to=str(period["to"]),
        unit=selector["unit"],
        statuses=statuses,
    )
    return [_row(_serve(item, cards)) for item in observations]


def _state_rows(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> list[dict[str, object]]:
    selector = slot["selector"]
    units = [(str(item["code"]), item["name_en"]) for item in spec["state_ut_order"]]
    exclude = {str(code) for code in slot.get("exclude_geography_codes", [])}
    codes = tuple(code for code, _name in units if code not in exclude)
    statuses = tuple(ObservationStatus(item) for item in _as_tuple(selector["status"]))
    observations = observations_matching(
        connection,
        vintage_id,
        series_id=selector["series_id"],
        geography_codes=codes,
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sectors=(selector["sector"],),
        reference_periods=(str(selector["reference_period"]),),
        units=(selector["unit"],),
        statuses=statuses,
    )
    by_code = {item.geography.code: item for item in observations}
    rows: list[dict[str, object]] = []
    for code, name_en in units:
        if code in exclude:
            continue
        observation = by_code.get(code)
        if observation is None:
            raise RenderError(f"state/UT {code} is missing; not inventing a figure")
        rows.append(
            _row(
                _serve(observation, cards),
                {"geography_code": code, "geography_name_en": name_en},
            )
        )
    return rows


def _division_rows(
    connection: Any,
    vintage_id: str,
    slot: dict[str, Any],
    spec: dict[str, Any],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> list[dict[str, object]]:
    selector = slot["selector"]
    units = tuple(str(item) for item in selector["units"])
    statuses = tuple(ObservationStatus(item) for item in _as_tuple(selector["status"]))
    observations = observations_matching(
        connection,
        vintage_id,
        series_id=selector["series_id"],
        geography_codes=(str(selector["geography_code"]),),
        geography_vintage=str(selector["geography_vintage"]),
        code_system=CodeSystem(selector["code_system"]),
        sectors=(selector["sector"],),
        reference_periods=(str(selector["reference_period"]),),
        units=units,
        statuses=statuses,
    )
    by_unit = {item.unit: item for item in observations}
    names = {item["code"]: item["name"] for item in spec["division_order"]}
    rows: list[dict[str, object]] = []
    for unit in units:
        observation = by_unit.get(unit)
        if observation is None:
            raise RenderError(
                f"division unit {unit} is missing; not inventing a figure"
            )
        code = unit.rsplit(" ", 1)[-1]
        rows.append(
            _row(
                _serve(observation, cards),
                {"division_code": code, "division_name": names[code]},
            )
        )
    return rows


def _member_rows(
    slot: dict[str, Any], bound_slots: dict[str, ServedObservation | BoundCopy | str]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for member in slot["members"]:
        bound = bound_slots[member["slot_id"]]
        if not isinstance(bound, ServedObservation):
            raise RenderError(f"chart member {member['slot_id']} is not published")
        rows.append(_row(bound, {"label": member["label"]}))
    return rows


def _fill_named_datasets(
    spec: dict[str, Any], datasets: dict[str, list[dict[str, object]]]
) -> dict[str, Any]:
    filled = copy.deepcopy(spec)
    _replace_named_data(filled, datasets)
    return filled


def _replace_named_data(
    node: Any, datasets: dict[str, list[dict[str, object]]]
) -> None:
    if isinstance(node, dict):
        data = node.get("data")
        if isinstance(data, dict) and isinstance(data.get("name"), str):
            name = data["name"]
            if name.startswith("slot:"):
                slot_id = name.removeprefix("slot:")
                if slot_id not in datasets:
                    raise RenderError(f"chart names unbound slot {slot_id}")
                node["data"] = {"values": datasets[slot_id]}
        for value in node.values():
            _replace_named_data(value, datasets)
    elif isinstance(node, list):
        for item in node:
            _replace_named_data(item, datasets)


def _as_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return (str(value),)


def _expand_copy(
    markdown_copy: str,
    vintage_id: str,
    spec: dict[str, Any],
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
    charts: dict[str, dict[str, Any]],
    displays: dict[str, DisplayValue],
    cite_blocks: dict[str, CatalogCiteBlock],
    miss_copies: dict[str, str],
    periods_by_cite: dict[str, frozenset[str]],
) -> str:
    text = markdown_copy.replace("{{data_vintage_id}}", html.escape(vintage_id))
    text = PERIOD_RE.sub(
        lambda match: _period_field(spec, match.group(1), match.group(2)), text
    )
    text = CITE_FIELD_RE.sub(
        lambda match: _in_text_cite_html(
            _citation_by_id(cards, match.group(1)),
            match.group(2),
            periods_by_cite,
        ),
        text,
    )
    text = STAT_RE.sub(
        lambda match: _stat_html(
            match.group(1),
            match.group(2),
            bound_slots,
            vintage_id,
            displays,
            miss_copies,
        ),
        text,
    )
    text = SLOT_RE.sub(
        lambda match: _slot_html(
            match.group(1), bound_slots, vintage_id, displays, miss_copies
        ),
        text,
    )
    emitted_panels: set[str] = set()
    text = CITE_BLOCK_RE.sub(
        lambda match: _cite_block_html(
            match.group(1),
            cards,
            vintage_id,
            bound_slots,
            emitted_panels,
            cite_blocks,
            periods_by_cite,
        ),
        text,
    )
    text = CAVEAT_BLOCK_RE.sub(
        lambda match: _caveat_block_html(
            _caveat_by_id(cards, match.group(1)), vintage_id
        ),
        text,
    )
    text = CHART_RE.sub(lambda match: _chart_placeholder(match.group(1), charts), text)
    return _expand_layout_tokens(text)


def _period_field(spec: dict[str, Any], role: str, field: str) -> str:
    try:
        value = spec["period_roles"][role][field]
    except KeyError as exc:
        raise RenderError(f"unknown period token period.{role}.{field}") from exc
    return html.escape(str(value))


def _cite_field(citation: Citation, field: str) -> str:
    try:
        value = getattr(citation, field)
    except AttributeError as exc:
        raise RenderError(f"unknown citation field {field}") from exc
    return _format_date_field(value)


def _in_text_cite_period(
    citation: Citation, periods_by_cite: dict[str, frozenset[str]]
) -> str:
    periods = periods_by_cite.get(citation.citation_id, frozenset())
    if citation.reference_period in periods:
        return citation.reference_period
    if len(periods) == 1:
        return next(iter(periods))
    if not periods:
        return citation.reference_period
    raise RenderError(
        f"in-text cite {citation.citation_id} period {citation.reference_period} "
        "is not a bound cite period"
    )


def _in_text_cite_html(
    citation: Citation,
    field: str,
    periods_by_cite: dict[str, frozenset[str]],
) -> str:
    value = html.escape(_cite_field(citation, field))
    period = _in_text_cite_period(citation, periods_by_cite)
    periods = periods_by_cite.get(
        citation.citation_id, frozenset({citation.reference_period})
    )
    element_id = cite_element_id(citation.citation_id, period, periods)
    panel_id = html.escape(f"{element_id}-panel", quote=True)
    return (
        f'<button type="button" class="in-text-cite" popovertarget="{panel_id}">'
        f"{value}</button>"
    )


def _producer_anchor(cite: CitizenCite) -> str:
    return (
        f'<a href="{html.escape(cite.url, quote=True)}">'
        f"{html.escape(cite.producer)}</a>"
    )


def _citizen_citation_dl(cite: CitizenCite) -> str:
    return (
        "<dl>"
        f"<dt>Producer</dt><dd>{_producer_anchor(cite)}</dd>"
        f"<dt>Series</dt><dd>{html.escape(cite.series)}</dd>"
        f"<dt>Reference period</dt><dd>{html.escape(cite.reference_period)}</dd>"
        f"<dt>Release date</dt><dd>{html.escape(cite.released)} (Asia/Kolkata)</dd>"
        f"<dt>Caveat</dt><dd>{html.escape(cite.caveat)}</dd>"
        "</dl>"
    )


def _cite_panel_html(element_id: str, cite: CitizenCite) -> str:
    panel_id = html.escape(f"{element_id}-panel", quote=True)
    return (
        f'<div id="{panel_id}" class="cite-panel" popover>'
        f"{_citizen_citation_dl(cite)}"
        "</div>"
    )


def _format_date_field(value: object) -> str:
    if value == "unknown":
        return "not printed"
    if isinstance(value, date):
        return f"{value.day} {value.strftime('%B %Y')}"
    return str(value)


def _slot_html(
    slot_id: str,
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    vintage_id: str,
    displays: dict[str, DisplayValue],
    miss_copies: dict[str, str],
) -> str:
    try:
        bound = bound_slots[slot_id]
    except KeyError as exc:
        raise RenderError(f"copy names unknown slot {slot_id}") from exc
    if isinstance(bound, BoundCopy):
        return html.escape(bound.text)
    if isinstance(bound, str):
        return (
            f'<span class="observation observation-missing" data-slot-id="{html.escape(slot_id)}">'
            f"{html.escape(bound)}</span>"
        )
    observation = bound.observation
    if observation.status is not ObservationStatus.value:
        copy = miss_copies.get(slot_id, "not published")
        return (
            f'<span class="observation observation-missing" data-slot-id="{html.escape(slot_id)}" '
            f'data-observation-id="{html.escape(observation.observation_id)}" '
            f'data-vintage-id="{html.escape(vintage_id)}">'
            f"{html.escape(copy)}</span>"
        )
    display = displays[slot_id]
    return (
        f'<span class="observation" data-slot-id="{html.escape(slot_id)}" '
        f'data-observation-id="{html.escape(observation.observation_id)}" '
        f'data-vintage-id="{html.escape(vintage_id)}">'
        f'<span class="observation-value">{html.escape(display.display_string)}</span>'
        f"</span>"
    )


def format_bound_number(value: float) -> str:
    return indian_grouped(value)


def _tidy_slot_punctuation(html_text: str) -> str:
    html_text = SLOT_VALUE_PUNCT_RE.sub(r"\1\2", html_text)
    return SLOT_MISSING_PUNCT_RE.sub(r"\1\2", html_text)


def _stat_html(
    slot_id: str,
    label: str | None,
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    vintage_id: str,
    displays: dict[str, DisplayValue],
    miss_copies: dict[str, str],
) -> str:
    figure = _slot_html(slot_id, bound_slots, vintage_id, displays, miss_copies)
    label_html = ""
    if label:
        label_html = f'<p class="stat-label">{html.escape(label.strip())}</p>'
    return f'<div class="stat">{label_html}<p class="stat-figure">{figure}</p></div>'


def _expand_layout_tokens(text: str) -> str:
    for name, (tag, class_name) in LAYOUT_BLOCKS.items():
        open_tag = f'<{tag} class="{class_name}" markdown="1">'
        if name == "how-this-is-measured":
            open_tag = (
                f'<{tag} class="{class_name}" '
                'data-cite-view="how-this-is-measured" markdown="1">'
            )
        text = text.replace(f"{{{{{name}}}}}", open_tag)
        text = text.replace(f"{{{{/{name}}}}}", f"</{tag}>")
    return text


def _inject_cite_strip(html_text: str) -> str:
    if "cite-strip" in html_text:
        return html_text
    card = re.search(
        r'<details class="citation-card source-byline"[^>]*>.*?</details>',
        html_text,
        flags=re.DOTALL,
    )
    if card is None:
        raise RenderError("first-screen cite strip is missing a citation card")
    insert_at = _element_end(html_text, STAT_ROW_OPEN)
    return html_text[:insert_at] + _cite_strip_from_card(card.group(0)) + html_text[insert_at:]


def _wire_source_lines(html_text: str) -> str:
    """Chart source-lines open the same cite panel as in-text cites (F-source-line-panel)."""

    def replace(match: re.Match[str]) -> str:
        inner = match.group(1)
        target = re.search(r'popovertarget="([^"]+)"', inner)
        if target is None:
            return match.group(0)
        cleaned = re.sub(
            r'<button type="button" class="in-text-cite" popovertarget="[^"]+">(.*?)</button>',
            r"\1",
            inner,
            flags=re.DOTALL,
        )
        return (
            f'<button type="button" class="source-line" '
            f'popovertarget="{target.group(1)}">{cleaned}</button>'
        )

    return re.sub(
        r"<p class=\"source-line\">(.*?)</p>",
        replace,
        html_text,
        flags=re.DOTALL,
    )


def _element_end(html_text: str, open_tag: str) -> int:
    start = html_text.find(open_tag)
    if start == -1:
        raise RenderError("first-screen cite strip needs a stat row")
    name_end = open_tag.find(" ")
    tag = open_tag[1:name_end] if name_end != -1 else open_tag[1:-1]
    open_needle = f"<{tag}"
    close_needle = f"</{tag}>"
    depth = 0
    pos = start
    while pos < len(html_text):
        next_open = html_text.find(open_needle, pos)
        next_close = html_text.find(close_needle, pos)
        if next_close == -1:
            raise RenderError("first-screen cite strip needs a stat row")
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + len(open_needle)
            continue
        depth -= 1
        pos = next_close + len(close_needle)
        if depth == 0:
            return pos
    raise RenderError("first-screen cite strip needs a stat row")


def _cite_strip_from_card(card_html: str) -> str:
    fields = _card_fields(card_html)
    required = ("Producer", "Series", "Reference period", "Release date")
    missing = [label for label in required if not fields.get(label, "").strip()]
    if missing:
        raise RenderError(
            "cite strip missing " + " and ".join(item.lower() for item in missing)
        )
    release = re.sub(r"\s*\(Asia/Kolkata\)\s*$", "", fields["Release date"]).strip()
    producer = html.escape(fields["Producer"])
    rest = html.escape(
        f"{fields['Series']} · {fields['Reference period']} · released {release}"
    )
    card_id = re.search(r'\bid="([^"]+)"', card_html)
    if card_id is None:
        raise RenderError("cite strip missing citation card id")
    panel_id = html.escape(f"{card_id.group(1)}-panel", quote=True)
    cite_attr = ""
    cite = re.search(r'data-citation-id="([^"]+)"', card_html)
    if cite is not None:
        cite_attr = f' data-citation-id="{html.escape(cite.group(1), quote=True)}"'
    vintage_attr = ""
    vintage = re.search(r'data-vintage-id="([^"]+)"', card_html)
    if vintage is not None:
        vintage_attr = f' data-vintage-id="{html.escape(vintage.group(1), quote=True)}"'
    return (
        f'<button type="button" class="source-byline cite-strip"'
        f"{cite_attr}{vintage_attr} popovertarget=\"{panel_id}\">"
        f'<span class="cite-producer">{producer}</span>'
        f'<span class="cite-rest"> · {rest}</span>'
        f"</button>"
    )


def _card_fields(card_html: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in re.finditer(
        r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", card_html, flags=re.DOTALL
    ):
        label = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        value = html.unescape(re.sub(r"<[^>]+>", "", match.group(2))).strip()
        fields[label] = value
    return fields


def _periods_by_citation(
    block_ids: tuple[str, ...],
    cite_blocks: dict[str, CatalogCiteBlock],
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
) -> dict[str, frozenset[str]]:
    found: dict[str, set[str]] = {}
    for block_id in block_ids:
        try:
            block = cite_blocks[block_id]
        except KeyError as exc:
            raise RenderError(f"unknown cite-block {block_id}") from exc
        if block.observation_slots:
            period = _cite_period_from_slots(block, bound_slots)
            for citation_id in block.citation_ids:
                found.setdefault(citation_id, set()).add(period)
            continue
        for citation_id in block.citation_ids:
            citation = _citation_by_id(cards, citation_id)
            found.setdefault(citation_id, set()).add(citation.reference_period)
    return {key: frozenset(value) for key, value in found.items()}


def _cite_block_html(
    block_id: str,
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
    vintage_id: str,
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
    emitted_panels: set[str],
    cite_blocks: dict[str, CatalogCiteBlock],
    periods_by_cite: dict[str, frozenset[str]],
) -> str:
    try:
        block = cite_blocks[block_id]
    except KeyError as exc:
        raise RenderError(f"unknown cite-block {block_id}") from exc
    reference_period = None
    if block.observation_slots:
        reference_period = _cite_period_from_slots(block, bound_slots)
    parts = [
        _citation_card_html(
            _citation_by_id(cards, citation_id),
            cards,
            vintage_id,
            emitted_panels,
            periods_by_cite,
            reference_period=reference_period,
        )
        for citation_id in block.citation_ids
    ]
    return "\n\n".join(part for part in parts if part)


def _cite_period_from_slots(
    block: CatalogCiteBlock,
    bound_slots: dict[str, ServedObservation | BoundCopy | str],
) -> str:
    periods: set[str] = set()
    for slot_id in block.observation_slots:
        try:
            bound = bound_slots[slot_id]
        except KeyError as exc:
            raise RenderError(f"cite-block names unknown slot {slot_id}") from exc
        if not isinstance(bound, ServedObservation):
            raise RenderError(
                f"cite-block slot {slot_id} is not a published observation"
            )
        observation = bound.observation
        if observation.citation_id not in block.citation_ids:
            raise RenderError(
                f"cite-block slot {slot_id} citation {observation.citation_id} "
                "is not in this block"
            )
        periods.add(observation.reference_period)
    if len(periods) != 1:
        raise RenderError(
            "cite-block observation slots must share one reference period"
        )
    return next(iter(periods))


def _citation_card_html(
    citation: Citation,
    cards: dict[str, tuple[Citation, CaveatNote, GeographyVintage]],
    vintage_id: str,
    emitted_panels: set[str],
    periods_by_cite: dict[str, frozenset[str]],
    *,
    reference_period: str | None = None,
) -> str:
    geography_vintage = None
    for series_citation, _caveat, geography in cards.values():
        if series_citation.citation_id == citation.citation_id:
            geography_vintage = geography.geography_vintage
            break
    if geography_vintage is None:
        raise RenderError(f"no geography vintage for {citation.citation_id}")
    period = citation.reference_period if reference_period is None else reference_period
    periods = periods_by_cite.get(citation.citation_id, frozenset({period}))
    element_id = cite_element_id(citation.citation_id, period, periods)
    if element_id in emitted_panels:
        return ""
    emitted_panels.add(element_id)
    cite = project_citizen_cite(citation, reference_period=period)
    summary = f"{cite.series} · {cite.reference_period} · released {cite.released}"
    cite_id = html.escape(citation.citation_id, quote=True)
    vintage = html.escape(vintage_id, quote=True)
    card = (
        f'<details class="citation-card source-byline" '
        f'id="{html.escape(element_id, quote=True)}" '
        f'data-citation-id="{cite_id}" data-vintage-id="{vintage}" '
        f'data-reference-period="{html.escape(period, quote=True)}">'
        f"<summary>{html.escape(summary)}</summary>"
        f"{_citizen_citation_dl(cite)}"
        "</details>"
    )
    return card + _cite_panel_html(element_id, cite)


def _citizen_method_for(caveat: CaveatNote) -> CitizenMethod:
    if caveat.citizen_note:
        return project_citizen_method(caveat)
    catalog_note = default_catalog().caveats.get(caveat.caveat_id)
    if catalog_note is None or not catalog_note.citizen_note:
        raise RenderError(f"{caveat.caveat_id} missing citizen_note")
    return project_citizen_method(catalog_note)


def _caveat_block_html(caveat: CaveatNote, vintage_id: str) -> str:
    method = _citizen_method_for(caveat)
    fields = [
        ("What it counts", method.what_it_counts),
        ("Coverage", method.coverage),
    ]
    if method.break_note is not None:
        fields.append(("Break", method.break_note))
    if method.lag_note is not None:
        fields.append(("Lag", method.lag_note))
    rows = "".join(
        f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>"
        for label, value in fields
    )
    return (
        f'<details class="caveat-note" data-caveat-id="{html.escape(caveat.caveat_id)}" '
        f'data-vintage-id="{html.escape(vintage_id)}">'
        f"<summary>Method</summary><dl>{rows}</dl></details>"
    )


def _chart_placeholder(chart_id: str, charts: dict[str, dict[str, Any]]) -> str:
    if chart_id not in charts:
        raise RenderError(f"copy names unknown chart {chart_id}")
    return f"<!--chart:{chart_id}-->"


def assert_single_vintage(page: BoundPage, vintage_id: str) -> None:
    if page.vintage_id != vintage_id:
        raise RenderError("one page cannot bind slots from two vintage_ids")
    ids = set(re.findall(r'data-vintage-id="([^"]+)"', page.body_html))
    ids.add(page.vintage_id)
    if ids != {vintage_id}:
        raise RenderError("one page cannot bind slots from two vintage_ids")


__all__ = [
    "C1_TEMPLATE_ID",
    "C2_TEMPLATE_ID",
    "C3_TEMPLATE_ID",
    "BoundPage",
    "RenderError",
    "assert_cite_views_complete",
    "assert_single_vintage",
    "bind_c1_page",
    "bind_c2_page",
    "bind_c3_page",
    "bind_page",
    "bind_pages_for_desk",
    "bind_pages_for_vintage",
    "c1_template_dir",
    "c2_template_dir",
    "c3_template_dir",
    "format_bound_number",
    "iter_cite_views",
    "wrap_cite_views",
    "write_contract_schema",
]
