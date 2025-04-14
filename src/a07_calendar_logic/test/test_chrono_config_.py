from src.a00_data_toolboxs.file_toolbox import save_file
from src.a00_data_toolboxs.dict_toolbox import get_json_from_dict
from src.a02_finance_toolboxs.finance_config import TimeLinePoint
from src.a06_bud_logic.bud import budunit_shop
from src.a07_calendar_logic.examples.chrono_examples import (
    get_creg_config,
    get_five_config,
    get_squirt_config,
    chrono_examples_dir,
    get_example_timeline_config,
    five_str,
)
from src.a07_calendar_logic.chrono import (
    C400Constants,
    get_c400_constants,
    day_length,
    hours_config_str,
    weekdays_config_str,
    months_config_str,
    monthday_distortion_str,
    timeline_title_str,
    c400_number_str,
    yr1_jan1_offset_str,
    validate_timeline_config,
    timeline_config_shop,
    get_default_timeline_config_dict,
    TimeLineUnit,
    timelineunit_shop,
    week_str,
    year_str,
    day_str,
    get_year_road,
    get_week_road,
    get_day_road,
    time_str,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
)
from copy import deepcopy as copy_deepcopy


def test_TimeLinePoint_Exists():
    # ESTABLISH / WHEN / THEN
    assert TimeLinePoint(4) == 4


def test_C400Constants_Exists():
    # ESTABLISH / WHEN
    x_c400_constants = C400Constants("x1", "x2", "x3", "x4", "x5", "x6", "x7")

    # THEN
    assert x_c400_constants.day_length == "x1"
    assert x_c400_constants.c400_leap_length == "x2"
    assert x_c400_constants.c400_clean_length == "x3"
    assert x_c400_constants.c100_length == "x4"
    assert x_c400_constants.yr4_leap_length == "x5"
    assert x_c400_constants.yr4_clean_length == "x6"
    assert x_c400_constants.year_length == "x7"


def test_get_c400_constantss_ReturnsObj():
    # ESTABLISH / WHEN
    x_c400_constants = get_c400_constants()

    assert x_c400_constants.day_length == 1440
    assert x_c400_constants.c400_leap_length == 210379680
    assert x_c400_constants.c400_clean_length == 210378240
    assert x_c400_constants.c100_length == 52594560
    assert x_c400_constants.yr4_leap_length == 2103840
    assert x_c400_constants.yr4_clean_length == 2102400
    assert x_c400_constants.year_length == 525600


def test_day_length_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert day_length() == get_c400_constants().day_length
    assert day_length() == 1440


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert hours_config_str() == "hours_config"
    assert weekdays_config_str() == "weekdays_config"
    assert months_config_str() == "months_config"
    assert monthday_distortion_str() == "monthday_distortion"
    assert timeline_title_str() == "timeline_title"
    assert c400_number_str() == "c400_number"
    assert yr1_jan1_offset_str() == "yr1_jan1_offset"


