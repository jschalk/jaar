from src.f02_bud.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.f06_listen.hub_tool import open_voice_file, open_plan_file
from src.f08_fisc.fisc import FiscUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_fisc_voices_accts_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fisc.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = open_voice_file(
            x_hubunit.fisc_mstr_dir, x_hubunit.fisc_title, x_hubunit.owner_name
        )
        voice_bud.settle_bud()
        df = get_bud_acctunits_dataframe(voice_bud)
        df.insert(0, "owner_name", voice_bud.owner_name)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_fisc_voices_accts_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
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
    df = get_fisc_voices_accts_dataframe(x_fisc)
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
    fig_title = f"fisc '{x_fisc.fisc_title}', voice accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_fisc_plans_accts_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fisc.get_owner_hubunits()
    # for all owners get plan
    plan_dfs = []
    for x_hubunit in owner_hubunits.values():
        plan = open_plan_file(
            x_hubunit.fisc_mstr_dir, x_hubunit.fisc_title, x_hubunit.owner_name
        )
        plan.settle_bud()
        plan_df = get_bud_acctunits_dataframe(plan)
        plan_df.insert(0, "owner_name", plan.owner_name)
        plan_dfs.append(plan_df)
    return pandas_concat(plan_dfs, ignore_index=True)


def get_fisc_plans_accts_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
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
    df = get_fisc_plans_accts_dataframe(x_fisc)
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
    fig_title = f"fisc '{x_fisc.fisc_title}', plan accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)
    return fig


def get_fisc_voices_agenda_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fisc.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = open_voice_file(
            x_hubunit.fisc_mstr_dir, x_hubunit.fisc_title, x_hubunit.owner_name
        )
        voice_bud.settle_bud()
        df = get_bud_agenda_dataframe(voice_bud)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_fisc_voices_agenda_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "item_title",
        "parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fisc_voices_agenda_dataframe(x_fisc)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df.item_title,
                df.parent_road,
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
    fig_title = f"fisc '{x_fisc.fisc_title}', voice agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)
    return fig


def get_fisc_plans_agenda_dataframe(x_fisc: FiscUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fisc.get_owner_hubunits()
    # for all owners get plan
    plan_dfs = []
    for x_hubunit in owner_hubunits.values():
        plan = open_plan_file(
            x_hubunit.fisc_mstr_dir, x_hubunit.fisc_title, x_hubunit.owner_name
        )
        plan.settle_bud()
        plan_df = get_bud_agenda_dataframe(plan)
        plan_dfs.append(plan_df)
    return pandas_concat(plan_dfs, ignore_index=True)


def get_fisc_plans_agenda_plotly_fig(x_fisc: FiscUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "item_title",
        "parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fisc_plans_agenda_dataframe(x_fisc)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df.item_title,
                df.parent_road,
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
    fig_title = f"fisc '{x_fisc.fisc_title}', plan agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)
    return fig
