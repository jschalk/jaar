from src.a03_group_logic._test_util.a03_str import credit_belief_str, debtit_belief_str


def test_strs_a03_functions_ReturnObjs():
    # ESTABLISH
    assert credit_belief_str() == "credit_belief"
    assert debtit_belief_str() == "debtit_belief"
