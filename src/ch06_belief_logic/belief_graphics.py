from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)
from src.ch00_data_toolbox.plotly_toolbox import (
    add_keep__rect,
    add_rect_arrow,
    add_simp_rect,
    conditional_fig_show,
)
from src.ch01_rope_logic.rope import RopePointer, get_parent_rope, is_sub_rope
from src.ch05_plan_logic.plan import PlanUnit
from src.ch06_belief_logic.belief_main import BeliefUnit
from src.ch06_belief_logic.belief_report import (
    get_belief_agenda_dataframe,
    get_belief_voiceunits_dataframe,
)


def _get_dot_diameter(x_ratio: float):
    return ((x_ratio**0.4)) * 100


def _get_parent_y(x_plan: PlanUnit, planunit_y_coordinate_dict: dict) -> RopePointer:
    parent_rope = get_parent_rope(x_plan.get_plan_rope())
    return planunit_y_coordinate_dict.get(parent_rope)


def _get_color_for_planunit_trace(x_planunit: PlanUnit, mode: str) -> str:
    if mode is None:
        if x_planunit.tree_level == 0:
            return "Red"
        elif x_planunit.tree_level == 1:
            return "Pink"
        elif x_planunit.tree_level == 2:
            return "Green"
        elif x_planunit.tree_level == 3:
            return "Blue"
        elif x_planunit.tree_level == 4:
            return "Purple"
        elif x_planunit.tree_level == 5:
            return "Gold"
        else:
            return "Black"
    elif mode == "Chore":
        return "Red" if x_planunit.task else "Pink"
    elif mode == "Keep":
        if x_planunit.problem_bool and x_planunit.healerunit.any_healer_name_exists():
            return "Purple"
        elif x_planunit.healerunit.any_healer_name_exists():
            return "Blue"
        elif x_planunit.problem_bool:
            return "Red"
        else:
            return "Pink"


def _add_individual_trace(
    trace_list: list,
    anno_list: list,
    parent_y,
    source_y,
    kid_plan: PlanUnit,
    mode: str,
):
    trace_list.append(
        plotly_Scatter(
            x=[kid_plan.tree_level - 1, kid_plan.tree_level],
            y=[parent_y, source_y],
            marker_size=_get_dot_diameter(kid_plan.fund_ratio),
            name=kid_plan.plan_label,
            marker_color=_get_color_for_planunit_trace(kid_plan, mode=mode),
        )
    )
    anno_list.append(
        dict(
            x=kid_plan.tree_level,
            y=source_y + (_get_dot_diameter(kid_plan.fund_ratio) / 150) + 0.002,
            text=kid_plan.plan_label,
            showarrow=False,
        )
    )


def _create_planunit_traces(
    trace_list, anno_list, x_belief: BeliefUnit, source_y: float, mode: str
):
    plans = [x_belief.planroot]
    y_planunit_y_coordinate_dict = {None: 0}
    prev_rope = x_belief.planroot.get_plan_rope()
    source_y = 0
    while plans != []:
        x_plan = plans.pop(-1)
        if is_sub_rope(x_plan.get_plan_rope(), prev_rope) is False:
            source_y -= 1
        _add_individual_trace(
            trace_list=trace_list,
            anno_list=anno_list,
            parent_y=_get_parent_y(x_plan, y_planunit_y_coordinate_dict),
            source_y=source_y,
            kid_plan=x_plan,
            mode=mode,
        )
        plans.extend(iter(x_plan.kids.values()))
        y_planunit_y_coordinate_dict[x_plan.get_plan_rope()] = source_y
        prev_rope = x_plan.get_plan_rope()


def _update_layout_fig(x_fig: plotly_Figure, mode: str, x_belief: BeliefUnit):
    fig_label = "Tree with lines Layout"
    if mode == "Chore":
        fig_label = "Plan Tree with chore plans in Red."
    fig_label += f" (Plans: {len(x_belief._plan_dict)})"
    fig_label += f" (sum_healerunit_share: {x_belief.sum_healerunit_share})"
    fig_label += f" (keeps_justified: {x_belief.keeps_justified})"
    x_fig.update_layout(title_text=fig_label, font_size=12)


