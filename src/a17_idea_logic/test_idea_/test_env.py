from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic._utils.env_a17 import (
    src_module_dir,
    idea_examples_dir,
    get_module_temp_dir,
    idea_fiscs_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{src_module_dir()=}")
    print(create_path(src_module_dir(), "_utils"))
    assert get_module_temp_dir() == f"{src_module_dir()}/_utils"


def test_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    # assert idea_examples_dir() == create_path(get_module_temp_dir(), "idea_examples")
    assert idea_examples_dir() == f"{get_module_temp_dir()}/idea_examples"


def test_idea_fiscs_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    fisc_mstr_dir = create_path(idea_examples_dir(), "fisc_mstr")
    # assert idea_fiscs_dir() == create_path(fisc_mstr_dir, "fiscs")
    assert idea_fiscs_dir() == f"{idea_examples_dir()}/fisc_mstr/fiscs"
