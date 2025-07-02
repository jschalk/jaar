from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file, set_dir
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import owner_plan_awardlink_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.hub_path import create_belief_json_path, create_gut_path
from src.a15_belief_logic.belief import beliefunit_shop
from src.a16_pidgin_logic.test._util.a16_str import (
    inx_name_str,
    otx_name_str,
    pidgin_name_str,
)
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_ownerunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import (  # add_pidginunits_to_stance_csv_strs,
    get_sheet_names,
)
from src.a18_etl_toolbox.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.tran_path import create_stance0001_path
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    create_update_voice_raw_empty_inx_col_sqlstr,
    create_update_voice_raw_existing_inx_col_sqlstr,
)


def test_collect_stance_csv_strs_ReturnsObj_Scenario0_NoBeliefUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(belief_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleBeliefUnit_NoOwnerUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(belief_json_path, None, a23_belief.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(belief_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_beliefunit_to_stance_csv_strs(a23_belief, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_OwnerUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(belief_json_path, None, a23_belief.get_json())
    # create owner gut file
    bob_gut = ownerunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit("Yao", 44, 55)
    a23_bob_gut_path = create_gut_path(belief_mstr_dir, a23_str, bob_str)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(belief_mstr_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_beliefunit_to_stance_csv_strs(a23_belief, expected_stance_csv_strs, ",")
    add_ownerunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


# # TODO #834
# # def test_collect_stance_csv_strs_ReturnsObj_Scenario3_gut_OwnerUnits(
# #     env_dir_setup_cleanup,
# # ):
# #     # ESTABLISH
# #     belief_mstr_dir = get_module_temp_dir()
# #     bob_str = "Bob"
# #     a23_str = "amy23"
# #     a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
# #     belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
# #     save_file(belief_json_path, None, a23_belief.get_json())
# #     # create owner gut file
# #     bob_gut = ownerunit_shop(bob_str, a23_str)
# #     bob_gut.add_acctunit("Yao", 44, 55)
# #     a23_bob_gut_path = create_gut_path(belief_mstr_dir, a23_str, bob_str)
# #     save_file(a23_bob_gut_path, None, bob_gut.get_json())

# #     # WHEN
# #     gen_stance_csv_strs = collect_stance_csv_strs(belief_mstr_dir)

# #     # THEN
# #     expected_stance_csv_strs = create_init_stance_idea_csv_strs()
# #     add_beliefunit_to_stance_csv_strs(a23_belief, expected_stance_csv_strs, ",")
# #     add_ownerunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
# #     assert gen_stance_csv_strs == expected_stance_csv_strs


# def test_add_pidginunits_to_stance_csv_strs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
#     # ESTABLISH database with pidgin data
#     bob_otx = "Bob"
#     bob_inx = "Bobby"
#     sue_otx = "Sue"
#     sue_inx = "Suzy"
#     yao_otx = "Yao"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     temp_dir = get_module_temp_dir()
#     db_path = create_path(temp_dir, "example3.db")
#     print(f"{db_path=}")
#     set_dir(temp_dir)

#     with sqlite3_connect(db_path) as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidname_dimen = pidgin_name_str()
#         pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
#         print(f"{pidname_s_vld_tablename=}")
#         insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
#         ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
#         VALUES
#           ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
#         , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
#         ;
#         """
#         cursor.execute(insert_pidname_sqlstr)

#         pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
#         insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename}
#         ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
#         VALUES
#           ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
#         , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
#         ;
#         """
#         cursor.execute(insert_pidname_sqlstr)
#     csv_strs = create_init_stance_idea_csv_strs()
#     br00042_str = "br00042"
#     br00043_str = "br00043"
#     br00044_str = "br00044"
#     br00045_str = "br00045"
#     print(f"{csv_strs.get(br00042_str)=}")
#     print(f"{csv_strs.get(br00043_str)=}")
#     print(f"{csv_strs.get(br00044_str)=}")
#     print(f"{csv_strs.get(br00045_str)=}")
#     print(f"{csv_strs.keys()=}")

#     # WHEN
#     csv_strs = add_pidginunits_to_stance_csv_strs(csv_strs, db_path)

#     # THEN csv_strs have added rows
#     expected_stance_csv_strs = create_init_stance_idea_csv_strs()

#     assert 1 == 2


def test_create_stance0001_file_CreatesFile_Scenario0_NoBeliefUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    belief_mstr_dir = create_path(get_module_temp_dir(), "belief_mstr")
    output_dir = create_path(get_module_temp_dir(), "output")
    stance0001_path = create_stance0001_path(output_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(belief_mstr_dir, output_dir, sue_str)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())
