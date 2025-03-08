from src.f00_instrument.file import create_path
from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_fisc.fisc import fiscunit_shop
from src.f09_idea.idea import fisc_build_from_df, create_idea_brick_csvs_from_fisc_objs
from src.f09_idea.idea_db_tool import get_ordered_csv
from src.f09_idea.examples.idea_env import idea_fiscs_dir, idea_env_setup_cleanup
from src.f09_idea.examples.idea_df_examples import (
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


# given a dataframe, build a fisc unit
def test_fisc_build_from_df_ReturnsObj_Scenario0_OneFiscTitle(
    idea_env_setup_cleanup,
):
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
    x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_fiscunits = fisc_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
    )

    # THEN
    assert x_fiscunits
    assert x_fiscunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_fiscunit = fiscunit_shop(
        present_time=5500,
        fisc_title=accord23_str,
        fisc_mstr_dir=x_fiscs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    accord23_fiscunit.add_dealunit(
        owner_name="Sue",
        time_int=777,
        quota=445,
        allow_prev_to_present_time_entry=True,
    )
    accord23_fiscunit.add_cashpurchase(
        owner_name="Zia",
        acct_name="Bob",
        time_int=777,
        amount=888,
    )
    gen_fiscunit = x_fiscunits.get(accord23_str)
    assert gen_fiscunit.fund_coin == x_fund_coin
    assert gen_fiscunit.respect_bit == x_respect_bit
    assert gen_fiscunit.penny == x_penny
    assert gen_fiscunit.fisc_title == accord23_str
    assert gen_fiscunit.fisc_mstr_dir == x_fiscs_dir
    assert gen_fiscunit.timeline == accord23_fiscunit.timeline
    assert gen_fiscunit.brokerunits == accord23_fiscunit.brokerunits
    assert gen_fiscunit.cashbook.tranunits == accord23_fiscunit.cashbook.tranunits
    print(f"{gen_fiscunit.brokerunits=}")
    assert len(gen_fiscunit.brokerunits) == 1
    assert len(gen_fiscunit.cashbook.tranunits) == 1
    assert gen_fiscunit == accord23_fiscunit


# given a dataframe, build a fisc unit
def test_fisc_build_from_df_ReturnsObj_Scenario1_TwoFiscTitles(
    idea_env_setup_cleanup,
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
    x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_fiscunits = fisc_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_fiscunit = fiscunit_shop(
        present_time=5500,
        fisc_title=accord23_str,
        fisc_mstr_dir=x_fiscs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_fiscunit = fiscunit_shop(
        present_time=444,
        fisc_title="jeffy45",
        fisc_mstr_dir=x_fiscs_dir,
        fund_coin=x_fund_coin,
        penny=x_penny,
        respect_bit=x_respect_bit,
        bridge=",",
        timeline=five_timelineunit,
    )
    assert x_fiscunits
    assert x_fiscunits.get(accord23_str) != None
    creg_fiscunit = x_fiscunits.get(accord23_str)
    assert creg_fiscunit.fund_coin == x_fund_coin
    assert creg_fiscunit.respect_bit == x_respect_bit
    assert creg_fiscunit.penny == x_penny
    assert creg_fiscunit.fisc_title == accord23_str
    assert creg_fiscunit.fisc_mstr_dir == x_fiscs_dir
    assert creg_fiscunit.timeline == accord23_fiscunit.timeline
    assert len(creg_fiscunit.brokerunits) == 3
    assert len(creg_fiscunit.cashbook.tranunits) == 4
    # assert creg_fiscunit == accord23_fiscunit

    five_fiscunit = x_fiscunits.get("jeffy45")
    assert five_fiscunit.fund_coin == x_fund_coin
    assert five_fiscunit.respect_bit == x_respect_bit
    assert five_fiscunit.penny == x_penny
    assert five_fiscunit.fisc_title == "jeffy45"
    assert five_fiscunit.fisc_mstr_dir == x_fiscs_dir
    assert len(five_fiscunit.brokerunits) == 2
    assert len(five_fiscunit.cashbook.tranunits) == 1
    jeffy45_timeline = jeffy45_fiscunit.timeline
    assert five_fiscunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_fiscunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_fiscunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_fiscunit.timeline == jeffy45_timeline
    # assert five_fiscunit == jeffy45_fiscunit


# # given a dataframe, build a fisc unit
# def test_create_idea_brick_csvs_from_fisc_objs_ReturnsObj_Scenario0_EmptyFiscUnit(
#     idea_env_setup_cleanup,
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
#     x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
#     accord23_str = "accord23"
#     slash_str = "/"
#     x_fiscunits = fisc_build_from_df(
#         br00000_df,
#         br00001_df,
#         br00002_df,
#         br00003_df,
#         br00004_df,
#         br00005_df,
#         x_fund_coin,
#         x_respect_bit,
#         x_penny,
#         x_fiscs_dir,
#     )

#     # WHEN
#     x_ideabricks = create_idea_brick_csvs_from_fisc_objs(x_fiscunits)

#     # THEN
#     ex2_br00000_csv = get_ordered_csv(get_ex2_br00000_df())
#     ex2_br00001_csv = get_ordered_csv(get_ex2_br00001_df())
#     ex2_br00002_csv = get_ordered_csv(get_ex2_br00002_df())
#     ex2_br00003_csv = get_ordered_csv(get_ex2_br00003_df())
#     ex2_br00004_csv = get_ordered_csv(get_ex2_br00004_df())
#     ex2_br00005_csv = get_ordered_csv(get_ex2_br00005_df())
#     print(f"{ex2_br00000_csv=}")

#     assert len(x_ideabricks) == 6
#     assert x_ideabricks.get("br00000") == ex2_br00000_csv
#     assert x_ideabricks.get("br00001") == ex2_br00001_csv
#     assert x_ideabricks.get("br00002") == ex2_br00002_csv
#     assert x_ideabricks.get("br00003") == ex2_br00003_csv
#     assert x_ideabricks.get("br00004") == ex2_br00004_csv
#     assert x_ideabricks.get("br00005") == ex2_br00005_csv


# def test_create_idea_brick_csvs_from_fisc_objs_ReturnsObj_Scenario1_TwoFiscTitles(
#     idea_env_setup_cleanup,
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
#     x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
#     accord23_str = "accord23"
#     slash_str = "/"
#     x_fiscunits = fisc_build_from_df(
#         br00000_df,
#         br00001_df,
#         br00002_df,
#         br00003_df,
#         br00004_df,
#         br00005_df,
#         x_fund_coin,
#         x_respect_bit,
#         x_penny,
#         x_fiscs_dir,
#     )

#     # WHEN
#     x_ideabricks = create_idea_brick_csvs_from_fisc_objs(x_fiscunits)

#     # THEN
#     ex2_br00000_csv = get_ordered_csv(get_ex2_br00000_df())
#     ex2_br00001_csv = get_ordered_csv(get_ex2_br00001_df())
#     ex2_br00002_csv = get_ordered_csv(get_ex2_br00002_df())
#     ex2_br00003_csv = get_ordered_csv(get_ex2_br00003_df())
#     ex2_br00004_csv = get_ordered_csv(get_ex2_br00004_df())
#     ex2_br00005_csv = get_ordered_csv(get_ex2_br00005_df())

#     assert len(x_ideabricks) == 6
#     assert x_ideabricks.get("br00000") == ex2_br00000_csv
#     assert x_ideabricks.get("br00001") == ex2_br00001_csv
#     assert x_ideabricks.get("br00002") == ex2_br00002_csv
#     assert x_ideabricks.get("br00003") == ex2_br00003_csv
#     assert x_ideabricks.get("br00004") == ex2_br00004_csv
#     assert x_ideabricks.get("br00005") == ex2_br00005_csv
