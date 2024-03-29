from src.instrument.file import delete_dir, dir_files
from pytest import fixture as pytest_fixture


def get_test_world_id():
    return "music_45"


def get_test_worlds_dir():
    return "src/world/examples/worlds"


def get_test_world_dir():
    return f"{get_test_worlds_dir()}/{get_test_world_id()}"


@pytest_fixture()
def worlds_dir_setup_cleanup():
    env_dir = get_test_worlds_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
