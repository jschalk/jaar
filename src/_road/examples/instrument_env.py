from src._instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_codespace_road_dir() -> str:
    return "src/_road"


def get_road_examples_dir():
    return f"{get_codespace_road_dir()}/examples"


def get_road_temp_env_dir():
    return f"{get_road_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_road_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
