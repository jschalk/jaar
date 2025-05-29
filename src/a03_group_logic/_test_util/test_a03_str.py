from src.a03_group_logic._test_util.a03_str import credit_belief_str, debtit_belief_str


def test_str_functions_ReturnsObj():
    # ESTABLISH
    assert credit_belief_str() == "credit_belief"
    assert debtit_belief_str() == "debtit_belief"
