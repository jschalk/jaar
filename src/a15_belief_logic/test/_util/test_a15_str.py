from src.a15_belief_logic.test._util.a15_str import (
    belief_budunit_str,
    belief_paybook_str,
    belief_timeline_hour_str,
    belief_timeline_month_str,
    belief_timeline_weekday_str,
    belief_timeoffi_str,
    beliefunit_str,
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
    assert beliefunit_str() == "beliefunit"
    assert belief_budunit_str() == "belief_budunit"
    assert belief_paybook_str() == "belief_paybook"
    assert belief_timeline_hour_str() == "belief_timeline_hour"
    assert belief_timeline_month_str() == "belief_timeline_month"
    assert belief_timeline_weekday_str() == "belief_timeline_weekday"
    assert belief_timeoffi_str() == "belief_timeoffi"
    assert job_listen_rotations_str() == "job_listen_rotations"
