from src.f00_instrument.plotly_toolbox import conditional_fig_show
from src.f04_gift.atom_config import acct_name_str, owner_name_str
from src.f07_fiscal.fiscal_report import (
    get_fiscal_souls_accts_dataframe,
    get_fiscal_souls_accts_plotly_fig,
    get_fiscal_voices_accts_dataframe,
    get_fiscal_voices_accts_plotly_fig,
    get_fiscal_souls_agenda_dataframe,
    get_fiscal_souls_agenda_plotly_fig,
    get_fiscal_voices_agenda_dataframe,
    get_fiscal_voices_agenda_plotly_fig,
)
from src.f07_fiscal.examples.example_fiscals import (
    create_example_fiscal2,
    create_example_fiscal3,
    create_example_fiscal4,
)
from src.f07_fiscal.examples.fiscal_env import env_dir_setup_cleanup


def test_get_fiscal_souls_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal2()

    # WHEN
    x_df = get_fiscal_souls_accts_dataframe(accord_fiscal)

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


def test_get_fiscal_souls_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal2()

    # WHEN
    x_fig = get_fiscal_souls_accts_plotly_fig(accord_fiscal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fiscal_voices_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal2()
    accord_fiscal.generate_all_voice_buds()

    # WHEN
    x_df = get_fiscal_voices_accts_dataframe(accord_fiscal)

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


def test_get_fiscal_voices_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal2()
    accord_fiscal.generate_all_voice_buds()

    # WHEN
    x_fig = get_fiscal_voices_accts_plotly_fig(accord_fiscal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fiscal_souls_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal3()

    # WHEN
    x_df = get_fiscal_souls_agenda_dataframe(accord_fiscal)

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


def test_get_fiscal_souls_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal3()

    # WHEN
    x_fig = get_fiscal_souls_agenda_plotly_fig(accord_fiscal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fiscal_voices_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fiscal = create_example_fiscal4()
    accord_fiscal.generate_all_voice_buds()

    # WHEN
    x_df = get_fiscal_voices_agenda_dataframe(accord_fiscal)

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


def test_get_fiscal_voices_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fiscal = create_example_fiscal4()
    accord_fiscal.generate_all_voice_buds()

    # WHEN
    x_fig = get_fiscal_voices_agenda_plotly_fig(accord_fiscal)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
