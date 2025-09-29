from src.ch02_rope_logic._ref.ch02_keywords import (
    Ch02Keywords,
    KnotTerm_str,
    LabelTerm_str,
    MomentLabel_str,
    NameTerm_str,
    NexusLabel_str,
    RopeTerm_str,
    TitleTerm_str,
    knot_str,
    parent_rope_str,
)


def test_Ch02Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch02Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert NexusLabel_str() == "NexusLabel"
    assert LabelTerm_str() == "LabelTerm"
    assert KnotTerm_str() == "KnotTerm"
    assert knot_str() == "knot"
    assert MomentLabel_str() == "MomentLabel"
