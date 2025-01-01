from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_brick_dir() -> str:
    return "src/f09_brick"


def src_brick_examples_dir() -> str:
    return "src/f09_brick/examples"


def brick_examples_dir() -> str:
    return f"{src_brick_examples_dir()}/brick_examples"


def brick_cmtys_dir() -> str:
    return f"{src_brick_examples_dir()}/cmtys"


@pytest_fixture()
def brick_env_setup_cleanup():
    env_dir = brick_cmtys_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
