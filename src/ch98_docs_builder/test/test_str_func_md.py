from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_file
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_keywords_by_chapter,
    get_keywords_by_chapter_md,
    get_keywords_src_config,
    save_keywords_by_chapter_md,
)
from src.ch98_docs_builder.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_keywords_enum_class_file_str,
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
    event_num_index = keywords_by_chapter_md.find("event_num")
    assert event_num_index > 0
    assert ch10_pack_index < event_num_index


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


def test_create_all_enum_keyword_classes_str_ReturnsObj():
    # ESTABLISH / WHEN
    classes_str = create_all_enum_keyword_classes_str()

    # THEN
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    expected_classes_str = """from enum import Enum
"""
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_keywords = cumlative_keywords.get(ch_prefix)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
        expected_classes_str += enum_class_str
    assert expected_classes_str == classes_str
    two_line_spacing_str = """from enum import Enum


class Ch00Key"""
    print(classes_str[:100])
    assert classes_str.find(two_line_spacing_str) == 0
