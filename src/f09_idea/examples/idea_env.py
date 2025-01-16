from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_idea_dir() -> str:
    return "src/f09_idea"


def src_idea_examples_dir() -> str:
    return "src/f09_idea/examples"


def idea_examples_dir() -> str:
    return f"{src_idea_examples_dir()}/idea_examples"


def idea_fiscals_dir() -> str:
    return f"{src_idea_examples_dir()}/fiscals"


@pytest_fixture()
def idea_env_setup_cleanup():
    env_dir = idea_fiscals_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
