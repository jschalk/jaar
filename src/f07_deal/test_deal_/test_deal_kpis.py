from src.f00_instrument.plotly_toolbox import conditional_fig_show
from src.f04_gift.atom_config import acct_name_str, owner_name_str
from src.f07_deal.deal_report import (
    get_deal_voices_accts_dataframe,
    get_deal_voices_accts_plotly_fig,
    get_deal_finals_accts_dataframe,
    get_deal_finals_accts_plotly_fig,
    get_deal_voices_agenda_dataframe,
    get_deal_voices_agenda_plotly_fig,
    get_deal_finals_agenda_dataframe,
    get_deal_finals_agenda_plotly_fig,
)
from src.f07_deal.examples.example_deals import (
    create_example_deal2,
    create_example_deal3,
    create_example_deal4,
)
from src.f07_deal.examples.deal_env import env_dir_setup_cleanup


def test_get_deal_voices_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal2()

    # WHEN
    x_df = get_deal_voices_accts_dataframe(accord_deal)

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


def test_get_deal_voices_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal2()

    # WHEN
    x_fig = get_deal_voices_accts_plotly_fig(accord_deal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_deal_finals_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal2()
    accord_deal.generate_all_final_buds()

    # WHEN
    x_df = get_deal_finals_accts_dataframe(accord_deal)

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


def test_get_deal_finals_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal2()
    accord_deal.generate_all_final_buds()

    # WHEN
    x_fig = get_deal_finals_accts_plotly_fig(accord_deal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_deal_voices_agenda_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal3()

    # WHEN
    x_df = get_deal_voices_agenda_dataframe(accord_deal)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "_lx",
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


def test_get_deal_voices_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal3()

    # WHEN
    x_fig = get_deal_voices_agenda_plotly_fig(accord_deal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_deal_finals_agenda_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_deal = create_example_deal4()
    accord_deal.generate_all_final_buds()

    # WHEN
    x_df = get_deal_finals_agenda_dataframe(accord_deal)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "_lx",
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


def test_get_deal_finals_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_deal = create_example_deal4()
    accord_deal.generate_all_final_buds()

    # WHEN
    x_fig = get_deal_finals_agenda_plotly_fig(accord_deal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
