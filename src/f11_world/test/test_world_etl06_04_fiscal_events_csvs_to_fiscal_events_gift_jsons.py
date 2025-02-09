from src.f00_instrument.file import create_path, open_file, save_file
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    owner_name_str,
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    atom_insert,
    atom_delete,
)
from src.f04_gift.gift import giftunit_shop, get_giftunit_from_json
from src.f05_listen.hub_paths import create_events_owner_dir_path
from src.f08_pidgin.pidgin_config import event_int_str
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_event_bud_csvs_to_gift_json_CreatesFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    credit77 = 77
    credit88 = 88
    debtit_empty = ""
    a23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    put_agg_tablename = f"{bud_acctunit_str()}_put_agg"
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    fiscals_dir = create_path(fizz_world._fiscal_mstr_dir, "fiscals")
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = create_events_owner_dir_path(fiscals_dir, a23_str, bob_inx, event7)
    e3_put_csv = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()}
{sue_inx},{event3},{a23_str},{bob_inx},{bob_inx},{credit77},{debtit_empty}
"""
    e7_put_csv = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()}
{sue_inx},{event7},{a23_str},{bob_inx},{bob_inx},{credit77},{debtit_empty}
{sue_inx},{event7},{a23_str},{bob_inx},{sue_inx},{credit88},{debtit_empty}
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    gift_filename = "all_gift.json"
    e3_gift_path = create_path(a23_bob_e3_dir, gift_filename)
    e7_gift_path = create_path(a23_bob_e7_dir, gift_filename)
    # print(f"{e3_gift_path=}")
    # print(f"{e7_gift_path=}")
    assert os_path_exists(e3_gift_path) is False
    assert os_path_exists(e7_gift_path) is False

    # WHEN
    fizz_world.event_bud_csvs_to_gift_json()

    # THEN
    assert os_path_exists(e3_gift_path)
    assert os_path_exists(e7_gift_path)
    # print(f"{open_file(e3_gift_path)=}")
    # print(f"{open_file(e7_gift_path)=}")
    # gifts_dir = create_path(fizz_world._fiscal_mstr_dir, "gifts")
    # atoms_dir = create_path(fizz_world._fiscal_mstr_dir, "atoms")
    # e3_gift = giftunit_shop(bob_inx, sue_inx, a23_str, gifts_dir, atoms_dir, event3)
    # e7_gift = giftunit_shop(bob_inx, sue_inx, a23_str, gifts_dir, atoms_dir, event7)
    expected_e3_gift = giftunit_shop(bob_inx, None, a23_str, event_int=event3)
    expected_e7_gift = giftunit_shop(bob_inx, None, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    expected_e3_gift._buddelta.add_atomunit(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): bob_inx},
        jvalues={credit_belief_str(): credit77, debtit_belief_str(): None},
    )
    expected_e7_gift._buddelta.add_atomunit(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): bob_inx},
        jvalues={credit_belief_str(): credit77, debtit_belief_str(): None},
    )
    expected_e7_gift._buddelta.add_atomunit(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): sue_inx},
        jvalues={credit_belief_str(): credit88, debtit_belief_str(): None},
    )
    e3_giftunit = get_giftunit_from_json(open_file(e3_gift_path))
    e7_giftunit = get_giftunit_from_json(open_file(e7_gift_path))
    # print(f"{e7_giftunit=}")
    assert e3_giftunit.event_int == expected_e3_gift.event_int
    expected_buddelta = expected_e3_gift._buddelta
    generated_e3_buddelta = e3_giftunit._buddelta
    assert generated_e3_buddelta.atomunits == expected_buddelta.atomunits
    assert e3_giftunit._buddelta == expected_e3_gift._buddelta
    assert e3_giftunit == expected_e3_gift
    e7_insert = e7_giftunit._buddelta.atomunits.get("INSERT")
    expected_e7_insert = expected_e7_gift._buddelta.atomunits.get("INSERT")
    # print(e7_insert.get("bud_acctunit").keys())
    # print(expected_e7_insert.get("bud_acctunit").keys())
    e7_budacct = e7_insert.get("bud_acctunit")
    expected_e7_budacct = expected_e7_insert.get("bud_acctunit")
    assert e7_budacct.keys() == expected_e7_budacct.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_giftunit._buddelta == expected_e7_gift._buddelta
    assert e7_giftunit == expected_e7_gift
