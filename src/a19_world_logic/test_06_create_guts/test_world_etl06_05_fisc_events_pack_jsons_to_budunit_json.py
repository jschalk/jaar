from src.a00_data_toolboxs.file_toolbox import create_path, open_file, save_file
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.a06_bud_logic.bud_tool import bud_acctunit_str
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    atom_insert,
)
from src.a09_pack_logic.pack import packunit_shop, get_packunit_from_json
from src.a12_hub_tools.hub_path import (
    create_owner_event_dir_path,
    create_budevent_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_utils import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_WorldUnit_event_pack_json_to_event_inherited_budunits_SetsFiles_bud_json(
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
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_bob_e3_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    a23_bob_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77, debtit_belief_str(): None}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44, debtit_belief_str(): None}
    a23_bob_e3_pack.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88, debtit_belief_str(): None}
    a23_bob_e7_pack.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    e3_all_pack_path = create_event_all_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    e7_all_pack_path = create_event_all_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    bud_filename = "bud.json"
    e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    e7_bud_path = create_path(a23_bob_e7_dir, bud_filename)
    assert os_path_exists(e3_bud_path) is False
    assert os_path_exists(e7_bud_path) is False

    # WHEN
    fizz_world.event_pack_json_to_event_inherited_budunits()

    # THEN
    assert os_path_exists(e3_bud_path)
    assert os_path_exists(e7_bud_path)
    expected_e3_bob_bud = budunit_shop(bob_inx, a23_str)
    expected_e7_bob_bud = budunit_shop(bob_inx, a23_str)
    expected_e3_bob_bud.add_acctunit(bob_inx, credit77)
    expected_e3_bob_bud.add_acctunit(yao_inx, credit44)
    expected_e7_bob_bud.add_acctunit(bob_inx, credit77)
    expected_e7_bob_bud.add_acctunit(sue_inx, credit88)
    expected_e7_bob_bud.add_acctunit(yao_inx, credit44)
    generated_e3_bud = budunit_get_from_json(open_file(e3_bud_path))
    generated_e7_bud = budunit_get_from_json(open_file(e7_bud_path))
    assert generated_e3_bud.accts == expected_e3_bob_bud.accts
    assert generated_e3_bud == expected_e3_bob_bud
    assert generated_e3_bud.get_dict() == expected_e3_bob_bud.get_dict()
    assert generated_e7_bud.accts == expected_e7_bob_bud.accts
    assert generated_e7_bud.get_dict() == expected_e7_bob_bud.get_dict()


def test_WorldUnit_event_pack_json_to_event_inherited_budunits_SetsFiles_expressed_pack(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "accord23"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_bob_e3_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44}
    a23_bob_e3_pack.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88}
    a23_bob_e7_pack.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_pack_path = create_event_all_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_all_pack_path = create_event_all_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(a23_bob_e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(a23_bob_e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    e3_expressed_pack_path = create_event_expressed_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    e7_expressed_pack_path = create_event_expressed_pack_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    assert os_path_exists(a23_bob_e3_all_pack_path)
    assert os_path_exists(a23_bob_e7_all_pack_path)
    assert os_path_exists(e3_expressed_pack_path) is False
    assert os_path_exists(e7_expressed_pack_path) is False

    # WHEN
    fizz_world.event_pack_json_to_event_inherited_budunits()

    # THEN
    assert os_path_exists(e3_expressed_pack_path)
    assert os_path_exists(e7_expressed_pack_path)
    gen_e3_express_pack = get_packunit_from_json(open_file(e3_expressed_pack_path))
    gen_e7_express_pack = get_packunit_from_json(open_file(e7_expressed_pack_path))
    expected_e3_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_pack.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    expected_e3_bob_pack.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    expected_e7_bob_pack.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    assert expected_e3_bob_pack == a23_bob_e3_pack
    assert expected_e7_bob_pack._buddelta != a23_bob_e7_pack._buddelta
    assert expected_e7_bob_pack != a23_bob_e7_pack
    # expected_e3_bob_pack.add_budatom()
    # expected_e3_bob_pack.add_budatom()
    # expected_e7_bob_pack.add_budatom()
    # expected_e7_bob_pack.add_budatom()
    # expected_e7_bob_pack.add_budatom()
    assert gen_e3_express_pack == expected_e3_bob_pack
    gen_e7_express_delta = gen_e7_express_pack._buddelta
    expected_e7_delta = expected_e7_bob_pack._buddelta
    assert gen_e7_express_delta.budatoms == expected_e7_delta.budatoms
    assert gen_e7_express_pack._buddelta == expected_e7_bob_pack._buddelta
    assert gen_e7_express_pack == expected_e7_bob_pack
