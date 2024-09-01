from src._instrument.file import open_file
from src._instrument.python_tool import get_dict_from_json, conditional_fig_show
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
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter


def chrono_examples_dir() -> str:
    return "src/chrono/examples"


def creg_str() -> str:
    return "creg"


def cinco_str() -> str:
    return "cinco"


def get_cinco_config() -> dict:
    return get_example_timeline_config(cinco_str())


def get_creg_config() -> dict:
    return get_example_timeline_config(creg_str())


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


def get_cregtime_text():
    return get_creg_config().get(timeline_label_text())


def creg_hour_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    return add_newtimeline_ideaunit(x_budunit, get_creg_config())


def add_time_cinco_ideaunit(x_budunit: BudUnit) -> BudUnit:
    return add_newtimeline_ideaunit(x_budunit, get_cinco_config())


def get_creg_min_from_dt(dt: datetime) -> int:
    return get_time_min_from_dt(dt, get_creg_config().get(yr1_jan1_offset_text()))


def get_cinco_min_from_dt(dt: datetime) -> int:
    return get_time_min_from_dt(dt, get_cinco_config().get(yr1_jan1_offset_text()))


def display_current_creg_cinco_min(graphics_bool: bool):
    current_datetime = datetime.now()
    current_creg = get_creg_min_from_dt(current_datetime)
    current_cinco = get_cinco_min_from_dt(current_datetime)

    curr_text = f"year: {current_datetime.year}"
    curr_text += f", month: {current_datetime.month}"
    curr_text += f", day: {current_datetime.day}"
    curr_text += f", hour: {current_datetime.hour}"
    curr_text += f", minute: {current_datetime.minute}"
    curr_text = f"<b>{curr_text}</b>"
    creg_min_text = f"<b>creg timeline min: {current_creg}</b>"
    cinco_min_text = f"<b>cinco timeline min: {current_cinco}</b>"
    curr_list = [curr_text, creg_min_text, cinco_min_text]
    xp_list = [1, 1, 1]
    yp_list = [3, 2, 1]

    x_fig = plotly_Figure()
    x_fig.update_xaxes(range=[-6, 8])
    x_fig.update_yaxes(range=[0, 5])
    x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
    x_fig.update_layout(font=x_font)
    x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
    x_fig.add_trace(x1_scatter)
    conditional_fig_show(x_fig, graphics_bool)
