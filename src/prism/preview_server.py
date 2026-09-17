"""Local unpublished preview: noindex, not the citizen prefix."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from prism.serving import PREVIEW_HEADERS, ServeError, resolve_preview_render


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        for name, value in PREVIEW_HEADERS.items():
            self.send_header(name, value)
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def serve_preview(data_root: Path, host: str, port: int) -> None:
    root = resolve_preview_render(data_root)
    if not root.exists():
        raise ServeError("preview render tree is missing")
    handler = partial(PreviewHandler, directory=str(root))
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()
