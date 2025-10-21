from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import delete_dir


def get_temp_dir():
    return "src\\ch11_bud\\test\\_util\\temp"


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
