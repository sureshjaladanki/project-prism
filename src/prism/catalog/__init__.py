"""Typed catalog: slice identity and wiring. Parsers and mappers stay Python."""

from __future__ import annotations

from collections import Counter
from datetime import date
from functools import lru_cache
from importlib import import_module
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from prism.catalog.registry import MAPPERS, PARSERS
from prism.schema import CaveatNote, Citation, GeographyVintage

_REGISTRY_MODULES = (
    "prism.ingest.xlsx_cpi_period",
    "prism.ingest.census_srs_xlsx_pdf",
    "prism.ingest.budget_cga_xlsx_pdf_html",
    "prism.pipeline.state_sector_period",
    "prism.pipeline.census_srs_ncp",
    "prism.pipeline.wide_measure_columns",
)


class CatalogError(ValueError):
    pass


class CatalogCompanion(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    url: str
    headers_name: str = "annex_headers.json"


class CatalogArtifact(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str
    url: str
    kind: Literal["xlsx", "xls", "pdf", "html"]
    share_note: str = ""
    companions: tuple[CatalogCompanion, ...] = ()


class CatalogSeries(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    series_id: str
    card: int
    name: str
    producer: str
    producer_slug: str
    source_vintage: str
    next_release: date | Literal["unknown"]
    geography_frame_id: str
    geography_vintage: str
    citation_id: str
    caveat_id: str
    artifact_id: str
    parser_id: str
    mapper_id: str
    named_hole: bool = False


class CatalogCiteBlock(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    block_id: str
    citation_ids: tuple[str, ...]
    observation_slots: tuple[str, ...] = ()

    @model_validator(mode="after")
    def citation_ids_present(self) -> CatalogCiteBlock:
        if not self.citation_ids:
            raise ValueError(f"{self.block_id} has no citation_ids")
        return self


class CatalogSlice(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    slice_id: str
    charter: str
    template_id: str
    artifacts: tuple[CatalogArtifact, ...]
    series: tuple[CatalogSeries, ...]
    cite_blocks: tuple[CatalogCiteBlock, ...] = ()

    @model_validator(mode="after")
    def artifacts_cover_series(self) -> CatalogSlice:
        ids = {artifact.artifact_id for artifact in self.artifacts}
        for entry in self.series:
            if entry.artifact_id not in ids:
                raise ValueError(
                    f"{entry.series_id} artifact_id {entry.artifact_id} is not on this slice"
                )
        return self

    def artifact(self, artifact_id: str) -> CatalogArtifact:
        for item in self.artifacts:
            if item.artifact_id == artifact_id:
                return item
        raise CatalogError(f"unknown artifact_id: {artifact_id}")

    def series_by_id(self) -> dict[str, CatalogSeries]:
        return {entry.series_id: entry for entry in self.series}

    def cite_block_by_id(self) -> dict[str, CatalogCiteBlock]:
        return {block.block_id: block for block in self.cite_blocks}


class Catalog(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    slices: tuple[CatalogSlice, ...]
    citations: dict[str, Citation] = Field(default_factory=dict)
    caveats: dict[str, CaveatNote] = Field(default_factory=dict)
    geographies: dict[str, GeographyVintage] = Field(default_factory=dict)

    def slice(self, slice_id: str) -> CatalogSlice:
        for item in self.slices:
            if item.slice_id == slice_id:
                return item
        raise CatalogError(f"unknown slice_id: {slice_id}")

    def series(self, series_id: str) -> CatalogSeries:
        for item in self.slices:
            found = item.series_by_id().get(series_id)
            if found is not None:
                return found
        raise CatalogError(f"unknown series_id: {series_id}")

    def slice_for_series(self, series_id: str) -> CatalogSlice:
        for item in self.slices:
            if series_id in item.series_by_id():
                return item
        raise CatalogError(f"unknown series_id: {series_id}")

    def slice_for_template(self, template_id: str) -> CatalogSlice:
        for item in self.slices:
            if item.template_id == template_id:
                return item
        raise CatalogError(f"unknown template_id: {template_id}")

    def artifact(self, artifact_id: str) -> CatalogArtifact:
        for item in self.slices:
            for art in item.artifacts:
                if art.artifact_id == artifact_id:
                    return art
        raise CatalogError(f"unknown artifact_id: {artifact_id}")

    def series_ids(self) -> tuple[str, ...]:
        return tuple(entry.series_id for item in self.slices for entry in item.series)

    def named_hole_series_ids(self) -> frozenset[str]:
        return frozenset(
            entry.series_id
            for item in self.slices
            for entry in item.series
            if entry.named_hole
        )

    def named_hole_citation_ids(self) -> frozenset[str]:
        return frozenset(
            entry.citation_id
            for item in self.slices
            for entry in item.series
            if entry.named_hole
        )


def ensure_registries() -> None:
    for name in _REGISTRY_MODULES:
        import_module(name)


def _join(package: str, *parts: str) -> Traversable:
    root = files(package)
    for part in parts:
        root = root.joinpath(part)
    return root


def _load_yaml_models(
    directory: Path | Traversable,
    model: type[Citation | CaveatNote | GeographyVintage],
) -> dict[str, Citation | CaveatNote | GeographyVintage]:
    loaded: dict[str, Citation | CaveatNote | GeographyVintage] = {}
    if isinstance(directory, Path):
        if not directory.is_dir():
            return loaded
        children = sorted(directory.glob("*.yaml"))
        for path in children:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            loaded[path.stem] = model.model_validate(payload)
        return loaded
    if not directory.is_dir():
        return loaded
    for child in sorted(directory.iterdir(), key=lambda item: item.name):
        if not child.name.endswith(".yaml"):
            continue
        payload = yaml.safe_load(child.read_text(encoding="utf-8"))
        loaded[child.name.removesuffix(".yaml")] = model.model_validate(payload)
    return loaded


def _slice_from_text(text: str) -> CatalogSlice:
    return CatalogSlice.model_validate(yaml.safe_load(text))


def _package_slices() -> tuple[CatalogSlice, ...]:
    root = _join("prism.catalog", "slices")
    slices: list[CatalogSlice] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.name.endswith(".yaml"):
            slices.append(_slice_from_text(child.read_text(encoding="utf-8")))
    return tuple(slices)


def load_catalog(
    *,
    extra_slices: tuple[Path, ...] = (),
    extra_cards: Path | None = None,
    require_registries: bool = True,
) -> Catalog:
    if require_registries:
        ensure_registries()
    slices = _package_slices() + tuple(
        _slice_from_text(path.read_text(encoding="utf-8")) for path in extra_slices
    )
    package_cards = _join("prism.catalog", "cards")
    citations = {
        key: value
        for key, value in _load_yaml_models(
            package_cards / "citations", Citation
        ).items()
        if isinstance(value, Citation)
    }
    caveats = {
        key: value
        for key, value in _load_yaml_models(
            package_cards / "caveats", CaveatNote
        ).items()
        if isinstance(value, CaveatNote)
    }
    geographies = {
        key: value
        for key, value in _load_yaml_models(
            package_cards / "geographies", GeographyVintage
        ).items()
        if isinstance(value, GeographyVintage)
    }
    if extra_cards is not None:
        citations.update(
            {
                key: value
                for key, value in _load_yaml_models(
                    extra_cards / "citations", Citation
                ).items()
                if isinstance(value, Citation)
            }
        )
        caveats.update(
            {
                key: value
                for key, value in _load_yaml_models(
                    extra_cards / "caveats", CaveatNote
                ).items()
                if isinstance(value, CaveatNote)
            }
        )
        geographies.update(
            {
                key: value
                for key, value in _load_yaml_models(
                    extra_cards / "geographies", GeographyVintage
                ).items()
                if isinstance(value, GeographyVintage)
            }
        )
    catalog = Catalog(
        slices=slices,
        citations=citations,
        caveats=caveats,
        geographies=geographies,
    )
    validate_catalog(catalog, require_registries=require_registries)
    return catalog


def validate_catalog(catalog: Catalog, *, require_registries: bool = True) -> None:
    series_ids = [entry.series_id for item in catalog.slices for entry in item.series]
    dupes = [key for key, count in Counter(series_ids).items() if count > 1]
    if dupes:
        raise CatalogError("duplicate series_id: " + ", ".join(sorted(dupes)))
    slice_ids = [item.slice_id for item in catalog.slices]
    slice_dupes = [key for key, count in Counter(slice_ids).items() if count > 1]
    if slice_dupes:
        raise CatalogError("duplicate slice_id: " + ", ".join(sorted(slice_dupes)))
    for item in catalog.slices:
        artifact_ids = [artifact.artifact_id for artifact in item.artifacts]
        artifact_dupes = [
            key for key, count in Counter(artifact_ids).items() if count > 1
        ]
        if artifact_dupes:
            raise CatalogError(
                f"duplicate artifact_id on {item.slice_id}: "
                + ", ".join(sorted(artifact_dupes))
            )
        for entry in item.series:
            if require_registries and entry.parser_id not in PARSERS:
                raise CatalogError(
                    f"{entry.series_id} unknown parser_id: {entry.parser_id}"
                )
            if require_registries and entry.mapper_id not in MAPPERS:
                raise CatalogError(
                    f"{entry.series_id} unknown mapper_id: {entry.mapper_id}"
                )
            if entry.citation_id not in catalog.citations:
                raise CatalogError(
                    f"{entry.series_id} missing citation_id: {entry.citation_id}"
                )
            if entry.caveat_id not in catalog.caveats:
                raise CatalogError(
                    f"{entry.series_id} missing caveat_id: {entry.caveat_id}"
                )
            if entry.series_id not in catalog.geographies:
                raise CatalogError(f"{entry.series_id} missing geography card")
            citation = catalog.citations[entry.citation_id]
            caveat = catalog.caveats[entry.caveat_id]
            if citation.citation_id != entry.citation_id:
                raise CatalogError(f"{entry.series_id} citation file id mismatch")
            if caveat.caveat_id != entry.caveat_id:
                raise CatalogError(f"{entry.series_id} caveat file id mismatch")
        slice_citations = {entry.citation_id for entry in item.series}
        block_ids = [block.block_id for block in item.cite_blocks]
        block_dupes = [key for key, count in Counter(block_ids).items() if count > 1]
        if block_dupes:
            raise CatalogError(
                f"duplicate cite block_id on {item.slice_id}: "
                + ", ".join(sorted(block_dupes))
            )
        for block in item.cite_blocks:
            for citation_id in block.citation_ids:
                if citation_id not in catalog.citations:
                    raise CatalogError(
                        f"cite-block {block.block_id} missing citation_id: {citation_id}"
                    )
                if citation_id not in slice_citations:
                    raise CatalogError(
                        f"cite-block {block.block_id} citation_id {citation_id} "
                        f"is not on {item.slice_id}"
                    )


@lru_cache(maxsize=1)
def default_catalog() -> Catalog:
    return load_catalog()


def list_catalog_rows() -> tuple[tuple[str, str, str, str], ...]:
    catalog = default_catalog()
    rows: list[tuple[str, str, str, str]] = []
    for item in catalog.slices:
        for entry in item.series:
            rows.append(
                (item.slice_id, entry.series_id, entry.parser_id, entry.mapper_id)
            )
    return tuple(rows)


def slice_citations(slice_id: str) -> dict[str, Citation]:
    catalog = default_catalog()
    return {
        entry.series_id: catalog.citations[entry.citation_id]
        for entry in catalog.slice(slice_id).series
    }


def slice_caveats(slice_id: str) -> dict[str, CaveatNote]:
    catalog = default_catalog()
    return {
        entry.series_id: catalog.caveats[entry.caveat_id]
        for entry in catalog.slice(slice_id).series
    }


def slice_geographies(slice_id: str) -> dict[str, GeographyVintage]:
    catalog = default_catalog()
    return {
        entry.series_id: catalog.geographies[entry.series_id]
        for entry in catalog.slice(slice_id).series
    }


def names_by_code(series_id: str) -> dict[str, str]:
    frame = default_catalog().geographies[series_id]
    return {unit.code: unit.name_en for unit in frame.units_included}
