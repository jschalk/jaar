from src.a02_finance_logic._ref.a02_terms import (
    fund_iota_str,
    fund_pool_str,
    knot_str,
    magnitude_str,
    penny_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert knot_str() == "knot"
    assert fund_pool_str() == "fund_pool"
    assert fund_iota_str() == "fund_iota"
    assert magnitude_str() == "magnitude"
    assert penny_str() == "penny"
