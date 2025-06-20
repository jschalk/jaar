from src.a15_vow_logic.test._util.a15_str import (
    brokerunits_str,
    cumulative_minute_str,
    hour_label_str,
    job_listen_rotations_str,
    month_label_str,
    paybook_str,
    vow_budunit_str,
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
    assert cumulative_minute_str() == "cumulative_minute"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
    assert vowunit_str() == "vowunit"
    assert vow_budunit_str() == "vow_budunit"
    assert vow_paybook_str() == "vow_paybook"
    assert vow_timeline_hour_str() == "vow_timeline_hour"
    assert vow_timeline_month_str() == "vow_timeline_month"
    assert vow_timeline_weekday_str() == "vow_timeline_weekday"
    assert vow_timeoffi_str() == "vow_timeoffi"
    assert job_listen_rotations_str() == "job_listen_rotations"
