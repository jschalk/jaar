from inspect import getdoc as inspect_getdoc
from pytest import raises as pytest_raises
from src.ch03_finance_logic.finance_config import (
    FundGrain,
    FundNum,
    MoneyUnit,
    PennyNum,
    RespectGrain,
    RespectNum,
    default_fund_grain_if_None,
    default_fund_pool,
    default_respect_num,
    default_RespectGrain_if_None,
    filter_penny,
    get_net,
    valid_finance_ratio,
    validate_fund_pool,
    validate_respect_num,
)


def test_RespectGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectGrain = RespectGrain(x_float)
    # THEN
    assert y_RespectGrain == x_float
    inspect_str = (
        "Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"
    )
    assert inspect_getdoc(y_RespectGrain) == inspect_str


def test_default_RespectGrain_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_RespectGrain_if_None() == 1
    assert default_RespectGrain_if_None(respect_grain=None) == 1
    assert default_RespectGrain_if_None(respect_grain=5) == 5
    assert default_RespectGrain_if_None(respect_grain=0.03) == 1


def test_RespectNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectNum = RespectNum(x_float)
    # THEN
    assert y_RespectNum == x_float
    assert inspect_getdoc(y_RespectNum) == "RespectNum inherits from float class"


def test_PennyNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_pennynum = PennyNum(x_float)
    # THEN
    assert y_pennynum == x_float
    assert inspect_getdoc(y_pennynum) == "Smallest Unit of Money"


def test_filter_penny_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert filter_penny() == 1
    assert filter_penny(5) == 5
    assert filter_penny(0.03) == 1


def test_MoneyUnit_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_moneyunit = MoneyUnit(x_float)
    # THEN
    assert y_moneyunit == x_float
    assert inspect_getdoc(y_moneyunit) == "MoneyUnit inherits from float class"


def test_FundNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_num = FundNum(x_float)
    # THEN
    assert y_fund_num == x_float
    inspect_str = "FundNum inherits from float class"
    assert inspect_getdoc(y_fund_num) == inspect_str


def test_default_fund_pool_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_fund_pool() == 1000000000


def test_validate_fund_pool_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_fund_pool() == default_fund_pool()
    assert validate_fund_pool(None) == default_fund_pool()
    assert validate_fund_pool(0.5) == default_fund_grain_if_None()
    assert (
        validate_fund_pool(default_fund_grain_if_None() - 0.01)
        == default_fund_grain_if_None()
    )
    assert validate_fund_pool(1) == 1
    assert validate_fund_pool(25) == 25


def test_FundGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_grainnum = FundGrain(x_float)
    # THEN
    assert y_fund_grainnum == x_float
    inspect_str = "Smallest Unit of fund_num"
    assert inspect_getdoc(y_fund_grainnum) == inspect_str


def test_default_fund_grain_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_fund_grain_if_None() == 1
    assert default_fund_grain_if_None(5) == 5
    assert default_fund_grain_if_None(0.03) == 0.03


def test_default_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_respect_num() == default_fund_pool()


def test_validate_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_respect_num() == default_respect_num()
    assert validate_respect_num(None) == default_respect_num()
    assert validate_respect_num(0.5) == default_RespectGrain_if_None()
    assert validate_respect_num(0.5) == 1
    assert (
        validate_respect_num(default_fund_grain_if_None() - 0.01)
        == default_fund_grain_if_None()
    )
    assert validate_respect_num(1) == 1
    assert validate_respect_num(25) == 25


def test_valid_finance_ratio_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert valid_finance_ratio(10, 1)
    assert valid_finance_ratio(10, 3) is False
    assert valid_finance_ratio(10.1, 1) is False
    assert valid_finance_ratio(10.1, 0.1) is False
    inspect_str = """Checks that big_number is wholly divisible by small_number"""
    assert inspect_getdoc(valid_finance_ratio) == inspect_str


def test_get_net_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_net(x_give=5, x_take=6) == -1
    assert get_net(x_give=55, x_take=6) == 49
    assert get_net(x_give=55, x_take=None) == 55
    assert get_net(x_give=None, x_take=44) == -44
    assert get_net(x_give=None, x_take=None) == 0

    with pytest_raises(Exception) as excinfo:
        get_net(x_give=-1, x_take=14)
    assert str(excinfo.value) == "get_net x_give=-1. Only non-negative numbers allowed."

    with pytest_raises(Exception) as excinfo:
        get_net(x_give=15, x_take=-5)
    assert str(excinfo.value) == "get_net x_take=-5. Only non-negative numbers allowed."

    with pytest_raises(Exception) as excinfo:
        get_net(x_give=-4, x_take=-5)
    assert (
        str(excinfo.value)
        == "get_net x_give=-4 and x_take=-5. Only non-negative numbers allowed."
    )
