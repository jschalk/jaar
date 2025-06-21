from src.a15_bank_logic.test._util.a15_str import (
    bank_budunit_str,
    bank_paybook_str,
    bank_timeline_hour_str,
    bank_timeline_month_str,
    bank_timeline_weekday_str,
    bank_timeoffi_str,
    bankunit_str,
    brokerunits_str,
    cumulative_minute_str,
    hour_label_str,
    job_listen_rotations_str,
    month_label_str,
    paybook_str,
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
    assert bankunit_str() == "bankunit"
    assert bank_budunit_str() == "bank_budunit"
    assert bank_paybook_str() == "bank_paybook"
    assert bank_timeline_hour_str() == "bank_timeline_hour"
    assert bank_timeline_month_str() == "bank_timeline_month"
    assert bank_timeline_weekday_str() == "bank_timeline_weekday"
    assert bank_timeoffi_str() == "bank_timeoffi"
    assert job_listen_rotations_str() == "job_listen_rotations"
