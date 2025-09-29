from src.ch15_moment_logic._ref.ch15_keywords import (
    Ch15Keywords,
    beliefbudhistorys_str,
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


def test_Ch15Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch15Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert momentunit_str() == "momentunit"
    assert moment_budunit_str() == "moment_budunit"
    assert moment_paybook_str() == "moment_paybook"
    assert moment_timeline_hour_str() == "moment_timeline_hour"
    assert moment_timeline_month_str() == "moment_timeline_month"
    assert moment_timeline_weekday_str() == "moment_timeline_weekday"
    assert moment_timeoffi_str() == "moment_timeoffi"
    assert beliefbudhistorys_str() == "beliefbudhistorys"
    assert cumulative_minute_str() == "cumulative_minute"
    assert hour_label_str() == "hour_label"
    assert paybook_str() == "paybook"
    assert month_label_str() == "month_label"
    assert job_listen_rotations_str() == "job_listen_rotations"
    assert weekday_label_str() == "weekday_label"
    assert weekday_order_str() == "weekday_order"
