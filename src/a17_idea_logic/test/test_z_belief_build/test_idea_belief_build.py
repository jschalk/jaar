from src.a00_data_toolbox.file_toolbox import create_path
from src.a07_timeline_logic.test._util.calendar_examples import get_five_config
from src.a07_timeline_logic.timeline_main import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a15_belief_logic.belief_main import beliefunit_shop
from src.a17_idea_logic.idea_main import belief_build_from_df
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    idea_beliefs_dir,
)
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


# ESTABLISH a dataframe, build a belief unit
def test_belief_build_from_df_ReturnsObj_Scenario0_OneBeliefLabel(
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
    x_beliefs_dir = create_path(idea_beliefs_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_beliefunits = belief_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_beliefs_dir,
    )

    # THEN
    assert x_beliefunits
    assert x_beliefunits.get(amy23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    expected_amy23_beliefunit = beliefunit_shop(
        belief_label=amy23_str,
        belief_mstr_dir=x_beliefs_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_amy23_beliefunit.add_budunit(
        believer_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_amy23_beliefunit.add_paypurchase(
        believer_name="Zia",
        partner_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_beliefunit = x_beliefunits.get(amy23_str)
    assert gen_beliefunit.fund_iota == x_fund_iota
    assert gen_beliefunit.respect_bit == x_respect_bit
    assert gen_beliefunit.penny == x_penny
    assert gen_beliefunit.belief_label == amy23_str
    assert gen_beliefunit.belief_mstr_dir == x_beliefs_dir
    assert gen_beliefunit.timeline == expected_amy23_beliefunit.timeline
    assert gen_beliefunit.brokerunits == expected_amy23_beliefunit.brokerunits
    a23_tranunits = expected_amy23_beliefunit.paybook.tranunits
    assert gen_beliefunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_beliefunit.brokerunits=}")
    assert len(gen_beliefunit.brokerunits) == 1
    assert len(gen_beliefunit.paybook.tranunits) == 1
    assert gen_beliefunit == expected_amy23_beliefunit


# ESTABLISH a dataframe, build a belief unit
def test_belief_build_from_df_ReturnsObj_Scenario1_TwoBeliefLabels(
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
    x_beliefs_dir = create_path(idea_beliefs_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_beliefunits = belief_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_beliefs_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    amy23_beliefunit = beliefunit_shop(
        belief_label=amy23_str,
        belief_mstr_dir=x_beliefs_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_beliefunit = beliefunit_shop(
        belief_label="jeffy45",
        belief_mstr_dir=x_beliefs_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=",",
        timeline=five_timelineunit,
    )
    assert x_beliefunits
    assert x_beliefunits.get(amy23_str) != None
    creg_beliefunit = x_beliefunits.get(amy23_str)
    assert creg_beliefunit.fund_iota == x_fund_iota
    assert creg_beliefunit.respect_bit == x_respect_bit
    assert creg_beliefunit.penny == x_penny
    assert creg_beliefunit.belief_label == amy23_str
    assert creg_beliefunit.belief_mstr_dir == x_beliefs_dir
    assert creg_beliefunit.timeline == amy23_beliefunit.timeline
    assert len(creg_beliefunit.brokerunits) == 3
    assert len(creg_beliefunit.paybook.tranunits) == 4
    # assert creg_beliefunit == amy23_beliefunit

    five_beliefunit = x_beliefunits.get("jeffy45")
    assert five_beliefunit.fund_iota == x_fund_iota
    assert five_beliefunit.respect_bit == x_respect_bit
    assert five_beliefunit.penny == x_penny
    assert five_beliefunit.belief_label == "jeffy45"
    assert five_beliefunit.belief_mstr_dir == x_beliefs_dir
    assert len(five_beliefunit.brokerunits) == 2
    assert len(five_beliefunit.paybook.tranunits) == 1
    jeffy45_timeline = jeffy45_beliefunit.timeline
    assert five_beliefunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_beliefunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_beliefunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_beliefunit.timeline == jeffy45_timeline
    # assert five_beliefunit == jeffy45_beliefunit
