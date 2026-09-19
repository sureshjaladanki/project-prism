"""Typer CLI: ingest → vintage → render. Citizen publish waits for Trust Auditor."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from prism.citizen_server import serve_citizen
from prism.ingest import ingest as run_ingest
from prism.ingest.retrieve import IngestError
from prism.pipeline import PipelineError, materialise_c1_vintage, materialise_c3_vintage
from prism.pointer_store import PublishError, publish_preview, read_preview_pointer
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


_VINTAGE_RUNNERS = {
    "c1": materialise_c1_vintage,
    "c3": materialise_c3_vintage,
}


@app.command("vintage")
def vintage(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    logs_root: Annotated[Path, typer.Option("--logs-root")] = Path("logs"),
    slice_id: Annotated[str, typer.Option("--slice-id")] = "c1",
) -> None:
    """Materialise an immutable data vintage. Does not publish or set preview."""

    runner = _VINTAGE_RUNNERS.get(slice_id)
    if runner is None:
        typer.echo(f"unknown slice-id {slice_id!r}; expected c1 or c3", err=True)
        raise typer.Exit(code=1)
    try:
        manifest, report = runner(data_root, logs_root)
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


@app.command("render")
def render_cmd(
    vintage_id: Annotated[str, typer.Option("--vintage-id")],
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    cms_root: Annotated[Path, typer.Option("--cms-root")] = Path("src/cms"),
    set_preview: Annotated[
        bool, typer.Option("--set-preview/--no-set-preview")
    ] = False,
) -> None:
    """Bind templates at one vintage and write data/renders/{vintage_id}/. Does not flip citizen."""

    try:
        dest = render(data_root, vintage_id, cms_root, set_preview=set_preview)
    except (RenderError, PublishError, VintageStoreError) as exc:
        typer.echo(f"render failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"render={dest.as_posix()}")
    typer.echo(f"vintage_id={vintage_id}")
    preview = read_preview_pointer(data_root)
    typer.echo(f"preview={preview or 'unset'}")


@app.command("preview")
def preview_cmd(
    data_root: Annotated[Path, typer.Option("--data-root")] = Path("data"),
    host: Annotated[str, typer.Option("--host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port")] = 4321,
    bind_pointer: Annotated[
        bool, typer.Option("--bind-pointer/--no-bind-pointer")
    ] = False,
    vintage_id: Annotated[str | None, typer.Option("--vintage-id")] = None,
) -> None:
    """Serve the preview pointer with noindex. Does not flip citizen."""

    if bind_pointer:
        if vintage_id is None:
            typer.echo("preview --bind-pointer requires --vintage-id", err=True)
            raise typer.Exit(code=1)
        try:
            publish_preview(data_root, vintage_id, render_complete=True)
        except PublishError as exc:
            typer.echo(f"preview pointer failed: {exc}", err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(f"preview={vintage_id}")
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
