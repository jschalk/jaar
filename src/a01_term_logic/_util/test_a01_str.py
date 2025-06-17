from src.a01_term_logic._util.a01_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    knot_str,
    parent_rope_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH
    assert knot_str() == "knot"
    assert NameTerm_str() == "NameTerm"
    assert TitleTerm_str() == "TitleTerm"
    assert LabelTerm_str() == "LabelTerm"
    assert RopeTerm_str() == "RopeTerm"
    assert parent_rope_str() == "parent_rope"
