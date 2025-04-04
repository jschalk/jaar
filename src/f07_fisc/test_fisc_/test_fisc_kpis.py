from src.f00_instrument.plotly_toolbox import conditional_fig_show
from src.f01_road.deal import owner_name_str
from src.f04_vow.atom_config import acct_name_str
from src.f07_fisc.fisc_report import (
    get_fisc_voices_accts_dataframe,
    get_fisc_voices_accts_plotly_fig,
    get_fisc_forecasts_accts_dataframe,
    get_fisc_forecasts_accts_plotly_fig,
    get_fisc_voices_agenda_dataframe,
    get_fisc_voices_agenda_plotly_fig,
    get_fisc_forecasts_agenda_dataframe,
    get_fisc_forecasts_agenda_plotly_fig,
)
from src.f07_fisc.examples.example_fiscs import (
    create_example_fisc2,
    create_example_fisc3,
    create_example_fisc4,
)
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup


def test_get_fisc_voices_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()

    # WHEN
    x_df = get_fisc_voices_accts_dataframe(accord_fisc)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        "credit_belief",
        "debtit_belief",
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

    assert set(x_df.columns) == acctunit_colums
    assert x_df.shape[0] == 8


def test_get_fisc_voices_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()

    # WHEN
    x_fig = get_fisc_voices_accts_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_forecasts_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()
    accord_fisc.generate_all_forecast_buds()

    # WHEN
    x_df = get_fisc_forecasts_accts_dataframe(accord_fisc)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        "credit_belief",
        "debtit_belief",
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
        "_inallocable_debtit_belief",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == acctunit_colums


def test_get_fisc_forecasts_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()
    accord_fisc.generate_all_forecast_buds()

    # WHEN
    x_fig = get_fisc_forecasts_accts_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_voices_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc3()

    # WHEN
    x_df = get_fisc_voices_agenda_dataframe(accord_fisc)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "_item_title",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] == 8


def test_get_fisc_voices_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc3()

    # WHEN
    x_fig = get_fisc_voices_agenda_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_forecasts_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fisc = create_example_fisc4()
    accord_fisc.generate_all_forecast_buds()

    # WHEN
    x_df = get_fisc_forecasts_agenda_dataframe(accord_fisc)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "_item_title",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] in [8, 9]


def test_get_fisc_forecasts_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc4()
    accord_fisc.generate_all_forecast_buds()

    # WHEN
    x_fig = get_fisc_forecasts_agenda_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
