from src._instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def src_span_dir() -> str:
    return "src/span"


def src_span_examples_dir() -> str:
    return "src/span/examples"


def span_examples_dir() -> str:
    return f"{src_span_examples_dir()}/span_examples"


def span_reals_dir() -> str:
    return f"{src_span_examples_dir()}/reals"


@pytest_fixture()
def span_env_setup_cleanup():
    env_dir = span_reals_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
