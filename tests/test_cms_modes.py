"""Preview desk includes unpublished slices; citizen desk does not."""

from __future__ import annotations

from pathlib import Path

from prism.template_bind import bind_pages_for_desk, bind_pages_for_vintage

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
CMS_ROOT = REPO_ROOT / "src" / "cms"
C1_VINTAGE_ID = "dv-20260916-234e263c8588"
C2_VINTAGE_ID = "dv-20260919-87b702f1fd66"
C3_VINTAGE_ID = "dv-20260918-846e99d0ca57"


def test_preview_desk_binds_c1_c2_c3_each_on_its_vintage() -> None:
    pages = bind_pages_for_desk(DATA_ROOT, CMS_ROOT, cms_mode="preview")
    by_id = {page.template_id: page for page in pages}
    assert set(by_id) == {
        "c1-prices-people-pay",
        "c2-people-of-india",
        "c3-union-money",
    }
    assert by_id["c1-prices-people-pay"].vintage_id == C1_VINTAGE_ID
    assert by_id["c1-prices-people-pay"].path == "/prices/retail-prices"
    assert by_id["c2-people-of-india"].vintage_id == C2_VINTAGE_ID
    assert by_id["c2-people-of-india"].path == "/people/population"
    assert by_id["c3-union-money"].vintage_id == C3_VINTAGE_ID
    assert by_id["c3-union-money"].path == "/money/union"


def test_citizen_desk_binds_only_the_published_c1_vintage() -> None:
    pages = bind_pages_for_desk(DATA_ROOT, CMS_ROOT, cms_mode="citizen")
    assert tuple(page.template_id for page in pages) == ("c1-prices-people-pay",)
    assert pages[0].vintage_id == C1_VINTAGE_ID


def test_one_vintage_bind_still_refuses_other_charters() -> None:
    c2_only = bind_pages_for_vintage(DATA_ROOT, C2_VINTAGE_ID, CMS_ROOT)
    assert tuple(page.template_id for page in c2_only) == ("c2-people-of-india",)


def test_home_template_does_not_repeat_shell_nav() -> None:
    source = (CMS_ROOT / "src" / "pages" / "index.astro").read_text(encoding="utf-8")
    assert 'class="fast-facts"' in source
    assert "hottest-rail" not in source
    assert "sleeve-index" not in source
    assert "{slice.citizen_question}" in source
    assert "<a href={slice.path}>{slice.fact_lede}</a>" not in source
    assert '<p class="byline">{slice.fact_lede}</p>' in source
