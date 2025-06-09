from src.a15_vow_logic._test_util.a15_str import (
    brokerunits_str,
    cumlative_day_str,
    cumlative_minute_str,
    hour_label_str,
    month_label_str,
    paybook_str,
    vow_dealunit_str,
    vow_paybook_str,
    vow_timeline_hour_str,
    vow_timeline_month_str,
    vow_timeline_weekday_str,
    vow_timeoffi_str,
    vowunit_str,
    weekday_label_str,
    weekday_order_str,
)


def test_str_functions_ReturnsObj():
    assert brokerunits_str() == "brokerunits"
    assert paybook_str() == "paybook"
    assert month_label_str() == "month_label"
    assert hour_label_str() == "hour_label"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
    assert vowunit_str() == "vowunit"
    assert vow_dealunit_str() == "vow_dealunit"
    assert vow_paybook_str() == "vow_paybook"
    assert vow_timeline_hour_str() == "vow_timeline_hour"
    assert vow_timeline_month_str() == "vow_timeline_month"
    assert vow_timeline_weekday_str() == "vow_timeline_weekday"
    assert vow_timeoffi_str() == "vow_timeoffi"
