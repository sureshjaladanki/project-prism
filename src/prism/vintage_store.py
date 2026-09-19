"""Immutable vintage directories. Unchanged series are hard-linked from cas, never copied."""

from __future__ import annotations

import hashlib
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from prism.paths import (
    CAVEAT_FILENAME,
    CITATION_FILENAME,
    GEOGRAPHY_FILENAME,
    MANIFEST_FILENAME,
    OBSERVATIONS_FILENAME,
    cas_dir,
    cas_path,
    vintage_dir,
    vintages_dir,
)
from prism.refresh import (
    VINTAGE_ID_PATTERN,
    ensure_utc,
    lineage_blocks_completeness,
    vintage_id_for,
)
from prism.schema import (
    CaveatNote,
    Citation,
    Completeness,
    GeographyVintage,
    InputManifest,
    RefreshTrigger,
    SeriesManifestEntry,
    VintageManifest,
    YesNo,
    canonical_json_bytes,
)


class VintageStoreError(ValueError):
    pass


@dataclass(frozen=True)
class SeriesWrite:
    producer: str
    series_id: str
    source_vintage: str
    raw_checksum: str
    parser_version: str
    lineage_ok: YesNo
    geography_vintage: str
    geography_frame_id: str
    caveat_id: str
    mapper_version: str
    observations_parquet: bytes
    citation: Citation
    caveat: CaveatNote
    geography: GeographyVintage


def payload_checksum(
    observations_parquet: bytes,
    citation: Citation,
    caveat: CaveatNote,
    geography: GeographyVintage,
) -> str:
    parts = (
        observations_parquet,
        canonical_json_bytes(citation),
        canonical_json_bytes(caveat),
        canonical_json_bytes(geography),
    )
    digest = hashlib.sha256()
    for part in parts:
        digest.update(hashlib.sha256(part).digest())
    return digest.hexdigest()


def cas_put(data_root: Path, payload: bytes) -> str:
    digest = hashlib.sha256(payload).hexdigest()
    dest = cas_path(data_root, digest)
    cas_dir(data_root).mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return digest
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{digest}.", suffix=".tmp", dir=cas_dir(data_root)
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        os.replace(tmp_name, dest)
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise
    return digest


def _install_from_cas(data_root: Path, payload: bytes, dest: Path) -> None:
    digest = cas_put(data_root, payload)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise VintageStoreError(f"refusing to overwrite {dest.as_posix()}")
    os.link(cas_path(data_root, digest), dest)


def _previous_checksums(manifest: VintageManifest | None) -> dict[str, str]:
    if manifest is None:
        return {}
    return {entry.series_id: entry.payload_checksum for entry in manifest.series}


