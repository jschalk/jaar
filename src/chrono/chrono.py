from src._instrument.python_tool import get_0_if_None, get_dict_from_json
from src._instrument.file import open_file
from src._road.road import RoadUnit, RoadNode
from src.bud.idea import (
    ideaunit_shop,
    IdeaUnit,
    ideas_calculated_range,
    all_ideas_between,
)
from src.bud.bud import BudUnit
from datetime import datetime
from dataclasses import dataclass


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
    c400_dict = get_dict_from_json(open_file("src/chrono/", "c400_constants.json"))
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
    return ideaunit_shop(c400_leap_str(), _denom=x_denom, _morph=True)


def stan_c400_clean_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().c400_clean_length
    return ideaunit_shop(c400_clean_str(), _denom=x_denom, _morph=True)


def stan_c100_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().c100_length
    return ideaunit_shop(c100_str(), _denom=x_denom, _morph=True)


def stan_yr4_leap_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return ideaunit_shop(yr4_leap_str(), _denom=x_denom, _morph=True)


def stan_yr4_clean_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().yr4_clean_length
    return ideaunit_shop(yr4_clean_str(), _denom=x_denom, _morph=True)


def stan_year_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().year_length
    return ideaunit_shop(year_str(), _denom=x_denom, _morph=True)


def stan_day_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().day_length
    return ideaunit_shop(day_str(), _denom=x_denom, _morph=True)


def stan_days_ideaunit() -> IdeaUnit:
    x_denom = get_c400_constants().day_length
    return ideaunit_shop(days_str(), _denom=x_denom)


def _get_morph_idea(x_text: str, x_denom: int) -> IdeaUnit:
    return ideaunit_shop(x_text, _denom=x_denom, _morph=True)


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


def new_timeline_ideaunit(timeline_label: str, c400_count: int) -> IdeaUnit:
    timeline_length = c400_count * get_c400_constants().c400_leap_length
    return ideaunit_shop(timeline_label, _begin=0, _close=timeline_length)


def add_newtimeline_ideaunit(x_budunit: BudUnit, timeline_config: dict):
    timeline_label = timeline_config.get(timeline_label_text())
    timeline_c400_count = timeline_config.get(c400_config_text())
    timeline_months_list = timeline_config.get(months_config_text())
    timeline_hours_list = timeline_config.get(hours_config_text())
    timeline_wkdays_list = timeline_config.get(weekdays_config_text())

    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, timeline_label)
    day_road = x_budunit.make_road(new_road, day_str())
    week_road = x_budunit.make_road(new_road, week_str())
    year_road = get_year_road(x_budunit, new_road)

    add_stan_ideaunits(x_budunit, time_road, timeline_label, timeline_c400_count)
    add_ideaunits(x_budunit, day_road, create_hour_ideaunits(timeline_hours_list))
    add_ideaunits(x_budunit, new_road, create_week_ideaunits(timeline_wkdays_list))
    add_ideaunits(x_budunit, week_road, create_weekday_ideaunits(timeline_wkdays_list))
    add_ideaunits(x_budunit, year_road, create_month_ideaunits(timeline_months_list))
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


def get_time_min_from_dt(dt: datetime, yr1_jan1_offset: int) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + yr1_jan1_offset


def get_timeline_min_difference(timeline_config0: dict, timeline_config1: dict) -> int:
    offset_x0 = timeline_config0.get(yr1_jan1_offset_text())
    offset_x1 = timeline_config1.get(yr1_jan1_offset_text())
    return offset_x0 - offset_x1


@dataclass
class ChronoPoint:
    timeline_min: int = None
    weekday_label: RoadNode = None
    month_label: RoadNode = None
    monthday_num: int = None
    c400_leap_count: int = None
    c100_count: int = None
    yr4_leap_count: int = None
    yr_count: int = None
    year_num: int = None
    hour_label: RoadNode = None
    minute_num: int = None


def chronopoint_shop(timeline_min: int):
    return ChronoPoint(timeline_min)


