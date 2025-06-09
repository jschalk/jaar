from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic._test_util.a17_env import (
    get_module_temp_dir,
    idea_examples_dir,
    idea_vows_dir,
    src_module_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{src_module_dir()=}")
    print(create_path(src_module_dir(), "_test_util"))
    assert get_module_temp_dir() == f"{src_module_dir()}/_test_util"


def test_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    # assert idea_examples_dir() == create_path(get_module_temp_dir(), "idea_examples")
    assert idea_examples_dir() == f"{get_module_temp_dir()}/idea_examples"


def test_idea_vows_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    vow_mstr_dir = create_path(idea_examples_dir(), "vow_mstr")
    # assert idea_vows_dir() == create_path(vow_mstr_dir, "vows")
    assert idea_vows_dir() == f"{idea_examples_dir()}/vow_mstr/vows"
