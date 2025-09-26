from src.ch02_rope_logic._ref.ch02_keywords import (
    CentralLabel_str,
    KnotTerm_str,
    LabelTerm_str,
    MomentLabel_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    knot_str,
    parent_rope_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert CentralLabel_str() == "CentralLabel"
    assert LabelTerm_str() == "LabelTerm"
    assert KnotTerm_str() == "KnotTerm"
    assert knot_str() == "knot"
    assert MomentLabel_str() == "MomentLabel"
    assert NameTerm_str() == "NameTerm"
    assert parent_rope_str() == "parent_rope"
    assert RopeTerm_str() == "RopeTerm"
    assert TitleTerm_str() == "TitleTerm"
