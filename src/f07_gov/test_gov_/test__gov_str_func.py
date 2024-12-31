from src.f07_gov.gov_config import (
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
    govunit_str,
    gov_deallog_str,
    gov_deal_episode_str,
    gov_cashbook_str,
    gov_timeline_hour_str,
    gov_timeline_month_str,
    gov_timeline_weekday_str,
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
    assert govunit_str() == "govunit"
    assert gov_deallog_str() == "gov_deallog"
    assert gov_deal_episode_str() == "gov_deal_episode"
    assert gov_cashbook_str() == "gov_cashbook"
    assert gov_timeline_hour_str() == "gov_timeline_hour"
    assert gov_timeline_month_str() == "gov_timeline_month"
    assert gov_timeline_weekday_str() == "gov_timeline_weekday"
