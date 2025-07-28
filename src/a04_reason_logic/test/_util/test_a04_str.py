from src.a04_reason_logic.test._util.a04_str import (
    _active_str,
    _chore_str,
    _status_str,
    belief_label_str,
    f_context_str,
    f_lower_str,
    f_state_str,
    f_upper_str,
    labor_title_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
)


def test_str_functions_ReturnsObj():
    assert _active_str() == "_active"
    assert _status_str() == "_status"
    assert _chore_str() == "_chore"
    assert belief_label_str() == "belief_label"
    assert f_context_str() == "f_context"
    assert f_upper_str() == "f_upper"
    assert f_lower_str() == "f_lower"
    assert f_state_str() == "f_state"
    assert labor_title_str() == "labor_title"
    assert reason_divisor_str() == "reason_divisor"
    assert reason_upper_str() == "reason_upper"
    assert reason_lower_str() == "reason_lower"
    assert reason_state_str() == "reason_state"
    assert reason_active_requisite_str() == "reason_active_requisite"
    assert reason_context_str() == "reason_context"
