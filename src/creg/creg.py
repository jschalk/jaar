from src._road.road import RoadUnit
from src.bud.idea import ideaunit_shop, IdeaUnit
from src.bud.bud import BudUnit
from datetime import datetime
from dataclasses import dataclass


def stan_c400_leap_config() -> dict[str, IdeaUnit]:
    x_text = c400_leap_str()
    return {x_text: ideaunit_shop(x_text, _denom=210379680, _morph=True)}


def stan_c400_clean_config() -> dict[str, IdeaUnit]:
    x_text = c400_clean_str()
    return {x_text: ideaunit_shop(x_text, _denom=210378240, _morph=True)}


def stan_c100_config() -> dict[str, IdeaUnit]:
    return {c100_str(): ideaunit_shop(c100_str(), _denom=52594560, _morph=True)}


def stan_yr4_leap_config() -> dict[str, IdeaUnit]:
    return {yr4_leap_str(): ideaunit_shop(yr4_leap_str(), _denom=2103840, _morph=True)}


def stan_yr4_clean_config() -> dict[str, IdeaUnit]:
    x_text = yr4_clean_str()
    return {x_text: ideaunit_shop(x_text, _denom=2102400, _morph=True)}


def stan_year_config() -> dict[str, IdeaUnit]:
    return {year_str(): ideaunit_shop(year_str(), _denom=525600, _morph=True)}


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


def day_length():
    return 1440


def week_length():
    return 10080


def cregtime_config() -> dict[str, IdeaUnit]:
    creg_text = get_cregtime_text()
    return {creg_text: ideaunit_shop(creg_text, _begin=0, _close=210379680 * 7)}


def creg_day_config() -> dict[str, IdeaUnit]:
    return {
        day_str(): ideaunit_shop(day_str(), _denom=day_length(), _morph=True),
        days_str(): ideaunit_shop(days_str(), _denom=day_length()),
    }


def creg_week_config() -> dict[str, IdeaUnit]:
    return {
        week_str(): ideaunit_shop(week_str(), _denom=week_length(), _morph=True),
        weeks_str(): ideaunit_shop(weeks_str(), _denom=week_length()),
    }


def mar_str() -> str:
    return "mar"


def apr_str() -> str:
    return "apr"


def may_str() -> str:
    return "may"


def jun_str() -> str:
    return "jun"


def jul_str() -> str:
    return "jul"


def aug_str() -> str:
    return "aug"


def sep_str() -> str:
    return "sep"


def oct_str() -> str:
    return "oct"


def nov_str() -> str:
    return "nov"


def dec_str() -> str:
    return "dec"


def jan_str() -> str:
    return "jan"


def feb_str() -> str:
    return "feb"


def creg_month_dict() -> dict[str, IdeaUnit]:
    return {
        mar_str(): ideaunit_shop(mar_str(), _gogo_want=0, _stop_want=44640),
        apr_str(): ideaunit_shop(apr_str(), _gogo_want=44640, _stop_want=84960),
        may_str(): ideaunit_shop(may_str(), _gogo_want=84960, _stop_want=129600),
        jun_str(): ideaunit_shop(jun_str(), _gogo_want=129600, _stop_want=172800),
        jul_str(): ideaunit_shop(jul_str(), _gogo_want=172800, _stop_want=217440),
        aug_str(): ideaunit_shop(aug_str(), _gogo_want=217440, _stop_want=260640),
        sep_str(): ideaunit_shop(sep_str(), _gogo_want=260640, _stop_want=305280),
        oct_str(): ideaunit_shop(oct_str(), _gogo_want=305280, _stop_want=349920),
        nov_str(): ideaunit_shop(nov_str(), _gogo_want=349920, _stop_want=393120),
        dec_str(): ideaunit_shop(dec_str(), _gogo_want=393120, _stop_want=437760),
        jan_str(): ideaunit_shop(jan_str(), _gogo_want=437760, _stop_want=480960),
        feb_str(): ideaunit_shop(feb_str(), _gogo_want=480960, _stop_want=525600),
    }


