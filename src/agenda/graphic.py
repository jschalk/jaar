from src._road.road import get_parent_road, RoadUnit, is_sub_road
from src.agenda.oath import OathUnit
from src.agenda.agenda import AgendaUnit
from src.agenda.report import (
    get_agenda_partyunits_dataframe,
    get_agenda_intent_dataframe,
)
from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)


def _get_dot_diameter(x_ratio: float):
    return ((x_ratio**0.4)) * 100


def _get_parent_y(x_oath: OathUnit, oathunit_y_coordinate_dict: dict) -> RoadUnit:
    parent_road = get_parent_road(x_oath.get_road())
    return oathunit_y_coordinate_dict.get(parent_road)


def _get_color_for_oathunit_trace(x_oathunit: OathUnit, mode: str) -> str:
    if mode is None:
        if x_oathunit._level == 0:
            return "Red"
        elif x_oathunit._level == 1:
            return "Pink"
        elif x_oathunit._level == 2:
            return "Green"
        elif x_oathunit._level == 3:
            return "Blue"
        elif x_oathunit._level == 4:
            return "Purple"
        elif x_oathunit._level == 5:
            return "Gold"
        else:
            return "Black"
    elif mode == "Task":
        return "Red" if x_oathunit.pledge else "Pink"
    elif mode == "Econ":
        if x_oathunit._problem_bool and x_oathunit._healerhold.any_idea_id_exists():
            return "Purple"
        elif x_oathunit._healerhold.any_idea_id_exists():
            return "Blue"
        elif x_oathunit._problem_bool:
            return "Red"
        else:
            return "Pink"


def _add_individual_trace(
    trace_list: list,
    anno_list: list,
    parent_y,
    source_y,
    kid_oath: OathUnit,
    mode: str,
):
    trace_list.append(
        plotly_Scatter(
            x=[kid_oath._level - 1, kid_oath._level],
            y=[parent_y, source_y],
            marker_size=_get_dot_diameter(kid_oath._agenda_importance),
            name=kid_oath._label,
            marker_color=_get_color_for_oathunit_trace(kid_oath, mode=mode),
        )
    )
    anno_list.append(
        dict(
            x=kid_oath._level,
            y=source_y + (_get_dot_diameter(kid_oath._agenda_importance) / 150) + 0.002,
            text=kid_oath._label,
            showarrow=False,
        )
    )


def _add_oathunit_traces(
    trace_list, anno_list, x_agenda: AgendaUnit, source_y: float, mode: str
):
    oaths = [x_agenda._oathroot]
    y_oathunit_y_coordinate_dict = {None: 0}
    prev_road = x_agenda._oathroot.get_road()
    source_y = 0
    while oaths != []:
        x_oath = oaths.pop(-1)
        if is_sub_road(x_oath.get_road(), prev_road) is False:
            source_y -= 1
        _add_individual_trace(
            trace_list=trace_list,
            anno_list=anno_list,
            parent_y=_get_parent_y(x_oath, y_oathunit_y_coordinate_dict),
            source_y=source_y,
            kid_oath=x_oath,
            mode=mode,
        )
        oaths.extend(iter(x_oath._kids.values()))
        y_oathunit_y_coordinate_dict[x_oath.get_road()] = source_y
        prev_road = x_oath.get_road()


def _update_layout_fig(x_fig: plotly_Figure, mode: str, x_agenda: AgendaUnit):
    x_title = "Tree with lines Layout"
    if mode == "Task":
        x_title = "Oath Tree with task oaths in Red."
    x_title += f" (Items: {len(x_agenda._oath_dict)})"
    x_title += f" (_sum_healerhold_importance: {x_agenda._sum_healerhold_importance})"
    x_title += f" (_econs_justified: {x_agenda._econs_justified})"
    x_fig.update_layout(
        title_text=x_title,
        font_size=12,
    )


def display_oathtree(x_agenda: AgendaUnit, mode: str = None) -> plotly_Figure:
    """Mode can be None, Task, Econ"""

    x_fig = plotly_Figure()
    source_y = 0
    trace_list = []
    anno_list = []
    print(f"{x_agenda._owner_id=}")
    _add_oathunit_traces(trace_list, anno_list, x_agenda, source_y, mode=mode)
    _update_layout_fig(x_fig, mode, x_agenda=x_agenda)
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


def get_agenda_partys_plotly_fig(x_agenda: AgendaUnit) -> plotly_Figure:
    column_header_list = [
        "party_id",
        "_party_credor_pool",
        "credor_weight",
        "_party_debtor_pool",
        "debtor_weight",
        "_agenda_cred",
        "_agenda_debt",
        "_agenda_intent_cred",
        "_agenda_intent_debt",
    ]
    df = get_agenda_partyunits_dataframe(x_agenda)
    df.insert(1, "_party_credor_pool", x_agenda._party_credor_pool)
    df.insert(4, "_party_debtor_pool", x_agenda._party_debtor_pool)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.party_id,
                df._party_credor_pool,
                df.credor_weight,
                df._party_debtor_pool,
                df.debtor_weight,
                df._agenda_cred,
                df._agenda_debt,
                df._agenda_intent_cred,
                df._agenda_intent_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"OwnerID '{x_agenda._owner_id}' agenda partys metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_agenda_intent_plotly_fig(x_agenda: AgendaUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "agenda_importance",
        "_label",
        "_parent_road",
    ]
    df = get_agenda_intent_dataframe(x_agenda)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.agenda_importance,
                df._label,
                df._parent_road,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"OwnerID '{x_agenda._owner_id}' agenda intent"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
