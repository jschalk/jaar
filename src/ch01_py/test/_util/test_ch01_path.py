from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch01_py._ref.ch01_path import (
    create_keywords_classes_file_path,
    create_src_keywords_path,
)
from src.ch01_py.file_toolbox import create_path, get_json_filename
from src.ch01_py.test._util.ch01_env import get_chapter_temp_dir

LINUX_OS = platform_system() == "Linux"


def test_create_src_keywords_path_ReturnsObj():
    # ESTABLISH
    src_dir = get_chapter_temp_dir()

    # WHEN
    keywords_class_file_path = create_src_keywords_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    expected_file_path = create_path(ref_dir, get_json_filename("keywords"))
    assert keywords_class_file_path == expected_file_path


def test_create_src_keywords_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ref")
    doc_str = create_path(ref_dir, get_json_filename("keywords"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_src_keywords_path) == doc_str


def test_create_keywords_classes_file_path_ReturnsObj():
    # ESTABLISH
    src_dir = "src"

    # WHEN
    keywords_class_file_path = create_keywords_classes_file_path(src_dir)

    # THEN
    ref_dir = create_path(src_dir, "ref")
    expected_keywords_file_path = create_path(ref_dir, "keywords.py")
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    assert keywords_class_file_path == expected_keywords_file_path


def test_create_keywords_classes_file_path_HasDocString():
    # ESTABLISH
    doc_str = create_keywords_classes_file_path("src")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keywords_classes_file_path) == doc_str
