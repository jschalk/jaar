from src.f01_road.road import get_default_fiscal_id_ideaunit
from src.f01_road.finance_tran import TimeConversion, timeconversion_shop


def test_TimeConversion_Exists():
    # ESTABLISH / WHEN
    x_timeconversion = TimeConversion()

    # THEN
    assert x_timeconversion.fiscal_id is None
    assert x_timeconversion.addin is None


def test_timeconversion_shop_ReturnObj_WithParameters():
    # ESTABLISH
    music_fiscal_id = 91
    music_addin = 91

    # WHEN
    x_timeconversion = timeconversion_shop(music_fiscal_id, music_addin)

    # THEN
    assert x_timeconversion.fiscal_id == music_fiscal_id
    assert x_timeconversion.addin == music_addin


def test_timeconversion_shop_ReturnObj_EmtpyParameters():
    # ESTABLISH / WHEN
    x_timeconversion = timeconversion_shop()

    # THEN
    assert x_timeconversion.fiscal_id == get_default_fiscal_id_ideaunit()
    assert x_timeconversion.addin == 0
