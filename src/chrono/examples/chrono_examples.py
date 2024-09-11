from src._instrument.file import open_file
from src._instrument.python_tool import get_dict_from_json, conditional_fig_show
from src.bud.idea import IdeaUnit
from src.bud.bud import BudUnit, budunit_shop
from src.chrono.chrono import (
    create_weekday_ideaunits,
    add_newtimeline_ideaunit,
    new_timeline_ideaunit,
    get_min_from_dt_offset,
    hours_config_str,
    weekdays_config_str,
    months_config_str,
    timeline_label_str,
    yr1_jan1_offset_str,
    c400_config_str,
    chronounit_shop,
)
from datetime import datetime
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter


def chrono_examples_dir() -> str:
    return "src/chrono/examples"


def creg_str() -> str:
    return "creg"


def five_str() -> str:
    return "five"


def get_five_config() -> dict:
    return get_example_timeline_config(five_str())


def get_creg_config() -> dict:
    return get_example_timeline_config(creg_str())


def get_squirt_config() -> dict:
    return get_example_timeline_config("squirt")


def get_example_timeline_config(timeline_label: str) -> dict:
    x_file_name = f"timeline_config_{timeline_label}.json"
    return get_dict_from_json(open_file(chrono_examples_dir(), x_file_name))


def cregtime_ideaunit() -> IdeaUnit:
    c400_count = get_creg_config().get(c400_config_str())
    return new_timeline_ideaunit(get_cregtime_str(), c400_count)


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
    return get_creg_config().get(hours_config_str())


def creg_weekdays_list() -> list[str]:
    return get_creg_config().get(weekdays_config_str())


def creg_weekday_ideaunits() -> dict[str, IdeaUnit]:
    return create_weekday_ideaunits(creg_weekdays_list())


def get_cregtime_str():
    return get_creg_config().get(timeline_label_str())


def creg_hour_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    return add_newtimeline_ideaunit(x_budunit, get_creg_config())


def add_time_five_ideaunit(x_budunit: BudUnit) -> BudUnit:
    return add_newtimeline_ideaunit(x_budunit, get_five_config())


def add_time_squirt_ideaunit(x_budunit: BudUnit) -> BudUnit:
    return add_newtimeline_ideaunit(x_budunit, get_squirt_config())


def get_creg_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_creg_config().get(yr1_jan1_offset_str()))


def get_five_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_five_config().get(yr1_jan1_offset_str()))


def get_squirt_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_squirt_config().get(yr1_jan1_offset_str()))


def display_current_creg_five_min(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime.now()
        current_creg = get_creg_min_from_dt(current_datetime)
        current_five = get_five_min_from_dt(current_datetime)

        curr_str = f"year: {current_datetime.year}"
        curr_str += f", month: {current_datetime.month}"
        curr_str += f", day: {current_datetime.day}"
        curr_str += f", hour: {current_datetime.hour}"
        curr_str += f", minute: {current_datetime.minute}"
        curr_str = f"<b>{curr_str}</b>"
        creg_min_str = f"<b>creg timeline min: {current_creg}</b>"
        five_min_str = f"<b>five timeline min: {current_five}</b>"
        curr_list = [curr_str, creg_min_str, five_min_str]
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


def display_current_creg_five_time_attrs(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime.now()
        sue_bud = budunit_shop("Sue")
        sue_bud = add_time_creg_ideaunit(sue_bud)
        sue_bud = add_time_five_ideaunit(sue_bud)
        time_road = sue_bud.make_l1_road("time")
        creg_road = sue_bud.make_road(time_road, creg_str())
        five_road = sue_bud.make_road(time_road, five_str())
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        creg_chronounit = chronounit_shop(sue_bud, creg_road, creg_min)
        five_chronounit = chronounit_shop(sue_bud, five_road, five_min)
        creg_chronounit.calc_timeline()
        five_chronounit.calc_timeline()
        creg_blurb = f"<b>{creg_chronounit.get_blurb()}</b>"
        five_blurb = f"<b>{five_chronounit.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg timeline min: {creg_min}</b>"
        five_min_str = f"<b>five timeline min: {five_min}</b>"
        curr_list = [dt_str, creg_min_str, creg_blurb, five_min_str, five_blurb]
        xp_list = [1, 1, 1, 1, 1]
        yp_list = [7, 5, 4, 2, 1]

        x_fig = plotly_Figure()
        x_fig.update_xaxes(range=[-6, 8])
        x_fig.update_yaxes(range=[0, 10])
        x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
        x_fig.update_layout(font=x_font)
        x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
        x_fig.add_trace(x1_scatter)
        conditional_fig_show(x_fig, graphics_bool)


def display_creg_five_squirt_time_attrs(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime(2031, 2, 17, 7, 47)
        sue_bud = budunit_shop("Sue")
        sue_bud = add_time_creg_ideaunit(sue_bud)
        sue_bud = add_time_five_ideaunit(sue_bud)
        sue_bud = add_time_squirt_ideaunit(sue_bud)
        time_road = sue_bud.make_l1_road("time")
        creg_road = sue_bud.make_road(time_road, creg_str())
        five_road = sue_bud.make_road(time_road, five_str())
        squirt_road = sue_bud.make_road(time_road, "squirt")
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        squirt_min = get_squirt_min_from_dt(current_datetime)
        creg_chronounit = chronounit_shop(sue_bud, creg_road, creg_min)
        five_chronounit = chronounit_shop(sue_bud, five_road, five_min)
        squirt_chronounit = chronounit_shop(sue_bud, squirt_road, squirt_min)
        creg_chronounit.calc_timeline()
        five_chronounit.calc_timeline()
        squirt_chronounit.calc_timeline()
        creg_blurb = f"<b>{creg_chronounit.get_blurb()}</b>"
        five_blurb = f"<b>{five_chronounit.get_blurb()}</b>"
        squirt_blurb = f"<b>{squirt_chronounit.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg timeline min: {creg_min}</b>"
        five_min_str = f"<b>five timeline min: {five_min}</b>"
        squirt_min_str = f"<b>squirt timeline min: {squirt_min}</b>"
        curr_list = [
            dt_str,
            creg_min_str,
            creg_blurb,
            five_min_str,
            five_blurb,
            squirt_min_str,
            squirt_blurb,
        ]
        xp_list = [1, 1, 1, 1, 1, 1, 1]
        yp_list = [7, 5, 4, 2, 1, -1, -2]

        x_fig = plotly_Figure()
        x_fig.update_xaxes(range=[-6, 8])
        x_fig.update_yaxes(range=[-5, 10])
        x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
        x_fig.update_layout(font=x_font)
        x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
        x_fig.add_trace(x1_scatter)
        conditional_fig_show(x_fig, graphics_bool)
