from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a04_reason_logic.reason_item import (
    PremiseStatusFinder,
    premisestatusfinder_shop,
)
from pytest import raises as pytest_raises
from plotly.graph_objects import Figure as plotly_figure, Scatter as plotly_Scatter


def test_PremiseStatusFinder_Exists():
    # ESTABLISH
    x_premise_open = 1
    x_premise_nigh = 1
    x_premise_divisor = 1
    x_fact_open_full = 1
    x_fact_nigh_full = 1

    # WHEN
    x_pbsd = PremiseStatusFinder(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_fact_open_full,
        x_fact_nigh_full,
    )

    # THEN
    assert x_pbsd.premise_open == x_premise_open
    assert x_pbsd.premise_nigh == x_premise_nigh
    assert x_pbsd.premise_divisor == x_premise_divisor
    assert x_pbsd.fact_open_full == x_fact_open_full
    assert x_pbsd.fact_nigh_full == x_fact_nigh_full


def test_premisestatusfinder_shop_ReturnsObj():
    # ESTABLISH
    x_premise_open = 1
    x_premise_nigh = 1
    x_premise_divisor = 1
    x_fact_open_full = 1
    x_fact_nigh_full = 1

    # WHEN
    x_pbsd = premisestatusfinder_shop(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_fact_open_full,
        x_fact_nigh_full,
    )

    # THEN
    assert x_pbsd.premise_open == x_premise_open
    assert x_pbsd.premise_nigh == x_premise_nigh
    assert x_pbsd.premise_divisor == x_premise_divisor
    assert x_pbsd.fact_open_full == x_fact_open_full
    assert x_pbsd.fact_nigh_full == x_fact_nigh_full


def test_PremiseStatusFinder_check_attr_CorrectlyRaisesError():
    with pytest_raises(Exception) as excinfo_1:
        premisestatusfinder_shop(
            premise_open=1,
            premise_nigh=None,
            premise_divisor=1,
            fact_open_full=1,
            fact_nigh_full=1,
        )
    assert str(excinfo_1.value) == "No parameter can be None"

    x_fact_open_full = 2
    x_fact_nigh_full = 1
    with pytest_raises(Exception) as excinfo_2:
        premisestatusfinder_shop(
            premise_open=1,
            premise_nigh=1,
            premise_divisor=1,
            fact_open_full=x_fact_open_full,
            fact_nigh_full=x_fact_nigh_full,
        )
    assert (
        str(excinfo_2.value)
        == f"self.fact_open_full={x_fact_open_full} cannot be greater that self.fact_nigh_full={x_fact_nigh_full}"
    )

    x_premise_divisor = -1
    with pytest_raises(Exception) as excinfo_3:
        premisestatusfinder_shop(
            premise_open=1,
            premise_nigh=1,
            premise_divisor=x_premise_divisor,
            fact_open_full=1,
            fact_nigh_full=1,
        )
    assert (
        str(excinfo_3.value)
        == f"self.premise_divisor={x_premise_divisor} cannot be less/equal to zero"
    )

    x_premise_divisor = 1
    x_premise_open = -1
    with pytest_raises(Exception) as excinfo_4:
        premisestatusfinder_shop(
            premise_open=x_premise_open,
            premise_nigh=1,
            premise_divisor=x_premise_divisor,
            fact_open_full=1,
            fact_nigh_full=1,
        )
    assert (
        str(excinfo_4.value)
        == f"self.premise_open={x_premise_open} cannot be less than zero or greater than self.premise_divisor={x_premise_divisor}"
    )

    x_premise_nigh = 2
    with pytest_raises(Exception) as excinfo_5:
        premisestatusfinder_shop(
            premise_open=1,
            premise_nigh=x_premise_nigh,
            premise_divisor=x_premise_divisor,
            fact_open_full=1,
            fact_nigh_full=1,
        )
    assert (
        str(excinfo_5.value)
        == f"self.premise_nigh={x_premise_nigh} cannot be less than zero or greater than self.premise_divisor={x_premise_divisor}"
    )


