from src._road.finance import (
    CoinUnit,
    PixelUnit,
    PennyUnit,
    MoneyUnit,
    default_coin_if_none,
    default_pixel_if_none,
    default_penny_if_none,
    trim_coin_excess,
    trim_pixel_excess,
    trim_penny_excess,
)
from inspect import getdoc as inspect_getdoc


def test_PixelUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pixelunit = PixelUnit(x_float)
    # THEN
    assert y_pixelunit == x_float
    inspect_str = "Smallest Unit of credor_weight or debtor_weight"
    assert inspect_getdoc(y_pixelunit) == inspect_str


def test_default_pixel_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_pixel_if_none() == 1
    assert default_pixel_if_none(5) == 5
    assert default_pixel_if_none(0.03) == 0.03


def test_trim_pixel_excess_ReturnsCorrectedFloat():
    # GIVEN / WHEN / THEN
    assert trim_pixel_excess(num=5.5, pixel=1) == 5
    assert trim_pixel_excess(num=0.5, pixel=1) == 0
    assert trim_pixel_excess(num=5.5, pixel=0.1) == 5.5
    assert trim_pixel_excess(num=0.5, pixel=0.01) == 0.5
    assert trim_pixel_excess(num=0.56, pixel=0.1) == 0.5
    assert trim_pixel_excess(num=0.56, pixel=0.133) == 0.532


def test_PennyUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pennyunit = PennyUnit(x_float)
    # THEN
    assert y_pennyunit == x_float
    assert inspect_getdoc(y_pennyunit) == "Smallest Unit of Money"


def test_default_penny_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_penny_if_none() == 1
    assert default_penny_if_none(5) == 5
    assert default_penny_if_none(0.03) == 1


def test_trim_penny_excess_ReturnsCorrectedFloat():
    # GIVEN / WHEN / THEN
    assert trim_penny_excess(num=5.5, penny=1) == 5
    assert trim_penny_excess(num=0.5, penny=1) == 0
    assert trim_penny_excess(num=5.5, penny=0.1) == 5.5
    assert trim_penny_excess(num=0.5, penny=0.01) == 0.5
    assert trim_penny_excess(num=0.56, penny=0.1) == 0.5
    assert trim_penny_excess(num=0.56, penny=0.133) == 0.532


def test_MoneyUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_moneyunit = MoneyUnit(x_float)
    # THEN
    assert y_moneyunit == x_float
    assert inspect_getdoc(y_moneyunit) == "MoneyUnit inherits from float class"


def test_CoinUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_coinunit = CoinUnit(x_float)
    # THEN
    assert y_coinunit == x_float
    inspect_str = "Smallest Unit of budget"
    assert inspect_getdoc(y_coinunit) == inspect_str


def test_default_coin_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_coin_if_none() == 1
    assert default_coin_if_none(5) == 5
    assert default_coin_if_none(0.03) == 0.03


def test_trim_coin_excess_ReturnsCorrectedFloat():
    # GIVEN / WHEN / THEN
    assert trim_coin_excess(num=5.5, coin=1) == 5
    assert trim_coin_excess(num=0.5, coin=1) == 0
    assert trim_coin_excess(num=5.5, coin=0.1) == 5.5
    assert trim_coin_excess(num=0.5, coin=0.01) == 0.5
    assert trim_coin_excess(num=0.56, coin=0.1) == 0.5
    assert trim_coin_excess(num=0.56, coin=0.133) == 0.532
