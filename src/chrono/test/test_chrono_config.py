from src._instrument.file import save_file
from src._instrument.python import get_json_from_dict
from src.chrono.examples.chrono_examples import (
    get_creg_config,
    get_squirt_config,
    chrono_examples_dir,
    get_example_timeline_config,
)
from src.chrono.chrono import (
    C400Standard,
    get_c400_standard,
    day_length,
    hours_config_text,
    weekdays_config_text,
    months_config_text,
    timeline_label_text,
    c400_config_text,
    yr1_jan1_offset_text,
    validate_timeline_config,
    create_timeline_config,
)
from copy import deepcopy as copy_deepcopy


def test_C400Standard_Exists():
    # ESTABLISH / WHEN
    x_c400_standard = C400Standard("x1", "x2", "x3", "x4", "x5", "x6", "x7")

    # THEN
    assert x_c400_standard.day_length == "x1"
    assert x_c400_standard.c400_leap_length == "x2"
    assert x_c400_standard.c400_clean_length == "x3"
    assert x_c400_standard.c100_length == "x4"
    assert x_c400_standard.yr4_leap_length == "x5"
    assert x_c400_standard.yr4_clean_length == "x6"
    assert x_c400_standard.year_length == "x7"


def test_get_c400_standards_ReturnsObj():
    # ESTABLISH / WHEN
    x_c400_standard = get_c400_standard()

    assert x_c400_standard.day_length == 1440
    assert x_c400_standard.c400_leap_length == 210379680
    assert x_c400_standard.c400_clean_length == 210378240
    assert x_c400_standard.c100_length == 52594560
    assert x_c400_standard.yr4_leap_length == 2103840
    assert x_c400_standard.yr4_clean_length == 2102400
    assert x_c400_standard.year_length == 525600


def test_day_length_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert day_length() == get_c400_standard().day_length
    assert day_length() == 1440


def test_is_timeline_config_valid_ReturnsObj_CheckElementsExist():
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
    creg_config.pop(hours_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(weekdays_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(months_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(timeline_label_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(c400_config_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(yr1_jan1_offset_text())
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[hours_config_text()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[months_config_text()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[weekdays_config_text()] = []
    assert not validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[yr1_jan1_offset_text()] = None
    assert not validate_timeline_config(creg_config)
    creg_config[yr1_jan1_offset_text()] = 0
    assert validate_timeline_config(creg_config)


def test_is_timeline_config_valid_ReturnsObj_CheckElementsRepeat():
    # ESTABLISH / WHEN / THEN
    orig_creg_config = get_creg_config()
    assert validate_timeline_config(orig_creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[months_config_text()] = [["x_str", 30], ["y_str", 180], ["x_str", 365]]
    assert not validate_timeline_config(creg_config)
    creg_config[months_config_text()] = [["x_str", 30], ["y_str", 180], ["z_str", 365]]
    assert validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[hours_config_text()] = [["x_str", 30], ["y_str", 180], ["x_str", 1440]]
    assert not validate_timeline_config(creg_config)
    creg_config[hours_config_text()] = [["x_str", 30], ["y_str", 180], ["z_str", 1440]]
    assert validate_timeline_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[weekdays_config_text()] = ["x_str", "y_str", "x_str"]
    assert not validate_timeline_config(creg_config)
    creg_config[weekdays_config_text()] = ["x_str", "y_str", "z_str"]
    assert validate_timeline_config(creg_config)


def test_create_timeline_config_ReturnsObj():
    # ESTABLISH
    cinco_text = "cinco"
    cinco_c400_count = 25
    cinco_yr1_jan1_offset = 2103796800  # 4000 years
    cinco_hour_length = 120
    cinco_month_length = 25
    cinco_weekday_list = ["Airday", "Bioday", "Chiday", "Danceday", "Ellday"]
    # months = ["B", "C", "E", "G", "H", "I", "K", "L", "N", "P", "Q", "R", "T", "U", "W"]
    # c_mons = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    cinco_months_list = [
        "Annita",
        "Bailey",
        "Cimon",
        "Dragon",
        "Elon",
        "Fresh",
        "Giraffe",
        "Holocene",
        "Iguana",
        "Journey",
        "Kayla",
        "Lebron",
        "Mikayla",
        "Ninon",
        "Obama",
    ]
    assert len(cinco_months_list) == 15
    calc_months_day_length = (len(cinco_months_list) - 1) * cinco_month_length
    assert calc_months_day_length == 350
    print(f"{len(cinco_months_list)=} {calc_months_day_length=}")

    # WHEN
    cinco_dict = create_timeline_config(
        timeline_label=cinco_text,
        c400_count=cinco_c400_count,
        hour_length=cinco_hour_length,
        month_length=cinco_month_length,
        weekday_list=cinco_weekday_list,
        months_list=cinco_months_list,
        yr1_jan1_offset=cinco_yr1_jan1_offset,
    )

    # THEN
    assert validate_timeline_config(cinco_dict)
    assert cinco_dict.get(timeline_label_text()) == cinco_text
    assert cinco_dict.get(c400_config_text()) == cinco_c400_count
    assert cinco_dict.get(weekdays_config_text()) == cinco_weekday_list
    x_months_config = cinco_dict.get(months_config_text())
    gen_months = [mon_config[0] for mon_config in x_months_config]
    assert gen_months == cinco_months_list
    assert x_months_config[0][0] == "Annita"
    assert x_months_config[0][1] == 25
    assert x_months_config[6][0] == "Giraffe"
    assert x_months_config[6][1] == 175
    assert x_months_config[13][0] == "Ninon"
    assert x_months_config[13][1] == 350
    assert x_months_config[14][0] == "Obama"
    assert x_months_config[14][1] == 365
    x_hours_config = cinco_dict.get(hours_config_text())
    assert len(x_hours_config) == 12
    assert x_hours_config[0] == ["0hr", 120]
    assert x_hours_config[4] == ["4hr", 600]
    assert cinco_dict.get(yr1_jan1_offset_text()) == cinco_yr1_jan1_offset

    cinco_file_name = f"timeline_config_{cinco_text}.json"
    cinco_file_text = get_json_from_dict(cinco_dict)
    save_file(chrono_examples_dir(), cinco_file_name, cinco_file_text)
    x_cinco_config = get_example_timeline_config(cinco_text)
    assert validate_timeline_config(x_cinco_config)
