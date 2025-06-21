from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic.test._util.a17_env import (
    get_module_temp_dir,
    idea_banks_dir,
    idea_examples_dir,
    src_module_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_module_temp_dir() == f"{src_module_dir()}/test/_util"


def test_idea_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    # assert idea_examples_dir() == create_path(get_module_temp_dir(), "idea_examples")
    assert idea_examples_dir() == f"{get_module_temp_dir()}/idea_examples"


def test_idea_banks_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    bank_mstr_dir = create_path(idea_examples_dir(), "bank_mstr")
    # assert idea_banks_dir() == create_path(bank_mstr_dir, "banks")
    assert idea_banks_dir() == f"{idea_examples_dir()}/bank_mstr/banks"
