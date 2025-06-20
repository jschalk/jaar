from src.a00_data_toolbox.file_toolbox import create_path
from src.a07_calendar_logic.chrono import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a07_calendar_logic.test._util.calendar_examples import get_five_config
from src.a15_vow_logic.vow import vowunit_shop
from src.a17_idea_logic.idea import vow_build_from_df
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup, idea_vows_dir
from src.a17_idea_logic.test._util.idea_df_examples import (
    get_ex1_br00000_df,
    get_ex1_br00001_df,
    get_ex1_br00002_df,
    get_ex1_br00003_df,
    get_ex1_br00004_df,
    get_ex1_br00005_df,
    get_ex2_br00000_df,
    get_ex2_br00001_df,
    get_ex2_br00002_df,
    get_ex2_br00003_df,
    get_ex2_br00004_df,
    get_ex2_br00005_df,
)


# ESTABLISH a dataframe, build a vow unit
def test_vow_build_from_df_ReturnsObj_Scenario0_OneVowLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex1_br00000_df()
    br00001_df = get_ex1_br00001_df()
    br00002_df = get_ex1_br00002_df()
    br00003_df = get_ex1_br00003_df()
    br00004_df = get_ex1_br00004_df()
    br00005_df = get_ex1_br00005_df()
    x_fund_iota = 55
    x_respect_bit = 66
    x_penny = 77
    x_job_listen_rotations = 7
    x_vows_dir = create_path(idea_vows_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_vowunits = vow_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_vows_dir,
    )

    # THEN
    assert x_vowunits
    assert x_vowunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    expected_accord23_vowunit = vowunit_shop(
        vow_label=accord23_str,
        vow_mstr_dir=x_vows_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_accord23_vowunit.add_budunit(
        owner_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_accord23_vowunit.add_paypurchase(
        owner_name="Zia",
        acct_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_vowunit = x_vowunits.get(accord23_str)
    assert gen_vowunit.fund_iota == x_fund_iota
    assert gen_vowunit.respect_bit == x_respect_bit
    assert gen_vowunit.penny == x_penny
    assert gen_vowunit.vow_label == accord23_str
    assert gen_vowunit.vow_mstr_dir == x_vows_dir
    assert gen_vowunit.timeline == expected_accord23_vowunit.timeline
    assert gen_vowunit.brokerunits == expected_accord23_vowunit.brokerunits
    a23_tranunits = expected_accord23_vowunit.paybook.tranunits
    assert gen_vowunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_vowunit.brokerunits=}")
    assert len(gen_vowunit.brokerunits) == 1
    assert len(gen_vowunit.paybook.tranunits) == 1
    assert gen_vowunit == expected_accord23_vowunit


# ESTABLISH a dataframe, build a vow unit
def test_vow_build_from_df_ReturnsObj_Scenario1_TwoVowLabels(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_iota = 55
    x_respect_bit = 66
    x_penny = 77
    x_vows_dir = create_path(idea_vows_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_vowunits = vow_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_vows_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_vowunit = vowunit_shop(
        vow_label=accord23_str,
        vow_mstr_dir=x_vows_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_vowunit = vowunit_shop(
        vow_label="jeffy45",
        vow_mstr_dir=x_vows_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=",",
        timeline=five_timelineunit,
    )
    assert x_vowunits
    assert x_vowunits.get(accord23_str) != None
    creg_vowunit = x_vowunits.get(accord23_str)
    assert creg_vowunit.fund_iota == x_fund_iota
    assert creg_vowunit.respect_bit == x_respect_bit
    assert creg_vowunit.penny == x_penny
    assert creg_vowunit.vow_label == accord23_str
    assert creg_vowunit.vow_mstr_dir == x_vows_dir
    assert creg_vowunit.timeline == accord23_vowunit.timeline
    assert len(creg_vowunit.brokerunits) == 3
    assert len(creg_vowunit.paybook.tranunits) == 4
    # assert creg_vowunit == accord23_vowunit

    five_vowunit = x_vowunits.get("jeffy45")
    assert five_vowunit.fund_iota == x_fund_iota
    assert five_vowunit.respect_bit == x_respect_bit
    assert five_vowunit.penny == x_penny
    assert five_vowunit.vow_label == "jeffy45"
    assert five_vowunit.vow_mstr_dir == x_vows_dir
    assert len(five_vowunit.brokerunits) == 2
    assert len(five_vowunit.paybook.tranunits) == 1
    jeffy45_timeline = jeffy45_vowunit.timeline
    assert five_vowunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_vowunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_vowunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_vowunit.timeline == jeffy45_timeline
    # assert five_vowunit == jeffy45_vowunit
