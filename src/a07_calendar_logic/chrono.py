from dataclasses import dataclass
from datetime import datetime
from os import getcwd as os_getcwd
from src.a00_data_toolbox.dict_toolbox import get_1_if_None
from src.a00_data_toolbox.file_toolbox import create_path, open_json
from src.a01_term_logic.rope import LabelTerm, RopeTerm
from src.a05_concept_logic.concept import (
    ConceptUnit,
    all_concepts_between as all_between,
    concepts_calculated_range as calc_range,
    conceptunit_shop,
)
from src.a06_plan_logic.plan import PlanUnit


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
    c400_constants_path = create_path("src/a07_calendar_logic", "c400_constants.json")
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


def stan_c400_leap_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().c400_leap_length
    return conceptunit_shop("c400_leap", denom=x_denom, morph=True)


def stan_c400_clean_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().c400_clean_length
    return conceptunit_shop("c400_clean", denom=x_denom, morph=True)


def stan_c100_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().c100_length
    return conceptunit_shop("c100", denom=x_denom, morph=True)


def stan_yr4_leap_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return conceptunit_shop("yr4_leap", denom=x_denom, morph=True)


def stan_yr4_clean_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().yr4_clean_length
    return conceptunit_shop("yr4_clean", denom=x_denom, morph=True)


def stan_year_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().year_length
    return conceptunit_shop("year", denom=x_denom, morph=True)


def stan_day_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().day_length
    return conceptunit_shop("day", denom=x_denom, morph=True)


def stan_days_conceptunit() -> ConceptUnit:
    x_denom = get_c400_constants().day_length
    return conceptunit_shop("days", denom=x_denom)


def _get_morph_concept(x_str: str, x_denom: int) -> ConceptUnit:
    return conceptunit_shop(x_str, denom=x_denom, morph=True)


def week_length(x_int: int) -> int:
    return day_length() * x_int


