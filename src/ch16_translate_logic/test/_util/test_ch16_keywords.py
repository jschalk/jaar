from src.ch16_translate_logic._ref.ch16_keywords import Ch16Keywords


def test_Ch16Keywords_AttributeNamesEqualValues():
    """Test that all Ch16Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch16Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
