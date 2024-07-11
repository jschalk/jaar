from src._road.finance import (
    CoinUnit,
    BudgetUnit,
    PixelUnit,
    PennyUnit,
    MoneyUnit,
    default_budget,
    validate_budget,
    default_coin_if_none,
    default_pixel_if_none,
    default_penny_if_none,
    trim_coin_excess,
    trim_pixel_excess,
    trim_penny_excess,
    FiscalUnit,
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


def test_BudgetUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_budgetunit = BudgetUnit(x_float)
    # THEN
    assert y_budgetunit == x_float
    inspect_str = "BudgetUnit inherits from float class"
    assert inspect_getdoc(y_budgetunit) == inspect_str


def test_default_budget_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert default_budget() == 1000000000


def test_validate_budget_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert validate_budget() == default_budget()
    assert validate_budget(None) == default_budget()
    assert validate_budget(0.5) == default_coin_if_none()
    assert validate_budget(default_coin_if_none() - 0.01) == default_coin_if_none()
    assert validate_budget(1) == 1
    assert validate_budget(25) == 25


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


def test_FiscalUnit_Exists():
    # GIVEN / WHEN
    x_fiscal = FiscalUnit()

    # THEN
    assert x_fiscal._budget is None
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
