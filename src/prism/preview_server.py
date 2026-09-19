"""Local unpublished preview: noindex, not the citizen prefix."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from prism.serving import (
    PREVIEW_HEADERS,
    ServeError,
    resolve_preview_render,
    resolve_tree_path,
    served_tree_file,
    slashless_redirect,
)

__all__ = ["PreviewHandler", "resolve_tree_path", "serve_preview"]


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        for name, value in PREVIEW_HEADERS.items():
            self.send_header(name, value)
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        location = slashless_redirect(self.path)
        if location is not None:
            self.send_response(301)
            self.send_header("Location", location)
            self.end_headers()
            return
        super().do_GET()

    def send_head(self) -> BytesIO | BinaryIO | None:
        root = Path(self.directory).resolve()
        served = served_tree_file(root, self.path, origin=None)
        if served is None:
            self.send_error(404, "File not found")
            return None
        status, path, body = served
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return BytesIO(body)


def serve_preview(data_root: Path, host: str, port: int) -> None:
    root = resolve_preview_render(data_root)
    if not root.exists():
        raise ServeError("preview render tree is missing")
    handler = partial(PreviewHandler, directory=str(root))
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()
