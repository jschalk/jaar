from src.ch00_purpose._ref.ch00_keywords import Ch00Keywords


def test_Ch00Keywords_attribute_names_equal_values():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch00Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
