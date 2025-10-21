from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import delete_dir


def src_chapter_dir() -> str:
    return "src/ch17_idea"


def get_temp_dir() -> str:
    return "src/ch17_idea/test/_util/idea_examples"


def idea_moment_mstr_dir() -> str:
    return "src/ch17_idea/test/_util/idea_examples/moment_mstr"


def idea_moments_dir() -> str:
    return "src/ch17_idea/test/_util/idea_examples/moment_mstr/moments"


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
