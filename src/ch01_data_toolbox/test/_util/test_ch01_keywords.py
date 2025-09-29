from src.ch01_data_toolbox._ref.ch01_keywords import Ch01Keywords


def test_Ch01Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch01Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
