from src.f02_bud.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.f07_fiscal.fiscal import FiscalUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_fiscal_voices_accts_dataframe(x_fiscal: FiscalUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fiscal.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_acctunits_dataframe(voice_bud)
        df.insert(0, "owner_id", voice_bud._owner_id)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_fiscal_voices_accts_plotly_fig(x_fiscal: FiscalUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "acct_id",
        "credit_belief",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_fiscal_voices_accts_dataframe(x_fiscal)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.acct_id,
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
    fig_title = f"Fiscal '{x_fiscal.fiscal_id}', voice accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_fiscal_finals_accts_dataframe(x_fiscal: FiscalUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fiscal.get_owner_hubunits()
    # for all owners get final
    final_dfs = []
    for x_hubunit in owner_hubunits.values():
        final_bud = x_hubunit.get_final_bud()
        final_bud.settle_bud()
        final_df = get_bud_acctunits_dataframe(final_bud)
        final_df.insert(0, "owner_id", final_bud._owner_id)
        final_dfs.append(final_df)
    return pandas_concat(final_dfs, ignore_index=True)


def get_fiscal_finals_accts_plotly_fig(x_fiscal: FiscalUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "acct_id",
        "credit_belief",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_fiscal_finals_accts_dataframe(x_fiscal)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.acct_id,
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
    fig_title = f"Fiscal '{x_fiscal.fiscal_id}', final accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_fiscal_voices_agenda_dataframe(x_fiscal: FiscalUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fiscal.get_owner_hubunits()
    # for all owners get voice
    voice_dfs = []
    for x_hubunit in owner_hubunits.values():
        voice_bud = x_hubunit.get_voice_bud()
        voice_bud.settle_bud()
        df = get_bud_agenda_dataframe(voice_bud)
        voice_dfs.append(df)
    return pandas_concat(voice_dfs, ignore_index=True)


def get_fiscal_voices_agenda_plotly_fig(x_fiscal: FiscalUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fiscal_voices_agenda_dataframe(x_fiscal)
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
    fig_title = f"Fiscal '{x_fiscal.fiscal_id}', voice agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_fiscal_finals_agenda_dataframe(x_fiscal: FiscalUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_fiscal.get_owner_hubunits()
    # for all owners get final
    final_dfs = []
    for x_hubunit in owner_hubunits.values():
        final_bud = x_hubunit.get_final_bud()
        final_bud.settle_bud()
        final_df = get_bud_agenda_dataframe(final_bud)
        final_dfs.append(final_df)
    return pandas_concat(final_dfs, ignore_index=True)


def get_fiscal_finals_agenda_plotly_fig(x_fiscal: FiscalUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "fund_ratio",
        "_label",
        "_parent_road",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_fiscal_finals_agenda_dataframe(x_fiscal)
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
    fig_title = f"Fiscal '{x_fiscal.fiscal_id}', final agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
