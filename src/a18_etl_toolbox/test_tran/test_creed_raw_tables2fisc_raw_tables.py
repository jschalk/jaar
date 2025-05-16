from src.a00_data_toolbox.file_toolbox import create_path, save_file, open_file
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    create_select_inconsistency_query,
)
from src.a02_finance_logic._utils.strs_a02 import (
    bridge_str,
    quota_str,
    deal_time_str,
    tran_time_str,
    celldepth_str,
    owner_name_str,
    fisc_word_str,
)
from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    face_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    event_int_str,
)
from src.a07_calendar_logic._utils.str_a07 import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_word_str,
)
from src.a15_fisc_logic._utils.str_a15 import (
    amount_str,
    hour_word_str,
    cumlative_minute_str,
    cumlative_day_str,
    month_word_str,
    weekday_order_str,
    weekday_word_str,
)
from src.a17_creed_logic._utils.str_a17 import creed_category_str, creed_number_str
from src.a17_creed_logic.creed_config import get_creed_config_dict
from src.a17_creed_logic.creed_db_tool import create_creed_sorted_table
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.a18_etl_toolbox.tran_sqlstrs import get_fisc_inconsistency_sqlstrs
from src.a18_etl_toolbox.transformers import (
    etl_inz_face_csv_files2creed_raw_tables,
    create_fisc_prime_tables,
    creed_raw_tables2fisc_raw_tables,
    etl_fisc_raw_tables_to_fisc_csvs,
    set_fisc_raw_error_message,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_creed_raw_tables2fisc_raw_tables_Scenario0_From_br00011_CreedFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    inz_faces_dir = get_module_temp_dir()
    sue_inz_dir = create_path(inz_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()}
{event3},{sue_inx},{accord23_str},{bob_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{yao_inx}
{event7},{sue_inx},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        etl_inz_face_csv_files2creed_raw_tables(cursor, inz_faces_dir)
        create_fisc_prime_tables(cursor)
        x_fisc = FiscPrimeObjsRef()
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # creed_number
            event3,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # creed_number
            event7,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario1_From_br00011_CreedTable(
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
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        br00011_tablename = f"{br00011_str}_raw"
        create_creed_sorted_table(cursor, br00011_tablename, br00011_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00011_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()})
VALUES 
  ({event3}, '{sue_inx}', '{accord23_str}', '{bob_inx}', '{bob_inx}')
, ({event3}, '{sue_inx}', '{accord23_str}', '{yao_inx}', '{bob_inx}')
, ({event3}, '{sue_inx}', '{accord23_str}', '{yao_inx}', '{yao_inx}')
, ({event7}, '{sue_inx}', '{accord23_str}', '{yao_inx}', '{yao_inx}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # creed_number
            event3,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # creed_number
            event7,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario2_Creed_br00000_Table_WithEmptyAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_word_str(),
    ]
    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00000_tablename = f"{br00000_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00000_tablename, br00000_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00000_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{timeline_word_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{bridge_str()})
VALUES
  ({event3}, '{sue_inx}', '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ({event3}, '{sue_inx}', '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ({event7}, '{sue_inx}', '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
;
"""
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # creed_number
            event7,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_word
            None,  # job_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario3_Creed_br00000_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_word_str(),
    ]
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_word = "accord23_timeline"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00000_tablename = f"{br00000_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00000_tablename, br00000_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00000_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{timeline_word_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{bridge_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_timeline_word}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
, ({event3},'{sue_inx}','{accord23_str}','{a23_timeline_word}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
, ({event7},'{sue_inx}','{accord23_str}','{a23_timeline_word}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}')
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_timeline_word,  # timeline_word
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            # a23_offi_time_max,  # _offi_time_max
            a23_bridge,  # bridge
            None,  # job_listen_rotations
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # creed_number
            event7,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
            a23_timeline_word,  # timeline_word
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            # a23_offi_time_max,  # _offi_time_max
            a23_bridge,  # bridge
            None,  # job_listen_rotations
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"      {expected_row0=}")
        print(f"      {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario4_Creed_br00001_Table_WithAttrs(
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
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        owner_name_str(),
        deal_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    a23_owner_name = bob_inx
    a23_deal_time = 22
    a23_quota = 33

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00001_tablename = f"{br00001_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00001_tablename, br00001_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00001_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{deal_time_str()},{quota_str()}, {celldepth_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
, ({event3},'{sue_inx}','{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
, ({event7},'{sue_inx}','{accord23_str}','{a23_owner_name}',{a23_deal_time},{a23_quota}, NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.deal_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.deal_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.deal_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00001_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_owner_name,
            a23_deal_time,
            a23_quota,
            None,  # celldepth
            None,  # note
        )
        expected_row1 = (
            br00001_str,  # creed_number
            event7,  # event_int
            sue_inx,  # face_name
            accord23_str,  # fisc_word
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


def test_creed_raw_tables2fisc_raw_tables_Scenario5_Creed_br00002_Table_WithAttrs(
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
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
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
        br00002_tablename = f"{br00002_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00002_tablename, br00002_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00002_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()},{tran_time_str()},{amount_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
, ({event3},'{sue_inx}','{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
, ({event7},'{sue_inx}','{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_tran_time},{a23_amount})
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.cash_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.cash_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.cash_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00002_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_owner_name,
            a23_acct_name,
            a23_tran_time,
            a23_amount,
            None,  # note
        )
        expected_row1 = (
            br00002_str,  # creed_number
            event7,
            sue_inx,
            accord23_str,  # fisc_word
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


def test_creed_raw_tables2fisc_raw_tables_Scenario6_Creed_br00003_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00003_str = "br00003"
    br00003_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        hour_word_str(),
        cumlative_minute_str(),
    ]
    a23_hour_word = "4pm"
    a23_cumlative_minute = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00003_tablename = f"{br00003_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00003_tablename, br00003_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00003_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{hour_word_str()},{cumlative_minute_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_hour_word}',{a23_cumlative_minute})
, ({event3},'{sue_inx}','{accord23_str}','{a23_hour_word}',{a23_cumlative_minute})
, ({event7},'{sue_inx}','{accord23_str}','{a23_hour_word}',{a23_cumlative_minute})
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.hour_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.hour_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.hour_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00003_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_cumlative_minute,
            a23_hour_word,
            None,  # note
        )
        expected_row1 = (
            br00003_str,  # creed_number
            event7,
            sue_inx,
            accord23_str,  # fisc_word
            a23_cumlative_minute,
            a23_hour_word,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario7_Creed_br00004_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00004_str = "br00004"
    br00004_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        month_word_str(),
        cumlative_day_str(),
    ]
    a23_month_word = "March"
    a23_cumlative_day = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00004_tablename = f"{br00004_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00004_tablename, br00004_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00004_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{month_word_str()},{cumlative_day_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_month_word}',{a23_cumlative_day})
, ({event3},'{sue_inx}','{accord23_str}','{a23_month_word}',{a23_cumlative_day})
, ({event7},'{sue_inx}','{accord23_str}','{a23_month_word}',{a23_cumlative_day})
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.mont_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.mont_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.mont_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00004_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_cumlative_day,
            a23_month_word,
            None,  # note
        )
        expected_row1 = (
            br00004_str,  # creed_number
            event7,
            sue_inx,
            accord23_str,  # fisc_word
            a23_cumlative_day,
            a23_month_word,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_creed_raw_tables2fisc_raw_tables_Scenario8_Creed_br00005_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00005_str = "br00005"
    br00005_columns = [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        weekday_word_str(),
        weekday_order_str(),
    ]
    a23_weekday_word = "wednesday"
    a23_weekday_order = 44

    with sqlite3_connect(":memory:") as fisc_db_conn:
        br00005_tablename = f"{br00005_str}_raw"
        cursor = fisc_db_conn.cursor()
        create_creed_sorted_table(cursor, br00005_tablename, br00005_columns)
        insert_raw_sqlstr = f"""
INSERT INTO {br00005_tablename} ({event_int_str()},{face_name_str()},{fisc_word_str()},{weekday_word_str()},{weekday_order_str()})
VALUES
  ({event3},'{sue_inx}','{accord23_str}','{a23_weekday_word}',{a23_weekday_order})
, ({event3},'{sue_inx}','{accord23_str}','{a23_weekday_word}',{a23_weekday_order})
, ({event7},'{sue_inx}','{accord23_str}','{a23_weekday_word}',{a23_weekday_order})
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        x_fisc = FiscPrimeObjsRef()
        create_fisc_prime_tables(cursor)
        assert get_row_count(cursor, x_fisc.week_raw_tablename) == 0

        # WHEN
        creed_raw_tables2fisc_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.week_raw_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.week_raw_tablename}")
        fiscunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00005_str,  # creed_number
            event3,
            sue_inx,
            accord23_str,  # fisc_word
            a23_weekday_order,
            a23_weekday_word,
            None,  # note
        )
        expected_row1 = (
            br00005_str,  # creed_number
            event7,
            sue_inx,
            accord23_str,  # fisc_word
            a23_weekday_order,
            a23_weekday_word,
            None,  # note
        )
        print(f"{fiscunit_db_rows[0]=}")
        print(f"{fiscunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscunit_db_rows[0] == expected_row0
        assert fiscunit_db_rows[1] == expected_row1
        assert fiscunit_db_rows == [expected_row0, expected_row1]


def test_etl_fisc_raw_tables_to_fisc_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        fisc_mstr_dir = get_module_temp_dir()
        fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
        x_fisc = FiscPrimeObjsRef(fiscs_dir)
        fisc_cols = FiscPrimeColumnsRef()
        insert_raw_sqlstr = f"""
INSERT INTO {x_fisc.unit_raw_tablename} ({creed_number_str()}, {event_int_str()}, {face_name_str()}, {fisc_word_str()})
VALUES 
  ('{br00011_str}', {event3}, '{sue_inx}', '{accord23_str}')
, ('{br00011_str}', {event3}, '{sue_inx}', '{accord23_str}')
, ('{br00011_str}', {event3}, '{sue_inx}', '{accord45_str}')
, ('{br00011_str}', {event7}, '{sue_inx}', '{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert os_path_exists(x_fisc.unit_raw_csv_path) is False
        assert os_path_exists(x_fisc.deal_raw_csv_path) is False
        assert os_path_exists(x_fisc.cash_raw_csv_path) is False
        assert os_path_exists(x_fisc.hour_raw_csv_path) is False
        assert os_path_exists(x_fisc.mont_raw_csv_path) is False
        assert os_path_exists(x_fisc.week_raw_csv_path) is False

        # WHEN
        etl_fisc_raw_tables_to_fisc_csvs(cursor, fiscs_dir)

        # THEN
        assert os_path_exists(x_fisc.unit_raw_csv_path)
        assert os_path_exists(x_fisc.deal_raw_csv_path)
        assert os_path_exists(x_fisc.cash_raw_csv_path)
        assert os_path_exists(x_fisc.hour_raw_csv_path)
        assert os_path_exists(x_fisc.mont_raw_csv_path)
        assert os_path_exists(x_fisc.week_raw_csv_path)
        unit_raw_csv_filename = x_fisc.unit_raw_csv_filename
        generated_fiscunit_csv = open_file(fiscs_dir, unit_raw_csv_filename)
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_raw_csv_header}
{br00011_str},{event3},{sue_inx},{accord23_str},,,,,,,,,,
{br00011_str},{event3},{sue_inx},{accord23_str},,,,,,,,,,
{br00011_str},{event3},{sue_inx},{accord45_str},,,,,,,,,,
{br00011_str},{event7},{sue_inx},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscunit_csv=}")
        print(f"{expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fisc.deal_raw_csv_path)) == 94
        assert len(open_file(x_fisc.cash_raw_csv_path)) == 87
        assert len(open_file(x_fisc.hour_raw_csv_path)) == 78
        assert len(open_file(x_fisc.mont_raw_csv_path)) == 76
        assert len(open_file(x_fisc.week_raw_csv_path)) == 78


def test_etl_fisc_raw_tables_to_fisc_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        fisc_mstr_dir = get_module_temp_dir()
        fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
        x_fisc = FiscPrimeObjsRef(fiscs_dir)
        fisc_cols = FiscPrimeColumnsRef()
        insert_raw_sqlstr = f"""
INSERT INTO {x_fisc.unit_raw_tablename} ({creed_number_str()}, {event_int_str()}, {face_name_str()}, {fisc_word_str()})
VALUES 
  ('{br00011_str}', {event3}, '{sue_inx}', '{accord23_str}')
, ('{br00011_str}', {event3}, '{sue_inx}', '{accord23_str}')
, ('{br00011_str}', {event3}, '{sue_inx}', '{accord45_str}')
, ('{br00011_str}', {event7}, '{sue_inx}', '{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert os_path_exists(x_fisc.unit_raw_csv_path) is False
        assert os_path_exists(x_fisc.deal_raw_csv_path) is False
        assert os_path_exists(x_fisc.cash_raw_csv_path) is False
        assert os_path_exists(x_fisc.hour_raw_csv_path) is False
        assert os_path_exists(x_fisc.mont_raw_csv_path) is False
        assert os_path_exists(x_fisc.week_raw_csv_path) is False

        # WHEN
        etl_fisc_raw_tables_to_fisc_csvs(cursor, fiscs_dir)

        # THEN
        assert os_path_exists(x_fisc.unit_raw_csv_path)
        assert os_path_exists(x_fisc.deal_raw_csv_path)
        assert os_path_exists(x_fisc.cash_raw_csv_path)
        assert os_path_exists(x_fisc.hour_raw_csv_path)
        assert os_path_exists(x_fisc.mont_raw_csv_path)
        assert os_path_exists(x_fisc.week_raw_csv_path)
        unit_raw_csv_filename = x_fisc.unit_raw_csv_filename
        generated_fiscunit_csv = open_file(fiscs_dir, unit_raw_csv_filename)
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_raw_csv_header}
{br00011_str},{event3},{sue_inx},{accord23_str},,,,,,,,,,
{br00011_str},{event3},{sue_inx},{accord23_str},,,,,,,,,,
{br00011_str},{event3},{sue_inx},{accord45_str},,,,,,,,,,
{br00011_str},{event7},{sue_inx},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscunit_csv=}")
        print(f"{expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fisc.deal_raw_csv_path)) == 94
        assert len(open_file(x_fisc.cash_raw_csv_path)) == 95
        assert len(open_file(x_fisc.hour_raw_csv_path)) == 84
        assert len(open_file(x_fisc.mont_raw_csv_path)) == 82
        assert len(open_file(x_fisc.week_raw_csv_path)) == 84


def test_GlobalVariablesForFisc_inconsistency_queryReturns_sqlstrs():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        # if dimen_config.get(creed_category_str()) != "pidgin"
        if dimen_config.get(creed_category_str()) == "fisc"
    }

    exclude_cols = {"creed_number", "event_int", "face_name", "error_message"}
    with sqlite3_connect(":memory:") as conn:
        create_fisc_prime_tables(conn)

        for x_dimen, x_sqlstr in get_fisc_inconsistency_sqlstrs().items():
            x_tablename = f"{x_dimen}_raw"
            dimen_config = creed_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns.remove(event_int_str())
            dimen_focus_columns.remove(face_name_str())
            expected_dimen_sqlstr = create_select_inconsistency_query(
                conn, x_tablename, dimen_focus_columns, exclude_cols
            )
            assert x_sqlstr == expected_dimen_sqlstr
            print(f"{x_dimen} checked...")


def test_set_fisc_raw_error_message_Scenario0_fisunit_WithNo_error_message(
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
    a23_timeline_word = "accord23_timeline"
    a23_job_listen_rotations = 6
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.unit_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.unit_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_word}',{a23_job_listen_rotations},NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_word}',{a23_job_listen_rotations},NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, error_message FROM {x_tablename};"
        # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
        cursor.execute(select_sqlstr)
        print(f"{select_sqlstr=}")
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [(event3, None), (event7, None)]

        # WHEN
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [(event3, None), (event7, None)]


def test_set_fisc_raw_error_message_Scenario1_fisunit_Some_error_message(
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
    a23_timeline_word = "accord23_timeline"
    a23_job_listen_rotations = 900
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.unit_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.unit_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}',{a23_fund_coin},{a23_penny_1},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_word}',{a23_job_listen_rotations},NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_word}',{a23_job_listen_rotations},NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_word}',{a23_job_listen_rotations},NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_raw_error_message_Scenario2_fishour_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_4hour_word = "4pm"
    a23_5hour_word = "5pm"
    a23_cumlative_minute_1 = 44
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.hour_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.hour_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}',{a23_cumlative_minute_1},'{a23_4hour_word}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{a23_cumlative_minute_1},'{a23_5hour_word}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}',{a23_cumlative_minute_1},'{a23_4hour_word}',NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_raw_error_message_Scenario3_fishour_Some_error_message(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_month_word_1 = "March"
    a23_month_word_2 = "Marche"
    _44_cumlative_day = 44
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.mont_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.mont_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}',{_44_cumlative_day},'{a23_month_word_1}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{_44_cumlative_day},'{a23_month_word_2}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}',{_44_cumlative_day},'{a23_month_word_2}',NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 3
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, x_error_message),
            (event7, accord23_str, x_error_message),
            (event7, accord45_str, None),
        ]


