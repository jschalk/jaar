from src.a00_data_toolbox.file_toolbox import delete_dir
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_module_dir() -> str:
    return "src/a17_idea_logic"


def get_module_temp_dir() -> str:
    return "src/a17_idea_logic/_test_util"


def idea_examples_dir() -> str:
    return "src/a17_idea_logic/_test_util/idea_examples"


def idea_fisc_mstr_dir() -> str:
    return "src/a17_idea_logic/_test_util/idea_examples/fisc_mstr"


def idea_fiscs_dir() -> str:
    return "src/a17_idea_logic/_test_util/idea_examples/fisc_mstr/fiscs"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = idea_examples_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
