from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import open_file, save_file
from src.ch10_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.ch12_hub_toolbox.ch12_path import (
    create_belief_event_dir_path as belief_event_dir,
    create_event_all_pack_path as all_pack_path,
)
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    Ch01Keywords as wx,
    Ch04Keywords as wx,
    belief_voiceunit_str,
    beliefunit_str,
    event_int_str,
    face_name_str,
    moment_label_str,
)
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch18_etl_toolbox.transformers import etl_event_belief_csvs_to_pack_json


def test_etl_event_belief_csvs_to_pack_json_CreatesFiles_Scenario0_IgnoresCSV_beliefunit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    a23_str = "amy23"
    put_agg_tablename = create_prime_tablename(beliefunit_str(), "h", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = get_chapter_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = belief_event_dir(moment_mstr_dir, a23_str, bob_inx, event3)
    e3_put_csv = f"""{event_int_str()},{face_name_str()},moment_label,belief_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_iota,penny,respect_bit
{event3},{sue_inx},{a23_str},{bob_inx},,,,,,,,
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    e3_all_pack_path = all_pack_path(moment_mstr_dir, a23_str, bob_inx, event3)
    assert os_path_exists(e3_all_pack_path) is False

    # WHEN
    etl_event_belief_csvs_to_pack_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_pack_path)
    expected_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    e3_packunit = get_packunit_from_json(open_file(e3_all_pack_path))
    assert e3_packunit.event_int == expected_e3_pack.event_int
    expected_beliefdelta = expected_e3_pack._beliefdelta
    generated_e3_beliefdelta = e3_packunit._beliefdelta
    assert generated_e3_beliefdelta.beliefatoms == expected_beliefdelta.beliefatoms
    assert e3_packunit._beliefdelta == expected_e3_pack._beliefdelta
    assert e3_packunit == expected_e3_pack


def test_etl_event_belief_csvs_to_pack_json_CreatesFiles_Scenario1(
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
    a23_str = "amy23"
    blrpern_str = belief_voiceunit_str()
    put_agg_tablename = create_prime_tablename(blrpern_str, "h", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = get_chapter_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, event7)
    a23_bob_e3_dir = belief_event_dir(moment_mstr_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = belief_event_dir(moment_mstr_dir, a23_str, bob_inx, event7)
    e3_put_csv = f"""{event_int_str()},{face_name_str()},{moment_label_str()},{wx.belief_name},{wx.voice_name},{wx.voice_cred_points},{wx.voice_debt_points}
{event3},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
"""
    e7_put_csv = f"""{event_int_str()},{face_name_str()},{moment_label_str()},{wx.belief_name},{wx.voice_name},{wx.voice_cred_points},{wx.voice_debt_points}
{event7},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
{event7},{sue_inx},{a23_str},{bob_inx},{sue_inx},{credit88},{debt_empty}
"""
    print(f"     {a23_bob_e3_dir=}  {put_agg_csv_filename}")
    print(f"     {a23_bob_e7_dir=}  {put_agg_csv_filename}")
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    e3_all_pack_path = all_pack_path(moment_mstr_dir, a23_str, bob_inx, event3)
    e7_all_pack_path = all_pack_path(moment_mstr_dir, a23_str, bob_inx, event7)
    print(f"   {e3_all_pack_path=}")
    print(f"   {e7_all_pack_path=}")
    assert os_path_exists(e3_all_pack_path) is False
    assert os_path_exists(e7_all_pack_path) is False

    # WHEN
    etl_event_belief_csvs_to_pack_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    # print(f"{open_file(e3_pack_path)=}")
    # print(f"{open_file(e7_pack_path)=}")
    # packs_dir = create_path(fay_world._moment_mstr_dir, "packs")
    # atoms_dir = create_path(fay_world._moment_mstr_dir, "atoms")
    # e3_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event3)
    # e7_pack = packunit_shop(bob_inx, sue_inx, a23_str, packs_dir, atoms_dir, event7)
    expected_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    expected_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    blrpern_dimen = belief_voiceunit_str()
    expected_e3_pack._beliefdelta.add_beliefatom(
        blrpern_dimen,
        wx.INSERT,
        jkeys={wx.voice_name: bob_inx},
        jvalues={wx.voice_cred_points: credit77, wx.voice_debt_points: None},
    )
    expected_e7_pack._beliefdelta.add_beliefatom(
        blrpern_dimen,
        wx.INSERT,
        jkeys={wx.voice_name: bob_inx},
        jvalues={wx.voice_cred_points: credit77, wx.voice_debt_points: None},
    )
    expected_e7_pack._beliefdelta.add_beliefatom(
        blrpern_dimen,
        wx.INSERT,
        jkeys={wx.voice_name: sue_inx},
        jvalues={wx.voice_cred_points: credit88, wx.voice_debt_points: None},
    )
    e3_packunit = get_packunit_from_json(open_file(e3_all_pack_path))
    e7_packunit = get_packunit_from_json(open_file(e7_all_pack_path))
    # print(f"{e7_packunit=}")
    assert e3_packunit.event_int == expected_e3_pack.event_int
    expected_beliefdelta = expected_e3_pack._beliefdelta
    generated_e3_beliefdelta = e3_packunit._beliefdelta
    assert generated_e3_beliefdelta.beliefatoms == expected_beliefdelta.beliefatoms
    assert e3_packunit._beliefdelta == expected_e3_pack._beliefdelta
    assert e3_packunit == expected_e3_pack
    e7_insert = e7_packunit._beliefdelta.beliefatoms.get("INSERT")
    expected_e7_insert = expected_e7_pack._beliefdelta.beliefatoms.get("INSERT")
    # print(e7_insert.get("belief_voiceunit").keys())
    # print(expected_e7_insert.get("belief_voiceunit").keys())
    e7_blrpern = e7_insert.get("belief_voiceunit")
    expected_e7_blrpern = expected_e7_insert.get("belief_voiceunit")
    assert e7_blrpern.keys() == expected_e7_blrpern.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_packunit._beliefdelta == expected_e7_pack._beliefdelta
    assert e7_packunit == expected_e7_pack
