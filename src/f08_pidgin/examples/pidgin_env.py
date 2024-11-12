from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_test_pidgins_dir():
    return "src/f08_pidgin/examples/fiscals"


def get_test_faces_dir():
    return f"{get_test_pidgins_dir()}/faces"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_pidgins_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
