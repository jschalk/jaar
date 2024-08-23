from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit
from src.creg.timebuilder import (
    create_weekday_ideaunits,
    add_newtimeline_ideaunit,
    new_timeline_ideaunit,
    get_time_min_from_dt,
    hours_config_text,
    weekdays_config_text,
    months_config_text,
    timeline_label_text,
    yr1_jan1_offset_text,
)
from datetime import datetime


def cregtime_ideaunit() -> dict[str, IdeaUnit]:
    return new_timeline_ideaunit(get_cregtime_text(), 7)


def get_wed():
    return creg_weekdays_list()[0]


def get_thu():
    return creg_weekdays_list()[1]


def get_fri():
    return creg_weekdays_list()[2]


def get_sat():
    return creg_weekdays_list()[3]


def get_sun():
    return creg_weekdays_list()[4]


def get_mon():
    return creg_weekdays_list()[5]


def get_tue():
    return creg_weekdays_list()[6]


def get_creg_config() -> dict:
    return {
        timeline_label_text(): "creg",
        yr1_jan1_offset_text(): 440640,
        hours_config_text(): [
            ["0-12am", 1 * 60],
            ["1-1am", 2 * 60],
            ["2-2am", 3 * 60],
            ["3-3am", 4 * 60],
            ["4-4am", 5 * 60],
            ["5-5am", 6 * 60],
            ["6-6am", 7 * 60],
            ["7-7am", 8 * 60],
            ["8-8am", 9 * 60],
            ["9-9am", 10 * 60],
            ["10-10am", 11 * 60],
            ["11-11am", 12 * 60],
            ["12-12pm", 13 * 60],
            ["13-1pm", 14 * 60],
            ["14-2pm", 15 * 60],
            ["15-3pm", 16 * 60],
            ["16-4pm", 17 * 60],
            ["17-5pm", 18 * 60],
            ["18-6pm", 19 * 60],
            ["19-7pm", 20 * 60],
            ["20-8pm", 21 * 60],
            ["21-9pm", 22 * 60],
            ["22-10pm", 23 * 60],
            ["23-11pm", 24 * 60],
        ],
        weekdays_config_text(): [
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
            "Monday",
            "Tuesday",
        ],
        months_config_text(): [
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
        ],
    }


def creg_hours_list() -> list[list[str, int]]:
    return get_creg_config().get(hours_config_text())


def creg_weekdays_list() -> list[str]:
    return get_creg_config().get(weekdays_config_text())


def creg_weekday_ideaunits() -> dict[str, IdeaUnit]:
    return create_weekday_ideaunits(creg_weekdays_list())


def creg_months_list() -> list[list[str, int]]:
    return get_creg_config().get(months_config_text())


def get_cregtime_text():
    return get_creg_config().get(timeline_label_text())


def creg_hour_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    timeline_text = get_cregtime_text()
    creg_c400_count = 7
    timeline_weekdays_list = creg_weekdays_list()
    timeline_months_list = creg_months_list()
    timeline_hours_list = creg_hours_list()
    add_newtimeline_ideaunit(
        x_budunit=x_budunit,
        timeline_text=timeline_text,
        timeline_c400_count=creg_c400_count,
        timeline_hours_list=timeline_hours_list,
        timeline_months_list=timeline_months_list,
        timeline_weekdays_list=timeline_weekdays_list,
    )
    return x_budunit


def get_creg_min_from_dt(dt: datetime) -> int:
    x_yr1_jan1_offset = get_creg_config().get(yr1_jan1_offset_text())
    return get_time_min_from_dt(dt=dt, yr1_jan1_offset=x_yr1_jan1_offset)
