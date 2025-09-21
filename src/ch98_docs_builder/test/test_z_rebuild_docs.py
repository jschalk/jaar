from src.ch98_docs_builder.doc_builder import (
    save_brick_formats_md,
    save_idea_brick_mds,
    save_module_blurbs_md,
    save_ropepointer_explanation_md,
    save_str_funcs_md,
)


def test_SpecialTestThatBuildsDocs():
    # ESTABLISH / WHEN / THEN
    destination_dir = "docs"
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    save_idea_brick_mds(destination_dir)
    save_brick_formats_md(destination_dir)
    save_module_blurbs_md(destination_dir)
    save_ropepointer_explanation_md(destination_dir)
    save_str_funcs_md(destination_dir)  # docs\str_funcs.md
