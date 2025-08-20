from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_believer_logic.test._util.a06_str import (
    addin_str,
    begin_str,
    believer_name_str,
    close_str,
    denom_str,
    morph_str,
    numor_str,
    parent_rope_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    plan_label_str,
)
from src.a15_coin_logic.coin_report import (
    get_coin_guts_agenda_dataframe,
    get_coin_guts_agenda_plotly_fig,
    get_coin_guts_partners_dataframe,
    get_coin_guts_partners_plotly_fig,
    get_coin_jobs_agenda_dataframe,
    get_coin_jobs_agenda_plotly_fig,
    get_coin_jobs_partners_dataframe,
    get_coin_jobs_partners_plotly_fig,
)
from src.a15_coin_logic.test._util.a15_env import env_dir_setup_cleanup
from src.a15_coin_logic.test._util.example_coins import (
    create_example_coin2,
    create_example_coin3,
    create_example_coin4,
)


def test_get_coin_guts_partners_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin2()

    # WHEN
    x_df = get_coin_guts_partners_dataframe(amy_coin)

    # THEN
    partnerunit_colums = {
        believer_name_str(),
        partner_name_str(),
        partner_cred_points_str(),
        partner_debt_points_str(),
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == partnerunit_colums
    assert x_df.shape[0] == 8


def test_get_coin_guts_partners_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin2()

    # WHEN
    x_fig = get_coin_guts_partners_plotly_fig(amy_coin)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_coin_jobs_partners_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin2()
    amy_coin.generate_all_jobs()

    # WHEN
    x_df = get_coin_jobs_partners_dataframe(amy_coin)

    # THEN
    partnerunit_colums = {
        believer_name_str(),
        partner_name_str(),
        partner_cred_points_str(),
        partner_debt_points_str(),
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
        "_inallocable_partner_debt_points",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == partnerunit_colums


def test_get_coin_jobs_partners_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin2()
    amy_coin.generate_all_jobs()

    # WHEN
    x_fig = get_coin_jobs_partners_plotly_fig(amy_coin)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_coin_guts_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin3()

    # WHEN
    x_df = get_coin_guts_agenda_dataframe(amy_coin)

    # THEN
    agenda_colums = {
        believer_name_str(),
        "fund_ratio",
        plan_label_str(),
        parent_rope_str(),
        begin_str(),
        close_str(),
        addin_str(),
        denom_str(),
        numor_str(),
        morph_str(),
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] == 8


def test_get_coin_guts_agenda_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin3()

    # WHEN
    x_fig = get_coin_guts_agenda_plotly_fig(amy_coin)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_coin_jobs_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    amy_coin = create_example_coin4()
    amy_coin.generate_all_jobs()

    # WHEN
    x_df = get_coin_jobs_agenda_dataframe(amy_coin)

    # THEN
    agenda_colums = {
        believer_name_str(),
        "fund_ratio",
        "plan_label",
        parent_rope_str(),
        begin_str(),
        close_str(),
        addin_str(),
        denom_str(),
        numor_str(),
        morph_str(),
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] in [8, 9]


def test_get_coin_jobs_agenda_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_coin = create_example_coin4()
    amy_coin.generate_all_jobs()

    # WHEN
    x_fig = get_coin_jobs_agenda_plotly_fig(amy_coin)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
