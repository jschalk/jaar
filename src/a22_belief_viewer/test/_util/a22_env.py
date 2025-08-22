from pytest import fixture as pytest_fixture
from src.a00_data_toolbox.file_toolbox import delete_dir
from typing import Any, Generator, Literal


def module_dir() -> str:
    return "src/a22_belief_viewer"


def get_module_temp_dir() -> Literal["src\\a22_belief_viewer\\test\\_util\\temp"]:
    return "src\\a22_belief_viewer\\test\\_util\\temp"


@pytest_fixture()
def env_dir_setup_cleanup() -> (
    Generator[Literal["src\\a22_belief_viewer\\test\\_util"], Any, None]
):
    env_dir = get_module_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
