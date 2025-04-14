from src.a00_data_toolboxs.file_toolbox import delete_dir, create_path
from pytest import fixture as pytest_fixture


def get_road_examples_dir():
    return "src/a00_data_toolboxs/examples"


def get_road_temp_env_dir():
    return create_path(get_road_examples_dir(), "temp")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_road_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
