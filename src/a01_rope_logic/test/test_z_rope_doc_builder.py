from src.a00_data_toolbox.file_toolbox import open_file
from src.a01_rope_logic._ref.a01_doc_builder import get_ropeterm_explanation_md


def test_get_ropeterm_explanation_md_ReturnsObj():
    # ESTABLISH / WHEN
    ropeterm_explanation_md = get_ropeterm_explanation_md()

    # THEN
    assert ropeterm_explanation_md
    expected_ropeterm_explanation_md = open_file("docs/ropeterm_explanation.md")
    # print(ropeterm_explanation_md)
    assert ropeterm_explanation_md == expected_ropeterm_explanation_md
