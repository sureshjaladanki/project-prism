"""HTTP retrieve of an official artifact. Same function every refresh."""

from __future__ import annotations

import hashlib
import json
import os
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx

from prism.paths import HEADERS_FILENAME, posix
from prism.refresh import ensure_utc

XLSX_MAGIC = b"PK\x03\x04"
PDF_MAGIC = b"%PDF"
XLS_OLE_MAGIC = b"\xd0\xcf\x11\xe0"
DEFAULT_TIMEOUT = httpx.Timeout(120.0)
USER_AGENT = "prism-ingest/1.0.0"
# desagri.gov.in serves with an expired certificate (verified 2026-09-22).
# Approved path: retry once with verify=False for these hosts only; record in headers.
INSECURE_TLS_RETRY_HOSTS = frozenset({"desagri.gov.in"})


class IngestError(ValueError):
    pass


@dataclass(frozen=True)
class RetrievedArtifact:
    url: str
    http_status: int
    content_type: str
    content: bytes
    filename: str
    checksum: str
    retrieved_at: str
    tls_mode: str = "verify"


def retrieved_at_stamp(moment: datetime | None = None) -> str:
    now = moment if moment is not None else datetime.now(UTC)
    return ensure_utc(now).strftime("%Y%m%dT%H%M%SZ")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def filename_from_url(url: str) -> str:
    name = url.rstrip("/").rsplit("/", 1)[-1]
    if name == "":
        raise IngestError(f"url has no filename: {url}")
    return name


def _system_ca_pem() -> str | None:
    enum_certificates = getattr(ssl, "enum_certificates", None)
    if enum_certificates is None:
        return None
    parts = [
        ssl.DER_cert_to_PEM_cert(der)
        for store in ("CA", "ROOT")
        for der, encoding, _trust in enum_certificates(store)
        if encoding == "x509_asn"
    ]
    if not parts:
        return None
    return "".join(parts)


def _ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    pem = _system_ca_pem()
    if pem is not None:
        context.load_verify_locations(cadata=pem)
    return context


def new_client() -> httpx.Client:
    return httpx.Client(
        follow_redirects=True,
        timeout=DEFAULT_TIMEOUT,
        headers={"User-Agent": USER_AGENT},
        verify=_ssl_context(),
    )


def _ssl_verify_failed(exc: BaseException) -> bool:
    text = str(exc).lower()
    return "certificate" in text or "ssl" in text or "tls" in text


def retrieve_artifact(
    url: str,
    *,
    client: httpx.Client,
    retrieved_at: str,
    filename: str | None = None,
) -> RetrievedArtifact:
    name = filename if filename is not None else filename_from_url(url)
    tls_mode = "verify"
    try:
        response = client.get(url)
    except httpx.ConnectError as exc:
        host = (urlparse(url).hostname or "").lower()
        if host not in INSECURE_TLS_RETRY_HOSTS or not _ssl_verify_failed(exc):
            raise
        # Approved insecure retry for hosts with broken TLS (desagri.gov.in expired cert).
        with httpx.Client(
            follow_redirects=True,
            timeout=DEFAULT_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            verify=False,
        ) as insecure:
            response = insecure.get(url)
        tls_mode = "insecure_retry"
    content_type = response.headers.get("content-type", "")
    return RetrievedArtifact(
        url=url,
        http_status=response.status_code,
        content_type=content_type,
        content=response.content,
        filename=name,
        checksum=sha256_hex(response.content),
        retrieved_at=retrieved_at,
        tls_mode=tls_mode,
    )


def is_xlsx(payload: bytes) -> bool:
    return payload.startswith(XLSX_MAGIC)


def is_pdf(payload: bytes) -> bool:
    return payload.startswith(PDF_MAGIC)


def is_xls_ole(payload: bytes) -> bool:
    return payload.startswith(XLS_OLE_MAGIC)


def is_json(payload: bytes) -> bool:
    head = payload.lstrip()[:1]
    if head not in {b"{", b"["}:
        return False
    try:
        json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    return True


def assert_payload_kind(payload: bytes, kind: str, url: str) -> None:
    if kind == "xlsx" and not is_xlsx(payload):
        raise IngestError(f"not an xlsx (magic missing) at {url}")
    if kind == "pdf" and not is_pdf(payload):
        raise IngestError(f"not a pdf (magic missing) at {url}")
    if kind == "xls" and not is_xls_ole(payload):
        raise IngestError(f"not an xls OLE compound file (magic missing) at {url}")
    if kind == "html":
        if is_pdf(payload) or is_xlsx(payload) or is_xls_ole(payload):
            raise IngestError(f"not html (office/pdf magic present) at {url}")
        head = payload.lstrip()[:2048].lower()
        if b"<html" not in head and b"<!doctype" not in head:
            raise IngestError(f"not html (no html/doctype in head) at {url}")
    if kind == "json" and not is_json(payload):
        raise IngestError(f"not json (object/array) at {url}")
    if kind not in {"xlsx", "pdf", "xls", "html", "json"}:
        raise IngestError(f"unknown artifact kind {kind} at {url}")


def write_headers(
    dest_dir: Path,
    artifact: RetrievedArtifact,
    filename: str = HEADERS_FILENAME,
) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / filename
    payload = {
        "url": artifact.url,
        "http_status": artifact.http_status,
        "content_type": artifact.content_type,
        "retrieved_at": artifact.retrieved_at,
        "filename": artifact.filename,
        "checksum": artifact.checksum,
        "tls_mode": artifact.tls_mode,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def install_file(dest: Path, payload: bytes, *, link_from: Path | None = None) -> str:
    """Write bytes, or hard-link from an existing copy of the same artifact."""

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise IngestError(f"refusing to overwrite {posix(dest)}")
    if link_from is not None:
        os.link(link_from, dest)
        return "hardlink"
    dest.write_bytes(payload)
    return "write"


def write_raw_artifact(
    dest_dir: Path,
    artifact: RetrievedArtifact,
    *,
    link_from: Path | None = None,
    headers_name: str = HEADERS_FILENAME,
    kind: str = "xlsx",
) -> tuple[Path, str]:
    write_headers(dest_dir, artifact, headers_name)
    if artifact.http_status != 200:
        raise IngestError(
            f"http_{artifact.http_status} for {artifact.url}; not substituting another file"
        )
    assert_payload_kind(artifact.content, kind, artifact.url)
    artifact_path = dest_dir / artifact.filename
    how = install_file(artifact_path, artifact.content, link_from=link_from)
    return artifact_path, how
