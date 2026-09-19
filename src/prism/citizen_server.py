"""Local citizen-view: published pointer, origin-bearing head tags."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from prism.serving import (
    ServeError,
    normalize_citizen_origin,
    resolve_citizen_render,
    served_tree_file,
    slashless_redirect,
)


class CitizenHandler(SimpleHTTPRequestHandler):
    citizen_origin: str = ""

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
        served = served_tree_file(root, self.path, origin=self.citizen_origin)
        if served is None:
            self.send_error(404, "File not found")
            return None
        status, path, body = served
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return BytesIO(body)


def serve_citizen(data_root: Path, host: str, port: int, origin: str) -> None:
    root = resolve_citizen_render(data_root)
    if not root.exists():
        raise ServeError("citizen render tree is missing")
    bound_origin = normalize_citizen_origin(origin)
    handler_cls = type(
        "BoundCitizenHandler",
        (CitizenHandler,),
        {"citizen_origin": bound_origin},
    )
    handler = partial(handler_cls, directory=str(root))
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()
