import importlib

import pytest

SUBPACKAGES = ["ingestion", "processing", "agent"]


@pytest.mark.parametrize("name", SUBPACKAGES)
def test_subpackage_is_importable(name: str) -> None:
    assert importlib.import_module(f"cognitive_agent.{name}")
