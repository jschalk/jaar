from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import delete_dir
from typing import Any, Generator, Literal


def get_temp_dir() -> Literal["src\\ch01_py\\test\\_util\\temp"]:
    return "src\\ch01_py\\test\\_util\\temp"


@pytest_fixture()
def temp_dir_setup() -> Generator[Literal["src\\ch01_py\\test\\_util"], Any, None]:
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
