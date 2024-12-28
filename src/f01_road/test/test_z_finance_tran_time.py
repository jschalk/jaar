from src.f01_road.road import get_default_deal_id_ideaunit
from src.f01_road.finance_tran import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert x_timeconversion.deal_id is None
    assert x_timeconversion.addin is None


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    accord_deal_id = 91
    accord_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(accord_deal_id, accord_addin)

    # THEN
    assert x_timeconversion.deal_id == accord_deal_id
    assert x_timeconversion.addin == accord_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.deal_id == get_default_deal_id_ideaunit()
    assert x_timeconversion.addin == 0
