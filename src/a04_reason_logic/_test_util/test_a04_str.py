from src.a04_reason_logic._test_util.a04_str import (
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    labor_title_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rconcept_active_requisite_str,
    rcontext_str,
)


def test_str_functions_ReturnsObj():
    assert pstate_str() == "pstate"
    assert pnigh_str() == "pnigh"
    assert fstate_str() == "fstate"
    assert popen_str() == "popen"
    assert fcontext_str() == "fcontext"
    assert rconcept_active_requisite_str() == "rconcept_active_requisite"
    assert fopen_str() == "fopen"
    assert fnigh_str() == "fnigh"
    assert rcontext_str() == "rcontext"
    assert labor_title_str() == "labor_title"
