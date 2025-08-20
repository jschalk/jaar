from src.a00_data_toolbox.file_toolbox import create_path
from src.a07_timeline_logic.test._util.calendar_examples import get_five_config
from src.a07_timeline_logic.timeline_main import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a15_coin_logic.coin_main import coinunit_shop
from src.a17_idea_logic.idea_main import coin_build_from_df
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup, idea_coins_dir
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


# ESTABLISH a dataframe, build a coin unit
def test_coin_build_from_df_ReturnsObj_Scenario0_OneCoinLabel(
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
    x_coins_dir = create_path(idea_coins_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_coinunits = coin_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_coins_dir,
    )

    # THEN
    assert x_coinunits
    assert x_coinunits.get(amy23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    expected_amy23_coinunit = coinunit_shop(
        coin_label=amy23_str,
        coin_mstr_dir=x_coins_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_amy23_coinunit.add_budunit(
        belief_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_amy23_coinunit.add_paypurchase(
        belief_name="Zia",
        partner_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_coinunit = x_coinunits.get(amy23_str)
    assert gen_coinunit.fund_iota == x_fund_iota
    assert gen_coinunit.respect_bit == x_respect_bit
    assert gen_coinunit.penny == x_penny
    assert gen_coinunit.coin_label == amy23_str
    assert gen_coinunit.coin_mstr_dir == x_coins_dir
    assert gen_coinunit.timeline == expected_amy23_coinunit.timeline
    assert gen_coinunit.brokerunits == expected_amy23_coinunit.brokerunits
    a23_tranunits = expected_amy23_coinunit.paybook.tranunits
    assert gen_coinunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_coinunit.brokerunits=}")
    assert len(gen_coinunit.brokerunits) == 1
    assert len(gen_coinunit.paybook.tranunits) == 1
    assert gen_coinunit == expected_amy23_coinunit


# ESTABLISH a dataframe, build a coin unit
def test_coin_build_from_df_ReturnsObj_Scenario1_TwoCoinLabels(
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
    x_coins_dir = create_path(idea_coins_dir(), "Fay")
    amy23_str = "amy23"
    slash_str = "/"

    # WHEN
    x_coinunits = coin_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_coins_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    amy23_coinunit = coinunit_shop(
        coin_label=amy23_str,
        coin_mstr_dir=x_coins_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_coinunit = coinunit_shop(
        coin_label="jeffy45",
        coin_mstr_dir=x_coins_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=",",
        timeline=five_timelineunit,
    )
    assert x_coinunits
    assert x_coinunits.get(amy23_str) != None
    creg_coinunit = x_coinunits.get(amy23_str)
    assert creg_coinunit.fund_iota == x_fund_iota
    assert creg_coinunit.respect_bit == x_respect_bit
    assert creg_coinunit.penny == x_penny
    assert creg_coinunit.coin_label == amy23_str
    assert creg_coinunit.coin_mstr_dir == x_coins_dir
    assert creg_coinunit.timeline == amy23_coinunit.timeline
    assert len(creg_coinunit.brokerunits) == 3
    assert len(creg_coinunit.paybook.tranunits) == 4
    # assert creg_coinunit == amy23_coinunit

    five_coinunit = x_coinunits.get("jeffy45")
    assert five_coinunit.fund_iota == x_fund_iota
    assert five_coinunit.respect_bit == x_respect_bit
    assert five_coinunit.penny == x_penny
    assert five_coinunit.coin_label == "jeffy45"
    assert five_coinunit.coin_mstr_dir == x_coins_dir
    assert len(five_coinunit.brokerunits) == 2
    assert len(five_coinunit.paybook.tranunits) == 1
    jeffy45_timeline = jeffy45_coinunit.timeline
    assert five_coinunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_coinunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_coinunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_coinunit.timeline == jeffy45_timeline
    # assert five_coinunit == jeffy45_coinunit
