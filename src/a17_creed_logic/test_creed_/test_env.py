from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_creed_logic._utils.env_a17 import (
    src_module_dir,
    creed_examples_dir,
    get_module_temp_dir,
    creed_fiscs_dir,
)


def test_get_module_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{src_module_dir()=}")
    print(create_path(src_module_dir(), "_utils"))
    assert get_module_temp_dir() == f"{src_module_dir()}/_utils"


def test_creed_examples_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    # assert creed_examples_dir() == create_path(get_module_temp_dir(), "creed_examples")
    assert creed_examples_dir() == f"{get_module_temp_dir()}/creed_examples"


def test_creed_fiscs_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    fisc_mstr_dir = create_path(creed_examples_dir(), "fisc_mstr")
    # assert creed_fiscs_dir() == create_path(fisc_mstr_dir, "fiscs")
    assert creed_fiscs_dir() == f"{creed_examples_dir()}/fisc_mstr/fiscs"
