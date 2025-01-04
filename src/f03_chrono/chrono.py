from src.f00_instrument.dict_toolbox import get_1_if_None, get_dict_from_json
from src.f00_instrument.file import open_file, create_path
from src.f01_road.road import RoadUnit, TimeLineIdea
from src.f02_bud.item import (
    itemunit_shop,
    ItemUnit,
    items_calculated_range as calc_range,
    all_items_between as all_between,
)
from src.f02_bud.bud import BudUnit
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
    c400_constants_path = create_path("src/f03_chrono/", "c400_constants.json")
    c400_dict = get_dict_from_json(open_file(c400_constants_path))
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


def stan_c400_leap_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().c400_leap_length
    return itemunit_shop(c400_leap_str(), denom=x_denom, morph=True)


def stan_c400_clean_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().c400_clean_length
    return itemunit_shop(c400_clean_str(), denom=x_denom, morph=True)


def stan_c100_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().c100_length
    return itemunit_shop(c100_str(), denom=x_denom, morph=True)


def stan_yr4_leap_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return itemunit_shop(yr4_leap_str(), denom=x_denom, morph=True)


def stan_yr4_clean_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().yr4_clean_length
    return itemunit_shop(yr4_clean_str(), denom=x_denom, morph=True)


def stan_year_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().year_length
    return itemunit_shop(year_str(), denom=x_denom, morph=True)


def stan_day_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().day_length
    return itemunit_shop(day_str(), denom=x_denom, morph=True)


def stan_days_itemunit() -> ItemUnit:
    x_denom = get_c400_constants().day_length
    return itemunit_shop(days_str(), denom=x_denom)


def _get_morph_item(x_str: str, x_denom: int) -> ItemUnit:
    return itemunit_shop(x_str, denom=x_denom, morph=True)


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


