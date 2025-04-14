from src.f00_instrument.file_toolbox import delete_dir
from src.f01_road.road import WorldID, get_default_world_id
from pytest import fixture as pytest_fixture


def get_test_world_id() -> WorldID:
    return get_default_world_id()


def get_test_worlds_dir():
    return "src/f12_world/examples/worlds"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_worlds_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
