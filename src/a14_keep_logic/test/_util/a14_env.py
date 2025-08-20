from pytest import fixture as pytest_fixture
from src.a00_data_toolbox.file_toolbox import delete_dir


def temp_moment_label():
    return "ex_keep04"


def temp_moment_mstr_dir():
    return "src\\a14_keep_logic\\test\\_util\\moment_mstr"


def get_module_temp_dir():
    return "src\\a14_keep_logic\\test\\_util\\moment_mstr\\moments"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_moment_mstr_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)
