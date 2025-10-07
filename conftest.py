import pytest
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_keywords_by_chapter,
    get_keywords_src_config,
)
from src.ch98_docs_builder.keyword_class_builder import save_keywords_enum_class_file


def pytest_addoption(parser):
    parser.addoption("--graphics_bool", action="store", default=False)
    parser.addoption("--run_big_tests", action="store", default=False)
    parser.addoption("--rebuild_bool", action="store", default=False)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    graphics_bool_value = metafunc.config.option.graphics_bool
    graphics_bool_value = str(graphics_bool_value).lower() == "true"
    if "graphics_bool" in metafunc.fixturenames and graphics_bool_value is not None:
        metafunc.parametrize("graphics_bool", [graphics_bool_value])
    run_big_tests_value = metafunc.config.option.run_big_tests
    run_big_tests_value = run_big_tests_value == "True"
    if "run_big_tests" in metafunc.fixturenames and run_big_tests_value is not None:
        metafunc.parametrize("run_big_tests", [run_big_tests_value])
    rebuild_bool_value = metafunc.config.option.rebuild_bool
    rebuild_bool_value = rebuild_bool_value == "True"
    if "rebuild_bool" in metafunc.fixturenames and rebuild_bool_value is not None:
        metafunc.parametrize("rebuild_bool", [rebuild_bool_value])


@pytest.fixture(scope="session", autouse=True)
def rewrite_files_before_tests():
    # This runs before any tests
    print("Rewriting keyword enum class defintions...")
    save_all_keyword_enum_class_python_files()
    print("Rewriting keyword enum class successful...")
    # No yield needed if you don't need teardown


def save_all_keyword_enum_class_python_files():
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    dest_dir = "src/ref"
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_keywords = cumlative_keywords.get(chapter_prefix)
        save_keywords_enum_class_file(dest_dir, chapter_prefix, chapter_keywords)
