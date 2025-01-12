from src.f00_instrument.file import create_path, save_file
from src.f00_instrument.db_toolbox import db_table_exists
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    cmty_title_str,
    owner_name_str,
)
from src.f07_cmty.cmty_config import (
    get_cmty_config_args,
    cmtyunit_str,
    cmty_deal_episode_str,
    cmty_cashbook_str,
    cmty_timeline_hour_str,
    cmty_timeline_month_str,
    cmty_timeline_weekday_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_sorting_columns
from src.f10_etl.transformers import (
    etl_aft_face_csv_files_to_fiscal_db,
    create_cmty_tables,
    populate_cmty_staging_tables,
    populate_cmty_agg_tables,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect
from copy import copy as copy_copy


def test_etl_aft_face_csv_files_to_fiscal_db_DBChanges(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    aft_faces_dir = get_test_etl_dir()
    sue_aft_dir = create_path(aft_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_staging_tablename = f"{br00011_str}_staging"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{cmty_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename) is False

        # ESTABLISH
        etl_aft_face_csv_files_to_fiscal_db(fiscal_db_conn, aft_faces_dir)

        # THEN
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename)
        print(f"{type(fiscal_db_conn)=}")
        assert fiscal_db_conn != None
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({br00011_staging_tablename})")
        br00011_db_columns = cursor.fetchall()
        br00011_expected_columns = [
            (0, face_name_str(), "TEXT", 0, None, 0),
            (1, event_int_str(), "INTEGER", 0, None, 0),
            (2, cmty_title_str(), "TEXT", 0, None, 0),
            (3, owner_name_str(), "TEXT", 0, None, 0),
            (4, acct_name_str(), "TEXT", 0, None, 0),
        ]
        print(f"      {br00011_db_columns=}")
        print(f"{br00011_expected_columns=}")
        assert br00011_db_columns == br00011_expected_columns
        cursor.execute(f"SELECT * FROM {br00011_staging_tablename}")
        br00011_db_rows = cursor.fetchall()
        expected_data = [
            (sue_inx, event3, accord23_str, bob_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, yao_inx),
            (sue_inx, event7, accord23_str, yao_inx, yao_inx),
        ]
        assert br00011_db_rows == expected_data


def test_create_cmty_tables_CreatesCmtyStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    agg_str = "_agg"
    cmtyunit_agg_tablename = f"{cmtyunit_str()}{agg_str}"
    cmtydeal_agg_tablename = f"{cmty_deal_episode_str()}{agg_str}"
    cmtycash_agg_tablename = f"{cmty_cashbook_str()}{agg_str}"
    cmtyhour_agg_tablename = f"{cmty_timeline_hour_str()}{agg_str}"
    cmtymont_agg_tablename = f"{cmty_timeline_month_str()}{agg_str}"
    cmtyweek_agg_tablename = f"{cmty_timeline_weekday_str()}{agg_str}"
    staging_str = "_staging"
    cmtyunit_stage_tablename = f"{cmtyunit_str()}{staging_str}"
    cmtydeal_stage_tablename = f"{cmty_deal_episode_str()}{staging_str}"
    cmtycash_stage_tablename = f"{cmty_cashbook_str()}{staging_str}"
    cmtyhour_stage_tablename = f"{cmty_timeline_hour_str()}{staging_str}"
    cmtymont_stage_tablename = f"{cmty_timeline_month_str()}{staging_str}"
    cmtyweek_stage_tablename = f"{cmty_timeline_weekday_str()}{staging_str}"
    cmtyunit_args = get_cmty_config_args(cmtyunit_str()).keys()
    cmtydeal_args = get_cmty_config_args(cmty_deal_episode_str()).keys()
    cmtycash_args = get_cmty_config_args(cmty_cashbook_str()).keys()
    cmtyhour_args = get_cmty_config_args(cmty_timeline_hour_str()).keys()
    cmtymont_args = get_cmty_config_args(cmty_timeline_month_str()).keys()
    cmtyweek_args = get_cmty_config_args(cmty_timeline_weekday_str()).keys()
    staging_columns = ["idea_number", "face_name", "event_int"]
    cmtyunit_agg_columns = get_sorting_columns(cmtyunit_args)
    cmtydeal_agg_columns = get_sorting_columns(cmtydeal_args)
    cmtycash_agg_columns = get_sorting_columns(cmtycash_args)
    cmtyhour_agg_columns = get_sorting_columns(cmtyhour_args)
    cmtymont_agg_columns = get_sorting_columns(cmtymont_args)
    cmtyweek_agg_columns = get_sorting_columns(cmtyweek_args)
    cmtyunit_agg_pragma = get_pragma_table_fetchall(cmtyunit_agg_columns)
    cmtydeal_agg_pragma = get_pragma_table_fetchall(cmtydeal_agg_columns)
    cmtycash_agg_pragma = get_pragma_table_fetchall(cmtycash_agg_columns)
    cmtyhour_agg_pragma = get_pragma_table_fetchall(cmtyhour_agg_columns)
    cmtymont_agg_pragma = get_pragma_table_fetchall(cmtymont_agg_columns)
    cmtyweek_agg_pragma = get_pragma_table_fetchall(cmtyweek_agg_columns)

    cmtyunit_stage_columns = copy_copy(staging_columns)
    cmtydeal_stage_columns = copy_copy(staging_columns)
    cmtycash_stage_columns = copy_copy(staging_columns)
    cmtyhour_stage_columns = copy_copy(staging_columns)
    cmtymont_stage_columns = copy_copy(staging_columns)
    cmtyweek_stage_columns = copy_copy(staging_columns)
    cmtyunit_stage_columns.extend(cmtyunit_agg_columns)
    cmtydeal_stage_columns.extend(cmtydeal_agg_columns)
    cmtycash_stage_columns.extend(cmtycash_agg_columns)
    cmtyhour_stage_columns.extend(cmtyhour_agg_columns)
    cmtymont_stage_columns.extend(cmtymont_agg_columns)
    cmtyweek_stage_columns.extend(cmtyweek_agg_columns)
    cmtyunit_stage_pragma = get_pragma_table_fetchall(cmtyunit_stage_columns)
    cmtydeal_stage_pragma = get_pragma_table_fetchall(cmtydeal_stage_columns)
    cmtycash_stage_pragma = get_pragma_table_fetchall(cmtycash_stage_columns)
    cmtyhour_stage_pragma = get_pragma_table_fetchall(cmtyhour_stage_columns)
    cmtymont_stage_pragma = get_pragma_table_fetchall(cmtymont_stage_columns)
    cmtyweek_stage_pragma = get_pragma_table_fetchall(cmtyweek_stage_columns)

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        assert db_table_exists(fiscal_db_conn, cmtyunit_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtydeal_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtycash_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtyhour_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtymont_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtyweek_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtyunit_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtydeal_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtycash_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtyhour_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtymont_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, cmtyweek_stage_tablename) is False

        # WHEN
        create_cmty_tables(fiscal_db_conn)

        # THEN
        assert db_table_exists(fiscal_db_conn, cmtyunit_agg_tablename)
        assert db_table_exists(fiscal_db_conn, cmtydeal_agg_tablename)
        assert db_table_exists(fiscal_db_conn, cmtycash_agg_tablename)
        assert db_table_exists(fiscal_db_conn, cmtyhour_agg_tablename)
        assert db_table_exists(fiscal_db_conn, cmtymont_agg_tablename)
        assert db_table_exists(fiscal_db_conn, cmtyweek_agg_tablename)

        assert db_table_exists(fiscal_db_conn, cmtyunit_stage_tablename)
        assert db_table_exists(fiscal_db_conn, cmtydeal_stage_tablename)
        assert db_table_exists(fiscal_db_conn, cmtycash_stage_tablename)
        assert db_table_exists(fiscal_db_conn, cmtyhour_stage_tablename)
        assert db_table_exists(fiscal_db_conn, cmtymont_stage_tablename)
        assert db_table_exists(fiscal_db_conn, cmtyweek_stage_tablename)
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({cmtyunit_agg_tablename})")
        assert cmtyunit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtydeal_agg_tablename})")
        assert cmtydeal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtycash_agg_tablename})")
        assert cmtycash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtyhour_agg_tablename})")
        assert cmtyhour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtymont_agg_tablename})")
        assert cmtymont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtyweek_agg_tablename})")
        assert cmtyweek_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({cmtyunit_stage_tablename})")
        assert cmtyunit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtydeal_stage_tablename})")
        assert cmtydeal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtycash_stage_tablename})")
        assert cmtycash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtyhour_stage_tablename})")
        assert cmtyhour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtymont_stage_tablename})")
        assert cmtymont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({cmtyweek_stage_tablename})")
        assert cmtyweek_stage_pragma == cursor.fetchall()


