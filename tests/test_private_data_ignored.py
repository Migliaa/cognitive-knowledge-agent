import subprocess
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIRECTORIES = ["inbox", "notes", "qdrant_data", "local"]
SOURCE_DIRECTORIES = ["src/cognitive_agent", "tests"]


def is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", path],
        cwd=REPOSITORY_ROOT,
        check=False,
    )
    if result.returncode not in (0, 1):
        result.check_returncode()
    return result.returncode == 0


@pytest.mark.parametrize("directory", PRIVATE_DIRECTORIES)
def test_private_data_is_ignored(directory: str) -> None:
    assert is_ignored(f"{directory}/sample.md")


@pytest.mark.parametrize("parent", SOURCE_DIRECTORIES)
@pytest.mark.parametrize("directory", PRIVATE_DIRECTORIES[:3])
def test_same_named_source_directory_is_tracked(parent: str, directory: str) -> None:
    assert not is_ignored(f"{parent}/{directory}/sample.py")
