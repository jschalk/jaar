from src._road.finance import (
    CoinNum,
    BudNum,
    PixelNum,
    PennyNum,
    MoneyUnit,
    default_bud_pool,
    validate_bud_pool,
    default_coin_if_none,
    default_pixel_if_none,
    default_penny_if_none,
    trim_coin_excess,
    trim_pixel_excess,
    trim_penny_excess,
    FiscalUnit,
)
from inspect import getdoc as inspect_getdoc


def test_PixelNum_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pixelnum = PixelNum(x_float)
    # THEN
    assert y_pixelnum == x_float
    inspect_str = "Smallest Unit of credor_weight or debtor_weight"
    assert inspect_getdoc(y_pixelnum) == inspect_str


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


def test_PennyNum_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_pennynum = PennyNum(x_float)
    # THEN
    assert y_pennynum == x_float
    assert inspect_getdoc(y_pennynum) == "Smallest Unit of Money"


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


def test_BudNum_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_budnum = BudNum(x_float)
    # THEN
    assert y_budnum == x_float
    inspect_str = "BudNum inherits from float class"
    assert inspect_getdoc(y_budnum) == inspect_str


def test_default_bud_pool_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert default_bud_pool() == 1000000000


def test_pool_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert validate_bud_pool() == default_bud_pool()
    assert validate_bud_pool(None) == default_bud_pool()
    assert validate_bud_pool(0.5) == default_coin_if_none()
    assert validate_bud_pool(default_coin_if_none() - 0.01) == default_coin_if_none()
    assert validate_bud_pool(1) == 1
    assert validate_bud_pool(25) == 25


def test_CoinNum_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_coinnum = CoinNum(x_float)
    # THEN
    assert y_coinnum == x_float
    inspect_str = "Smallest Unit of bud"
    assert inspect_getdoc(y_coinnum) == inspect_str


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


def test_FiscalUnit_Exists():
    # GIVEN / WHEN
    x_fiscal = FiscalUnit()

    # THEN
    assert x_fiscal._bud_pool is None
    assert x_fiscal._coin is None
    assert x_fiscal._pixel is None
    assert x_fiscal._penny is None


# def test_fiscalunit_shop_ReturnsCorrectObj():
#     # GIVEN
#     casa_text = "casa"
#     casa_road = create_road(root_label(), casa_text)
#     email_text = "check email"
#     email_road = create_road(casa_road, email_text)

#     # WHEN
#     email_fiscal = fiscalunit_shop(need=email_road)

#     # THEN
#     assert email_fiscal.need == email_road


# def test_FiscalUnit_clear_status_CorrectlySetsAttrs():
#     # WHEN
#     casa_text = "casa"
#     casa_road = create_road(root_label(), casa_text)
#     casa_fiscal = fiscalunit_shop(need=casa_road)
#     # THEN
#     assert casa_fiscal._status is None

#     # GIVEN
#     casa_fiscal._status = True
#     assert casa_fiscal._status

#     # WHEN
#     casa_fiscal.clear_status()

#     # THEN
#     assert casa_fiscal._status is None
