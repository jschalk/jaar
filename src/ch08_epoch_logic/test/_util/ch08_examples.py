from datetime import datetime
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch01_data_toolbox.file_toolbox import open_json
from src.ch01_data_toolbox.plotly_toolbox import conditional_fig_show
from src.ch06_plan_logic.plan import PlanUnit
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch08_epoch_logic.epoch_main import (
    add_newepoch_planunit,
    beliefepochpoint_shop,
    create_weekday_planunits,
    get_min_from_dt_offset,
    new_epoch_planunit,
)
from src.ref.ch08_keywords import Ch08Keywords as wx


def get_five_config() -> dict:
    return get_example_epoch_config(wx.five)


def get_creg_config() -> dict:
    return get_example_epoch_config(wx.creg)


def get_squirt_config() -> dict:
    return get_example_epoch_config("squirt")


def get_example_epoch_config(epoch_label: str) -> dict:
    x_dir = "src/ch08_epoch_logic/test/_util"
    x_filename = f"epoch_config_{epoch_label}.json"
    return open_json(x_dir, x_filename)


def cregtime_planunit() -> PlanUnit:
    c400_number = get_creg_config().get(wx.c400_number)
    return new_epoch_planunit(get_cregtime_str(), c400_number)


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
    return get_creg_config().get(wx.hours_config)


def creg_weekdays_list() -> list[str]:
    return get_creg_config().get(wx.weekdays_config)


def creg_weekday_planunits() -> dict[str, PlanUnit]:
    return create_weekday_planunits(creg_weekdays_list())


def get_cregtime_str() -> str:
    return get_creg_config().get(wx.epoch_label)


def creg_hour_int_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_planunit(x_beliefunit: BeliefUnit) -> BeliefUnit:
    """Add creg epoch planunit to beliefunit"""
    return add_newepoch_planunit(x_beliefunit, get_creg_config())


def add_time_five_planunit(x_beliefunit: BeliefUnit) -> BeliefUnit:
    """Add five epoch planunit to beliefunit"""
    return add_newepoch_planunit(x_beliefunit, get_five_config())


def add_time_squirt_planunit(x_beliefunit: BeliefUnit) -> BeliefUnit:
    """Add squirt epoch planunit to beliefunit"""
    return add_newepoch_planunit(x_beliefunit, get_squirt_config())


def get_creg_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_creg_config().get(wx.yr1_jan1_offset))


def get_five_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_five_config().get(wx.yr1_jan1_offset))


def get_squirt_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_squirt_config().get(wx.yr1_jan1_offset))


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
        creg_min_str = f"<b>creg epoch min: {current_creg}</b>"
        five_min_str = f"<b>five epoch min: {current_five}</b>"
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
        sue_belief = beliefunit_shop("Sue")
        sue_belief = add_time_creg_planunit(sue_belief)
        sue_belief = add_time_five_planunit(sue_belief)
        time_rope = sue_belief.make_l1_rope("time")
        creg_rope = sue_belief.make_rope(time_rope, wx.creg)
        five_rope = sue_belief.make_rope(time_rope, wx.five)
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        creg_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, creg_min)
        five_epochpoint = beliefepochpoint_shop(sue_belief, five_rope, five_min)
        creg_epochpoint.calc_epoch()
        five_epochpoint.calc_epoch()
        creg_blurb = f"<b>{creg_epochpoint.get_blurb()}</b>"
        five_blurb = f"<b>{five_epochpoint.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg epoch min: {creg_min}</b>"
        five_min_str = f"<b>five epoch min: {five_min}</b>"
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
        sue_belief = beliefunit_shop("Sue")
        sue_belief = add_time_creg_planunit(sue_belief)
        sue_belief = add_time_five_planunit(sue_belief)
        sue_belief = add_time_squirt_planunit(sue_belief)
        time_rope = sue_belief.make_l1_rope("time")
        creg_rope = sue_belief.make_rope(time_rope, wx.creg)
        five_rope = sue_belief.make_rope(time_rope, wx.five)
        squirt_rope = sue_belief.make_rope(time_rope, "squirt")
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        squirt_min = get_squirt_min_from_dt(current_datetime)
        creg_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, creg_min)
        five_epochpoint = beliefepochpoint_shop(sue_belief, five_rope, five_min)
        squirt_epochpoint = beliefepochpoint_shop(sue_belief, squirt_rope, squirt_min)
        creg_epochpoint.calc_epoch()
        five_epochpoint.calc_epoch()
        squirt_epochpoint.calc_epoch()
        creg_blurb = f"<b>{creg_epochpoint.get_blurb()}</b>"
        five_blurb = f"<b>{five_epochpoint.get_blurb()}</b>"
        squirt_blurb = f"<b>{squirt_epochpoint.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg epoch min: {creg_min}</b>"
        five_min_str = f"<b>five epoch min: {five_min}</b>"
        squirt_min_str = f"<b>squirt epoch min: {squirt_min}</b>"
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


