from src.a06_owner_logic.owner_graphics import (
    display_plantree,
    ownerunit_graph0,
    ownerunit_graph1,
    ownerunit_graph2,
    ownerunit_graph3,
    ownerunit_graph4,
)
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with_4_levels,
    get_ownerunit_with_4_levels_and_2reasons,
    get_ownerunit_x1_3levels_1reason_1facts,
)


def test_ownerunit_graph_Showsgraph0OwnerGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_plantree(get_ownerunit_with_4_levels(), graphics_bool)
    display_plantree(get_ownerunit_with_4_levels_and_2reasons(), "Chore", graphics_bool)
    display_plantree(get_ownerunit_x1_3levels_1reason_1facts(), graphics_bool)
    ownerunit_graph0(graphics_bool)
    ownerunit_graph1(graphics_bool)
    ownerunit_graph2(graphics_bool)
    ownerunit_graph3(graphics_bool)
    ownerunit_graph4(graphics_bool)
