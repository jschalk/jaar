# from src._world.examples.example_worlds import (
#     world_v001_with_large_agenda,
#     get_world_with_4_levels,
#     get_world_with_4_levels_and_2reasons,
#     get_world_x1_3levels_1reason_1facts,
#     get_world_laundry_example1,
# )

# from src._world.world import worldunit_shop
# from src._world.graphic import (
#     worldunit_explanation0,
#     worldunit_explanation1,
#     worldunit_explanation2,
#     worldunit_explanation3,
#     worldunit_explanation4,
#     fund_explanation0,
#     display_ideatree,
#     get_world_chars_plotly_fig,
#     get_world_agenda_plotly_fig,
# )
# from src.gift.atom_graphic import atomunit_periodic_table0
# from src.listen.listen_graphic import (
#     get_listen_structures0_fig,
#     get_listen_structures1_fig,
#     get_listen_structures2_fig,
#     get_listen_structures3_fig,
# )
# from src.money.money_graphic import (
#     get_money_structures0_fig,
#     get_money_structures1_fig,
#     get_money_structures2_fig,
#     get_money_structures3_fig,
#     get_money_structures4_fig,
#     get_money_structures5_fig,
# )
# from src.real.real_graphic import get_real_structures0_fig


# def test_display_graphics_listed():
#     # a_world = get_1node_world()
#     # a_world = get_2node_world()
#     # a_world = get_3node_world()
#     # a_world = get_5nodeHG_world()
#     # a_world = get_7nodeJRoot_world()
#     # a_world = world_v001()
#     a_world = get_world_with_4_levels()
#     a_world.settle_world()
#     print(f"World {a_world._real_id}: Nodes ({len(a_world._idea_dict)})")

#     # THEN
#     display_ideatree(a_world).show()

#     # b_world = get_1node_world()
#     # b_world = get_2node_world()
#     # b_world = get_3node_world()
#     # b_world = get_5nodeHG_world()
#     # b_world = get_7nodeJRoot_world()
#     b_world = get_world_laundry_example1()
#     # b_world = world_v001()
#     b_world.settle_world()
#     print(f"World {b_world._real_id}: Nodes ({len(b_world._idea_dict)})")

#     # THEN
#     display_ideatree(b_world, mode="Task").show()

#     # ESTABLISH
#     luca_world = worldunit_shop()
#     luca_world.set_credor_respect(500)
#     luca_world.set_debtor_resepect(400)
#     yao_text = "Yao"
#     yao_credor_weight = 66
#     yao_debtor_weight = 77
#     luca_world.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
#     sue_text = "Sue"
#     sue_credor_weight = 434
#     sue_debtor_weight = 323
#     luca_world.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)

#     # WHEN
#     get_world_chars_plotly_fig(luca_world).show()

#     yao_world = world_v001_with_large_agenda()
#     week_text = "weekdays"
#     week_road = yao_world.make_l1_road(week_text)
#     assert len(yao_world.get_agenda_dict()) == 63

#     # WHEN
#     get_world_agenda_plotly_fig(yao_world).show()

#     # ESTABLISH / WHEN
#     worldunit_explanation0_fig = worldunit_explanation0()
#     worldunit_explanation1_fig = worldunit_explanation1()
#     worldunit_explanation2_fig = worldunit_explanation2()
#     worldunit_explanation3_fig = worldunit_explanation3()
#     worldunit_explanation4_fig = worldunit_explanation4()
#     fund_explanation0_fig = fund_explanation0()

#     # THEN
#     worldunit_explanation0_fig.show()
#     worldunit_explanation1_fig.show()
#     worldunit_explanation2_fig.show()
#     worldunit_explanation3_fig.show()
#     worldunit_explanation4_fig.show()
#     fund_explanation0_fig.show()

#     # ESTABLISH / WHEN
#     atomunit_periodic_table0_fig = atomunit_periodic_table0()
#     atomunit_periodic_table0_fig.show()

#     listen_structures0_fig = get_listen_structures0_fig()
#     listen_structures1_fig = get_listen_structures1_fig()
#     listen_structures2_fig = get_listen_structures2_fig()
#     listen_structures3_fig = get_listen_structures3_fig()

#     # THEN
#     listen_structures0_fig.show()
#     listen_structures1_fig.show()
#     listen_structures2_fig.show()
#     listen_structures3_fig.show()

#     # ESTABLISH / WHEN
#     money_structures0_fig = get_money_structures0_fig()
#     money_structures1_fig = get_money_structures1_fig()
#     money_structures2_fig = get_money_structures2_fig()
#     money_structures3_fig = get_money_structures3_fig()
#     money_structures4_fig = get_money_structures4_fig()
#     money_structures5_fig = get_money_structures5_fig()

#     # THEN
#     money_structures0_fig.show()
#     money_structures1_fig.show()
#     money_structures2_fig.show()
#     money_structures3_fig.show()
#     money_structures4_fig.show()
#     money_structures5_fig.show()

#     # ESTABLISH / WHEN
#     real_structures0_fig = get_real_structures0_fig()

#     # THEN
#     real_structures0_fig.show()