def get_expected_creg_2024_markdown() -> str:
    return """
                               Year 2024                                

       March                     April                      May         
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
             1  2  3       1  2  3  4  5  6  7             1  2  3  4  5
 4  5  6  7  8  9 10       8  9 10 11 12 13 14       6  7  8  9 10 11 12
11 12 13 14 15 16 17      15 16 17 18 19 20 21      13 14 15 16 17 18 19
18 19 20 21 22 23 24      22 23 24 25 26 27 28      20 21 22 23 24 25 26
25 26 27 28 29 30 31      29 30                     27 28 29 30 31      

        June                      July                     August       
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2       1  2  3  4  5  6  7                1  2  3  4
 3  4  5  6  7  8  9       8  9 10 11 12 13 14       5  6  7  8  9 10 11
10 11 12 13 14 15 16      15 16 17 18 19 20 21      12 13 14 15 16 17 18
17 18 19 20 21 22 23      22 23 24 25 26 27 28      19 20 21 22 23 24 25
24 25 26 27 28 29 30      29 30 31                  26 27 28 29 30 31   

     September                  October                   November      
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1          1  2  3  4  5  6                   1  2  3
 2  3  4  5  6  7  8       7  8  9 10 11 12 13       4  5  6  7  8  9 10
 9 10 11 12 13 14 15      14 15 16 17 18 19 20      11 12 13 14 15 16 17
16 17 18 19 20 21 22      21 22 23 24 25 26 27      18 19 20 21 22 23 24
23 24 25 26 27 28 29      28 29 30 31               25 26 27 28 29 30   
30                                                                      

      December               January (2025)           February (2025)   
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1             1  2  3  4  5                      1  2
 2  3  4  5  6  7  8       6  7  8  9 10 11 12       3  4  5  6  7  8  9
 9 10 11 12 13 14 15      13 14 15 16 17 18 19      10 11 12 13 14 15 16
16 17 18 19 20 21 22      20 21 22 23 24 25 26      17 18 19 20 21 22 23
23 24 25 26 27 28 29      27 28 29 30 31            24 25 26 27 28      
30 31                                                                   """


def get_expected_creg_year0_markdown() -> str:
    return """
                                 Year 0                                 

       March                     April                      May         
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
 1  2  3  4  5  6  7                1  2  3  4                      1  2
 8  9 10 11 12 13 14       5  6  7  8  9 10 11       3  4  5  6  7  8  9
15 16 17 18 19 20 21      12 13 14 15 16 17 18      10 11 12 13 14 15 16
22 23 24 25 26 27 28      19 20 21 22 23 24 25      17 18 19 20 21 22 23
29 30 31                  26 27 28 29 30            24 25 26 27 28 29 30
                                                    31                  

        June                      July                     August       
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
    1  2  3  4  5  6                1  2  3  4                         1
 7  8  9 10 11 12 13       5  6  7  8  9 10 11       2  3  4  5  6  7  8
14 15 16 17 18 19 20      12 13 14 15 16 17 18       9 10 11 12 13 14 15
21 22 23 24 25 26 27      19 20 21 22 23 24 25      16 17 18 19 20 21 22
28 29 30                  26 27 28 29 30 31         23 24 25 26 27 28 29
                                                    30 31               

     September                  October                   November      
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
       1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7
 6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14
13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21
20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28
27 28 29 30               25 26 27 28 29 30 31      29 30               

      December                January (1)               February (1)    
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
       1  2  3  4  5                      1  2          1  2  3  4  5  6
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       7  8  9 10 11 12 13
13 14 15 16 17 18 19      10 11 12 13 14 15 16      14 15 16 17 18 19 20
20 21 22 23 24 25 26      17 18 19 20 21 22 23      21 22 23 24 25 26 27
27 28 29 30 31            24 25 26 27 28 29 30      28                  
                          31                                            """


def get_expected_five_5524_markdown() -> str:
    return """
                                Year 5224                                 

   Fredrick              Geo               Holocene             Iguana    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Jesus                Keel               LeBron             Mikayla    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Ninon               Obama              Preston              Quorum    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

  RioGrande             Simon               Trump     
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14         
18 19 20 21 22      18 19 20 21 22                    
23 24               23 24                             """
