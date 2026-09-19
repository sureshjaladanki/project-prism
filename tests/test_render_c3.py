"""C3 template bind and preview render. Does not move citizen."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from prism.paths import render_complete_path, render_dir
from prism.pointer_store import read_citizen_pointer
from prism.template_bind import RenderError, bind_c3_page

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
CMS_ROOT = REPO_ROOT / "src" / "cms"
C1_VINTAGE_ID = "dv-20260916-234e263c8588"
C3_VINTAGE_ID = "dv-20260918-846e99d0ca57"
C3_SLICE_HTML = Path("money") / "union" / "index.html"


def test_bind_c3_refuses_to_mix_c1_vintage() -> None:
    with pytest.raises(RenderError, match="refusing to mix vintage"):
        bind_c3_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)


def test_bind_c3_page_is_one_vintage() -> None:
    page = bind_c3_page(DATA_ROOT, C3_VINTAGE_ID, CMS_ROOT)
    assert page.template_id == "c3-union-money"
    assert page.path == "/money/union"
    assert page.vintage_id == C3_VINTAGE_ID
    ids = set(re.findall(r'data-vintage-id="([^"]+)"', page.body_html))
    assert ids == {C3_VINTAGE_ID}
    assert "unknown / not a table" in page.body_html
    assert page.citizen_question.startswith("What does the Union collect")


@pytest.mark.cms_render
def test_c3_preview_tree_has_union_slice_and_leaves_citizen() -> None:
    dest = render_dir(DATA_ROOT, C3_VINTAGE_ID)
    if not render_complete_path(DATA_ROOT, C3_VINTAGE_ID).exists():
        pytest.fail("C3 Astro render is not complete")
    html = (dest / C3_SLICE_HTML).read_text(encoding="utf-8")
    assert 'data-prism-page="slice"' in html
    assert 'data-prism-path="/money/union"' in html
    assert (
        "<title>What does the Union collect, and what does it spend it on?</title>"
        in html
    )
    assert "unknown / not a table" in html
    assert ">undefined<" not in html
    assert (
        dest / "money" / "union" / "charts" / "collect-beside-spend.vl.json"
    ).exists()
    assert read_citizen_pointer(DATA_ROOT) == C1_VINTAGE_ID
