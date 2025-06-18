from src.a07_calendar_logic._util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
    creg_hour_int_label,
    creg_str,
    creg_weekday_conceptunits,
    cregtime_conceptunit,
    display_current_creg_five_min,
    five_str,
    get_creg_config,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_five_config,
    get_five_min_from_dt,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)
from src.a07_calendar_logic.chrono import (
    get_c400_constants,
    get_first_weekday_index_of_year,
    get_min_from_dt,
    get_timeline_min_difference,
    get_year_rope,
)


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario0_creg_timeline_config():
    # ESTABLISH
    weekdays_config = get_creg_config().get("weekdays_config")
    print(f"{weekdays_config=}")
    week_length = len(weekdays_config)

    # WHEN
    x2000_index = get_first_weekday_index_of_year(week_length, 2000)
    x2001_index = get_first_weekday_index_of_year(week_length, 2001)
    x2002_index = get_first_weekday_index_of_year(week_length, 2002)
    x2003_index = get_first_weekday_index_of_year(week_length, 2003)
    x2004_index = get_first_weekday_index_of_year(week_length, 2004)

    # THEN
    print(f"{weekdays_config[x2000_index]=}")
    print(f"{weekdays_config[x2001_index]=}")
    print(f"{weekdays_config[x2002_index]=}")
    print(f"{weekdays_config[x2003_index]=}")
    print(f"{weekdays_config[x2004_index]=}")

    assert weekdays_config[x2000_index] == "Wednesday"
    assert weekdays_config[x2001_index] == "Thursday"
    assert weekdays_config[x2002_index] == "Friday"
    assert weekdays_config[x2003_index] == "Saturday"
    assert weekdays_config[x2004_index] == "Monday"
