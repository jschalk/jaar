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
    p_divisor_str,
    p_lower_str,
    p_state_str,
    p_upper_str,
    r_context_str,
    r_plan_active_requisite_str,
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
    assert p_divisor_str() == "p_divisor"
    assert p_upper_str() == "p_upper"
    assert p_lower_str() == "p_lower"
    assert p_state_str() == "p_state"
    assert r_plan_active_requisite_str() == "r_plan_active_requisite"
    assert r_context_str() == "r_context"
