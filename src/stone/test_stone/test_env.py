from src.stone.examples.stone_env import (
    stone_examples_dir,
    src_stone_examples_dir,
    stone_reals_dir,
)


def test_src_stone_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_stone_examples_dir() == "src/stone/examples"


def test_stone_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert stone_examples_dir() == f"{src_stone_examples_dir()}/stone_examples"


def test_stone_reals_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert stone_reals_dir() == f"{src_stone_examples_dir()}/reals"