def test_PremiseStatusFinder_AbbrevationMethodsReturnsObjs():
    # ESTABLISH
    x_premise_open = 1
    x_premise_nigh = 2
    x_premise_divisor = 3
    x_fact_open_full = 4
    x_fact_nigh_full = 5

    # WHEN
    x_pbsd = premisestatusfinder_shop(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_fact_open_full,
        x_fact_nigh_full,
    )

    # THEN
    assert x_pbsd.bo() == x_fact_open_full % x_premise_divisor
    assert x_pbsd.bn() == x_fact_nigh_full % x_premise_divisor
    assert x_pbsd.po() == x_premise_open
    assert x_pbsd.pn() == x_premise_nigh
    assert x_pbsd.pd() == x_premise_divisor


# for PremiseStatusFinder tests
def add_trace(
    fig: plotly_figure,
    x_int: int,
    x_end: int,
    y_int: int,
    trace_name: str,
    x_color: str = None,
    showlegend: bool = False,
    case_str: str = "",
    sought_str: str = "",
    sought_status_str: str = "",
    premise_divisor: float = 0,
) -> plotly_figure:
    x_end = x_int if x_end is None else x_end
    x_color = "Black" if x_color is None else x_color
    x_marker_size = 12 if x_color == "Blue" else 10
    fig.add_trace(
        plotly_Scatter(
            x=[x_int, x_end],
            y=[y_int, y_int],
            marker_size=x_marker_size,
            name=trace_name,
            marker_color=x_color,
            showlegend=showlegend,
        )
    )
    fig.add_annotation(
        x=premise_divisor + 0.15, y=y_int, text=sought_str, showarrow=False
    )
    fig.add_annotation(
        x=premise_divisor + 0.4, y=y_int, text=sought_status_str, showarrow=False
    )
    fig.add_annotation(x=-0.1, y=y_int, text=case_str, showarrow=False)


# for PremiseStatusFinder tests
def add_traces(
    fig: plotly_figure,
    x_pbsd: PremiseStatusFinder,
    y_int: int,
    showlegend: bool = False,
    case_str: str = "",
    sought_str: str = "",
    sought_status_str: str = "",
    premise_divisor: float = 1,
) -> plotly_figure:
    fact_str = "FactUnit Remaiinder range"
    premise_str = "Premise Range"
    blue_str = "Blue"
    pink_str = "Pink"
    sl = showlegend
    if x_pbsd.po() <= x_pbsd.pn():
        add_trace(fig, x_pbsd.po(), x_pbsd.pn(), y_int, premise_str, blue_str, sl)
    else:
        add_trace(fig, 0, x_pbsd.pn(), y_int, premise_str, blue_str, sl)
        add_trace(fig, x_pbsd.po(), x_pbsd.pd(), y_int, premise_str, blue_str, sl)

    if x_pbsd.bo() <= x_pbsd.bn():
        add_trace(
            fig,
            x_pbsd.bo(),
            x_pbsd.bn(),
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            sought_str=sought_str,
            sought_status_str=sought_status_str,
            premise_divisor=premise_divisor,
        )
    else:
        add_trace(
            fig,
            0,
            x_pbsd.bn(),
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            sought_str=sought_str,
            sought_status_str=sought_status_str,
            premise_divisor=premise_divisor,
        )
        add_trace(fig, x_pbsd.bo(), x_pbsd.pd(), y_int, fact_str, pink_str, sl)


# for PremiseStatusFinder tests
def show_x(
    sought_active: bool,
    sought_task_status: bool,
    x_pbsd: PremiseStatusFinder,
    fig: plotly_figure,
    trace_y: float,
    case_str: str,
    showlegend: bool = False,
    graphics_bool: bool = False,
) -> float:
    if not graphics_bool:
        return
    sought_str = "TRUE" if sought_active else "FALSE"
    sought_status_str = "TRUE" if sought_task_status else "FALSE"
    add_traces(
        fig, x_pbsd, trace_y, showlegend, case_str, sought_str, sought_status_str, 1
    )
    if (
        x_pbsd.get_active() != sought_active
        or x_pbsd.get_task_status() != sought_task_status
    ):
        fig.show()
    return 0.1


