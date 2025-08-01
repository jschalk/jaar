from pytest import fixture as pytest_fixture
from src.a00_data_toolbox.file_toolbox import delete_dir


def get_module_temp_dir():
    return "src\\a18_etl_toolbox\\test\\_util\\etls"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_module_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
