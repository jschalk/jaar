# from datetime import datetime
# from src._road.road import RoadUnit
# from src._world.world import worldunit_shop, get_from_json as worldunit_get_from_json
# from src._world.idea import IdeaUnit, ideaunit_shop
# from src._world.reason_idea import reasonunit_shop
# from src._world.beliefbox import beliefbox_shop, awardlink_shop
# from src._world.char import charlink_shop
# from src._world.reason_doer import doerunit_shop
# from src._world.examples.example_worlds import (
#     get_world_with_4_levels as example_worlds_get_world_with_4_levels,
#     get_world_with_4_levels_and_2reasons as example_worlds_get_world_with_4_levels_and_2reasons,
#     get_world_with7amCleanTableReason as example_worlds_get_world_with7amCleanTableReason,
#     get_world_with_4_levels_and_2reasons_2facts as example_worlds_get_world_with_4_levels_and_2reasons_2facts,
#     world_v001 as example_worlds_world_v001,
#     world_v001_with_large_agenda as example_worlds_world_v001_with_large_agenda,
#     world_v002 as example_worlds_world_v002,
# )


# def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario0():
#     # Given
#     sue_text = "Sue"
#     sue_worldunit = worldunit_shop(sue_text)
#     assert sue_worldunit._beliefs == {}

#     # WHEN
#     sue_worldunit._calc_charunit_metrics()

#     # THEN
#     assert sue_worldunit._beliefs == {}


# def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario1():
#     # Given
#     sue_text = "Sue"
#     sue_worldunit = worldunit_shop(sue_text)
#     yao_text = "Yao"
#     sue_worldunit.add_charunit(yao_text)
#     yao_charunit = sue_worldunit.get_char(yao_text)
#     assert yao_charunit._credor_pool == 0
#     assert yao_charunit._debtor_pool == 0
#     assert yao_charunit.get_belieflink(yao_text)._credor_pool == 0
#     assert yao_charunit.get_belieflink(yao_text)._debtor_pool == 0
#     assert sue_worldunit._beliefs == {}

#     # WHEN
#     sue_worldunit._calc_charunit_metrics()

#     # THEN
#     assert yao_charunit._credor_pool != 0
#     assert yao_charunit._debtor_pool != 0
#     assert yao_charunit._credor_pool == sue_worldunit._credor_respect
#     assert yao_charunit._debtor_pool == sue_worldunit._debtor_respect
#     yao_belieflink = yao_charunit.get_belieflink(yao_text)
#     assert yao_belieflink._credor_pool != 0
#     assert yao_belieflink._debtor_pool != 0
#     assert yao_belieflink._credor_pool == sue_worldunit._credor_respect
#     assert yao_belieflink._debtor_pool == sue_worldunit._debtor_respect
#     # assert len(sue_worldunit._beliefs) == 1
#     # yao_beliefbox = sue_worldunit.get_beliefbox(yao_text)
#     # assert len(yao_beliefbox._chars) == 1
#     # yao_belieflink = yao_beliefbox.get_belieflink(yao_text)
#     # assert yao_belieflink._credor_pool != 0
#     # assert yao_belieflink._debtor_pool != 0
#     # assert yao_belieflink._credor_pool == sue_worldunit._credor_respect
#     # assert yao_belieflink._debtor_pool == sue_worldunit._debtor_respect
#     # assert yao_belieflink._credor_pool == 200000000
#     # assert yao_belieflink._debtor_pool == 200000000


# def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario2():
#     # Given
#     sue_text = "Sue"
#     sue_worldunit = worldunit_shop(sue_text)
#     yao_text = "Yao"
#     sue_worldunit.add_charunit(yao_text)
#     yao_charunit = sue_worldunit.get_char(yao_text)
#     ohio_text = "Ohio"
#     yao_charunit.add_belieflink(ohio_text)
#     assert yao_charunit._credor_pool == 0
#     assert yao_charunit._debtor_pool == 0
#     assert yao_charunit.get_belieflink(yao_text)._credor_pool == 0
#     assert yao_charunit.get_belieflink(yao_text)._debtor_pool == 0
#     assert sue_worldunit._beliefs == {}

#     # WHEN
#     sue_worldunit._calc_charunit_metrics()

#     # THEN
#     assert sue_worldunit.get_char(yao_text)._credor_pool != 0
#     assert sue_worldunit.get_char(yao_text)._debtor_pool != 0
#     assert yao_charunit.get_belieflink(yao_text)._credor_pool != 0
#     assert yao_charunit.get_belieflink(yao_text)._debtor_pool != 0
#     yao_ohio_belieflink = yao_charunit.get_belieflink(yao_text)
#     assert yao_ohio_belieflink._credor_pool != 0
#     assert yao_ohio_belieflink._debtor_pool != 0
#     assert yao_ohio_belieflink._credor_pool == sue_worldunit._credor_respect
#     assert yao_ohio_belieflink._debtor_pool == sue_worldunit._debtor_respect
#     assert yao_ohio_belieflink._credor_pool == 200000000
#     assert yao_ohio_belieflink._debtor_pool == 200000000
#     # assert len(sue_worldunit._beliefs) == 2
#     # ohio_beliefbox = sue_worldunit.get_beliefbox(ohio_text)
#     # assert len(ohio_beliefbox._chars) == 1
