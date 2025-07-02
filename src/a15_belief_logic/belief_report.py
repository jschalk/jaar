from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_owner_logic.report import (
    get_owner_acctunits_dataframe,
    get_owner_agenda_dataframe,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file
from src.a15_belief_logic.belief import BeliefUnit


def get_belief_guts_accts_dataframe(x_belief: BeliefUnit) -> DataFrame:
    # get list of all owner paths
    belief_owner_names = x_belief._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in belief_owner_names:
        gut_owner = open_gut_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, owner_name
        )
        gut_owner.settle_owner()
        df = get_owner_acctunits_dataframe(gut_owner)
        df.insert(0, "owner_name", gut_owner.owner_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_belief_guts_accts_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
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
                df.owner_name,
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
    # get list of all owner paths
    belief_owner_names = x_belief._get_owner_folder_names()
    # for all owners get gut
    job_dfs = []
    for owner_name in belief_owner_names:
        job = open_job_file(x_belief.belief_mstr_dir, x_belief.belief_label, owner_name)
        job.settle_owner()
        job_df = get_owner_acctunits_dataframe(job)
        job_df.insert(0, "owner_name", job.owner_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_belief_jobs_accts_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
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
                df.owner_name,
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
    # get list of all owner paths
    belief_owner_names = x_belief._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in belief_owner_names:
        gut_owner = open_gut_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, owner_name
        )
        gut_owner.settle_owner()
        df = get_owner_agenda_dataframe(gut_owner)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_belief_guts_agenda_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
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
                df.owner_name,
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
    # get list of all owner paths
    job_dfs = []
    for x_owner_name in x_belief._get_owner_folder_names():

        job = open_job_file(
            x_belief.belief_mstr_dir, x_belief.belief_label, x_owner_name
        )
        job.settle_owner()
        job_df = get_owner_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_belief_jobs_agenda_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
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
                df.owner_name,
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
