from src._road.finance import (
    BudCoin,
    BudNum,
    BitNum,
    PennyNum,
    MoneyUnit,
    RespectNum,
    default_bud_pool,
    validate_bud_pool,
    default_respect_num,
    validate_respect_num,
    default_bud_coin_if_none,
    default_bit_if_none,
    default_penny_if_none,
    trim_bud_coin_excess,
    trim_bit_excess,
    trim_penny_excess,
    FiscalUnit,
    valid_fiscal_ratio,
)
from inspect import getdoc as inspect_getdoc


def test_BitNum_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_BitNum = BitNum(x_float)
    # THEN
    assert y_BitNum == x_float
    inspect_str = "Smallest Unit of credor_weight or debtor_weight ala 'the slightest bit of respect!'"
    assert inspect_getdoc(y_BitNum) == inspect_str


def test_default_bit_if_none_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert default_bit_if_none() == 1
    assert default_bit_if_none(None) == 1
    assert default_bit_if_none(5) == 5
    assert default_bit_if_none(0.03) == 1


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


def test_BudNum_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_budnum = BudNum(x_float)
    # THEN
    assert y_budnum == x_float
    inspect_str = "BudNum inherits from float class"
    assert inspect_getdoc(y_budnum) == inspect_str


def test_default_bud_pool_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_bud_pool() == 1000000000


def test_validate_bud_pool_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_bud_pool() == default_bud_pool()
    assert validate_bud_pool(None) == default_bud_pool()
    assert validate_bud_pool(0.5) == default_bud_coin_if_none()
    assert (
        validate_bud_pool(default_bud_coin_if_none() - 0.01)
        == default_bud_coin_if_none()
    )
    assert validate_bud_pool(1) == 1
    assert validate_bud_pool(25) == 25


def test_BudCoin_exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_bud_coinnum = BudCoin(x_float)
    # THEN
    assert y_bud_coinnum == x_float
    inspect_str = "Smallest Unit of bud"
    assert inspect_getdoc(y_bud_coinnum) == inspect_str


def test_default_bud_coin_if_none_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert default_bud_coin_if_none() == 1
    assert default_bud_coin_if_none(5) == 5
    assert default_bud_coin_if_none(0.03) == 0.03


def test_trim_bud_coin_excess_ReturnsCorrectedFloat():
    # ESTABLISH / WHEN / THEN
    assert trim_bud_coin_excess(num=5.5, bud_coin=1) == 5
    assert trim_bud_coin_excess(num=0.5, bud_coin=1) == 0
    assert trim_bud_coin_excess(num=5.5, bud_coin=0.1) == 5.5
    assert trim_bud_coin_excess(num=0.5, bud_coin=0.01) == 0.5
    assert trim_bud_coin_excess(num=0.56, bud_coin=0.1) == 0.5
    assert trim_bud_coin_excess(num=0.56, bud_coin=0.133) == 0.532


def test_FiscalUnit_Exists():
    # ESTABLISH / WHEN
    x_fiscal = FiscalUnit()

    # THEN
    assert x_fiscal._bud_pool is None
    assert x_fiscal._bud_coin is None
    assert x_fiscal._bit is None
    assert x_fiscal._penny is None


def test_default_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_respect_num() == default_bud_pool()


def test_validate_respect_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_respect_num() == default_respect_num()
    assert validate_respect_num(None) == default_respect_num()
    assert validate_respect_num(0.5) == default_bit_if_none()
    assert validate_respect_num(0.5) == 1
    assert (
        validate_respect_num(default_bud_coin_if_none() - 0.01)
        == default_bud_coin_if_none()
    )
    assert validate_respect_num(1) == 1
    assert validate_respect_num(25) == 25


def test_valid_fiscal_ratio_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert valid_fiscal_ratio(10, 1)
    assert valid_fiscal_ratio(10, 3) is False
    assert valid_fiscal_ratio(10.1, 1) is False
    assert valid_fiscal_ratio(10.1, 0.1) is False
    inspect_str = """Checks that big_number is wholly divisible by small_number"""
    assert inspect_getdoc(valid_fiscal_ratio) == inspect_str
