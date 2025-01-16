from src.f07_fiscal.fiscal_config import (
    timeline_str,
    current_time_str,
    deallogs_str,
    cashbook_str,
    amount_str,
    month_title_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_title_str,
    weekday_order_str,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
)


def test_str_functions_ReturnsObj():
    assert timeline_str() == "timeline"
    assert current_time_str() == "current_time"
    assert deallogs_str() == "deallogs"
    assert cashbook_str() == "cashbook"
    assert amount_str() == "amount"
    assert month_title_str() == "month_title"
    assert hour_title_str() == "hour_title"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_title_str() == "weekday_title"
    assert weekday_order_str() == "weekday_order"
    assert fiscalunit_str() == "fiscalunit"
    assert fiscal_deal_episode_str() == "fiscal_deal_episode"
    assert fiscal_cashbook_str() == "fiscal_cashbook"
    assert fiscal_timeline_hour_str() == "fiscal_timeline_hour"
    assert fiscal_timeline_month_str() == "fiscal_timeline_month"
    assert fiscal_timeline_weekday_str() == "fiscal_timeline_weekday"
