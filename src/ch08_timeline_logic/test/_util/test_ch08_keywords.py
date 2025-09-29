from src.ch08_timeline_logic._ref.ch08_keywords import (
    Ch08Keywords,
    TimeLineLabel_str,
    TimeLinePoint_str,
    c100_str,
    c400_clean_str,
    c400_leap_str,
    c400_number_str,
    creg_str,
    cumulative_day_str,
    day_str,
    days_str,
    five_str,
    hour_str,
    hours_config_str,
    monthday_distortion_str,
    months_config_str,
    readable_str,
    time_str,
    timeline_label_str,
    timeline_str,
    week_str,
    weekdays_config_str,
    weeks_str,
    year_str,
    yr1_jan1_offset_str,
    yr4_clean_str,
    yr4_leap_str,
)


def test_Ch08Keywords_AttributeNamesEqualValues():
    """Test that all Ch09Keywords enum member names equal their values."""
    # ESTABLISH / WHEN / THEN

    for member in Ch08Keywords:
        assertion_failure_str = (
            f"Enum member name '{member.name}' does not match value '{member.value}'"
        )
        assert member.name == member.value, assertion_failure_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert TimeLineLabel_str() == "TimeLineLabel"
    assert TimeLinePoint_str() == "TimeLinePoint"
    assert c100_str() == "c100"
    assert c400_leap_str() == "c400_leap"
    assert c400_clean_str() == "c400_clean"
    assert c400_number_str() == "c400_number"
    assert creg_str() == "creg"
    assert cumulative_day_str() == "cumulative_day"
    assert day_str() == "day"
    assert days_str() == "days"
    assert five_str() == "five"
    assert hour_str() == "hour"
    assert hours_config_str() == "hours_config"
    assert monthday_distortion_str() == "monthday_distortion"
    assert months_config_str() == "months_config"
    assert readable_str() == "readable"
    assert time_str() == "time"
    assert timeline_str() == "timeline"
    assert timeline_label_str() == "timeline_label"
    assert week_str() == "week"
    assert weeks_str() == "weeks"
    assert weekdays_config_str() == "weekdays_config"
    assert year_str() == "year"
    assert yr1_jan1_offset_str() == "yr1_jan1_offset"
    assert yr4_leap_str() == "yr4_leap"
    assert yr4_clean_str() == "yr4_clean"
