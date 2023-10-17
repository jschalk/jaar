from src.oath.x_func import delete_dir as x_func_delete_dir
from pytest import fixture as pytest_fixture


def oath_env():
    return "src/oath/examples"


def get_oath_temp_env_dir():
    return "src/oath/examples/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_oath_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)
