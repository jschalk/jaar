from src.f00_data_toolboxs.file_toolbox import create_path
from src.f10_idea.examples.idea_env import (
    src_idea_dir,
    idea_examples_dir,
    src_idea_examples_dir,
    idea_fiscs_dir,
)


def test_src_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert src_idea_examples_dir() == create_path(src_idea_dir(), "examples")


def test_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert idea_examples_dir() == create_path(src_idea_examples_dir(), "idea_examples")


def test_idea_fiscs_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    fisc_mstr_dir = create_path(idea_examples_dir(), "fisc_mstr")
    assert idea_fiscs_dir() == create_path(fisc_mstr_dir, "fiscs")