# def jan_gogo_want():    return creg_month_dict().get(jan_str())._gogo_want
# def feb_gogo_want():    return creg_month_dict().get(feb_str())._gogo_want
# def mar_gogo_want():    return creg_month_dict().get(mar_str())._gogo_want
# def apr_gogo_want():    return creg_month_dict().get(apr_str())._gogo_want
# def may_gogo_want():    return creg_month_dict().get(may_str())._gogo_want
# def jun_gogo_want():    return creg_month_dict().get(jun_str())._gogo_want
# def jul_gogo_want():    return creg_month_dict().get(jul_str())._gogo_want
# def aug_gogo_want():    return creg_month_dict().get(aug_str())._gogo_want
# def sep_gogo_want():    return creg_month_dict().get(sep_str())._gogo_want
# def oct_gogo_want():    return creg_month_dict().get(oct_str())._gogo_want
# def nov_gogo_want():    return creg_month_dict().get(nov_str())._gogo_want
# def dec_gogo_want():    return creg_month_dict().get(dec_str())._gogo_want
# def jan_stop_want():    return creg_month_dict().get(jan_str())._stop_want
# def feb_stop_want():    return creg_month_dict().get(feb_str())._stop_want
# def mar_stop_want():    return creg_month_dict().get(mar_str())._stop_want
# def apr_stop_want():    return creg_month_dict().get(apr_str())._stop_want
# def may_stop_want():    return creg_month_dict().get(may_str())._stop_want
# def jun_stop_want():    return creg_month_dict().get(jun_str())._stop_want
# def jul_stop_want():    return creg_month_dict().get(jul_str())._stop_want
# def aug_stop_want():    return creg_month_dict().get(aug_str())._stop_want
# def sep_stop_want():    return creg_month_dict().get(sep_str())._stop_want
# def oct_stop_want():    return creg_month_dict().get(oct_str())._stop_want
# def nov_stop_want():    return creg_month_dict().get(nov_str())._stop_want
# def dec_stop_want():    return creg_month_dict().get(dec_str())._stop_want
def jan_gogo_want():
    return creg_month_dict().get(jan_str())._gogo_want


def feb_gogo_want():
    return creg_month_dict().get(feb_str())._gogo_want


def mar_gogo_want():
    return creg_month_dict().get(mar_str())._gogo_want


def apr_gogo_want():
    return creg_month_dict().get(apr_str())._gogo_want


def may_gogo_want():
    return creg_month_dict().get(may_str())._gogo_want


def jun_gogo_want():
    return creg_month_dict().get(jun_str())._gogo_want


def jul_gogo_want():
    return creg_month_dict().get(jul_str())._gogo_want


def aug_gogo_want():
    return creg_month_dict().get(aug_str())._gogo_want


def sep_gogo_want():
    return creg_month_dict().get(sep_str())._gogo_want


def oct_gogo_want():
    return creg_month_dict().get(oct_str())._gogo_want


def nov_gogo_want():
    return creg_month_dict().get(nov_str())._gogo_want


def dec_gogo_want():
    return creg_month_dict().get(dec_str())._gogo_want


def jan_stop_want():
    return creg_month_dict().get(jan_str())._stop_want


def feb_stop_want():
    return creg_month_dict().get(feb_str())._stop_want


def mar_stop_want():
    return creg_month_dict().get(mar_str())._stop_want


def apr_stop_want():
    return creg_month_dict().get(apr_str())._stop_want


def may_stop_want():
    return creg_month_dict().get(may_str())._stop_want


def jun_stop_want():
    return creg_month_dict().get(jun_str())._stop_want


def jul_stop_want():
    return creg_month_dict().get(jul_str())._stop_want


def aug_stop_want():
    return creg_month_dict().get(aug_str())._stop_want


