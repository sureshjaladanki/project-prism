"""Citizen serve injects origin; preview and the shared tree do not."""

from __future__ import annotations

import json
from functools import partial
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

from prism.citizen_server import CitizenHandler
from prism.preview_server import PreviewHandler
from prism.serving import (
    PREVIEW_BANNER_MARK,
    ServeError,
    canonical_href,
    inject_citizen_origin,
    inject_preview_banner,
    normalize_citizen_origin,
)

ORIGIN = "https://prism.example.test"

SLICE_HTML = """<!doctype html>
<html lang="en" data-prism-page="slice" data-prism-path="/prices/retail-prices" data-vintage-id="dv-test">
  <head>
    <title>How fast are retail prices rising in India, including food?</title>
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary" />
    <script type="application/ld+json">[{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Prism","item":"/"},{"@type":"ListItem","position":2,"name":"Prices and production","item":"/prices"},{"@type":"ListItem","position":3,"name":"How fast are retail prices rising in India, including food?"}]}]</script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
  </body>
</html>
"""

HOME_HTML = """<!doctype html>
<html lang="en" data-prism-page="home" data-prism-path="/" data-vintage-id="dv-test">
  <head>
    <title>Prism — official numbers on India</title>
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Prism"}</script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
  </body>
</html>
"""

NOTFOUND_HTML = """<!doctype html>
<html lang="en" data-prism-page="notfound">
  <head>
    <title>Page not found · Prism</title>
    <meta name="robots" content="noindex" />
  </head>
  <body></body>
</html>
"""


def test_normalize_citizen_origin_is_a_host() -> None:
    assert normalize_citizen_origin("https://prism.example.test/") == ORIGIN
    with pytest.raises(ServeError, match="host"):
        normalize_citizen_origin("https://prism.example.test/prices")
    with pytest.raises(ServeError, match="invalid"):
        normalize_citizen_origin("not-a-url")


def test_inject_adds_canonical_og_url_and_json_ld_origin() -> None:
    out = inject_citizen_origin(SLICE_HTML.encode("utf-8"), ORIGIN).decode("utf-8")
    href = canonical_href(ORIGIN, "/prices/retail-prices")
    assert f'<link rel="canonical" href="{href}" />' in out
    assert f'<meta property="og:url" content="{href}" />' in out
    payload = json.loads(
        out.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
    )
    items = payload[0]["itemListElement"]
    assert items[0]["item"] == f"{ORIGIN}/"
    assert items[1]["item"] == f"{ORIGIN}/prices"
    assert "item" not in items[2]


def test_inject_adds_website_url_and_home_canonical() -> None:
    out = inject_citizen_origin(HOME_HTML.encode("utf-8"), ORIGIN).decode("utf-8")
    assert f'<link rel="canonical" href="{ORIGIN}/" />' in out
    payload = json.loads(
        out.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
    )
    assert payload["@type"] == "WebSite"
    assert payload["url"] == ORIGIN


def test_inject_skips_canonical_on_notfound() -> None:
    out = inject_citizen_origin(NOTFOUND_HTML.encode("utf-8"), ORIGIN).decode("utf-8")
    assert 'rel="canonical"' not in out
    assert "og:url" not in out


def test_inject_is_idempotent() -> None:
    once = inject_citizen_origin(SLICE_HTML.encode("utf-8"), ORIGIN)
    twice = inject_citizen_origin(once, ORIGIN).decode("utf-8")
    assert twice.count('rel="canonical"') == 1
    assert twice.count('property="og:url"') == 1


