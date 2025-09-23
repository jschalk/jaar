from pytest import fixture as pytest_fixture
from src.ch01_data_toolbox.file_toolbox import delete_dir


def get_chapter_temp_dir():
    return "src\\ch21_lobby_logic\\test\\_util\\lobbys"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_chapter_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
