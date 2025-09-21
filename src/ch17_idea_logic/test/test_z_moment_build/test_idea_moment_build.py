from src.a00_data_toolbox.file_toolbox import create_path
from src.a07_timeline_logic.test._util.calendar_examples import get_five_config
from src.a07_timeline_logic.timeline_main import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch17_idea_logic.idea_main import moment_build_from_df
from src.ch17_idea_logic.test._util.ch17_env import (
    env_dir_setup_cleanup,
    idea_moments_dir,
)
from src.ch17_idea_logic.test._util.idea_df_examples import (
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


# ESTABLISH a dataframe, build a moment unit
def test_moment_build_from_df_ReturnsObj_Scenario0_OneMomentLabel(
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
    x_moments_dir = create_path(idea_moments_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_momentunits = moment_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_moments_dir,
    )

    # THEN
    assert x_momentunits
    assert x_momentunits.get(amy23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    expected_amy23_momentunit = momentunit_shop(
        moment_label=amy23_str,
        moment_mstr_dir=x_moments_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_amy23_momentunit.add_budunit(
        belief_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_amy23_momentunit.add_paypurchase(
        belief_name="Zia",
        voice_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_momentunit = x_momentunits.get(amy23_str)
    assert gen_momentunit.fund_iota == x_fund_iota
    assert gen_momentunit.respect_bit == x_respect_bit
    assert gen_momentunit.penny == x_penny
    assert gen_momentunit.moment_label == amy23_str
    assert gen_momentunit.moment_mstr_dir == x_moments_dir
    assert gen_momentunit.timeline == expected_amy23_momentunit.timeline
    assert gen_momentunit.brokerunits == expected_amy23_momentunit.brokerunits
    a23_tranunits = expected_amy23_momentunit.paybook.tranunits
    assert gen_momentunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_momentunit.brokerunits=}")
    assert len(gen_momentunit.brokerunits) == 1
    assert len(gen_momentunit.paybook.tranunits) == 1
    assert gen_momentunit == expected_amy23_momentunit


# ESTABLISH a dataframe, build a moment unit
def test_moment_build_from_df_ReturnsObj_Scenario1_TwoMomentLabels(
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
    x_moments_dir = create_path(idea_moments_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_momentunits = moment_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_moments_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    amy23_momentunit = momentunit_shop(
        moment_label=amy23_str,
        moment_mstr_dir=x_moments_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_momentunit = momentunit_shop(
        moment_label="jeffy45",
        moment_mstr_dir=x_moments_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=",",
        timeline=five_timelineunit,
    )
    assert x_momentunits
    assert x_momentunits.get(amy23_str) != None
    creg_momentunit = x_momentunits.get(amy23_str)
    assert creg_momentunit.fund_iota == x_fund_iota
    assert creg_momentunit.respect_bit == x_respect_bit
    assert creg_momentunit.penny == x_penny
    assert creg_momentunit.moment_label == amy23_str
    assert creg_momentunit.moment_mstr_dir == x_moments_dir
    assert creg_momentunit.timeline == amy23_momentunit.timeline
    assert len(creg_momentunit.brokerunits) == 3
    assert len(creg_momentunit.paybook.tranunits) == 4
    # assert creg_momentunit == amy23_momentunit

    five_momentunit = x_momentunits.get("jeffy45")
    assert five_momentunit.fund_iota == x_fund_iota
    assert five_momentunit.respect_bit == x_respect_bit
    assert five_momentunit.penny == x_penny
    assert five_momentunit.moment_label == "jeffy45"
    assert five_momentunit.moment_mstr_dir == x_moments_dir
    assert len(five_momentunit.brokerunits) == 2
    assert len(five_momentunit.paybook.tranunits) == 1
    jeffy45_timeline = jeffy45_momentunit.timeline
    assert five_momentunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_momentunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_momentunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_momentunit.timeline == jeffy45_timeline
    # assert five_momentunit == jeffy45_momentunit
