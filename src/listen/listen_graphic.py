from src._instrument.python_tool import conditional_fig_show
from src._road.jaar_config import voice_str, action_str
from src._road.finance import default_money_magnitude
from src.bud.bud import BudUnit
from src.bud.graphic import display_ideatree
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter


def add_bud_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None):
    if x_color is None:
        x_color = "LightSeaGreen"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_direc_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_econ__rect(
    fig: plotly_Figure, x0, y0, x1, y1, text1=None, text2=None, text3=None, text4=None
):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0 + 0.5, y1, text1)
    add_rect_str(fig, x0 + 0.5, y1 - 0.2, text2)
    add_rect_str(fig, x0 + 0.5, y1 - 0.4, text3)
    add_rect_str(fig, x0 + 0.5, y1 - 0.6, text4)


def add_rect_str(fig, x0, y0, text):
    x_margin = 0.2
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None):
    if color is None:
        color = "black"
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # arrow only
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=3,
        arrowcolor=color,
    )


def get_hubunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def get_listen_structures0_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        sue_str = "Sue"
        bob_str = "Bob"
        yao_str = "Yao"
        fig = get_hubunit_base_fig()
        sue_voice_str = f"{sue_str}.{voice_str()}"
        sue_action_str = f"{sue_str}.{action_str()}"
        yao_action_str = f"{yao_str}.{action_str()}"
        bob_action_str = f"{bob_str}.{action_str()}"
        dir_action_str = f"{action_str()}s directory"
        dir_voice_str = f"{voice_str()}s directory"

        green_str = "Green"
        med_purple = "MediumPurple"
        add_bud_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_voice_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 6.3, 8.3, dir_voice_str)
        add_bud_rect(fig, 1.0, 1.0, 2.0, 2.0, sue_action_str, green_str)
        add_bud_rect(fig, 3.0, 1.0, 4.0, 2.0, yao_action_str)
        add_bud_rect(fig, 5.0, 1.0, 6.0, 2.0, bob_action_str)
        add_direc_rect(fig, 0.7, 0.7, 6.3, 2.3, dir_action_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 5,4 5.5,2", color=med_purple)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3,4 3.5,2", color=med_purple)
        add_rect_arrow(fig, 1.75, 2, 1.75, 6.8, green_str)
        add_rect_arrow(fig, 3.43, 2.3, 3.5, 2, med_purple)
        add_rect_arrow(fig, 5.41, 2.3, 5.5, 2, med_purple)

        fig.add_trace(
            plotly_Scatter(
                x=[4.0, 4.0],
                y=[9.0, 8.75],
                text=[
                    "Reality Bud Listening Structures",
                    "The voice bud listens to other's action buds and builds a new bud from itself and others",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures1_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_hubunit_base_fig()
        sue_str = "Sue"
        bob_str = "Bob"
        sue_voice_str = f"{sue_str}.{voice_str()}"
        dir_voice_str = f"{voice_str()}s dir"

        green_str = "Green"
        blue_str = "blue"
        add_bud_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_voice_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_voice_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_str)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_str)

        sue_duty_str = f"{sue_str} duty"
        sue_job_str = f"{sue_str} job"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Econ = project1"
        d_sue1_p4 = f"Money = {default_money_magnitude()} "
        d_bob1_p1 = f"Healer = {bob_str} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Econ = project1"
        d_bob1_p4 = f"Money = {default_money_magnitude()} "
        d_sue2_p1 = f"Healer = {sue_str} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Project = project3"
        d_sue2_p4 = f"Money={default_money_magnitude()} "

        add_bud_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_econ__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_bud_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_econ__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_bud_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_econ__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[2.0],
                y=[13],
                text=["Bud Listening Structures"],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures2_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_hubunit_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_str = "Sue"
        bob_str = "Bob"
        sue_voice_str = f"{sue_str}.{voice_str()}"
        sue_action_str = f"{sue_str}.{action_str()}"
        dir_action_str = f"{action_str()}s dir"
        dir_voice_str = f"{voice_str()}s dir"

        green_str = "Green"
        blue_str = "blue"
        add_bud_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_voice_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_voice_str)
        add_bud_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_action_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_action_str)

        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_str)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=blue_str)
        add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, blue_str)

        sue_duty_str = f"{sue_str} duty"
        sue_job_str = f"{sue_str} job"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Econ = project1"
        d_sue1_p4 = f"Money = {default_money_magnitude()} "
        d_bob1_p1 = f"Healer = {bob_str} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Econ = project1"
        d_bob1_p4 = f"Money = {default_money_magnitude()} "
        d_sue2_p1 = f"Healer = {sue_str} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Project = project3"
        d_sue2_p4 = f"Money={default_money_magnitude()} "

        add_bud_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_econ__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_bud_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_econ__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_bud_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_econ__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Bud Listening Structures",
                    "Flow of Buds to Econs",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures3_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_hubunit_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_str = "Sue"
        bob_str = "Bob"
        yao_str = "Yao"
        sue_voice_str = f"{sue_str}.{voice_str()}"
        sue_action_str = f"{sue_str}.{action_str()}"
        dir_action_str = f"{action_str()}s dir"
        dir_voice_str = f"{voice_str()}s dir"

        green_str = "Green"
        blue_str = "blue"
        blue_str = "blue"
        add_bud_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_voice_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_voice_str)
        add_bud_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_action_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_action_str)

        add_rect_arrow(fig, 3.85, 3.8, 4, 3.6, blue_str)
        add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 7.4,2.1 7.5,2", color=blue_str)
        add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 5.4,2.2 5.5,2", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_str)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_str)
        # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=blue_str)
        # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=blue_str)
        add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, blue_str)

        sue_duty_str = f"{sue_str} duty"
        sue_job_str = f"{sue_str} job"
        bob_job_str = f"{bob_str} job"
        yao_job_str = f"{yao_str} job"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Econ = project1"
        d_sue1_p4 = f"Money = {default_money_magnitude()} "

        add_bud_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_bud_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_econ__rect(
            fig, 2.7, 0.7, 8.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_bud_rect(fig, 5.0, 1.0, 6.0, 2.0, yao_job_str)
        add_bud_rect(fig, 7.0, 1.0, 8.0, 2.0, bob_job_str)

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Bud Listening Structures",
                    "Flow of Buds to Econs",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def fund_explanation0(
    x_bud: BudUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    fig = display_ideatree(x_bud, mode, False)
    fig.update_xaxes(range=[-1, 11])
    fig.update_yaxes(range=[-5, 3])

    green_str = "Green"
    blue_str = "blue"
    blue_str = "blue"
    d_sue1_p1 = "How fund is distributed."
    d_sue1_p2 = "Regular Fund: Green arrows, all fund_coins end up at AcctUnits"
    d_sue1_p3 = "Agenda Fund: Blue arrows, fund_coins from active tasks"
    d_sue1_p4 = f"Money = {default_money_magnitude()} "
    teamunit_str = "      Awardlinks"
    add_bud_rect(fig, 2, -0.3, 3, 0.3, teamunit_str)
    add_rect_arrow(fig, 2, 0.1, 1.2, 0.1, green_str)
    add_rect_arrow(fig, 2, -0.1, 1.2, -0.1, blue_str)
    add_bud_rect(fig, 4, -1.2, 5, -0.8, teamunit_str)
    add_rect_arrow(fig, 4, -0.9, 3.1, -0.9, green_str)
    add_rect_arrow(fig, 4, -1.1, 3.1, -1.1, blue_str)
    add_bud_rect(fig, 4, -3.2, 5, -2.8, teamunit_str)
    add_rect_arrow(fig, 4, -2.9, 3.1, -2.9, green_str)
    add_econ__rect(fig, -0.5, -4.5, 10, 2.3, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    groupbox_str = "GroupBox"
    orange_str = "orange"
    add_bud_rect(fig, 5.5, -0.2, 6.25, 0.4, groupbox_str, orange_str)
    add_bud_rect(fig, 5.5, -0.8, 6.25, -0.2, groupbox_str, orange_str)
    add_bud_rect(fig, 5.5, -1.4, 6.25, -0.8, groupbox_str, orange_str)
    add_rect_arrow(fig, 9, -3.9, 3.1, -3.9, green_str)
    add_rect_arrow(fig, 9, -1.9, 3.1, -1.9, green_str)
    add_rect_arrow(fig, 9, -2.1, 3.1, -2.1, blue_str)
    add_rect_arrow(fig, 5.5, 0.1, 3, 0.1, green_str)
    add_rect_arrow(fig, 5.5, -0.1, 3, -0.1, blue_str)
    add_rect_arrow(fig, 5.5, -0.9, 5, -0.9, green_str)
    add_rect_arrow(fig, 5.5, -1.1, 5, -1.1, blue_str)
    add_rect_arrow(fig, 5.5, -1.3, 5, -2.9, green_str)
    membership_str = "membership"
    darkred_str = "DarkRed"
    add_bud_rect(fig, 7, 0.4, 7.75, 1, membership_str, darkred_str)
    add_bud_rect(fig, 7, -0.2, 7.75, 0.4, membership_str, darkred_str)
    add_bud_rect(fig, 7, -0.8, 7.75, -0.2, membership_str, darkred_str)
    add_bud_rect(fig, 7, -1.4, 7.75, -0.8, membership_str, darkred_str)
    add_rect_arrow(fig, 7, -0.4, 6.25, -0.4, blue_str)
    add_rect_arrow(fig, 7, -0.6, 6.25, -0.6, green_str)
    add_rect_arrow(fig, 9, -0.4, 7.75, -0.4, blue_str)
    add_rect_arrow(fig, 9, -0.6, 7.75, -0.6, green_str)
    acctunit_str = "acctunit"
    purple_str = "purple"
    add_bud_rect(fig, 9, -0.4, 9.75, 0.2, acctunit_str, purple_str)
    add_bud_rect(fig, 9, -1.0, 9.75, -0.4, acctunit_str, purple_str)
    add_bud_rect(fig, 9, -1.6, 9.75, -1.0, acctunit_str, purple_str)
    add_bud_rect(fig, 9, -2.2, 9.75, -1.6, acctunit_str, purple_str)
    add_bud_rect(fig, 9, -4.0, 9.75, -2.2, acctunit_str, purple_str)

    conditional_fig_show(fig, graphics_bool)
    # fig.add_trace(
    #     plotly_Scatter(
    #         x=[1.0],
    #         y=[3.75],
    #         text=["What Jaar Buds Are Made of Explanation 0"],
    #         mode="text",
    #     )
    # )
