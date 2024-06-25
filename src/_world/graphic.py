from src._road.road import get_parent_road, RoadUnit, is_sub_road
from src._world.idea import IdeaUnit
from src._world.world import WorldUnit
from src._world.report import (
    get_world_otherunits_dataframe,
    get_world_agenda_dataframe,
)
from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)


def _get_dot_diameter(x_ratio: float):
    return ((x_ratio**0.4)) * 100


def _get_parent_y(x_idea: IdeaUnit, ideaunit_y_coordinate_dict: dict) -> RoadUnit:
    parent_road = get_parent_road(x_idea.get_road())
    return ideaunit_y_coordinate_dict.get(parent_road)


def _get_color_for_ideaunit_trace(x_ideaunit: IdeaUnit, mode: str) -> str:
    if mode is None:
        if x_ideaunit._level == 0:
            return "Red"
        elif x_ideaunit._level == 1:
            return "Pink"
        elif x_ideaunit._level == 2:
            return "Green"
        elif x_ideaunit._level == 3:
            return "Blue"
        elif x_ideaunit._level == 4:
            return "Purple"
        elif x_ideaunit._level == 5:
            return "Gold"
        else:
            return "Black"
    elif mode == "Task":
        return "Red" if x_ideaunit.pledge else "Pink"
    elif mode == "Econ":
        if x_ideaunit._problem_bool and x_ideaunit._healerhold.any_belief_id_exists():
            return "Purple"
        elif x_ideaunit._healerhold.any_belief_id_exists():
            return "Blue"
        elif x_ideaunit._problem_bool:
            return "Red"
        else:
            return "Pink"


def _add_individual_trace(
    trace_list: list,
    anno_list: list,
    parent_y,
    source_y,
    kid_idea: IdeaUnit,
    mode: str,
):
    trace_list.append(
        plotly_Scatter(
            x=[kid_idea._level - 1, kid_idea._level],
            y=[parent_y, source_y],
            marker_size=_get_dot_diameter(kid_idea._world_importance),
            name=kid_idea._label,
            marker_color=_get_color_for_ideaunit_trace(kid_idea, mode=mode),
        )
    )
    anno_list.append(
        dict(
            x=kid_idea._level,
            y=source_y + (_get_dot_diameter(kid_idea._world_importance) / 150) + 0.002,
            text=kid_idea._label,
            showarrow=False,
        )
    )


def _add_ideaunit_traces(
    trace_list, anno_list, x_world: WorldUnit, source_y: float, mode: str
):
    ideas = [x_world._idearoot]
    y_ideaunit_y_coordinate_dict = {None: 0}
    prev_road = x_world._idearoot.get_road()
    source_y = 0
    while ideas != []:
        x_idea = ideas.pop(-1)
        if is_sub_road(x_idea.get_road(), prev_road) is False:
            source_y -= 1
        _add_individual_trace(
            trace_list=trace_list,
            anno_list=anno_list,
            parent_y=_get_parent_y(x_idea, y_ideaunit_y_coordinate_dict),
            source_y=source_y,
            kid_idea=x_idea,
            mode=mode,
        )
        ideas.extend(iter(x_idea._kids.values()))
        y_ideaunit_y_coordinate_dict[x_idea.get_road()] = source_y
        prev_road = x_idea.get_road()


def _update_layout_fig(x_fig: plotly_Figure, mode: str, x_world: WorldUnit):
    x_title = "Tree with lines Layout"
    if mode == "Task":
        x_title = "Idea Tree with task ideas in Red."
    x_title += f" (Items: {len(x_world._idea_dict)})"
    x_title += f" (_sum_healerhold_importance: {x_world._sum_healerhold_importance})"
    x_title += f" (_econs_justified: {x_world._econs_justified})"
    x_fig.update_layout(
        title_text=x_title,
        font_size=12,
    )


def display_ideatree(x_world: WorldUnit, mode: str = None) -> plotly_Figure:
    """Mode can be None, Task, Econ"""

    x_fig = plotly_Figure()
    source_y = 0
    trace_list = []
    anno_list = []
    print(f"{x_world._owner_id=}")
    _add_ideaunit_traces(trace_list, anno_list, x_world, source_y, mode=mode)
    _update_layout_fig(x_fig, mode, x_world=x_world)
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

    return x_fig


def get_world_others_plotly_fig(x_world: WorldUnit) -> plotly_Figure:
    column_header_list = [
        "other_id",
        "_other_credor_pool",
        "credor_weight",
        "_other_debtor_pool",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_world_otherunits_dataframe(x_world)
    df.insert(1, "_other_credor_pool", x_world._other_credor_pool)
    df.insert(4, "_other_debtor_pool", x_world._other_debtor_pool)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.other_id,
                df._other_credor_pool,
                df.credor_weight,
                df._other_debtor_pool,
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
    fig_title = f"OwnerID '{x_world._owner_id}' world others metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_world_agenda_plotly_fig(x_world: WorldUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
    ]
    df = get_world_agenda_dataframe(x_world)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.world_importance,
                df._label,
                df._parent_road,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"OwnerID '{x_world._owner_id}' world agenda"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig