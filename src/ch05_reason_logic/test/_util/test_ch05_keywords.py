from src.ch05_reason_logic._ref.ch05_keywords import (
    Ch05Keywords,
    active_str,
    cases_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    factheirs_str,
    factunits_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    reasonunits_str,
    status_str,
    task_str,
)


def test_Ch05Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch05Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert active_str() == "active"
    assert status_str() == "status"
    assert task_str() == "task"
    assert cases_str() == "cases"
    assert fact_context_str() == "fact_context"
    assert fact_upper_str() == "fact_upper"
    assert fact_lower_str() == "fact_lower"
    assert fact_state_str() == "fact_state"
    assert factheirs_str() == "factheirs"
    assert factunits_str() == "factunits"
    assert reason_divisor_str() == "reason_divisor"
    assert reason_upper_str() == "reason_upper"
    assert reason_lower_str() == "reason_lower"
    assert reason_state_str() == "reason_state"
    assert reason_active_requisite_str() == "reason_active_requisite"
    assert reason_context_str() == "reason_context"
    assert reasonunits_str() == "reasonunits"
