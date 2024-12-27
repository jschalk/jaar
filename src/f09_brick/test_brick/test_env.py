from src.f09_brick.examples.brick_env import (
    brick_examples_dir,
    src_brick_examples_dir,
    brick_deals_dir,
)


def test_src_brick_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_brick_examples_dir() == "src/f09_brick/examples"


def test_brick_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_examples_dir() == f"{src_brick_examples_dir()}/brick_examples"


def test_brick_deals_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert brick_deals_dir() == f"{src_brick_examples_dir()}/deals"
