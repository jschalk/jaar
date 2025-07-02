from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_believer_logic.report import (
    get_believer_acctunits_dataframe,
    get_believer_agenda_dataframe,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file
from src.a15_belief_logic.belief import BeliefUnit


def get_belief_guts_accts_dataframe(x_belief: BeliefUnit) -> DataFrame:
    # get list of all believer paths
    belief_believer_names = x_belief._get_believer_folder_names()
    # for all believers get gut
    gut_dfs = []
    for believer_name in belief_believer_names:
        gut_believer = open_gut_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, believer_name
        )
        gut_believer.settle_believer()
        df = get_believer_acctunits_dataframe(gut_believer)
        df.insert(0, "believer_name", gut_believer.believer_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_belief_guts_accts_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "believer_name",
        "acct_name",
        "acct_cred_points",
        "acct_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_belief_guts_accts_dataframe(x_belief)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.believer_name,
                df.acct_name,
                df.acct_cred_points,
                df.acct_debt_points,
                df._fund_give,
                df._fund_take,
                df._fund_agenda_give,
                df._fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"belief '{x_belief.belief_label}', gut accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_belief_jobs_accts_dataframe(x_belief: BeliefUnit) -> DataFrame:
    # get list of all believer paths
    belief_believer_names = x_belief._get_believer_folder_names()
    # for all believers get gut
    job_dfs = []
    for believer_name in belief_believer_names:
        job = open_job_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, believer_name
        )
        job.settle_believer()
        job_df = get_believer_acctunits_dataframe(job)
        job_df.insert(0, "believer_name", job.believer_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_belief_jobs_accts_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "believer_name",
        "acct_name",
        "acct_cred_points",
        "acct_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_belief_jobs_accts_dataframe(x_belief)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.believer_name,
                df.acct_name,
                df.acct_cred_points,
                df.acct_debt_points,
                df._fund_give,
                df._fund_take,
                df._fund_agenda_give,
                df._fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"belief '{x_belief.belief_label}', job accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_belief_guts_agenda_dataframe(x_belief: BeliefUnit) -> DataFrame:
    # get list of all believer paths
    belief_believer_names = x_belief._get_believer_folder_names()
    # for all believers get gut
    gut_dfs = []
    for believer_name in belief_believer_names:
        gut_believer = open_gut_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, believer_name
        )
        gut_believer.settle_believer()
        df = get_believer_agenda_dataframe(gut_believer)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_belief_guts_agenda_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "believer_name",
        "fund_ratio",
        "plan_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_belief_guts_agenda_dataframe(x_belief)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.believer_name,
                df.fund_ratio,
                df.plan_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"belief '{x_belief.belief_label}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_belief_jobs_agenda_dataframe(x_belief: BeliefUnit) -> DataFrame:
    # get list of all believer paths
    job_dfs = []
    for x_believer_name in x_belief._get_believer_folder_names():

        job = open_job_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, x_believer_name
        )
        job.settle_believer()
        job_df = get_believer_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_belief_jobs_agenda_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "believer_name",
        "fund_ratio",
        "plan_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_belief_jobs_agenda_dataframe(x_belief)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.believer_name,
                df.fund_ratio,
                df.plan_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"belief '{x_belief.belief_label}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
