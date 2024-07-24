from src.span.examples.span_env import (
    span_examples_dir,
    src_span_examples_dir,
    span_reals_dir,
)


def test_src_span_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_span_examples_dir() == "src/span/examples"


def test_span_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert span_examples_dir() == f"{src_span_examples_dir()}/span_examples"


def test_span_reals_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert span_reals_dir() == f"{src_span_examples_dir()}/reals"
