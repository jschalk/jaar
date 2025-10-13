from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_file
from src.ch98_docs_builder.doc_builder import (
    get_keywords_by_chapter_md,
    save_keywords_by_chapter_md,
)
from src.ch98_docs_builder.test._util.ch98_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def test_get_keywords_by_chapter_md_SetsFile_CheckMarkdownHasAllStrFunctions():
    # ESTABLISH / WHEN
    keywords_by_chapter_md = get_keywords_by_chapter_md()

    # THEN
    print(keywords_by_chapter_md)
    assert keywords_by_chapter_md.find("words by Chapter") > 0
    ch10_pack_index = keywords_by_chapter_md.find("ch10_pack")
    assert ch10_pack_index > 0
    event_int_index = keywords_by_chapter_md.find("event_int")
    assert event_int_index > 0
    assert ch10_pack_index < event_int_index


def test_save_keywords_by_chapter_md_SavesFile_get_keywords_by_chapter_md_ToGivenDirectory(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    temp_dir = get_chapter_temp_dir()
    keywords_by_chapter_md_path = create_path(temp_dir, "keywords_by_chapter.md")
    assert not os_path_exists(keywords_by_chapter_md_path)

    # WHEN
    keywords_by_chapter_md = save_keywords_by_chapter_md(temp_dir)

    # THEN
    assert os_path_exists(keywords_by_chapter_md_path)
    keywords_by_chapter_md = get_keywords_by_chapter_md()
    assert open_file(keywords_by_chapter_md_path) == keywords_by_chapter_md
