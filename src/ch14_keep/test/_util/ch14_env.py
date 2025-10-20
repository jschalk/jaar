from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import delete_dir


def temp_moment_label():
    return "ex_keep04"


def temp_moment_mstr_dir():
    return "src\\ch14_keep\\test\\_util\\moment_mstr"


def get_temp_dir():
    return "src\\ch14_keep\\test\\_util\\moment_mstr\\moments"


@pytest_fixture()
def temp_dir_setup():
    env_dir = temp_moment_mstr_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)
