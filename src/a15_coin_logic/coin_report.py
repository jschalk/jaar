from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_belief_logic.belief_report import (
    get_belief_agenda_dataframe,
    get_belief_partnerunits_dataframe,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file
from src.a15_coin_logic.coin_main import CoinUnit


def get_coin_guts_partners_dataframe(x_coin: CoinUnit) -> DataFrame:
    # get list of all belief paths
    coin_belief_names = x_coin._get_belief_folder_names()
    # for all beliefs get gut
    gut_dfs = []
    for belief_name in coin_belief_names:
        gut_belief = open_gut_file(x_coin.coin_mstr_dir, x_coin.coin_label, belief_name)
        gut_belief.settle_belief()
        df = get_belief_partnerunits_dataframe(gut_belief)
        df.insert(0, "belief_name", gut_belief.belief_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_coin_guts_partners_plotly_fig(x_coin: CoinUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
        "partner_name",
        "partner_cred_points",
        "partner_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_coin_guts_partners_dataframe(x_coin)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
                df.partner_name,
                df.partner_cred_points,
                df.partner_debt_points,
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
    fig_label = f"coin '{x_coin.coin_label}', gut partners metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_coin_jobs_partners_dataframe(x_coin: CoinUnit) -> DataFrame:
    # get list of all belief paths
    coin_belief_names = x_coin._get_belief_folder_names()
    # for all beliefs get gut
    job_dfs = []
    for belief_name in coin_belief_names:
        job = open_job_file(x_coin.coin_mstr_dir, x_coin.coin_label, belief_name)
        job.settle_belief()
        job_df = get_belief_partnerunits_dataframe(job)
        job_df.insert(0, "belief_name", job.belief_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_coin_jobs_partners_plotly_fig(x_coin: CoinUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
        "partner_name",
        "partner_cred_points",
        "partner_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_coin_jobs_partners_dataframe(x_coin)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
                df.partner_name,
                df.partner_cred_points,
                df.partner_debt_points,
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
    fig_label = f"coin '{x_coin.coin_label}', job partners metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_coin_guts_agenda_dataframe(x_coin: CoinUnit) -> DataFrame:
    # get list of all belief paths
    coin_belief_names = x_coin._get_belief_folder_names()
    # for all beliefs get gut
    gut_dfs = []
    for belief_name in coin_belief_names:
        gut_belief = open_gut_file(x_coin.coin_mstr_dir, x_coin.coin_label, belief_name)
        gut_belief.settle_belief()
        df = get_belief_agenda_dataframe(gut_belief)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_coin_guts_agenda_plotly_fig(x_coin: CoinUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
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
    df = get_coin_guts_agenda_dataframe(x_coin)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
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
    fig_label = f"coin '{x_coin.coin_label}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_coin_jobs_agenda_dataframe(x_coin: CoinUnit) -> DataFrame:
    # get list of all belief paths
    job_dfs = []
    for x_belief_name in x_coin._get_belief_folder_names():

        job = open_job_file(x_coin.coin_mstr_dir, x_coin.coin_label, x_belief_name)
        job.settle_belief()
        job_df = get_belief_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_coin_jobs_agenda_plotly_fig(x_coin: CoinUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
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
    df = get_coin_jobs_agenda_dataframe(x_coin)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
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
    fig_label = f"coin '{x_coin.coin_label}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
