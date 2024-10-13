from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_test_filters_dir():
    return "src/f10_filter/examples/fiscals"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_filters_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
