from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_bud_logic.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.a12_hub_tools.hub_tool import open_gut_file, open_job_file
from src.a15_fisc_logic.fisc import FiscUnit


def get_fisc_guts_accts_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    fisc_owner_names = x_fisc._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in fisc_owner_names:
        gut_bud = open_gut_file(x_fisc.fisc_mstr_dir, x_fisc.fisc_label, owner_name)
        gut_bud.settle_bud()
        df = get_bud_acctunits_dataframe(gut_bud)
        df.insert(0, "owner_name", gut_bud.owner_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_fisc_guts_accts_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "acct_name",
        "credit_belief",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_fisc_guts_accts_dataframe(x_fisc)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.acct_name,
                df.credit_belief,
                df.debtit_belief,
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
    fig_label = f"fisc '{x_fisc.fisc_label}', gut accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_fisc_jobs_accts_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    fisc_owner_names = x_fisc._get_owner_folder_names()
    # for all owners get gut
    job_dfs = []
    for owner_name in fisc_owner_names:
        job = open_job_file(x_fisc.fisc_mstr_dir, x_fisc.fisc_label, owner_name)
        job.settle_bud()
        job_df = get_bud_acctunits_dataframe(job)
        job_df.insert(0, "owner_name", job.owner_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_fisc_jobs_accts_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "acct_name",
        "credit_belief",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_fisc_jobs_accts_dataframe(x_fisc)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.acct_name,
                df.credit_belief,
                df.debtit_belief,
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
    fig_label = f"fisc '{x_fisc.fisc_label}', job accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_fisc_guts_agenda_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    fisc_owner_names = x_fisc._get_owner_folder_names()
    # for all owners get gut
    gut_dfs = []
    for owner_name in fisc_owner_names:
        gut_bud = open_gut_file(x_fisc.fisc_mstr_dir, x_fisc.fisc_label, owner_name)
        gut_bud.settle_bud()
        df = get_bud_agenda_dataframe(gut_bud)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_fisc_guts_agenda_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_way",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fisc_guts_agenda_dataframe(x_fisc)
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
                df.parent_way,
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
    fig_label = f"fisc '{x_fisc.fisc_label}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_fisc_jobs_agenda_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    job_dfs = []
    for x_owner_name in x_fisc._get_owner_folder_names():

        job = open_job_file(x_fisc.fisc_mstr_dir, x_fisc.fisc_label, x_owner_name)
        job.settle_bud()
        job_df = get_bud_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_fisc_jobs_agenda_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_way",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fisc_jobs_agenda_dataframe(x_fisc)
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
                df.parent_way,
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
    fig_label = f"fisc '{x_fisc.fisc_label}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
