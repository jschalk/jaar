# from src.bud.examples.example_buds import (
#     budunit_v001_with_large_agenda,
#     get_budunit_with_4_levels,
#     get_budunit_with_4_levels_and_2reasons,
#     get_budunit_x1_3levels_1reason_1facts,
#     get_budunit_laundry_example1,
# )

# from src.bud.bud import budunit_shop
# from src.bud.graphic import (
#     budunit_explanation0,
#     budunit_explanation1,
#     budunit_explanation2,
#     budunit_explanation3,
#     budunit_explanation4,
#     fund_explanation0,
#     display_ideatree,
#     get_bud_chars_plotly_fig,
#     get_bud_agenda_plotly_fig,
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
#     # a_bud = get_1node_bud()
#     # a_bud = get_2node_bud()
#     # a_bud = get_3node_bud()
#     # a_bud = get_5nodeHG_bud()
#     # a_bud = get_7nodeJRoot_bud()
#     # a_bud = budunit_v001()
#     a_bud = get_budunit_with_4_levels()
#     a_bud.settle_bud()
#     print(f"Bud {a_bud._real_id}: Nodes ({len(a_bud._idea_dict)})")

#     # THEN
#     display_ideatree(a_bud).show()

#     # b_bud = get_1node_bud()
#     # b_bud = get_2node_bud()
#     # b_bud = get_3node_bud()
#     # b_bud = get_5nodeHG_bud()
#     # b_bud = get_7nodeJRoot_bud()
#     b_bud = get_budunit_laundry_example1()
#     # b_bud = budunit_v001()
#     b_bud.settle_bud()
#     print(f"Bud {b_bud._real_id}: Nodes ({len(b_bud._idea_dict)})")

#     # THEN
#     display_ideatree(b_bud, mode="Task").show()

#     # ESTABLISH
#     luca_bud = budunit_shop()
#     luca_bud.set_credor_respect(500)
#     luca_bud.set_debtor_resepect(400)
#     yao_text = "Yao"
#     yao_credor_weight = 66
#     yao_debtor_weight = 77
#     luca_bud.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
#     sue_text = "Sue"
#     sue_credor_weight = 434
#     sue_debtor_weight = 323
#     luca_bud.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)

#     # WHEN
#     get_bud_chars_plotly_fig(luca_bud).show()

#     yao_bud = budunit_v001_with_large_agenda()
#     week_text = "weekdays"
#     week_road = yao_bud.make_l1_road(week_text)
#     assert len(yao_bud.get_agenda_dict()) == 63

#     # WHEN
#     get_bud_agenda_plotly_fig(yao_bud).show()

#     # ESTABLISH / WHEN
#     budunit_explanation0_fig = budunit_explanation0()
#     budunit_explanation1_fig = budunit_explanation1()
#     budunit_explanation2_fig = budunit_explanation2()
#     budunit_explanation3_fig = budunit_explanation3()
#     budunit_explanation4_fig = budunit_explanation4()
#     fund_explanation0_fig = fund_explanation0()

#     # THEN
#     budunit_explanation0_fig.show()
#     budunit_explanation1_fig.show()
#     budunit_explanation2_fig.show()
#     budunit_explanation3_fig.show()
#     budunit_explanation4_fig.show()
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
