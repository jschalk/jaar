from dataclasses import dataclass
from datetime import datetime
from os import getcwd as os_getcwd
from src.a00_data_toolbox.dict_toolbox import get_1_if_None
from src.a00_data_toolbox.file_toolbox import create_path, open_json
from src.a01_term_logic.rope import LabelTerm, RopeTerm, create_rope
from src.a05_plan_logic.plan import (
    PlanUnit,
    all_plans_between,
    plans_calculated_range as calc_range,
    planunit_shop,
)
from src.a06_belief_logic.belief_main import BeliefUnit


class TimeLineLabel(LabelTerm):
    "TimeLineLabel is required for every TimeLineUnit. It is a LabelTerm that must not contain the knot."

    pass


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
    c400_constants_path = create_path("src/a07_timeline_logic", "c400_constants.json")
    c400_dict = open_json(c400_constants_path)
    return C400Constants(
        day_length=c400_dict.get("day_length"),
        c400_leap_length=c400_dict.get("c400_leap_length"),
        c400_clean_length=c400_dict.get("c400_clean_length"),
        c100_length=c400_dict.get("c100_length"),
        yr4_leap_length=c400_dict.get("yr4_leap_length"),
        yr4_clean_length=c400_dict.get("yr4_clean_length"),
        year_length=c400_dict.get("year_length"),
    )


def day_length() -> int:
    return 1440


def stan_c400_leap_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c400_leap_length
    return planunit_shop("c400_leap", denom=x_denom, morph=True)


def stan_c400_clean_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c400_clean_length
    return planunit_shop("c400_clean", denom=x_denom, morph=True)


def stan_c100_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c100_length
    return planunit_shop("c100", denom=x_denom, morph=True)


def stan_yr4_leap_planunit() -> PlanUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return planunit_shop("yr4_leap", denom=x_denom, morph=True)


def stan_yr4_clean_planunit() -> PlanUnit:
    x_denom = get_c400_constants().yr4_clean_length
    return planunit_shop("yr4_clean", denom=x_denom, morph=True)


def stan_year_planunit() -> PlanUnit:
    x_denom = get_c400_constants().year_length
    return planunit_shop("year", denom=x_denom, morph=True)


def stan_day_planunit() -> PlanUnit:
    x_denom = get_c400_constants().day_length
    return planunit_shop("day", denom=x_denom, morph=True)


def stan_days_planunit() -> PlanUnit:
    x_denom = get_c400_constants().day_length
    return planunit_shop("days", denom=x_denom)


def week_length(x_int: int) -> int:
    """Return the length of a week in minutes."""
    return day_length() * x_int


