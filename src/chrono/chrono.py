from src._instrument.python import get_0_if_None
from src._road.road import RoadUnit
from src.bud.idea import ideaunit_shop, IdeaUnit
from src.bud.bud import BudUnit
from datetime import datetime


def validate_timeline_config(config_dict: dict) -> bool:
    config_elements = [
        hours_config_text(),
        weekdays_config_text(),
        months_config_text(),
        timeline_label_text(),
        c400_config_text(),
        yr1_jan1_offset_text(),
    ]
    for config_key in config_elements:
        config_element = config_dict.get(config_key)
        len_elements = {
            hours_config_text(),
            weekdays_config_text(),
            months_config_text(),
        }
        if config_element is None:
            return False
        elif config_key in len_elements and len(config_element) == 0:
            return False
        elif config_key in {weekdays_config_text()}:
            if _duplicate_exists(config_element):
                return False
        elif config_key in {months_config_text(), hours_config_text()}:
            str_list = [x_config[0] for x_config in config_element]
            if _duplicate_exists(str_list):
                return False
    return True


def _duplicate_exists(config_element: list) -> bool:
    return len(config_element) != len(set(config_element))


def create_timeline_config(
    timeline_label: str,
    c400_count: int,
    hour_length: int,
    month_length: int,
    weekday_list: list[str],
    months_list: list[str],
    yr1_jan1_offset: int = None,
) -> dict:
    months_range = range(len(months_list))
    month_config = [_month_config(x, months_list, month_length) for x in months_range]
    hours_count = round(1440 / hour_length)
    hours_range = range(hours_count)
    hour_config = [_hour_config(x, hours_count, hour_length) for x in hours_range]
    return {
        hours_config_text(): hour_config,
        weekdays_config_text(): weekday_list,
        months_config_text(): month_config,
        timeline_label_text(): timeline_label,
        c400_config_text(): c400_count,
        yr1_jan1_offset_text(): get_0_if_None(yr1_jan1_offset),
    }


def _month_config(month_num, months_list, month_length) -> list[str, int]:
    stop_minute = (month_num + 1) * month_length
    is_last_month = month_num == len(months_list) - 1
    return [months_list[month_num], (365 if is_last_month else stop_minute)]


def _hour_config(hour_num, hours_count, hour_length) -> list[str, int]:
    hour_str = f"{hour_num}hr"
    hour_stop = 1440 if hour_num == hours_count - 1 else (hour_num + 1) * hour_length
    return [hour_str, hour_stop]


def day_length() -> int:
    return 1440


def week_length(x_int: int) -> int:
    return day_length() * x_int


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


def time_str() -> str:
    return "time"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def hour_str():
    return "hour"


def week_str():
    return "week"


def weeks_str():
    return f"{week_str()}s"


def hours_config_text() -> str:
    return "hours_config"


def weekdays_config_text() -> str:
    return "weekdays_config"


def months_config_text() -> str:
    return "months_config"


def timeline_label_text() -> str:
    return "timeline_label"


def c400_config_text() -> str:
    return "c400_config"


def yr1_jan1_offset_text() -> str:
    return "yr1_jan1_offset"


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


def create_month_ideaunits(x_months_list: list[list[str, int]]) -> dict[str, IdeaUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_idea = ideaunit_shop(x_month_str, _gogo_want=x_gogo, _stop_want=x_stop)
        x_dict[x_month_str] = x_idea
        current_day = x_month_days
    return x_dict


def create_hour_ideaunits(x_hours_list: list[str]) -> dict[str, IdeaUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_idea = ideaunit_shop(x_hour_str, _gogo_want=current_min, _stop_want=x_stop)
        x_dict[x_hour_str] = x_idea
        current_min = x_stop
    return x_dict


def create_week_ideaunits(x_weekdays_list) -> dict[str, IdeaUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_text = "week"
    weeks_text = f"{week_text}s"
    return {
        week_text: ideaunit_shop(week_text, _denom=x_week_lenth, _morph=True),
        weeks_text: ideaunit_shop(weeks_text, _denom=x_week_lenth),
    }


def new_timeline_ideaunit(timeline_text: str, c400_count: int) -> dict[str, IdeaUnit]:
    x_text = timeline_text
    return {x_text: ideaunit_shop(x_text, _begin=0, _close=210379680 * c400_count)}


def add_newtimeline_ideaunit(x_budunit: BudUnit, timeline_config: dict):
    timeline_text = timeline_config.get(timeline_label_text())
    timeline_c400_count = timeline_config.get(c400_config_text())
    timeline_weekdays_list = timeline_config.get(weekdays_config_text())
    timeline_months_list = timeline_config.get(months_config_text())
    timeline_hours_list = timeline_config.get(hours_config_text())

    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, timeline_text)
    c400_leap_road = x_budunit.make_road(new_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = x_budunit.make_road(yr4_clean_road, year_str())
    day_road = x_budunit.make_road(new_road, day_str())
    week_road = x_budunit.make_road(new_road, week_str())

    x_weekdays_list = timeline_weekdays_list
    x_budunit.set_l1_idea(ideaunit_shop(time_str()))
    timeline_ideaunit = new_timeline_ideaunit(timeline_text, timeline_c400_count)
    add_x_ideaunits(x_budunit, time_road, timeline_ideaunit)
    add_x_ideaunits(x_budunit, new_road, stan_day_ideaunits())
    add_x_ideaunits(x_budunit, day_road, create_hour_ideaunits(timeline_hours_list))
    add_x_ideaunits(x_budunit, new_road, create_week_ideaunits(timeline_weekdays_list))
    add_x_ideaunits(x_budunit, week_road, create_weekday_ideaunits(x_weekdays_list))
    add_x_ideaunits(x_budunit, new_road, stan_c400_leap_ideaunits())
    add_x_ideaunits(x_budunit, c400_leap_road, stan_c400_clean_ideaunits())
    add_x_ideaunits(x_budunit, c400_clean_road, stan_c100_ideaunits())
    add_x_ideaunits(x_budunit, c100_road, stan_yr4_leap_ideaunits())
    add_x_ideaunits(x_budunit, yr4_leap_road, stan_yr4_clean_ideaunits())
    add_x_ideaunits(x_budunit, yr4_clean_road, stan_year_ideaunits())
    add_x_ideaunits(x_budunit, year_road, create_month_ideaunits(timeline_months_list))
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
#     minutes_fact = x_budunit.make_road(time_road, "something")
#     x_budunit.set_fact(minutes_fact, minutes_fact, open_minutes, nigh_minutes)


def get_year_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c400_leap_road = x_budunit.make_road(time_range_root_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    return x_budunit.make_road(yr4_clean_road, year_str())


def get_time_min_from_dt(dt: datetime, yr1_jan1_offset: int) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + yr1_jan1_offset
