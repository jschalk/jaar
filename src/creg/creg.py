from src._road.road import RoadUnit
from src.bud.idea import ideaunit_shop, IdeaUnit
from src.bud.bud import BudUnit
from datetime import datetime


def day_length():
    return 1440


def week_length():
    return 10080


def stan_c400_leap_ideaunits() -> dict[str, IdeaUnit]:
    x_text = c400_leap_str()
    return {x_text: ideaunit_shop(x_text, _denom=210379680, _morph=True)}


def stan_c400_clean_ideaunits() -> dict[str, IdeaUnit]:
    x_text = c400_clean_str()
    return {x_text: ideaunit_shop(x_text, _denom=210378240, _morph=True)}


def stan_c100_ideaunits() -> dict[str, IdeaUnit]:
    return {c100_str(): ideaunit_shop(c100_str(), _denom=52594560, _morph=True)}


def stan_yr4_leap_ideaunits() -> dict[str, IdeaUnit]:
    return {yr4_leap_str(): ideaunit_shop(yr4_leap_str(), _denom=2103840, _morph=True)}


def stan_yr4_clean_ideaunits() -> dict[str, IdeaUnit]:
    x_text = yr4_clean_str()
    return {x_text: ideaunit_shop(x_text, _denom=2102400, _morph=True)}


def stan_year_ideaunits() -> dict[str, IdeaUnit]:
    return {year_str(): ideaunit_shop(year_str(), _denom=525600, _morph=True)}


def stan_day_ideaunits() -> dict[str, IdeaUnit]:
    return {
        day_str(): ideaunit_shop(day_str(), _denom=day_length(), _morph=True),
        days_str(): ideaunit_shop(days_str(), _denom=day_length()),
    }


