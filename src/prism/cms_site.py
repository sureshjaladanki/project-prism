"""Route catalog for one vintage. Slugs come from template front matter."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NoReturn

if TYPE_CHECKING:
    from prism.template_bind import BoundPage


def _fail(message: str) -> NoReturn:
    from prism.template_bind import RenderError

    raise RenderError(message)


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FACT_LEDE_RE = re.compile(r'<div class="fact-lede">(.*?)</div>', re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
HOTTEST_RAIL_RE = re.compile(
    r'(<nav class="hottest-rail"[^>]*>)(.*?)(</nav>)',
    re.DOTALL | re.IGNORECASE,
)
ANCHOR_RE = re.compile(
    r"<a\s+[^>]*href=\"([^\"]+)\"[^>]*>.*?</a>", re.DOTALL | re.IGNORECASE
)

HOUSE_PATHS = ("/how-this-works", "/sources")
HOUSE_PAGES = (
    {
        "path": "/how-this-works",
        "title": "How this works · Prism",
        "h1": "How this works",
        "description": (
            "Prism shows official government statistics as published. "
            "High or low, good or bad — the reader decides."
        ),
    },
    {
        "path": "/sources",
        "title": "Sources · Prism",
        "h1": "Sources",
        "description": (
            "Every number names the producing office, the series, and the date."
        ),
    },
)
CHARTER_ORDER = {
    "C1": 1,
    "C2": 2,
    "C3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
    "C7": 7,
    "C8": 8,
}


@dataclass(frozen=True)
class SleeveSpec:
    token: str
    path: str
    header_label: str
    hub_label: str


SLEEVES: tuple[SleeveSpec, ...] = (
    SleeveSpec("people", "/people", "People", "People"),
    SleeveSpec("work", "/work", "Work", "Work"),
    SleeveSpec("money", "/money", "Money", "Money"),
    SleeveSpec("prices-and-production", "/prices", "Prices", "Prices and production"),
    SleeveSpec("delivery", "/delivery", "Delivery", "Delivery"),
)

SLEEVE_BY_TOKEN = {sleeve.token: sleeve for sleeve in SLEEVES}
HUB_PATHS = {sleeve.path for sleeve in SLEEVES}
RESERVED_PATHS = HUB_PATHS | set(HOUSE_PATHS) | {"/"}


def sleeve_path(token: str, slug: str) -> str:
    spec = SLEEVE_BY_TOKEN.get(token)
    if spec is None:
        _fail(f"unknown sleeve token: {token}")
    if not SLUG_RE.fullmatch(slug):
        _fail(f"invalid slug: {slug}")
    path = f"{spec.path}/{slug}"
    if path in RESERVED_PATHS:
        _fail(f"slice path collides with a hub or house path: {path}")
    return path


def plain_fact_lede(body_html: str) -> str:
    match = FACT_LEDE_RE.search(body_html)
    if match is None:
        _fail("bound fact-lede is empty while the H1 shows")
    text = TAG_RE.sub("", match.group(1))
    text = " ".join(text.split())
    if text == "":
        _fail("bound fact-lede is empty while the H1 shows")
    return text


def filter_hottest_rail(body_html: str, allowed_paths: set[str]) -> str:
    def replace_nav(match: re.Match[str]) -> str:
        inner = ANCHOR_RE.sub(
            lambda anchor: _keep_anchor(anchor, allowed_paths), match.group(2)
        )
        return f"{match.group(1)}{inner}{match.group(3)}"

    return HOTTEST_RAIL_RE.sub(replace_nav, body_html)


def _keep_anchor(match: re.Match[str], allowed_paths: set[str]) -> str:
    href = match.group(1)
    if href.startswith("#") or href in allowed_paths:
        return match.group(0)
    return ""


def build_site_catalog(vintage_id: str, pages: tuple[BoundPage, ...]) -> dict[str, Any]:
    seen: set[tuple[str, str]] = set()
    slices: list[dict[str, str]] = []
    for page in pages:
        key = (page.sleeve, page.slug)
        if key in seen:
            _fail("two published templates share a slug in the same sleeve")
        seen.add(key)
        slices.append(
            {
                "template_id": page.template_id,
                "charter": page.charter,
                "sleeve": page.sleeve,
                "slug": page.slug,
                "path": page.path,
                "citizen_question": page.citizen_question,
                "fact_lede": page.fact_lede,
            }
        )
    slices.sort(key=lambda item: (CHARTER_ORDER.get(item["charter"], 99), item["path"]))
    return {
        "vintage_id": vintage_id,
        "sleeves": [
            {
                "token": sleeve.token,
                "path": sleeve.path,
                "header_label": sleeve.header_label,
                "hub_label": sleeve.hub_label,
            }
            for sleeve in SLEEVES
        ],
        "slices": slices,
        "house": [dict(page) for page in HOUSE_PAGES],
    }


def allowed_hrefs(catalog: dict[str, Any]) -> set[str]:
    paths = {sleeve["path"] for sleeve in catalog["sleeves"]}
    paths.update(item["path"] for item in catalog["slices"])
    paths.update(item["path"] for item in catalog["house"])
    paths.add("/")
    return paths


def dump_site_catalog(catalog: dict[str, Any]) -> bytes:
    return (
        json.dumps(catalog, ensure_ascii=False, sort_keys=True, indent=2).encode(
            "utf-8"
        )
        + b"\n"
    )


__all__ = [
    "HOUSE_PAGES",
    "SLEEVES",
    "SLEEVE_BY_TOKEN",
    "allowed_hrefs",
    "build_site_catalog",
    "dump_site_catalog",
    "filter_hottest_rail",
    "plain_fact_lede",
    "sleeve_path",
]
