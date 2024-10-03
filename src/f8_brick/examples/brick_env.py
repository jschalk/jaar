from src.f0_instrument.file import delete_dir
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_brick_dir() -> str:
    return "src/f8_brick"


def src_brick_examples_dir() -> str:
    return "src/f8_brick/examples"


def brick_examples_dir() -> str:
    return f"{src_brick_examples_dir()}/brick_examples"


def brick_fiscals_dir() -> str:
    return f"{src_brick_examples_dir()}/fiscals"


@pytest_fixture()
def brick_env_setup_cleanup():
    env_dir = brick_fiscals_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
