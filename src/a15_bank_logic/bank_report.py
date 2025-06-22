from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_plan_logic.report import (
    get_plan_acctunits_dataframe,
    get_plan_agenda_dataframe,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file
from src.a15_bank_logic.bank import BankUnit


def get_bank_guts_accts_dataframe(x_bank: BankUnit) -> DataFrame:
    # get list of all owner paths
    bank_owner_names = x_bank._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in bank_owner_names:
        gut_plan = open_gut_file(x_bank.bank_mstr_dir, x_bank.bank_label, owner_name)
        gut_plan.settle_plan()
        df = get_plan_acctunits_dataframe(gut_plan)
        df.insert(0, "owner_name", gut_plan.owner_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_bank_guts_accts_plotly_fig(x_bank: BankUnit) -> plotly_Figure:
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
    df = get_bank_guts_accts_dataframe(x_bank)
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
    fig_label = f"bank '{x_bank.bank_label}', gut accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_bank_jobs_accts_dataframe(x_bank: BankUnit) -> DataFrame:
    # get list of all owner paths
    bank_owner_names = x_bank._get_owner_folder_names()
    # for all owners get gut
    job_dfs = []
    for owner_name in bank_owner_names:
        job = open_job_file(x_bank.bank_mstr_dir, x_bank.bank_label, owner_name)
        job.settle_plan()
        job_df = get_plan_acctunits_dataframe(job)
        job_df.insert(0, "owner_name", job.owner_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_bank_jobs_accts_plotly_fig(x_bank: BankUnit) -> plotly_Figure:
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
    df = get_bank_jobs_accts_dataframe(x_bank)
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
    fig_label = f"bank '{x_bank.bank_label}', job accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_bank_guts_agenda_dataframe(x_bank: BankUnit) -> DataFrame:
    # get list of all owner paths
    bank_owner_names = x_bank._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in bank_owner_names:
        gut_plan = open_gut_file(x_bank.bank_mstr_dir, x_bank.bank_label, owner_name)
        gut_plan.settle_plan()
        df = get_plan_agenda_dataframe(gut_plan)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_bank_guts_agenda_plotly_fig(x_bank: BankUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_bank_guts_agenda_dataframe(x_bank)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df.concept_label,
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
    fig_label = f"bank '{x_bank.bank_label}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_bank_jobs_agenda_dataframe(x_bank: BankUnit) -> DataFrame:
    # get list of all owner paths
    job_dfs = []
    for x_owner_name in x_bank._get_owner_folder_names():

        job = open_job_file(x_bank.bank_mstr_dir, x_bank.bank_label, x_owner_name)
        job.settle_plan()
        job_df = get_plan_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_bank_jobs_agenda_plotly_fig(x_bank: BankUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_bank_jobs_agenda_dataframe(x_bank)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df.concept_label,
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
    fig_label = f"bank '{x_bank.bank_label}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
