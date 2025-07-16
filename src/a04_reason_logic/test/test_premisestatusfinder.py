from plotly.graph_objects import Figure as plotly_figure, Scatter as plotly_Scatter
from pytest import raises as pytest_raises
from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a04_reason_logic.reason_plan import (
    PremiseStatusFinder,
    premisestatusfinder_shop,
)


def test_PremiseStatusFinder_Exists():
    # ESTABLISH
    x_p_lower = 1
    x_p_upper = 1
    x_p_divisor = 1
    x_f_lower_full = 1
    x_f_upper_full = 1

    # WHEN
    x_pbsd = PremiseStatusFinder(
        x_p_lower,
        x_p_upper,
        x_p_divisor,
        x_f_lower_full,
        x_f_upper_full,
    )

    # THEN
    assert x_pbsd.p_lower == x_p_lower
    assert x_pbsd.p_upper == x_p_upper
    assert x_pbsd.p_divisor == x_p_divisor
    assert x_pbsd.f_lower_full == x_f_lower_full
    assert x_pbsd.f_upper_full == x_f_upper_full


def test_premisestatusfinder_shop_ReturnsObj():
    # ESTABLISH
    x_p_lower = 1
    x_p_upper = 1
    x_p_divisor = 1
    x_f_lower_full = 1
    x_f_upper_full = 1

    # WHEN
    x_pbsd = premisestatusfinder_shop(
        x_p_lower,
        x_p_upper,
        x_p_divisor,
        x_f_lower_full,
        x_f_upper_full,
    )

    # THEN
    assert x_pbsd.p_lower == x_p_lower
    assert x_pbsd.p_upper == x_p_upper
    assert x_pbsd.p_divisor == x_p_divisor
    assert x_pbsd.f_lower_full == x_f_lower_full
    assert x_pbsd.f_upper_full == x_f_upper_full


def test_PremiseStatusFinder_check_attr_CorrectlyRaisesError():
    with pytest_raises(Exception) as excinfo_1:
        premisestatusfinder_shop(
            p_lower=1,
            p_upper=None,
            p_divisor=1,
            f_lower_full=1,
            f_upper_full=1,
        )
    assert str(excinfo_1.value) == "No parameter can be None"

    x_f_lower_full = 2
    x_f_upper_full = 1
    with pytest_raises(Exception) as excinfo_2:
        premisestatusfinder_shop(
            p_lower=1,
            p_upper=1,
            p_divisor=1,
            f_lower_full=x_f_lower_full,
            f_upper_full=x_f_upper_full,
        )
    assert (
        str(excinfo_2.value)
        == f"self.f_lower_full={x_f_lower_full} cannot be greater than self.f_upper_full={x_f_upper_full}"
    )

    x_p_divisor = -1
    with pytest_raises(Exception) as excinfo_3:
        premisestatusfinder_shop(
            p_lower=1,
            p_upper=1,
            p_divisor=x_p_divisor,
            f_lower_full=1,
            f_upper_full=1,
        )
    assert (
        str(excinfo_3.value)
        == f"self.p_divisor={x_p_divisor} cannot be less/equal to zero"
    )

    x_p_divisor = 1
    x_p_lower = -1
    with pytest_raises(Exception) as excinfo_4:
        premisestatusfinder_shop(
            p_lower=x_p_lower,
            p_upper=1,
            p_divisor=x_p_divisor,
            f_lower_full=1,
            f_upper_full=1,
        )
    assert (
        str(excinfo_4.value)
        == f"self.p_lower={x_p_lower} cannot be less than zero or greater than self.p_divisor={x_p_divisor}"
    )

    x_p_upper = 2
    with pytest_raises(Exception) as excinfo_5:
        premisestatusfinder_shop(
            p_lower=1,
            p_upper=x_p_upper,
            p_divisor=x_p_divisor,
            f_lower_full=1,
            f_upper_full=1,
        )
    assert (
        str(excinfo_5.value)
        == f"self.p_upper={x_p_upper} cannot be less than zero or greater than self.p_divisor={x_p_divisor}"
    )


