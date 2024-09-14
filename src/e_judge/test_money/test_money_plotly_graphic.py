from src.e_judge.money_graphic import (
    get_money_structures0_fig,
    get_money_structures1_fig,
    get_money_structures2_fig,
    get_money_structures3_fig,
    get_money_structures4_fig,
    get_money_structures5_fig,
)


def test_money_graphics_ExplainThingsWell(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_money_structures0_fig(graphics_bool)
    get_money_structures1_fig(graphics_bool)
    get_money_structures2_fig(graphics_bool)
    get_money_structures3_fig(graphics_bool)
    get_money_structures4_fig(graphics_bool)
    get_money_structures5_fig(graphics_bool)
