from src.a15_fisc_logic._test_util.a15_str import (
    brokerunits_str,
    cashbook_str,
    cumlative_day_str,
    cumlative_minute_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
    fiscunit_str,
    hour_label_str,
    month_label_str,
    weekday_label_str,
    weekday_order_str,
)


def test_str_functions_ReturnsObj():
    assert brokerunits_str() == "brokerunits"
    assert cashbook_str() == "cashbook"
    assert month_label_str() == "month_label"
    assert hour_label_str() == "hour_label"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
    assert fiscunit_str() == "fiscunit"
    assert fisc_dealunit_str() == "fisc_dealunit"
    assert fisc_cashbook_str() == "fisc_cashbook"
    assert fisc_timeline_hour_str() == "fisc_timeline_hour"
    assert fisc_timeline_month_str() == "fisc_timeline_month"
    assert fisc_timeline_weekday_str() == "fisc_timeline_weekday"
    assert fisc_timeoffi_str() == "fisc_timeoffi"
