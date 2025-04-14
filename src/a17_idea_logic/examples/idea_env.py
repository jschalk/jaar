from src.a00_data_toolboxs.file_toolbox import delete_dir, create_path
from pytest import fixture as pytest_fixture
from os import makedirs as os_makedirs


def src_idea_dir() -> str:
    return create_path("src", "a17_idea_logic")


def src_idea_examples_dir() -> str:
    return create_path(src_idea_dir(), "examples")


def idea_examples_dir() -> str:
    return create_path(src_idea_examples_dir(), "idea_examples")


def idea_fisc_mstr_dir() -> str:
    return create_path(idea_examples_dir(), "fisc_mstr")


def idea_fiscs_dir() -> str:
    return create_path(idea_fisc_mstr_dir(), "fiscs")


@pytest_fixture()
def idea_env_setup_cleanup():
    env_dir = idea_examples_dir()
    delete_dir(env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)
