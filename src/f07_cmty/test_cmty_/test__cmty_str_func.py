from src.f07_cmty.cmty_config import (
    timeline_str,
    current_time_str,
    deallogs_str,
    cashbook_str,
    amount_str,
    month_idea_str,
    hour_idea_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_idea_str,
    weekday_order_str,
    cmtyunit_str,
    cmty_deallog_str,
    cmty_deal_episode_str,
    cmty_cashbook_str,
    cmty_timeline_hour_str,
    cmty_timeline_month_str,
    cmty_timeline_weekday_str,
)


def test_str_functions_ReturnsObj():
    assert timeline_str() == "timeline"
    assert current_time_str() == "current_time"
    assert deallogs_str() == "deallogs"
    assert cashbook_str() == "cashbook"
    assert amount_str() == "amount"
    assert month_idea_str() == "month_idea"
    assert hour_idea_str() == "hour_idea"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_idea_str() == "weekday_idea"
    assert weekday_order_str() == "weekday_order"
    assert cmtyunit_str() == "cmtyunit"
    assert cmty_deallog_str() == "cmty_deallog"
    assert cmty_deal_episode_str() == "cmty_deal_episode"
    assert cmty_cashbook_str() == "cmty_cashbook"
    assert cmty_timeline_hour_str() == "cmty_timeline_hour"
    assert cmty_timeline_month_str() == "cmty_timeline_month"
    assert cmty_timeline_weekday_str() == "cmty_timeline_weekday"
