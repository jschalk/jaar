from src.f07_deal.deal_config import (
    timeline_str,
    current_time_str,
    turnlogs_str,
    bankbook_str,
    amount_str,
    month_idea_str,
    hour_idea_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_idea_str,
    weekday_order_str,
    dealunit_str,
    deal_turnlog_str,
    deal_turn_episode_str,
    deal_bankbook_str,
    deal_timeline_hour_str,
    deal_timeline_month_str,
    deal_timeline_weekday_str,
)


def test_str_functions_ReturnsObj():
    assert timeline_str() == "timeline"
    assert current_time_str() == "current_time"
    assert turnlogs_str() == "turnlogs"
    assert bankbook_str() == "bankbook"
    assert amount_str() == "amount"
    assert month_idea_str() == "month_idea"
    assert hour_idea_str() == "hour_idea"
    assert cumlative_minute_str() == "cumlative_minute"
    assert cumlative_day_str() == "cumlative_day"
    assert weekday_idea_str() == "weekday_idea"
    assert weekday_order_str() == "weekday_order"
    assert dealunit_str() == "dealunit"
    assert deal_turnlog_str() == "deal_turnlog"
    assert deal_turn_episode_str() == "deal_turn_episode"
    assert deal_bankbook_str() == "deal_bankbook"
    assert deal_timeline_hour_str() == "deal_timeline_hour"
    assert deal_timeline_month_str() == "deal_timeline_month"
    assert deal_timeline_weekday_str() == "deal_timeline_weekday"
