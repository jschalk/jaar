from src.a00_data_toolbox.file_toolbox import create_path
from src.a07_timeline_logic.test._util.calendar_examples import get_five_config
from src.a07_timeline_logic.timeline import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a15_bank_logic.bank import bankunit_shop
from src.a17_idea_logic.idea import bank_build_from_df
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup, idea_banks_dir
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


# ESTABLISH a dataframe, build a bank unit
def test_bank_build_from_df_ReturnsObj_Scenario0_OneBankLabel(
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
    x_banks_dir = create_path(idea_banks_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_bankunits = bank_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_banks_dir,
    )

    # THEN
    assert x_bankunits
    assert x_bankunits.get(accord23_str) != None
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    expected_accord23_bankunit = bankunit_shop(
        bank_label=accord23_str,
        bank_mstr_dir=x_banks_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_accord23_bankunit.add_budunit(
        owner_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_accord23_bankunit.add_paypurchase(
        owner_name="Zia",
        acct_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_bankunit = x_bankunits.get(accord23_str)
    assert gen_bankunit.fund_iota == x_fund_iota
    assert gen_bankunit.respect_bit == x_respect_bit
    assert gen_bankunit.penny == x_penny
    assert gen_bankunit.bank_label == accord23_str
    assert gen_bankunit.bank_mstr_dir == x_banks_dir
    assert gen_bankunit.timeline == expected_accord23_bankunit.timeline
    assert gen_bankunit.brokerunits == expected_accord23_bankunit.brokerunits
    a23_tranunits = expected_accord23_bankunit.paybook.tranunits
    assert gen_bankunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_bankunit.brokerunits=}")
    assert len(gen_bankunit.brokerunits) == 1
    assert len(gen_bankunit.paybook.tranunits) == 1
    assert gen_bankunit == expected_accord23_bankunit


# ESTABLISH a dataframe, build a bank unit
def test_bank_build_from_df_ReturnsObj_Scenario1_TwoBankLabels(
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
    x_banks_dir = create_path(idea_banks_dir(), "fizz")
    accord23_str = "accord23"
    slash_str = "/"

    # WHEN
    x_bankunits = bank_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_banks_dir,
    )

    # THEN
    creg_timelineunit = timelineunit_shop(get_default_timeline_config_dict())
    accord23_bankunit = bankunit_shop(
        bank_label=accord23_str,
        bank_mstr_dir=x_banks_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=slash_str,
        timeline=creg_timelineunit,
    )
    five_timelineunit = timelineunit_shop(get_five_config())
    jeffy45_bankunit = bankunit_shop(
        bank_label="jeffy45",
        bank_mstr_dir=x_banks_dir,
        fund_iota=x_fund_iota,
        penny=x_penny,
        respect_bit=x_respect_bit,
        knot=",",
        timeline=five_timelineunit,
    )
    assert x_bankunits
    assert x_bankunits.get(accord23_str) != None
    creg_bankunit = x_bankunits.get(accord23_str)
    assert creg_bankunit.fund_iota == x_fund_iota
    assert creg_bankunit.respect_bit == x_respect_bit
    assert creg_bankunit.penny == x_penny
    assert creg_bankunit.bank_label == accord23_str
    assert creg_bankunit.bank_mstr_dir == x_banks_dir
    assert creg_bankunit.timeline == accord23_bankunit.timeline
    assert len(creg_bankunit.brokerunits) == 3
    assert len(creg_bankunit.paybook.tranunits) == 4
    # assert creg_bankunit == accord23_bankunit

    five_bankunit = x_bankunits.get("jeffy45")
    assert five_bankunit.fund_iota == x_fund_iota
    assert five_bankunit.respect_bit == x_respect_bit
    assert five_bankunit.penny == x_penny
    assert five_bankunit.bank_label == "jeffy45"
    assert five_bankunit.bank_mstr_dir == x_banks_dir
    assert len(five_bankunit.brokerunits) == 2
    assert len(five_bankunit.paybook.tranunits) == 1
    jeffy45_timeline = jeffy45_bankunit.timeline
    assert five_bankunit.timeline.hours_config == jeffy45_timeline.hours_config
    assert five_bankunit.timeline.weekdays_config == jeffy45_timeline.weekdays_config
    assert five_bankunit.timeline.months_config == jeffy45_timeline.months_config
    assert five_bankunit.timeline == jeffy45_timeline
    # assert five_bankunit == jeffy45_bankunit
