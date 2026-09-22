"""Catalog spine, validate CLI, and Track A guards."""

from __future__ import annotations

import ast
import csv
import io
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
import yaml
from typer.testing import CliRunner

from prism.catalog import (
    CatalogCiteBlock,
    CatalogError,
    default_catalog,
    load_catalog,
    validate_catalog,
)
from prism.catalog.registry import (
    MapperSpec,
    ParserSpec,
    register_mapper,
    register_parser,
)
from prism.cli import app
from prism.citizen_projection import denomination_from_unit
from prism.ingest.parsed_table import ParsedTable
from prism.ingest.run import ingest
from prism.pipeline.run import materialise_vintage
from prism.schema import (
    CaveatNote,
    CodeSystem,
    Completeness,
    GeographyRef,
    GeographyUnit,
    GeographyVintage,
    Observation,
    ObservationLineage,
    ObservationStatus,
    YesNo,
)
from tests.factories import CREATED_AT


def test_catalog_validate_cli_ok() -> None:
    result = CliRunner().invoke(app, ["catalog", "validate"])
    assert result.exit_code == 0
    assert "catalog ok" in result.stdout


def test_every_catalog_caveat_has_citizen_note() -> None:
    catalog = default_catalog()
    assert catalog.caveats
    for caveat_id, note in catalog.caveats.items():
        assert note.citizen_note, f"{caveat_id} missing citizen_note"


def test_cite_blocks_live_on_slice_yaml() -> None:
    catalog = default_catalog()
    c1 = catalog.slice_for_template("c1-prices-people-pay")
    assert c1.cite_block_by_id()["general-latest"].citation_ids == (
        "cite-c1-cpi-general-base-2024-2026-08",
    )
    bind_src = Path(__file__).resolve().parents[1] / "src" / "prism" / "template_bind.py"
    assert "CITE_BLOCKS" not in bind_src.read_text(encoding="utf-8")


def test_catalog_rejects_unknown_cite_block_citation() -> None:
    catalog = default_catalog()
    first = catalog.slices[0]
    broken = catalog.model_copy(
        update={
            "slices": (
                first.model_copy(
                    update={
                        "cite_blocks": first.cite_blocks
                        + (
                            CatalogCiteBlock(
                                block_id="ghost",
                                citation_ids=("cite-does-not-exist",),
                            ),
                        )
                    }
                ),
            )
            + catalog.slices[1:]
        }
    )
    with pytest.raises(CatalogError, match="missing citation_id"):
        validate_catalog(broken)


def test_catalog_validate_unknown_parser() -> None:
    catalog = default_catalog()
    first = catalog.slices[0]
    broken = catalog.model_copy(
        update={
            "slices": (
                first.model_copy(
                    update={
                        "series": (
                            first.series[0].model_copy(
                                update={"parser_id": "not-a-parser"}
                            ),
                        )
                        + first.series[1:]
                    }
                ),
            )
            + catalog.slices[1:]
        }
    )
    with pytest.raises(CatalogError, match="unknown parser_id"):
        validate_catalog(broken)


def test_catalog_validate_duplicate_series() -> None:
    catalog = default_catalog()
    first = catalog.slices[0]
    broken = catalog.model_copy(
        update={
            "slices": (
                first.model_copy(update={"series": first.series + first.series[:1]}),
            )
            + catalog.slices[1:]
        }
    )
    with pytest.raises(CatalogError, match="duplicate series_id"):
        validate_catalog(broken)


def test_catalog_validate_missing_citation() -> None:
    catalog = default_catalog()
    first = catalog.slices[0]
    broken = catalog.model_copy(
        update={
            "slices": (
                first.model_copy(
                    update={
                        "series": (
                            first.series[0].model_copy(
                                update={"citation_id": "cite-missing"}
                            ),
                        )
                        + first.series[1:]
                    }
                ),
            )
            + catalog.slices[1:]
        }
    )
    with pytest.raises(CatalogError, match="missing citation_id"):
        validate_catalog(broken)


def _parse_fixture(payload: bytes) -> ParsedTable:
    del payload
    text = "value\n3\n"
    rows = list(csv.DictReader(io.StringIO(text)))
    return ParsedTable(
        csv_text=text,
        row_count=len(rows),
        nulls="none",
        lineage_ok=YesNo.yes,
        flags="none",
    )


