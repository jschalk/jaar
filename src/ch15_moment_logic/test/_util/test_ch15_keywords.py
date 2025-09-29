from src.ch15_moment_logic._ref.ch15_keywords import Ch15Keywords, Ch15Keywords as wx


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
    assert wx.momentunit == "momentunit"
    assert wx.moment_budunit == "moment_budunit"
    assert wx.moment_paybook == "moment_paybook"
    assert wx.moment_timeline_hour == "moment_timeline_hour"
    assert wx.moment_timeline_month == "moment_timeline_month"
    assert wx.moment_timeline_weekday == "moment_timeline_weekday"
    assert wx.moment_timeoffi == "moment_timeoffi"
    assert wx.beliefbudhistorys == "beliefbudhistorys"
    assert wx.cumulative_minute == "cumulative_minute"
    assert wx.hour_label == "hour_label"
    assert wx.paybook == "paybook"
    assert wx.month_label == "month_label"
    assert wx.job_listen_rotations == "job_listen_rotations"
    assert wx.weekday_label == "weekday_label"
    assert wx.weekday_order == "weekday_order"
