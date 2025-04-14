from src.f00_data_toolboxs.file_toolbox import delete_dir, create_path
from pytest import fixture as pytest_fixture


def get_example_pidgins_dir():
    return "src/f09_pidgin/examples/fiscs"


def get_example_face_dir():
    faces_dir = create_path(get_example_pidgins_dir(), "faces")
    return create_path(faces_dir, "sue")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_example_pidgins_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
