import click

from rich.console import Console
from rich.table import Table

from pijp.config import Manifest


@click.command(help="Lists all available pipelines defined in the manifest.")
@click.pass_context
def pipelines(ctx: click.Context) -> None:
    console: Console = ctx.obj["console"]
    manifest: Manifest = ctx.obj["manifest"]

    table = Table(expand=True)
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Jobs")

    for name, pipeline in manifest.pipelines.items():
        table.add_row(name, pipeline.description, str(len(pipeline.jobs)))

    console.print(table)
