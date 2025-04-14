from src.a00_data_toolboxs.file_toolbox import create_path, save_file, open_file
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f06_listen.hub_path import create_owner_event_dir_path, create_gut_path
from src.f11_etl.transformers import etl_event_inherited_budunits_to_fisc_gut
from src.f11_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from os.path import exists as os_path_exists

# create test where event create_owner_event_dir_path()
# test that dealunit with depth 0 is able to create
# test that dealunit with depth 1 is able to create nested budunits directories and populate with event relevant


def test_etl_event_inherited_budunits_to_fisc_gut_SetsFiles_Scenario0(
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
    fisc_mstr_dir = get_test_etl_dir()
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
    print(e3_bud_path)
    print(e7_bud_path)
    a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_event_inherited_budunits_to_fisc_gut(fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_bud = budunit_get_from_json(open_file(a23_bob_gut_path))
    assert generated_gut_bud.accts == e7_bob_bud.accts
    assert generated_gut_bud == e7_bob_bud
    assert generated_gut_bud.get_dict() == e7_bob_bud.get_dict()