def test_PremiseStatusFinder_AbbrevationMethodsReturnsObjs():
    # ESTABLISH
    x_p_lower = 1
    x_p_upper = 2
    x_p_divisor = 3
    x_f_lower_full = 4
    x_f_upper_full = 5

    # WHEN
    x_pbsd = premisestatusfinder_shop(
        x_p_lower,
        x_p_upper,
        x_p_divisor,
        x_f_lower_full,
        x_f_upper_full,
    )

    # THEN
    assert x_pbsd.bo() == x_f_lower_full % x_p_divisor
    assert x_pbsd.bn() == x_f_upper_full % x_p_divisor
    assert x_pbsd.po() == x_p_lower
    assert x_pbsd.pn() == x_p_upper
    assert x_pbsd.pd() == x_p_divisor


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
    p_divisor: float = 0,
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
    fig.add_annotation(x=p_divisor + 0.15, y=y_int, text=sought_str, showarrow=False)
    fig.add_annotation(
        x=p_divisor + 0.4, y=y_int, text=sought_status_str, showarrow=False
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
    p_divisor: float = 1,
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
            p_divisor=p_divisor,
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
            p_divisor=p_divisor,
        )
        add_trace(fig, x_pbsd.bo(), x_pbsd.pd(), y_int, fact_str, pink_str, sl)


