from src.f00_instrument.file import create_path, save_file, open_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f05_listen.hub_path import create_owner_event_dir_path, create_voice_path
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_event_inherited_budunits_to_fisc_voice_SetsFiles_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_bob_e3_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    bud_filename = "bud.json"
    e3_bob_bud = budunit_shop(bob_inx, a23_str)
    e7_bob_bud = budunit_shop(bob_inx, a23_str)
    e3_bob_bud.add_acctunit(bob_inx, credit77)
    e3_bob_bud.add_acctunit(yao_inx, credit44)
    e7_bob_bud.add_acctunit(bob_inx, credit77)
    e7_bob_bud.add_acctunit(sue_inx, credit88)
    e7_bob_bud.add_acctunit(yao_inx, credit44)
    save_file(a23_bob_e3_dir, bud_filename, e3_bob_bud.get_json())
    save_file(a23_bob_e7_dir, bud_filename, e7_bob_bud.get_json())
    e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    e7_bud_path = create_path(a23_bob_e7_dir, bud_filename)
    assert os_path_exists(e3_bud_path)
    assert os_path_exists(e7_bud_path)
    a23_bob_voice_path = create_voice_path(fisc_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_voice_path) is False

    # WHEN
    fizz_world.event_inherited_budunits_to_fisc_voice()

    # THEN
    assert os_path_exists(a23_bob_voice_path)
    generated_voice_bud = budunit_get_from_json(open_file(a23_bob_voice_path))
    assert generated_voice_bud.accts == e7_bob_bud.accts
    assert generated_voice_bud == e7_bob_bud
    assert generated_voice_bud.get_dict() == e7_bob_bud.get_dict()
