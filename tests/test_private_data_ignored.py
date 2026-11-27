import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIRECTORIES = ["inbox", "notes", "qdrant_data", "local"]
SOURCE_DIRECTORIES = ["src/cognitive_agent", "tests"]


def isolated_git_environment() -> dict[str, str]:
    inherited = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return inherited | {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def run_git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-c", f"core.excludesFile={os.devnull}", *arguments],
        cwd=repository,
        env=isolated_git_environment(),
        check=False,
    )


@pytest.fixture(scope="module")
def reviewed_rules_repository(tmp_path_factory: pytest.TempPathFactory) -> Path:
    repository = tmp_path_factory.mktemp("ignore_rules")
    run_git(repository, "init", "--quiet", "--template=").check_returncode()
    shutil.copyfile(REPOSITORY_ROOT / ".gitignore", repository / ".gitignore")
    return repository


def is_ignored(repository: Path, path: str) -> bool:
    result = run_git(repository, "check-ignore", "--no-index", "--quiet", path)
    if result.returncode not in (0, 1):
        result.check_returncode()
    return result.returncode == 0


@pytest.mark.parametrize("directory", PRIVATE_DIRECTORIES)
def test_private_data_is_ignored(reviewed_rules_repository: Path, directory: str) -> None:
    assert is_ignored(reviewed_rules_repository, f"{directory}/sample.md")


@pytest.mark.parametrize("parent", SOURCE_DIRECTORIES)
@pytest.mark.parametrize("directory", PRIVATE_DIRECTORIES[:3])
def test_same_named_source_directory_is_tracked(
    reviewed_rules_repository: Path, parent: str, directory: str
) -> None:
    assert not is_ignored(reviewed_rules_repository, f"{parent}/{directory}/sample.py")
