from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_cmty.cmty import cmtyunit_shop
from src.f09_brick.examples.brick_env import brick_cmtys_dir, brick_env_setup_cleanup
from src.f09_brick.examples.brick_df_examples import (
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
from src.f09_brick.brick import cmty_build_from_df


# given a dataframe, build a cmty unit
def test_cmty_build_from_df_ReturnsObj_Scenario0_OneCmtyTitle(brick_env_setup_cleanup):
    # ESTABLISH
    br00000_df = get_ex1_br00000_df()
    br00001_df = get_ex1_br00001_df()
    br00002_df = get_ex1_br00002_df()
    br00003_df = get_ex1_br00003_df()
    br00004_df = get_ex1_br00004_df()
    br00005_df = get_ex1_br00005_df()
    x_fund_coin = 55
    x_respect_bit = 66
    x_penny = 77
    x_cmtys_dir = f"{brick_cmtys_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_cmtyunits = cmty_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_cmtys_dir,
    )

    # THEN
    assert x_cmtyunits
    assert x_cmtyunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_cmtyunit = cmtyunit_shop(
        current_time=5500,
        cmty_title=accord23_str,
        cmtys_dir=x_cmtys_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    accord23_cmtyunit.add_dealepisode(
        x_owner_name="Sue",
        x_time_int=777,
        x_money_magnitude=445,
        allow_prev_to_current_time_entry=True,
    )
    accord23_cmtyunit.add_cashpurchase(
        x_owner_name="Zia",
        x_acct_name="Bob",
        x_time_int=777,
        x_amount=888,
    )
    gen_cmtyunit = x_cmtyunits.get(accord23_str)
    assert gen_cmtyunit.fund_coin == x_fund_coin
    assert gen_cmtyunit.respect_bit == x_respect_bit
    assert gen_cmtyunit.penny == x_penny
    assert gen_cmtyunit.cmty_title == accord23_str
    assert gen_cmtyunit.cmtys_dir == x_cmtys_dir
    assert gen_cmtyunit.timeline == accord23_cmtyunit.timeline
    assert gen_cmtyunit.deallogs == accord23_cmtyunit.deallogs
    assert gen_cmtyunit.cashbook.tranunits == accord23_cmtyunit.cashbook.tranunits
    print(f"{gen_cmtyunit.deallogs=}")
    assert len(gen_cmtyunit.deallogs) == 1
    assert len(gen_cmtyunit.cashbook.tranunits) == 1
    assert gen_cmtyunit == accord23_cmtyunit


# given a dataframe, build a cmty unit
def test_cmty_build_from_df_ReturnsObj_Scenario1_TwoCmtyTitles(
    brick_env_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_coin = 55
    x_respect_bit = 66
    x_penny = 77
    x_cmtys_dir = f"{brick_cmtys_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_cmtyunits = cmty_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_cmtys_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_cmtyunit = cmtyunit_shop(
        current_time=5500,
        cmty_title=accord23_str,
        cmtys_dir=x_cmtys_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_cmtyunit = cmtyunit_shop(
        current_time=444,
        cmty_title="jeffy45",
        cmtys_dir=x_cmtys_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=",",
        timeline=five_timelineunit,
    )
    assert x_cmtyunits
    assert x_cmtyunits.get(accord23_str) != None
    creg_cmtyunit = x_cmtyunits.get(accord23_str)
    assert creg_cmtyunit.fund_coin == x_fund_coin
    assert creg_cmtyunit.respect_bit == x_respect_bit
    assert creg_cmtyunit.penny == x_penny
    assert creg_cmtyunit.cmty_title == accord23_str
    assert creg_cmtyunit.cmtys_dir == x_cmtys_dir
    assert creg_cmtyunit.timeline == accord23_cmtyunit.timeline
    assert len(creg_cmtyunit.deallogs) == 3
    assert len(creg_cmtyunit.cashbook.tranunits) == 4
    # assert creg_cmtyunit == accord23_cmtyunit

    five_cmtyunit = x_cmtyunits.get("jeffy45")
    assert five_cmtyunit.fund_coin == x_fund_coin
    assert five_cmtyunit.respect_bit == x_respect_bit
    assert five_cmtyunit.penny == x_penny
    assert five_cmtyunit.cmty_title == "jeffy45"
    assert five_cmtyunit.cmtys_dir == x_cmtys_dir
    assert len(five_cmtyunit.deallogs) == 2
    assert len(five_cmtyunit.cashbook.tranunits) == 1
    jeffy45_timeline = jeffy45_cmtyunit.timeline
    assert five_cmtyunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_cmtyunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_cmtyunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_cmtyunit.timeline == jeffy45_timeline
    # assert five_cmtyunit == jeffy45_cmtyunit
