from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_example_pidgins_dir():
    return "src/f08_pidgin/examples/fiscs"


def get_example_face_dir():
    return f"{get_example_pidgins_dir()}/faces/sue"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_example_pidgins_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