def write_vintage(
    data_root: Path,
    *,
    created_at: datetime,
    trigger: RefreshTrigger,
    series: tuple[SeriesWrite, ...],
    completeness: Completeness,
    previous: VintageManifest | None,
    required_series_ids: tuple[str, ...],
) -> VintageManifest:
    created_at = ensure_utc(created_at)
    if not series:
        raise VintageStoreError("a vintage must list at least one series")
    if completeness is Completeness.complete:
        present = {item.series_id: item for item in series}
        missing = [
            series_id for series_id in required_series_ids if series_id not in present
        ]
        if missing:
            raise VintageStoreError(
                "complete vintage missing required series: " + ", ".join(missing)
            )
        blocked = [
            series_id
            for series_id in required_series_ids
            if lineage_blocks_completeness(series_id, present[series_id].lineage_ok)
        ]
        if blocked:
            raise VintageStoreError(
                "complete vintage requires lineage_ok for: " + ", ".join(blocked)
            )

    previous_checksums = _previous_checksums(previous)
    entries: list[SeriesManifestEntry] = []
    for item in series:
        if item.citation.citation_id == "" or item.caveat.caveat_id == "":
            raise VintageStoreError("citation_id and caveat_id are required")
        if item.geography.geography_vintage == "":
            raise VintageStoreError("geography.geography_vintage is required")
        if item.caveat.caveat_id != item.caveat_id:
            raise VintageStoreError("caveat_id does not match the caveat note")
        checksum = payload_checksum(
            item.observations_parquet, item.citation, item.caveat, item.geography
        )
        reused = (
            YesNo.yes
            if previous_checksums.get(item.series_id) == checksum
            else YesNo.no
        )
        entries.append(
            SeriesManifestEntry(
                producer=item.producer,
                series_id=item.series_id,
                source_vintage=item.source_vintage,
                raw_checksum=item.raw_checksum,
                parser_version=item.parser_version,
                lineage_ok=item.lineage_ok,
                geography_vintage=item.geography_vintage,
                geography_frame_id=item.geography_frame_id,
                payload_checksum=checksum,
                reused=reused,
                caveat_id=item.caveat_id,
                mapper_version=item.mapper_version,
            )
        )

    input_manifest = InputManifest(
        created_at=created_at, trigger=trigger, series=tuple(entries)
    )
    vintage_id = vintage_id_for(created_at.date(), input_manifest)
    dest = vintage_dir(data_root, vintage_id)
    if dest.exists():
        raise VintageStoreError(f"vintage {vintage_id} is immutable and already exists")

    vintages_dir(data_root).mkdir(parents=True, exist_ok=True)
    tmp = vintages_dir(data_root) / f".tmp-{vintage_id}"
    if tmp.exists():
        raise VintageStoreError(f"stale temp vintage directory at {tmp.as_posix()}")
    tmp.mkdir()
    try:
        for item in series:
            series_tmp = tmp / "series" / item.series_id
            _install_from_cas(
                data_root, item.observations_parquet, series_tmp / OBSERVATIONS_FILENAME
            )
            _install_from_cas(
                data_root,
                canonical_json_bytes(item.citation),
                series_tmp / CITATION_FILENAME,
            )
            _install_from_cas(
                data_root,
                canonical_json_bytes(item.caveat),
                series_tmp / CAVEAT_FILENAME,
            )
            _install_from_cas(
                data_root,
                canonical_json_bytes(item.geography),
                series_tmp / GEOGRAPHY_FILENAME,
            )
        manifest = VintageManifest(
            vintage_id=vintage_id,
            created_at=created_at,
            trigger=trigger,
            series=tuple(entries),
            completeness=completeness,
        )
        (tmp / MANIFEST_FILENAME).write_bytes(canonical_json_bytes(manifest))
        tmp.rename(dest)
    except Exception:
        _remove_tree(tmp)
        raise
    return manifest


def load_manifest(data_root: Path, vintage_id: str) -> VintageManifest:
    path = vintage_dir(data_root, vintage_id) / MANIFEST_FILENAME
    return VintageManifest.model_validate_json(path.read_bytes())


def list_manifests(data_root: Path) -> tuple[VintageManifest, ...]:
    root = vintages_dir(data_root)
    if not root.exists():
        return ()
    manifests: list[VintageManifest] = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or VINTAGE_ID_PATTERN.fullmatch(path.name) is None:
            continue
        manifests.append(load_manifest(data_root, path.name))
    return tuple(manifests)


def latest_manifest(data_root: Path) -> VintageManifest | None:
    manifests = list_manifests(data_root)
    if not manifests:
        return None
    return max(manifests, key=lambda item: item.created_at)


def latest_manifest_with_series(
    data_root: Path, series_ids: tuple[str, ...]
) -> VintageManifest | None:
    matches = [
        item
        for item in list_manifests(data_root)
        if {entry.series_id for entry in item.series} == set(series_ids)
    ]
    if not matches:
        return None
    return max(matches, key=lambda item: item.created_at)


def _remove_tree(path: Path) -> None:
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            child.rmdir()
    path.rmdir()
