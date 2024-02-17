import logging
import os

import click

from rich.console import Console
from rich.logging import RichHandler

from pijp.commands import run, pipelines, plan
from pijp.config.manifest import Manifest
from pijp.utils.ids import get_runner_id


def setup_root_logger(debug: bool, console: Console) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RichHandler(
                console=console,
                show_path=False,
            )
        ],
    )


@click.group()
@click.option(
    "-f",
    "--file",
    type=str,
    default="pijp.yml",
    help="Specify the manifest file to use (default: pijp.yml).",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for verbose logging.",
)
@click.version_option()
@click.pass_context
def cli(ctx: click.Context, file: str, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["console"] = Console()

    ctx.obj["debug"] = debug
    setup_root_logger(debug, ctx.obj["console"])

    ctx.obj["runner_id"] = get_runner_id()
    ctx.obj["manifest_path"] = os.path.abspath(file)
    ctx.obj["manifest"] = Manifest.load_file(ctx.obj["manifest_path"])


cli.add_command(pipelines)
cli.add_command(plan)
cli.add_command(run)


def main() -> None:
    try:
        cli()  # pylint: disable=E1120
    except Exception as exc:  # pylint: disable=W0718
        logging.error(exc)


if __name__ == "__main__":
    main()
