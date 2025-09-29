from src.ch12_hub_toolbox._ref.ch12_keywords import Ch12Keywords, Ch12Keywords as wx


def test_Ch12Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch12Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
