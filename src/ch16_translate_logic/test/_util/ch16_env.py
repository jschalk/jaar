from pytest import fixture as pytest_fixture
from src.ch01_data_toolbox.file_toolbox import create_path, delete_dir


def get_chapter_temp_dir():
    return "src\\ch16_translate_logic\\test\\_util\\moments"


def get_example_face_dir():
    faces_dir = create_path(get_chapter_temp_dir(), "faces")
    return create_path(faces_dir, "sue")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_chapter_temp_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