# for PremiseStatusFinder tests
def show_x(
    sought_active: bool,
    sought_chore_status: bool,
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
    sought_status_str = "TRUE" if sought_chore_status else "FALSE"
    add_traces(
        fig, x_pbsd, trace_y, showlegend, case_str, sought_str, sought_status_str, 1
    )
    if (
        x_pbsd.get_active() != sought_active
        or x_pbsd.get_chore_status() != sought_chore_status
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
        trace_name="p_divisor Range",
        x_color=None,
        showlegend=True,
        case_str="Case",
        sought_str="active",
        sought_status_str="Chore Status",
        p_divisor=pd,
    )
    fig_label = "When Fact.range < p_divisor: Premise.active Checks."
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def test_PremiseStatusFinder_get_active_ReturnsObj(graphics_bool):
    """Check scenarios PremiseUnit._active. Plotly graph can be used to identify problems."""
    # # Case A
    assert premisestatusfinder_shop(0.3, 0.7, 1, 0.1, 1.2).get_active()

    # # Case B1
    graph_b = graphics_bool
    pd = 1  # p_divisor
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
    sought_chore = True
    linel = -0.1
    show_x(sought_active, sought_chore, caseb1_1, fig, linel, "caseb1_1", True, graph_b)
    assert caseb1_1.get_active() == sought_active
    assert caseb1_1.get_chore_status() == sought_chore
    sought_active = True
    sought_chore = False
    linel -= 0.1
    show_x(
        sought_active, sought_chore, caseb1_2, fig, linel, "caseb1_2", False, graph_b
    )
    assert caseb1_2.get_active() == sought_active
    assert caseb1_2.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_3, fig, linel, "caseb1_3", False, graph_b
    )
    assert caseb1_3.get_active() == sought_active
    assert caseb1_3.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb1_4, fig, linel, "caseb1_4", False, graph_b
    )
    assert caseb1_4.get_active() == sought_active
    assert caseb1_4.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_5, fig, linel, "caseb1_5", False, graph_b
    )
    assert caseb1_5.get_active() == sought_active
    assert caseb1_5.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_6, fig, linel, "caseb1_6", False, graph_b
    )
    assert caseb1_6.get_active() == sought_active
    assert caseb1_6.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb1_7, fig, linel, "caseb1_7", False, graph_b
    )
    assert caseb1_7.get_active() == sought_active
    assert caseb1_7.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_8, fig, linel, "caseb1_8", False, graph_b
    )
    assert caseb1_8.get_active() == sought_active
    assert caseb1_8.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_9, fig, linel, "caseb1_9", False, graph_b
    )
    assert caseb1_9.get_active() == sought_active
    assert caseb1_9.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb1_10, fig, linel, "caseb1_10", False, graph_b
    )
    assert caseb1_10.get_active() == sought_active
    assert caseb1_10.get_chore_status() == sought_chore

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
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb2_1, fig, linel, "caseb2_1", False, graph_b
    )
    assert caseb2_1.get_active() == sought_active
    assert caseb2_1.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb2_2, fig, linel, "caseb2_2", False, graph_b
    )
    assert caseb2_2.get_active() == sought_active
    assert caseb2_2.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb2_3, fig, linel, "caseb2_3", False, graph_b
    )
    assert caseb2_3.get_active() == sought_active
    assert caseb2_3.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb2_4, fig, linel, "caseb2_4", False, graph_b
    )
    assert caseb2_4.get_active() == sought_active
    assert caseb2_4.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb2_5, fig, linel, "caseb2_5", False, graph_b
    )
    assert caseb2_5.get_active() == sought_active
    assert caseb2_5.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb2_6, fig, linel, "caseb2_6", False, graph_b
    )
    assert caseb2_6.get_active() == sought_active
    assert caseb2_6.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb2_7, fig, linel, "caseb2_7", False, graph_b
    )
    assert caseb2_7.get_active() == sought_active
    assert caseb2_7.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb2_8, fig, linel, "caseb2_8", False, graph_b
    )
    assert caseb2_8.get_active() == sought_active
    assert caseb2_8.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb2_9, fig, linel, "caseb2_9", False, graph_b
    )
    assert caseb2_9.get_active() == sought_active
    assert caseb2_9.get_chore_status() == sought_chore

    # Case B3
    linel -= 0.1
    sought_active = True
    sought_chore = True
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
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb3_1, fig, linel, "caseb3_1", False, graph_b
    )
    assert caseb3_1.get_active() == sought_active
    assert caseb3_1.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_2, fig, linel, "caseb3_2", False, graph_b
    )
    assert caseb3_2.get_active() == sought_active
    assert caseb3_2.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_3, fig, linel, "caseb3_3", False, graph_b
    )
    assert caseb3_3.get_active() == sought_active
    assert caseb3_3.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_4, fig, linel, "caseb3_4", False, graph_b
    )
    assert caseb3_4.get_active() == sought_active
    assert caseb3_4.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_5, fig, linel, "caseb3_5", False, graph_b
    )
    assert caseb3_5.get_active() == sought_active
    assert caseb3_5.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_6, fig, linel, "caseb3_6", False, graph_b
    )
    assert caseb3_6.get_active() == sought_active
    assert caseb3_6.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = False
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_7, fig, linel, "caseb3_7", False, graph_b
    )
    assert caseb3_7.get_active() == sought_active
    assert caseb3_7.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb3_8, fig, linel, "caseb3_8", False, graph_b
    )
    assert caseb3_8.get_active() == sought_active
    assert caseb3_8.get_chore_status() == sought_chore

    # Case B4
    linel -= 0.1
    sought_active = True
    sought_chore = True
    caseb4_1 = premisestatusfinder_shop(0.7, 0.3, pd, 0.6, 1.2)
    caseb4_2 = premisestatusfinder_shop(0.7, 0.3, pd, 0.8, 1.4)
    caseb4_3 = premisestatusfinder_shop(0.7, 0.3, pd, 0.6, 1.4)
    caseb4_4 = premisestatusfinder_shop(0.7, 0.3, pd, 0.8, 1.2)
    caseb4_5 = premisestatusfinder_shop(0.7, 0.3, pd, 0.2, 1.1)
    caseb4_6 = premisestatusfinder_shop(0.7, 0.3, pd, 0.9, 1.8)
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb4_1, fig, linel, "caseb4_1", False, graph_b
    )
    assert caseb4_1.get_active() == sought_active
    assert caseb4_1.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb4_2, fig, linel, "caseb4_2", False, graph_b
    )
    assert caseb4_2.get_active() == sought_active
    assert caseb4_2.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = True
    show_x(
        sought_active, sought_chore, caseb4_3, fig, linel, "caseb4_3", False, graph_b
    )
    assert caseb4_3.get_active() == sought_active
    assert caseb4_3.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb4_4, fig, linel, "caseb4_4", False, graph_b
    )
    assert caseb4_4.get_active() == sought_active
    assert caseb4_4.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb4_5, fig, linel, "caseb4_5", False, graph_b
    )
    assert caseb4_5.get_active() == sought_active
    assert caseb4_5.get_chore_status() == sought_chore
    linel -= 0.1
    sought_active = True
    sought_chore = False
    show_x(
        sought_active, sought_chore, caseb4_6, fig, linel, "caseb4_6", False, graph_b
    )
    assert caseb4_6.get_active() == sought_active
    assert caseb4_6.get_chore_status() == sought_chore

    # Bottom p_divisor line
    _add_last_trace_and_show(fig, pd, linel, graph_b)


