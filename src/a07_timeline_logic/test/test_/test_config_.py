from copy import deepcopy as copy_deepcopy
from inspect import getdoc as inspect_getdoc
from src.a01_term_logic.rope import create_rope, default_knot_if_None
from src.a01_term_logic.test._util.a01_str import knot_str
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a07_timeline_logic.test._util.a07_str import (
    c100_str,
    c400_clean_str,
    c400_leap_str,
    c400_number_str,
    day_str,
    hours_config_str,
    monthday_distortion_str,
    months_config_str,
    time_str,
    timeline_label_str,
    week_str,
    weekdays_config_str,
    year_str,
    yr1_jan1_offset_str,
    yr4_clean_str,
    yr4_leap_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    five_str,
    get_creg_config,
    get_example_timeline_config,
    get_squirt_config,
)
from src.a07_timeline_logic.timeline_main import (
    C400Constants,
    TimeLineLabel,
    TimeLineUnit,
    day_length,
    get_c400_constants,
    get_day_rope,
    get_default_timeline_config_dict,
    get_timeline_rope,
    get_week_rope,
    get_year_rope,
    timeline_config_shop,
    timelineunit_shop,
    validate_timeline_config,
)


def test_TimeLineLabel_exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_timelinelabel = TimeLineLabel(empty_str)
    # THEN
    assert x_timelinelabel == empty_str
    doc_str = f"TimeLineLabel is required for every TimeLineUnit. It is a LabelTerm that must not contain the {knot_str()}."
    assert inspect_getdoc(x_timelinelabel) == doc_str


def test_get_timeline_rope_ReturnsObj_Scenario0_default_knot():
    # ESTABLISH
    fay_belief_label = "Fay"
    bob_timeline_label = "Bob_time3"
    default_knot = default_knot_if_None()

    # WHEN
    bob_rope = get_timeline_rope(fay_belief_label, bob_timeline_label, default_knot)

    # THEN
    assert bob_rope
    time_rope = create_rope(fay_belief_label, "time")
    expected_bob_rope = create_rope(time_rope, bob_timeline_label)
    assert bob_rope == expected_bob_rope


def test_get_timeline_rope_ReturnsObj_Scenario1_slash_knot():
    # ESTABLISH
    fay_belief_label = "Fay"
    bob_timeline_label = "Bob_time3"
    slash_knot = "/"
    assert slash_knot != default_knot_if_None()

    # WHEN
    bob_rope = get_timeline_rope(fay_belief_label, bob_timeline_label, slash_knot)

    # THEN
    assert bob_rope
    time_rope = create_rope(fay_belief_label, "time", slash_knot)
    expected_bob_rope = create_rope(time_rope, bob_timeline_label, slash_knot)
    assert bob_rope == expected_bob_rope


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
    creg_config.pop(timeline_label_str())
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
    five_weekday_list = ["Anaday", "Baileyday", "Chiday", "Danceday", "Eastday"]
    # months = ["B", "C", "E", "G", "H", "I", "K", "L", "N", "P", "Q", "R", "T", "U", "W"]
    # c_mons = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    five_months_list = [
        "Fredrick",
        "Geo",
        "Holocene",
        "Iguana",
        "Jesus",
        "Keel",
        "LeBron",
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
        timeline_label=five_str(),
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
    assert five_dict.get(timeline_label_str()) == five_str()
    assert five_dict.get(c400_number_str()) == five_c400_number
    assert five_dict.get(weekdays_config_str()) == five_weekday_list
    x_months_config = five_dict.get(months_config_str())
    gen_months = [mon_config[0] for mon_config in x_months_config]
    assert gen_months == five_months_list
    assert x_months_config[0][0] == "Fredrick"
    assert x_months_config[0][1] == 25
    assert x_months_config[6][0] == "LeBron"
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
    expected_config = get_example_timeline_config(five_str())
    assert validate_timeline_config(expected_config)
    assert expected_config.get(hours_config_str()) == x_hours_config
    assert expected_config == five_dict