@dataclass
class ChronoRange:
    x_budunit: BudUnit = None
    time_range_root_road: RoadUnit = None
    copen: int = None
    cnigh: int = None
    # calculated fields
    _timeline_idea: IdeaUnit = None
    _copen_weekday: str = None
    _cnigh_weekday: str = None
    _copen_monthday: str = None
    _cnigh_monthday: str = None
    _copen_month: str = None
    _cnigh_month: str = None
    _copen_hour: str = None
    _cnigh_hour: str = None
    _copen_minute: str = None
    _cnigh_minute: str = None
    _copen_c400_count: str = None
    _cnigh_c400_count: str = None
    _copen_c100_count: str = None
    _cnigh_c100_count: str = None
    _copen_yr4_count: str = None
    _cnigh_yr4_count: str = None
    _copen_year_count: str = None
    _cnigh_year_count: str = None
    _copen_year_num: str = None
    _cnigh_year_num: str = None

    def _set_timeline_idea(self):
        self._timeline_idea = self.x_budunit.get_idea_obj(self.time_range_root_road)

    def _set_weekday(self):
        week_road = get_week_road(self.x_budunit, self.time_range_root_road)
        week_idea = self.x_budunit.get_idea_obj(week_road)
        x_idea_list = [self._timeline_idea, week_idea]
        open_rangeunit = ideas_calculated_range(x_idea_list, self.copen, self.copen)
        nigh_rangeunit = ideas_calculated_range(x_idea_list, self.cnigh, self.cnigh)
        open_weekday_dict = week_idea.get_kids_in_range(open_rangeunit.gogo)
        nigh_weekday_dict = week_idea.get_kids_in_range(nigh_rangeunit.gogo)
        for x_weekday in open_weekday_dict.keys():
            self._copen_weekday = x_weekday
        for x_weekday in nigh_weekday_dict.keys():
            self._cnigh_weekday = x_weekday

    def _set_month(self):
        year_road = get_year_road(self.x_budunit, self.time_range_root_road)
        year_idea = self.x_budunit.get_idea_obj(year_road)
        x_idea_dict = self.x_budunit._idea_dict
        idea_list = all_ideas_between(x_idea_dict, self.time_range_root_road, year_road)
        open_rangeunit = ideas_calculated_range(idea_list, self.copen, self.copen)
        nigh_rangeunit = ideas_calculated_range(idea_list, self.cnigh, self.cnigh)
        gogo_month_dict = year_idea.get_kids_in_range(open_rangeunit.gogo)
        stop_month_dict = year_idea.get_kids_in_range(nigh_rangeunit.gogo)
        copen_month_idea = None
        cnigh_month_idea = None
        print(f"{gogo_month_dict=}")
        for x_monthname, month_idea in gogo_month_dict.items():
            self._copen_month = x_monthname
            copen_month_idea = month_idea
        for x_monthname, month_idea in stop_month_dict.items():
            self._cnigh_month = x_monthname
            cnigh_month_idea = month_idea

        self._copen_monthday = open_rangeunit.gogo - copen_month_idea._gogo_calc
        self._cnigh_monthday = nigh_rangeunit.gogo - cnigh_month_idea._gogo_calc
        self._copen_monthday = self._copen_monthday // 1440
        self._cnigh_monthday = self._cnigh_monthday // 1440

    def _set_hour(self):
        day_road = get_day_road(self.x_budunit, self.time_range_root_road)
        day_idea = self.x_budunit.get_idea_obj(day_road)
        x_idea_list = [self._timeline_idea, day_idea]
        copen_rangeunit = ideas_calculated_range(x_idea_list, self.copen, self.copen)
        cnigh_rangeunit = ideas_calculated_range(x_idea_list, self.cnigh, self.cnigh)
        copen_hour_dict = day_idea.get_kids_in_range(copen_rangeunit.gogo)
        cnigh_hour_dict = day_idea.get_kids_in_range(cnigh_rangeunit.gogo)
        for x_hour, hour_idea in copen_hour_dict.items():
            self._copen_hour = x_hour
            copen_hour_idea = hour_idea
        for x_hour, hour_idea in cnigh_hour_dict.items():
            self._cnigh_hour = x_hour
            cnigh_hour_idea = hour_idea

        self._copen_minute = copen_rangeunit.gogo - copen_hour_idea._gogo_calc
        self._cnigh_minute = cnigh_rangeunit.gogo - cnigh_hour_idea._gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        # count 400 year blocks
        self._copen_c400_count = self.copen // c400_constants.c400_leap_length
        self._cnigh_c400_count = self.cnigh // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_clean_road = get_c400_clean_road(self.x_budunit, self.time_range_root_road)
        c400_clean_idea_list = all_ideas_between(
            self.x_budunit._idea_dict, self.time_range_root_road, c400_clean_road
        )
        c400_clean_o_range = ideas_calculated_range(
            c400_clean_idea_list, self.copen, self.copen
        )
        c400_clean_n_range = ideas_calculated_range(
            c400_clean_idea_list, self.cnigh, self.cnigh
        )
        self._copen_c100_count = c400_clean_o_range.gogo // c400_constants.c100_length
        self._cnigh_c100_count = c400_clean_n_range.gogo // c400_constants.c100_length

        # count 4 year blocks
        c100_road = get_c100_road(self.x_budunit, self.time_range_root_road)
        c100_idea_list = all_ideas_between(
            self.x_budunit._idea_dict, self.time_range_root_road, c100_road
        )
        c100_o_range = ideas_calculated_range(c100_idea_list, self.copen, self.copen)
        c100_n_range = ideas_calculated_range(c100_idea_list, self.cnigh, self.cnigh)
        self._copen_yr4_count = c100_o_range.gogo // c400_constants.yr4_leap_length
        self._cnigh_yr4_count = c100_n_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_clean_road = get_yr4_clean_road(self.x_budunit, self.time_range_root_road)
        yr4_clean_idea_list = all_ideas_between(
            self.x_budunit._idea_dict, self.time_range_root_road, yr4_clean_road
        )
        yr4_clean_o_range = ideas_calculated_range(
            yr4_clean_idea_list, self.copen, self.copen
        )
        yr4_clean_n_range = ideas_calculated_range(
            yr4_clean_idea_list, self.cnigh, self.cnigh
        )
        self._copen_year_count = yr4_clean_o_range.gogo // c400_constants.year_length
        self._cnigh_year_count = yr4_clean_n_range.gogo // c400_constants.year_length

        self._copen_year_num = self._copen_c400_count * 400
        self._cnigh_year_num = self._cnigh_c400_count * 400
        self._copen_year_num += self._copen_c100_count * 100
        self._cnigh_year_num += self._cnigh_c100_count * 100
        self._copen_year_num += self._copen_yr4_count * 4
        self._cnigh_year_num += self._cnigh_yr4_count * 4
        self._copen_year_num += self._copen_year_count
        self._cnigh_year_num += self._cnigh_year_count

    def calc_timeline(self):
        self._set_timeline_idea()
        self._set_weekday()
        self._set_month()
        self._set_hour()
        self._set_year()


def chronorange_shop(
    x_budunit: BudUnit, time_range_root_road: str, copen: int, cnigh: int
):
    return ChronoRange(x_budunit, time_range_root_road, copen=copen, cnigh=cnigh)
