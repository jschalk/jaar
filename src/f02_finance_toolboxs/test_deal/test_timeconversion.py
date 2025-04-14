from src.a01_word_logic.road import get_default_fisc_title
from src.f02_finance_toolboxs.deal import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert not x_timeconversion.fisc_title
    assert not x_timeconversion.addin


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_fisc_title = "accord34"
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_fisc_title, accord_addin)

    # THEN
    assert x_timeconversion.fisc_title == accord_fisc_title
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.fisc_title == get_default_fisc_title()
    assert x_timeconversion.addin == 0
