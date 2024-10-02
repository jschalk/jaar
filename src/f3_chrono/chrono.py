from src.f0_instrument.dict_tool import get_0_if_None, get_dict_from_json
from src.f0_instrument.file import open_file
from src.f1_road.road import RoadUnit
from src.f2_bud.idea import (
    ideaunit_shop,
    IdeaUnit,
    ideas_calculated_range as calc_range,
    all_ideas_between as all_between,
)
from src.f2_bud.bud import BudUnit
from datetime import datetime
from dataclasses import dataclass
from os import getcwd as os_getcwd


def c400_leap_str():
    return "c400_leap"


def c400_clean_str():
    return "c400_clean"


def c100_str():
    return "c100"


def yr4_leap_str():
    return "yr4_leap"


def yr4_clean_str():
    return "yr4_clean"


def year_str():
    return "year"


@dataclass
class C400Constants:
    day_length: int
    c400_leap_length: int
    c400_clean_length: int
    c100_length: int
    yr4_leap_length: int
    yr4_clean_length: int
    year_length: int


def get_c400_constants() -> C400Constants:
    c400_dict = get_dict_from_json(open_file("src/f3_chrono/", "c400_constants.json"))
    return C400Constants(
        day_length=c400_dict.get(f"{day_str()}_length"),
        c400_leap_length=c400_dict.get(f"{c400_leap_str()}_length"),
        c400_clean_length=c400_dict.get(f"{c400_clean_str()}_length"),
        c100_length=c400_dict.get(f"{c100_str()}_length"),
        yr4_leap_length=c400_dict.get(f"{yr4_leap_str()}_length"),
        yr4_clean_length=c400_dict.get(f"{yr4_clean_str()}_length"),
        year_length=c400_dict.get(f"{year_str()}_length"),
    )


def day_length() -> int:
    return 1440


def stan_c400_leap_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().c400_leap_length
    return ideaunit_shop(c400_leap_str(), denom=x_denom, morph=True)


def stan_c400_clean_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().c400_clean_length
    return ideaunit_shop(c400_clean_str(), denom=x_denom, morph=True)


def stan_c100_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().c100_length
    return ideaunit_shop(c100_str(), denom=x_denom, morph=True)


def stan_yr4_leap_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return ideaunit_shop(yr4_leap_str(), denom=x_denom, morph=True)


def stan_yr4_clean_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().yr4_clean_length
    return ideaunit_shop(yr4_clean_str(), denom=x_denom, morph=True)


def stan_year_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().year_length
    return ideaunit_shop(year_str(), denom=x_denom, morph=True)


def stan_day_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().day_length
    return ideaunit_shop(day_str(), denom=x_denom, morph=True)


def stan_days_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().day_length
    return ideaunit_shop(days_str(), denom=x_denom)


def _get_morph_idea(x_str: str, x_denom: int) -> IdeaUnit:
    return ideaunit_shop(x_str, denom=x_denom, morph=True)


def week_length(x_int: int) -> int:
    return day_length() * x_int


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


