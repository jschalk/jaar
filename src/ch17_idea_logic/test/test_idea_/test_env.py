from src.ch00_data_toolbox.file_toolbox import create_path
from src.ch17_idea_logic.test._util.ch17_env import (
    get_module_temp_dir,
    idea_moments_dir,
    src_module_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_module_temp_dir() == f"{src_module_dir()}/test/_util/idea_examples"


def test_idea_moments_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    moment_mstr_dir = create_path(get_module_temp_dir(), "moment_mstr")
    # assert idea_moments_dir() == create_path(moment_mstr_dir, "moments")
    assert idea_moments_dir() == f"{get_module_temp_dir()}/moment_mstr/moments"
