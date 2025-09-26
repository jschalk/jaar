from src.ch03_finance_logic._ref.ch03_keywords import (
    BitNum_str,
    FundIota_str,
    FundNum_str,
    GrainFloat_str,
    MoneyUnit_str,
    PennyNum_str,
    RespectNum_str,
    fund_iota_str,
    fund_pool_str,
    knot_str,
    magnitude_str,
    penny_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert BitNum_str() == "BitNum"
    assert FundIota_str() == "FundIota"
    assert GrainFloat_str() == "GrainFloat"
    assert FundNum_str() == "FundNum"
    assert MoneyUnit_str() == "MoneyUnit"
    assert PennyNum_str() == "PennyNum"
    assert RespectNum_str() == "RespectNum"
    assert knot_str() == "knot"
    assert fund_pool_str() == "fund_pool"
    assert fund_iota_str() == "fund_iota"
    assert magnitude_str() == "magnitude"
    assert penny_str() == "penny"
