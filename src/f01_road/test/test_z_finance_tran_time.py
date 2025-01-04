from src.f01_road.road import get_default_cmty_title
from src.f01_road.finance_tran import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert not x_timeconversion.cmty_title
    assert not x_timeconversion.addin


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_cmty_title = "accord34"
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_cmty_title, accord_addin)

    # THEN
    assert x_timeconversion.cmty_title == accord_cmty_title
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.cmty_title == get_default_cmty_title()
    assert x_timeconversion.addin == 0
