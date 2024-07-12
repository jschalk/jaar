from src._world.report import (
    get_world_charunits_dataframe,
    get_world_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_voices_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_world = x_hubunit.get_voice_world()
        voice_world.calc_world_metrics()
        df = get_world_charunits_dataframe(voice_world)
        df.insert(0, "owner_id", voice_world._owner_id)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_real_voices_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_voices_chars_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.char_id,
                df.credor_weight,
                df.debtor_weight,
                df._world_cred,
                df._world_debt,
                df._world_agenda_cred,
                df._world_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', voice chars metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_actions_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get action
    action_dfs = []
    for x_hubunit in owner_hubunits.values():
        action_world = x_hubunit.get_action_world()
        action_world.calc_world_metrics()
        action_df = get_world_charunits_dataframe(action_world)
        action_df.insert(0, "owner_id", action_world._owner_id)
        action_dfs.append(action_df)
    return pandas_concat(action_dfs, ignore_index=True)


def get_real_actions_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_actions_chars_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.char_id,
                df.credor_weight,
                df.debtor_weight,
                df._world_cred,
                df._world_debt,
                df._world_agenda_cred,
                df._world_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', action chars metrics"
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
        voice_world = x_hubunit.get_voice_world()
        voice_world.calc_world_metrics()
        df = get_world_agenda_dataframe(voice_world)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_real_voices_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "bud_share",
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
                df.bud_share,
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
        action_world = x_hubunit.get_action_world()
        action_world.calc_world_metrics()
        action_df = get_world_agenda_dataframe(action_world)
        action_dfs.append(action_df)
    return pandas_concat(action_dfs, ignore_index=True)


def get_real_actions_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "bud_share",
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
                df.bud_share,
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