def create_weekday_planunits(x_weekdays: list[str]) -> dict[str, PlanUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_plan = planunit_shop(
            x_weekdays[x_weekday_num],
            gogo_want=x_weekday_num * day_length(),
            stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_plan
    return x_dict


def create_month_planunits(
    x_months_list: list[list[str, int]], monthday_distortion: int
) -> dict[str, PlanUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_addin = monthday_distortion * day_length()
        x_plan = planunit_shop(
            x_month_str, gogo_want=x_gogo, stop_want=x_stop, addin=x_addin
        )
        x_dict[x_month_str] = x_plan
        current_day = x_month_days
    return x_dict


def create_hour_planunits(x_hours_list: list[str]) -> dict[str, PlanUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_plan = planunit_shop(x_hour_str, gogo_want=current_min, stop_want=x_stop)
        x_dict[x_hour_str] = x_plan
        current_min = x_stop
    return x_dict


def create_week_planunits(x_weekdays_list) -> dict[str, PlanUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_str = "week"
    weeks_str = "weeks"
    return {
        week_str: planunit_shop(week_str, denom=x_week_lenth, morph=True),
        weeks_str: planunit_shop(weeks_str, denom=x_week_lenth),
    }


def new_timeline_planunit(timeline_label: TimeLineLabel, c400_number: int) -> PlanUnit:
    timeline_length = c400_number * get_c400_constants().c400_leap_length
    return planunit_shop(timeline_label, begin=0, close=timeline_length)


def get_timeline_rope(moment_label: str, timeline_label: str, knot: str) -> RopeTerm:
    time_rope = create_rope(moment_label, "time", knot)
    return create_rope(time_rope, timeline_label, knot)


def add_newtimeline_planunit(x_beliefunit: BeliefUnit, timeline_config: dict):
    x_plan_label = timeline_config.get("timeline_label")
    x_c400_number = timeline_config.get("c400_number")
    x_months = timeline_config.get("months_config")
    x_mday = timeline_config.get("monthday_distortion")
    x_hours_list = timeline_config.get("hours_config")
    x_weekdays_list = timeline_config.get("weekdays_config")
    x_yr1_jan1_offset = timeline_config.get("yr1_jan1_offset")

    timeline_rope = get_timeline_rope(
        moment_label=x_beliefunit.moment_label,
        timeline_label=x_plan_label,
        knot=x_beliefunit.knot,
    )
    day_rope = x_beliefunit.make_rope(timeline_rope, "day")
    week_rope = x_beliefunit.make_rope(timeline_rope, "week")
    year_rope = get_year_rope(x_beliefunit, timeline_rope)

    add_stan_planunits(x_beliefunit, x_plan_label, x_c400_number)
    add_planunits(x_beliefunit, day_rope, create_hour_planunits(x_hours_list))
    add_planunits(x_beliefunit, timeline_rope, create_week_planunits(x_weekdays_list))
    add_planunits(x_beliefunit, week_rope, create_weekday_planunits(x_weekdays_list))
    add_planunits(x_beliefunit, year_rope, create_month_planunits(x_months, x_mday))
    offset_plan = planunit_shop("yr1_jan1_offset", addin=x_yr1_jan1_offset)
    x_beliefunit.set_plan(offset_plan, timeline_rope)
    return x_beliefunit


def add_planunits(
    x_beliefunit: BeliefUnit,
    parent_rope: RopeTerm,
    config_dict: dict[str, PlanUnit],
):
    for x_time_planunit in config_dict.values():
        x_beliefunit.set_plan(x_time_planunit, parent_rope)


def add_stan_planunits(
    x_beliefunit: BeliefUnit,
    timeline_label: TimeLineLabel,
    timeline_c400_number: int,
):
    time_rope = x_beliefunit.make_l1_rope("time")
    timeline_rope = get_timeline_rope(
        moment_label=x_beliefunit.moment_label,
        timeline_label=timeline_label,
        knot=x_beliefunit.knot,
    )
    c400_leap_rope = x_beliefunit.make_rope(timeline_rope, "c400_leap")
    c400_clean_rope = x_beliefunit.make_rope(c400_leap_rope, "c400_clean")
    c100_rope = x_beliefunit.make_rope(c400_clean_rope, "c100")
    yr4_leap_rope = x_beliefunit.make_rope(c100_rope, "yr4_leap")
    yr4_clean_rope = x_beliefunit.make_rope(yr4_leap_rope, "yr4_clean")

    if not x_beliefunit.plan_exists(time_rope):
        x_beliefunit.set_l1_plan(planunit_shop("time"))
    timeline_planunit = new_timeline_planunit(timeline_label, timeline_c400_number)
    x_beliefunit.set_plan(timeline_planunit, time_rope)
    x_beliefunit.set_plan(stan_c400_leap_planunit(), timeline_rope)
    x_beliefunit.set_plan(stan_c400_clean_planunit(), c400_leap_rope)
    x_beliefunit.set_plan(stan_c100_planunit(), c400_clean_rope)
    x_beliefunit.set_plan(stan_yr4_leap_planunit(), c100_rope)
    x_beliefunit.set_plan(stan_yr4_clean_planunit(), yr4_leap_rope)
    x_beliefunit.set_plan(stan_year_planunit(), yr4_clean_rope)
    x_beliefunit.set_plan(stan_day_planunit(), timeline_rope)
    x_beliefunit.set_plan(stan_days_planunit(), timeline_rope)


def get_c400_clean_rope(
    x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm
) -> RopeTerm:
    c400_leap_rope = x_beliefunit.make_rope(time_range_root_rope, "c400_leap")
    return x_beliefunit.make_rope(c400_leap_rope, "c400_clean")


def get_c100_rope(x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    c400_clean_rope = get_c400_clean_rope(x_beliefunit, time_range_root_rope)
    return x_beliefunit.make_rope(c400_clean_rope, "c100")


def get_yr4_clean_rope(
    x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm
) -> RopeTerm:
    c100_rope = get_c100_rope(x_beliefunit, time_range_root_rope)
    yr4_leap_rope = x_beliefunit.make_rope(c100_rope, "yr4_leap")
    return x_beliefunit.make_rope(yr4_leap_rope, "yr4_clean")


def get_year_rope(x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    yr4_clean_rope = get_yr4_clean_rope(x_beliefunit, time_range_root_rope)
    return x_beliefunit.make_rope(yr4_clean_rope, "year")


def get_week_rope(x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    return x_beliefunit.make_rope(time_range_root_rope, "week")


def get_day_rope(x_beliefunit: BeliefUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    return x_beliefunit.make_rope(time_range_root_rope, "day")


def validate_timeline_config(config_dict: dict) -> bool:
    config_elements = [
        "hours_config",
        "weekdays_config",
        "months_config",
        "monthday_distortion",
        "timeline_label",
        "c400_number",
        "yr1_jan1_offset",
    ]
    for config_key in config_elements:
        config_element = config_dict.get(config_key)
        len_elements = {
            "hours_config",
            "weekdays_config",
            "months_config",
        }
        if config_element is None:
            return False
        elif config_key in len_elements and len(config_element) == 0:
            return False
        elif config_key in "weekdays_config":
            if _duplicate_exists(config_element):
                return False
        elif config_key in {"months_config", "hours_config"}:
            str_list = [x_config[0] for x_config in config_element]
            if _duplicate_exists(str_list):
                return False
    return True


def _duplicate_exists(config_element: list) -> bool:
    return len(config_element) != len(set(config_element))


def get_default_hours_config() -> list[list[str, int]]:
    return [
        ["12am", 60],
        ["1am", 120],
        ["2am", 180],
        ["3am", 240],
        ["4am", 300],
        ["5am", 360],
        ["6am", 420],
        ["7am", 480],
        ["8am", 540],
        ["9am", 600],
        ["10am", 660],
        ["11am", 720],
        ["12pm", 780],
        ["1pm", 840],
        ["2pm", 900],
        ["3pm", 960],
        ["4pm", 1020],
        ["5pm", 1080],
        ["6pm", 1140],
        ["7pm", 1200],
        ["8pm", 1260],
        ["9pm", 1320],
        ["10pm", 1380],
        ["11pm", 1440],
    ]


def get_default_months_config() -> list[list[str, int]]:
    return [
        ["March", 31],
        ["April", 61],
        ["May", 92],
        ["June", 122],
        ["July", 153],
        ["August", 184],
        ["September", 214],
        ["October", 245],
        ["November", 275],
        ["December", 306],
        ["January", 337],
        ["February", 365],
    ]


def get_default_weekdays_config() -> list[list[str, int]]:
    return [
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
    ]


def timeline_config_shop(
    timeline_label: TimeLineLabel = None,
    c400_number: int = None,
    hour_length: int = None,
    month_length: int = None,
    weekday_list: list[str] = None,
    months_list: list[str] = None,
    monthday_distortion: int = None,
    yr1_jan1_offset: int = None,
) -> dict:
    if timeline_label is None:
        timeline_label = "creg"
    if c400_number is None:
        c400_number = 7
    if yr1_jan1_offset is None:
        yr1_jan1_offset = 440640

    if hour_length:
        hours_count = round(1440 / hour_length)
        hours_range = range(hours_count)
        hour_config = [_hour_config(x, hours_count, hour_length) for x in hours_range]
    else:
        hour_config = get_default_hours_config()
    if not weekday_list:
        weekday_list = get_default_weekdays_config()
    if months_list:
        months_range = range(len(months_list))
        month_config = [
            _month_config(x, months_list, month_length) for x in months_range
        ]
    else:
        month_config = get_default_months_config()
    return {
        "hours_config": hour_config,
        "weekdays_config": weekday_list,
        "months_config": month_config,
        "timeline_label": timeline_label,
        "c400_number": c400_number,
        "monthday_distortion": get_1_if_None(monthday_distortion),
        "yr1_jan1_offset": yr1_jan1_offset,
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
    x_belief: BeliefUnit, timeline_rope: RopeTerm, x_datetime: datetime
) -> int:
    offset_rope = x_belief.make_rope(timeline_rope, "yr1_jan1_offset")
    offset_plan = x_belief.get_plan_obj(offset_rope)
    offset_addin = offset_plan.addin
    return get_min_from_dt_offset(x_datetime, offset_addin)


def get_timeline_min_difference(timeline_config0: dict, timeline_config1: dict) -> int:
    offset_x0 = timeline_config0.get("yr1_jan1_offset")
    offset_x1 = timeline_config1.get("yr1_jan1_offset")
    return offset_x0 - offset_x1


class TimeLinePoint(int):
    pass


@dataclass
class BeliefTimelinePoint:
    """Given belief, timeline_rope, and TimelinePoint, returns time technology attrs
    _c400_number: count of 400 year cycles
    _c100_count: count of 100 year cycles after _c400_number years removed
    _hour
    _minute
    _monthday
    _month
    _yr4_count: 4 year cycles after _c100_count, _c100 years removed
    _year_count:  1 year after _c100_count, _c100_count, _yr4_count years removed
    _year_num: calculated year from c400, c100, yr4, year_count
    _weekday
    _timeline_plan PlanUnit
    readable time blurb from BeliefUnit, time_range_root_rope, and minute integer."""

    x_beliefunit: BeliefUnit = None
    time_range_root_rope: RopeTerm = None
    x_min: TimeLinePoint = None
    # calculated fields
    _timeline_plan: PlanUnit = None
    _weekday: str = None
    _monthday: str = None
    _month: str = None
    _hour: str = None
    _minute: str = None
    _c400_number: str = None
    _c100_count: str = None
    _yr4_count: str = None
    _year_count: str = None
    _year_num: str = None

    def _set_timeline_plan(self):
        self._timeline_plan = self.x_beliefunit.get_plan_obj(self.time_range_root_rope)

    def _set_weekday(self):
        week_rope = get_week_rope(self.x_beliefunit, self.time_range_root_rope)
        week_plan = self.x_beliefunit.get_plan_obj(week_rope)
        x_plan_list = [self._timeline_plan, week_plan]
        reason_lower_rangeunit = calc_range(x_plan_list, self.x_min, self.x_min)
        reason_lower_weekday_dict = week_plan.get_kids_in_range(
            reason_lower_rangeunit.gogo
        )
        for x_weekday in reason_lower_weekday_dict.keys():
            self._weekday = x_weekday

    def _set_month(self):
        year_rope = get_year_rope(self.x_beliefunit, self.time_range_root_rope)
        year_plan = self.x_beliefunit.get_plan_obj(year_rope)
        x_plan_dict = self.x_beliefunit._plan_dict
        plan_list = all_plans_between(
            x_plan_dict,
            self.time_range_root_rope,
            year_rope,
            knot=self.x_beliefunit.knot,
        )
        reason_lower_rangeunit = calc_range(plan_list, self.x_min, self.x_min)
        gogo_month_dict = year_plan.get_kids_in_range(reason_lower_rangeunit.gogo)
        month_plan = None
        for x_monthname, month_plan in gogo_month_dict.items():
            self._month = x_monthname
            month_plan = month_plan

        self._monthday = (
            reason_lower_rangeunit.gogo - month_plan.gogo_calc + month_plan.addin
        )
        self._monthday = self._monthday // 1440

    def _set_hour(self):
        day_rope = get_day_rope(self.x_beliefunit, self.time_range_root_rope)
        day_plan = self.x_beliefunit.get_plan_obj(day_rope)
        x_plan_list = [self._timeline_plan, day_plan]
        rangeunit = calc_range(x_plan_list, self.x_min, self.x_min)
        hour_dict = day_plan.get_kids_in_range(rangeunit.gogo)
        for x_hour, hour_plan in hour_dict.items():
            self._hour = x_hour
            hour_plan = hour_plan

        self._minute = rangeunit.gogo - hour_plan.gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        x_time_rope = self.time_range_root_rope
        x_plan_dict = self.x_beliefunit._plan_dict
        # count 400 year blocks
        self._c400_number = self.x_min // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_clean_rope = get_c400_clean_rope(self.x_beliefunit, x_time_rope)
        c400_clean_plan_list = all_plans_between(
            x_plan_dict, x_time_rope, c400_clean_rope, knot=self.x_beliefunit.knot
        )
        c400_clean_range = calc_range(c400_clean_plan_list, self.x_min, self.x_min)
        self._c100_count = c400_clean_range.gogo // c400_constants.c100_length

        # count 4 year blocks
        c100_rope = get_c100_rope(self.x_beliefunit, x_time_rope)
        c100_plan_list = all_plans_between(
            x_plan_dict, x_time_rope, c100_rope, knot=self.x_beliefunit.knot
        )
        c100_range = calc_range(c100_plan_list, self.x_min, self.x_min)
        self._yr4_count = c100_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_clean_rope = get_yr4_clean_rope(self.x_beliefunit, x_time_rope)
        yr4_clean_plans = all_plans_between(
            x_plan_dict, x_time_rope, yr4_clean_rope, knot=self.x_beliefunit.knot
        )
        yr4_clean_range = calc_range(yr4_clean_plans, self.x_min, self.x_min)
        self._year_count = yr4_clean_range.gogo // c400_constants.year_length

        self._year_num = self._c400_number * 400
        self._year_num += self._c100_count * 100
        self._year_num += self._yr4_count * 4
        self._year_num += self._year_count

    def calc_timeline(self):
        self.x_beliefunit.cash_out()
        self._set_timeline_plan()
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


def belieftimelinepoint_shop(
    x_beliefunit: BeliefUnit, time_range_root_rope: str, x_min: int
):
    return BeliefTimelinePoint(x_beliefunit, time_range_root_rope, x_min=x_min)


def timeline_config_path() -> str:
    "Returns path: a07_timeline_logic/default_timeline_config.json"

    src_dir = create_path(os_getcwd(), "src")
    module_dir = create_path(src_dir, "a07_timeline_logic")
    return create_path(module_dir, "default_timeline_config.json")


def get_default_timeline_config_dict() -> dict:
    return open_json(timeline_config_path())


@dataclass
class TimeLineUnit:
    c400_number: int = None
    hours_config: list[list[str, int]] = None
    months_config: list[list[str, int]] = None
    monthday_distortion: int = None
    timeline_label: TimeLineLabel = None
    weekdays_config: list[str] = None
    yr1_jan1_offset: int = None

    def to_dict(self) -> dict:
        return {
            "c400_number": self.c400_number,
            "hours_config": self.hours_config,
            "months_config": self.months_config,
            "monthday_distortion": self.monthday_distortion,
            "timeline_label": self.timeline_label,
            "weekdays_config": self.weekdays_config,
            "yr1_jan1_offset": self.yr1_jan1_offset,
        }


def timelineunit_shop(timeline_config: dict = None) -> TimeLineUnit:
    default_timeline = get_default_timeline_config_dict()
    if not timeline_config:
        timeline_config = default_timeline
    if timeline_config.get("timeline_label") is None:
        timeline_config["timeline_label"] = default_timeline.get("timeline_label")
    if timeline_config.get("c400_number") is None:
        timeline_config["c400_number"] = default_timeline.get("c400_number")
    if timeline_config.get("monthday_distortion") is None:
        x_monthday_distortion = default_timeline.get("monthday_distortion")
        timeline_config["monthday_distortion"] = x_monthday_distortion
    if timeline_config.get("hours_config") is None:
        timeline_config["hours_config"] = default_timeline.get("hours_config")
    if timeline_config.get("months_config") is None:
        timeline_config["months_config"] = default_timeline.get("months_config")
    if timeline_config.get("weekdays_config") is None:
        timeline_config["weekdays_config"] = default_timeline.get("weekdays_config")
    if timeline_config.get("yr1_jan1_offset") is None:
        timeline_config["yr1_jan1_offset"] = default_timeline.get("yr1_jan1_offset")
    return TimeLineUnit(
        c400_number=timeline_config.get("c400_number"),
        hours_config=timeline_config.get("hours_config"),
        months_config=timeline_config.get("months_config"),
        monthday_distortion=timeline_config.get("monthday_distortion"),
        timeline_label=timeline_config.get("timeline_label"),
        weekdays_config=timeline_config.get("weekdays_config"),
        yr1_jan1_offset=timeline_config.get("yr1_jan1_offset"),
    )


def get_first_weekday_index_of_year(week_length, year: int) -> int:
    # Count leap years between year 0 and year N - 1
    leaps = (year // 4) - (year // 100) + (year // 400)
    total_days = (year - leaps) * 365 + leaps * 366
    return total_days % week_length
