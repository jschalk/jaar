from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a02_finance_logic._test_util.a02_str import owner_name_str
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    addin_str,
    begin_str,
    close_str,
    concept_label_str,
    credit_belief_str,
    debtit_belief_str,
    denom_str,
    morph_str,
    numor_str,
    parent_way_str,
)
from src.a15_fisc_logic._test_util.a15_env import env_dir_setup_cleanup
from src.a15_fisc_logic._test_util.example_fiscs import (
    create_example_fisc2,
    create_example_fisc3,
    create_example_fisc4,
)
from src.a15_fisc_logic.fisc_report import (
    get_fisc_guts_accts_dataframe,
    get_fisc_guts_accts_plotly_fig,
    get_fisc_guts_agenda_dataframe,
    get_fisc_guts_agenda_plotly_fig,
    get_fisc_jobs_accts_dataframe,
    get_fisc_jobs_accts_plotly_fig,
    get_fisc_jobs_agenda_dataframe,
    get_fisc_jobs_agenda_plotly_fig,
)


def test_get_fisc_guts_accts_dataframe_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    accord_fisc = create_example_fisc2()

    # WHEN
    x_df = get_fisc_guts_accts_dataframe(accord_fisc)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        credit_belief_str(),
        debtit_belief_str(),
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


def test_get_fisc_guts_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()

    # WHEN
    x_fig = get_fisc_guts_accts_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_jobs_accts_dataframe_ReturnsObj(env_dir_setup_cleanup, graphics_bool):
    # ESTABLISH
    accord_fisc = create_example_fisc2()
    accord_fisc.generate_all_jobs()

    # WHEN
    x_df = get_fisc_jobs_accts_dataframe(accord_fisc)

    # THEN
    acctunit_colums = {
        owner_name_str(),
        acct_name_str(),
        credit_belief_str(),
        debtit_belief_str(),
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


def test_get_fisc_jobs_accts_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc2()
    accord_fisc.generate_all_jobs()

    # WHEN
    x_fig = get_fisc_jobs_accts_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_guts_agenda_dataframe_ReturnsObj(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc3()

    # WHEN
    x_df = get_fisc_guts_agenda_dataframe(accord_fisc)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        concept_label_str(),
        parent_way_str(),
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


def test_get_fisc_guts_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc3()

    # WHEN
    x_fig = get_fisc_guts_agenda_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_fisc_jobs_agenda_dataframe_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fisc = create_example_fisc4()
    accord_fisc.generate_all_jobs()

    # WHEN
    x_df = get_fisc_jobs_agenda_dataframe(accord_fisc)

    # THEN
    agenda_colums = {
        owner_name_str(),
        "fund_ratio",
        "concept_label",
        parent_way_str(),
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


def test_get_fisc_jobs_agenda_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup, graphics_bool
):
    # ESTABLISH
    accord_fisc = create_example_fisc4()
    accord_fisc.generate_all_jobs()

    # WHEN
    x_fig = get_fisc_jobs_agenda_plotly_fig(accord_fisc)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
