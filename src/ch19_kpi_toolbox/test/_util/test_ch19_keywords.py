from src.ch19_kpi_toolbox._ref.ch19_keywords import Ch19Keywords


def test_Ch19Keywords_AttributeNamesEqualValues():
    """Test that all Ch19Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch19Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
