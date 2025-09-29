from src.ch10_pack_logic._ref.ch10_keywords import Ch10Keywords


def test_Ch10Keywords_AttributeNamesEqualValues():
    """Test that all Ch10Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch10Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