def display_plantree(
    x_belief: BeliefUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    """Mode can be None, Chore, Keep"""

    x_belief.cashout()
    x_fig = plotly_Figure()
    source_y = 0
    trace_list = []
    anno_list = []
    _create_planunit_traces(trace_list, anno_list, x_belief, source_y, mode=mode)
    _update_layout_fig(x_fig, mode, x_belief=x_belief)
    while trace_list:
        x_trace = trace_list.pop(-1)
        x_fig.add_trace(x_trace)
        x_anno = anno_list.pop(-1)
        x_fig.add_annotation(
            x=x_anno.get("x"),
            y=x_anno.get("y"),
            text=x_anno.get("text"),
            font_size=20,
            showarrow=False,
        )
    if graphics_bool:
        conditional_fig_show(x_fig, graphics_bool)
    else:
        return x_fig


def get_belief_voices_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "voice_name",
        "_credor_respect",
        "voice_cred_points",
        "_debtor_respect",
        "voice_debt_points",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
    ]
    df = get_belief_voiceunits_dataframe(x_belief)
    df.insert(1, "_credor_respect", x_belief.credor_respect)
    df.insert(4, "_debtor_respect", x_belief.debtor_respect)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.voice_name,
                df._credor_respect,
                df.voice_cred_points,
                df._debtor_respect,
                df.voice_debt_points,
                df.fund_give,
                df.fund_take,
                df.fund_agenda_give,
                df.fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"BeliefName '{x_belief.belief_name}' belief voices metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_belief_agenda_plotly_fig(x_belief: BeliefUnit) -> plotly_Figure:
    column_header_list = [
        "belief_name",
        "fund_ratio",
        "plan_label",
        "parent_rope",
    ]
    df = get_belief_agenda_dataframe(x_belief)
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
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"BeliefName '{x_belief.belief_name}' belief agenda"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def add_rect_str(fig, x, y, text):
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=x,
        y=y,
        text=text,
        showarrow=False,
    )


def create_plan_rect(
    fig: plotly_Figure,
    base_width,
    base_h,
    level,
    level_width0,
    level_width1,
    display_str,
    show_red: bool = False,
):
    level_bump = level * 0.125
    home_form_x0 = base_width + 0.1
    home_form_x1 = 1 - base_width - 0.1
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * level_width0)
    shape_x1 = home_form_x0 + (home_width * level_width1)
    shape_y0 = level_bump + base_h + 0.25
    shape_y1 = level_bump + base_h + 0.375
    x_color = "Red" if show_red else "RoyalBlue"
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_str(fig, x=text_x, y=text_y, text=display_str)


def add_group_rect(
    fig: plotly_Figure,
    base_width,
    base_h,
    level,
    level_width0,
    level_width1,
    display_str,
):
    # shape_x0 = base_width
    # shape_x1 = 1 - base_width
    # shape_y0 = base_h + 0.125
    # shape_y1 = base_h + 0.25

    level_bump = level * 0.125
    home_form_x0 = base_width
    home_form_x1 = 1 - base_width
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * level_width0)
    shape_x1 = home_form_x0 + (home_width * level_width1)
    shape_y0 = level_bump + base_h
    shape_y1 = level_bump + base_h + 0.125

    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(color="Green", width=8),
        fillcolor=None,
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_str(fig, x=text_x, y=text_y, text=display_str)


def add_people_rect(
    fig: plotly_Figure,
    base_width,
    base_h,
    level,
    level_width0,
    level_width1,
    display_str,
):
    level_bump = level * 0.125
    home_form_x0 = base_width
    home_form_x1 = 1 - base_width
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * level_width0)
    shape_x1 = home_form_x0 + (home_width * level_width1)
    shape_y0 = level_bump + base_h
    shape_y1 = level_bump + base_h + 0.125
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color="DarkRed",
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_str(fig, x=text_x, y=text_y, text=display_str)


def get_beliefunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 4])
    fig.update_yaxes(range=[0, 4])
    return fig