def test_timeline_config_shop_ReturnsObj_NoParameters():
    # ESTABLISH
    h_c400_number = 7
    h_hours_config = [
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
    h_timeline_label = "creg"
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
    print(f"{timeline_label_str()=}")
    print(f"{generated_dict.get(timeline_label_str())=}")
    assert generated_dict.get(c400_number_str()) == h_c400_number

    assert generated_dict.get(timeline_label_str()) == h_timeline_label
    assert generated_dict.get(c400_number_str()) == h_c400_number
    assert generated_dict.get(hours_config_str()) == h_hours_config
    assert generated_dict.get(months_config_str()) == h_months_config
    assert generated_dict.get(monthday_distortion_str()) == h_monthday_distortion
    assert generated_dict.get(timeline_label_str()) == h_timeline_label
    assert generated_dict.get(weekdays_config_str()) == h_weekdays_config
    assert generated_dict.get(yr1_jan1_offset_str()) == h_yr1_jan1_offset
    assert validate_timeline_config(generated_dict)


def test_get_year_rope_ReturnsObj():
    # ESTABLISH
    fay_str = "Fay34"
    sue_believerunit = believerunit_shop("Sue")
    time_rope = sue_believerunit.make_l1_rope(time_str())
    fay_rope = sue_believerunit.make_rope(time_rope, fay_str)
    c400_leap_rope = sue_believerunit.make_rope(fay_rope, c400_leap_str())
    c400_clean_rope = sue_believerunit.make_rope(c400_leap_rope, c400_clean_str())
    c100_rope = sue_believerunit.make_rope(c400_clean_rope, c100_str())
    yr4_leap_rope = sue_believerunit.make_rope(c100_rope, yr4_leap_str())
    yr4_clean_rope = sue_believerunit.make_rope(yr4_leap_rope, yr4_clean_str())
    year_rope = sue_believerunit.make_rope(yr4_clean_rope, year_str())

    # WHEN / THEN
    assert year_rope == get_year_rope(sue_believerunit, fay_rope)


def test_get_week_rope_ReturnsObj():
    # ESTABLISH
    fay_str = "Fay34"
    sue_believerunit = believerunit_shop("Sue")
    time_rope = sue_believerunit.make_l1_rope(time_str())
    fay_rope = sue_believerunit.make_rope(time_rope, fay_str)
    week_rope = sue_believerunit.make_rope(fay_rope, week_str())

    # WHEN / THEN
    assert week_rope == get_week_rope(sue_believerunit, fay_rope)


def test_get_day_rope_ReturnsObj():
    # ESTABLISH
    fay_str = "Fay34"
    sue_believerunit = believerunit_shop("Sue")
    time_rope = sue_believerunit.make_l1_rope(time_str())
    fay_rope = sue_believerunit.make_rope(time_rope, fay_str)
    day_rope = sue_believerunit.make_rope(fay_rope, day_str())

    # WHEN / THEN
    assert day_rope == get_day_rope(sue_believerunit, fay_rope)


def test_TimeLineUnit_Exists():
    # ESTABLISH / WHEN
    x_timelineunit = TimeLineUnit()

    # THEN
    assert x_timelineunit
    assert not x_timelineunit.c400_number
    assert not x_timelineunit.hours_config
    assert not x_timelineunit.months_config
    assert not x_timelineunit.monthday_distortion
    assert not x_timelineunit.timeline_label
    assert not x_timelineunit.weekdays_config
    assert not x_timelineunit.yr1_jan1_offset


def test_timelineunit_shop_ReturnsObj_Scenario0_Default():
    # ESTABLISH
    creg_config = get_creg_config()

    # WHEN
    x_timelineunit = timelineunit_shop()

    # THEN
    creg_c400_number = creg_config.get(c400_number_str())
    creg_hours_config = creg_config.get(hours_config_str())
    creg_months_config = creg_config.get(months_config_str())
    creg_timeline_label = creg_config.get(timeline_label_str())
    creg_weekdays_config = creg_config.get(weekdays_config_str())
    creg_monthday_distortion = creg_config.get(monthday_distortion_str())
    creg_yr1_jan1_offset = creg_config.get(yr1_jan1_offset_str())

    assert x_timelineunit
    assert x_timelineunit.c400_number == creg_c400_number
    assert x_timelineunit.hours_config == creg_hours_config
    assert x_timelineunit.months_config == creg_months_config
    assert x_timelineunit.monthday_distortion == creg_monthday_distortion
    assert x_timelineunit.timeline_label == creg_timeline_label
    assert x_timelineunit.weekdays_config == creg_weekdays_config
    assert x_timelineunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_timelineunit_shop_ReturnsObj_Scenario1_WhenTimeLineUnitAttributesAreNone():
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
    creg_timeline_label = creg_config.get(timeline_label_str())
    creg_weekdays_config = creg_config.get(weekdays_config_str())
    creg_monthday_distortion = creg_config.get(monthday_distortion_str())
    creg_yr1_jan1_offset = creg_config.get(yr1_jan1_offset_str())

    assert x_timelineunit
    assert x_timelineunit.c400_number == creg_c400_number
    assert x_timelineunit.hours_config == creg_hours_config
    assert x_timelineunit.months_config == creg_months_config
    assert x_timelineunit.monthday_distortion == creg_monthday_distortion
    assert x_timelineunit.timeline_label == creg_timeline_label
    assert x_timelineunit.weekdays_config == creg_weekdays_config
    assert x_timelineunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_timelineunit_shop_ReturnsObj_Scenario2_timeline_label_Missing():
    # ESTABLISH
    incomplete_creg_config = get_creg_config()
    incomplete_creg_config.pop(timeline_label_str())
    incomplete_creg_config.pop(hours_config_str())
    assert incomplete_creg_config

    # WHEN
    x_timelineunit = timelineunit_shop(incomplete_creg_config)

    # THEN
    creg_config = get_creg_config()
    creg_c400_number = creg_config.get(c400_number_str())
    creg_hours_config = creg_config.get(hours_config_str())
    creg_months_config = creg_config.get(months_config_str())
    creg_timeline_label = creg_config.get(timeline_label_str())
    creg_weekdays_config = creg_config.get(weekdays_config_str())
    creg_monthday_distortion = creg_config.get(monthday_distortion_str())
    creg_yr1_jan1_offset = creg_config.get(yr1_jan1_offset_str())

    assert x_timelineunit
    assert x_timelineunit.c400_number == creg_c400_number
    assert x_timelineunit.hours_config == creg_hours_config
    assert x_timelineunit.months_config == creg_months_config
    assert x_timelineunit.monthday_distortion == creg_monthday_distortion
    assert x_timelineunit.timeline_label == creg_timeline_label
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
