from src.ch21_lobby_logic._ref.ch21_keywords import Ch21Keywords


def test_Ch21Keywords_AttributeNamesEqualValues():
    """Test that all Ch21Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch21Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