def _serve(tmp_path: Path, handler_cls: type) -> ThreadingHTTPServer:
    handler = partial(handler_cls, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_preview_does_not_inject_origin(tmp_path: Path) -> None:
    nested = tmp_path / "prices" / "retail-prices"
    nested.mkdir(parents=True)
    (nested / "index.html").write_text(SLICE_HTML, encoding="utf-8")
    (tmp_path / "404.html").write_text(NOTFOUND_HTML, encoding="utf-8")
    server = _serve(
        tmp_path,
        type(
            "BoundPreviewHandler",
            (PreviewHandler,),
            {"preview_tree_id": "dv-test"},
        ),
    )
    try:
        conn = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        conn.request("GET", "/prices/retail-prices")
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        assert response.status == 200
        assert response.getheader("X-Robots-Tag") == "noindex, nofollow"
        assert 'rel="canonical"' not in body
        assert "og:url" not in body
        assert '"item":"/"' in body.replace(" ", "")
        assert PREVIEW_BANNER_MARK in body
        assert "Preview · not published · dv-test" in body
        conn.close()
    finally:
        server.shutdown()
        server.server_close()


def test_preview_banner_uses_tree_vintage_and_has_no_control() -> None:
    out = inject_preview_banner(SLICE_HTML.encode("utf-8"), "dv-test").decode("utf-8")
    assert 'class="preview-banner"' in out
    assert "Preview · not published · dv-test" in out
    banner = out.split('class="preview-banner">', 1)[1].split("</p>", 1)[0]
    assert "<a" not in banner
    assert "<button" not in banner
    first_anchor = out.find("<a")
    assert first_anchor != -1
    assert 'class="skip-link"' in out[first_anchor : first_anchor + 80]
    twice = inject_preview_banner(out.encode("utf-8"), "dv-test").decode("utf-8")
    assert twice.count(PREVIEW_BANNER_MARK) == 1


def test_citizen_injects_origin_from_data_prism_path(tmp_path: Path) -> None:
    nested = tmp_path / "how-this-works"
    nested.mkdir(parents=True)
    house = SLICE_HTML.replace(
        'data-prism-page="slice"', 'data-prism-page="house"'
    ).replace(
        'data-prism-path="/prices/retail-prices"',
        'data-prism-path="/how-this-works"',
    )
    (nested / "index.html").write_text(house, encoding="utf-8")
    (tmp_path / "404.html").write_text(NOTFOUND_HTML, encoding="utf-8")
    handler_cls = type(
        "BoundCitizenHandler",
        (CitizenHandler,),
        {"citizen_origin": ORIGIN},
    )
    server = _serve(tmp_path, handler_cls)
    try:
        conn = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        conn.request("GET", "/how-this-works")
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        assert response.status == 200
        assert response.getheader("X-Robots-Tag") is None
        href = canonical_href(ORIGIN, "/how-this-works")
        assert f'<link rel="canonical" href="{href}" />' in body
        assert f'<meta property="og:url" content="{href}" />' in body
        assert PREVIEW_BANNER_MARK not in body
        conn.request("GET", "/missing")
        missing = conn.getresponse()
        missing_body = missing.read().decode("utf-8")
        assert missing.status == 404
        assert 'rel="canonical"' not in missing_body
        conn.close()
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.cms_render
def test_shared_render_html_omits_canonical_and_og_url() -> None:
    from tests.test_blueprint_contract import _c1_render_dir, _c1_slice_html

    slice_html = _c1_slice_html()
    assert 'rel="canonical"' not in slice_html
    assert "og:url" not in slice_html
    assert PREVIEW_BANNER_MARK not in slice_html
    home = (_c1_render_dir() / "index.html").read_text(encoding="utf-8")
    assert 'rel="canonical"' not in home
    house = (_c1_render_dir() / "how-this-works" / "index.html").read_text(
        encoding="utf-8"
    )
    assert 'rel="canonical"' not in house
    assert "og:url" not in house
    assert 'data-prism-path="/how-this-works"' in house
    assert "High or low, good or bad" in house
    assert "4.82" not in house
    sources = (_c1_render_dir() / "sources" / "index.html").read_text(encoding="utf-8")
    assert 'data-prism-path="/sources"' in sources
    assert 'rel="canonical"' not in sources
    assert "How fast are retail prices rising in India, including food?" in sources
    assert "4.82" not in sources
    assert 'href="/prices/retail-prices"' in sources
