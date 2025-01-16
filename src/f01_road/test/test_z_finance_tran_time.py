from src.f01_road.road import get_default_fiscal_title
from src.f01_road.finance_tran import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert not x_timeconversion.fiscal_title
    assert not x_timeconversion.addin


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_fiscal_title = "accord34"
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_fiscal_title, accord_addin)

    # THEN
    assert x_timeconversion.fiscal_title == accord_fiscal_title
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.fiscal_title == get_default_fiscal_title()
    assert x_timeconversion.addin == 0
