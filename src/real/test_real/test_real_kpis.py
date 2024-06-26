from src.real.real_report import (
    get_real_souls_chars_dataframe,
    get_real_souls_chars_plotly_fig,
    get_real_beings_chars_dataframe,
    get_real_beings_chars_plotly_fig,
    get_real_souls_agenda_dataframe,
    get_real_souls_agenda_plotly_fig,
    get_real_beings_agenda_dataframe,
    get_real_beings_agenda_plotly_fig,
)
from src.real.examples.example_reals import (
    create_example_real2,
    create_example_real3,
    create_example_real4,
)
from src.real.examples.real_env import env_dir_setup_cleanup


def test_get_real_souls_chars_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_df = get_real_souls_chars_dataframe(music_real)

    # THEN
    charunit_colums = {
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_beliefholds",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_world_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 8


def test_get_real_souls_chars_plotly_fig_DisplaysCorrectInfo(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_fig = get_real_souls_chars_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_beings_chars_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_being_worlds()

    # WHEN
    x_df = get_real_beings_chars_dataframe(music_real)

    # THEN
    charunit_colums = {
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_beliefholds",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_world_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "_inallocable_debtor_weight",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == charunit_colums


def test_get_real_beings_chars_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_being_worlds()

    # WHEN
    x_fig = get_real_beings_chars_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_souls_agenda_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_df = get_real_souls_agenda_dataframe(music_real)

    # THEN
    agenda_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] == 8


def test_get_real_souls_agenda_plotly_fig_DisplaysCorrectInfo(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_fig = get_real_souls_agenda_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_real_beings_agenda_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_being_worlds()

    # WHEN
    x_df = get_real_beings_agenda_dataframe(music_real)

    # THEN
    agenda_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] in [8, 9]


def test_get_real_beings_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_being_worlds()

    # WHEN
    x_fig = get_real_beings_agenda_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2
