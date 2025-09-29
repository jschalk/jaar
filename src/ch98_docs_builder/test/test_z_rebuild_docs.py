from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_dir_filenames,
    open_json,
    save_json,
)
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_descs,
    save_brick_formats_md,
    save_chapter_blurbs_md,
    save_idea_brick_mds,
    save_keywords_by_chapter_md,
    save_ropeterm_explanation_md,
)


def test_SpecialTestThatBuildsDocs():
    """
    Intended to be the last test before the style checker (linter) tests.
    Should only create documentation and/or sort json files
    """
    # ESTABLISH / WHEN / THEN
    destination_dir = "docs"
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    save_idea_brick_mds(destination_dir)
    save_brick_formats_md(destination_dir)
    save_chapter_blurbs_md(destination_dir)
    save_ropeterm_explanation_md(destination_dir)
    save_keywords_by_chapter_md(destination_dir)  # docs\keywords_by_chapter.md

    # # resave json files so that they are ordered alphabetically
    # for chapter_dir in get_chapter_descs().values():
    #     json_file_tuples = get_dir_filenames(chapter_dir, {"json"})
    #     for x_dir, x_filename in json_file_tuples:
    #         json_filepath = create_path(x_dir, x_filename)
    #         print(f"{json_filepath=}")
    #         print(f"{x_dir} {x_filename=}")
    #         json_dir = create_path(chapter_dir, x_dir)
    #         save_json(json_dir, x_filename, open_json(json_dir, x_filename))
