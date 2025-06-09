from src.a10_plan_calc._test_util.a10_str import jmetrics_str, plan_groupunit_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert plan_groupunit_str() == "plan_groupunit"
