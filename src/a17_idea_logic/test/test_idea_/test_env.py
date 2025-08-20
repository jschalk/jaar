from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic.test._util.a17_env import (
    get_module_temp_dir,
    idea_coins_dir,
    src_module_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_module_temp_dir() == f"{src_module_dir()}/test/_util/idea_examples"


def test_idea_coins_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    coin_mstr_dir = create_path(get_module_temp_dir(), "coin_mstr")
    # assert idea_coins_dir() == create_path(coin_mstr_dir, "coins")
    assert idea_coins_dir() == f"{get_module_temp_dir()}/coin_mstr/coins"