def create_weekday_ideaunits(x_weekdays: list[str]) -> dict[str, IdeaUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_idea = ideaunit_shop(
            x_weekdays[x_weekday_num],
            _gogo_want=x_weekday_num * day_length(),
            _stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_idea
    return x_dict


def c400_leap_str():
    return "c400_leap_str"


def c400_clean_str():
    return "c400_clean_str"


def c100_str():
    return "c100_str"


def yr4_leap_str():
    return "yr4_leap_str"


def yr4_clean_str():
    return "yr4_clean_str"


def year_str():
    return "year_str"


def years_str() -> str:
    return f"{year_str()}"


def cregtime_ideaunit() -> dict[str, IdeaUnit]:
    creg_text = get_cregtime_text()
    return {creg_text: ideaunit_shop(creg_text, _begin=0, _close=210379680 * 7)}


def creg_week_ideaunits() -> dict[str, IdeaUnit]:
    x_text = creg_week_str()
    return {
        x_text: ideaunit_shop(x_text, _denom=week_length(), _morph=True),
        weeks_str(): ideaunit_shop(weeks_str(), _denom=week_length()),
    }


def create_month_ideaunits(x_months_list: list[list[str, int]]) -> dict[str, IdeaUnit]:
    x_dict = {}
    current_day = 0
    for xmonths in x_months_list:
        x_month_list = xmonths
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_idea = ideaunit_shop(x_month_str, _gogo_want=x_gogo, _stop_want=x_stop)
        x_dict[x_month_str] = x_idea
        current_day = x_month_days
    return x_dict


def get_wed():
    return creg_weekday_ideaunits().get("Wednesday")._label


def get_thu():
    return creg_weekday_ideaunits().get("Thursday")._label


def get_fri():
    return creg_weekday_ideaunits().get("Friday")._label


def get_sat():
    return creg_weekday_ideaunits().get("Saturday")._label


def get_sun():
    return creg_weekday_ideaunits().get("Sunday")._label


def get_mon():
    return creg_weekday_ideaunits().get("Monday")._label


def get_tue():
    return creg_weekday_ideaunits().get("Tuesday")._label


def creg_hour_ideaunits() -> dict[int, str]:
    return {
        0: ideaunit_shop("0-12am", _gogo_want=0 * 60, _stop_want=1 * 60),
        1: ideaunit_shop("1-1am", _gogo_want=1 * 60, _stop_want=2 * 60),
        2: ideaunit_shop("2-2am", _gogo_want=2 * 60, _stop_want=3 * 60),
        3: ideaunit_shop("3-3am", _gogo_want=3 * 60, _stop_want=4 * 60),
        4: ideaunit_shop("4-4am", _gogo_want=4 * 60, _stop_want=5 * 60),
        5: ideaunit_shop("5-5am", _gogo_want=5 * 60, _stop_want=6 * 60),
        6: ideaunit_shop("6-6am", _gogo_want=6 * 60, _stop_want=7 * 60),
        7: ideaunit_shop("7-7am", _gogo_want=7 * 60, _stop_want=8 * 60),
        8: ideaunit_shop("8-8am", _gogo_want=8 * 60, _stop_want=9 * 60),
        9: ideaunit_shop("9-9am", _gogo_want=9 * 60, _stop_want=10 * 60),
        10: ideaunit_shop("10-10am", _gogo_want=10 * 60, _stop_want=11 * 60),
        11: ideaunit_shop("11-11am", _gogo_want=11 * 60, _stop_want=12 * 60),
        12: ideaunit_shop("12-12pm", _gogo_want=12 * 60, _stop_want=13 * 60),
        13: ideaunit_shop("13-1pm", _gogo_want=13 * 60, _stop_want=14 * 60),
        14: ideaunit_shop("14-2pm", _gogo_want=14 * 60, _stop_want=15 * 60),
        15: ideaunit_shop("15-3pm", _gogo_want=15 * 60, _stop_want=16 * 60),
        16: ideaunit_shop("16-4pm", _gogo_want=16 * 60, _stop_want=17 * 60),
        17: ideaunit_shop("17-5pm", _gogo_want=17 * 60, _stop_want=18 * 60),
        18: ideaunit_shop("18-6pm", _gogo_want=18 * 60, _stop_want=19 * 60),
        19: ideaunit_shop("19-7pm", _gogo_want=19 * 60, _stop_want=20 * 60),
        20: ideaunit_shop("20-8pm", _gogo_want=20 * 60, _stop_want=21 * 60),
        21: ideaunit_shop("21-9pm", _gogo_want=21 * 60, _stop_want=22 * 60),
        22: ideaunit_shop("22-10pm", _gogo_want=22 * 60, _stop_want=23 * 60),
        23: ideaunit_shop("23-11pm", _gogo_want=23 * 60, _stop_want=24 * 60),
        hour_str(): ideaunit_shop(hour_str(), _denom=60, _morph=True),
    }


def creg_weekday_ideaunits() -> dict[str, IdeaUnit]:
    x_weekdays = [
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
    ]
    return create_weekday_ideaunits(x_weekdays)


def creg_month_ideaunits() -> dict[str, IdeaUnit]:
    x_months_list = [
        ["mar", 31],
        ["apr", 59],
        ["may", 90],
        ["jun", 120],
        ["jul", 151],
        ["aug", 181],
        ["sep", 212],
        ["oct", 243],
        ["nov", 273],
        ["dec", 304],
        ["jan", 334],
        ["feb", 365],
    ]
    return create_month_ideaunits(x_months_list)


def time_str() -> str:
    return "time"


def get_cregtime_text():
    return "cregtime"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def get_hour_label(x_int: int) -> str:
    return creg_hour_ideaunits().get(x_int)._label


def hour_str():
    return "hour"


def creg_week_str():
    return "creg_week"


def weeks_str():
    return f"{creg_week_str()}s"


def add_time_creg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    time_road = x_budunit.make_l1_road(time_str())
    creg_road = x_budunit.make_road(time_road, get_cregtime_text())
    day_road = x_budunit.make_road(creg_road, day_str())
    week_road = x_budunit.make_road(creg_road, creg_week_str())
    c400_leap_road = x_budunit.make_road(creg_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = x_budunit.make_road(yr4_clean_road, year_str())

    x_budunit.set_l1_idea(ideaunit_shop(time_str()))
    # to create a new timeline config file
    #   name of timeline
    # , names of the days of the week
    # , names and number of days of each month
    # , names and number of minutes in each hour
    add_x_ideaunits(x_budunit, time_road, cregtime_ideaunit())
    add_x_ideaunits(x_budunit, creg_road, stan_day_ideaunits())
    add_x_ideaunits(x_budunit, day_road, creg_hour_ideaunits())
    add_x_ideaunits(x_budunit, creg_road, creg_week_ideaunits())
    add_x_ideaunits(x_budunit, week_road, creg_weekday_ideaunits())
    add_x_ideaunits(x_budunit, creg_road, stan_c400_leap_ideaunits())
    add_x_ideaunits(x_budunit, c400_leap_road, stan_c400_clean_ideaunits())
    add_x_ideaunits(x_budunit, c400_clean_road, stan_c100_ideaunits())
    add_x_ideaunits(x_budunit, c100_road, stan_yr4_leap_ideaunits())
    add_x_ideaunits(x_budunit, yr4_leap_road, stan_yr4_clean_ideaunits())
    add_x_ideaunits(x_budunit, yr4_clean_road, stan_year_ideaunits())
    add_x_ideaunits(x_budunit, year_road, creg_month_ideaunits())
    return x_budunit


def add_x_ideaunits(
    x_budunit: BudUnit, parent_road: RoadUnit, config_dict: dict[str, IdeaUnit]
):
    for x_time_ideaunit in config_dict.values():
        x_budunit.set_idea(x_time_ideaunit, parent_road)


# def set_time_facts(
#     x_budunit: BudUnit, open: datetime = None, nigh: datetime = None
# ) -> None:
#     open_minutes = get_time_min_from_dt(dt=open) if open is not None else None
#     nigh_minutes = get_time_min_from_dt(dt=nigh) if nigh is not None else None
#     time_road = x_budunit.make_l1_road("time")
#     minutes_fact = x_budunit.make_road(time_road, "cregtime")
#     x_budunit.set_fact(minutes_fact, minutes_fact, open_minutes, nigh_minutes)


def get_year_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c400_leap_road = x_budunit.make_road(time_range_root_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    return x_budunit.make_road(yr4_clean_road, year_str())


def get_time_min_from_dt(dt: datetime) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + 440640
