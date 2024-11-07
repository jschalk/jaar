from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_fiscal.examples.example_fiscals import create_example_fiscal2
from src.f07_fiscal.fiscal import fiscalunit_shop
from src.f09_brick.examples.brick_df_examples import (
    get_ex1_br00000_df,
    get_ex1_br00001_df,
    get_ex1_br00002_df,
    get_ex1_br00003_df,
    get_ex1_br00004_df,
    get_ex1_br00005_df,
)
from src.f09_brick.brick import fiscal_build_from_df
from pandas import DataFrame


# given a dataframe, build a fiscal unit
def test_fiscal_build_from_df_ReturnsObj():
    # ESTABLISH / WHEN

    # brick_format_00000_fiscalunit_v0_0_0
    # brick_format_00001_fiscal_purview_episode_v0_0_0
    # brick_format_00002_fiscal_cashbook_v0_0_0
    # brick_format_00003_fiscal_timeline_hour_v0_0_0
    # brick_format_00004_fiscal_timeline_month_v0_0_0
    # brick_format_00005_fiscal_timeline_weekday_v0_0_0
    br00000_df = get_ex1_br00000_df()
    br00001_df = get_ex1_br00001_df()
    br00002_df = get_ex1_br00002_df()
    br00003_df = get_ex1_br00003_df()
    br00004_df = get_ex1_br00004_df()
    br00005_df = get_ex1_br00005_df()
    x_fund_coin = 55
    x_respect_bit = 66
    x_penny = 77
    x_fiscals_dir = "/fizz/fiscals/"
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
        slash_text,
    )

    # THEN
    # creg_timelineunit = TimeLineUnit(
    #     c400_number=7,
    #     monthday_distortion=1,
    #     timeline_label="creg",
    #     yr1_jan1_offset=440640,
    # )
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
    assert x_fiscalunits
    assert x_fiscalunits.get(music23_str) != None
    gen_fiscalunit = x_fiscalunits.get(music23_str)
    assert gen_fiscalunit.fund_coin == x_fund_coin
    assert gen_fiscalunit.respect_bit == x_respect_bit
    assert gen_fiscalunit.penny == x_penny
    assert gen_fiscalunit.fiscal_id == music23_str
    assert gen_fiscalunit.fiscals_dir == x_fiscals_dir
    assert gen_fiscalunit.timeline == music23_fiscalunit.timeline
    assert gen_fiscalunit == music23_fiscalunit
