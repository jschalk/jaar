from src._instrument.file import delete_dir
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_stone_dir() -> str:
    return "src/stone"


def src_stone_examples_dir() -> str:
    return "src/stone/examples"


def stone_examples_dir() -> str:
    return f"{src_stone_examples_dir()}/stone_examples"


def stone_fiscals_dir() -> str:
    return f"{src_stone_examples_dir()}/fiscals"


@pytest_fixture()
def stone_env_setup_cleanup():
    env_dir = stone_fiscals_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
