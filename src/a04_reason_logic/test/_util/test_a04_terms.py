from src.a04_reason_logic.test._util.a04_terms import (
    active_str,
    cases_str,
    chore_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    factheirs_str,
    factunits_str,
    moment_label_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    reasonunits_str,
    status_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert active_str() == "active"
    assert status_str() == "status"
    assert chore_str() == "chore"
    assert cases_str() == "cases"
    assert moment_label_str() == "moment_label"
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
