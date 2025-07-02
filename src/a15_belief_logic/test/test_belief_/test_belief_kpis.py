from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    addin_str,
    begin_str,
    close_str,
    concept_label_str,
    denom_str,
    morph_str,
    numor_str,
    owner_name_str,
    parent_rope_str,
)
from src.a15_belief_logic.belief_report import (
    get_belief_guts_accts_dataframe,
    get_belief_guts_accts_plotly_fig,
    get_belief_guts_agenda_dataframe,
    get_belief_guts_agenda_plotly_fig,
    get_belief_jobs_accts_dataframe,
    get_belief_jobs_accts_plotly_fig,
    get_belief_jobs_agenda_dataframe,
    get_belief_jobs_agenda_plotly_fig,
)
from src.a15_belief_logic.test._util.a15_env import env_dir_setup_cleanup
from src.a15_belief_logic.test._util.example_beliefs import (
    create_example_belief2,
    create_example_belief3,
    create_example_belief4,
)


def test_get_belief_guts_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief2()

    # WHEN
    x_df = get_belief_guts_accts_dataframe(amy_belief)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        acct_cred_points_str(),
        acct_debt_points_str(),
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


def test_get_belief_guts_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief2()

    # WHEN
    x_fig = get_belief_guts_accts_plotly_fig(amy_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_belief_jobs_accts_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief2()
    amy_belief.generate_all_jobs()

    # WHEN
    x_df = get_belief_jobs_accts_dataframe(amy_belief)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        acct_cred_points_str(),
        acct_debt_points_str(),
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
        "_inallocable_acct_debt_points",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == acctunit_colums


def test_get_belief_jobs_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief2()
    amy_belief.generate_all_jobs()

    # WHEN
    x_fig = get_belief_jobs_accts_plotly_fig(amy_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_belief_guts_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief3()

    # WHEN
    x_df = get_belief_guts_agenda_dataframe(amy_belief)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        concept_label_str(),
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


def test_get_belief_guts_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief3()

    # WHEN
    x_fig = get_belief_guts_agenda_plotly_fig(amy_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_belief_jobs_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    amy_belief = create_example_belief4()
    amy_belief.generate_all_jobs()

    # WHEN
    x_df = get_belief_jobs_agenda_dataframe(amy_belief)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "concept_label",
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


def test_get_belief_jobs_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    amy_belief = create_example_belief4()
    amy_belief.generate_all_jobs()

    # WHEN
    x_fig = get_belief_jobs_agenda_plotly_fig(amy_belief)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
