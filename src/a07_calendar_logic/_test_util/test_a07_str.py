from src.a07_calendar_logic._test_util.a07_str import (
    c100_str,
    c400_leap_str,
    c400_clean_str,
    c400_number_str,
    day_str,
    hours_config_str,
    months_config_str,
    monthday_distortion_str,
    weekdays_config_str,
    time_str,
    timeline_label_str,
    week_str,
    year_str,
    yr1_jan1_offset_str,
    yr4_leap_str,
    yr4_clean_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert hours_config_str() == "hours_config"
    assert weekdays_config_str() == "weekdays_config"
    assert months_config_str() == "months_config"
    assert monthday_distortion_str() == "monthday_distortion"
    assert timeline_label_str() == "timeline_label"
    assert c400_number_str() == "c400_number"
    assert yr1_jan1_offset_str() == "yr1_jan1_offset"
