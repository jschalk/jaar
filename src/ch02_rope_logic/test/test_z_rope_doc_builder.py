from src.ch01_data_toolbox.file_toolbox import open_file
from src.ch02_rope_logic._ref.ch02_doc_builder import get_ropepointer_explanation_md


def test_get_ropepointer_explanation_md_ReturnsObj():
    # ESTABLISH / WHEN
    ropepointer_explanation_md = get_ropepointer_explanation_md()

    # THEN
    assert ropepointer_explanation_md
    expected_ropepointer_explanation_md = open_file("docs/ropepointer_explanation.md")
    # print(ropepointer_explanation_md)
    assert ropepointer_explanation_md == expected_ropepointer_explanation_md
