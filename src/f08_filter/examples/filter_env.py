from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_test_filters_dir():
    return "src/f08_filter/examples/fiscals"


def get_test_faces_dir():
    return f"{get_test_filters_dir()}/faces"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_filters_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
