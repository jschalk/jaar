from src.ch20_world_logic._ref.ch20_keywords import Ch20Keywords, WorldName_str


def test_Ch20Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch20Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert WorldName_str() == "WorldName"
