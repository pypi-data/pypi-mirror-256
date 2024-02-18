import logging
import re

from pydantic import BaseModel, validator
import yaml

from pijp.config.pipeline import Pipeline


class Manifest(BaseModel):
    version: str
    pipelines: dict[str, Pipeline] = {}

    @validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        pattern = r"^\d+\.\d+$"
        if not re.match(pattern, value):
            raise ValueError(f"Version {value} is not a valid MAJOR.MINOR version")

        return value

    @validator("pipelines")
    @classmethod
    def validate_pipelines(cls, value: dict[str, Pipeline]) -> dict[str, Pipeline]:
        max_pipelines = 1000
        current_pipelines = len(value)

        if len(value) > max_pipelines:
            raise ValueError(
                f"Number of pipelines is limited to {max_pipelines} ({current_pipelines})"
            )

        return value

    @classmethod
    def load_file(cls, file_path: str) -> "Manifest":
        """
        Load and parse the manifest file.

        Args:
            file_path (str): The path to the manifest file.

        Returns:
            Manifest: An instance of the Manifest class populated with the data from the file.
        """

        logging.debug("Loading manifest file from %s", file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return cls(**data)
