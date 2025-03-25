from src.f00_instrument.file import delete_dir, create_path
from pytest import fixture as pytest_fixture


def get_codespace_favor_dir() -> str:
    return "src/f04_favor"


def get_favor_examples_dir():
    return create_path(get_codespace_favor_dir(), "examples")


def get_favor_temp_env_dir():
    return create_path(get_favor_examples_dir(), "temp")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_favor_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
