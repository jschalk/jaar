from src.a04_reason_logic.test._util.a04_str import (
    _active_str,
    _chore_str,
    _status_str,
    belief_label_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert _active_str() == "_active"
    assert _status_str() == "_status"
    assert _chore_str() == "_chore"
    assert belief_label_str() == "belief_label"
    assert fact_context_str() == "fact_context"
    assert fact_upper_str() == "fact_upper"
    assert fact_lower_str() == "fact_lower"
    assert fact_state_str() == "fact_state"
    assert reason_divisor_str() == "reason_divisor"
    assert reason_upper_str() == "reason_upper"
    assert reason_lower_str() == "reason_lower"
    assert reason_state_str() == "reason_state"
    assert reason_active_requisite_str() == "reason_active_requisite"
    assert reason_context_str() == "reason_context"
