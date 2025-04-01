from src.f00_instrument.file import create_path, open_file, save_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_vow.atom_config import (
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    atom_insert,
)
from src.f04_vow.vow import vowunit_shop, get_vowunit_from_json
from src.f05_listen.hub_path import (
    create_owner_event_dir_path,
    create_budevent_path,
    create_event_all_vow_path,
    create_event_expressed_vow_path,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_event_vow_json_to_event_inherited_budunits_SetsFiles_bud_json(
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
    a23_bob_e3_vow = vowunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_vow = vowunit_shop(bob_inx, None, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77, debtit_belief_str(): None}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44, debtit_belief_str(): None}
    a23_bob_e3_vow.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_vow.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88, debtit_belief_str(): None}
    a23_bob_e7_vow.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_vow.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    e3_all_vow_path = create_event_all_vow_path(fisc_mstr_dir, a23_str, bob_inx, event3)
    e7_all_vow_path = create_event_all_vow_path(fisc_mstr_dir, a23_str, bob_inx, event7)
    save_file(e3_all_vow_path, None, a23_bob_e3_vow.get_json())
    save_file(e7_all_vow_path, None, a23_bob_e7_vow.get_json())
    assert os_path_exists(e3_all_vow_path)
    assert os_path_exists(e7_all_vow_path)
    bud_filename = "bud.json"
    e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    e7_bud_path = create_path(a23_bob_e7_dir, bud_filename)
    assert os_path_exists(e3_bud_path) is False
    assert os_path_exists(e7_bud_path) is False

    # WHEN
    fizz_world.event_vow_json_to_event_inherited_budunits()

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


def test_WorldUnit_event_vow_json_to_event_inherited_budunits_SetsFiles_expressed_vow(
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
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_bob_e3_vow = vowunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_vow = vowunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44}
    a23_bob_e3_vow.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_vow.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88}
    a23_bob_e7_vow.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_vow.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_vow_path = create_event_all_vow_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_all_vow_path = create_event_all_vow_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(a23_bob_e3_all_vow_path, None, a23_bob_e3_vow.get_json())
    save_file(a23_bob_e7_all_vow_path, None, a23_bob_e7_vow.get_json())
    e3_expressed_vow_path = create_event_expressed_vow_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    e7_expressed_vow_path = create_event_expressed_vow_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    assert os_path_exists(a23_bob_e3_all_vow_path)
    assert os_path_exists(a23_bob_e7_all_vow_path)
    assert os_path_exists(e3_expressed_vow_path) is False
    assert os_path_exists(e7_expressed_vow_path) is False

    # WHEN
    fizz_world.event_vow_json_to_event_inherited_budunits()

    # THEN
    assert os_path_exists(e3_expressed_vow_path)
    assert os_path_exists(e7_expressed_vow_path)
    gen_e3_express_vow = get_vowunit_from_json(open_file(e3_expressed_vow_path))
    gen_e7_express_vow = get_vowunit_from_json(open_file(e7_expressed_vow_path))
    expected_e3_bob_vow = vowunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_vow = vowunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_vow.add_budatom(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    expected_e3_bob_vow.add_budatom(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    expected_e7_bob_vow.add_budatom(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    assert expected_e3_bob_vow == a23_bob_e3_vow
    assert expected_e7_bob_vow._buddelta != a23_bob_e7_vow._buddelta
    assert expected_e7_bob_vow != a23_bob_e7_vow
    # expected_e3_bob_vow.add_budatom()
    # expected_e3_bob_vow.add_budatom()
    # expected_e7_bob_vow.add_budatom()
    # expected_e7_bob_vow.add_budatom()
    # expected_e7_bob_vow.add_budatom()
    assert gen_e3_express_vow == expected_e3_bob_vow
    gen_e7_express_delta = gen_e7_express_vow._buddelta
    expected_e7_delta = expected_e7_bob_vow._buddelta
    assert gen_e7_express_delta.budatoms == expected_e7_delta.budatoms
    assert gen_e7_express_vow._buddelta == expected_e7_bob_vow._buddelta
    assert gen_e7_express_vow == expected_e7_bob_vow
