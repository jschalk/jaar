from src.a10_belief_calc.test._util.a10_str import belief_groupunit_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert belief_groupunit_str() == "belief_groupunit"
