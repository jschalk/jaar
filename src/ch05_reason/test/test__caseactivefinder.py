from plotly.graph_objects import Figure as plotly_figure, Scatter as plotly_Scatter
from pytest import raises as pytest_raises
from src.ch01_py.plotly_toolbox import conditional_fig_show
from src.ch05_reason.reason import CaseActiveFinder, caseactivefinder_shop


def test_CaseActiveFinder_Exists():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 1
    x_reason_divisor = 1
    x_fact_lower_full = 1
    x_fact_upper_full = 1

    # WHEN
    x_csf = CaseActiveFinder(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.reason_lower == x_reason_lower
    assert x_csf.reason_upper == x_reason_upper
    assert x_csf.reason_divisor == x_reason_divisor
    assert x_csf.fact_lower_full == x_fact_lower_full
    assert x_csf.fact_upper_full == x_fact_upper_full


def test_caseactivefinder_shop_ReturnsObj():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 1
    x_reason_divisor = 1
    x_fact_lower_full = 1
    x_fact_upper_full = 1

    # WHEN
    x_csf = caseactivefinder_shop(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.reason_lower == x_reason_lower
    assert x_csf.reason_upper == x_reason_upper
    assert x_csf.reason_divisor == x_reason_divisor
    assert x_csf.fact_lower_full == x_fact_lower_full
    assert x_csf.fact_upper_full == x_fact_upper_full


def test_CaseActiveFinder_check_attr_RaisesError_Scenario0():
    # ESTABLISH / WHEN
    with pytest_raises(Exception) as excinfo_1:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=None,
            reason_divisor=1,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assert str(excinfo_1.value) == "No parameter can be None"


def test_CaseActiveFinder_check_attr_RaisesError_Scenario1():
    # ESTABLISH
    x_fact_lower_full = 2
    x_fact_upper_full = 1

    # WHEN
    with pytest_raises(Exception) as excinfo_2:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=1,
            reason_divisor=1,
            fact_lower_full=x_fact_lower_full,
            fact_upper_full=x_fact_upper_full,
        )

    # THEN
    assertion_fail_str = f"self.fact_lower_full={x_fact_lower_full} cannot be greater than self.fact_upper_full={x_fact_upper_full}"
    assert str(excinfo_2.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario2():
    # ESTABLISH
    x_reason_divisor = -1

    # WHEN
    with pytest_raises(Exception) as excinfo_3:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=1,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = (
        f"self.reason_divisor={x_reason_divisor} cannot be less/equal to zero"
    )
    assert str(excinfo_3.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario3():
    # ESTABLISH
    x_reason_divisor = 1
    x_reason_lower = -1

    # WHEN
    with pytest_raises(Exception) as excinfo_4:
        caseactivefinder_shop(
            reason_lower=x_reason_lower,
            reason_upper=1,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = f"self.reason_lower={x_reason_lower} cannot be less than zero or greater than self.reason_divisor={x_reason_divisor}"
    assert str(excinfo_4.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario4():
    # ESTABLISH
    x_reason_divisor = 1
    x_reason_upper = 2

    # WHEN
    with pytest_raises(Exception) as excinfo_5:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=x_reason_upper,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = f"self.reason_upper={x_reason_upper} cannot be less than zero or greater than self.reason_divisor={x_reason_divisor}"
    assert str(excinfo_5.value) == assertion_fail_str


def test_CaseActiveFinder_get_fact_lower_remainder_ReturnsObj():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 2
    x_reason_divisor = 3
    x_fact_lower_full = 4
    x_fact_upper_full = 5

    # WHEN
    x_csf = caseactivefinder_shop(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.get_fact_lower_remainder() == x_fact_lower_full % x_reason_divisor
    assert x_csf.get_fact_upper_remainder() == x_fact_upper_full % x_reason_divisor


# for CaseActiveFinder tests
def add_trace(
    fig: plotly_figure,
    x_int: int,
    x_end: int,
    y_int: int,
    trace_name: str,
    x_color: str = None,
    showlegend: bool = False,
    case_str: str = "",
    expect_str: str = "",
    expect_task_str: str = "",
    reason_divisor: float = 0,
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
        x=reason_divisor + 0.15, y=y_int, text=expect_str, showarrow=False
    )
    fig.add_annotation(
        x=reason_divisor + 0.4, y=y_int, text=expect_task_str, showarrow=False
    )
    fig.add_annotation(x=-0.1, y=y_int, text=case_str, showarrow=False)


# for CaseActiveFinder tests
def add_traces(
    fig: plotly_figure,
    x_csf: CaseActiveFinder,
    y_int: int,
    showlegend: bool = False,
    case_str: str = "",
    expect_str: str = "",
    expect_task_str: str = "",
    reason_divisor: float = 1,
) -> plotly_figure:
    fact_str = "FactUnit range"
    case_str = "Case Range"
    blue_str = "Blue"
    pink_str = "Pink"
    sl = showlegend

    if x_csf.reason_lower <= x_csf.reason_upper:
        add_trace(
            fig, x_csf.reason_lower, x_csf.reason_upper, y_int, case_str, blue_str, sl
        )
    else:
        add_trace(fig, 0, x_csf.reason_upper, y_int, case_str, blue_str, sl)
        add_trace(
            fig,
            x_csf.reason_lower,
            x_csf.reason_divisor,
            y_int,
            case_str,
            blue_str,
            sl,
        )

    if x_csf.get_fact_lower_remainder() <= x_csf.get_fact_upper_remainder():
        x_int = x_csf.get_fact_lower_remainder()
        x_end = x_csf.get_fact_upper_remainder()
        if x_csf.fact_upper_full == x_csf.reason_divisor:
            x_end = x_csf.reason_divisor
        add_trace(
            fig,
            x_int,
            x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            expect_str=expect_str,
            expect_task_str=expect_task_str,
            reason_divisor=reason_divisor,
        )
    else:
        trace1_x_int = 0
        trace1_x_end = x_csf.get_fact_upper_remainder()
        trace2_x_int = x_csf.get_fact_lower_remainder()
        trace2_x_end = x_csf.reason_divisor

        add_trace(
            fig,
            trace1_x_int,
            trace1_x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            expect_str=expect_str,
            expect_task_str=expect_task_str,
            reason_divisor=reason_divisor,
        )
        add_trace(
            fig,
            trace2_x_int,
            trace2_x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
        )


# for CaseActiveFinder tests
def show_x(
    expect_active: bool,
    expect_task_bool: bool,
    x_csf: CaseActiveFinder,
    fig: plotly_figure,
    trace_y: float,
    case_str: str,
    showlegend: bool = False,
    graphics_bool: bool = False,
) -> float:
    if not graphics_bool:
        return
    expect_str = "TRUE" if expect_active else "FALSE"
    expect_task_str = "TRUE" if expect_task_bool else "FALSE"
    add_traces(
        fig, x_csf, trace_y, showlegend, case_str, expect_str, expect_task_str, 1
    )
    if (
        x_csf.get_active_bool() != expect_active
        or x_csf.get_task_bool() != expect_task_bool
    ):
        fig.show()
    return 0.1


# for CaseActiveFinder tests
def get_fig(pd: float, graphics_bool: bool) -> plotly_figure:
    if not graphics_bool:
        return None
    fig = plotly_figure()
    add_trace(
        fig=fig,
        x_int=0.0,
        x_end=pd,
        y_int=0.0,
        trace_name="reason_divisor Range",
        x_color=None,
        showlegend=True,
        case_str="Scenario",
        expect_str="case_active",
        expect_task_str="task Bool",
        reason_divisor=pd,
    )
    fig_label = "Given Fact Range and Case Range assert expected Case.case_active, Case.Task Bools."
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def test_CaseActiveFinder_get_active_get_task_bool_ReturnsObj_Scenari0_fact_range_LessThan_Divisor(
    graphics_bool,
):
    # ESTABLISH / WHEN / THEN
    """Check scenarios CaseUnit.active. Plotly graph can be used to identify problems."""
    # # Scenario A
    assert caseactivefinder_shop(0.3, 0.7, 1, 0.1, 1.2).get_active_bool()

    # # Scenario B1
    graph_b = graphics_bool
    pd = 1  # reason_divisor
    fig = get_fig(pd, graphics_bool)
    caseb1_1 = caseactivefinder_shop(0.3, 0.7, pd, 0.5, 0.8)
    caseb1_2 = caseactivefinder_shop(0.3, 0.7, pd, 0.2, 0.5)
    caseb1_3 = caseactivefinder_shop(0.3, 0.7, pd, 0.4, 0.6)
    caseb1_4 = caseactivefinder_shop(0.3, 0.7, pd, 0.2, 0.8)
    caseb1_5 = caseactivefinder_shop(0.3, 0.7, pd, 0.1, 0.3)
    caseb1_6 = caseactivefinder_shop(0.3, 0.7, pd, 0.7, 0.8)
    caseb1_7 = caseactivefinder_shop(0.3, 0.3, pd, 0.3, 0.5)
    caseb1_8 = caseactivefinder_shop(0.3, 0.3, pd, 0.1, 0.3)
    caseb1_9 = caseactivefinder_shop(0.3, 0.3, pd, 0.3, 0.3)
    caseb1_10 = caseactivefinder_shop(0.0, 0.0, pd, 0.0, 0.0)

    expect_active = True
    expect_task = True
    linel = -0.1
    show_x(expect_active, expect_task, caseb1_1, fig, linel, "caseb1_1", True, graph_b)
    assert caseb1_1.get_active_bool() == expect_active
    assert caseb1_1.get_task_bool() == expect_task
    expect_active = True
    expect_task = False
    linel -= 0.1
    show_x(expect_active, expect_task, caseb1_2, fig, linel, "caseb1_2", False, graph_b)
    assert caseb1_2.get_active_bool() == expect_active
    assert caseb1_2.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb1_3, fig, linel, "caseb1_3", False, graph_b)
    assert caseb1_3.get_active_bool() == expect_active
    assert caseb1_3.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb1_4, fig, linel, "caseb1_4", False, graph_b)
    assert caseb1_4.get_active_bool() == expect_active
    assert caseb1_4.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb1_5, fig, linel, "caseb1_5", False, graph_b)
    assert caseb1_5.get_active_bool() == expect_active
    assert caseb1_5.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb1_6, fig, linel, "caseb1_6", False, graph_b)
    assert caseb1_6.get_active_bool() == expect_active
    assert caseb1_6.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb1_7, fig, linel, "caseb1_7", False, graph_b)
    assert caseb1_7.get_active_bool() == expect_active
    assert caseb1_7.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb1_8, fig, linel, "caseb1_8", False, graph_b)
    assert caseb1_8.get_active_bool() == expect_active
    assert caseb1_8.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb1_9, fig, linel, "caseb1_9", False, graph_b)
    assert caseb1_9.get_active_bool() == expect_active
    assert caseb1_9.get_task_bool() == expect_task
    linel -= 0.1
    exp_active = True
    exp_task = False
    show_x(exp_active, exp_task, caseb1_10, fig, linel, "caseb1_10", False, graph_b)
    assert caseb1_10.get_active_bool() == expect_active
    assert caseb1_10.get_task_bool() == expect_task

    # Scenario B2
    linel -= 0.1
    caseb2_1 = caseactivefinder_shop(0.3, 0.7, pd, 0.8, 1.4)
    caseb2_2 = caseactivefinder_shop(0.3, 0.7, pd, 0.6, 1.2)
    caseb2_3 = caseactivefinder_shop(0.3, 0.7, pd, 0.6, 1.4)
    caseb2_4 = caseactivefinder_shop(0.3, 0.7, pd, 0.9, 1.8)
    caseb2_5 = caseactivefinder_shop(0.3, 0.7, pd, 0.2, 1.1)
    caseb2_6 = caseactivefinder_shop(0.3, 0.7, pd, 0.9, 1.1)
    caseb2_7 = caseactivefinder_shop(0.3, 0.7, pd, 0.7, 1.2)
    caseb2_8 = caseactivefinder_shop(0.7, 0.7, pd, 0.7, 1.2)
    caseb2_9 = caseactivefinder_shop(0.3, 0.7, pd, 0.9, 1.3)

    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb2_1, fig, linel, "caseb2_1", False, graph_b)
    assert caseb2_1.get_active_bool() == expect_active
    assert caseb2_1.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb2_2, fig, linel, "caseb2_2", False, graph_b)
    assert caseb2_2.get_active_bool() == expect_active
    assert caseb2_2.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb2_3, fig, linel, "caseb2_3", False, graph_b)
    assert caseb2_3.get_active_bool() == expect_active
    assert caseb2_3.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb2_4, fig, linel, "caseb2_4", False, graph_b)
    assert caseb2_4.get_active_bool() == expect_active
    assert caseb2_4.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb2_5, fig, linel, "caseb2_5", False, graph_b)
    assert caseb2_5.get_active_bool() == expect_active
    assert caseb2_5.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb2_6, fig, linel, "caseb2_6", False, graph_b)
    assert caseb2_6.get_active_bool() == expect_active
    assert caseb2_6.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb2_7, fig, linel, "caseb2_7", False, graph_b)
    assert caseb2_7.get_active_bool() == expect_active
    assert caseb2_7.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb2_8, fig, linel, "caseb2_8", False, graph_b)
    assert caseb2_8.get_active_bool() == expect_active
    assert caseb2_8.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb2_9, fig, linel, "caseb2_9", False, graph_b)
    assert caseb2_9.get_active_bool() == expect_active
    assert caseb2_9.get_task_bool() == expect_task

    # Scenario B3
    linel -= 0.1
    expect_active = True
    expect_task = True
    caseb3_1 = caseactivefinder_shop(0.7, 0.3, pd, 0.2, 0.5)
    caseb3_2 = caseactivefinder_shop(0.7, 0.3, pd, 0.5, 0.8)
    caseb3_3 = caseactivefinder_shop(0.7, 0.3, pd, 0.2, 0.8)
    caseb3_4 = caseactivefinder_shop(0.7, 0.3, pd, 0.1, 0.2)
    caseb3_5 = caseactivefinder_shop(0.7, 0.3, pd, 0.8, 0.9)
    caseb3_6 = caseactivefinder_shop(0.7, 0.3, pd, 0.4, 0.6)
    caseb3_7 = caseactivefinder_shop(0.7, 0.3, pd, 0.3, 0.5)
    caseb3_8 = caseactivefinder_shop(0.7, 0.3, pd, 0.7, 0.7)
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb3_1, fig, linel, "caseb3_1", False, graph_b)
    assert caseb3_1.get_active_bool() == expect_active
    assert caseb3_1.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb3_2, fig, linel, "caseb3_2", False, graph_b)
    assert caseb3_2.get_active_bool() == expect_active
    assert caseb3_2.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb3_3, fig, linel, "caseb3_3", False, graph_b)
    assert caseb3_3.get_active_bool() == expect_active
    assert caseb3_3.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb3_4, fig, linel, "caseb3_4", False, graph_b)
    assert caseb3_4.get_active_bool() == expect_active
    assert caseb3_4.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb3_5, fig, linel, "caseb3_5", False, graph_b)
    assert caseb3_5.get_active_bool() == expect_active
    assert caseb3_5.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb3_6, fig, linel, "caseb3_6", False, graph_b)
    assert caseb3_6.get_active_bool() == expect_active
    assert caseb3_6.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = False
    expect_task = False
    show_x(expect_active, expect_task, caseb3_7, fig, linel, "caseb3_7", False, graph_b)
    assert caseb3_7.get_active_bool() == expect_active
    assert caseb3_7.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb3_8, fig, linel, "caseb3_8", False, graph_b)
    assert caseb3_8.get_active_bool() == expect_active
    assert caseb3_8.get_task_bool() == expect_task

    # Scenario B4
    linel -= 0.1
    caseb4_1 = caseactivefinder_shop(0.7, 0.3, pd, 0.6, 1.2)
    caseb4_2 = caseactivefinder_shop(0.7, 0.3, pd, 0.8, 1.4)
    caseb4_3 = caseactivefinder_shop(0.7, 0.3, pd, 0.6, 1.4)
    caseb4_4 = caseactivefinder_shop(0.7, 0.3, pd, 0.8, 1.2)
    caseb4_5 = caseactivefinder_shop(0.7, 0.3, pd, 0.2, 1.1)
    caseb4_6 = caseactivefinder_shop(0.7, 0.3, pd, 0.9, 1.8)
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb4_1, fig, linel, "caseb4_1", False, graph_b)
    assert caseb4_1.get_active_bool() == expect_active
    assert caseb4_1.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb4_2, fig, linel, "caseb4_2", False, graph_b)
    assert caseb4_2.get_active_bool() == expect_active
    assert caseb4_2.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = True
    show_x(expect_active, expect_task, caseb4_3, fig, linel, "caseb4_3", False, graph_b)
    assert caseb4_3.get_active_bool() == expect_active
    assert caseb4_3.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb4_4, fig, linel, "caseb4_4", False, graph_b)
    assert caseb4_4.get_active_bool() == expect_active
    assert caseb4_4.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb4_5, fig, linel, "caseb4_5", False, graph_b)
    assert caseb4_5.get_active_bool() == expect_active
    assert caseb4_5.get_task_bool() == expect_task
    linel -= 0.1
    expect_active = True
    expect_task = False
    show_x(expect_active, expect_task, caseb4_6, fig, linel, "caseb4_6", False, graph_b)
    assert caseb4_6.get_active_bool() == expect_active
    assert caseb4_6.get_task_bool() == expect_task

    # Scenario B5
    linel -= 0.1
    caseb5_0 = caseactivefinder_shop(0.3, 0.7, pd, 0.0, 1.0)
    caseb5_1 = caseactivefinder_shop(0.0, 1.0, pd, 0.0, 1.0)
    linel -= 0.1
    exp_active = True
    exp_task = True
    show_x(exp_active, exp_task, caseb5_0, fig, linel, "caseb1_11", False, graph_b)
    assert caseb5_0.get_active_bool() == exp_active
    assert caseb5_0.get_task_bool() == exp_task
    linel -= 0.1
    exp_active = True
    exp_task = False
    show_x(exp_active, exp_task, caseb5_1, fig, linel, "caseb1_12", False, graph_b)
    assert caseb5_1.get_active_bool() == exp_active
    assert caseb5_1.get_task_bool() == exp_task

    # Bottom reason_divisor line
    _add_last_trace_and_show(fig, pd, linel, graph_b)


