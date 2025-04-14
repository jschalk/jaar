from src.f00_instrument.file_toolbox import delete_dir, create_path
from pytest import fixture as pytest_fixture


def get_codespace_pack_dir() -> str:
    return "src/f04_pack"


def get_pack_examples_dir():
    return create_path(get_codespace_pack_dir(), "examples")


def get_pack_temp_env_dir():
    return create_path(get_pack_examples_dir(), "temp")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_pack_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
