from src.f01_road.jaar_config import get_test_fiscs_dir, get_test_fisc_mstr_dir
from src.f00_instrument.file import delete_dir
from pytest import fixture as pytest_fixture


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_fisc_mstr_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
