from src.f09_idea.examples.idea_env import (
    idea_examples_dir,
    src_idea_examples_dir,
    idea_cmtys_dir,
)


def test_src_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_idea_examples_dir() == "src/f09_idea/examples"


def test_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert idea_examples_dir() == f"{src_idea_examples_dir()}/idea_examples"


def test_idea_cmtys_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert idea_cmtys_dir() == f"{src_idea_examples_dir()}/cmtys"
