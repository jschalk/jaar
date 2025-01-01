from src.f02_bud.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.f07_cmty.cmty import CmtyUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_cmty_voices_accts_dataframe(x_cmty: CmtyUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_cmty.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_acctunits_dataframe(voice_bud)
        df.insert(0, "owner_name", voice_bud.owner_name)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_cmty_voices_accts_plotly_fig(x_cmty: CmtyUnit) -> plotly_Figure:
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
    df = get_cmty_voices_accts_dataframe(x_cmty)
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
    fig_title = f"cmty '{x_cmty.cmty_idea}', voice accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_cmty_finals_accts_dataframe(x_cmty: CmtyUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_cmty.get_owner_hubunits()
    # for all owners get final
    final_dfs = []
    for x_hubunit in owner_hubunits.values():
        final_bud = x_hubunit.get_final_bud()
        final_bud.settle_bud()
        final_df = get_bud_acctunits_dataframe(final_bud)
        final_df.insert(0, "owner_name", final_bud.owner_name)
        final_dfs.append(final_df)
    return pandas_concat(final_dfs, ignore_index=True)


def get_cmty_finals_accts_plotly_fig(x_cmty: CmtyUnit) -> plotly_Figure:
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
    df = get_cmty_finals_accts_dataframe(x_cmty)
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
    fig_title = f"cmty '{x_cmty.cmty_idea}', final accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_cmty_voices_agenda_dataframe(x_cmty: CmtyUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_cmty.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_agenda_dataframe(voice_bud)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_cmty_voices_agenda_plotly_fig(x_cmty: CmtyUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "_idee",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_cmty_voices_agenda_dataframe(x_cmty)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df._idee,
                df._parent_road,
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
    fig_title = f"cmty '{x_cmty.cmty_idea}', voice agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_cmty_finals_agenda_dataframe(x_cmty: CmtyUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_cmty.get_owner_hubunits()
    # for all owners get final
    final_dfs = []
    for x_hubunit in owner_hubunits.values():
        final_bud = x_hubunit.get_final_bud()
        final_bud.settle_bud()
        final_df = get_bud_agenda_dataframe(final_bud)
        final_dfs.append(final_df)
    return pandas_concat(final_dfs, ignore_index=True)


def get_cmty_finals_agenda_plotly_fig(x_cmty: CmtyUnit) -> plotly_Figure:
    column_header_list = [
        "owner_name",
        "fund_ratio",
        "_idee",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_cmty_finals_agenda_dataframe(x_cmty)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_name,
                df.fund_ratio,
                df._idee,
                df._parent_road,
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
    fig_title = f"cmty '{x_cmty.cmty_idea}', final agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
