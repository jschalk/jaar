from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch17_idea.test._util.ch17_env import (
    get_chapter_temp_dir,
    idea_moments_dir,
    src_chapter_dir,
)


def test_get_chapter_temp_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_temp_dir() == f"{src_chapter_dir()}/test/_util/idea_examples"


def test_idea_moments_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    moment_mstr_dir = create_path(get_chapter_temp_dir(), "moment_mstr")
    # assert idea_moments_dir() == create_path(moment_mstr_dir, "moments")
    assert idea_moments_dir() == f"{get_chapter_temp_dir()}/moment_mstr/moments"
