"""C2 template bind and preview render. Does not move citizen."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from prism.paths import render_complete_path, render_dir
from prism.pointer_store import read_citizen_pointer, read_preview_pointer
from prism.template_bind import RenderError, bind_c2_page

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
CMS_ROOT = REPO_ROOT / "src" / "cms"
C1_VINTAGE_ID = "dv-20260916-234e263c8588"
C2_VINTAGE_ID = "dv-20260919-87b702f1fd66"
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
    assert page.citizen_question.startswith("How many people live in India")


@pytest.mark.cms_render
def test_c2_preview_tree_has_population_slice_and_leaves_citizen() -> None:
    dest = render_dir(DATA_ROOT, C2_VINTAGE_ID)
    if not render_complete_path(DATA_ROOT, C2_VINTAGE_ID).exists():
        pytest.fail("C2 Astro render is not complete")
    html = (dest / C2_SLICE_HTML).read_text(encoding="utf-8")
    assert 'data-prism-page="slice"' in html
    assert 'data-prism-path="/people/population"' in html
    assert (
        "<title>How many people live in India, where, and how is that changing?</title>"
        in html
    )
    assert ">undefined<" not in html
    assert 'data-cms-mode="preview"' in html
    assert (
        dest / "people" / "population" / "charts" / "india-residence-2011.vl.json"
    ).exists()
    assert (dest / "prices" / "retail-prices" / "index.html").exists()
    assert (dest / "money" / "union" / "index.html").exists()
    home = (dest / "index.html").read_text(encoding="utf-8")
    assert "/prices/retail-prices" in home
    assert "/people/population" in home
    assert "/money/union" in home
    assert read_citizen_pointer(DATA_ROOT) == C1_VINTAGE_ID
    assert read_preview_pointer(DATA_ROOT) == C2_VINTAGE_ID
