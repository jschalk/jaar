from src.listen.examples.example_listen_buds import get_fund_explanation_bud
from src.listen.listen_graphic import (
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
    fund_explanation0,
)


def test_listen_structures0_ShowsExplanation0Graph():
    # ESTABLISH / WHEN
    # listen_structures0_fig = get_listen_structures0_fig()
    # listen_structures1_fig = get_listen_structures1_fig()
    # listen_structures2_fig = get_listen_structures2_fig()
    listen_structures3_fig = get_listen_structures3_fig()

    # # THEN
    # show_figure = True
    # if show_figure:
    #     listen_structures0_fig.show()
    #     # listen_structures1_fig.show()
    #     # listen_structures2_fig.show()
    #     # listen_structures3_fig.show()


def test_fund_explanation_Graph():
    # ESTABLISH / WHEN
    x_budunit = get_fund_explanation_bud()
    fund_explanation0_fig = fund_explanation0(x_budunit, "Task")

    # THEN
    # fund_explanation0_fig.show()
