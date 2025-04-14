from src.f00_data_toolboxs.file_toolbox import delete_dir
from pytest import fixture as pytest_fixture


def get_test_fisc_mstr_dir():
    return "src/f08_fisc/examples/fisc_mstr"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_fisc_mstr_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
