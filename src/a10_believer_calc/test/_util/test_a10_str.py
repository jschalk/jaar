from src.a10_believer_calc.test._util.a10_str import (
    believer_groupunit_str,
    jmetrics_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert believer_groupunit_str() == "believer_groupunit"
