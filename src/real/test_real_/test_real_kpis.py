from src._instrument.python_tool import conditional_fig_show
from src.gift.atom_config import acct_id_str
from src.real.real_report import (
    get_real_voices_accts_dataframe,
    get_real_voices_accts_plotly_fig,
    get_real_actions_accts_dataframe,
    get_real_actions_accts_plotly_fig,
    get_real_voices_agenda_dataframe,
    get_real_voices_agenda_plotly_fig,
    get_real_actions_agenda_dataframe,
    get_real_actions_agenda_plotly_fig,
)
from src.real.examples.example_reals import (
    create_example_real2,
    create_example_real3,
    create_example_real4,
)
from src.real.examples.real_env import env_dir_setup_cleanup


def test_get_real_voices_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real2()

    # WHEN
    x_df = get_real_voices_accts_dataframe(music_real)

    # THEN
    acctunit_colums = {
        "owner_id",
        acct_id_str(),
        "credit_score",
        "debtit_score",
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


def test_get_real_voices_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real2()

    # WHEN
    x_fig = get_real_voices_accts_plotly_fig(music_real)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_real_actions_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real2()
    music_real.generate_all_action_buds()

    # WHEN
    x_df = get_real_actions_accts_dataframe(music_real)

    # THEN
    acctunit_colums = {
        "owner_id",
        acct_id_str(),
        "credit_score",
        "debtit_score",
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
        "_inallocable_debtit_score",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == acctunit_colums


def test_get_real_actions_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real2()
    music_real.generate_all_action_buds()

    # WHEN
    x_fig = get_real_actions_accts_plotly_fig(music_real)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_real_voices_agenda_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real3()

    # WHEN
    x_df = get_real_voices_agenda_dataframe(music_real)

    # THEN
    agenda_colums = {
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_morph",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] == 8


def test_get_real_voices_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real3()

    # WHEN
    x_fig = get_real_voices_agenda_plotly_fig(music_real)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_real_actions_agenda_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_real = create_example_real4()
    music_real.generate_all_action_buds()

    # WHEN
    x_df = get_real_actions_agenda_dataframe(music_real)

    # THEN
    agenda_colums = {
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_morph",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] in [8, 9]


def test_get_real_actions_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_real = create_example_real4()
    music_real.generate_all_action_buds()

    # WHEN
    x_fig = get_real_actions_agenda_plotly_fig(music_real)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
