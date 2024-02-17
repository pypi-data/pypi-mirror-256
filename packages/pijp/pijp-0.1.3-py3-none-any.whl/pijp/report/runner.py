from typing import Optional
import datetime
import importlib.metadata
import logging
import time
import uuid
import os

from humanize import naturaldelta
from pydantic import BaseModel, Field, root_validator

from rich import box
from rich.console import Console, ConsoleOptions, RenderResult
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from pijp.config.jobs import JobStatus
from pijp.config.pipeline import Pipeline, PipelineResult
from pijp.report.system import SystemReport
from pijp.report.vcs.git import GitReport


class RunnerReport(BaseModel):
    system: SystemReport = SystemReport()
    vcs: Optional[GitReport] = None
    runner_id: uuid.UUID
    version: str = importlib.metadata.version("pijp")
    manifest_path: str
    pipelines: dict[str, Pipeline] = {}
    results: dict[str, PipelineResult] = {}
    created_at: float = Field(default_factory=time.time)

    @root_validator(skip_on_failure=True)
    @classmethod
    def get_vcs_report(cls, values: dict) -> dict:
        manifest_path = values.get("manifest_path")

        if manifest_path:
            path = os.path.dirname(manifest_path)
            git_report = GitReport.from_path(path)
            if git_report:
                values["vcs"] = git_report

        return values

    def __rich_console__(self, _console: Console, _options: ConsoleOptions) -> RenderResult:
        yield Rule("Pipeline report")
        yield ""

        for name, result in self.results.items():
            pipeline_duration = (
                naturaldelta(result.duration) if result.duration is not None else "Unknown"
            )
            table = Table(
                title=(f"Pipeline '{name}'" f": {result.status.name} " f"in {pipeline_duration}"),
                expand=True,
                show_lines=True,
                safe_box=True,
                box=box.SQUARE,
            )
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Stage")
            table.add_column("Started at")
            table.add_column("Duration")
            table.add_column("Status")
            table.add_column("Exit code")
            table.add_column("Can fail")

            for index, stage in enumerate(result.plan):
                for job_name in stage:
                    if job_name not in result.jobs:
                        logging.warning("Job %s has no report. Probably never ran!", job_name)
                        continue

                    job_result = result.jobs[job_name]

                    job_status = Text("Unknown", style="gray")
                    if job_result.status is not None:
                        if job_result.status is JobStatus.SUCCESS:
                            style = "green"
                        elif job_result.status is JobStatus.SKIPPED:
                            style = "yellow"
                        else:
                            style = "red"

                        job_status = Text(job_result.status.name, style=style)

                    job = self.pipelines[name].jobs[job_name]
                    table.add_row(
                        job_name,
                        str(type(job).__name__),
                        str(index + 1),
                        str(datetime.datetime.fromtimestamp(job_result.created_at)),
                        (
                            naturaldelta(job_result.duration)
                            if job_result.duration is not None
                            else "No data"
                        ),
                        job_status,
                        (
                            str(job_result.exit_code)
                            if job_result.exit_code is not None
                            else "Unknown"
                        ),
                        "Yes" if job.can_fail else "No",
                    )

            yield table
