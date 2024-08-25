from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit
from src.chrono.chrono import (
    create_weekday_ideaunits,
    add_newtimeline_ideaunit,
    new_timeline_ideaunit,
    get_time_min_from_dt,
    hours_config_text,
    weekdays_config_text,
    months_config_text,
    timeline_label_text,
    yr1_jan1_offset_text,
    c400_config_text,
)
from datetime import datetime


def chrono_examples_dir() -> str:
    return "src/chrono/examples"


def get_creg_config() -> dict:
    return get_example_timeline_config("creg")


def get_squirt_config() -> dict:
    return get_example_timeline_config("squirt")


def get_example_timeline_config(timeline_label: str) -> dict:
    x_file_name = f"timeline_config_{timeline_label}.json"
    return get_dict_from_json(open_file(chrono_examples_dir(), x_file_name))


def cregtime_ideaunit() -> IdeaUnit:
    c400_count = get_creg_config().get(c400_config_text())
    return new_timeline_ideaunit(get_cregtime_text(), c400_count)


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
    return add_newtimeline_ideaunit(x_budunit, get_creg_config())


def get_creg_min_from_dt(dt: datetime) -> int:
    x_yr1_jan1_offset = get_creg_config().get(yr1_jan1_offset_text())
    return get_time_min_from_dt(dt=dt, yr1_jan1_offset=x_yr1_jan1_offset)