def test_validate_timeline_config_ReturnsObj_CheckEachElementIsNecessary():
    # ESTABLISH / WHEN / THEN
    assert not validate_timeline_config({})

    # ESTABLISH / WHEN / THEN
    orig_creg_config = get_creg_config()
    x_squirt_config = get_squirt_config()
    assert validate_timeline_config(orig_creg_config)
    assert validate_timeline_config(x_squirt_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    assert validate_timeline_config(creg_config)
    creg_config.pop(hours_config_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(weekdays_config_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(months_config_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(monthday_distortion_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(timeline_title_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(c400_number_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(yr1_jan1_offset_str())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[hours_config_str()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[months_config_str()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[weekdays_config_str()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[yr1_jan1_offset_str()] = None
    assert not validate_timeline_config(creg_config)
    creg_config[yr1_jan1_offset_str()] = 0
    assert validate_timeline_config(creg_config)


def test_get_default_timeline_config_dict_IsValid():
    # ESTABLISH / WHEN
    default_config = get_default_timeline_config_dict()
    # THEN
    assert validate_timeline_config(default_config)


def test_is_timeline_config_valid_ReturnsObj_CheckObjsRepeat():
    # ESTABLISH / WHEN / THEN
    orig_creg_config = get_creg_config()
    assert validate_timeline_config(orig_creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[months_config_str()] = [["x_str", 30], ["y_str", 180], ["x_str", 365]]
    assert not validate_timeline_config(creg_config)
    creg_config[months_config_str()] = [["x_str", 30], ["y_str", 180], ["z_str", 365]]
    assert validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[hours_config_str()] = [["x_str", 30], ["y_str", 180], ["x_str", 1440]]
    assert not validate_timeline_config(creg_config)
    creg_config[hours_config_str()] = [["x_str", 30], ["y_str", 180], ["z_str", 1440]]
    assert validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[weekdays_config_str()] = ["x_str", "y_str", "x_str"]
    assert not validate_timeline_config(creg_config)
    creg_config[weekdays_config_str()] = ["x_str", "y_str", "z_str"]
    assert validate_timeline_config(creg_config)


def test_timeline_config_shop_ReturnsObj_AllParameters():
    # ESTABLISH
    five_c400_number = 25
    five_yr1_jan1_offset = 1683037440 + 440640  # 3200 years + JanLen + FebLen
    five_hour_length = 72
    five_month_length = 25
    five_weekday_list = ["Anaday", "Baileyday", "Chiday", "Danceday", "Elonday"]
    # months = ["B", "C", "E", "G", "H", "I", "K", "L", "N", "P", "Q", "R", "T", "U", "W"]
    # c_mons = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    five_months_list = [
        "Fresh",
        "Geo",
        "Holocene",
        "Iguana",
        "Jinping",
        "Keel",
        "Lebron",
        "Mikayla",
        "Ninon",
        "Obama",
        "Preston",
        "Quorum",
        "RioGrande",
        "Simon",
        "Trump",
    ]
    assert len(five_months_list) == 15
    calc_months_day_length = (len(five_months_list) - 1) * five_month_length
    assert calc_months_day_length == 350
    print(f"{len(five_months_list)=} {calc_months_day_length=}")

    # WHEN
    five_dict = timeline_config_shop(
        timeline_title=five_str(),
        c400_number=five_c400_number,
        hour_length=five_hour_length,
        month_length=five_month_length,
        weekday_list=five_weekday_list,
        months_list=five_months_list,
        yr1_jan1_offset=five_yr1_jan1_offset,
        monthday_distortion=0,
    )

    # THEN
    assert validate_timeline_config(five_dict)
    assert five_dict.get(timeline_title_str()) == five_str()
    assert five_dict.get(c400_number_str()) == five_c400_number
    assert five_dict.get(weekdays_config_str()) == five_weekday_list
    x_months_config = five_dict.get(months_config_str())
    gen_months = [mon_config[0] for mon_config in x_months_config]
    assert gen_months == five_months_list
    assert x_months_config[0][0] == "Fresh"
    assert x_months_config[0][1] == 25
    assert x_months_config[6][0] == "Lebron"
    assert x_months_config[6][1] == 175
    assert x_months_config[13][0] == "Simon"
    assert x_months_config[13][1] == 350
    assert x_months_config[14][0] == "Trump"
    assert x_months_config[14][1] == 365
    x_hours_config = five_dict.get(hours_config_str())
    assert len(x_hours_config) == 20
    assert x_hours_config[0] == ["0hr", 72]
    assert x_hours_config[4] == ["4hr", 360]
    assert five_dict.get(yr1_jan1_offset_str()) == five_yr1_jan1_offset

    # five_filename = f"timeline_config_{five_str()}.json"
    # five_file_str = get_json_from_dict(five_dict)
    # save_file(chrono_examples_dir(), five_filename, five_file_str)
    expected_config = get_example_timeline_config(five_str())
    assert validate_timeline_config(expected_config)
    assert expected_config.get(hours_config_str()) == x_hours_config
    assert expected_config == five_dict


def test_timeline_config_shop_ReturnsObj_NoParameters():
    # ESTABLISH
    h_c400_number = 7
    h_hours_config = [
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
    h_months_config = [
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
    h_monthday_distortion = 1
    h_timeline_title = "creg"
    h_weekdays_config = [
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
    ]
    h_yr1_jan1_offset = 440640

    # WHEN
    generated_dict = timeline_config_shop()

    # THEN
    print(f"{generated_dict=}")
    print(f"{set(generated_dict.keys())=}")
    print(f"{timeline_title_str()=}")
    print(f"{generated_dict.get(timeline_title_str())=}")
    assert generated_dict.get(c400_number_str()) == h_c400_number

    assert generated_dict.get(timeline_title_str()) == h_timeline_title
    assert generated_dict.get(c400_number_str()) == h_c400_number
    assert generated_dict.get(hours_config_str()) == h_hours_config
    assert generated_dict.get(months_config_str()) == h_months_config
    assert generated_dict.get(monthday_distortion_str()) == h_monthday_distortion
    assert generated_dict.get(timeline_title_str()) == h_timeline_title
    assert generated_dict.get(weekdays_config_str()) == h_weekdays_config
    assert generated_dict.get(yr1_jan1_offset_str()) == h_yr1_jan1_offset
    assert validate_timeline_config(generated_dict)


def test_get_year_road_ReturnsObj():
    # ESTABLISH
    fizz_str = "fizz34"
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    fizz_road = sue_budunit.make_road(time_road, fizz_str)
    c400_leap_road = sue_budunit.make_road(fizz_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())

    # WHEN / THEN
    assert year_road == get_year_road(sue_budunit, fizz_road)


def test_get_week_road_ReturnsObj():
    # ESTABLISH
    fizz_str = "fizz34"
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    fizz_road = sue_budunit.make_road(time_road, fizz_str)
    week_road = sue_budunit.make_road(fizz_road, week_str())

    # WHEN / THEN
    assert week_road == get_week_road(sue_budunit, fizz_road)


def test_get_day_road_ReturnsObj():
    # ESTABLISH
    fizz_str = "fizz34"
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    fizz_road = sue_budunit.make_road(time_road, fizz_str)
    day_road = sue_budunit.make_road(fizz_road, day_str())

    # WHEN / THEN
    assert day_road == get_day_road(sue_budunit, fizz_road)


def test_TimeLineUnit_Exists():
    # ESTABLISH / WHEN
    x_timelineunit = TimeLineUnit()

    # THEN
    assert x_timelineunit
    assert not x_timelineunit.c400_number
    assert not x_timelineunit.hours_config
    assert not x_timelineunit.months_config
    assert not x_timelineunit.monthday_distortion
    assert not x_timelineunit.timeline_title
    assert not x_timelineunit.weekdays_config
    assert not x_timelineunit.yr1_jan1_offset


def test_timelineunit_shop_ReturnsObj_Default():
    # ESTABLISH
    creg_config = get_creg_config()

    # WHEN
    x_timelineunit = timelineunit_shop()

    # THEN
    creg_c400_number = creg_config.get(c400_number_str())
    creg_hours_config = creg_config.get(hours_config_str())
    creg_months_config = creg_config.get(months_config_str())
    creg_timeline_title = creg_config.get(timeline_title_str())
    creg_weekdays_config = creg_config.get(weekdays_config_str())
    creg_monthday_distortion = creg_config.get(monthday_distortion_str())
    creg_yr1_jan1_offset = creg_config.get(yr1_jan1_offset_str())

    assert x_timelineunit
    assert x_timelineunit.c400_number == creg_c400_number
    assert x_timelineunit.hours_config == creg_hours_config
    assert x_timelineunit.months_config == creg_months_config
    assert x_timelineunit.monthday_distortion == creg_monthday_distortion
    assert x_timelineunit.timeline_title == creg_timeline_title
    assert x_timelineunit.weekdays_config == creg_weekdays_config
    assert x_timelineunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_timelineunit_shop_ReturnsObj_WhenTimeLineUnitAttributesAreNone():
    # ESTABLISH
    incomplete_creg_config = get_creg_config()
    incomplete_creg_config.pop(c400_number_str())
    incomplete_creg_config.pop(hours_config_str())
    incomplete_creg_config.pop(months_config_str())
    incomplete_creg_config.pop(monthday_distortion_str())
    incomplete_creg_config.pop(weekdays_config_str())
    incomplete_creg_config.pop(yr1_jan1_offset_str())
    assert incomplete_creg_config

    # WHEN
    x_timelineunit = timelineunit_shop(incomplete_creg_config)

    # THEN
    creg_config = get_creg_config()
    creg_c400_number = creg_config.get(c400_number_str())
    creg_hours_config = creg_config.get(hours_config_str())
    creg_months_config = creg_config.get(months_config_str())
    creg_timeline_title = creg_config.get(timeline_title_str())
    creg_weekdays_config = creg_config.get(weekdays_config_str())
    creg_monthday_distortion = creg_config.get(monthday_distortion_str())
    creg_yr1_jan1_offset = creg_config.get(yr1_jan1_offset_str())

    assert x_timelineunit
    assert x_timelineunit.c400_number == creg_c400_number
    assert x_timelineunit.hours_config == creg_hours_config
    assert x_timelineunit.months_config == creg_months_config
    assert x_timelineunit.monthday_distortion == creg_monthday_distortion
    assert x_timelineunit.timeline_title == creg_timeline_title
    assert x_timelineunit.weekdays_config == creg_weekdays_config
    assert x_timelineunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_TimeLineUnit_get_dict_ReturnsObj():
    # ESTABLISH
    x_timelineunit = timelineunit_shop()

    # WHEN
    x_config = x_timelineunit.get_dict()

    # THEN
    assert x_config
    assert x_config == get_creg_config()
