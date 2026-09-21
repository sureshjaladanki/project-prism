"""C2 template bind and preview render. Does not move citizen."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from prism.desk_store import load_desk
from prism.paths import render_complete_path, render_dir
from prism.pointer_store import read_citizen_pointer, read_preview_pointer
from prism.template_bind import RenderError, bind_c2_page, format_bound_number

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
CMS_ROOT = REPO_ROOT / "src" / "cms"
C1_VINTAGE_ID = "dv-20260916-234e263c8588"
C2_VINTAGE_ID = "dv-20260921-617d0e9cf03f"
C2_SLICE_HTML = Path("people") / "population" / "index.html"


def test_bind_c2_refuses_to_mix_c1_vintage() -> None:
    with pytest.raises(RenderError, match="refusing to mix vintage"):
        bind_c2_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)


def test_bind_c2_page_is_one_vintage() -> None:
    page = bind_c2_page(DATA_ROOT, C2_VINTAGE_ID, CMS_ROOT)
    assert page.template_id == "c2-people-of-india"
    assert page.path == "/people/population"
    assert page.vintage_id == C2_VINTAGE_ID
    ids = set(re.findall(r'data-vintage-id="([^"]+)"', page.body_html))
    assert ids == {C2_VINTAGE_ID}
    assert "Census 2011" in page.body_html
    assert "does not pick a winner" in page.body_html
    assert "next_release" not in page.body_html
    assert "on this desk" not in page.body_html
    assert "Districts are parked" not in page.body_html
    assert page.citizen_question.startswith("How many people live in India")
    assert "121.09 Cr" in page.body_html
    assert page.fact_lede.startswith("On 1 March 2011, Census 2011 counted 121.09 Cr")
    assert "Updated not printed" not in page.body_html
    assert "Release date not printed" not in page.body_html
    assert "Census day 1 March 2011" in page.body_html
    assert "A later census total has not been published." in page.body_html
    assert "6.4 ." not in page.body_html
    assert "6.4</span></span>." in page.body_html
    assert "<!--chart:india-residence-2011-->" not in page.body_html
    assert "india-residence-2011" not in page.charts


def test_bound_numbers_use_indian_grouping() -> None:
    assert format_bound_number(1_210_854_977) == "1,21,08,54,977"
    assert format_bound_number(5_347_314.81) == "53,47,314.81"
    assert format_bound_number(6.4) == "6.4"
    assert format_bound_number(4.82) == "4.82"
    assert format_bound_number(1000) == "1,000"
    assert format_bound_number(100000) == "1,00,000"
    assert format_bound_number(833_748_852) == "83,37,48,852"


@pytest.mark.cms_render
def test_c2_preview_tree_has_population_slice_and_leaves_citizen() -> None:
    preview = read_preview_pointer(DATA_ROOT)
    assert preview is not None
    dest = render_dir(DATA_ROOT, preview)
    if not render_complete_path(DATA_ROOT, preview).exists():
        pytest.fail("preview Astro render is not complete")
    html = (dest / C2_SLICE_HTML).read_text(encoding="utf-8")
    assert 'data-prism-page="slice"' in html
    assert 'data-prism-path="/people/population"' in html
    assert (
        "<title>How many people live in India, where, and how is that changing?</title>"
        in html
    )
    assert ">undefined<" not in html
    assert 'data-cms-mode="preview"' in html
    assert not (
        dest / "people" / "population" / "charts" / "india-residence-2011.vl.json"
    ).exists()
    assert (dest / "prices" / "retail-prices" / "index.html").exists()
    assert (dest / "money" / "union" / "index.html").exists()
    home = (dest / "index.html").read_text(encoding="utf-8")
    assert "/prices/retail-prices" in home
    assert "/people/population" in home
    assert "/money/union" in home
    citizen = read_citizen_pointer(DATA_ROOT)
    assert citizen is not None
    assert citizen != preview
    citizen_desk = load_desk(DATA_ROOT, citizen)
    assert all(
        item.template_id != "c2-people-of-india" for item in citizen_desk.slices
    )
    preview_desk = load_desk(DATA_ROOT, preview)
    assert any(item.vintage_id == C2_VINTAGE_ID for item in preview_desk.slices)
