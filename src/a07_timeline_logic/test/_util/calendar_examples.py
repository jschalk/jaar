from datetime import datetime
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.a00_data_toolbox.file_toolbox import open_json
from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a05_concept_logic.concept import ConceptUnit
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_timeline_logic.test._util.a07_env import get_module_examples_dir
from src.a07_timeline_logic.test._util.a07_str import (
    c400_number_str,
    creg_str,
    five_str,
    hours_config_str,
    months_config_str,
    timeline_label_str,
    weekdays_config_str,
    yr1_jan1_offset_str,
)
from src.a07_timeline_logic.timeline import (
    add_newtimeline_conceptunit,
    create_weekday_conceptunits,
    get_min_from_dt_offset,
    new_timeline_conceptunit,
    plantimelinepoint_shop,
)


def get_five_config() -> dict:
    return get_example_timeline_config(five_str())


def get_creg_config() -> dict:
    return get_example_timeline_config(creg_str())


def get_squirt_config() -> dict:
    return get_example_timeline_config("squirt")


def get_example_timeline_config(timeline_label: str) -> dict:
    x_filename = f"timeline_config_{timeline_label}.json"
    return open_json(get_module_examples_dir(), x_filename)


def cregtime_conceptunit() -> ConceptUnit:
    c400_number = get_creg_config().get(c400_number_str())
    return new_timeline_conceptunit(get_cregtime_str(), c400_number)


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


def creg_weekday_conceptunits() -> dict[str, ConceptUnit]:
    return create_weekday_conceptunits(creg_weekdays_list())


def get_cregtime_str() -> str:
    return get_creg_config().get(timeline_label_str())


def creg_hour_int_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_conceptunit(x_planunit: PlanUnit) -> PlanUnit:
    return add_newtimeline_conceptunit(x_planunit, get_creg_config())


def add_time_five_conceptunit(x_planunit: PlanUnit) -> PlanUnit:
    return add_newtimeline_conceptunit(x_planunit, get_five_config())


def add_time_squirt_conceptunit(x_planunit: PlanUnit) -> PlanUnit:
    return add_newtimeline_conceptunit(x_planunit, get_squirt_config())


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
        sue_plan = planunit_shop("Sue")
        sue_plan = add_time_creg_conceptunit(sue_plan)
        sue_plan = add_time_five_conceptunit(sue_plan)
        time_rope = sue_plan.make_l1_rope("time")
        creg_rope = sue_plan.make_rope(time_rope, creg_str())
        five_rope = sue_plan.make_rope(time_rope, five_str())
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        creg_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, creg_min)
        five_timelinepoint = plantimelinepoint_shop(sue_plan, five_rope, five_min)
        creg_timelinepoint.calc_timeline()
        five_timelinepoint.calc_timeline()
        creg_blurb = f"<b>{creg_timelinepoint.get_blurb()}</b>"
        five_blurb = f"<b>{five_timelinepoint.get_blurb()}</b>"

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
        sue_plan = planunit_shop("Sue")
        sue_plan = add_time_creg_conceptunit(sue_plan)
        sue_plan = add_time_five_conceptunit(sue_plan)
        sue_plan = add_time_squirt_conceptunit(sue_plan)
        time_rope = sue_plan.make_l1_rope("time")
        creg_rope = sue_plan.make_rope(time_rope, creg_str())
        five_rope = sue_plan.make_rope(time_rope, five_str())
        squirt_rope = sue_plan.make_rope(time_rope, "squirt")
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        squirt_min = get_squirt_min_from_dt(current_datetime)
        creg_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, creg_min)
        five_timelinepoint = plantimelinepoint_shop(sue_plan, five_rope, five_min)
        squirt_timelinepoint = plantimelinepoint_shop(sue_plan, squirt_rope, squirt_min)
        creg_timelinepoint.calc_timeline()
        five_timelinepoint.calc_timeline()
        squirt_timelinepoint.calc_timeline()
        creg_blurb = f"<b>{creg_timelinepoint.get_blurb()}</b>"
        five_blurb = f"<b>{five_timelinepoint.get_blurb()}</b>"
        squirt_blurb = f"<b>{squirt_timelinepoint.get_blurb()}</b>"

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
