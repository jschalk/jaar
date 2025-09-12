from src.a98_docs_builder.module_eval import save_str_funcs_md


def test_SpecialTestThatBuildsDocs():
    # ESTABLISH / WHEN / THEN
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    # docs\a17_idea_brick_formats\ (#TODO build from test_idea_brick_formats_MarkdownFileExists)
    # docs\idea_brick_formats.md (#TODO build from test_idea_brick_formats_MarkdownFileExists)
    # docs\module_blurbs.md (#TODO put blurb in each module and rebuild this markdown file each run)
    # docs\ropeterm_explanation.md (Probably leave as is)
    save_str_funcs_md("docs")  # docs\str_funcs.md
