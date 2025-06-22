from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_file, save_file
from src.a02_finance_logic.test._util.a02_str import belief_label_str, owner_name_str
from src.a06_plan_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    plan_acctunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.hub_path import (
    create_event_all_pack_path as all_pack_path,
    create_owner_event_dir_path as owner_event_dir,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a18_etl_toolbox.transformers import etl_event_plan_csvs_to_pack_json


def test_etl_event_plan_csvs_to_pack_json_CreatesFiles_Scenario0_IgnoresCSV_planunit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    a23_str = "accord23"
    put_agg_tablename = create_prime_tablename(planunit_str(), "v", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    belief_mstr_dir = get_module_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = owner_event_dir(belief_mstr_dir, a23_str, bob_inx, event3)
    e3_put_csv = f"""{event_int_str()},{face_name_str()},belief_label,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_iota,penny,respect_bit
{event3},{sue_inx},{a23_str},{bob_inx},,,,,,,,
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    e3_all_pack_path = all_pack_path(belief_mstr_dir, a23_str, bob_inx, event3)
    assert os_path_exists(e3_all_pack_path) is False

    # WHEN
    etl_event_plan_csvs_to_pack_json(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_pack_path)
    expected_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    e3_packunit = get_packunit_from_json(open_file(e3_all_pack_path))
    assert e3_packunit.event_int == expected_e3_pack.event_int
    expected_plandelta = expected_e3_pack._plandelta
    generated_e3_plandelta = e3_packunit._plandelta
    assert generated_e3_plandelta.planatoms == expected_plandelta.planatoms
    assert e3_packunit._plandelta == expected_e3_pack._plandelta
    assert e3_packunit == expected_e3_pack


def test_etl_event_plan_csvs_to_pack_json_CreatesFiles_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    credit77 = 77
    credit88 = 88
    debt_empty = ""
    a23_str = "accord23"
    plnacct_str = plan_acctunit_str()
    put_agg_tablename = create_prime_tablename(plnacct_str, "v", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    belief_mstr_dir = get_module_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = owner_event_dir(belief_mstr_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = owner_event_dir(belief_mstr_dir, a23_str, bob_inx, event7)
    e3_put_csv = f"""{event_int_str()},{face_name_str()},{belief_label_str()},{owner_name_str()},{acct_name_str()},{acct_cred_points_str()},{acct_debt_points_str()}
{event3},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
"""
    e7_put_csv = f"""{event_int_str()},{face_name_str()},{belief_label_str()},{owner_name_str()},{acct_name_str()},{acct_cred_points_str()},{acct_debt_points_str()}
{event7},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
{event7},{sue_inx},{a23_str},{bob_inx},{sue_inx},{credit88},{debt_empty}
"""
    print(f"     {a23_bob_e3_dir=}  {put_agg_csv_filename}")
    print(f"     {a23_bob_e7_dir=}  {put_agg_csv_filename}")
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    e3_all_pack_path = all_pack_path(belief_mstr_dir, a23_str, bob_inx, event3)
    e7_all_pack_path = all_pack_path(belief_mstr_dir, a23_str, bob_inx, event7)
    print(f"   {e3_all_pack_path=}")
    print(f"   {e7_all_pack_path=}")
    assert os_path_exists(e3_all_pack_path) is False
    assert os_path_exists(e7_all_pack_path) is False

    # WHEN
    etl_event_plan_csvs_to_pack_json(belief_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    # print(f"{open_file(e3_pack_path)=}")
    # print(f"{open_file(e7_pack_path)=}")
    # packs_dir = create_path(fizz_world._belief_mstr_dir, "packs")
    # atoms_dir = create_path(fizz_world._belief_mstr_dir, "atoms")
    # e3_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event3)
    # e7_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event7)
    expected_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    expected_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    plnacct_dimen = plan_acctunit_str()
    expected_e3_pack._plandelta.add_planatom(
        plnacct_dimen,
        INSERT_str(),
        jkeys={acct_name_str(): bob_inx},
        jvalues={acct_cred_points_str(): credit77, acct_debt_points_str(): None},
    )
    expected_e7_pack._plandelta.add_planatom(
        plnacct_dimen,
        INSERT_str(),
        jkeys={acct_name_str(): bob_inx},
        jvalues={acct_cred_points_str(): credit77, acct_debt_points_str(): None},
    )
    expected_e7_pack._plandelta.add_planatom(
        plnacct_dimen,
        INSERT_str(),
        jkeys={acct_name_str(): sue_inx},
        jvalues={acct_cred_points_str(): credit88, acct_debt_points_str(): None},
    )
    e3_packunit = get_packunit_from_json(open_file(e3_all_pack_path))
    e7_packunit = get_packunit_from_json(open_file(e7_all_pack_path))
    # print(f"{e7_packunit=}")
    assert e3_packunit.event_int == expected_e3_pack.event_int
    expected_plandelta = expected_e3_pack._plandelta
    generated_e3_plandelta = e3_packunit._plandelta
    assert generated_e3_plandelta.planatoms == expected_plandelta.planatoms
    assert e3_packunit._plandelta == expected_e3_pack._plandelta
    assert e3_packunit == expected_e3_pack
    e7_insert = e7_packunit._plandelta.planatoms.get("INSERT")
    expected_e7_insert = expected_e7_pack._plandelta.planatoms.get("INSERT")
    # print(e7_insert.get("plan_acctunit").keys())
    # print(expected_e7_insert.get("plan_acctunit").keys())
    e7_plnacct = e7_insert.get("plan_acctunit")
    expected_e7_plnacct = expected_e7_insert.get("plan_acctunit")
    assert e7_plnacct.keys() == expected_e7_plnacct.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_packunit._plandelta == expected_e7_pack._plandelta
    assert e7_packunit == expected_e7_pack
