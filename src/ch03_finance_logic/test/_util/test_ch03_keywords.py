from src.ch03_finance_logic._ref.ch03_keywords import (
    BitNum_str,
    Ch03Keywords,
    FundIota_str,
    FundNum_str,
    GrainFloat_str,
    MoneyUnit_str,
    PennyNum_str,
    RespectNum_str,
    fund_iota_str,
    fund_pool_str,
    magnitude_str,
    penny_str,
)


def test_Ch03Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch03Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert BitNum_str() == "BitNum"
    assert FundIota_str() == "FundIota"
    assert GrainFloat_str() == "GrainFloat"
    assert FundNum_str() == "FundNum"
    assert MoneyUnit_str() == "MoneyUnit"
    assert PennyNum_str() == "PennyNum"
    assert RespectNum_str() == "RespectNum"
    assert fund_pool_str() == "fund_pool"
    assert fund_iota_str() == "fund_iota"
    assert magnitude_str() == "magnitude"
    assert penny_str() == "penny"
