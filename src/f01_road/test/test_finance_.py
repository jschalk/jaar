from src.f01_road.finance import (
    FundCoin,
    FundNum,
    BitNum,
    PennyNum,
    MoneyUnit,
    RespectNum,
    default_fund_pool,
    validate_fund_pool,
    default_respect_num,
    validate_respect_num,
    default_fund_coin_if_none,
    default_respect_bit_if_none,
    default_penny_if_none,
    trim_fund_coin_excess,
    trim_bit_excess,
    trim_penny_excess,
    valid_finance_ratio,
    get_net,
)
from inspect import getdoc as inspect_getdoc
from pytest import raises as pytest_raises


def test_BitNum_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_BitNum = BitNum(x_float)
    # THEN
    assert y_BitNum == x_float
    inspect_str = "Smallest Unit of credit_belief or debtit_belief (RespectNum) ala 'the slightest bit of respect!'"
    assert inspect_getdoc(y_BitNum) == inspect_str


def test_default_respect_bit_if_none_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert default_respect_bit_if_none() == 1
    assert default_respect_bit_if_none(None) == 1
    assert default_respect_bit_if_none(5) == 5
    assert default_respect_bit_if_none(0.03) == 1


def test_trim_bit_excess_ReturnsCorrectedFloat():
    # ESTABLISH / WHEN / THEN
    assert trim_bit_excess(num=5.5, bit=1) == 5
    assert trim_bit_excess(num=0.5, bit=1) == 0
    assert trim_bit_excess(num=5.5, bit=0.1) == 5.5
    assert trim_bit_excess(num=0.5, bit=0.01) == 0.5
    assert trim_bit_excess(num=0.56, bit=0.1) == 0.5
    assert trim_bit_excess(num=0.56, bit=0.133) == 0.532


def test_RespectNum_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectNum = RespectNum(x_float)
    # THEN
    assert y_RespectNum == x_float
    assert inspect_getdoc(y_RespectNum) == "RespectNum inherits from float class"


def test_PennyNum_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_pennynum = PennyNum(x_float)
    # THEN
    assert y_pennynum == x_float
    assert inspect_getdoc(y_pennynum) == "Smallest Unit of Money"


def test_default_penny_if_none_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert default_penny_if_none() == 1
    assert default_penny_if_none(5) == 5
    assert default_penny_if_none(0.03) == 1


def test_trim_penny_excess_ReturnsCorrectedFloat():
    # ESTABLISH / WHEN / THEN
    assert trim_penny_excess(num=5.5, penny=1) == 5
    assert trim_penny_excess(num=0.5, penny=1) == 0
    assert trim_penny_excess(num=5.5, penny=0.1) == 5.5
    assert trim_penny_excess(num=0.5, penny=0.01) == 0.5
    assert trim_penny_excess(num=0.56, penny=0.1) == 0.5
    assert trim_penny_excess(num=0.56, penny=0.133) == 0.532


def test_MoneyUnit_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_moneyunit = MoneyUnit(x_float)
    # THEN
    assert y_moneyunit == x_float
    assert inspect_getdoc(y_moneyunit) == "MoneyUnit inherits from float class"


def test_FundNum_exists():
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
    assert validate_fund_pool(0.5) == default_fund_coin_if_none()
    assert (
        validate_fund_pool(default_fund_coin_if_none() - 0.01)
        == default_fund_coin_if_none()
    )
    assert validate_fund_pool(1) == 1
    assert validate_fund_pool(25) == 25


def test_FundCoin_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_coinnum = FundCoin(x_float)
    # THEN
    assert y_fund_coinnum == x_float
    inspect_str = "Smallest Unit of fund_num"
    assert inspect_getdoc(y_fund_coinnum) == inspect_str


def test_default_fund_coin_if_none_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert default_fund_coin_if_none() == 1
    assert default_fund_coin_if_none(5) == 5
    assert default_fund_coin_if_none(0.03) == 0.03


def test_trim_fund_coin_excess_ReturnsCorrectedFloat():
    # ESTABLISH / WHEN / THEN
    assert trim_fund_coin_excess(num=5.5, fund_coin=1) == 5
    assert trim_fund_coin_excess(num=0.5, fund_coin=1) == 0
    assert trim_fund_coin_excess(num=5.5, fund_coin=0.1) == 5.5
    assert trim_fund_coin_excess(num=0.5, fund_coin=0.01) == 0.5
    assert trim_fund_coin_excess(num=0.56, fund_coin=0.1) == 0.5
    assert trim_fund_coin_excess(num=0.56, fund_coin=0.133) == 0.532


def test_default_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_respect_num() == default_fund_pool()


def test_validate_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_respect_num() == default_respect_num()
    assert validate_respect_num(None) == default_respect_num()
    assert validate_respect_num(0.5) == default_respect_bit_if_none()
    assert validate_respect_num(0.5) == 1
    assert (
        validate_respect_num(default_fund_coin_if_none() - 0.01)
        == default_fund_coin_if_none()
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
