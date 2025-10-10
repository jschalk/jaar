from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch08_epoch_logic.epoch_main import (
    epochunit_shop,
    get_default_epoch_config_dict,
)
from src.ch08_epoch_logic.test._util.ch08_examples import get_five_config
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch17_idea.idea_main import moment_build_from_df
from src.ch17_idea.test._util.ch17_env import env_dir_setup_cleanup, idea_moments_dir
from src.ch17_idea.test._util.ch17_examples import (
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
    x_fund_grain = 55
    x_respect_grain = 66
    x_money_grain = 77
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
        x_fund_grain,
        x_respect_grain,
        x_money_grain,
        x_moments_dir,
    )

    # THEN
    assert x_momentunits
    assert x_momentunits.get(amy23_str) != None
    creg_epochunit = epochunit_shop(get_default_epoch_config_dict())
    expected_amy23_momentunit = momentunit_shop(
        moment_label=amy23_str,
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        money_grain=x_money_grain,
        respect_grain=x_respect_grain,
        knot=slash_str,
        epoch=creg_epochunit,
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
    assert gen_momentunit.fund_grain == x_fund_grain
    assert gen_momentunit.respect_grain == x_respect_grain
    assert gen_momentunit.money_grain == x_money_grain
    assert gen_momentunit.moment_label == amy23_str
    assert gen_momentunit.moment_mstr_dir == x_moments_dir
    assert gen_momentunit.epoch == expected_amy23_momentunit.epoch
    assert (
        gen_momentunit.beliefbudhistorys == expected_amy23_momentunit.beliefbudhistorys
    )
    a23_tranunits = expected_amy23_momentunit.paybook.tranunits
    assert gen_momentunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_momentunit.beliefbudhistorys=}")
    assert len(gen_momentunit.beliefbudhistorys) == 1
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
    x_fund_grain = 55
    x_respect_grain = 66
    x_money_grain = 77
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
        x_fund_grain,
        x_respect_grain,
        x_money_grain,
        x_moments_dir,
    )

    # THEN
    creg_epochunit = epochunit_shop(get_default_epoch_config_dict())
    amy23_momentunit = momentunit_shop(
        moment_label=amy23_str,
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        money_grain=x_money_grain,
        respect_grain=x_respect_grain,
        knot=slash_str,
        epoch=creg_epochunit,
    )
    five_epochunit = epochunit_shop(get_five_config())
    jeffy45_momentunit = momentunit_shop(
        moment_label="jeffy45",
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        money_grain=x_money_grain,
        respect_grain=x_respect_grain,
        knot=",",
        epoch=five_epochunit,
    )
    assert x_momentunits
    assert x_momentunits.get(amy23_str) != None
    creg_momentunit = x_momentunits.get(amy23_str)
    assert creg_momentunit.fund_grain == x_fund_grain
    assert creg_momentunit.respect_grain == x_respect_grain
    assert creg_momentunit.money_grain == x_money_grain
    assert creg_momentunit.moment_label == amy23_str
    assert creg_momentunit.moment_mstr_dir == x_moments_dir
    assert creg_momentunit.epoch == amy23_momentunit.epoch
    assert len(creg_momentunit.beliefbudhistorys) == 3
    assert len(creg_momentunit.paybook.tranunits) == 4
    # assert creg_momentunit == amy23_momentunit

    five_momentunit = x_momentunits.get("jeffy45")
    assert five_momentunit.fund_grain == x_fund_grain
    assert five_momentunit.respect_grain == x_respect_grain
    assert five_momentunit.money_grain == x_money_grain
    assert five_momentunit.moment_label == "jeffy45"
    assert five_momentunit.moment_mstr_dir == x_moments_dir
    assert len(five_momentunit.beliefbudhistorys) == 2
    assert len(five_momentunit.paybook.tranunits) == 1
    jeffy45_epoch = jeffy45_momentunit.epoch
    assert five_momentunit.epoch.hours_config == jeffy45_epoch.hours_config
    assert five_momentunit.epoch.weekdays_config == jeffy45_epoch.weekdays_config
    assert five_momentunit.epoch.months_config == jeffy45_epoch.months_config
    assert five_momentunit.epoch == jeffy45_epoch
    # assert five_momentunit == jeffy45_momentunit
