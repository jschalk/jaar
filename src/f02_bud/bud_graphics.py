from src.f00_instrument.plotly_toolbox import (
    conditional_fig_show,
    add_simp_rect,
    add_rect_arrow,
    add_keep__rect,
)
from src.f01_road.road import get_parent_road, RoadUnit, is_sub_road
from src.f02_bud.item import ItemUnit
from src.f02_bud.bud import BudUnit
from src.f02_bud.report import get_bud_acctunits_dataframe, get_bud_agenda_dataframe
from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)


def _get_dot_diameter(x_ratio: float):
    return ((x_ratio**0.4)) * 100


def _get_parent_y(x_item: ItemUnit, itemunit_y_coordinate_dict: dict) -> RoadUnit:
    parent_road = get_parent_road(x_item.get_road())
    return itemunit_y_coordinate_dict.get(parent_road)


def _get_color_for_itemunit_trace(x_itemunit: ItemUnit, mode: str) -> str:
    if mode is None:
        if x_itemunit._level == 0:
            return "Red"
        elif x_itemunit._level == 1:
            return "Pink"
        elif x_itemunit._level == 2:
            return "Green"
        elif x_itemunit._level == 3:
            return "Blue"
        elif x_itemunit._level == 4:
            return "Purple"
        elif x_itemunit._level == 5:
            return "Gold"
        else:
            return "Black"
    elif mode == "Task":
        return "Red" if x_itemunit.pledge else "Pink"
    elif mode == "Keep":
        if x_itemunit.problem_bool and x_itemunit.healerlink.any_healer_id_exists():
            return "Purple"
        elif x_itemunit.healerlink.any_healer_id_exists():
            return "Blue"
        elif x_itemunit.problem_bool:
            return "Red"
        else:
            return "Pink"


def _add_individual_trace(
    trace_list: list,
    anno_list: list,
    parent_y,
    source_y,
    kid_item: ItemUnit,
    mode: str,
):
    trace_list.append(
        plotly_Scatter(
            x=[kid_item._level - 1, kid_item._level],
            y=[parent_y, source_y],
            marker_size=_get_dot_diameter(kid_item._fund_ratio),
            name=kid_item._lx,
            marker_color=_get_color_for_itemunit_trace(kid_item, mode=mode),
        )
    )
    anno_list.append(
        dict(
            x=kid_item._level,
            y=source_y + (_get_dot_diameter(kid_item._fund_ratio) / 150) + 0.002,
            text=kid_item._lx,
            showarrow=False,
        )
    )


def _create_itemunit_traces(
    trace_list, anno_list, x_bud: BudUnit, source_y: float, mode: str
):
    items = [x_bud._itemroot]
    y_itemunit_y_coordinate_dict = {None: 0}
    prev_road = x_bud._itemroot.get_road()
    source_y = 0
    while items != []:
        x_item = items.pop(-1)
        if is_sub_road(x_item.get_road(), prev_road) is False:
            source_y -= 1
        _add_individual_trace(
            trace_list=trace_list,
            anno_list=anno_list,
            parent_y=_get_parent_y(x_item, y_itemunit_y_coordinate_dict),
            source_y=source_y,
            kid_item=x_item,
            mode=mode,
        )
        items.extend(iter(x_item._kids.values()))
        y_itemunit_y_coordinate_dict[x_item.get_road()] = source_y
        prev_road = x_item.get_road()


def _update_layout_fig(x_fig: plotly_Figure, mode: str, x_bud: BudUnit):
    x_title = "Tree with lines Layout"
    if mode == "Task":
        x_title = "Item Tree with task items in Red."
    x_title += f" (Items: {len(x_bud._item_dict)})"
    x_title += f" (_sum_healerlink_share: {x_bud._sum_healerlink_share})"
    x_title += f" (_keeps_justified: {x_bud._keeps_justified})"
    x_fig.update_layout(title_text=x_title, font_size=12)


