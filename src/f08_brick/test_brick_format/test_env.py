from src.f08_brick.examples.brick_env import (
    brick_examples_dir,
    src_brick_examples_dir,
    brick_fiscals_dir,
)


def test_src_brick_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_brick_examples_dir() == "src/f08_brick/examples"


def test_brick_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_examples_dir() == f"{src_brick_examples_dir()}/brick_examples"


def test_brick_fiscals_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_fiscals_dir() == f"{src_brick_examples_dir()}/fiscals"
