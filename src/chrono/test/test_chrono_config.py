from src.bud.group import awardlink_shop
from src.bud.reason_idea import reasonunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.chrono.examples.chrono_examples import get_creg_config
from src.chrono.chrono import (
    day_length,
    week_length,
    time_str,
    year_str,
    get_year_road,
    stan_c400_leap_ideaunits,
    stan_c400_clean_ideaunits,
    stan_c100_ideaunits,
    stan_yr4_leap_ideaunits,
    stan_yr4_clean_ideaunits,
    stan_year_ideaunits,
    day_str,  # "day"
    days_str,  # f"{get_day()}s"
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    year_str,
    hour_str,
    weeks_str,
    week_str,
    hours_config_text,
    weekdays_config_text,
    months_config_text,
    timeline_label_text,
    c400_config_text,
    yr1_jan1_offset_text,
    validate_timeline_config,
)
from copy import deepcopy as copy_deepcopy


def test_is_timeline_config_valid_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not validate_timeline_config({})
    x_creg_config = get_creg_config()

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(hours_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(weekdays_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(months_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(timeline_label_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(c400_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(yr1_jan1_offset_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config[hours_config_text()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config[months_config_text()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(x_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config[weekdays_config_text()] = []
    assert not validate_timeline_config(creg_config)


def test_create_config_ReturnsObj():
    # ESTABLISH
    c400_count = 8
    hours_count = 6
    months_count = 14
    months_length = 25
    timeline_text = "cinqo"
    weekday_strs = ["Airday", "Bioday", "Ceoday", "Dogday", "Ellday"]

    # WHEN

    # THEN

    x_dict = {
        "c400_config": 7,
        "hours_config": [
            ["0-12am", 60],
            ["22-10pm", 1380],
            ["23-11pm", 1440],
        ],
        "months_config": [
            ["mar", 31],
            ["dec", 304],
            ["jan", 334],
            ["feb", 365],
        ],
        "timeline_label": "creg",
        "weekdays_config": [
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
            "Monday",
            "Tuesday",
        ],
        "yr1_jan1_offset": 440640,
    }
    # assert 1 == 2
