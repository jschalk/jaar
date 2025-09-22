from src.ch01_data_toolbox.plotly_toolbox import conditional_fig_show
from src.ch15_moment_logic._ref.ch15_terms import (
    addin_str,
    begin_str,
    belief_name_str,
    close_str,
    denom_str,
    morph_str,
    numor_str,
    parent_rope_str,
    plan_label_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)
from src.ch15_moment_logic.moment_report import (
    get_moment_guts_agenda_dataframe,
    get_moment_guts_agenda_plotly_fig,
    get_moment_guts_voices_dataframe,
    get_moment_guts_voices_plotly_fig,
    get_moment_jobs_agenda_dataframe,
    get_moment_jobs_agenda_plotly_fig,
    get_moment_jobs_voices_dataframe,
    get_moment_jobs_voices_plotly_fig,
)
from src.ch15_moment_logic.test._util.ch15_env import env_dir_setup_cleanup
from src.ch15_moment_logic.test._util.example_moments import (
    create_example_moment2,
    create_example_moment3,
    create_example_moment4,
)


def test_get_moment_guts_voices_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment2()

    # WHEN
    x_df = get_moment_guts_voices_dataframe(amy_moment)

    # THEN
    voiceunit_colums = {
        belief_name_str(),
        voice_name_str(),
        voice_cred_points_str(),
        voice_debt_points_str(),
        "memberships",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == voiceunit_colums
    assert x_df.shape[0] == 8


def test_get_moment_guts_voices_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment2()

    # WHEN
    x_fig = get_moment_guts_voices_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_jobs_voices_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment2()
    amy_moment.generate_all_jobs()

    # WHEN
    x_df = get_moment_jobs_voices_dataframe(amy_moment)

    # THEN
    voiceunit_colums = {
        belief_name_str(),
        voice_name_str(),
        voice_cred_points_str(),
        voice_debt_points_str(),
        "memberships",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
        "inallocable_voice_debt_points",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == voiceunit_colums


def test_get_moment_jobs_voices_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment2()
    amy_moment.generate_all_jobs()

    # WHEN
    x_fig = get_moment_jobs_voices_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_guts_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment3()

    # WHEN
    x_df = get_moment_guts_agenda_dataframe(amy_moment)

    # THEN
    agenda_colums = {
        belief_name_str(),
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


def test_get_moment_guts_agenda_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment3()

    # WHEN
    x_fig = get_moment_guts_agenda_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_jobs_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    amy_moment = create_example_moment4()
    amy_moment.generate_all_jobs()

    # WHEN
    x_df = get_moment_jobs_agenda_dataframe(amy_moment)

    # THEN
    agenda_colums = {
        belief_name_str(),
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


def test_get_moment_jobs_agenda_plotly_fig_DisplaysInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_moment = create_example_moment4()
    amy_moment.generate_all_jobs()

    # WHEN
    x_fig = get_moment_jobs_agenda_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
