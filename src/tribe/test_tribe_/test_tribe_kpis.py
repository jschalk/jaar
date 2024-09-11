from src._instrument.python_tool import conditional_fig_show
from src.gift.atom_config import acct_id_str, owner_id_str
from src.tribe.tribe_report import (
    get_tribe_voices_accts_dataframe,
    get_tribe_voices_accts_plotly_fig,
    get_tribe_actions_accts_dataframe,
    get_tribe_actions_accts_plotly_fig,
    get_tribe_voices_agenda_dataframe,
    get_tribe_voices_agenda_plotly_fig,
    get_tribe_actions_agenda_dataframe,
    get_tribe_actions_agenda_plotly_fig,
)
from src.tribe.examples.example_tribes import (
    create_example_tribe2,
    create_example_tribe3,
    create_example_tribe4,
)
from src.tribe.examples.tribe_env import env_dir_setup_cleanup


def test_get_tribe_voices_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe2()

    # WHEN
    x_df = get_tribe_voices_accts_dataframe(music_tribe)

    # THEN
    acctunit_colums = {
        owner_id_str(),
        acct_id_str(),
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


def test_get_tribe_voices_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe2()

    # WHEN
    x_fig = get_tribe_voices_accts_plotly_fig(music_tribe)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_tribe_actions_accts_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe2()
    music_tribe.generate_all_action_buds()

    # WHEN
    x_df = get_tribe_actions_accts_dataframe(music_tribe)

    # THEN
    acctunit_colums = {
        owner_id_str(),
        acct_id_str(),
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


def test_get_tribe_actions_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe2()
    music_tribe.generate_all_action_buds()

    # WHEN
    x_fig = get_tribe_actions_accts_plotly_fig(music_tribe)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_tribe_voices_agenda_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe3()

    # WHEN
    x_df = get_tribe_voices_agenda_dataframe(music_tribe)

    # THEN
    agenda_colums = {
        owner_id_str(),
        "fund_ratio",
        "_label",
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


def test_get_tribe_voices_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe3()

    # WHEN
    x_fig = get_tribe_voices_agenda_plotly_fig(music_tribe)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_tribe_actions_agenda_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_tribe = create_example_tribe4()
    music_tribe.generate_all_action_buds()

    # WHEN
    x_df = get_tribe_actions_agenda_dataframe(music_tribe)

    # THEN
    agenda_colums = {
        owner_id_str(),
        "fund_ratio",
        "_label",
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


def test_get_tribe_actions_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    music_tribe = create_example_tribe4()
    music_tribe.generate_all_action_buds()

    # WHEN
    x_fig = get_tribe_actions_agenda_plotly_fig(music_tribe)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
