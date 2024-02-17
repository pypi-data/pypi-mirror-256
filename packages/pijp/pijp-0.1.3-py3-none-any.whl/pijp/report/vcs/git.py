from typing import Literal, Optional

from git import Repo, InvalidGitRepositoryError
from pydantic import BaseModel


class GitReport(BaseModel):
    type: Literal["git"] = "git"
    branch: str
    last_commit: str
    remotes: dict[str, list[str]]

    @classmethod
    def from_path(cls, path: str) -> Optional["GitReport"]:
        try:
            repo = Repo(path)
            remotes = {remote.name: list(remote.urls) for remote in repo.remotes}

            return GitReport(
                branch=repo.active_branch.name,
                last_commit=repo.head.commit.hexsha,
                remotes=remotes,
            )
        except (InvalidGitRepositoryError, ValueError):
            return None