def test_set_fisc_raw_error_message_Scenario4_fisweek_Some_error_message(
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
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.week_raw_tablename
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.week_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}',{order1},'{mon_str}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{order2},'{tue_str}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}',{order2},'{wed_str}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}',{order1},'{mon_str}',NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}',{order3},'{wed_str}',NULL)
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, {weekday_order_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, order1, None),
            (event7, accord23_str, order2, x_error_message),
            (event7, accord23_str, order2, x_error_message),
            (event7, accord45_str, order1, None),
            (event7, accord45_str, order3, None),
        ]


def test_set_fisc_raw_error_message_Scenario5_fisdeal_Some_error_message(
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
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.deal_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.deal_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_2},NULL,NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}','{a23_owner_name}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}','{a23_owner_name}',{t2_deal_time},{t2_quota},NULL,NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, {deal_time_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t1_deal_time, x_error_message),
            (event7, accord23_str, t2_deal_time, None),
            (event7, accord45_str, t1_deal_time, None),
            (event7, accord45_str, t2_deal_time, None),
        ]


def test_set_fisc_raw_error_message_Scenario6_fiscash_Some_error_message(
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
        create_fisc_prime_tables(cursor)
        x_tablename = x_objs.cash_raw_tablename
        assert db_table_exists(cursor, x_tablename)
        insert_raw_sqlstr = f"""
INSERT INTO {x_tablename} ({x_cols.cash_raw_csv_header})
VALUES
  ('br00333',{event3},'{sue_inx}','{accord23_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_1},NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_2},NULL)
, ('br00333',{event7},'{sue_inx}','{accord23_str}','{yao_inx}','{bob_inx}',{t2_tran_time},{t2_amount},NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}','{yao_inx}','{bob_inx}',{t1_tran_time},{t1_amount_1},NULL)
, ('br00333',{event7},'{sue_inx}','{accord45_str}','{yao_inx}','{bob_inx}',{t2_tran_time},{t2_amount},NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_tablename) == 5
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_word_str()}, {tran_time_str()}, error_message FROM {x_tablename};"
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
        set_fisc_raw_error_message(cursor)

        # THEN
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        x_error_message = "Inconsistent data"
        assert rows == [
            (event3, accord23_str, t1_tran_time, x_error_message),
            (event7, accord23_str, t1_tran_time, x_error_message),
            (event7, accord23_str, t2_tran_time, None),
            (event7, accord45_str, t1_tran_time, None),
            (event7, accord45_str, t2_tran_time, None),
        ]
