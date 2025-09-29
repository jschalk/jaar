from src.ch11_bud_logic._ref.ch11_keywords import (
    Ch11Keywords,
    Ch11Keywords as wx,
    ancestors_str,
    mandate_str,
)


def test_Ch11Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch11Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    pass
