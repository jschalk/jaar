from src.a10_bud_calc._test_util.a10_str import (
    jmetrics_str,
    fund_take_str,
    fund_give_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert fund_take_str() == "fund_take"
    assert fund_give_str() == "fund_give"
