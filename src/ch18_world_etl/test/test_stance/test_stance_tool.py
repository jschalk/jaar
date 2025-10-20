from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.file_toolbox import create_path, save_json, set_dir
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch10_lesson._ref.ch10_path import create_gut_path, create_moment_json_path
from src.ch15_moment.moment_main import momentunit_shop
from src.ch17_idea.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_momentunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.ch17_idea.idea_db_tool import get_sheet_names
from src.ch18_world_etl._ref.ch18_path import (
    create_moment_mstr_path,
    create_stance0001_path,
    create_world_db_path,
)
from src.ch18_world_etl.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from src.ref.keywords import Ch18Keywords as kw


def test_collect_stance_csv_strs_ReturnsObj_Scenario0_NoMomentUnits(
    temp_dir_setup,
):
    # ESTABLISH
    world_dir = get_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario1_SingleMomentUnit_NoBeliefUnits(
    temp_dir_setup,
):
    # ESTABLISH
    world_dir = get_temp_dir()
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_json(moment_json_path, None, a23_moment.to_dict())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_momentunit_to_stance_csv_strs(a23_moment, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_gut_BeliefUnits(
    temp_dir_setup,
):
    # ESTABLISH
    world_dir = get_temp_dir()
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    bob_str = "Bob"
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_json(moment_json_path, None, a23_moment.to_dict())
    # create belief gut file
    bob_gut = beliefunit_shop(bob_str, a23_str)
    bob_gut.add_voiceunit("Yao", 44, 55)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_str, bob_str)
    save_json(a23_bob_gut_path, None, bob_gut.to_dict())

    # WHEN
    gen_stance_csv_strs = collect_stance_csv_strs(world_dir)

    # THEN
    expected_stance_csv_strs = create_init_stance_idea_csv_strs()
    add_momentunit_to_stance_csv_strs(a23_moment, expected_stance_csv_strs, ",")
    add_beliefunit_to_stance_csv_strs(bob_gut, expected_stance_csv_strs, ",")
    assert gen_stance_csv_strs == expected_stance_csv_strs


def test_collect_stance_csv_strs_ReturnsObj_Scenario2_TranslateRowsInDB(
    temp_dir_setup,
):
    # ESTABLISH database with translate data
    yao_str = "Yao"
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    spark1 = 1
    spark7 = 7
    slash_str = "/"
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = get_temp_dir()
    output_dir = create_path(get_temp_dir(), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
        VALUES
          ('{sue_otx}', '{slash_str}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{slash_str}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)
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
        "spark_num,face_name,otx_title,inx_title,otx_knot,inx_knot,unknown_str\n"
    )
    expected_br00043_csv = f"""spark_num,face_name,otx_name,inx_name,otx_knot,inx_knot,unknown_str
,{bob_otx},{bob_otx},{bob_inx},{slash_str},{colon_str},{bob_unknown_str}
,{sue_otx},{sue_otx},{sue_inx},{slash_str},{colon_str},{sue_unknown_str}
"""
    expected_br00044_csv = (
        "spark_num,face_name,otx_label,inx_label,otx_knot,inx_knot,unknown_str\n"
    )
    expected_br00045_csv = (
        "spark_num,face_name,otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n"
    )
    assert br00042_csv == expected_br00042_csv
    assert br00043_csv == expected_br00043_csv
    assert br00044_csv == expected_br00044_csv
    assert br00045_csv == expected_br00045_csv


def test_create_stance0001_file_CreatesFile_Scenario0_NoMomentUnits(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    world_dir = get_temp_dir()
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


def test_create_stance0001_file_CreatesFile_Scenario1_TranslateRowsInDB(
    temp_dir_setup,
):
    # ESTABLISH database with translate data
    yao_str = "Yao"
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    spark1 = 1
    spark7 = 7
    slash_str = "/"
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = get_temp_dir()
    output_dir = create_path(get_temp_dir(), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
        VALUES
          ('{sue_otx}', '{slash_str}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{slash_str}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)
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
