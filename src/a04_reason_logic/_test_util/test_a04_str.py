from src.a04_reason_logic._test_util.a04_str import (
    _active_str,
    _chore_str,
    _status_str,
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
    assert _active_str() == "_active"
    assert _status_str() == "_status"
    assert _chore_str() == "_chore"
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
