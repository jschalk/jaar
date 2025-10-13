from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import delete_dir
from typing import Any, Generator, Literal


def get_chapter_temp_dir() -> str:
    return "src/ch98_docs_builder"


def get_chapter_temp_dir() -> Literal["src\\ch98_docs_builder\\test\\_util\\temp"]:
    return "src\\ch98_docs_builder\\test\\_util\\temp"


@pytest_fixture()
def env_dir_setup_cleanup() -> (
    Generator[Literal["src\\ch98_docs_builder\\test\\_util"], Any, None]
):
    env_dir = get_chapter_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