# for PremiseStatusFinder tests
def get_fig(pd: float, graphics_bool: bool) -> plotly_figure:
    if not graphics_bool:
        return None
    fig = plotly_figure()
    add_trace(
        fig=fig,
        x_int=0.0,
        x_end=pd,
        y_int=0.0,
        trace_name="Divisor Range",
        x_color=None,
        showlegend=True,
        case_str="Case",
        sought_str="active",
        sought_status_str="Task Status",
        premise_divisor=pd,
    )
    fig_tag = "When Fact.range < Premise_divisor: Premise.active Checks."
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_tag, title_font_size=20)
    return fig


def test_PremiseStatusFinder_get_active_ReturnsObj(graphics_bool):
    """Check scenarios PremiseUnit._active. Plotly graph can be used to identify problems."""
    # # Case A
    assert premisestatusfinder_shop(0.3, 0.7, 1, 0.1, 1.2).get_active()

    # # Case B1
    graph_b = graphics_bool
    pd = 1  # premise_divisor
    fig = get_fig(pd, graphics_bool)
    caseb1_1 = premisestatusfinder_shop(0.3, 0.7, pd, 0.5, 0.8)
    caseb1_2 = premisestatusfinder_shop(0.3, 0.7, pd, 0.2, 0.5)
    caseb1_3 = premisestatusfinder_shop(0.3, 0.7, pd, 0.4, 0.6)
    caseb1_4 = premisestatusfinder_shop(0.3, 0.7, pd, 0.2, 0.8)
    caseb1_5 = premisestatusfinder_shop(0.3, 0.7, pd, 0.1, 0.3)
    caseb1_6 = premisestatusfinder_shop(0.3, 0.7, pd, 0.7, 0.8)
    caseb1_7 = premisestatusfinder_shop(0.3, 0.3, pd, 0.3, 0.5)
    caseb1_8 = premisestatusfinder_shop(0.3, 0.3, pd, 0.1, 0.3)
    caseb1_9 = premisestatusfinder_shop(0.3, 0.3, pd, 0.3, 0.3)
    caseb1_10 = premisestatusfinder_shop(0.0, 0.0, pd, 0.0, 0.0)

    sought_active = True
    sought_task = True
    linel = -0.1
    show_x(sought_active, sought_task, caseb1_1, fig, linel, "caseb1_1", True, graph_b)
    assert caseb1_1.get_active() == sought_active
    assert caseb1_1.get_task_status() == sought_task
    sought_active = True
    sought_task = False
    linel -= 0.1
    show_x(sought_active, sought_task, caseb1_2, fig, linel, "caseb1_2", False, graph_b)
    assert caseb1_2.get_active() == sought_active
    assert caseb1_2.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb1_3, fig, linel, "caseb1_3", False, graph_b)
    assert caseb1_3.get_active() == sought_active
    assert caseb1_3.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb1_4, fig, linel, "caseb1_4", False, graph_b)
    assert caseb1_4.get_active() == sought_active
    assert caseb1_4.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb1_5, fig, linel, "caseb1_5", False, graph_b)
    assert caseb1_5.get_active() == sought_active
    assert caseb1_5.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb1_6, fig, linel, "caseb1_6", False, graph_b)
    assert caseb1_6.get_active() == sought_active
    assert caseb1_6.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb1_7, fig, linel, "caseb1_7", False, graph_b)
    assert caseb1_7.get_active() == sought_active
    assert caseb1_7.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb1_8, fig, linel, "caseb1_8", False, graph_b)
    assert caseb1_8.get_active() == sought_active
    assert caseb1_8.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb1_9, fig, linel, "caseb1_9", False, graph_b)
    assert caseb1_9.get_active() == sought_active
    assert caseb1_9.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(
        sought_active, sought_task, caseb1_10, fig, linel, "caseb1_10", False, graph_b
    )
    assert caseb1_10.get_active() == sought_active
    assert caseb1_10.get_task_status() == sought_task

    # Case B2
    linel -= 0.1
    caseb2_1 = premisestatusfinder_shop(0.3, 0.7, pd, 0.8, 1.4)
    caseb2_2 = premisestatusfinder_shop(0.3, 0.7, pd, 0.6, 1.2)
    caseb2_3 = premisestatusfinder_shop(0.3, 0.7, pd, 0.6, 1.4)
    caseb2_4 = premisestatusfinder_shop(0.3, 0.7, pd, 0.9, 1.8)
    caseb2_5 = premisestatusfinder_shop(0.3, 0.7, pd, 0.2, 1.1)
    caseb2_6 = premisestatusfinder_shop(0.3, 0.7, pd, 0.9, 1.1)
    caseb2_7 = premisestatusfinder_shop(0.3, 0.7, pd, 0.7, 1.2)
    caseb2_8 = premisestatusfinder_shop(0.7, 0.7, pd, 0.7, 1.2)
    caseb2_9 = premisestatusfinder_shop(0.3, 0.7, pd, 0.9, 1.3)

    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb2_1, fig, linel, "caseb2_1", False, graph_b)
    assert caseb2_1.get_active() == sought_active
    assert caseb2_1.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb2_2, fig, linel, "caseb2_2", False, graph_b)
    assert caseb2_2.get_active() == sought_active
    assert caseb2_2.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb2_3, fig, linel, "caseb2_3", False, graph_b)
    assert caseb2_3.get_active() == sought_active
    assert caseb2_3.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb2_4, fig, linel, "caseb2_4", False, graph_b)
    assert caseb2_4.get_active() == sought_active
    assert caseb2_4.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb2_5, fig, linel, "caseb2_5", False, graph_b)
    assert caseb2_5.get_active() == sought_active
    assert caseb2_5.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb2_6, fig, linel, "caseb2_6", False, graph_b)
    assert caseb2_6.get_active() == sought_active
    assert caseb2_6.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb2_7, fig, linel, "caseb2_7", False, graph_b)
    assert caseb2_7.get_active() == sought_active
    assert caseb2_7.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb2_8, fig, linel, "caseb2_8", False, graph_b)
    assert caseb2_8.get_active() == sought_active
    assert caseb2_8.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb2_9, fig, linel, "caseb2_9", False, graph_b)
    assert caseb2_9.get_active() == sought_active
    assert caseb2_9.get_task_status() == sought_task

    # Case B3
    linel -= 0.1
    sought_active = True
    sought_task = True
    caseb3_1 = premisestatusfinder_shop(0.7, 0.3, pd, 0.2, 0.5)
    caseb3_2 = premisestatusfinder_shop(0.7, 0.3, pd, 0.5, 0.8)
    caseb3_3 = premisestatusfinder_shop(0.7, 0.3, pd, 0.2, 0.8)
    caseb3_4 = premisestatusfinder_shop(0.7, 0.3, pd, 0.1, 0.2)
    caseb3_5 = premisestatusfinder_shop(0.7, 0.3, pd, 0.8, 0.9)
    caseb3_6 = premisestatusfinder_shop(0.7, 0.3, pd, 0.4, 0.6)
    caseb3_7 = premisestatusfinder_shop(0.7, 0.3, pd, 0.3, 0.5)
    caseb3_8 = premisestatusfinder_shop(0.7, 0.3, pd, 0.7, 0.7)
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb3_1, fig, linel, "caseb3_1", False, graph_b)
    assert caseb3_1.get_active() == sought_active
    assert caseb3_1.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb3_2, fig, linel, "caseb3_2", False, graph_b)
    assert caseb3_2.get_active() == sought_active
    assert caseb3_2.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb3_3, fig, linel, "caseb3_3", False, graph_b)
    assert caseb3_3.get_active() == sought_active
    assert caseb3_3.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb3_4, fig, linel, "caseb3_4", False, graph_b)
    assert caseb3_4.get_active() == sought_active
    assert caseb3_4.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb3_5, fig, linel, "caseb3_5", False, graph_b)
    assert caseb3_5.get_active() == sought_active
    assert caseb3_5.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb3_6, fig, linel, "caseb3_6", False, graph_b)
    assert caseb3_6.get_active() == sought_active
    assert caseb3_6.get_task_status() == sought_task
    linel -= 0.1
    sought_active = False
    sought_task = False
    show_x(sought_active, sought_task, caseb3_7, fig, linel, "caseb3_7", False, graph_b)
    assert caseb3_7.get_active() == sought_active
    assert caseb3_7.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb3_8, fig, linel, "caseb3_8", False, graph_b)
    assert caseb3_8.get_active() == sought_active
    assert caseb3_8.get_task_status() == sought_task

    # Case B4
    linel -= 0.1
    sought_active = True
    sought_task = True
    caseb4_1 = premisestatusfinder_shop(0.7, 0.3, pd, 0.6, 1.2)
    caseb4_2 = premisestatusfinder_shop(0.7, 0.3, pd, 0.8, 1.4)
    caseb4_3 = premisestatusfinder_shop(0.7, 0.3, pd, 0.6, 1.4)
    caseb4_4 = premisestatusfinder_shop(0.7, 0.3, pd, 0.8, 1.2)
    caseb4_5 = premisestatusfinder_shop(0.7, 0.3, pd, 0.2, 1.1)
    caseb4_6 = premisestatusfinder_shop(0.7, 0.3, pd, 0.9, 1.8)
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb4_1, fig, linel, "caseb4_1", False, graph_b)
    assert caseb4_1.get_active() == sought_active
    assert caseb4_1.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb4_2, fig, linel, "caseb4_2", False, graph_b)
    assert caseb4_2.get_active() == sought_active
    assert caseb4_2.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = True
    show_x(sought_active, sought_task, caseb4_3, fig, linel, "caseb4_3", False, graph_b)
    assert caseb4_3.get_active() == sought_active
    assert caseb4_3.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb4_4, fig, linel, "caseb4_4", False, graph_b)
    assert caseb4_4.get_active() == sought_active
    assert caseb4_4.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb4_5, fig, linel, "caseb4_5", False, graph_b)
    assert caseb4_5.get_active() == sought_active
    assert caseb4_5.get_task_status() == sought_task
    linel -= 0.1
    sought_active = True
    sought_task = False
    show_x(sought_active, sought_task, caseb4_6, fig, linel, "caseb4_6", False, graph_b)
    assert caseb4_6.get_active() == sought_active
    assert caseb4_6.get_task_status() == sought_task

    # Bottom divisor line
    _add_last_trace_and_show(fig, pd, linel, graph_b)


