from src.f00_instrument.file import create_path
from src.f01_road.allot import allot_nested_scale, allot_scale
from src.f04_gift.atom_config import face_name_str, fiscal_title_str
from src.f05_listen.hub_tool import create_events_owner_dir
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_title_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import upsert_sheet, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup


# create test where event create_events_owner_dir()
# test that deal_episode with depth 0 is able to create
# test that deal_episode with depth 1 is able to create nested budunits directories and populate with event relevant


# def test_WorldUnit_event_gift_json_to_event_inherited_budunits_SetsFiles_bud_json(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bobby"
#     yao_inx = "Yaoe"
#     event3 = 3
#     event7 = 7
#     credit44 = 44
#     credit77 = 77
#     credit88 = 88
#     a23_str = "accord23"
#     fizz_world = worldunit_shop("fizz")
#     fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
#     a23_bob_e3_dir = create_events_owner_dir(fiscals_dir, a23_str, bob_inx, event3)
#     a23_bob_e7_dir = create_events_owner_dir(fiscals_dir, a23_str, bob_inx, event7)
#     bud_filename = "bud.json"
#     e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
#     e7_bud_path = create_path(a23_bob_e7_dir, bud_filename)

#     # WHEN
#     fizz_world.event_gift_json_to_event_inherited_budunits()

#     # THEN
#     assert os_path_exists(e3_bud_path)
#     assert os_path_exists(e7_bud_path)
#     expected_e3_bob_bud = budunit_shop(bob_inx, a23_str)
#     expected_e7_bob_bud = budunit_shop(bob_inx, a23_str)
#     expected_e3_bob_bud.add_acctunit(bob_inx, credit77)
#     expected_e3_bob_bud.add_acctunit(yao_inx, credit44)
#     expected_e7_bob_bud.add_acctunit(bob_inx, credit77)
#     expected_e7_bob_bud.add_acctunit(sue_inx, credit88)
#     expected_e7_bob_bud.add_acctunit(yao_inx, credit44)
#     generated_e3_bud = budunit_get_from_json(open_file(e3_bud_path))
#     generated_e7_bud = budunit_get_from_json(open_file(e7_bud_path))
#     assert generated_e3_bud.accts == expected_e3_bob_bud.accts
#     assert generated_e3_bud == expected_e3_bob_bud
#     assert generated_e3_bud.get_dict() == expected_e3_bob_bud.get_dict()
#     assert generated_e7_bud.accts == expected_e7_bob_bud.accts
#     assert generated_e7_bud.get_dict() == expected_e7_bob_bud.get_dict()
