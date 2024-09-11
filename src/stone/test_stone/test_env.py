from src.stone.examples.stone_env import (
    stone_examples_dir,
    src_stone_examples_dir,
    stone_tribes_dir,
)


def test_src_stone_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_stone_examples_dir() == "src/stone/examples"


def test_stone_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert stone_examples_dir() == f"{src_stone_examples_dir()}/stone_examples"


def test_stone_tribes_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert stone_tribes_dir() == f"{src_stone_examples_dir()}/tribes"
