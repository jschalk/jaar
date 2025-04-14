from src.a00_data_toolboxs.file_toolbox import delete_dir
from pytest import fixture as pytest_fixture


def get_codespace_instrument_dir() -> str:
    return "src/a00_data_toolboxs"


def get_instrument_examples_dir():
    return f"{get_codespace_instrument_dir()}/examples"


def get_instrument_temp_env_dir():
    return f"{get_instrument_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_instrument_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
