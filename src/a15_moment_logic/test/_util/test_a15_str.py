from src.a15_moment_logic.test._util.a15_str import (
    brokerunits_str,
    cumulative_minute_str,
    hour_label_str,
    job_listen_rotations_str,
    moment_budunit_str,
    moment_paybook_str,
    moment_timeline_hour_str,
    moment_timeline_month_str,
    moment_timeline_weekday_str,
    moment_timeoffi_str,
    momentunit_str,
    month_label_str,
    paybook_str,
    weekday_label_str,
    weekday_order_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert momentunit_str() == "momentunit"
    assert moment_budunit_str() == "moment_budunit"
    assert moment_paybook_str() == "moment_paybook"
    assert moment_timeline_hour_str() == "moment_timeline_hour"
    assert moment_timeline_month_str() == "moment_timeline_month"
    assert moment_timeline_weekday_str() == "moment_timeline_weekday"
    assert moment_timeoffi_str() == "moment_timeoffi"
    assert brokerunits_str() == "brokerunits"
    assert cumulative_minute_str() == "cumulative_minute"
    assert hour_label_str() == "hour_label"
    assert paybook_str() == "paybook"
    assert month_label_str() == "month_label"
    assert job_listen_rotations_str() == "job_listen_rotations"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