def create_weekday_itemunits(x_weekdays: list[str]) -> dict[str, ItemUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_item = itemunit_shop(
            x_weekdays[x_weekday_num],
            gogo_want=x_weekday_num * day_length(),
            stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_item
    return x_dict


def create_month_itemunits(
    x_months_list: list[list[str, int]], monthday_distortion: int
) -> dict[str, ItemUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_addin = monthday_distortion * day_length()
        x_item = itemunit_shop(
            x_month_str, gogo_want=x_gogo, stop_want=x_stop, addin=x_addin
        )
        x_dict[x_month_str] = x_item
        current_day = x_month_days
    return x_dict


def create_hour_itemunits(x_hours_list: list[str]) -> dict[str, ItemUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_item = itemunit_shop(x_hour_str, gogo_want=current_min, stop_want=x_stop)
        x_dict[x_hour_str] = x_item
        current_min = x_stop
    return x_dict


def create_week_itemunits(x_weekdays_list) -> dict[str, ItemUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_str = "week"
    weeks_str = f"{week_str}s"
    return {
        week_str: itemunit_shop(week_str, denom=x_week_lenth, morph=True),
        weeks_str: itemunit_shop(weeks_str, denom=x_week_lenth),
    }


def new_timeline_itemunit(timeline_idea: TimeLineIdea, c400_count: int) -> ItemUnit:
    timeline_length = c400_count * get_c400_constants().c400_leap_length
    return itemunit_shop(timeline_idea, begin=0, close=timeline_length)


def add_newtimeline_itemunit(x_budunit: BudUnit, timeline_config: dict):
    x_item_title = timeline_config.get(timeline_idea_str())
    x_c400_count = timeline_config.get(c400_number_str())
    x_months = timeline_config.get(months_config_str())
    x_mday = timeline_config.get(monthday_distortion_str())
    x_hours_list = timeline_config.get(hours_config_str())
    x_wkdays_list = timeline_config.get(weekdays_config_str())
    x_yr1_jan1_offset = timeline_config.get(yr1_jan1_offset_str())

    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, x_item_title)
    day_road = x_budunit.make_road(new_road, day_str())
    week_road = x_budunit.make_road(new_road, week_str())
    year_road = get_year_road(x_budunit, new_road)

    add_stan_itemunits(x_budunit, time_road, x_item_title, x_c400_count)
    add_itemunits(x_budunit, day_road, create_hour_itemunits(x_hours_list))
    add_itemunits(x_budunit, new_road, create_week_itemunits(x_wkdays_list))
    add_itemunits(x_budunit, week_road, create_weekday_itemunits(x_wkdays_list))
    add_itemunits(x_budunit, year_road, create_month_itemunits(x_months, x_mday))
    offset_item = itemunit_shop(yr1_jan1_offset_str(), addin=x_yr1_jan1_offset)
    x_budunit.set_item(offset_item, new_road)
    return x_budunit


def add_itemunits(
    x_budunit: BudUnit, parent_road: RoadUnit, config_dict: dict[str, ItemUnit]
):
    for x_time_itemunit in config_dict.values():
        x_budunit.set_item(x_time_itemunit, parent_road)


def add_stan_itemunits(
    x_budunit: BudUnit,
    time_road: RoadUnit,
    timeline_idea: TimeLineIdea,
    timeline_c400_count: int,
):
    time_road = x_budunit.make_l1_road(time_str())
    new_road = x_budunit.make_road(time_road, timeline_idea)
    c400_leap_road = x_budunit.make_road(new_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())

    if not x_budunit.item_exists(time_road):
        x_budunit.set_l1_item(itemunit_shop(time_str()))
    timeline_itemunit = new_timeline_itemunit(timeline_idea, timeline_c400_count)
    x_budunit.set_item(timeline_itemunit, time_road)
    x_budunit.set_item(stan_c400_leap_itemunit(), new_road)
    x_budunit.set_item(stan_c400_clean_itemunit(), c400_leap_road)
    x_budunit.set_item(stan_c100_itemunit(), c400_clean_road)
    x_budunit.set_item(stan_yr4_leap_itemunit(), c100_road)
    x_budunit.set_item(stan_yr4_clean_itemunit(), yr4_leap_road)
    x_budunit.set_item(stan_year_itemunit(), yr4_clean_road)
    x_budunit.set_item(stan_day_itemunit(), new_road)
    x_budunit.set_item(stan_days_itemunit(), new_road)


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


def timeline_idea_str() -> str:
    return "timeline_idea"


def c400_number_str() -> str:
    return "c400_number"


def yr1_jan1_offset_str() -> str:
    return "yr1_jan1_offset"


def validate_timeline_config(config_dict: dict) -> bool:
    config_elements = [
        hours_config_str(),
        weekdays_config_str(),
        months_config_str(),
        monthday_distortion_str(),
        timeline_idea_str(),
        c400_number_str(),
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


def create_timeline_config(
    timeline_idea: TimeLineIdea = None,
    c400_count: int = None,
    hour_length: int = None,
    month_length: int = None,
    weekday_list: list[str] = None,
    months_list: list[str] = None,
    monthday_distortion: int = None,
    yr1_jan1_offset: int = None,
) -> dict:
    if timeline_idea is None:
        timeline_idea = "creg"
    if c400_count is None:
        c400_count = 7
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
        hours_config_str(): hour_config,
        weekdays_config_str(): weekday_list,
        months_config_str(): month_config,
        timeline_idea_str(): timeline_idea,
        c400_number_str(): c400_count,
        monthday_distortion_str(): get_1_if_None(monthday_distortion),
        yr1_jan1_offset_str(): yr1_jan1_offset,
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
    offset_item = x_bud.get_item_obj(offset_road)
    offset_amount = offset_item.addin
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
    _timeline_item: ItemUnit = None
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

    def _set_timeline_item(self):
        self._timeline_item = self.x_budunit.get_item_obj(self.time_range_root_road)

    def _set_weekday(self):
        week_road = get_week_road(self.x_budunit, self.time_range_root_road)
        week_item = self.x_budunit.get_item_obj(week_road)
        x_item_list = [self._timeline_item, week_item]
        open_rangeunit = calc_range(x_item_list, self.x_min, self.x_min)
        open_weekday_dict = week_item.get_kids_in_range(open_rangeunit.gogo)
        for x_weekday in open_weekday_dict.keys():
            self._weekday = x_weekday

    def _set_month(self):
        year_road = get_year_road(self.x_budunit, self.time_range_root_road)
        year_item = self.x_budunit.get_item_obj(year_road)
        x_item_dict = self.x_budunit._item_dict
        item_list = all_between(x_item_dict, self.time_range_root_road, year_road)
        open_rangeunit = calc_range(item_list, self.x_min, self.x_min)
        gogo_month_dict = year_item.get_kids_in_range(open_rangeunit.gogo)
        month_item = None
        for x_monthname, month_item in gogo_month_dict.items():
            self._month = x_monthname
            month_item = month_item

        self._monthday = open_rangeunit.gogo - month_item._gogo_calc + month_item.addin
        self._monthday = self._monthday // 1440

    def _set_hour(self):
        day_road = get_day_road(self.x_budunit, self.time_range_root_road)
        day_item = self.x_budunit.get_item_obj(day_road)
        x_item_list = [self._timeline_item, day_item]
        rangeunit = calc_range(x_item_list, self.x_min, self.x_min)
        hour_dict = day_item.get_kids_in_range(rangeunit.gogo)
        for x_hour, hour_item in hour_dict.items():
            self._hour = x_hour
            hour_item = hour_item

        self._minute = rangeunit.gogo - hour_item._gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        x_time_road = self.time_range_root_road
        x_item_dict = self.x_budunit._item_dict
        # count 400 year blocks
        self._c400_count = self.x_min // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_clean_road = get_c400_clean_road(self.x_budunit, x_time_road)
        c400_clean_item_list = all_between(x_item_dict, x_time_road, c400_clean_road)
        c400_clean_range = calc_range(c400_clean_item_list, self.x_min, self.x_min)
        self._c100_count = c400_clean_range.gogo // c400_constants.c100_length

        # count 4 year blocks
        c100_road = get_c100_road(self.x_budunit, x_time_road)
        c100_item_list = all_between(x_item_dict, x_time_road, c100_road)
        c100_range = calc_range(c100_item_list, self.x_min, self.x_min)
        self._yr4_count = c100_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_clean_road = get_yr4_clean_road(self.x_budunit, x_time_road)
        yr4_clean_items = all_between(x_item_dict, x_time_road, yr4_clean_road)
        yr4_clean_range = calc_range(yr4_clean_items, self.x_min, self.x_min)
        self._year_count = yr4_clean_range.gogo // c400_constants.year_length

        self._year_num = self._c400_count * 400
        self._year_num += self._c100_count * 100
        self._year_num += self._yr4_count * 4
        self._year_num += self._year_count

    def calc_timeline(self):
        self.x_budunit.settle_bud()
        self._set_timeline_item()
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
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f03_chrono")


def get_default_timeline_config_file_name() -> str:
    return "default_timeline_config.json"


def get_default_timeline_config_dict() -> dict:
    x_filename = get_default_timeline_config_file_name()
    return get_dict_from_json(open_file(config_file_dir(), x_filename))


@dataclass
class TimeLineUnit:
    c400_number: int = None
    hours_config: list[list[str, int]] = None
    months_config: list[list[str, int]] = None
    monthday_distortion: int = None
    timeline_idea: TimeLineIdea = None
    weekdays_config: list[str] = None
    yr1_jan1_offset: int = None

    def get_dict(self) -> dict:
        return {
            "c400_number": self.c400_number,
            "hours_config": self.hours_config,
            "months_config": self.months_config,
            "monthday_distortion": self.monthday_distortion,
            "timeline_idea": self.timeline_idea,
            "weekdays_config": self.weekdays_config,
            "yr1_jan1_offset": self.yr1_jan1_offset,
        }


def timelineunit_shop(timeline_config: dict = None) -> TimeLineUnit:
    if timeline_config is None:
        timeline_config = get_default_timeline_config_dict()
    return TimeLineUnit(
        c400_number=timeline_config.get(c400_number_str()),
        hours_config=timeline_config.get(hours_config_str()),
        months_config=timeline_config.get(months_config_str()),
        monthday_distortion=timeline_config.get(monthday_distortion_str()),
        timeline_idea=timeline_config.get(timeline_idea_str()),
        weekdays_config=timeline_config.get(weekdays_config_str()),
        yr1_jan1_offset=timeline_config.get(yr1_jan1_offset_str()),
    )
