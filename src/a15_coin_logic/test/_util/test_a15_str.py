from src.a15_coin_logic.test._util.a15_str import (
    brokerunits_str,
    coin_budunit_str,
    coin_paybook_str,
    coin_timeline_hour_str,
    coin_timeline_month_str,
    coin_timeline_weekday_str,
    coin_timeoffi_str,
    coinunit_str,
    cumulative_minute_str,
    hour_label_str,
    job_listen_rotations_str,
    month_label_str,
    paybook_str,
    weekday_label_str,
    weekday_order_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert coinunit_str() == "coinunit"
    assert coin_budunit_str() == "coin_budunit"
    assert coin_paybook_str() == "coin_paybook"
    assert coin_timeline_hour_str() == "coin_timeline_hour"
    assert coin_timeline_month_str() == "coin_timeline_month"
    assert coin_timeline_weekday_str() == "coin_timeline_weekday"
    assert coin_timeoffi_str() == "coin_timeoffi"
    assert brokerunits_str() == "brokerunits"
    assert cumulative_minute_str() == "cumulative_minute"
    assert hour_label_str() == "hour_label"
    assert paybook_str() == "paybook"
    assert month_label_str() == "month_label"
    assert job_listen_rotations_str() == "job_listen_rotations"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
