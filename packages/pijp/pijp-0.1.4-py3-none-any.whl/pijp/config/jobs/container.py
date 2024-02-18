from typing import Any, Callable, Literal, Optional
import logging
import os
import string
import uuid

import docker
from docker.models.containers import Container

from pydantic import PrivateAttr

from pijp.config.jobs.base import BaseJob
from pijp.utils import no_op
from pijp.utils.scripts import get_script_file


class ContainerJob(BaseJob):
    type: Literal["container"] = "container"
    image: str = "alpine:latest"
    interpreter: str = "/bin/sh"
    pre_commands: list[str] = []
    commands: list[str] = []
    post_commands: list[str] = []
    entrypoint: list[str] = ["/bin/sh"]
    volumes: list[str] = []
    network_mode: str = "bridge"
    privileged: bool = False

    _container: Optional[Container] = PrivateAttr(default=None)

    def on_run(
        self,
        pipeline_id: uuid.UUID,
        name: str,
        variables: dict[str, str],
        progress_callback: Callable[[dict[str, Any]], None] = no_op,
    ) -> int:
        commands = [
            *self.pre_commands,
            *self.commands,
            *self.post_commands,
        ]
        if not commands:
            logging.warning("Empty script for job '%s'", name)

        filename = get_script_file(commands=commands, interpreter=self.interpreter)
        image = string.Template(self.image).substitute(**variables)
        client = docker.from_env()

        try:
            client.images.get(image)
        except docker.errors.ImageNotFound:
            for line in client.api.pull(image, stream=True, decode=True):
                if "status" not in line:
                    continue

                parts = [
                    line["status"],
                    f"({line['id']})" if "id" in line else "",
                    f": {line['progress']}" if "progress" in line else "",
                ]

                progress_callback(
                    {
                        "job_id": self._id,
                        "name": name,
                        "output": " ".join(filter(None, parts)),
                    }
                )

        self._container = client.containers.run(
            image=image,
            privileged=self.privileged,
            entrypoint=self.entrypoint,
            command="/opt/start.sh",
            working_dir="/opt/workspace",
            volumes=[
                *[normalize_volume(volume) for volume in self.volumes],
                f"{filename}:/opt/start.sh:ro",
                f"{os.getcwd()}:/opt/workspace",
            ],
            environment=variables,
            detach=True,
            network_mode=self.network_mode,
            labels={
                "org.pijp.session_id": str(pipeline_id),
                "org.pijp.job_name": name,
            },
        )

        for line in self._container.logs(stream=True, follow=True):
            progress_callback(
                {
                    "job_id": self._id,
                    "name": name,
                    "output": line.decode().rstrip(),
                }
            )

        result = self._container.wait()

        # NOTE: This is to avoid a double removal. At this
        # point we can assume that the container was stopped and removed.
        if not self._cancelled:
            self._container.remove(force=True)

        exit_code = int(result.get("StatusCode", 0))
        return exit_code

    def on_cancel(self) -> None:
        if self._container is not None:
            self._container.remove(force=True)


def normalize_volume(volume: str) -> str:
    host_path, guest_path = volume.split(":")
    host_volume = os.path.abspath(os.path.expanduser(host_path))

    return f"{host_volume}:{guest_path}"
