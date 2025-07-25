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
    r_context_str,
    r_divisor_str,
    r_lower_str,
    r_plan_active_requisite_str,
    r_state_str,
    r_upper_str,
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
    assert r_divisor_str() == "r_divisor"
    assert r_upper_str() == "r_upper"
    assert r_lower_str() == "r_lower"
    assert r_state_str() == "r_state"
    assert r_plan_active_requisite_str() == "r_plan_active_requisite"
    assert r_context_str() == "r_context"
