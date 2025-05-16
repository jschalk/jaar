from src.a01_way_logic.way import get_default_fisc_word
from src.a02_finance_logic.deal import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert not x_timeconversion.fisc_word
    assert not x_timeconversion.addin


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_fisc_word = "accord34"
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_fisc_word, accord_addin)

    # THEN
    assert x_timeconversion.fisc_word == accord_fisc_word
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.fisc_word == get_default_fisc_word()
    assert x_timeconversion.addin == 0
