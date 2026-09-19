"""Parser and mapper registries. Filled by ingest/pipeline modules, not by YAML."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from prism.schema import GeographyVintage, Observation, ObservationLineage

MapperFn = Callable[
    [list[dict[str, str]], str, str, str, GeographyVintage, ObservationLineage],
    tuple[Observation, ...],
]


@dataclass(frozen=True)
class ParserSpec:
    parse: Callable[[bytes], Any]
    lineage_name: str
    kind: str


@dataclass(frozen=True)
class MapperSpec:
    map_rows: MapperFn
    version: str


PARSERS: dict[str, ParserSpec] = {}
MAPPERS: dict[str, MapperSpec] = {}


def register_parser(parser_id: str, spec: ParserSpec) -> None:
    PARSERS[parser_id] = spec


def register_mapper(mapper_id: str, spec: MapperSpec) -> None:
    MAPPERS[mapper_id] = spec
