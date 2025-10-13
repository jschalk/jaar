from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import count_dirs_files, create_path, open_file
from src.ch02_rope._ref.ch02_doc_builder import get_ropeterm_explanation_md
from src.ch98_docs_builder.doc_builder import (
    get_chapter_blurbs_md,
    get_keywords_src_config,
    save_brick_formats_md,
    save_chapter_blurbs_md,
    save_idea_brick_mds,
    save_ropeterm_explanation_md,
)
from src.ch98_docs_builder.test._util.ch98_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ref.ch98_keywords import Ch98Keywords as wx


def test_get_keywords_src_config_ReturnsObj():
    # ESTABLISH / WHEN
    keywords_config = get_keywords_src_config()

    # THEN
    assert keywords_config
    assert keywords_config.get(wx.fund_pool)
    for keyword, ref_dict in keywords_config.items():
        assert set(ref_dict.keys()) == {"init_chapter"}
        print(f"{keyword=} {ref_dict=}")


def test_get_chapter_blurbs_md_ReturnsObj():
    # ESTABLISH / WHEN
    chapter_blurbs_md = get_chapter_blurbs_md()

    # THEN
    assert chapter_blurbs_md
    assert chapter_blurbs_md.find("ch04") > 0


def test_save_chapter_blurbs_md_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_chapter_temp_dir()
    chapter_blurbs_path = create_path(temp_dir, "chapter_blurbs.md")
    assert not os_path_exists(chapter_blurbs_path)

    # WHEN
    save_chapter_blurbs_md(temp_dir)

    # THEN
    assert os_path_exists(chapter_blurbs_path)
    expected_chapter_blurbs_md = get_chapter_blurbs_md()
    assert open_file(chapter_blurbs_path) == expected_chapter_blurbs_md


def test_save_ropeterm_explanation_md_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_chapter_temp_dir()
    file_path = create_path(temp_dir, "ropeterm_explanation.md")
    assert not os_path_exists(file_path)

    # WHEN
    save_ropeterm_explanation_md(temp_dir)

    # THEN
    assert os_path_exists(file_path)
    assert open_file(file_path) == get_ropeterm_explanation_md()


def test_save_idea_brick_mds_CreatesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_chapter_temp_dir()
    assert count_dirs_files(temp_dir) == 0

    # WHEN
    save_idea_brick_mds(temp_dir)

    # THEN
    assert count_dirs_files(temp_dir) == 41


def test_save_idea_brick_formats_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    doc_main_dir = get_chapter_temp_dir()
    idea_brick_formats_path = create_path(doc_main_dir, "idea_brick_formats.md")
    assert not os_path_exists(idea_brick_formats_path)

    # WHEN
    save_brick_formats_md(doc_main_dir)

    # THEN
    assert os_path_exists(idea_brick_formats_path)
    idea_brick_formats_md = open_file(idea_brick_formats_path)
    assert idea_brick_formats_md.find("br00004") > 0
