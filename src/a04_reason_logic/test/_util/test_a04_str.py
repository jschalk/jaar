from src.a04_reason_logic.test._util.a04_str import (
    _active_str,
    _chore_str,
    _status_str,
    belief_label_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    labor_title_str,
    pdivisor_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
    rplan_active_requisite_str,
)


def test_str_functions_ReturnsObj():
    assert _active_str() == "_active"
    assert _status_str() == "_status"
    assert _chore_str() == "_chore"
    assert belief_label_str() == "belief_label"
    assert fcontext_str() == "fcontext"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fstate_str() == "fstate"
    assert labor_title_str() == "labor_title"
    assert pdivisor_str() == "pdivisor"
    assert pnigh_str() == "pnigh"
    assert popen_str() == "popen"
    assert pstate_str() == "pstate"
    assert rplan_active_requisite_str() == "rplan_active_requisite"
    assert rcontext_str() == "rcontext"
