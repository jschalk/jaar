from src.f00_instrument.file_toolbox import create_path, open_file, save_file
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_pack.atom_config import (
    face_name_str,
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    event_int_str,
    atom_insert,
    atom_delete,
)
from src.f04_pack.pack import packunit_shop, get_packunit_from_json
from src.f06_listen.hub_path import (
    create_owner_event_dir_path,
    create_event_all_pack_path as event_all_pack_path,
)

from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_event_bud_csvs_to_pack_json_CreatesFiles(
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
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_owner_event_dir_path(
        fisc_mstr_dir, a23_str, bob_inx, event7
    )
    e3_put_csv = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()}
{sue_inx},{event3},{a23_str},{bob_inx},{bob_inx},{credit77},{debtit_empty}
"""
    e7_put_csv = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()}
{sue_inx},{event7},{a23_str},{bob_inx},{bob_inx},{credit77},{debtit_empty}
{sue_inx},{event7},{a23_str},{bob_inx},{sue_inx},{credit88},{debtit_empty}
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    e3_all_pack_path = event_all_pack_path(fisc_mstr_dir, a23_str, bob_inx, event3)
    e7_all_pack_path = event_all_pack_path(fisc_mstr_dir, a23_str, bob_inx, event7)
    assert os_path_exists(e3_all_pack_path) is False
    assert os_path_exists(e7_all_pack_path) is False

    # WHEN
    fizz_world.event_bud_csvs_to_pack_json()

    # THEN
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    # print(f"{open_file(e3_pack_path)=}")
    # print(f"{open_file(e7_pack_path)=}")
    # packs_dir = create_path(fizz_world._fisc_mstr_dir, "packs")
    # atoms_dir = create_path(fizz_world._fisc_mstr_dir, "atoms")
    # e3_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event3)
    # e7_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event7)
    expected_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    expected_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    budacct_dimen = bud_acctunit_str()
    insert_str = atom_insert()
    expected_e3_pack._buddelta.add_budatom(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): bob_inx},
        jvalues={credit_belief_str(): credit77, debtit_belief_str(): None},
    )
    expected_e7_pack._buddelta.add_budatom(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): bob_inx},
        jvalues={credit_belief_str(): credit77, debtit_belief_str(): None},
    )
    expected_e7_pack._buddelta.add_budatom(
        budacct_dimen,
        insert_str,
        jkeys={acct_name_str(): sue_inx},
        jvalues={credit_belief_str(): credit88, debtit_belief_str(): None},
    )
    e3_packunit = get_packunit_from_json(open_file(e3_all_pack_path))
    e7_packunit = get_packunit_from_json(open_file(e7_all_pack_path))
    # print(f"{e7_packunit=}")
    assert e3_packunit.event_int == expected_e3_pack.event_int
    expected_buddelta = expected_e3_pack._buddelta
    generated_e3_buddelta = e3_packunit._buddelta
    assert generated_e3_buddelta.budatoms == expected_buddelta.budatoms
    assert e3_packunit._buddelta == expected_e3_pack._buddelta
    assert e3_packunit == expected_e3_pack
    e7_insert = e7_packunit._buddelta.budatoms.get("INSERT")
    expected_e7_insert = expected_e7_pack._buddelta.budatoms.get("INSERT")
    # print(e7_insert.get("bud_acctunit").keys())
    # print(expected_e7_insert.get("bud_acctunit").keys())
    e7_budacct = e7_insert.get("bud_acctunit")
    expected_e7_budacct = expected_e7_insert.get("bud_acctunit")
    assert e7_budacct.keys() == expected_e7_budacct.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_packunit._buddelta == expected_e7_pack._buddelta
    assert e7_packunit == expected_e7_pack
