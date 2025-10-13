from random import random as random_random
from src.ch01_py.file_toolbox import (
    create_path,
    get_dir_filenames,
    open_file,
    open_json,
    save_file,
    save_json,
)
from src.ch98_docs_builder._ref.ch98_path import create_keywords_classes_file_path
from src.ch98_docs_builder.doc_builder import (
    get_chapter_descs,
    save_brick_formats_md,
    save_chapter_blurbs_md,
    save_idea_brick_mds,
    save_keywords_by_chapter_md,
    save_ropeterm_explanation_md,
)
from src.ch98_docs_builder.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
)


def test_SpecialTestThatBuildsDocs():
    """
    Intended to be the last test before the style checker (linter) tests.
    Should only create documentation and/or sort json files
    """
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    destination_dir = "docs"
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    save_idea_brick_mds(destination_dir)
    save_brick_formats_md(destination_dir)
    save_chapter_blurbs_md(destination_dir)
    save_ropeterm_explanation_md(destination_dir)
    save_keywords_by_chapter_md(destination_dir)  # docs\keywords_by_chapter.md

    # resave json files so that they are ordered alphabetically
    # No need to always resave all json files, so just do it 4% of the time
    if random_random() < 0.04:
        for chapter_dir in get_chapter_descs().values():
            json_file_tuples = get_dir_filenames(chapter_dir, {"json"})
            for x_dir, x_filename in json_file_tuples:
                json_filepath = create_path(x_dir, x_filename)
                print(f"{json_filepath=}")
                print(f"{x_dir} {x_filename=}")
                json_dir = create_path(chapter_dir, x_dir)
                save_json(json_dir, x_filename, open_json(json_dir, x_filename))

    # save file for all Enum class references
    keywords_classes_file_path = create_keywords_classes_file_path("src")
    enum_classes_str = create_all_enum_keyword_classes_str()
    current_classes_file_str = open_file(keywords_classes_file_path)
    print(enum_classes_str[:100])
    save_file(keywords_classes_file_path, None, enum_classes_str)
    assertion_failure_str = (
        "Special case: keywords.py file was rebuilt, run test again."
    )
    assert enum_classes_str == current_classes_file_str, assertion_failure_str
