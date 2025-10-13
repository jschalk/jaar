from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch01_py.file_toolbox import create_path
from src.ch98_docs_builder._ref.ch98_path import (
    create_keywords_class_file_path,
    create_keywords_classes_file_path,
    get_keywords_filename,
)
from src.ch98_docs_builder.test._util.ch98_env import get_chapter_temp_dir

LINUX_OS = platform_system() == "Linux"


def test_create_keywords_class_file_path_ReturnsObj():
    # ESTABLISH
    chapter_dir = get_chapter_temp_dir()
    ref_dir = create_path(chapter_dir, "ref")
    chXX_str = "chXX"

    # WHEN
    keywords_class_file_path = create_keywords_class_file_path(ref_dir, chXX_str)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    expected_file_path = create_path(ref_dir, get_keywords_filename(chXX_str))
    assert keywords_class_file_path == expected_file_path


def test_create_keywords_class_file_path_HasDocString():
    # ESTABLISH
    doc_str = create_keywords_class_file_path("src\\ref", chapter_prefix="chXX")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keywords_class_file_path) == doc_str


def test_create_keywords_classes_file_path_ReturnsObj():
    # ESTABLISH
    ref_dir = create_path("src", "ref")
    expected_keywords_file_path = create_path(ref_dir, "keywords.py")

    # WHEN
    keywords_class_file_path = create_keywords_classes_file_path()

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    assert keywords_class_file_path == expected_keywords_file_path


def test_create_keywords_classes_file_path_HasDocString():
    # ESTABLISH
    doc_str = create_keywords_classes_file_path()
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keywords_classes_file_path) == doc_str
