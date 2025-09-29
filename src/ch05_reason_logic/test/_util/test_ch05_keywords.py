from src.ch05_reason_logic._ref.ch05_keywords import Ch05Keywords


def test_Ch05Keywords_AttributeNamesEqualValues():
    """Test that all Ch05Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch05Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
