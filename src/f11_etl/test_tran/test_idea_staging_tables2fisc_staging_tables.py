from src.a00_data_toolboxs.file_toolbox import create_path, save_file, open_file
from src.a00_data_toolboxs.db_toolbox import (
    db_table_exists,
    get_row_count,
    create_select_inconsistency_query,
)
from src.a02_finance_toolboxs.deal import (
    bridge_str,
    quota_str,
    deal_time_str,
    tran_time_str,
    celldepth_str,
    owner_name_str,
    fisc_title_str,
)
from src.a07_calendar_logic.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
)
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    face_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    event_int_str,
)
from src.a15_fisc_logic.fisc_config import (
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fiscunit_str,
    offi_time_str,
    amount_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    month_title_str,
    weekday_order_str,
    weekday_title_str,
)
from src.f10_idea.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_category_str,
)
from src.f10_idea.idea_db_tool import create_idea_sorted_table
from src.f11_etl.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.f11_etl.tran_sqlstrs import get_fisc_inconsistency_sqlstrs
from src.f11_etl.transformers import (
    etl_inz_face_csv_files2idea_staging_tables,
    create_fisc_tables,
    idea_staging_tables2fisc_staging_tables,
    etl_fisc_staging_tables_to_fisc_csvs,
    set_fisc_staging_error_message,
)
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_idea_staging_tables2fisc_staging_tables_Scenario0_From_br00011_IdeaFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    inz_faces_dir = get_test_etl_dir()
    sue_inz_dir = create_path(inz_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        etl_inz_face_csv_files2idea_staging_tables(cursor, inz_faces_dir)
        create_fisc_tables(cursor)
        x_fisc = FiscPrimeObjsRef()
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario1_From_br00011_IdeaTable(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00011_str = "br00011"
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        br00011_tablename = f"{br00011_str}_staging"
        create_idea_sorted_table(cursor, br00011_tablename, br00011_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00011_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()})
VALUES 
  ('{sue_inx}', {event3}, '{accord23_str}', '{bob_inx}', '{bob_inx}')
, ('{sue_inx}', {event3}, '{accord23_str}', '{yao_inx}', '{bob_inx}')
, ('{sue_inx}', {event3}, '{accord23_str}', '{yao_inx}', '{yao_inx}')
, ('{sue_inx}', {event7}, '{accord23_str}', '{yao_inx}', '{yao_inx}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario2_Idea_br00000_Table_WithEmptyAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_title_str(),
    ]
    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00000_tablename = f"{br00000_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00000_tablename, br00000_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00000_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{timeline_title_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{bridge_str()})
VALUES
  ('{sue_inx}', {event3}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ('{sue_inx}', {event3}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ('{sue_inx}', {event7}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
;
"""
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
            None,  # plan_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario3_Idea_br00000_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_title_str(),
    ]
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00000_tablename = f"{br00000_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00000_tablename, br00000_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00000_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{timeline_title_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{bridge_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_timeline_title}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
, ('{sue_inx}',{event3},'{accord23_str}','{a23_timeline_title}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
, ('{sue_inx}',{event7},'{accord23_str}','{a23_timeline_title}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_timeline_title,  # timeline_title
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            # a23_offi_time_max,  # _offi_time_max
            a23_bridge,  # bridge
            None,  # plan_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_timeline_title,  # timeline_title
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            # a23_offi_time_max,  # _offi_time_max
            a23_bridge,  # bridge
            None,  # plan_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row0=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario4_Idea_br00001_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00001_str = "br00001"
    br00001_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        deal_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    a23_owner_name = bob_inx
    a23_deal_time = 22
    a23_quota = 33

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00001_tablename = f"{br00001_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00001_tablename, br00001_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00001_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{deal_time_str()},{quota_str()}, {celldepth_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
, ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
, ('{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.deal_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.deal_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.deal_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00001_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_owner_name,
            a23_deal_time,
            a23_quota,
            None,  # celldepth
            None,  # note
        )
        expected_row1 = (
            br00001_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_owner_name,
            a23_deal_time,
            a23_quota,
            None,  # celldepth
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario5_Idea_br00002_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00002_str = "br00002"
    br00002_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        tran_time_str(),
        amount_str(),
    ]
    a23_owner_name = bob_inx
    a23_acct_name = "Yao"
    a23_tran_time = 33
    a23_amount = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00002_tablename = f"{br00002_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00002_tablename, br00002_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00002_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{tran_time_str()},{amount_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.cash_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.cash_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.cash_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00002_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_owner_name,
            a23_acct_name,
            a23_tran_time,
            a23_amount,
            None,  # note
        )
        expected_row1 = (
            br00002_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_owner_name,
            a23_acct_name,
            a23_tran_time,
            a23_amount,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario6_Idea_br00003_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00003_str = "br00003"
    br00003_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    a23_hour_title = "4pm"
    a23_cumlative_minute = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00003_tablename = f"{br00003_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00003_tablename, br00003_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00003_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{hour_title_str()},{cumlative_minute_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.hour_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.hour_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.hour_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00003_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_cumlative_minute,
            a23_hour_title,
            None,  # note
        )
        expected_row1 = (
            br00003_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_cumlative_minute,
            a23_hour_title,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario7_Idea_br00004_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00004_str = "br00004"
    br00004_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        month_title_str(),
        cumlative_day_str(),
    ]
    a23_month_title = "March"
    a23_cumlative_day = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00004_tablename = f"{br00004_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00004_tablename, br00004_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00004_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{month_title_str()},{cumlative_day_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.mont_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.mont_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.mont_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00004_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_cumlative_day,
            a23_month_title,
            None,  # note
        )
        expected_row1 = (
            br00004_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_cumlative_day,
            a23_month_title,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fisc_staging_tables_Scenario8_Idea_br00005_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00005_str = "br00005"
    br00005_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        weekday_title_str(),
        weekday_order_str(),
    ]
    a23_weekday_title = "wednesday"
    a23_weekday_order = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00005_tablename = f"{br00005_str}_staging"
        cursor = fisc_db_conn.cursor()
        create_idea_sorted_table(cursor, br00005_tablename, br00005_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00005_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{weekday_title_str()},{weekday_order_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_tables(cursor)
        assert get_row_count(cursor, x_fisc.week_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fisc_staging_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.week_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.week_stage_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00005_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fisc_title
            a23_weekday_order,
            a23_weekday_title,
            None,  # note
        )
        expected_row1 = (
            br00005_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fisc_title
            a23_weekday_order,
            a23_weekday_title,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_etl_fisc_staging_tables_to_fisc_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        fisc_mstr_dir = get_test_etl_dir()
        fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
        x_fisc = FiscPrimeObjsRef(fiscs_dir)
        fisc_cols = FiscPrimeColumnsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fisc.unit_stage_tablename} ({idea_number_str()}, {face_name_str()}, {event_int_str()}, {fisc_title_str()})
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert os_path_exists(x_fisc.unit_stage_csv_path) is False
        assert os_path_exists(x_fisc.deal_stage_csv_path) is False
        assert os_path_exists(x_fisc.cash_stage_csv_path) is False
        assert os_path_exists(x_fisc.hour_stage_csv_path) is False
        assert os_path_exists(x_fisc.mont_stage_csv_path) is False
        assert os_path_exists(x_fisc.week_stage_csv_path) is False

        # WHEN
        etl_fisc_staging_tables_to_fisc_csvs(cursor, fiscs_dir)

        # THEN
        assert os_path_exists(x_fisc.unit_stage_csv_path)
        assert os_path_exists(x_fisc.deal_stage_csv_path)
        assert os_path_exists(x_fisc.cash_stage_csv_path)
        assert os_path_exists(x_fisc.hour_stage_csv_path)
        assert os_path_exists(x_fisc.mont_stage_csv_path)
        assert os_path_exists(x_fisc.week_stage_csv_path)
        unit_stage_csv_filename = x_fisc.unit_stage_csv_filename
        generated_fiscunit_csv = open_file(fiscs_dir, unit_stage_csv_filename)
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_staging_csv_header}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord45_str},,,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscunit_csv=}")
        print(f"{expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fisc.deal_stage_csv_path)) == 94
        assert len(open_file(x_fisc.cash_stage_csv_path)) == 86
        assert len(open_file(x_fisc.hour_stage_csv_path)) == 77
        assert len(open_file(x_fisc.mont_stage_csv_path)) == 75
        assert len(open_file(x_fisc.week_stage_csv_path)) == 77


def test_etl_fisc_staging_tables_to_fisc_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        fisc_mstr_dir = get_test_etl_dir()
        fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
        x_fisc = FiscPrimeObjsRef(fiscs_dir)
        fisc_cols = FiscPrimeColumnsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fisc.unit_stage_tablename} ({idea_number_str()}, {face_name_str()}, {event_int_str()}, {fisc_title_str()})
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert os_path_exists(x_fisc.unit_stage_csv_path) is False
        assert os_path_exists(x_fisc.deal_stage_csv_path) is False
        assert os_path_exists(x_fisc.cash_stage_csv_path) is False
        assert os_path_exists(x_fisc.hour_stage_csv_path) is False
        assert os_path_exists(x_fisc.mont_stage_csv_path) is False
        assert os_path_exists(x_fisc.week_stage_csv_path) is False

        # WHEN
        etl_fisc_staging_tables_to_fisc_csvs(cursor, fiscs_dir)

        # THEN
        assert os_path_exists(x_fisc.unit_stage_csv_path)
        assert os_path_exists(x_fisc.deal_stage_csv_path)
        assert os_path_exists(x_fisc.cash_stage_csv_path)
        assert os_path_exists(x_fisc.hour_stage_csv_path)
        assert os_path_exists(x_fisc.mont_stage_csv_path)
        assert os_path_exists(x_fisc.week_stage_csv_path)
        unit_stage_csv_filename = x_fisc.unit_stage_csv_filename
        generated_fiscunit_csv = open_file(fiscs_dir, unit_stage_csv_filename)
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_staging_csv_header}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord45_str},,,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscunit_csv=}")
        print(f"{expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fisc.deal_stage_csv_path)) == 94
        assert len(open_file(x_fisc.cash_stage_csv_path)) == 95
        assert len(open_file(x_fisc.hour_stage_csv_path)) == 85
        assert len(open_file(x_fisc.mont_stage_csv_path)) == 83
        assert len(open_file(x_fisc.week_stage_csv_path)) == 85


def test_GlobalVariablesForFisc_inconsistency_queryReturns_sqlstrs():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        # if dimen_config.get(idea_category_str()) != "pidgin"
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    exclude_cols = {"idea_number", "face_name", "event_int", "error_message"}
    with sqlite3_connect(":memory:") as conn:
        create_fisc_tables(conn)

        for x_dimen, x_sqlstr in get_fisc_inconsistency_sqlstrs().items():
            x_tablename = f"{x_dimen}_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns.remove(event_int_str())
            dimen_focus_columns.remove(face_name_str())
            expected_dimen_sqlstr = create_select_inconsistency_query(
                conn, x_tablename, dimen_focus_columns, exclude_cols
            )
            assert x_sqlstr == expected_dimen_sqlstr
            print(f"{x_dimen} checked...")


def test_set_fisc_staging_error_message_Scenario0_fiscunit_WithNo_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    # a23_offi_time_max = 44
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"
    a23_plan_listen_rotations = 6
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.unit_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.unit_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',{a23_plan_listen_rotations},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',{a23_plan_listen_rotations},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, error_message FROM {x_tablename};"
        # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [(event3, None), (event7, None)]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [(event3, None), (event7, None)]


def test_set_fisc_staging_error_message_Scenario1_fiscunit_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_fund_coin = 11
    a23_penny_1 = 22
    a23_penny_2 = 99
    a23_respect_bit = 33
    # a23_offi_time_max = 44
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"
    a23_plan_listen_rotations = 900
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.unit_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.unit_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny_1},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',{a23_plan_listen_rotations},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',{a23_plan_listen_rotations},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',{a23_plan_listen_rotations},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, None),
            (event7, accord23_str, None),
            (event7, accord45_str, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_staging_error_message_Scenario2_fischour_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_4hour_title = "4pm"
    a23_5hour_title = "5pm"
    a23_cumlative_minute_1 = 44
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.hour_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.hour_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_cumlative_minute_1},'{a23_4hour_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_cumlative_minute_1},'{a23_5hour_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{a23_cumlative_minute_1},'{a23_4hour_title}',NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, None),
            (event7, accord23_str, None),
            (event7, accord45_str, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_staging_error_message_Scenario3_fischour_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_month_title_1 = "March"
    a23_month_title_2 = "Marche"
    _44_cumlative_day = 44
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.mont_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.mont_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{_44_cumlative_day},'{a23_month_title_1}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{_44_cumlative_day},'{a23_month_title_2}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{_44_cumlative_day},'{a23_month_title_2}',NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, None),
            (event7, accord23_str, None),
            (event7, accord45_str, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_staging_error_message_Scenario4_fiscweek_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    wed_str = "Wednesday"
    tue_str = "Tuesday"
    mon_str = "Monday"
    order1 = 1
    order2 = 2
    order3 = 3
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.week_stage_tablename
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.week_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{order1},'{mon_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{order2},'{tue_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{order2},'{wed_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{order1},'{mon_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{order3},'{wed_str}',NULL)
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {weekday_order_str()}, error_message FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, order1, None),
            (event7, accord23_str, order2, None),
            (event7, accord23_str, order2, None),
            (event7, accord45_str, order1, None),
            (event7, accord45_str, order3, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, order1, None),
            (event7, accord23_str, order2, x_error_message),
            (event7, accord23_str, order2, x_error_message),
            (event7, accord45_str, order1, None),
            (event7, accord45_str, order3, None),
        ]


def test_set_fisc_staging_error_message_Scenario5_fiscdeal_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_owner_name = bob_inx
    t1_deal_time = 33
    t1_quota_1 = 200
    t1_quota_2 = 300
    t2_deal_time = 55
    t2_quota = 400
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.deal_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.deal_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_2},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {deal_time_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, t1_deal_time, None),
            (event7, accord23_str, t1_deal_time, None),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]


def test_set_fisc_staging_error_message_Scenario6_fisccash_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    t1_tran_time = 33
    t2_tran_time = 55
    t1_amount_1 = 200
    t1_amount_2 = 300
    t2_amount = 400
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        x_tablename = x_objs.cash_stage_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_staging_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.cash_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_2},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{yao_inx}','{bob_inx}',{t2_tran_time},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{yao_inx}','{bob_inx}',{t2_tran_time},{t2_amount},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {tran_time_str()}, error_message FROM {x_tablename};"
        # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        # print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        # print(f"{rows=}")
        assert rows == [
            (event3, accord23_str, t1_tran_time, None),
            (event7, accord23_str, t1_tran_time, None),
            (event7, accord23_str, t2_tran_time, None),
            (event7, accord45_str, t1_tran_time, None),
            (event7, accord45_str, t2_tran_time, None),
        ]

        # WHEN
        set_fisc_staging_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent fisc data"
        assert rows == [
            (event3, accord23_str, t1_tran_time, x_error_message),
            (event7, accord23_str, t1_tran_time, x_error_message),
            (event7, accord23_str, t2_tran_time, None),
            (event7, accord45_str, t1_tran_time, None),
            (event7, accord45_str, t2_tran_time, None),
        ]
