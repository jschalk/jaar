from src.a01_term_logic._test_util.a01_str import (
    LabelTerm_str,
    NameTerm_str,
    TitleTerm_str,
    WayTerm_str,
    bridge_str,
    parent_way_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH
    assert bridge_str() == "bridge"
    assert NameTerm_str() == "NameTerm"
    assert TitleTerm_str() == "TitleTerm"
    assert LabelTerm_str() == "LabelTerm"
    assert WayTerm_str() == "WayTerm"
    assert parent_way_str() == "parent_way"