def sep_stop_want():
    return creg_month_dict().get(sep_str())._stop_want


def oct_stop_want():
    return creg_month_dict().get(oct_str())._stop_want


def nov_stop_want():
    return creg_month_dict().get(nov_str())._stop_want


def dec_stop_want():
    return creg_month_dict().get(dec_str())._stop_want


def get_wed():
    return creg_weekday_config().get("Wednesday")._label


def get_thu():
    return creg_weekday_config().get("Thursday")._label


def get_fri():
    return creg_weekday_config().get("Friday")._label


def get_sat():
    return creg_weekday_config().get("Saturday")._label


def get_sun():
    return creg_weekday_config().get("Sunday")._label


def get_mon():
    return creg_weekday_config().get("Monday")._label


def get_tue():
    return creg_weekday_config().get("Tuesday")._label


def creg_hour_config() -> dict[int, str]:
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


def week_begin():
    return 0


def week_close():
    return 7 * day_length()


def creg_weekday_config() -> dict[str, IdeaUnit]:
    x_wed = "Wednesday"
    x_thu = "Thursday"
    x_fri = "Friday"
    x_sat = "Saturday"
    x_sun = "Sunday"
    x_mon = "Monday"
    x_tue = "Tuesday"
    day_len = day_length()
    return {
        x_wed: ideaunit_shop(x_wed, _gogo_want=0 * day_len, _stop_want=1 * day_len),
        x_thu: ideaunit_shop(x_thu, _gogo_want=1 * day_len, _stop_want=2 * day_len),
        x_fri: ideaunit_shop(x_fri, _gogo_want=2 * day_len, _stop_want=3 * day_len),
        x_sat: ideaunit_shop(x_sat, _gogo_want=3 * day_len, _stop_want=4 * day_len),
        x_sun: ideaunit_shop(x_sun, _gogo_want=4 * day_len, _stop_want=5 * day_len),
        x_mon: ideaunit_shop(x_mon, _gogo_want=5 * day_len, _stop_want=6 * day_len),
        x_tue: ideaunit_shop(x_tue, _gogo_want=6 * day_len, _stop_want=7 * day_len),
    }


def time_str() -> str:
    return "time"


def get_cregtime_text():
    return "cregtime"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def creg_hour_str(x_int: int) -> str:
    return creg_hour_config().get(x_int)._label


def hour_str():
    return "hour"


def week_str():
    return "week"


def weeks_str():
    return f"{week_str()}s"


def add_time_creg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    time_road = x_budunit.make_l1_road(time_str())
    creg_road = x_budunit.make_road(time_road, get_cregtime_text())
    day_road = x_budunit.make_road(creg_road, day_str())
    week_road = x_budunit.make_road(creg_road, week_str())
    c400_leap_road = x_budunit.make_road(creg_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = x_budunit.make_road(yr4_clean_road, year_str())

    x_budunit.set_l1_idea(ideaunit_shop(time_str()))

    add_x_ideaunits(x_budunit, time_road, cregtime_config())
    add_x_ideaunits(x_budunit, creg_road, creg_day_config())
    add_x_ideaunits(x_budunit, day_road, creg_hour_config())
    add_x_ideaunits(x_budunit, creg_road, creg_week_config())
    add_x_ideaunits(x_budunit, week_road, creg_weekday_config())
    add_x_ideaunits(x_budunit, creg_road, stan_c400_leap_config())
    add_x_ideaunits(x_budunit, c400_leap_road, stan_c400_clean_config())
    add_x_ideaunits(x_budunit, c400_clean_road, stan_c100_config())
    add_x_ideaunits(x_budunit, c100_road, stan_yr4_leap_config())
    add_x_ideaunits(x_budunit, yr4_leap_road, stan_yr4_clean_config())
    add_x_ideaunits(x_budunit, yr4_clean_road, stan_year_config())
    add_x_ideaunits(x_budunit, year_road, creg_month_dict())
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
