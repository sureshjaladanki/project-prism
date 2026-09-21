"""Nine blueprint tests. 4–8 need a real Astro render of C1."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from prism.desk_store import DeskSlice, load_desk, write_desk
from prism.paths import (
    cas_path,
    citizen_pointer_path,
    preview_pointer_path,
    render_complete_path,
    render_dir,
    series_dir,
)
from prism.pointer_store import (
    PublishError,
    publish_citizen,
    read_citizen_pointer,
    read_preview_pointer,
)
from prism.refresh import (
    C1_SERIES_IDS,
    CARDS_1_3_NEXT_RELEASE,
    SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    SERIES_CPI_CFPI_BASE_2024,
    SERIES_CPI_DIVISION_GROUP_BASE_2024,
    SERIES_CPI_GENERAL_BASE_2024,
    scheduled_series_on,
)
from prism.render import SHELL_PAGES, RenderIncompleteError, _mark_complete
from prism.schema import (
    Completeness,
    GeographyRef,
    Observation,
    ObservationStatus,
    RefreshTrigger,
    ServedObservation,
)
from prism.serving import (
    bind_observation,
    chart_payload,
    citizen_may_read,
    preview_response_headers,
    resolve_citizen_render,
    resolve_preview_render,
)
from prism.template_bind import (
    C1_TEMPLATE_ID,
    RenderError,
    assert_cite_views_complete,
    bind_c1_page,
    wrap_cite_views,
)
from prism.vega_lite_gates import (
    ChartSpecError,
    assert_chart_rows_cited,
    assert_generated_spec,
)
from prism.vintage_store import write_vintage
from tests.desk_fixtures import write_complete_c1_desk
from tests.factories import (
    CREATED_AT,
    make_caveat,
    make_citation,
    make_geography_ref,
    make_observation,
    make_selector,
    make_series_write,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
CMS_ROOT = REPO_ROOT / "src" / "cms"
C1_VINTAGE_ID = "dv-20260916-234e263c8588"
C1_SLICE_HTML = Path("prices") / "retail-prices" / "index.html"


def _c1_render_dir() -> Path:
    dest = resolve_citizen_render(DATA_ROOT)
    if not (dest / C1_SLICE_HTML).exists():
        pytest.fail("C1 Astro render is not complete")
    return dest


def _c1_slice_html() -> str:
    return (_c1_render_dir() / C1_SLICE_HTML).read_text(encoding="utf-8")


def test_01_observation_without_citation_id_cannot_be_written() -> None:
    payload = make_observation().model_dump()
    del payload["citation_id"]
    with pytest.raises(ValidationError):
        Observation.model_validate(payload)
    with pytest.raises(ValidationError):
        make_observation(citation_id="")


def test_02_observation_without_caveat_id_cannot_be_written() -> None:
    payload = make_observation().model_dump()
    del payload["caveat_id"]
    with pytest.raises(ValidationError):
        Observation.model_validate(payload)
    with pytest.raises(ValidationError):
        make_observation(caveat_id="")


def test_03_geography_without_vintage_cannot_be_written() -> None:
    payload = make_geography_ref().model_dump()
    del payload["geography_vintage"]
    with pytest.raises(ValidationError):
        GeographyRef.model_validate(payload)
    with pytest.raises(ValidationError):
        make_geography_ref(geography_vintage="")


@pytest.mark.cms_render
def test_04_publish_does_not_move_citizen_pointer_if_required_template_failed(
    tmp_path: Path,
) -> None:
    first_desk, first = write_complete_c1_desk(tmp_path, b"PARQUET-A", CREATED_AT)
    publish_citizen(
        tmp_path,
        first_desk.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    later = datetime(2026, 9, 16, 10, 0, tzinfo=UTC)
    second = write_vintage(
        tmp_path,
        created_at=later,
        trigger=RefreshTrigger.source_change,
        series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET-B"),),
        completeness=Completeness.complete,
        previous=first,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    second_desk = write_desk(
        tmp_path,
        created_at=later,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=second.vintage_id),
        ),
        completeness=Completeness.complete,
    )
    dest = render_dir(tmp_path, second_desk.desk_id)
    dest.mkdir(parents=True)
    required = SHELL_PAGES + ("prices/retail-prices/index.html",)
    with pytest.raises(RenderIncompleteError, match="required template failed"):
        _mark_complete(dest, required)
    assert not render_complete_path(tmp_path, second_desk.desk_id).exists()
    with pytest.raises(PublishError, match="render is not complete"):
        publish_citizen(
            tmp_path,
            second_desk.desk_id,
            render_complete=True,
            contract_tests_passed=True,
        )
    assert read_citizen_pointer(tmp_path) == first_desk.desk_id
    c1 = _c1_render_dir()
    assert (c1 / "index.html").exists()
    assert (c1 / C1_SLICE_HTML).exists()
    assert (c1 / "404.html").exists()
    assert (c1 / "how-this-works" / "index.html").exists()
    assert (c1 / "sources" / "index.html").exists()
    for sleeve in ("people", "work", "money", "prices", "delivery"):
        assert (c1 / sleeve / "index.html").exists()
    home = (c1 / "index.html").read_text(encoding="utf-8")
    assert 'data-prism-page="home"' in home
    assert (
        "How fast are retail prices rising in India, including food?"
        not in home.split("<title>")[1].split("</title>")[0]
    )
    assert "/people/population" not in home
    assert "/money/union" not in home
    assert not (c1 / "people" / "population" / "index.html").exists()
    assert not (c1 / "money" / "union" / "index.html").exists()
    assert render_complete_path(DATA_ROOT, C1_VINTAGE_ID).exists()


@pytest.mark.cms_render
def test_05_citizen_route_cannot_read_non_published_vintage() -> None:
    citizen = read_citizen_pointer(DATA_ROOT)
    assert citizen is not None
    assert citizen.startswith("desk-")
    desk = load_desk(DATA_ROOT, citizen)
    assert any(binding.vintage_id == C1_VINTAGE_ID for binding in desk.slices)
    assert citizen_may_read(DATA_ROOT, C1_VINTAGE_ID) is True
    assert citizen_may_read(DATA_ROOT, "dv-19990101-aaaaaaaaaaaa") is False
    assert resolve_citizen_render(DATA_ROOT) == render_dir(DATA_ROOT, citizen)
    headers = preview_response_headers()
    assert "noindex" in headers["X-Robots-Tag"]
    assert "private" in headers["Cache-Control"]
    preview = read_preview_pointer(DATA_ROOT)
    assert preview is not None
    assert preview.startswith("desk-")
    preview_root = resolve_preview_render(DATA_ROOT)
    assert preview_root == render_dir(DATA_ROOT, preview)
    assert not citizen_pointer_path(DATA_ROOT).samefile(preview_pointer_path(DATA_ROOT))


@pytest.mark.cms_render
def test_06_one_citizen_page_cannot_bind_slots_from_two_vintages() -> None:
    page = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)
    assert page.vintage_id == C1_VINTAGE_ID
    html = _c1_slice_html()
    ids = set(re.findall(r'data-vintage-id="([^"]+)"', html))
    assert ids == {C1_VINTAGE_ID}
    assert 'data-prism-page="slice"' in html
    assert 'data-prism-path="/prices/retail-prices"' in html
    assert (
        "<title>How fast are retail prices rising in India, including food?</title>"
        in html
    )
    assert 'class="skip-link"' in html
    assert 'href="/prices"' in html
    with pytest.raises(RenderError, match="refusing to mix vintage"):
        bind_c1_page(DATA_ROOT, "dv-19990101-aaaaaaaaaaaa", CMS_ROOT)


@pytest.mark.cms_render
def test_07_chart_payload_cannot_include_number_without_citation_card() -> None:
    with pytest.raises(ValidationError):
        ServedObservation(
            observation=make_observation(),
            citation=make_citation(citation_id="cite-other"),
            caveat=make_caveat(),
        )
    with pytest.raises(ChartSpecError, match="citation"):
        assert_chart_rows_cited([{"value": 1.2, "observation_id": "obs-x"}])
    charts_dir = _c1_render_dir() / "prices" / "retail-prices" / "charts"
    specs = list(charts_dir.glob("*.vl.json"))
    assert specs, "generated Vega-Lite JSON missing from the C1 render tree"
    for path in specs:
        spec = json.loads(path.read_text(encoding="utf-8"))
        assert_generated_spec(spec)


@pytest.mark.cms_render
def test_08_default_state_order_is_not_rank_or_red_green() -> None:
    charts_dir = _c1_render_dir() / "prices" / "retail-prices" / "charts"
    state_spec = json.loads(
        (charts_dir / "state-ut-combined-inflation-latest.vl.json").read_text(
            encoding="utf-8"
        )
    )
    encoding = state_spec["encoding"]
    sort = encoding["y"]["sort"]
    assert encoding["y"]["field"] == "geography_name_en"
    assert sort["field"] == "geography_name_en"
    assert sort["order"] == "ascending"
    assert sort["field"] not in {"plotValue", "value"}
    values = state_spec["data"]["values"]
    names = [row["geography_name_en"] for row in values]
    assert names == sorted(names)
    assert "All India" not in names
    for path in charts_dir.glob("*.vl.json"):
        assert_generated_spec(json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.cms_render
def test_chart_svg_title_does_not_crush_the_plot() -> None:
    html = _c1_slice_html()
    figures = re.findall(
        r'<figure class="chart"[^>]*>.*?</figure>', html, flags=re.DOTALL
    )
    assert len(figures) >= 6
    for figure in figures:
        assert '<p class="chart-title"' in figure
        assert '<div class="chart-plot">' in figure
        assert re.search(
            r"<figcaption>.*</figcaption>\s*<div class=\"chart-plot\">\s*<svg",
            figure,
            flags=re.DOTALL,
        )
        svg_open = re.search(r"<svg([^>]+)>", figure)
        assert svg_open is not None
        attrs = svg_open.group(1)
        width = float(re.search(r'\bwidth="([0-9.]+)"', attrs).group(1))
        assert width <= 1400, attrs


def _bound_observation_html(slot_id: str, value: str) -> str:
    return (
        f'<span class="observation" data-slot-id="{slot_id}" '
        'data-observation-id="obs-x" data-vintage-id="dv-test">'
        f'<span class="observation-value">{value}</span></span>'
    )


def test_named_cite_view_omitting_cards_fails_closed() -> None:
    wrapped = wrap_cite_views(
        "<h2>Provisional and Final</h2>"
        "<!-- cite-view: provisional-and-final. Fail the render if any required card is missing. -->"
        + _bound_observation_html(
            "all-india-combined-general-inflation-latest-f", "4.45"
        )
    )
    with pytest.raises(RenderError, match="provisional-and-final"):
        assert_cite_views_complete(wrapped)


def test_any_cite_view_omitting_cards_fails_closed() -> None:
    named = wrap_cite_views(
        "<h2>How this is measured</h2>"
        "<!-- cite-view: how-this-is-measured. Fail the render if any required card is missing. -->"
        + _bound_observation_html("all-india-combined-general-index-latest-p", "108.74")
    )
    with pytest.raises(RenderError, match="how-this-is-measured"):
        assert_cite_views_complete(named)

    unnamed = wrap_cite_views(
        "<h2>How this is measured</h2>"
        + _bound_observation_html("all-india-combined-general-index-latest-p", "108.74")
    )
    assert "data-cite-view=" not in unnamed
    with pytest.raises(RenderError, match="unnamed"):
        assert_cite_views_complete(unnamed)

    zero_cards = (
        '<section class="cite-view">'
        + _bound_observation_html("all-india-combined-general-index-latest-p", "108.74")
        + "</section>"
    )
    with pytest.raises(RenderError, match="unnamed"):
        assert_cite_views_complete(zero_cards)


def test_cite_in_same_view_as_the_number() -> None:
    html = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT).body_html
    assert_cite_views_complete(html)
    first = _named_cite_view(html, "first-screen")
    assert re.search(r'class="observation-value">[^<]+<', first)
    assert "National Statistics Office" in first
    assert "Consumer Price Index (CPI) General" in first
    assert "2026-08" in first or "August 2026" in first
    assert "14 September 2026" in first
    assert "<dt>Geography vintage</dt>" not in first
    assert "<dt>Data vintage</dt>" not in first
    assert f'data-vintage-id="{C1_VINTAGE_ID}"' in first
    assert re.search(
        r'<dt>Producer</dt><dd><a href="https?://[^"]+">[^<]*National Statistics Office',
        first,
    )
    assert 'class="in-text-cite"' in first
    assert 'class="cite-panel" popover' in first
    assert "Caveat" in first
    assert "tooltip" not in first.lower() or "National Statistics Office" in first
    assert 'data-slot-id="all-india-combined-general-inflation-latest-f"' in first
    assert 'data-slot-id="all-india-combined-cfpi-inflation-latest-f"' in first
    assert re.search(r'class="observation-value">4\.45<', first)
    assert re.search(r'class="observation-value">5\.52<', first)
    targets = re.findall(r'class="in-text-cite"[^>]*popovertarget="([^"]+)"', html)
    assert targets
    for target in targets:
        assert target.endswith("-panel")
        card_id = target[: -len("-panel")]
        opening = re.search(
            rf'<details class="citation-card[^"]*" id="{re.escape(card_id)}"[^>]*>',
            html,
        )
        assert opening is not None
        panel = re.search(
            rf'<div id="{re.escape(target)}" class="cite-panel" popover>',
            html,
        )
        assert panel is not None
        cite_id = re.search(r'data-citation-id="([^"]+)"', opening.group(0))
        period = re.search(r'data-reference-period="([^"]+)"', opening.group(0))
        assert cite_id is not None
        assert period is not None
        if cite_id.group(1).startswith("cite-c1-cpi-general"):
            assert period.group(1) == "2026-08"
    assert "How to read this series" not in html
    assert "<dt>Do not</dt>" not in html
    assert "<summary>Method</summary>" in html
    july_cards = _july_final_cards(first)
    assert len(july_cards) >= 2
    for card in july_cards:
        assert "National Statistics Office" in card
        assert "14 September 2026" in card
        assert "<dt>Reference period</dt><dd>2026-08</dd>" not in card
    measured = _named_cite_view(html, "how-this-is-measured")
    assert "<h2>Methodology</h2>" in html
    assert 'data-slot-id="all-india-combined-general-index-latest-p"' not in measured
    assert 'class="citation-card' not in measured
    assert 'class="caveat-note' not in measured


def test_c1_chart_rows_carry_display_scale() -> None:
    page = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)
    blob = json.dumps(page.charts)
    assert '"display_scale": "none"' in blob
    assert "121.09 Cr" not in page.body_html


def test_c1_cite_period_is_one_card_per_month() -> None:
    html = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT).body_html
    cards = re.findall(
        r'<details class="citation-card source-byline"(?! cite-strip)([^>]*)>(.*?)</details>',
        html,
        flags=re.DOTALL,
    )
    ids = [re.search(r'\bid="([^"]+)"', attrs).group(1) for attrs, _ in cards]
    assert len(ids) == len(set(ids))
    by_cite: dict[str, set[str]] = {}
    for attrs, body in cards:
        cite_id = re.search(r'data-citation-id="([^"]+)"', attrs)
        period = re.search(r"<dt>Reference period</dt><dd>([^<]+)</dd>", body)
        assert cite_id is not None
        assert period is not None
        by_cite.setdefault(cite_id.group(1), set()).add(period.group(1))
    general = "cite-c1-cpi-general-base-2024-2026-08"
    food = "cite-c1-cpi-cfpi-base-2024-2026-08"
    assert by_cite[general] == {"2026-07", "2026-08"}
    assert by_cite[food] == {"2026-07", "2026-08"}
    strip = re.search(
        r'<button type="button" class="source-byline cite-strip"[^>]*>.*?</button>',
        html,
        flags=re.DOTALL,
    )
    assert strip is not None
    assert "2026-08" in strip.group(0) or "August 2026" in strip.group(0)
    assert "2026-07" not in strip.group(0)
    assert 'popovertarget="' in strip.group(0)
    assert 'data-citation-id="' in strip.group(0)


def test_july_final_cite_binds_observation_month() -> None:
    page = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)
    first = _named_cite_view(page.body_html, "first-screen")
    assert 'data-slot-id="all-india-combined-general-inflation-latest-f"' in first
    assert 'data-slot-id="all-india-combined-cfpi-inflation-latest-f"' in first
    july_cards = _july_final_cards(first)
    assert len(july_cards) >= 2
    for card in july_cards:
        assert "<dt>Reference period</dt><dd>2026-08</dd>" not in card
    assert 'class="stat-row"' in page.body_html
    assert 'class="hero"' in page.body_html
    assert 'cite-strip' in page.body_html
    assert 'class="how-measured"' in page.body_html
    assert '<h2 id="food">' in page.body_html
    assert "<h3 " not in page.body_html
    assert page.slug == "retail-prices"
    assert page.path == "/prices/retail-prices"
    assert page.sleeve == "prices-and-production"
    assert page.fact_lede != ""


def test_wrap_cite_views_covers_preamble_numbers() -> None:
    wrapped = wrap_cite_views(
        "<!-- cite-view: first-screen -->"
        + _bound_observation_html(
            "all-india-combined-general-inflation-latest-p", "4.82"
        )
        + "<h2>Food, same month</h2><p>No number here.</p>"
    )
    first = _named_cite_view(wrapped, "first-screen")
    assert 'data-slot-id="all-india-combined-general-inflation-latest-p"' in first
    with pytest.raises(RenderError, match="first-screen"):
        assert_cite_views_complete(wrapped)


def test_division_axis_uses_full_annex_names() -> None:
    page = bind_c1_page(DATA_ROOT, C1_VINTAGE_ID, CMS_ROOT)
    spec = page.charts["all-india-division-inflation-latest"]
    names = [row["division_name"] for row in spec["data"]["values"]]
    sort_order = spec["encoding"]["y"]["sort"]
    assert names == sort_order
    assert "Paan, tobacco and intoxicants" in names
    assert "Paan" not in names


def _july_final_cards(html: str) -> list[str]:
    cards = re.findall(
        r'<details class="citation-card[^"]*"[^>]*>(.*?)</details>', html, flags=re.DOTALL
    )
    return [
        card for card in cards if "<dt>Reference period</dt><dd>2026-07</dd>" in card
    ]


def _named_cite_view(html: str, name: str) -> str:
    match = re.search(
        rf'<section class="(?:cite-view|how-measured)(?:\s[^"]*)?" data-cite-view="{re.escape(name)}">',
        html,
    )
    assert match is not None, f"missing cite-view {name}"
    rest = html[match.end() :]
    next_view = re.search(r'<section class="(?:cite-view|how-measured)"', rest)
    if next_view is None:
        return rest
    return rest[: next_view.start()]


def test_09_unchanged_series_are_not_byte_copied(tmp_path: Path) -> None:
    first = make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET-V1")
    manifest_a = write_vintage(
        tmp_path,
        created_at=CREATED_AT,
        trigger=RefreshTrigger.on_demand,
        series=(first,),
        completeness=Completeness.complete,
        previous=None,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    later = datetime(2026, 9, 16, 9, 0, tzinfo=UTC)
    second = make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET-V1")
    manifest_b = write_vintage(
        tmp_path,
        created_at=later,
        trigger=RefreshTrigger.on_demand,
        series=(second,),
        completeness=Completeness.complete,
        previous=manifest_a,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    assert manifest_b.series[0].reused.value == "yes"
    assert manifest_a.vintage_id != manifest_b.vintage_id
    path_a = (
        series_dir(tmp_path, manifest_a.vintage_id, SERIES_CPI_GENERAL_BASE_2024)
        / "observations.parquet"
    )
    path_b = (
        series_dir(tmp_path, manifest_b.vintage_id, SERIES_CPI_GENERAL_BASE_2024)
        / "observations.parquet"
    )
    digest = hashlib.sha256(b"PARQUET-V1").hexdigest()
    cas = cas_path(tmp_path, digest)
    assert path_a.exists()
    assert os.path.samefile(path_a, cas)
    assert os.path.samefile(path_b, cas)
    assert os.stat(cas).st_nlink >= 3


@pytest.mark.cms_render
@pytest.mark.skip(reason="Unchanged pages need a real C1 render tree (UI/UX Developer)")
def test_09b_unchanged_pages_are_not_byte_copied() -> None:
    raise NotImplementedError


def test_served_observation_always_carries_citation() -> None:
    observation = make_observation()
    citation = make_citation()
    caveat = make_caveat()
    served = bind_observation(observation, citation, caveat, make_selector())
    payload = chart_payload(served)
    assert "citation" in payload
    assert payload["citation"]["citation_id"] == citation.citation_id
    assert payload["value"] == observation.value
    with pytest.raises(ValidationError):
        ServedObservation(
            observation=observation,
            citation=make_citation(citation_id="cite-other"),
            caveat=caveat,
        )


def test_hottest_rail_drops_paths_missing_from_the_catalog() -> None:
    from prism.cms_site import filter_hottest_rail

    html = (
        '<nav aria-label="Further questions" class="hottest-rail">'
        '<a href="#food">How fast is food rising?</a>'
        '<a href="/people/population">How many people live in India?</a>'
        "</nav>"
    )
    out = filter_hottest_rail(html, {"/prices/retail-prices"})
    assert 'href="#food"' in out
    assert "/people/population" not in out


def test_hottest_rail_injects_catalog_siblings() -> None:
    from prism.cms_site import apply_hottest_rail

    html = (
        '<nav class="hottest-rail" aria-label="Further questions">'
        '<a href="#food">How fast is food rising?</a>'
        "</nav>"
    )
    slices = [
        {
            "path": "/prices/retail-prices",
            "citizen_question": "How fast are retail prices rising in India, including food?",
        },
        {
            "path": "/people/population",
            "citizen_question": "How many people live in India, where, and how is that changing?",
        },
        {
            "path": "/money/union",
            "citizen_question": "What does the Union collect, and what does it spend it on?",
        },
    ]
    out = apply_hottest_rail(
        html,
        allowed_paths={item["path"] for item in slices},
        current_path="/prices/retail-prices",
        slices=slices,
    )
    assert 'href="#food"' in out
    assert 'href="/people/population"' in out
    assert 'href="/money/union"' in out
    assert out.index("#food") < out.index("/people/population")
    assert "/prices/retail-prices" not in out


def test_hottest_rail_omits_empty_sibling_group() -> None:
    from prism.cms_site import apply_hottest_rail

    html = (
        '<nav class="hottest-rail" aria-label="Further questions">'
        '<a href="#food">How fast is food rising?</a>'
        "</nav>"
    )
    slices = [
        {
            "path": "/prices/retail-prices",
            "citizen_question": "How fast are retail prices rising in India, including food?",
        }
    ]
    out = apply_hottest_rail(
        html,
        allowed_paths={"/prices/retail-prices"},
        current_path="/prices/retail-prices",
        slices=slices,
    )
    assert 'href="#food"' in out
    assert out.count("<a ") == 1


def test_fact_lede_one_line_keeps_decimal_in_first_sentence() -> None:
    from prism.cms_site import fact_lede_one_line

    text = (
        "Year-on-year inflation was 4.82 percent as of August 2026, "
        "All India Combined. Food was 2.15 percent."
    )
    assert fact_lede_one_line(text) == (
        "Year-on-year inflation was 4.82 percent as of August 2026, "
        "All India Combined."
    )


def test_preview_resolves_slashless_paths_and_unknown_to_404(tmp_path: Path) -> None:
    from functools import partial
    from http.client import HTTPConnection
    from http.server import ThreadingHTTPServer
    from threading import Thread

    from prism.preview_server import PreviewHandler, resolve_tree_path

    (tmp_path / "index.html").write_text("home", encoding="utf-8")
    nested = tmp_path / "prices" / "retail-prices"
    nested.mkdir(parents=True)
    (nested / "index.html").write_text("slice", encoding="utf-8")
    (tmp_path / "404.html").write_text(
        "<title>Page not found · Prism</title>", encoding="utf-8"
    )
    assert resolve_tree_path(tmp_path, "/").name == "index.html"
    assert (
        resolve_tree_path(tmp_path, "/prices/retail-prices").parent.name
        == "retail-prices"
    )
    assert resolve_tree_path(tmp_path, "/nope").name == "404.html"

    handler = partial(PreviewHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        conn.request("GET", "/nope")
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        assert response.status == 404
        assert "Page not found · Prism" in body
        assert response.getheader("X-Robots-Tag") == "noindex, nofollow"
        conn.request("GET", "/prices/retail-prices")
        ok = conn.getresponse()
        assert ok.status == 200
        assert ok.read().decode("utf-8") == "slice"
        conn.close()
    finally:
        server.shutdown()
        server.server_close()


def test_c1_series_ids_map_to_four_cards() -> None:
    assert C1_SERIES_IDS == (
        SERIES_CPI_GENERAL_BASE_2024,
        SERIES_CPI_CFPI_BASE_2024,
        SERIES_CPI_DIVISION_GROUP_BASE_2024,
        SERIES_CPI_BACK_SERIES_LINKED_BASE_2024,
    )
    scheduled = scheduled_series_on(CARDS_1_3_NEXT_RELEASE)
    assert [binding.card for binding in scheduled] == [1, 2, 3]
    assert scheduled_series_on(date(2026, 10, 13)) == ()


def test_publish_keeps_previous_citizen_when_render_incomplete(tmp_path: Path) -> None:
    first_desk, first = write_complete_c1_desk(tmp_path, b"PARQUET-A", CREATED_AT)
    publish_citizen(
        tmp_path,
        first_desk.desk_id,
        render_complete=True,
        contract_tests_passed=True,
    )
    later = datetime(2026, 9, 16, 10, 0, tzinfo=UTC)
    second = write_vintage(
        tmp_path,
        created_at=later,
        trigger=RefreshTrigger.source_change,
        series=(make_series_write(SERIES_CPI_GENERAL_BASE_2024, b"PARQUET-B"),),
        completeness=Completeness.complete,
        previous=first,
        required_series_ids=(SERIES_CPI_GENERAL_BASE_2024,),
    )
    second_desk = write_desk(
        tmp_path,
        created_at=later,
        slices=(
            DeskSlice(template_id=C1_TEMPLATE_ID, vintage_id=second.vintage_id),
        ),
        completeness=Completeness.complete,
    )
    with pytest.raises(PublishError, match="render is not complete"):
        publish_citizen(
            tmp_path,
            second_desk.desk_id,
            render_complete=False,
            contract_tests_passed=True,
        )
    assert read_citizen_pointer(tmp_path) == first_desk.desk_id


def test_status_value_cannot_treat_blank_as_zero() -> None:
    with pytest.raises(ValidationError):
        make_observation(value=None, status=ObservationStatus.value)
    hole = make_observation(
        value=None, status=ObservationStatus.unknown, unit="inflation (%)"
    )
    assert hole.value is None


def test_observation_rejects_invented_fields() -> None:
    payload = make_observation().model_dump()
    payload["nickname"] = "cpi"
    with pytest.raises(ValidationError):
        Observation.model_validate(payload)


def test_default_state_order_is_alphabetical_not_rank() -> None:
    from prism.serving import DEFAULT_STATE_ORDER

    assert DEFAULT_STATE_ORDER == "alphabetical_official_english_name"
