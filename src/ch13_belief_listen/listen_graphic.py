from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch01_py.plotly_toolbox import (
    add_2_curve,
    add_direc_rect,
    add_keep__rect,
    add_rect_arrow,
    add_simp_rect,
    conditional_fig_show,
)
from src.ch03_allot.allot import default_pool_num
from src.ch07_belief_logic.belief_graphics import display_plantree
from src.ch07_belief_logic.belief_main import BeliefUnit


def get_packfilehandler_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def get_listen_structures0_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        sue_str = "Sue"
        bob_str = "Bob"
        yao_str = "Yao"
        fig = get_packfilehandler_base_fig()
        sue_gut_str = f"{sue_str}.gut"
        sue_job_str = f"{sue_str}.job"
        yao_job_str = f"{yao_str}.job"
        bob_job_str = f"{bob_str}.job"
        dir_job_str = f"jobs directory"
        dir_gut_str = f"guts directory"

        green_str = "Green"
        med_purple = "MediumPurple"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 6.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, 1.0, 2.0, 2.0, sue_job_str, green_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, yao_job_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, bob_job_str)
        add_direc_rect(fig, 0.7, 0.7, 6.3, 2.3, dir_job_str)
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
                    "momentity Belief Listening Structures",
                    "The gut belief listens to other's job beliefs and builds a new belief from itself and others",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures1_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_packfilehandler_base_fig()
        sue_str = "Sue"
        bob_str = "Bob"
        sue_gut_str = f"{sue_str}.gut"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        blue_str = "blue"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_str)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_str)

        sue_duty_str = f"{sue_str} duty"
        sue_vision_str = f"{sue_str} vision"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Money = {default_pool_num()} "
        d_bob1_p1 = f"Healer = {bob_str} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Keep = keep1"
        d_bob1_p4 = f"Money = {default_pool_num()} "
        d_sue2_p1 = f"Healer = {sue_str} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Keep = keep3"
        d_sue2_p4 = f"Money={default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_keep__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_simp_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_keep__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[2.0],
                y=[13],
                text=["Belief Listening Structures"],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures2_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_packfilehandler_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_str = "Sue"
        bob_str = "Bob"
        sue_gut_str = f"{sue_str}.gut"
        sue_job_str = f"{sue_str}.job"
        dir_job_str = f"jobs dir"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        blue_str = "blue"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_job_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_job_str)

        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_str)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=blue_str)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=blue_str)
        add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, blue_str)

        sue_duty_str = f"{sue_str} duty"
        sue_vision_str = f"{sue_str} vision"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Money = {default_pool_num()} "
        d_bob1_p1 = f"Healer = {bob_str} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Keep = keep1"
        d_bob1_p4 = f"Money = {default_pool_num()} "
        d_sue2_p1 = f"Healer = {sue_str} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Keep = keep3"
        d_sue2_p4 = f"Money={default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_keep__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_simp_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_keep__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Belief Listening Structures",
                    "Flow of Beliefs to Keeps",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures3_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_packfilehandler_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_str = "Sue"
        bob_str = "Bob"
        yao_str = "Yao"
        sue_gut_str = f"{sue_str}.gut"
        sue_job_str = f"{sue_str}.job"
        dir_job_str = f"jobs dir"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        blue_str = "blue"
        blue_str = "blue"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_job_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_job_str)

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
        sue_vision_str = f"{sue_str} vision"
        bob_vision_str = f"{bob_str} vision"
        yao_vision_str = f"{yao_str} vision"
        d_sue1_p1 = f"Healer = {sue_str} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Money = {default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 8.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, yao_vision_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, bob_vision_str)

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Belief Listening Structures",
                    "Flow of Beliefs to Keeps",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def fund_graph13(
    x_belief: BeliefUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    fig = display_plantree(x_belief, mode, False)
    fig.update_xaxes(range=[-1, 11])
    fig.update_yaxes(range=[-5, 3])

    green_str = "Green"
    blue_str = "blue"
    blue_str = "blue"
    d_sue1_p1 = "How fund is distributed."
    d_sue1_p2 = "Regular Fund: Green arrows, all fund_grains end up at VoiceUnits"
    d_sue1_p3 = "Agenda Fund: Blue arrows, fund_grains from active tasks"
    d_sue1_p4 = f"Money = {default_pool_num()} "
    laborunit_str = "      AwardUnits"
    add_simp_rect(fig, 2, -0.3, 3, 0.3, laborunit_str)
    add_rect_arrow(fig, 2, 0.1, 1.2, 0.1, green_str)
    add_rect_arrow(fig, 2, -0.1, 1.2, -0.1, blue_str)
    add_simp_rect(fig, 4, -1.2, 5, -0.8, laborunit_str)
    add_rect_arrow(fig, 4, -0.9, 3.1, -0.9, green_str)
    add_rect_arrow(fig, 4, -1.1, 3.1, -1.1, blue_str)
    add_simp_rect(fig, 4, -3.2, 5, -2.8, laborunit_str)
    add_rect_arrow(fig, 4, -2.9, 3.1, -2.9, green_str)
    add_keep__rect(fig, -0.5, -4.5, 10, 2.3, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    groupunit_str = "GroupUnit"
    orange_str = "orange"
    add_simp_rect(fig, 5.5, -0.2, 6.25, 0.4, groupunit_str, orange_str)
    add_simp_rect(fig, 5.5, -0.8, 6.25, -0.2, groupunit_str, orange_str)
    add_simp_rect(fig, 5.5, -1.4, 6.25, -0.8, groupunit_str, orange_str)
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
    add_simp_rect(fig, 7, 0.4, 7.75, 1, membership_str, darkred_str)
    add_simp_rect(fig, 7, -0.2, 7.75, 0.4, membership_str, darkred_str)
    add_simp_rect(fig, 7, -0.8, 7.75, -0.2, membership_str, darkred_str)
    add_simp_rect(fig, 7, -1.4, 7.75, -0.8, membership_str, darkred_str)
    add_rect_arrow(fig, 7, -0.4, 6.25, -0.4, blue_str)
    add_rect_arrow(fig, 7, -0.6, 6.25, -0.6, green_str)
    add_rect_arrow(fig, 9, -0.4, 7.75, -0.4, blue_str)
    add_rect_arrow(fig, 9, -0.6, 7.75, -0.6, green_str)
    voiceunit_str = "voiceunit"
    purple_str = "purple"
    add_simp_rect(fig, 9, -0.4, 9.75, 0.2, voiceunit_str, purple_str)
    add_simp_rect(fig, 9, -1.0, 9.75, -0.4, voiceunit_str, purple_str)
    add_simp_rect(fig, 9, -1.6, 9.75, -1.0, voiceunit_str, purple_str)
    add_simp_rect(fig, 9, -2.2, 9.75, -1.6, voiceunit_str, purple_str)
    add_simp_rect(fig, 9, -4.0, 9.75, -2.2, voiceunit_str, purple_str)

    conditional_fig_show(fig, graphics_bool)