def _add_last_trace_and_show(fig: plotly_figure, pd, linel, graphics_bool: bool):
    if graphics_bool:
        add_trace(fig, 0.0, pd, linel - 0.2, "reason_divisor Range", None)
        conditional_fig_show(fig, graphics_bool)


def test_CaseActiveFinder_get_active_get_task_bool_ReturnsObj_Scenario1_Seperated_reason_range_Inside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=20000,
        fact_upper_full=29000,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    x_str2 = f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    x_str3 = f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    print(x_str2)
    print(x_str3)
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_task_bool()=}")
    # assert segr_obj.fact_range_len == 9000
    # assert segr_obj.get_fact_upper_mod_div() == 200

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_task_bool()


def test_CaseActiveFinder_get_active_get_task_bool_ReturnsObj_Scenario2_reason_range_Inside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=1300,
        fact_upper_full=1400,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_task_bool()


def test_CaseActiveFinder_get_active_get_task_bool_ReturnsObj_Scenario3_reason_range_Outside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=1300,
        fact_upper_full=1300,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool() is False
    assert segr_obj.get_task_bool() is False


def test_CaseActiveFinder_get_active_get_task_bool_ReturnsObj_Scenario4_fact_range_Equals_divisor():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=600.0,
        reason_upper=690.0,
        reason_divisor=1440,
        fact_lower_full=0,
        fact_upper_full=1440,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_task_bool()
