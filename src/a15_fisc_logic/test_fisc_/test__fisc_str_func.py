from src.a15_fisc_logic.fisc_config import (
    timeline_str,
    offi_time_str,
    brokerunits_str,
    cashbook_str,
    amount_str,
    month_tag_str,
    hour_tag_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_tag_str,
    weekday_order_str,
    fiscunit_str,
    fisc_dealunit_str,
    fisc_cashbook_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
)


def test_str_functions_ReturnsObj():
    assert timeline_str() == "timeline"
    assert offi_time_str() == "offi_time"
    assert brokerunits_str() == "brokerunits"
    assert cashbook_str() == "cashbook"
    assert amount_str() == "amount"
    assert month_tag_str() == "month_tag"
    assert hour_tag_str() == "hour_tag"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_tag_str() == "weekday_tag"
    assert weekday_order_str() == "weekday_order"
    assert fiscunit_str() == "fiscunit"
    assert fisc_dealunit_str() == "fisc_dealunit"
    assert fisc_cashbook_str() == "fisc_cashbook"
    assert fisc_timeline_hour_str() == "fisc_timeline_hour"
    assert fisc_timeline_month_str() == "fisc_timeline_month"
    assert fisc_timeline_weekday_str() == "fisc_timeline_weekday"
