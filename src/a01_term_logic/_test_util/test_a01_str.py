from src.a01_term_logic._test_util.a01_str import (
    bridge_str,
    NameTerm_str,
    TitleTerm_str,
    LabelTerm_str,
    WayTerm_str,
    fisc_label_str,
    parent_way_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH
    assert bridge_str() == "bridge"
    assert NameTerm_str() == "NameTerm"
    assert TitleTerm_str() == "TitleTerm"
    assert LabelTerm_str() == "LabelTerm"
    assert WayTerm_str() == "WayTerm"
    assert fisc_label_str() == "fisc_label"
    assert parent_way_str() == "parent_way"
