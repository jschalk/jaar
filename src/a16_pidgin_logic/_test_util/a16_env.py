from pytest import fixture as pytest_fixture
from src.a00_data_toolbox.file_toolbox import create_path, delete_dir


def get_module_temp_dir():
    return "src\\a16_pidgin_logic\\_test_util\\fiscs"


def get_example_face_dir():
    faces_dir = create_path(get_module_temp_dir(), "faces")
    return create_path(faces_dir, "sue")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_module_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
