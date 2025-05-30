from src.a10_bud_calc._test_util.a10_str import jmetrics_str, bud_groupunit_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert bud_groupunit_str() == "bud_groupunit"
