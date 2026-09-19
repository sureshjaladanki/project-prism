"""What a template or chart may bind. Nothing serves a bare float."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from prism.desk_store import load_desk
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

_PRISM_PAGE_RE = re.compile(r'data-prism-page="([^"]*)"')
_PRISM_PATH_RE = re.compile(r'data-prism-path="([^"]*)"')
_JSON_LD_RE = re.compile(
    r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)
_HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
_CANONICAL_RE = re.compile(r'rel=["\']canonical["\']', re.IGNORECASE)
_OG_URL_RE = re.compile(r'property=["\']og:url["\']', re.IGNORECASE)


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


SLICE_INDEX_HTML = {
    "c1-prices-people-pay": Path("prices") / "retail-prices" / "index.html",
    "c2-people-of-india": Path("people") / "population" / "index.html",
    "c3-union-money": Path("money") / "union" / "index.html",
}


def _require_complete_render(data_root: Path, desk_id: str) -> Path:
    dest = render_dir(data_root, desk_id)
    if not render_complete_path(data_root, desk_id).exists():
        raise ServeError(f"render is not complete for {desk_id}")
    if not (dest / "index.html").exists():
        raise ServeError(f"required template failed to render for {desk_id}")
    record = load_desk(data_root, desk_id)
    for binding in record.slices:
        rel = SLICE_INDEX_HTML.get(binding.template_id)
        if rel is not None and not (dest / rel).exists():
            raise ServeError(f"required template failed to render for {desk_id}")
    return dest


def resolve_citizen_render(data_root: Path) -> Path:
    desk_id = read_citizen_pointer(data_root)
    if desk_id is None:
        raise ServeError("citizen route cannot read a non-published vintage")
    return _require_complete_render(data_root, desk_id)


def resolve_preview_render(data_root: Path) -> Path:
    desk_id = read_preview_pointer(data_root)
    if desk_id is None:
        raise ServeError("no preview pointer")
    return _require_complete_render(data_root, desk_id)


def citizen_may_read(data_root: Path, vintage_id: str) -> bool:
    desk_id = read_citizen_pointer(data_root)
    if desk_id is None:
        return False
    if desk_id == vintage_id:
        return True
    record = load_desk(data_root, desk_id)
    return any(binding.vintage_id == vintage_id for binding in record.slices)


def preview_response_headers() -> dict[str, str]:
    return dict(PREVIEW_HEADERS)


def normalize_citizen_origin(origin: str) -> str:
    parsed = urlparse(origin)
    if parsed.scheme not in {"http", "https"} or parsed.netloc == "":
        raise ServeError(f"invalid citizen origin: {origin}")
    if parsed.path not in {"", "/"} or parsed.query != "" or parsed.fragment != "":
        raise ServeError(f"citizen origin must be a host, not a path: {origin}")
    return f"{parsed.scheme}://{parsed.netloc}"


def canonical_href(origin: str, path: str) -> str:
    if path == "/":
        return f"{origin}/"
    return f"{origin}{path}"


def resolve_tree_path(root: Path, url_path: str) -> Path:
    parsed = urlparse(url_path)
    rel = unquote(parsed.path).lstrip("/")
    base = root.resolve()
    candidate = (base / rel).resolve() if rel else base
    try:
        candidate.relative_to(base)
    except ValueError:
        return base / "404.html"
    if candidate.is_file():
        return candidate
    index = candidate / "index.html" if rel else base / "index.html"
    if index.is_file():
        return index
    return base / "404.html"


def served_tree_file(
    root: Path, url_path: str, *, origin: str | None
) -> tuple[int, Path, bytes] | None:
    path = resolve_tree_path(root, url_path)
    requested = unquote(urlparse(url_path).path).rstrip("/")
    not_found = path.name == "404.html" and requested != "/404.html"
    if not path.is_file():
        return None
    body = path.read_bytes()
    if origin is not None and path.suffix.lower() == ".html":
        body = inject_citizen_origin(body, origin)
    status = 404 if not_found else 200
    return status, path, body


def slashless_redirect(url_path: str) -> str | None:
    parsed = urlparse(url_path)
    request_path = unquote(parsed.path)
    if request_path == "/" or not request_path.endswith("/"):
        return None
    location = request_path.rstrip("/") or "/"
    if parsed.query:
        return f"{location}?{parsed.query}"
    return location


def inject_citizen_origin(html: bytes, origin: str) -> bytes:
    origin = normalize_citizen_origin(origin)
    text = html.decode("utf-8")
    path = _citizen_path(text)
    if path is not None:
        href = canonical_href(origin, path)
        text = _ensure_head_tags(text, href)
    text = _JSON_LD_RE.sub(lambda match: _rewrite_json_ld_script(match, origin), text)
    return text.encode("utf-8")


def _citizen_path(html: str) -> str | None:
    page_match = _PRISM_PAGE_RE.search(html)
    if page_match is not None and page_match.group(1) == "notfound":
        return None
    path_match = _PRISM_PATH_RE.search(html)
    if path_match is None:
        return None
    path = path_match.group(1)
    if path == "":
        return None
    if not path.startswith("/"):
        raise ServeError(f"data-prism-path must be a root-relative path: {path}")
    return path


def _ensure_head_tags(html: str, href: str) -> str:
    tags: list[str] = []
    if _CANONICAL_RE.search(html) is None:
        tags.append(f'<link rel="canonical" href="{href}" />')
    if _OG_URL_RE.search(html) is None:
        tags.append(f'<meta property="og:url" content="{href}" />')
    if tags == []:
        return html
    close = _HEAD_CLOSE_RE.search(html)
    if close is None:
        raise ServeError("HTML is missing </head>; cannot inject canonical")
    insertion = "".join(f"    {tag}\n" for tag in tags)
    return html[: close.start()] + insertion + html[close.start() :]


def _rewrite_json_ld_script(match: re.Match[str], origin: str) -> str:
    payload = json.loads(match.group(2))
    rewritten = _absolutize_json_ld(payload, origin)
    serialized = json.dumps(rewritten, ensure_ascii=False, separators=(",", ":"))
    return f"{match.group(1)}{serialized}{match.group(3)}"


def _absolutize_json_ld(node: object, origin: str) -> object:
    if isinstance(node, list):
        return [_absolutize_json_ld(item, origin) for item in node]
    if not isinstance(node, dict):
        return node
    out = {key: _absolutize_json_ld(value, origin) for key, value in node.items()}
    if out.get("@type") == "WebSite" and "url" not in out:
        out["url"] = origin
    item = out.get("item")
    if isinstance(item, str) and item.startswith("/") and not item.startswith("//"):
        out["item"] = canonical_href(origin, item)
    return out
