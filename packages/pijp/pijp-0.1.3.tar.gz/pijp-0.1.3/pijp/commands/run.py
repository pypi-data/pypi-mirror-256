from typing import Any, Optional
import logging
import re
import signal
import sys
import uuid

import click

from rich.console import Console
from rich.text import Text

from pijp.config import Manifest
from pijp.config.jobs import JobStatus
from pijp.report import RunnerReport
from pijp.utils.colors import ColorCycle


def parse_vars(_ctx: click.Context, _param: str, values: list[str]) -> dict[str, str]:
    variables: dict[str, str] = {}
    for value in values:
        try:
            key, val = value.split("=", 1)
            if not re.match(r"^[A-Z_]+[A-Z0-9_]*$", key):
                raise click.BadParameter(f"Invalid environment variable name: '{key}'")

            variables[key] = val
        except ValueError as exc:
            raise click.BadParameter("Variables must be in the format KEY=VALUE") from exc

    return variables


@click.command(help="Executes the specified pipeline according to the plan.")
@click.argument("name", metavar="PIPELINE")
@click.option(
    "-c",
    "--concurrent",
    type=int,
    default=None,
    help="Number of concurrent jobs",
)
@click.option(
    "-e",
    "--env",
    "variables",
    multiple=True,
    callback=parse_vars,
    help="Add variable",
)
@click.pass_context
def run(
    ctx: click.Context,
    name: str,
    concurrent: Optional[int],
    variables: dict[str, str],
) -> None:
    console: Console = ctx.obj["console"]
    runner_id: uuid.UUID = ctx.obj["runner_id"]
    manifest: Manifest = ctx.obj["manifest"]
    manifest_path: str = ctx.obj["manifest_path"]

    if name not in manifest.pipelines:
        raise ValueError(f"No pipeline named {name}")
    pipeline = manifest.pipelines[name]

    runner_report = RunnerReport(
        runner_id=runner_id,
        manifest_path=manifest_path,
        pipelines={name: pipeline},
    )

    def signal_handler(signum, _) -> None:
        logging.warning(
            "Received signal: %s (%d). Exiting...",
            signal.Signals(signum).name,
            signum,
        )
        pipeline.cancel()

        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    output = OutputHandler(console)
    with console.status(f"Running '{name}' pipeline...") as _status:
        runner_report.results[name] = pipeline.run(
            name,
            variables,
            concurrent,
            stage_start_callback=output.on_stage_start,
            job_complete_callback=output.on_job_complete,
            job_progress_callback=output.on_job_progress,
        )

    console.print(runner_report)


class OutputHandler:
    _job_colors: dict[str, str] = {}

    def __init__(self, _console: Console) -> None:
        self.console = _console

    def on_stage_start(self, data: dict[str, Any]) -> None:
        self.console.rule(f"[bold] Stage {data['index']} ({len(data['job_names'])} jobs)")

    def on_job_complete(self, data: dict[str, Any]) -> None:
        status: JobStatus = data["status"]
        name: str = data["name"]

        if status == JobStatus.CANCELLED:
            logging.error("Job %s was cancelled!", name)
        elif status == JobStatus.SKIPPED:
            logging.warning("Skipped job '%s'", name)
        elif status == JobStatus.FAILED_EXIT_CODE:
            logging.error("Job '%s' exited with error code!", name)
        elif status == JobStatus.FAILED_TIMEOUT:
            logging.error("Job '%s' timed out!", name)

    def on_job_progress(self, data: dict[str, Any]) -> None:
        name: str = data["name"]
        output: str = data["output"]

        if not name in self._job_colors:
            self._job_colors[name] = ColorCycle().next_color()

        if not output.startswith("#pijp#"):
            self.console.print(
                Text(f"[{name}]", style=self._job_colors[name]),
                Text(output),
                sep="\t",
                highlight=False,
            )
