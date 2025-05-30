from src.a04_reason_logic._test_util.a04_str import (
    _status_str,
    _task_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    labor_title_str,
    pdivisor_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rconcept_active_requisite_str,
    rcontext_str,
)


def test_str_functions_ReturnsObj():
    assert _status_str() == "_status"
    assert _task_str() == "_task"
    assert fcontext_str() == "fcontext"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fstate_str() == "fstate"
    assert labor_title_str() == "labor_title"
    assert pdivisor_str() == "pdivisor"
    assert pnigh_str() == "pnigh"
    assert popen_str() == "popen"
    assert pstate_str() == "pstate"
    assert rconcept_active_requisite_str() == "rconcept_active_requisite"
    assert rcontext_str() == "rcontext"
