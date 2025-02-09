from src.f00_instrument.file import create_path, open_file, save_file
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import (
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    atom_insert,
)
from src.f04_gift.gift import giftunit_shop, get_giftunit_from_json
from src.f05_listen.hub_paths import create_events_owner_dir_path
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_event_gift_json_to_event_inherited_budunits_SetsFiles_bud_json(
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
    fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
    a23_bob_e3_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event7)
    a23_bob_e3_gift = giftunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_gift = giftunit_shop(bob_inx, None, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77, debtit_belief_str(): None}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44, debtit_belief_str(): None}
    a23_bob_e3_gift.add_atomunit(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_gift.add_atomunit(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88, debtit_belief_str(): None}
    a23_bob_e7_gift.add_atomunit(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_gift.add_atomunit(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    all_gift_filename = "all_gift.json"
    save_file(a23_bob_e3_dir, all_gift_filename, a23_bob_e3_gift.get_json())
    save_file(a23_bob_e7_dir, all_gift_filename, a23_bob_e7_gift.get_json())
    e3_gift_path = create_path(a23_bob_e3_dir, all_gift_filename)
    e7_gift_path = create_path(a23_bob_e7_dir, all_gift_filename)
    assert os_path_exists(e3_gift_path)
    assert os_path_exists(e7_gift_path)
    bud_filename = "bud.json"
    e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    e7_bud_path = create_path(a23_bob_e7_dir, bud_filename)
    assert os_path_exists(e3_bud_path) is False
    assert os_path_exists(e7_bud_path) is False

    # WHEN
    fizz_world.event_gift_json_to_event_inherited_budunits()

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


def test_WorldUnit_event_gift_json_to_event_inherited_budunits_SetsFiles_expressed_gift(
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
    fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
    a23_bob_e3_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event7)
    a23_bob_e3_gift = giftunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_gift = giftunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    bob_jkeys = {acct_name_str(): bob_inx}
    bob_jvalues = {credit_belief_str(): credit77}
    yao_jkeys = {acct_name_str(): yao_inx}
    yao_jvalues = {credit_belief_str(): credit44}
    a23_bob_e3_gift.add_atomunit(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e3_gift.add_atomunit(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    sue_jkeys = {acct_name_str(): sue_inx}
    sue_jvalues = {credit_belief_str(): credit88}
    a23_bob_e7_gift.add_atomunit(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    a23_bob_e7_gift.add_atomunit(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    all_gift_filename = "all_gift.json"
    save_file(a23_bob_e3_dir, all_gift_filename, a23_bob_e3_gift.get_json())
    save_file(a23_bob_e7_dir, all_gift_filename, a23_bob_e7_gift.get_json())
    expressed_gift_filename = "expressed_gift.json"
    e3_all_gift_path = create_path(a23_bob_e3_dir, all_gift_filename)
    e7_all_gift_path = create_path(a23_bob_e7_dir, all_gift_filename)
    e3_expressed_gift_path = create_path(a23_bob_e3_dir, expressed_gift_filename)
    e7_expressed_gift_path = create_path(a23_bob_e7_dir, expressed_gift_filename)
    assert os_path_exists(e3_all_gift_path)
    assert os_path_exists(e7_all_gift_path)
    assert os_path_exists(e3_expressed_gift_path) is False
    assert os_path_exists(e7_expressed_gift_path) is False

    # WHEN
    fizz_world.event_gift_json_to_event_inherited_budunits()

    # THEN
    assert os_path_exists(e3_expressed_gift_path)
    assert os_path_exists(e7_expressed_gift_path)
    gen_e3_express_gift = get_giftunit_from_json(open_file(e3_expressed_gift_path))
    gen_e7_express_gift = get_giftunit_from_json(open_file(e7_expressed_gift_path))
    expected_e3_bob_gift = giftunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_gift = giftunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_gift.add_atomunit(budacct_dimen, insert_str, bob_jkeys, bob_jvalues)
    expected_e3_bob_gift.add_atomunit(budacct_dimen, insert_str, yao_jkeys, yao_jvalues)
    expected_e7_bob_gift.add_atomunit(budacct_dimen, insert_str, sue_jkeys, sue_jvalues)
    assert expected_e3_bob_gift == a23_bob_e3_gift
    assert expected_e7_bob_gift._buddelta != a23_bob_e7_gift._buddelta
    assert expected_e7_bob_gift != a23_bob_e7_gift
    # expected_e3_bob_gift.add_atomunit()
    # expected_e3_bob_gift.add_atomunit()
    # expected_e7_bob_gift.add_atomunit()
    # expected_e7_bob_gift.add_atomunit()
    # expected_e7_bob_gift.add_atomunit()
    assert gen_e3_express_gift == expected_e3_bob_gift
    gen_e7_express_delta = gen_e7_express_gift._buddelta
    expected_e7_delta = expected_e7_bob_gift._buddelta
    assert gen_e7_express_delta.atomunits == expected_e7_delta.atomunits
    assert gen_e7_express_gift._buddelta == expected_e7_bob_gift._buddelta
    assert gen_e7_express_gift == expected_e7_bob_gift
