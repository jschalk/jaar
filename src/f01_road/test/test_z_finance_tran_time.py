from src.f01_road.road import get_default_deal_idea
from src.f01_road.finance_tran import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert not x_timeconversion.deal_idea
    assert not x_timeconversion.addin


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_deal_idea = "accord34"
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_deal_idea, accord_addin)

    # THEN
    assert x_timeconversion.deal_idea == accord_deal_idea
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.deal_idea == get_default_deal_idea()
    assert x_timeconversion.addin == 0