def display_itemtree(
    x_bud: BudUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    """Mode can be None, Task, Keep"""

    x_bud.settle_bud()
    x_fig = plotly_Figure()
    source_y = 0
    trace_list = []
    anno_list = []
    _create_itemunit_traces(trace_list, anno_list, x_bud, source_y, mode=mode)
    _update_layout_fig(x_fig, mode, x_bud=x_bud)
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


def get_bud_accts_plotly_fig(x_bud: BudUnit) -> plotly_Figure:
    column_header_list = [
        "acct_id",
        "_credor_respect",
        "credit_belief",
        "_debtor_respect",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
    ]
    df = get_bud_acctunits_dataframe(x_bud)
    df.insert(1, "_credor_respect", x_bud.credor_respect)
    df.insert(4, "_debtor_respect", x_bud.debtor_respect)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.acct_id,
                df._credor_respect,
                df.credit_belief,
                df._debtor_respect,
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
    fig_title = f"OwnerID '{x_bud._owner_id}' bud accts metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_bud_agenda_plotly_fig(x_bud: BudUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "fund_ratio",
        "_lx",
        "_parent_road",
    ]
    df = get_bud_agenda_dataframe(x_bud)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.fund_ratio,
                df._lx,
                df._parent_road,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"OwnerID '{x_bud._owner_id}' bud agenda"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

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


def create_item_rect(
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


def get_budunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 4])
    fig.update_yaxes(range=[0, 4])
    return fig


