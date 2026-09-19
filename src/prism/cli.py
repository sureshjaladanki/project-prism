"""Typer CLI: ingest → vintage → render. Citizen publish waits for Trust Auditor."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer

from prism.citizen_server import serve_citizen
from prism.desk_store import (
    DeskStoreError,
    preview_slices,
    slices_from_cli,
    write_desk,
)
from prism.ingest import ingest as run_ingest
from prism.ingest.retrieve import IngestError
from prism.pipeline import PipelineError, materialise_vintage
from prism.pointer_store import (
    PublishError,
    publish_citizen,
    publish_preview,
    read_preview_pointer,
)
from prism.preview_server import serve_preview
from prism.refresh import lineage_record_blocks_completeness
from prism.render import render
from prism.schema import Completeness, LineageRecord
from prism.serving import ServeError
from prism.template_bind import RenderError
from prism.vintage_store import VintageStoreError

app = typer.Typer(no_args_is_help=True, help="Prism: ingest, vintage, render, publish.")


@app.callback()
def main() -> None:
    """Prism CLI. Citizen publish is not this command."""


def _report_lineage(records: tuple[LineageRecord, ...]) -> None:
    failed = False
    for record in records:
        typer.echo(
            f"{record.citation_id} lineage_ok={record.lineage_ok.value} "
            f"source_changed={record.source_changed.value} parser={record.parser} "
            f"rows={record.row_count}"
        )
        typer.echo(f"  raw={record.raw_path}")
        typer.echo(f"  derived={record.derived_path}")
        typer.echo(f"  checksum={record.checksum}")
        typer.echo(f"  nulls={record.nulls}")
        typer.echo(f"  flags={record.flags}")
        if lineage_record_blocks_completeness(record):
            failed = True
    if failed:
        raise typer.Exit(code=1)


@app.command("ingest")
def ingest_cmd(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    series_id: Annotated[list[str] | None, typer.Option("--series-id")] = None,
) -> None:
    """Retrieve locked series into data/. Omit --series-id to ingest C1, C2, and C3."""

    try:
        records = run_ingest(
            data_root, series_ids=tuple(series_id) if series_id else None
        )
    except IngestError as exc:
        typer.echo(f"ingest failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    _report_lineage(records)


catalog_app = typer.Typer(help="List and validate the typed catalog.")
app.add_typer(catalog_app, name="catalog")


@catalog_app.command("list")
def catalog_list() -> None:
    from prism.catalog import list_catalog_rows

    for slice_id, series_id, parser_id, mapper_id in list_catalog_rows():
        typer.echo(f"{slice_id}\t{series_id}\t{parser_id}\t{mapper_id}")


@catalog_app.command("validate")
def catalog_validate() -> None:
    from prism.catalog import CatalogError, default_catalog

    try:
        catalog = default_catalog()
    except CatalogError as exc:
        typer.echo(f"catalog invalid: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(
        f"catalog ok slices={len(catalog.slices)} series={len(catalog.series_ids())}"
    )


@app.command("vintage")
def vintage(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    logs_root: Annotated[Path, typer.Option("--logs-root")] = Path("logs"),
    slice_id: Annotated[str, typer.Option("--slice-id")] = "c1",
) -> None:
    """Materialise an immutable data vintage. Does not publish or set preview."""

    from prism.catalog import CatalogError, default_catalog

    try:
        default_catalog().slice(slice_id)
    except CatalogError:
        typer.echo(f"unknown slice-id {slice_id!r}", err=True)
        raise typer.Exit(code=1) from None
    try:
        manifest, report = materialise_vintage(data_root, logs_root, slice_id=slice_id)
    except (PipelineError, VintageStoreError) as exc:
        typer.echo(f"vintage failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"vintage_id={manifest.vintage_id}")
    typer.echo(f"trigger={manifest.trigger.value}")
    typer.echo(f"completeness={manifest.completeness.value}")
    typer.echo(f"run_id={report['run_id']}")
    series_rows = report["series"]
    if not isinstance(series_rows, list):
        raise typer.Exit(code=1)
    for row in series_rows:
        if not isinstance(row, dict):
            continue
        typer.echo(
            f"{row['series_id']} reused={row['reused']} rewritten={row['rewritten']} "
            f"observations={row['observation_count']}"
        )
    if manifest.completeness is Completeness.failed:
        raise typer.Exit(code=1)


@app.command("desk")
def desk_cmd(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    slice_spec: Annotated[list[str] | None, typer.Option("--slice")] = None,
    preview: Annotated[bool, typer.Option("--preview/--no-preview")] = False,
) -> None:
    """Write an immutable desk record. Does not render or flip a pointer."""

    try:
        if preview:
            specs = preview_slices(data_root)
        elif slice_spec:
            specs = slices_from_cli(tuple(slice_spec))
        else:
            typer.echo("desk requires --slice slice_id=vintage_id or --preview", err=True)
            raise typer.Exit(code=1)
        record = write_desk(
            data_root,
            created_at=datetime.now(tz=UTC),
            slices=specs,
            completeness=Completeness.complete,
        )
    except typer.Exit:
        raise
    except (DeskStoreError, VintageStoreError) as exc:
        typer.echo(f"desk failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"desk_id={record.desk_id}")
    for binding in record.slices:
        typer.echo(f"{binding.template_id} vintage_id={binding.vintage_id}")


@app.command("render")
def render_cmd(
    desk_id: Annotated[str, typer.Option("--desk-id")],
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    cms_root: Annotated[Path, typer.Option("--cms-root")] = Path("src/cms"),
    set_preview: Annotated[
        bool, typer.Option("--set-preview/--no-set-preview")
    ] = False,
    cms_mode: Annotated[str, typer.Option("--cms-mode")] = "preview",
) -> None:
    """Bind the desk and write data/renders/{desk_id}/. Does not flip citizen."""

    try:
        dest = render(
            data_root,
            desk_id,
            cms_root,
            set_preview=set_preview,
            cms_mode=cms_mode,
        )
    except (RenderError, PublishError, VintageStoreError, DeskStoreError) as exc:
        typer.echo(f"render failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"render={dest.as_posix()}")
    typer.echo(f"desk_id={desk_id}")
    preview_id = read_preview_pointer(data_root)
    typer.echo(f"preview={preview_id or 'unset'}")


@app.command("publish")
def publish_cmd(
    desk_id: Annotated[str, typer.Option("--desk-id")],
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    citizen: Annotated[bool, typer.Option("--citizen/--no-citizen")] = False,
    contract_tests_passed: Annotated[
        bool, typer.Option("--contract-tests-passed/--no-contract-tests-passed")
    ] = False,
) -> None:
    """Flip a pointer. Citizen requires --contract-tests-passed."""

    try:
        if citizen:
            publish_citizen(
                data_root,
                desk_id,
                render_complete=True,
                contract_tests_passed=contract_tests_passed,
            )
        else:
            publish_preview(data_root, desk_id, render_complete=True)
    except PublishError as exc:
        typer.echo(f"publish failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"desk_id={desk_id}")
    if citizen:
        typer.echo("pointer=citizen")
    else:
        typer.echo("pointer=preview")


@app.command("preview")
def preview_cmd(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    host: Annotated[str, typer.Option("--host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port")] = 4321,
    bind_pointer: Annotated[
        bool, typer.Option("--bind-pointer/--no-bind-pointer")
    ] = False,
    desk_id: Annotated[str | None, typer.Option("--desk-id")] = None,
) -> None:
    """Serve the preview desk (published and unpublished slices) with noindex. Does not flip citizen."""

    if bind_pointer:
        if desk_id is None:
            typer.echo("preview --bind-pointer requires --desk-id", err=True)
            raise typer.Exit(code=1)
        try:
            publish_preview(data_root, desk_id, render_complete=True)
        except PublishError as exc:
            typer.echo(f"preview pointer failed: {exc}", err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(f"preview={desk_id}")
        return
    try:
        serve_preview(data_root, host, port)
    except ServeError as exc:
        typer.echo(f"preview failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@app.command("serve")
def serve_cmd(
    origin: Annotated[str, typer.Option("--origin", envvar="PRISM_CITIZEN_ORIGIN")],
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    host: Annotated[str, typer.Option("--host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port")] = 8080,
) -> None:
    """Serve the citizen pointer. Injects canonical and og:url. Does not scrape."""

    try:
        serve_citizen(data_root, host, port, origin)
    except ServeError as exc:
        typer.echo(f"serve failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
