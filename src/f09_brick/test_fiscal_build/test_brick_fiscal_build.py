from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_fiscal.fiscal import fiscalunit_shop
from src.f09_brick.examples.brick_env import brick_fiscals_dir, brick_env_setup_cleanup
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
from src.f09_brick.brick import fiscal_build_from_df


# given a dataframe, build a fiscal unit
def test_fiscal_build_from_df_ReturnsObj_Scenario0_OneFiscalID(brick_env_setup_cleanup):
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
    x_fiscals_dir = f"{brick_fiscals_dir()}/fizz"
    music23_str = "music23"
    slash_text = "/"

    # WHEN
    x_fiscalunits = fiscal_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscals_dir,
    )

    # THEN
    assert x_fiscalunits
    assert x_fiscalunits.get(music23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    music23_fiscalunit = fiscalunit_shop(
        current_time=5500,
        fiscal_id=music23_str,
        fiscals_dir=x_fiscals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        road_delimiter=slash_text,
        timeline=creg_timelineunit,
    )
    music23_fiscalunit.add_purviewepisode(
        x_owner_id="Sue",
        x_time_id=777,
        x_money_magnitude=445,
        allow_prev_to_current_time_entry=True,
    )
    music23_fiscalunit.add_cashpurchase(
        x_owner_id="Zia",
        x_acct_id="Bob",
        x_time_id=777,
        x_amount=888,
    )
    gen_fiscalunit = x_fiscalunits.get(music23_str)
    assert gen_fiscalunit.fund_coin == x_fund_coin
    assert gen_fiscalunit.respect_bit == x_respect_bit
    assert gen_fiscalunit.penny == x_penny
    assert gen_fiscalunit.fiscal_id == music23_str
    assert gen_fiscalunit.fiscals_dir == x_fiscals_dir
    assert gen_fiscalunit.timeline == music23_fiscalunit.timeline
    assert gen_fiscalunit.purviewlogs == music23_fiscalunit.purviewlogs
    assert gen_fiscalunit.cashbook.tranunits == music23_fiscalunit.cashbook.tranunits
    print(f"{gen_fiscalunit.purviewlogs=}")
    assert len(gen_fiscalunit.purviewlogs) == 1
    assert len(gen_fiscalunit.cashbook.tranunits) == 1
    assert gen_fiscalunit == music23_fiscalunit


# given a dataframe, build a fiscal unit
def test_fiscal_build_from_df_ReturnsObj_Scenario1_TwoFiscalIDs(
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
    x_fiscals_dir = f"{brick_fiscals_dir()}/fizz"
    music23_str = "music23"
    slash_text = "/"

    # WHEN
    x_fiscalunits = fiscal_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscals_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    music23_fiscalunit = fiscalunit_shop(
        current_time=5500,
        fiscal_id=music23_str,
        fiscals_dir=x_fiscals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        road_delimiter=slash_text,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_fiscalunit = fiscalunit_shop(
        current_time=444,
        fiscal_id="jeffy45",
        fiscals_dir=x_fiscals_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        road_delimiter=",",
        timeline=five_timelineunit,
    )
    assert x_fiscalunits
    assert x_fiscalunits.get(music23_str) != None
    creg_fiscalunit = x_fiscalunits.get(music23_str)
    assert creg_fiscalunit.fund_coin == x_fund_coin
    assert creg_fiscalunit.respect_bit == x_respect_bit
    assert creg_fiscalunit.penny == x_penny
    assert creg_fiscalunit.fiscal_id == music23_str
    assert creg_fiscalunit.fiscals_dir == x_fiscals_dir
    assert creg_fiscalunit.timeline == music23_fiscalunit.timeline
    assert len(creg_fiscalunit.purviewlogs) == 3
    assert len(creg_fiscalunit.cashbook.tranunits) == 4
    # assert creg_fiscalunit == music23_fiscalunit

    five_fiscalunit = x_fiscalunits.get("jeffy45")
    assert five_fiscalunit.fund_coin == x_fund_coin
    assert five_fiscalunit.respect_bit == x_respect_bit
    assert five_fiscalunit.penny == x_penny
    assert five_fiscalunit.fiscal_id == "jeffy45"
    assert five_fiscalunit.fiscals_dir == x_fiscals_dir
    assert len(five_fiscalunit.purviewlogs) == 2
    assert len(five_fiscalunit.cashbook.tranunits) == 1
    jeffy45_timeline = jeffy45_fiscalunit.timeline
    assert five_fiscalunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_fiscalunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_fiscalunit.timeline == jeffy45_timeline
    # assert five_fiscalunit == jeffy45_fiscalunit


# # given a dataframe, build a fiscal unit
# def test_fiscal_build_from_df_ReturnsObj_Scenario2_IncludeCashBook(
#     brick_env_setup_cleanup,
# ):
#     # ESTABLISH
#     br00000_df = get_ex2_br00000_df()
#     br00001_df = get_ex2_br00001_df()
#     br00002_df = get_ex2_br00002_df()
#     br00003_df = get_ex2_br00003_df()
#     br00004_df = get_ex2_br00004_df()
#     br00005_df = get_ex2_br00005_df()
#     x_fund_coin = 55
#     x_respect_bit = 66
#     x_penny = 77
#     x_fiscals_dir = f"{brick_fiscals_dir()}/fizz"
#     music23_str = "music23"
#     slash_text = "/"

#     # WHEN
#     x_fiscalunits = fiscal_build_from_df(
#         br00000_df,
#         br00001_df,
#         br00002_df,
#         br00003_df,
#         br00004_df,
#         br00005_df,
#         x_fund_coin,
#         x_respect_bit,
#         x_penny,
#         x_fiscals_dir,
#         slash_text,
#     )

#     # THEN
#     creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
#     music23_fiscalunit = fiscalunit_shop(
#         current_time=5500,
#         fiscal_id=music23_str,
#         fiscals_dir=x_fiscals_dir,
#         fund_coin=x_fund_coin,
#         penny=x_penny,
#         respect_bit=x_respect_bit,
#         road_delimiter=slash_text,
#         timeline=creg_timelineunit,
#     )
#     five_timelineunit = timelineunit_shop(get_five_config())
#     jeffy45_fiscalunit = fiscalunit_shop(
#         current_time=444,
#         fiscal_id="jeffy45",
#         fiscals_dir=x_fiscals_dir,
#         fund_coin=x_fund_coin,
#         penny=x_penny,
#         respect_bit=x_respect_bit,
#         road_delimiter=",",
#         timeline=five_timelineunit,
#     )
#     assert x_fiscalunits
#     assert x_fiscalunits.get(music23_str) != None
#     creg_fiscalunit = x_fiscalunits.get(music23_str)
#     assert creg_fiscalunit.fund_coin == x_fund_coin
#     assert creg_fiscalunit.respect_bit == x_respect_bit
#     assert creg_fiscalunit.penny == x_penny
#     assert creg_fiscalunit.fiscal_id == music23_str
#     assert creg_fiscalunit.fiscals_dir == x_fiscals_dir
#     assert creg_fiscalunit.timeline == music23_fiscalunit.timeline
#     assert creg_fiscalunit == music23_fiscalunit
#     five_fiscalunit = x_fiscalunits.get("jeffy45")
#     assert five_fiscalunit.fund_coin == x_fund_coin
#     assert five_fiscalunit.respect_bit == x_respect_bit
#     assert five_fiscalunit.penny == x_penny
#     assert five_fiscalunit.fiscal_id == "jeffy45"
#     assert five_fiscalunit.fiscals_dir == x_fiscals_dir
#     jeffy45_timeline = jeffy45_fiscalunit.timeline
#     assert five_fiscalunit.timeline.hours_config == jeffy45_timeline.hours_config
#     assert five_fiscalunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
#     assert five_fiscalunit.timeline == jeffy45_timeline
#     assert five_fiscalunit == jeffy45_fiscalunit