def test_populate_cmty_staging_tables_PopulatesCmtyStagingTables(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    aft_faces_dir = get_test_etl_dir()
    sue_aft_dir = create_path(aft_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{cmty_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)

    cmtyunit_tablename = f"{cmtyunit_str()}_staging"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        etl_aft_face_csv_files_to_fiscal_db(fiscal_db_conn, aft_faces_dir)
        create_cmty_tables(fiscal_db_conn)
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {cmtyunit_tablename}")
        cmtyunit_db_rows = cursor.fetchall()
        assert cmtyunit_db_rows == []

        # WHEN
        populate_cmty_staging_tables(fiscal_db_conn)

        # THEN
        cursor.execute(f"SELECT * FROM {cmtyunit_tablename}")
        cmtyunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # cmty_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row2 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # cmty_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        assert cmtyunit_db_rows == [expected_row1, expected_row2]


def test_populate_cmty_agg_tables_PopulatesCmtyAggTables(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    cmtyunit_stage_tablename = f"{cmtyunit_str()}_staging"
    cmtyunit_agg_tablename = f"{cmtyunit_str()}_agg"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_cmty_tables(fiscal_db_conn)

        cursor = fiscal_db_conn.cursor()
        insert_staging_sqlstr = f"""
INSERT INTO cmtyunit_staging (idea_number, face_name, event_int, cmty_title)
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        cursor.execute(f"SELECT * FROM {cmtyunit_stage_tablename};")
        cmtyunit_stage_rows = cursor.fetchall()
        assert len(cmtyunit_stage_rows) == 4
        cursor.execute(f"SELECT * FROM {cmtyunit_agg_tablename};")
        cmtyunit_agg_rows = cursor.fetchall()
        assert cmtyunit_agg_rows == []

        # WHEN
        populate_cmty_agg_tables(fiscal_db_conn)

        # THEN
        cursor.execute(f"SELECT * FROM {cmtyunit_agg_tablename};")
        cmtyunit_agg_rows = cursor.fetchall()
        expected_row1 = (
            accord23_str,  # cmty_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row2 = (
            accord45_str,  # cmty_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        assert cmtyunit_agg_rows == [expected_row1, expected_row2]
