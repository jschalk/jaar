from src.bud.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_voices_accts_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_acctunits_dataframe(voice_bud)
        df.insert(0, "owner_id", voice_bud._owner_id)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_real_voices_accts_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "acct_id",
        "credit_score",
        "debtit_score",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_real_voices_accts_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.acct_id,
                df.credit_score,
                df.debtit_score,
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
    fig_title = f"Real '{x_real.real_id}', voice accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_actions_accts_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get action
    action_dfs = []
    for x_hubunit in owner_hubunits.values():
        action_bud = x_hubunit.get_action_bud()
        action_bud.settle_bud()
        action_df = get_bud_acctunits_dataframe(action_bud)
        action_df.insert(0, "owner_id", action_bud._owner_id)
        action_dfs.append(action_df)
    return pandas_concat(action_dfs, ignore_index=True)


def get_real_actions_accts_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "acct_id",
        "credit_score",
        "debtit_score",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_real_actions_accts_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.acct_id,
                df.credit_score,
                df.debtit_score,
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
    fig_title = f"Real '{x_real.real_id}', action accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_voices_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_agenda_dataframe(voice_bud)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_real_voices_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_voices_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.fund_ratio,
                df._label,
                df._parent_road,
                df._begin,
                df._close,
                df._addin,
                df._denom,
                df._numor,
                df._reest,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', voice agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_actions_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get action
    action_dfs = []
    for x_hubunit in owner_hubunits.values():
        action_bud = x_hubunit.get_action_bud()
        action_bud.settle_bud()
        action_df = get_bud_agenda_dataframe(action_bud)
        action_dfs.append(action_df)
    return pandas_concat(action_dfs, ignore_index=True)


def get_real_actions_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_actions_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.fund_ratio,
                df._label,
                df._parent_road,
                df._begin,
                df._close,
                df._addin,
                df._denom,
                df._numor,
                df._reest,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', action agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
