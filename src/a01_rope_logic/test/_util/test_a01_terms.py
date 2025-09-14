from src.a01_rope_logic.test._util.a01_terms import (
    LabelTerm_str,
    NameTerm_str,
    RopePointer_str,
    TitleTerm_str,
    knot_str,
    parent_rope_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert knot_str() == "knot"
    assert NameTerm_str() == "NameTerm"
    assert TitleTerm_str() == "TitleTerm"
    assert LabelTerm_str() == "LabelTerm"
    assert RopePointer_str() == "RopePointer"
    assert parent_rope_str() == "parent_rope"
