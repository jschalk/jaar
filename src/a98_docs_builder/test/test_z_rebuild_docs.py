from src.a98_docs_builder.doc_builder import save_module_blurbs_md, save_str_funcs_md


def test_SpecialTestThatBuildsDocs():
    # ESTABLISH / WHEN / THEN
    destination_dir = "docs"
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    # docs\a17_idea_brick_formats\ (#TODO build from test_idea_brick_formats_MarkdownFileExists)
    # docs\idea_brick_formats.md (#TODO build from test_idea_brick_formats_MarkdownFileExists)
    save_module_blurbs_md(destination_dir)
    # docs\ropeterm_explanation.md (Probably leave as is)
    save_str_funcs_md(destination_dir)  # docs\str_funcs.md
