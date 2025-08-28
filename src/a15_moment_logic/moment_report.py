from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.a06_belief_logic.belief_report import (
    get_belief_agenda_dataframe,
    get_belief_voiceunits_dataframe,
)
from src.a12_hub_toolbox.hub_tool import open_gut_file, open_job_file
from src.a15_moment_logic.moment_main import MomentUnit


def get_moment_guts_voices_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all belief paths
    moment_belief_names = x_moment._get_belief_folder_names()
    # for all beliefs get gut
    gut_dfs = []
    for belief_name in moment_belief_names:
        gut_belief = open_gut_file(
            x_moment.moment_mstr_dir, x_moment.moment_label, belief_name
        )
        gut_belief.cash_out()
        df = get_belief_voiceunits_dataframe(gut_belief)
        df.insert(0, "belief_name", gut_belief.belief_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_voices_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
        "voice_name",
        "voice_cred_points",
        "voice_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_moment_guts_voices_dataframe(x_moment)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
                df.voice_name,
                df.voice_cred_points,
                df.voice_debt_points,
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
    fig_label = f"moment '{x_moment.moment_label}', gut voices metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_moment_jobs_voices_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all belief paths
    moment_belief_names = x_moment._get_belief_folder_names()
    # for all beliefs get gut
    job_dfs = []
    for belief_name in moment_belief_names:
        job = open_job_file(
            x_moment.moment_mstr_dir, x_moment.moment_label, belief_name
        )
        job.cash_out()
        job_df = get_belief_voiceunits_dataframe(job)
        job_df.insert(0, "belief_name", job.belief_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_voices_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
        "voice_name",
        "voice_cred_points",
        "voice_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_moment_jobs_voices_dataframe(x_moment)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.belief_name,
                df.voice_name,
                df.voice_cred_points,
                df.voice_debt_points,
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
    fig_label = f"moment '{x_moment.moment_label}', job voices metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_guts_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all belief paths
    moment_belief_names = x_moment._get_belief_folder_names()
    # for all beliefs get gut
    gut_dfs = []
    for belief_name in moment_belief_names:
        gut_belief = open_gut_file(
            x_moment.moment_mstr_dir, x_moment.moment_label, belief_name
        )
        gut_belief.cash_out()
        df = get_belief_agenda_dataframe(gut_belief)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
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
    df = get_moment_guts_agenda_dataframe(x_moment)
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
    fig_label = f"moment '{x_moment.moment_label}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_jobs_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all belief paths
    job_dfs = []
    for x_belief_name in x_moment._get_belief_folder_names():

        job = open_job_file(
            x_moment.moment_mstr_dir, x_moment.moment_label, x_belief_name
        )
        job.cash_out()
        job_df = get_belief_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
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
    df = get_moment_jobs_agenda_dataframe(x_moment)
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
    fig_label = f"moment '{x_moment.moment_label}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