def create_weekday_conceptunits(x_weekdays: list[str]) -> dict[str, ConceptUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_concept = conceptunit_shop(
            x_weekdays[x_weekday_num],
            gogo_want=x_weekday_num * day_length(),
            stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_concept
    return x_dict


def create_month_conceptunits(
    x_months_list: list[list[str, int]], monthday_distortion: int
) -> dict[str, ConceptUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_addin = monthday_distortion * day_length()
        x_concept = conceptunit_shop(
            x_month_str, gogo_want=x_gogo, stop_want=x_stop, addin=x_addin
        )
        x_dict[x_month_str] = x_concept
        current_day = x_month_days
    return x_dict


def create_hour_conceptunits(x_hours_list: list[str]) -> dict[str, ConceptUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_concept = conceptunit_shop(
            x_hour_str, gogo_want=current_min, stop_want=x_stop
        )
        x_dict[x_hour_str] = x_concept
        current_min = x_stop
    return x_dict


def create_week_conceptunits(x_weekdays_list) -> dict[str, ConceptUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_str = "week"
    weeks_str = "weeks"
    return {
        week_str: conceptunit_shop(week_str, denom=x_week_lenth, morph=True),
        weeks_str: conceptunit_shop(weeks_str, denom=x_week_lenth),
    }


def new_timeline_conceptunit(
    timeline_label: TimeLineLabel, c400_number: int
) -> ConceptUnit:
    timeline_length = c400_number * get_c400_constants().c400_leap_length
    return conceptunit_shop(timeline_label, begin=0, close=timeline_length)


def add_newtimeline_conceptunit(x_planunit: PlanUnit, timeline_config: dict):
    x_concept_label = timeline_config.get("timeline_label")
    x_c400_number = timeline_config.get("c400_number")
    x_months = timeline_config.get("months_config")
    x_mday = timeline_config.get("monthday_distortion")
    x_hours_list = timeline_config.get("hours_config")
    x_wkdays_list = timeline_config.get("weekdays_config")
    x_yr1_jan1_offset = timeline_config.get("yr1_jan1_offset")

    time_rope = x_planunit.make_l1_rope("time")
    new_rope = x_planunit.make_rope(time_rope, x_concept_label)
    day_rope = x_planunit.make_rope(new_rope, "day")
    week_rope = x_planunit.make_rope(new_rope, "week")
    year_rope = get_year_rope(x_planunit, new_rope)

    add_stan_conceptunits(x_planunit, time_rope, x_concept_label, x_c400_number)
    add_conceptunits(x_planunit, day_rope, create_hour_conceptunits(x_hours_list))
    add_conceptunits(x_planunit, new_rope, create_week_conceptunits(x_wkdays_list))
    add_conceptunits(x_planunit, week_rope, create_weekday_conceptunits(x_wkdays_list))
    add_conceptunits(x_planunit, year_rope, create_month_conceptunits(x_months, x_mday))
    offset_concept = conceptunit_shop("yr1_jan1_offset", addin=x_yr1_jan1_offset)
    x_planunit.set_concept(offset_concept, new_rope)
    return x_planunit


def add_conceptunits(
    x_planunit: PlanUnit, parent_rope: RopeTerm, config_dict: dict[str, ConceptUnit]
):
    for x_time_conceptunit in config_dict.values():
        x_planunit.set_concept(x_time_conceptunit, parent_rope)


def add_stan_conceptunits(
    x_planunit: PlanUnit,
    time_rope: RopeTerm,
    timeline_label: TimeLineLabel,
    timeline_c400_number: int,
):
    time_rope = x_planunit.make_l1_rope("time")
    new_rope = x_planunit.make_rope(time_rope, timeline_label)
    c400_leap_rope = x_planunit.make_rope(new_rope, "c400_leap")
    c400_clean_rope = x_planunit.make_rope(c400_leap_rope, "c400_clean")
    c100_rope = x_planunit.make_rope(c400_clean_rope, "c100")
    yr4_leap_rope = x_planunit.make_rope(c100_rope, "yr4_leap")
    yr4_clean_rope = x_planunit.make_rope(yr4_leap_rope, "yr4_clean")

    if not x_planunit.concept_exists(time_rope):
        x_planunit.set_l1_concept(conceptunit_shop("time"))
    timeline_conceptunit = new_timeline_conceptunit(
        timeline_label, timeline_c400_number
    )
    x_planunit.set_concept(timeline_conceptunit, time_rope)
    x_planunit.set_concept(stan_c400_leap_conceptunit(), new_rope)
    x_planunit.set_concept(stan_c400_clean_conceptunit(), c400_leap_rope)
    x_planunit.set_concept(stan_c100_conceptunit(), c400_clean_rope)
    x_planunit.set_concept(stan_yr4_leap_conceptunit(), c100_rope)
    x_planunit.set_concept(stan_yr4_clean_conceptunit(), yr4_leap_rope)
    x_planunit.set_concept(stan_year_conceptunit(), yr4_clean_rope)
    x_planunit.set_concept(stan_day_conceptunit(), new_rope)
    x_planunit.set_concept(stan_days_conceptunit(), new_rope)


def get_c400_clean_rope(
    x_planunit: PlanUnit, time_range_root_rope: RopeTerm
) -> RopeTerm:
    c400_leap_rope = x_planunit.make_rope(time_range_root_rope, "c400_leap")
    return x_planunit.make_rope(c400_leap_rope, "c400_clean")


def get_c100_rope(x_planunit: PlanUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    c400_clean_rope = get_c400_clean_rope(x_planunit, time_range_root_rope)
    return x_planunit.make_rope(c400_clean_rope, "c100")


def get_yr4_clean_rope(
    x_planunit: PlanUnit, time_range_root_rope: RopeTerm
) -> RopeTerm:
    c100_rope = get_c100_rope(x_planunit, time_range_root_rope)
    yr4_leap_rope = x_planunit.make_rope(c100_rope, "yr4_leap")
    return x_planunit.make_rope(yr4_leap_rope, "yr4_clean")


def get_year_rope(x_planunit: PlanUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    yr4_clean_rope = get_yr4_clean_rope(x_planunit, time_range_root_rope)
    return x_planunit.make_rope(yr4_clean_rope, "year")


def get_week_rope(x_planunit: PlanUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    return x_planunit.make_rope(time_range_root_rope, "week")


def get_day_rope(x_planunit: PlanUnit, time_range_root_rope: RopeTerm) -> RopeTerm:
    return x_planunit.make_rope(time_range_root_rope, "day")


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
        ["0-12am", 60],
        ["1-1am", 120],
        ["2-2am", 180],
        ["3-3am", 240],
        ["4-4am", 300],
        ["5-5am", 360],
        ["6-6am", 420],
        ["7-7am", 480],
        ["8-8am", 540],
        ["9-9am", 600],
        ["10-10am", 660],
        ["11-11am", 720],
        ["12-12pm", 780],
        ["13-1pm", 840],
        ["14-2pm", 900],
        ["15-3pm", 960],
        ["16-4pm", 1020],
        ["17-5pm", 1080],
        ["18-6pm", 1140],
        ["19-7pm", 1200],
        ["20-8pm", 1260],
        ["21-9pm", 1320],
        ["22-10pm", 1380],
        ["23-11pm", 1440],
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
    x_plan: PlanUnit, timeline_rope: RopeTerm, x_datetime: datetime
) -> int:
    offset_rope = x_plan.make_rope(timeline_rope, "yr1_jan1_offset")
    offset_concept = x_plan.get_concept_obj(offset_rope)
    offset_amount = offset_concept.addin
    return get_min_from_dt_offset(x_datetime, offset_amount)


def get_timeline_min_difference(timeline_config0: dict, timeline_config1: dict) -> int:
    offset_x0 = timeline_config0.get("yr1_jan1_offset")
    offset_x1 = timeline_config1.get("yr1_jan1_offset")
    return offset_x0 - offset_x1


@dataclass
class ChronoUnit:
    x_planunit: PlanUnit = None
    time_range_root_rope: RopeTerm = None
    x_min: int = None
    # calculated fields
    _timeline_concept: ConceptUnit = None
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

    def _set_timeline_concept(self):
        self._timeline_concept = self.x_planunit.get_concept_obj(
            self.time_range_root_rope
        )

    def _set_weekday(self):
        week_rope = get_week_rope(self.x_planunit, self.time_range_root_rope)
        week_concept = self.x_planunit.get_concept_obj(week_rope)
        x_concept_list = [self._timeline_concept, week_concept]
        popen_rangeunit = calc_range(x_concept_list, self.x_min, self.x_min)
        popen_weekday_dict = week_concept.get_kids_in_range(popen_rangeunit.gogo)
        for x_weekday in popen_weekday_dict.keys():
            self._weekday = x_weekday

    def _set_month(self):
        year_rope = get_year_rope(self.x_planunit, self.time_range_root_rope)
        year_concept = self.x_planunit.get_concept_obj(year_rope)
        x_concept_dict = self.x_planunit._concept_dict
        concept_list = all_between(x_concept_dict, self.time_range_root_rope, year_rope)
        popen_rangeunit = calc_range(concept_list, self.x_min, self.x_min)
        gogo_month_dict = year_concept.get_kids_in_range(popen_rangeunit.gogo)
        month_concept = None
        for x_monthname, month_concept in gogo_month_dict.items():
            self._month = x_monthname
            month_concept = month_concept

        self._monthday = (
            popen_rangeunit.gogo - month_concept._gogo_calc + month_concept.addin
        )
        self._monthday = self._monthday // 1440

    def _set_hour(self):
        day_rope = get_day_rope(self.x_planunit, self.time_range_root_rope)
        day_concept = self.x_planunit.get_concept_obj(day_rope)
        x_concept_list = [self._timeline_concept, day_concept]
        rangeunit = calc_range(x_concept_list, self.x_min, self.x_min)
        hour_dict = day_concept.get_kids_in_range(rangeunit.gogo)
        for x_hour, hour_concept in hour_dict.items():
            self._hour = x_hour
            hour_concept = hour_concept

        self._minute = rangeunit.gogo - hour_concept._gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        x_time_rope = self.time_range_root_rope
        x_concept_dict = self.x_planunit._concept_dict
        # count 400 year blocks
        self._c400_number = self.x_min // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_clean_rope = get_c400_clean_rope(self.x_planunit, x_time_rope)
        c400_clean_concept_list = all_between(
            x_concept_dict, x_time_rope, c400_clean_rope
        )
        c400_clean_range = calc_range(c400_clean_concept_list, self.x_min, self.x_min)
        self._c100_count = c400_clean_range.gogo // c400_constants.c100_length

        # count 4 year blocks
        c100_rope = get_c100_rope(self.x_planunit, x_time_rope)
        c100_concept_list = all_between(x_concept_dict, x_time_rope, c100_rope)
        c100_range = calc_range(c100_concept_list, self.x_min, self.x_min)
        self._yr4_count = c100_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_clean_rope = get_yr4_clean_rope(self.x_planunit, x_time_rope)
        yr4_clean_concepts = all_between(x_concept_dict, x_time_rope, yr4_clean_rope)
        yr4_clean_range = calc_range(yr4_clean_concepts, self.x_min, self.x_min)
        self._year_count = yr4_clean_range.gogo // c400_constants.year_length

        self._year_num = self._c400_number * 400
        self._year_num += self._c100_count * 100
        self._year_num += self._yr4_count * 4
        self._year_num += self._year_count

    def calc_timeline(self):
        self.x_planunit.settle_plan()
        self._set_timeline_concept()
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


def chronounit_shop(x_planunit: PlanUnit, time_range_root_rope: str, x_min: int):
    return ChronoUnit(x_planunit, time_range_root_rope, x_min=x_min)


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a07_calendar_logic")


def get_default_timeline_config_filename() -> str:
    return "default_timeline_config.json"


def get_default_timeline_config_dict() -> dict:
    x_filename = get_default_timeline_config_filename()
    return open_json(config_file_dir(), x_filename)


@dataclass
class TimeLineUnit:
    c400_number: int = None
    hours_config: list[list[str, int]] = None
    months_config: list[list[str, int]] = None
    monthday_distortion: int = None
    timeline_label: TimeLineLabel = None
    weekdays_config: list[str] = None
    yr1_jan1_offset: int = None

    def get_dict(self) -> dict:
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