def beliefunit_graph0(graphics_bool) -> plotly_Figure:
    if not graphics_bool:
        return
    fig = get_beliefunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")
    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[3.75],
            text=["What Beliefs Are Made Of: Graph 0"],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def beliefunit_graph1(graphics_bool) -> plotly_Figure:
    fig = get_beliefunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    add_group_rect(fig, base_w, base_h, 2, 0, 0.2, "group1")
    add_group_rect(fig, base_w, base_h, 2, 0.2, 0.4, "group2")
    add_group_rect(fig, base_w, base_h, 2, 0.4, 0.6, "group3")
    add_group_rect(fig, base_w, base_h, 2, 0.6, 1, "group4")
    add_people_rect(fig, base_w, base_h, 0, 0, 0.3, "voice0")
    add_people_rect(fig, base_w, base_h, 0, 0.3, 0.5, "voice1")
    add_people_rect(fig, base_w, base_h, 0, 0.5, 0.7, "voice2")
    add_people_rect(fig, base_w, base_h, 0, 0.7, 1, "voice3")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Beliefs Are Made Of: Graph 1",
                "People are in blue",
                "Groups are in green",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def beliefunit_graph2(graphics_bool) -> plotly_Figure:
    fig = get_beliefunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_plan_rect(fig, base_w, base_h, 0, 0, 1, "Root Plan")
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Beliefs Are Made Of: Graph 1",
                "Tasks are from Plans",
                "All plans build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def beliefunit_graph3(graphics_bool) -> plotly_Figure:
    fig = get_beliefunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_plan_rect(fig, base_w, base_h, 2, 0.4, 0.7, "Sub Plan")
    create_plan_rect(fig, base_w, base_h, 2, 0.3, 0.4, "Sub Plan")
    create_plan_rect(fig, base_w, base_h, 1, 0, 0.3, "Sub Plan")
    create_plan_rect(fig, base_w, base_h, 1, 0.3, 0.7, "Sub Plan")
    create_plan_rect(fig, base_w, base_h, 1, 0.7, 1, "Sub Plan")
    create_plan_rect(fig, base_w, base_h, 0, 0, 1, "Root Plan")
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Beliefs Are Made Of: Graph 1",
                "Tasks are from Plans",
                "All plans build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def beliefunit_graph4(graphics_bool) -> plotly_Figure:
    fig = get_beliefunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_plan_rect(fig, base_w, base_h, 2, 0.4, 0.7, "Case against Task")
    create_plan_rect(fig, base_w, base_h, 2, 0.1, 0.4, "Case for Task")
    create_plan_rect(fig, base_w, base_h, 1, 0, 0.1, "Plan")
    create_plan_rect(fig, base_w, base_h, 1, 0.1, 0.7, "Task Reason Base")
    create_plan_rect(fig, base_w, base_h, 0, 0, 1, "Root Plan")
    create_plan_rect(fig, base_w, base_h, 1, 0.7, 1, "Task Itself", True)
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Beliefs Are Made Of: Graph 1",
                "Some Plans are tasks, others are reasons for tasks",
                "All plans build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def fund_graph0(
    x_belief: BeliefUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    fig = display_plantree(x_belief, mode, False)
    fig.update_xaxes(range=[-1, 11])
    fig.update_yaxes(range=[-5.5, 3])

    green_str = "Green"
    blue_str = "blue"
    blue_str = "blue"
    d_sue1_label = "How fund is distributed."
    laborunit_str = "      AwardHeirs"
    add_rect_arrow(fig, 0.6, -0.1, 0.1, -0.1, "Purple")
    add_rect_arrow(fig, 0.6, -0.8, 0.1, -0.1, "Purple")
    add_rect_arrow(fig, 1.8, -1.1, 1.2, -1.1, "Purple")
    add_rect_arrow(fig, 1.8, -2.4, 1.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -1.1, 2.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -1.6, 2.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -3.1, 2.2, -3.1, "Purple")
    add_rect_arrow(fig, 2.7, -3.6, 2.2, -3.1, "Purple")

    add_simp_rect(fig, 2, -0.3, 3, 0.3, laborunit_str)
    add_rect_arrow(fig, 2, 0.1, 1.2, 0.1, green_str)
    add_rect_arrow(fig, 2, -0.1, 1.2, -0.1, blue_str)
    add_simp_rect(fig, 4, -1.2, 5, -0.8, laborunit_str)
    add_rect_arrow(fig, 4, -0.9, 3.1, -0.9, green_str)
    add_rect_arrow(fig, 4, -1.1, 3.1, -1.1, blue_str)
    add_simp_rect(fig, 4, -3.2, 5, -2.8, laborunit_str)
    add_rect_arrow(fig, 4, -2.9, 3.1, -2.9, green_str)
    add_keep__rect(fig, -0.5, -4.5, 10, 2.3, d_sue1_label, "", "", "")
    d_sue1_p0 = "Fund Source is PlanRoot. Each Plan fund range calculated by star "
    d_sue1_p1 = "PlanRoot Fund ranges: Black arrows. Sum of childless Plan's funds equal planroot's fund "
    d_sue1_p2 = "Regular Fund: Green arrows, all fund_iotas end up at VoiceUnits"
    d_sue1_p3 = "Agenda Fund: Blue arrows, fund_iotas from active chores"
    d_sue1_p4 = f"fund_pool = {x_belief.fund_pool} "
    fig.add_trace(
        plotly_Scatter(
            x=[4, 4, 4, 4, 4],
            y=[2, 1.75, 1.50, 1.25, 1],
            text=[d_sue1_p0, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4],
            mode="text",
        )
    )
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
    add_simp_rect(fig, 9, -0.4, 9.75, 0.2, voiceunit_str, "gold")
    add_simp_rect(fig, 9, -1.0, 9.75, -0.4, voiceunit_str, "gold")
    add_simp_rect(fig, 9, -1.6, 9.75, -1.0, voiceunit_str, "gold")
    add_simp_rect(fig, 9, -2.2, 9.75, -1.6, voiceunit_str, "gold")
    add_simp_rect(fig, 9, -4.0, 9.75, -2.2, voiceunit_str, "gold")

    fund_t0 = "BeliefUnit.fund_pool"
    fund_t1_0 = "PlanUnit.fund_onset"
    fund_t1_1 = "PlanUnit.fund_cease"
    fund_t2_0 = "AwardHeir.fund_give"
    fund_t2_1 = "AwardHeir.fund_take"

    fund_trace3_0 = "GroupUnit.fund_give"
    fund_trace3_1 = "GroupUnit.fund_take"
    fund_trace3_2 = "GroupUnit.fund_agenda_give"
    fund_trace3_3 = "GroupUnit.fund_agenda_take"

    fund_trace4_0 = "MemberShip.fund_give"
    fund_trace4_1 = "MemberShip.fund_take"
    fund_trace4_2 = "MemberShip.fund_agenda_give"
    fund_trace4_3 = "MemberShip.fund_agenda_take"

    fund_trace5_0 = "VoiceUnit.fund_give"
    fund_trace5_1 = "VoiceUnit.fund_take"
    fund_trace5_2 = "VoiceUnit.fund_agenda_give"
    fund_trace5_3 = "VoiceUnit.fund_agenda_take"

    tracex_list = [fund_t0, fund_t1_0, fund_t1_1, fund_t2_0, fund_t2_1]
    fig.add_trace(
        plotly_Scatter(
            y=[-5, -4.85, -5.15, -4.85, -5.15],
            x=[0, 2, 2, 4, 4],
            text=tracex_list,
            mode="text",
        )
    )
    trace3_list = [fund_trace3_0, fund_trace3_1, fund_trace3_2, fund_trace3_3]
    fig.add_trace(
        plotly_Scatter(
            y=[-4.65, -4.85, -5.15, -5.35],
            x=[6, 6, 6, 6],
            text=trace3_list,
            mode="text",
        )
    )
    trace4_list = [fund_trace4_0, fund_trace4_1, fund_trace4_2, fund_trace4_3]
    fig.add_trace(
        plotly_Scatter(
            y=[-4.65, -4.85, -5.15, -5.35],
            x=[8, 8, 8, 8],
            text=trace4_list,
            mode="text",
        )
    )
    trace5_list = [fund_trace5_0, fund_trace5_1, fund_trace5_2, fund_trace5_3]
    fig.add_trace(
        plotly_Scatter(
            y=[-4.65, -4.85, -5.15, -5.35],
            x=[10, 10, 10, 10],
            text=trace5_list,
            mode="text",
        )
    )

    conditional_fig_show(fig, graphics_bool)
