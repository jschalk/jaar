from src.ch03_allot_toolbox._ref.ch03_keywords import Ch03Keywords


def test_Ch03Keywords_AttributeNamesEqualValues():
    """Test that all Ch03Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch03Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str
