"""Parser and mapper registries. Filled by ingest/pipeline modules, not by YAML."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

from prism.schema import GeographyVintage, Observation, ObservationLineage

MapperFn = Callable[
    [list[dict[str, str]], str, str, str, GeographyVintage, ObservationLineage],
    tuple[Observation, ...],
]

# RetrievedArtifact is defined in ingest.retrieve; keep the type loose here.
RetrieverFn = Callable[[httpx.Client, str, str], Any]


@dataclass(frozen=True)
class ParserSpec:
    parse: Callable[[bytes], Any]
    lineage_name: str
    kind: str


@dataclass(frozen=True)
class MapperSpec:
    map_rows: MapperFn
    version: str


@dataclass(frozen=True)
class RetrieverSpec:
    retrieve: RetrieverFn
    filename: str


PARSERS: dict[str, ParserSpec] = {}
MAPPERS: dict[str, MapperSpec] = {}
RETRIEVERS: dict[str, RetrieverSpec] = {}


def register_parser(parser_id: str, spec: ParserSpec) -> None:
    PARSERS[parser_id] = spec


def register_mapper(mapper_id: str, spec: MapperSpec) -> None:
    MAPPERS[mapper_id] = spec


def register_retriever(retrieve_id: str, spec: RetrieverSpec) -> None:
    RETRIEVERS[retrieve_id] = spec
