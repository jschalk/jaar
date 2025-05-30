from src.a10_bud_calc._test_util.a10_str import bud_groupunit_str, jmetrics_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert bud_groupunit_str() == "bud_groupunit"
