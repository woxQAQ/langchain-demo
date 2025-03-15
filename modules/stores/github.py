from git import Repo
from git.types import PathLike


def clone_into(repo_path: PathLike, output_path: PathLike):
    repo = Repo.clone_from(url=repo_path, to_path=output_path)
    return repo