def budunit_explanation0(graphics_bool) -> plotly_Figure:
    if not graphics_bool:
        return
    fig = get_budunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")
    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[3.75],
            text=["What Jaar Buds Are Made of Explanation 0"],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def budunit_explanation1(graphics_bool) -> plotly_Figure:
    fig = get_budunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    add_group_rect(fig, base_w, base_h, 2, 0, 0.2, "group1")
    add_group_rect(fig, base_w, base_h, 2, 0.2, 0.4, "group2")
    add_group_rect(fig, base_w, base_h, 2, 0.4, 0.6, "group3")
    add_group_rect(fig, base_w, base_h, 2, 0.6, 1, "group4")
    add_people_rect(fig, base_w, base_h, 0, 0, 0.3, "acct0")
    add_people_rect(fig, base_w, base_h, 0, 0.3, 0.5, "acct1")
    add_people_rect(fig, base_w, base_h, 0, 0.5, 0.7, "acct2")
    add_people_rect(fig, base_w, base_h, 0, 0.7, 1, "acct3")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Jaar Buds Are Made of Explanation 1",
                "People are in blue",
                "Groups are in green",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def budunit_explanation2(graphics_bool) -> plotly_Figure:
    fig = get_budunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_item_rect(fig, base_w, base_h, 0, 0, 1, "Root Item")
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Jaar Buds Are Made of Explanation 1",
                "Pledges are from Items",
                "All items build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def budunit_explanation3(graphics_bool) -> plotly_Figure:
    fig = get_budunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_item_rect(fig, base_w, base_h, 2, 0.4, 0.7, "Sub Item")
    create_item_rect(fig, base_w, base_h, 2, 0.3, 0.4, "Sub Item")
    create_item_rect(fig, base_w, base_h, 1, 0, 0.3, "Sub Item")
    create_item_rect(fig, base_w, base_h, 1, 0.3, 0.7, "Sub Item")
    create_item_rect(fig, base_w, base_h, 1, 0.7, 1, "Sub Item")
    create_item_rect(fig, base_w, base_h, 0, 0, 1, "Root Item")
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Jaar Buds Are Made of Explanation 1",
                "Pledges are from Items",
                "All items build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def budunit_explanation4(graphics_bool) -> plotly_Figure:
    fig = get_budunit_base_fig()

    # Add shapes
    base_w = 0.1
    base_h = 0.125
    create_item_rect(fig, base_w, base_h, 2, 0.4, 0.7, "Premise against Pledge")
    create_item_rect(fig, base_w, base_h, 2, 0.1, 0.4, "Premise for Pledge")
    create_item_rect(fig, base_w, base_h, 1, 0, 0.1, "Item")
    create_item_rect(fig, base_w, base_h, 1, 0.1, 0.7, "Pledge Reason Base")
    create_item_rect(fig, base_w, base_h, 0, 0, 1, "Root Item")
    create_item_rect(fig, base_w, base_h, 1, 0.7, 1, "Pledge Itself", True)
    add_group_rect(fig, base_w, base_h, 1, 0, 1, "groups")
    add_people_rect(fig, base_w, base_h, 0, 0, 1, "people")

    fig.add_trace(
        plotly_Scatter(
            x=[2.0, 2.00, 2.00],
            y=[3.75, 3.5, 3.25],
            text=[
                "What Jaar Buds Are Made of Explanation 1",
                "Some Items are pledges, others are reasons for pledges",
                "All items build from one",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)


def fund_explanation0(
    x_bud: BudUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    fig = display_itemtree(x_bud, mode, False)
    fig.update_xaxes(range=[-1, 11])
    fig.update_yaxes(range=[-5.5, 3])

    green_str = "Green"
    blue_str = "blue"
    blue_str = "blue"
    d_sue1_title = "How fund is distributed."
    teamunit_str = "      AwardHeirs"
    add_rect_arrow(fig, 0.6, -0.1, 0.1, -0.1, "Purple")
    add_rect_arrow(fig, 0.6, -0.8, 0.1, -0.1, "Purple")
    add_rect_arrow(fig, 1.8, -1.1, 1.2, -1.1, "Purple")
    add_rect_arrow(fig, 1.8, -2.4, 1.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -1.1, 2.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -1.6, 2.2, -1.1, "Purple")
    add_rect_arrow(fig, 2.7, -3.1, 2.2, -3.1, "Purple")
    add_rect_arrow(fig, 2.7, -3.6, 2.2, -3.1, "Purple")

    add_simp_rect(fig, 2, -0.3, 3, 0.3, teamunit_str)
    add_rect_arrow(fig, 2, 0.1, 1.2, 0.1, green_str)
    add_rect_arrow(fig, 2, -0.1, 1.2, -0.1, blue_str)
    add_simp_rect(fig, 4, -1.2, 5, -0.8, teamunit_str)
    add_rect_arrow(fig, 4, -0.9, 3.1, -0.9, green_str)
    add_rect_arrow(fig, 4, -1.1, 3.1, -1.1, blue_str)
    add_simp_rect(fig, 4, -3.2, 5, -2.8, teamunit_str)
    add_rect_arrow(fig, 4, -2.9, 3.1, -2.9, green_str)
    add_keep__rect(fig, -0.5, -4.5, 10, 2.3, d_sue1_title, "", "", "")
    d_sue1_p0 = "Fund Source is ItemRoot. Each Item fund range calculated by mass "
    d_sue1_p1 = "ItemRoot Fund ranges: Black arrows. Sum of childless Item's funds equal itemroot's fund "
    d_sue1_p2 = "Regular Fund: Green arrows, all fund_coins end up at AcctUnits"
    d_sue1_p3 = "Agenda Fund: Blue arrows, fund_coins from active tasks"
    d_sue1_p4 = f"fund_pool = {x_bud.fund_pool} "
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
    acctunit_str = "acctunit"
    purple_str = "purple"
    add_simp_rect(fig, 9, -0.4, 9.75, 0.2, acctunit_str, "gold")
    add_simp_rect(fig, 9, -1.0, 9.75, -0.4, acctunit_str, "gold")
    add_simp_rect(fig, 9, -1.6, 9.75, -1.0, acctunit_str, "gold")
    add_simp_rect(fig, 9, -2.2, 9.75, -1.6, acctunit_str, "gold")
    add_simp_rect(fig, 9, -4.0, 9.75, -2.2, acctunit_str, "gold")

    fund_t0 = "BudUnit.fund_pool"
    fund_t1_0 = "ItemUnit._fund_onset"
    fund_t1_1 = "ItemUnit._fund_cease"
    fund_t2_0 = "AwardHeir._fund_give"
    fund_t2_1 = "AwardHeir._fund_take"

    fund_trace3_0 = "GroupUnit._fund_give"
    fund_trace3_1 = "GroupUnit._fund_take"
    fund_trace3_2 = "GroupUnit._fund_agenda_give"
    fund_trace3_3 = "GroupUnit._fund_agenda_take"

    fund_trace4_0 = "MemberShip._fund_give"
    fund_trace4_1 = "MemberShip._fund_take"
    fund_trace4_2 = "MemberShip._fund_agenda_give"
    fund_trace4_3 = "MemberShip._fund_agenda_take"

    fund_trace5_0 = "AcctUnit._fund_give"
    fund_trace5_1 = "AcctUnit._fund_take"
    fund_trace5_2 = "AcctUnit._fund_agenda_give"
    fund_trace5_3 = "AcctUnit._fund_agenda_take"

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
