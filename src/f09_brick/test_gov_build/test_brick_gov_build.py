from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_gov.gov import govunit_shop
from src.f09_brick.examples.brick_env import brick_govs_dir, brick_env_setup_cleanup
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
from src.f09_brick.brick import gov_build_from_df


# given a dataframe, build a gov unit
def test_gov_build_from_df_ReturnsObj_Scenario0_OneGovIdea(brick_env_setup_cleanup):
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
    x_govs_dir = f"{brick_govs_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_govunits = gov_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_govs_dir,
    )

    # THEN
    assert x_govunits
    assert x_govunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_govunit = govunit_shop(
        current_time=5500,
        gov_idea=accord23_str,
        govs_dir=x_govs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    accord23_govunit.add_dealepisode(
        x_owner_name="Sue",
        x_time_int=777,
        x_money_magnitude=445,
        allow_prev_to_current_time_entry=True,
    )
    accord23_govunit.add_cashpurchase(
        x_owner_name="Zia",
        x_acct_name="Bob",
        x_time_int=777,
        x_amount=888,
    )
    gen_govunit = x_govunits.get(accord23_str)
    assert gen_govunit.fund_coin == x_fund_coin
    assert gen_govunit.respect_bit == x_respect_bit
    assert gen_govunit.penny == x_penny
    assert gen_govunit.gov_idea == accord23_str
    assert gen_govunit.govs_dir == x_govs_dir
    assert gen_govunit.timeline == accord23_govunit.timeline
    assert gen_govunit.deallogs == accord23_govunit.deallogs
    assert gen_govunit.cashbook.tranunits == accord23_govunit.cashbook.tranunits
    print(f"{gen_govunit.deallogs=}")
    assert len(gen_govunit.deallogs) == 1
    assert len(gen_govunit.cashbook.tranunits) == 1
    assert gen_govunit == accord23_govunit


# given a dataframe, build a gov unit
def test_gov_build_from_df_ReturnsObj_Scenario1_TwoGovIdeas(
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
    x_govs_dir = f"{brick_govs_dir()}/fizz"
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_govunits = gov_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_govs_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_govunit = govunit_shop(
        current_time=5500,
        gov_idea=accord23_str,
        govs_dir=x_govs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_govunit = govunit_shop(
        current_time=444,
        gov_idea="jeffy45",
        govs_dir=x_govs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=",",
        timeline=five_timelineunit,
    )
    assert x_govunits
    assert x_govunits.get(accord23_str) != None
    creg_govunit = x_govunits.get(accord23_str)
    assert creg_govunit.fund_coin == x_fund_coin
    assert creg_govunit.respect_bit == x_respect_bit
    assert creg_govunit.penny == x_penny
    assert creg_govunit.gov_idea == accord23_str
    assert creg_govunit.govs_dir == x_govs_dir
    assert creg_govunit.timeline == accord23_govunit.timeline
    assert len(creg_govunit.deallogs) == 3
    assert len(creg_govunit.cashbook.tranunits) == 4
    # assert creg_govunit == accord23_govunit

    five_govunit = x_govunits.get("jeffy45")
    assert five_govunit.fund_coin == x_fund_coin
    assert five_govunit.respect_bit == x_respect_bit
    assert five_govunit.penny == x_penny
    assert five_govunit.gov_idea == "jeffy45"
    assert five_govunit.govs_dir == x_govs_dir
    assert len(five_govunit.deallogs) == 2
    assert len(five_govunit.cashbook.tranunits) == 1
    jeffy45_timeline = jeffy45_govunit.timeline
    assert five_govunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_govunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_govunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_govunit.timeline == jeffy45_timeline
    # assert five_govunit == jeffy45_govunit
