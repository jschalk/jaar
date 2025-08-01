from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file, set_dir
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import believer_plan_awardlink_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.a12_path import create_belief_json_path, create_gut_path
from src.a15_belief_logic.belief_main import beliefunit_shop
from src.a16_pidgin_logic.test._util.a16_str import (
    inx_knot_str,
    inx_name_str,
    otx_knot_str,
    otx_name_str,
    pidgin_name_str,
    unknown_str_str,
)
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_believerunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import get_sheet_names
from src.a18_etl_toolbox.a18_path import (
    create_belief_mstr_path,
    create_stance0001_path,
    create_world_db_path,
)
from src.a18_etl_toolbox.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
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
    world_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleBeliefUnit_NoBelieverUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    world_dir = get_module_temp_dir()
    belief_mstr_dir = create_belief_mstr_path(world_dir)
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(belief_json_path, None, a23_belief.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_beliefunit_to_stance_csv_strs(a23_belief, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_BelieverUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    world_dir = get_module_temp_dir()
    belief_mstr_dir = create_belief_mstr_path(world_dir)
    bob_str = "Bob"
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(belief_json_path, None, a23_belief.get_json())
    # create believer gut file
    bob_gut = believerunit_shop(bob_str, a23_str)
    bob_gut.add_partnerunit("Yao", 44, 55)
    a23_bob_gut_path = create_gut_path(belief_mstr_dir, a23_str, bob_str)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_beliefunit_to_stance_csv_strs(a23_belief, expected_stance_csv_strs, ",")
    add_believerunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_PidginRowsInDB(
    env_dir_setup_cleanup,
):
    # ESTABLISH database with pidgin data
    yao_str = "Yao"
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    event1 = 1
    event7 = 7
    slash_str = "/"
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = get_module_temp_dir()
    output_dir = create_path(get_module_temp_dir(), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename}
        ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
        VALUES
          ('{sue_otx}', '{slash_str}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{slash_str}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_pidcore_sqlstr)
    db_conn.close()

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    assert gen_stance_csv_strs
    generated_stance_csv_keys = set(gen_stance_csv_strs.keys())
    print(f"{generated_stance_csv_keys=}")
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert generated_stance_csv_keys == set(stance_csv_strs.keys())
    br00042_str = "br00042"
    br00043_str = "br00043"
    br00044_str = "br00044"
    br00045_str = "br00045"
    br00042_csv = gen_stance_csv_strs.get(br00042_str)
    br00043_csv = gen_stance_csv_strs.get(br00043_str)
    br00044_csv = gen_stance_csv_strs.get(br00044_str)
    br00045_csv = gen_stance_csv_strs.get(br00045_str)

    expected_br00042_csv = (
        "event_int,face_name,otx_title,inx_title,otx_knot,inx_knot,unknown_str\n"
    )
    expected_br00043_csv = f"""event_int,face_name,otx_name,inx_name,otx_knot,inx_knot,unknown_str
,{bob_otx},{bob_otx},{bob_inx},{slash_str},{colon_str},{bob_unknown_str}
,{sue_otx},{sue_otx},{sue_inx},{slash_str},{colon_str},{sue_unknown_str}
"""
    expected_br00044_csv = (
        "event_int,face_name,otx_label,inx_label,otx_knot,inx_knot,unknown_str\n"
    )
    expected_br00045_csv = (
        "event_int,face_name,otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n"
    )
    assert br00042_csv == expected_br00042_csv
    assert br00043_csv == expected_br00043_csv
    assert br00044_csv == expected_br00044_csv
    assert br00045_csv == expected_br00045_csv


def test_create_stance0001_file_CreatesFile_Scenario0_NoBeliefUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    world_dir = get_module_temp_dir()
    output_dir = create_path(world_dir, "output")
    stance0001_path = create_stance0001_path(output_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(world_dir, output_dir, sue_str)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())


def test_create_stance0001_file_CreatesFile_Scenario1_PidginRowsInDB(
    env_dir_setup_cleanup,
):
    # ESTABLISH database with pidgin data
    yao_str = "Yao"
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    event1 = 1
    event7 = 7
    slash_str = "/"
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = get_module_temp_dir()
    output_dir = create_path(get_module_temp_dir(), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename}
        ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
        VALUES
          ('{sue_otx}', '{slash_str}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{slash_str}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_pidcore_sqlstr)
    db_conn.close()

    stance0001_path = create_stance0001_path(output_dir)
    assert os_path_exists(stance0001_path) is False

    # WHEN
    create_stance0001_file(world_dir, output_dir, yao_str, False)

    # THEN
    assert os_path_exists(stance0001_path)
    bob_stance0001_sheetnames = get_sheet_names(stance0001_path)
    print(f"{bob_stance0001_sheetnames=}")
    stance_csv_strs = create_init_stance_idea_csv_strs()
    assert set(bob_stance0001_sheetnames) == set(stance_csv_strs.keys())
    br00042_str = "br00042"
    br00043_str = "br00043"
    br00044_str = "br00044"
    br00045_str = "br00045"
    br00042_df = pandas_read_excel(stance0001_path, br00042_str)
    br00043_df = pandas_read_excel(stance0001_path, br00043_str)
    br00044_df = pandas_read_excel(stance0001_path, br00044_str)
    br00045_df = pandas_read_excel(stance0001_path, br00045_str)
    assert len(br00042_df) == 0
    assert len(br00043_df) == 2
    assert len(br00044_df) == 0
    assert len(br00045_df) == 0
