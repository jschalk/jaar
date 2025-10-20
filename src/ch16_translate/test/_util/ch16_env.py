from pytest import fixture as pytest_fixture
from src.ch01_py.file_toolbox import create_path, delete_dir


def get_temp_dir():
    return "src\\ch16_translate\\test\\_util\\moments"


def get_example_face_dir():
    faces_dir = create_path(get_temp_dir(), "faces")
    return create_path(faces_dir, "sue")


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