def _add_last_trace_and_show(fig: plotly_figure, pd, linel, graphics_bool: bool):
    if graphics_bool:
        add_trace(fig, 0.0, pd, linel - 0.2, "Divisor Range", None)
        conditional_fig_show(fig, graphics_bool)


def test_premisefactstatusdata_CorrectlyCalculates_active_AndTaskStatusExample_01():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
        fact_open_full=20000,
        fact_nigh_full=29000,
    )
    print(f"----\n  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=} \tdifference:{segr_obj.fact_nigh_full-segr_obj.fact_open_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")

    # THEN
    # assert segr_obj._fact_range_len == 9000
    # assert segr_obj.get_fact_nigh_mod_div() == 200
    assert segr_obj.get_active()
    assert segr_obj.get_task_status()


def test_premisefactstatusdata_CorrectlyCalculates_active_AndTaskStatusExample_02():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
        fact_open_full=1300,
        fact_nigh_full=1400,
    )
    print(f"----\n  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=} \tdifference:{segr_obj.fact_nigh_full-segr_obj.fact_open_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")

    # THEN
    assert segr_obj.get_active()
    assert segr_obj.get_task_status()


def test_premisefactstatusdata_CorrectlyCalculates_active_AndTaskStatusExample_03():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
        fact_open_full=1300,
        fact_nigh_full=1300,
    )
    print(f"----\n  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.fact_open_full=}  {segr_obj.fact_nigh_full=} \tdifference:{segr_obj.fact_nigh_full-segr_obj.fact_open_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")

    # THEN
    assert segr_obj.get_active() is False
    assert segr_obj.get_task_status() is False