def _add_last_trace_and_show(fig: plotly_figure, pd, linel, graphics_bool: bool):
    if graphics_bool:
        add_trace(fig, 0.0, pd, linel - 0.2, "p_divisor Range", None)
        conditional_fig_show(fig, graphics_bool)


def test_premisefactstatusdata_CorrectlyCalculates_active_AndChoreStatusExample_01():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        p_lower=1305.0,
        p_upper=1305.0,
        p_divisor=1440,
        f_lower_full=20000,
        f_upper_full=29000,
    )
    print(f"----\n  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=}")
    print(f"  {segr_obj.p_lower=}  {segr_obj.p_upper=}  {segr_obj.p_divisor=}")
    print(
        f"  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=} \tdifference:{segr_obj.f_upper_full-segr_obj.f_lower_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_chore_status()=}")

    # THEN
    # assert segr_obj._fact_range_len == 9000
    # assert segr_obj.get_f_upper_mod_div() == 200
    assert segr_obj.get_active()
    assert segr_obj.get_chore_status()


def test_premisefactstatusdata_CorrectlyCalculates_active_AndChoreStatusExample_02():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        p_lower=1305.0,
        p_upper=1305.0,
        p_divisor=1440,
        f_lower_full=1300,
        f_upper_full=1400,
    )
    print(f"----\n  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=}")
    print(f"  {segr_obj.p_lower=}  {segr_obj.p_upper=}  {segr_obj.p_divisor=}")
    print(
        f"  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=} \tdifference:{segr_obj.f_upper_full-segr_obj.f_lower_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_chore_status()=}")

    # THEN
    assert segr_obj.get_active()
    assert segr_obj.get_chore_status()


def test_premisefactstatusdata_CorrectlyCalculates_active_AndChoreStatusExample_03():
    # ESTABLISH / WHEN
    segr_obj = premisestatusfinder_shop(
        p_lower=1305.0,
        p_upper=1305.0,
        p_divisor=1440,
        f_lower_full=1300,
        f_upper_full=1300,
    )
    print(f"----\n  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=}")
    print(f"  {segr_obj.p_lower=}  {segr_obj.p_upper=}  {segr_obj.p_divisor=}")
    print(
        f"  {segr_obj.f_lower_full=}  {segr_obj.f_upper_full=} \tdifference:{segr_obj.f_upper_full-segr_obj.f_lower_full}"
    )
    print(f"  {segr_obj.get_active()=}  {segr_obj.get_chore_status()=}")

    # THEN
    assert segr_obj.get_active() is False
    assert segr_obj.get_chore_status() is False