def create_weekday_ideaunits(x_weekdays: list[str]) -> dict[str, IdeaUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_idea = ideaunit_shop(
            x_weekdays[x_weekday_num],
            gogo_want=x_weekday_num * day_length(),
            stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_idea
    return x_dict


def create_month_ideaunits(
    x_months_list: list[list[str, int]], monthday_distortion: int
) -> dict[str, IdeaUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_addin = monthday_distortion * day_length()
        x_idea = ideaunit_shop(
            x_month_str, gogo_want=x_gogo, stop_want=x_stop, addin=x_addin
        )
        x_dict[x_month_str] = x_idea
        current_day = x_month_days
    return x_dict


def create_hour_ideaunits(x_hours_list: list[str]) -> dict[str, IdeaUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_idea = ideaunit_shop(x_hour_str, gogo_want=current_min, stop_want=x_stop)
        x_dict[x_hour_str] = x_idea
        current_min = x_stop
    return x_dict


def create_week_ideaunits(x_weekdays_list) -> dict[str, IdeaUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_str = "week"
    weeks_str = f"{week_str}s"
    return {
        week_str: ideaunit_shop(week_str, denom=x_week_lenth, morph=True),
        weeks_str: ideaunit_shop(weeks_str, denom=x_week_lenth),
    }


def new_timeline_ideaunit(timeline_label: str, c400_count: int) -> IdeaUnit:
    timeline_length = c400_count * get_c400_constants().c400_leap_length
    return ideaunit_shop(timeline_label, begin=0, close=timeline_length)


def add_newtimeline_ideaunit(x_budunit: BudUnit, timeline_config: dict):
    x_label = timeline_config.get(timeline_label_str())
    x_c400_count = timeline_config.get(c400_config_str())
    x_months = timeline_config.get(months_config_str())
    x_mday = timeline_config.get(monthday_distortion_str())
    x_hours_list = timeline_config.get(hours_config_str())
    x_wkdays_list = timeline_config.get(weekdays_config_str())
    x_yr1_jan1_offset = timeline_config.get(yr1_jan1_offset_str())

    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, x_label)
    day_road = x_budunit.make_road(new_road, day_str())
    week_road = x_budunit.make_road(new_road, week_str())
    year_road = get_year_road(x_budunit, new_road)

    add_stan_ideaunits(x_budunit, time_road, x_label, x_c400_count)
    add_ideaunits(x_budunit, day_road, create_hour_ideaunits(x_hours_list))
    add_ideaunits(x_budunit, new_road, create_week_ideaunits(x_wkdays_list))
    add_ideaunits(x_budunit, week_road, create_weekday_ideaunits(x_wkdays_list))
    add_ideaunits(x_budunit, year_road, create_month_ideaunits(x_months, x_mday))
    offset_idea = ideaunit_shop(yr1_jan1_offset_str(), addin=x_yr1_jan1_offset)
    x_budunit.set_idea(offset_idea, new_road)
    return x_budunit


def add_ideaunits(
    x_budunit: BudUnit, parent_road: RoadUnit, config_dict: dict[str, IdeaUnit]
):
    for x_time_ideaunit in config_dict.values():
        x_budunit.set_idea(x_time_ideaunit, parent_road)


def add_stan_ideaunits(
    x_budunit: BudUnit,
    time_road: RoadUnit,
    timeline_label: str,
    timeline_c400_count: int,
):
    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, timeline_label)
    c400_leap_road = x_budunit.make_road(new_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())

    if not x_budunit.idea_exists(time_road):
        x_budunit.set_l1_idea(ideaunit_shop(time_str()))
    timeline_ideaunit = new_timeline_ideaunit(timeline_label, timeline_c400_count)
    x_budunit.set_idea(timeline_ideaunit, time_road)
    x_budunit.set_idea(stan_c400_leap_ideaunit(), new_road)
    x_budunit.set_idea(stan_c400_clean_ideaunit(), c400_leap_road)
    x_budunit.set_idea(stan_c100_ideaunit(), c400_clean_road)
    x_budunit.set_idea(stan_yr4_leap_ideaunit(), c100_road)
    x_budunit.set_idea(stan_yr4_clean_ideaunit(), yr4_leap_road)
    x_budunit.set_idea(stan_year_ideaunit(), yr4_clean_road)
    x_budunit.set_idea(stan_day_ideaunit(), new_road)
    x_budunit.set_idea(stan_days_ideaunit(), new_road)


def get_c400_clean_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c400_leap_road = x_budunit.make_road(time_range_root_road, c400_leap_str())
    return x_budunit.make_road(c400_leap_road, c400_clean_str())


def get_c100_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c400_clean_road = get_c400_clean_road(x_budunit, time_range_root_road)
    return x_budunit.make_road(c400_clean_road, c100_str())


def get_yr4_clean_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c100_road = get_c100_road(x_budunit, time_range_root_road)
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    return x_budunit.make_road(yr4_leap_road, yr4_clean_str())


def get_year_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    yr4_clean_road = get_yr4_clean_road(x_budunit, time_range_root_road)
    return x_budunit.make_road(yr4_clean_road, year_str())


def get_week_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    return x_budunit.make_road(time_range_root_road, week_str())


def get_day_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    return x_budunit.make_road(time_range_root_road, day_str())


def hours_config_str() -> str:
    return "hours_config"


def weekdays_config_str() -> str:
    return "weekdays_config"


def months_config_str() -> str:
    return "months_config"


def monthday_distortion_str() -> str:
    return "monthday_distortion"


def timeline_label_str() -> str:
    return "timeline_label"


def c400_config_str() -> str:
    return "c400_config"


def yr1_jan1_offset_str() -> str:
    return "yr1_jan1_offset"


def validate_timeline_config(config_dict: dict) -> bool:
    config_elements = [
        hours_config_str(),
        weekdays_config_str(),
        months_config_str(),
        monthday_distortion_str(),
        timeline_label_str(),
        c400_config_str(),
        yr1_jan1_offset_str(),
    ]
    for config_key in config_elements:
        config_element = config_dict.get(config_key)
        len_elements = {
            hours_config_str(),
            weekdays_config_str(),
            months_config_str(),
        }
        if config_element is None:
            return False
        elif config_key in len_elements and len(config_element) == 0:
            return False
        elif config_key in {weekdays_config_str()}:
            if _duplicate_exists(config_element):
                return False
        elif config_key in {months_config_str(), hours_config_str()}:
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
    monthday_distortion: int = None,
    yr1_jan1_offset: int = None,
) -> dict:
    months_range = range(len(months_list))
    month_config = [_month_config(x, months_list, month_length) for x in months_range]
    hours_count = round(1440 / hour_length)
    hours_range = range(hours_count)
    hour_config = [_hour_config(x, hours_count, hour_length) for x in hours_range]
    return {
        hours_config_str(): hour_config,
        weekdays_config_str(): weekday_list,
        months_config_str(): month_config,
        timeline_label_str(): timeline_label,
        c400_config_str(): c400_count,
        monthday_distortion_str(): get_0_if_None(monthday_distortion),
        yr1_jan1_offset_str(): get_0_if_None(yr1_jan1_offset),
    }


def _month_config(month_num, months_list, month_length) -> list[str, int]:
    stop_minute = (month_num + 1) * month_length
    is_last_month = month_num == len(months_list) - 1
    return [months_list[month_num], (365 if is_last_month else stop_minute)]


def _hour_config(hour_num, hours_count, hour_length) -> list[str, int]:
    hour_str = f"{hour_num}hr"
    hour_stop = 1440 if hour_num == hours_count - 1 else (hour_num + 1) * hour_length
    return [hour_str, hour_stop]


def get_min_from_dt_offset(dt: datetime, yr1_jan1_offset: int) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + yr1_jan1_offset


def get_min_from_dt(
    x_bud: BudUnit, timeline_road: RoadUnit, x_datetime: datetime
) -> int:
    offset_road = x_bud.make_road(timeline_road, yr1_jan1_offset_str())
    offset_idea = x_bud.get_idea_obj(offset_road)
    offset_amount = offset_idea.addin
    return get_min_from_dt_offset(x_datetime, offset_amount)


def get_timeline_min_difference(timeline_config0: dict, timeline_config1: dict) -> int:
    offset_x0 = timeline_config0.get(yr1_jan1_offset_str())
    offset_x1 = timeline_config1.get(yr1_jan1_offset_str())
    return offset_x0 - offset_x1


@dataclass
class ChronoUnit:
    x_budunit: BudUnit = None
    time_range_root_road: RoadUnit = None
    x_min: int = None
    # calculated fields
    _timeline_idea: IdeaUnit = None
    _weekday: str = None
    _monthday: str = None
    _month: str = None
    _hour: str = None
    _minute: str = None
    _c400_count: str = None
    _c100_count: str = None
    _yr4_count: str = None
    _year_count: str = None
    _year_num: str = None

    def _set_timeline_idea(self):
        self._timeline_idea = self.x_budunit.get_idea_obj(self.time_range_root_road)

    def _set_weekday(self):
        week_road = get_week_road(self.x_budunit, self.time_range_root_road)
        week_idea = self.x_budunit.get_idea_obj(week_road)
        x_idea_list = [self._timeline_idea, week_idea]
        open_rangeunit = calc_range(x_idea_list, self.x_min, self.x_min)
        open_weekday_dict = week_idea.get_kids_in_range(open_rangeunit.gogo)
        for x_weekday in open_weekday_dict.keys():
            self._weekday = x_weekday

    def _set_month(self):
        year_road = get_year_road(self.x_budunit, self.time_range_root_road)
        year_idea = self.x_budunit.get_idea_obj(year_road)
        x_idea_dict = self.x_budunit._idea_dict
        idea_list = all_between(x_idea_dict, self.time_range_root_road, year_road)
        open_rangeunit = calc_range(idea_list, self.x_min, self.x_min)
        gogo_month_dict = year_idea.get_kids_in_range(open_rangeunit.gogo)
        month_idea = None
        for x_monthname, month_idea in gogo_month_dict.items():
            self._month = x_monthname
            month_idea = month_idea

        self._monthday = open_rangeunit.gogo - month_idea._gogo_calc + month_idea.addin
        self._monthday = self._monthday // 1440

    def _set_hour(self):
        day_road = get_day_road(self.x_budunit, self.time_range_root_road)
        day_idea = self.x_budunit.get_idea_obj(day_road)
        x_idea_list = [self._timeline_idea, day_idea]
        rangeunit = calc_range(x_idea_list, self.x_min, self.x_min)
        hour_dict = day_idea.get_kids_in_range(rangeunit.gogo)
        for x_hour, hour_idea in hour_dict.items():
            self._hour = x_hour
            hour_idea = hour_idea

        self._minute = rangeunit.gogo - hour_idea._gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        x_time_road = self.time_range_root_road
        x_idea_dict = self.x_budunit._idea_dict
        # count 400 year blocks
        self._c400_count = self.x_min // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_clean_road = get_c400_clean_road(self.x_budunit, x_time_road)
        c400_clean_idea_list = all_between(x_idea_dict, x_time_road, c400_clean_road)
        c400_clean_range = calc_range(c400_clean_idea_list, self.x_min, self.x_min)
        self._c100_count = c400_clean_range.gogo // c400_constants.c100_length

        # count 4 year blocks
        c100_road = get_c100_road(self.x_budunit, x_time_road)
        c100_idea_list = all_between(x_idea_dict, x_time_road, c100_road)
        c100_range = calc_range(c100_idea_list, self.x_min, self.x_min)
        self._yr4_count = c100_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_clean_road = get_yr4_clean_road(self.x_budunit, x_time_road)
        yr4_clean_ideas = all_between(x_idea_dict, x_time_road, yr4_clean_road)
        yr4_clean_range = calc_range(yr4_clean_ideas, self.x_min, self.x_min)
        self._year_count = yr4_clean_range.gogo // c400_constants.year_length

        self._year_num = self._c400_count * 400
        self._year_num += self._c100_count * 100
        self._year_num += self._yr4_count * 4
        self._year_num += self._year_count

    def calc_timeline(self):
        self.x_budunit.settle_bud()
        self._set_timeline_idea()
        self._set_weekday()
        self._set_month()
        self._set_hour()
        self._set_year()

    def get_blurb(self) -> str:
        x_str = f"{self._hour}"
        x_str += f":{self._minute}"
        x_str += f", {self._weekday}"
        x_str += f", {self._monthday}"
        x_str += f" {self._month}"
        x_str += f", {self._year_num}"
        return x_str


def chronounit_shop(x_budunit: BudUnit, time_range_root_road: str, x_min: int):
    return ChronoUnit(x_budunit, time_range_root_road, x_min=x_min)


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f3_chrono"


def get_default_timeline_config_file_name() -> str:
    return "default_timeline_config.json"


def get_default_timeline_config_dict() -> dict:
    x_filename = get_default_timeline_config_file_name()
    return get_dict_from_json(open_file(config_file_dir(), x_filename))


@dataclass
class TimeLineUnit:
    c400_config: int = None
    hours_config: list[list[str, int]] = None
    months_config: list[list[str, int]] = None
    monthday_distortion: int = None
    timeline_label: str = None
    weekdays_config: list[str] = None
    yr1_jan1_offset: int = None

    def get_dict(self) -> dict:
        return {
            "c400_config": self.c400_config,
            "hours_config": self.hours_config,
            "months_config": self.months_config,
            "monthday_distortion": self.monthday_distortion,
            "timeline_label": self.timeline_label,
            "weekdays_config": self.weekdays_config,
            "yr1_jan1_offset": self.yr1_jan1_offset,
        }


def timelineunit_shop(timeline_config: dict = None) -> TimeLineUnit:
    if timeline_config is None:
        timeline_config = get_default_timeline_config_dict()
    return TimeLineUnit(
        c400_config=timeline_config.get(c400_config_str()),
        hours_config=timeline_config.get(hours_config_str()),
        months_config=timeline_config.get(months_config_str()),
        monthday_distortion=timeline_config.get(monthday_distortion_str()),
        timeline_label=timeline_config.get(timeline_label_str()),
        weekdays_config=timeline_config.get(weekdays_config_str()),
        yr1_jan1_offset=timeline_config.get(yr1_jan1_offset_str()),
    )