def test_fixture_slice_generic_runners(tmp_path: Path) -> None:
    def map_rows(
        rows: list[dict[str, str]],
        series_id: str,
        citation_id: str,
        caveat_id: str,
        geography: GeographyVintage,
        lineage: ObservationLineage,
    ) -> tuple[Observation, ...]:
        unit = geography.units_included[0]
        return (
            Observation(
                observation_id=f"obs-{series_id}-{unit.code}-total-2024-count",
                series_id=series_id,
                citation_id=citation_id,
                caveat_id=caveat_id,
                geography=GeographyRef(
                    code=unit.code,
                    geography_vintage=geography.geography_vintage,
                    code_system=geography.code_system,
                ),
                sector="Total",
                reference_period="2024",
                value=float(rows[0]["value"]),
                unit="count",
                denomination=denomination_from_unit("count"),
                status=ObservationStatus.value,
                lineage=lineage,
            ),
        )

    register_parser(
        "fixture-csv",
        ParserSpec(parse=_parse_fixture, lineage_name="fixture-csv-1.0.0", kind="html"),
    )
    register_mapper(
        "fixture-identity",
        MapperSpec(map_rows=map_rows, version="fixture-1.0.0"),
    )
    slices = tmp_path / "slices"
    slices.mkdir()
    (slices / "fx.yaml").write_text(
        """
slice_id: fx
charter: FX
template_id: fx-template
artifacts:
  - artifact_id: fixture-table
    url: https://example.gov/table.csv
    kind: html
    share_note: ""
    companions: []
series:
  - series_id: fixture-count
    card: 1
    name: Fixture count
    producer: Fixture Office
    producer_slug: fixture
    source_vintage: "2024"
    next_release: unknown
    geography_frame_id: fx-frame
    geography_vintage: "2024"
    citation_id: cite-fixture-count
    caveat_id: caveat-fixture-count
    artifact_id: fixture-table
    parser_id: fixture-csv
    mapper_id: fixture-identity
    named_hole: false
""",
        encoding="utf-8",
    )
    cards = tmp_path / "cards"
    (cards / "citations").mkdir(parents=True)
    (cards / "caveats").mkdir()
    (cards / "geographies").mkdir()
    (cards / "citations" / "cite-fixture-count.yaml").write_text(
        "citation_id: cite-fixture-count\n"
        "producer: Fixture Office\n"
        "series: Fixture count\n"
        "id: table.csv\n"
        "reference_period: '2024'\n"
        "release_date: unknown\n"
        "url: https://example.gov/table.csv\n"
        "geography_as_published: Fixture land\n"
        "frequency: annual\n"
        "licence: not stated\n"
        "next_release: unknown\n"
        "caveat_one_line: A fixture.\n",
        encoding="utf-8",
    )
    (cards / "caveats" / "caveat-fixture-count.yaml").write_text(
        yaml.safe_dump(
            CaveatNote(
                caveat_id="caveat-fixture-count",
                concept="count",
                unit="count",
                population="fixture",
                reference_period="2024",
                producer_definition="fixture table",
                comparable_from="2024",
                breaks="none",
                lags="none",
                disagrees_with="none",
                do_not="do not treat as official",
                citizen_note="A fixture count from a fixture table.",
            ).model_dump(mode="json")
        ),
        encoding="utf-8",
    )
    (cards / "geographies" / "fixture-count.yaml").write_text(
        yaml.safe_dump(
            GeographyVintage(
                frame_id="fx-frame",
                geography_vintage="2024",
                code_system=CodeSystem.none,
                frame="Union",
                units_included=(
                    GeographyUnit(
                        code="fx", name_en="Fixture", geography_vintage="2024"
                    ),
                ),
                units_missing=("none",),
                breaks="none",
                crosswalk="none",
            ).model_dump(mode="json")
        ),
        encoding="utf-8",
    )
    extra = load_catalog(
        extra_slices=(slices / "fx.yaml",), extra_cards=cards, require_registries=True
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"<!DOCTYPE html><html></html>",
            headers={"content-type": "text/html"},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    data_root = tmp_path / "data"
    records = ingest(
        data_root,
        client=client,
        retrieved_at=datetime(2026, 9, 19, 8, 0, tzinfo=UTC),
        series_ids=("fixture-count",),
        catalog=extra,
    )
    assert records[0].lineage_ok is YesNo.yes
    manifest, _report = materialise_vintage(
        data_root,
        tmp_path / "logs",
        slice_id="fx",
        created_at=CREATED_AT,
        catalog=extra,
    )
    assert manifest.completeness is Completeness.complete
    assert [entry.series_id for entry in manifest.series] == ["fixture-count"]


def test_pipeline_does_not_import_httpx_or_retrieve() -> None:
    root = Path("src/prism/pipeline")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            for name in names:
                assert name != "httpx", path
                assert not name.startswith("prism.ingest.retrieve"), path


def test_ingest_does_not_import_observation() -> None:
    root = Path("src/prism/ingest")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "prism.schema":
                imported = {alias.name for alias in node.names}
                assert "Observation" not in imported, path
            if isinstance(node, ast.ImportFrom) and node.module == "prism.pipeline":
                raise AssertionError(path)
