from src.a00_data_toolboxs.file_toolbox import delete_dir
from pytest import fixture as pytest_fixture


def get_test_etl_dir():
    return "src/a18_etl_toolbox/examples/etls"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_etl_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
