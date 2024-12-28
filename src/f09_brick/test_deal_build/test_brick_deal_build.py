from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_deal.deal import dealunit_shop
from src.f09_brick.examples.brick_env import brick_deals_dir, brick_env_setup_cleanup
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
from src.f09_brick.brick import deal_build_from_df


# given a dataframe, build a deal unit
def test_deal_build_from_df_ReturnsObj_Scenario0_OneDealID(brick_env_setup_cleanup):
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
    x_deals_dir = f"{brick_deals_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_dealunits = deal_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_deals_dir,
    )

    # THEN
    assert x_dealunits
    assert x_dealunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_dealunit = dealunit_shop(
        current_time=5500,
        deal_id=accord23_str,
        deals_dir=x_deals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    accord23_dealunit.add_purviewepisode(
        x_owner_id="Sue",
        x_time_int=777,
        x_money_magnitude=445,
        allow_prev_to_current_time_entry=True,
    )
    accord23_dealunit.add_cashpurchase(
        x_owner_id="Zia",
        x_acct_id="Bob",
        x_time_int=777,
        x_amount=888,
    )
    gen_dealunit = x_dealunits.get(accord23_str)
    assert gen_dealunit.fund_coin == x_fund_coin
    assert gen_dealunit.respect_bit == x_respect_bit
    assert gen_dealunit.penny == x_penny
    assert gen_dealunit.deal_id == accord23_str
    assert gen_dealunit.deals_dir == x_deals_dir
    assert gen_dealunit.timeline == accord23_dealunit.timeline
    assert gen_dealunit.purviewlogs == accord23_dealunit.purviewlogs
    assert gen_dealunit.cashbook.tranunits == accord23_dealunit.cashbook.tranunits
    print(f"{gen_dealunit.purviewlogs=}")
    assert len(gen_dealunit.purviewlogs) == 1
    assert len(gen_dealunit.cashbook.tranunits) == 1
    assert gen_dealunit == accord23_dealunit


# given a dataframe, build a deal unit
def test_deal_build_from_df_ReturnsObj_Scenario1_TwoDealIDs(
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
    x_deals_dir = f"{brick_deals_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_dealunits = deal_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_deals_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_dealunit = dealunit_shop(
        current_time=5500,
        deal_id=accord23_str,
        deals_dir=x_deals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_dealunit = dealunit_shop(
        current_time=444,
        deal_id="jeffy45",
        deals_dir=x_deals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=",",
        timeline=five_timelineunit,
    )
    assert x_dealunits
    assert x_dealunits.get(accord23_str) != None
    creg_dealunit = x_dealunits.get(accord23_str)
    assert creg_dealunit.fund_coin == x_fund_coin
    assert creg_dealunit.respect_bit == x_respect_bit
    assert creg_dealunit.penny == x_penny
    assert creg_dealunit.deal_id == accord23_str
    assert creg_dealunit.deals_dir == x_deals_dir
    assert creg_dealunit.timeline == accord23_dealunit.timeline
    assert len(creg_dealunit.purviewlogs) == 3
    assert len(creg_dealunit.cashbook.tranunits) == 4
    # assert creg_dealunit == accord23_dealunit

    five_dealunit = x_dealunits.get("jeffy45")
    assert five_dealunit.fund_coin == x_fund_coin
    assert five_dealunit.respect_bit == x_respect_bit
    assert five_dealunit.penny == x_penny
    assert five_dealunit.deal_id == "jeffy45"
    assert five_dealunit.deals_dir == x_deals_dir
    assert len(five_dealunit.purviewlogs) == 2
    assert len(five_dealunit.cashbook.tranunits) == 1
    jeffy45_timeline = jeffy45_dealunit.timeline
    assert five_dealunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_dealunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_dealunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_dealunit.timeline == jeffy45_timeline
    # assert five_dealunit == jeffy45_dealunit
