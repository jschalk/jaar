from src.a00_data_toolbox.file_toolbox import create_path
from src.a00_data_toolbox.db_toolbox import (
    create_select_query,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_label_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    inx_way_str,
    otx_way_str,
    inx_title_str,
    otx_title_str,
    unknown_term_str,
)
from src.a17_creed_logic._utils.str_a17 import (
    creed_number_str,
    brick_agg_str,
    brick_valid_str,
)
from src.a17_creed_logic.creed_db_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_creed_format_filenames,
    create_creed_sorted_table,
)
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.tran_sqlstrs import create_pidgin_prime_tables
from src.a18_etl_toolbox.transformers import (
    etl_brick_agg_df_to_brick_pidgin_raw_df,
    brick_valid_tables_to_pidgin_prime_raw_tables,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir as etl_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect, Cursor as sqlite_Cursor


def test_get_pidgen_creed_format_filenames_ReturnsObj():
    # ESTABLISH / WHEN
    pidgen_creed_filenames = _get_pidgen_creed_format_filenames()

    # THEN
    print(f"pbranch examples for {pidgen_creed_filenames=}")
    assert pidgen_creed_filenames == {
        "br00042.xlsx",
        "br00043.xlsx",
        "br00044.xlsx",
        "br00045.xlsx",
        "br00113.xlsx",
        "br00115.xlsx",
        "br00116.xlsx",
        "br00117.xlsx",
    }


def test_etl_brick_agg_df_to_brick_pidgin_raw_df_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    m_str = "accord23"
    event1 = 1
    event2 = 2
    event5 = 5
    brick_dir = etl_dir()
    br00113_file_path = create_path(brick_dir, "br00113.xlsx")
    br00113_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(brick_dir, "br00043.xlsx")
    br00043_columns = [
        event_int_str(),
        face_name_str(),
        otx_name_str(),
        inx_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, brick_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, brick_agg_str(), br00043_df)
    pidgin_path = create_brick_pidgin_path(brick_dir)

    br00115_file_path = create_path(brick_dir, "br00115.xlsx")
    br00115_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00042_file_path = create_path(brick_dir, "br00042.xlsx")
    br00042_columns = [
        event_int_str(),
        face_name_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, brick_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, brick_agg_str(), br00042_df)

    br00116_file_path = create_path(brick_dir, "br00116.xlsx")
    br00116_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00044_file_path = create_path(brick_dir, "br00044.xlsx")
    br00044_columns = [
        event_int_str(),
        face_name_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, brick_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, brick_agg_str(), br00044_df)

    br00117_file_path = create_path(brick_dir, "br00117.xlsx")
    br00117_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_way_str(),
        inx_way_str(),
    ]
    br00045_file_path = create_path(brick_dir, "br00045.xlsx")
    br00045_columns = [
        event_int_str(),
        face_name_str(),
        otx_way_str(),
        inx_way_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, brick_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, brick_agg_str(), br00045_df)

    events = {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_brick_agg_df_to_brick_pidgin_raw_df(events, brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_raw_str = "title_raw"
    name_raw_str = "name_raw"
    label_raw_str = "label_raw"
    way_raw_str = "way_raw"
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, title_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, way_raw_str)

    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_raw_str)
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_raw_str)
    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_raw_str)
    gen_way_df = pandas_read_excel(pidgin_path, sheet_name=way_raw_str)

    title_file_columns = PidginPrimeColumns().pidgin_title_raw_columns
    assert list(gen_title_df.columns) == title_file_columns
    assert len(gen_title_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_title3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title_rows = [e1_title3, e1_title4]
    e1_title_df = DataFrame(e1_title_rows, columns=title_file_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)

    name_raw_columns = PidginPrimeColumns().pidgin_name_raw_columns
    assert list(gen_name_df.columns) == name_raw_columns
    assert len(gen_name_df) == 2
    b3 = "br00113"
    b4 = "br00043"
    e1_name3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_name4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_name_rows = [e1_name3, e1_name4]
    e1_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

    label_file_columns = [
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    assert list(gen_label_df.columns) == label_file_columns
    assert len(gen_label_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_label3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

    way_file_columns = [
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        otx_way_str(),
        inx_way_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    assert list(gen_way_df.columns) == way_file_columns
    assert len(gen_way_df) == 2
    b3 = "br00117"
    b4 = "br00045"
    e1_way3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_way4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_way_rows = [e1_way3, e1_way4]
    e1_way_df = DataFrame(e1_way_rows, columns=way_file_columns)
    assert len(gen_way_df) == len(e1_way_df)
    print(f"{gen_way_df.to_csv()=}")
    print(f" {e1_way_df.to_csv()=}")
    assert gen_way_df.to_csv(index=False) == e1_way_df.to_csv(index=False)


def create_brick_valid_table(cursor, creed_number: str):
    if creed_number == "br00113":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_label_str(),
            owner_name_str(),
            acct_name_str(),
            otx_name_str(),
            inx_name_str(),
        ]
    elif creed_number == "br00043":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_name_str(),
            inx_name_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_term_str(),
        ]
    elif creed_number == "br00115":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_label_str(),
            owner_name_str(),
            acct_name_str(),
            otx_title_str(),
            inx_title_str(),
        ]
    elif creed_number == "br00042":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_title_str(),
            inx_title_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_term_str(),
        ]
    elif creed_number == "br00116":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_label_str(),
            owner_name_str(),
            acct_name_str(),
            otx_label_str(),
            inx_label_str(),
        ]
    elif creed_number == "br00044":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_label_str(),
            inx_label_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_term_str(),
        ]
    elif creed_number == "br00117":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_label_str(),
            owner_name_str(),
            acct_name_str(),
            otx_way_str(),
            inx_way_str(),
        ]
    elif creed_number == "br00045":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_way_str(),
            inx_way_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_term_str(),
        ]
    agg_tablename = f"{brick_valid_str()}_{creed_number}"
    create_creed_sorted_table(cursor, agg_tablename, x_columns)


def populate_brick_valid_table(cursor, creed_number: str):
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    a23_str = "accord23"
    a45_str = "accord45"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event9 = 9
    agg_tablename = f"{brick_valid_str()}_{creed_number}"
    if creed_number == "br00042":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_title_str()}
, {inx_title_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_term_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event2}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event5}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif creed_number == "br00043":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_term_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event2}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event5}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif creed_number == "br00044":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_label_str()}
, {inx_label_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_term_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event0}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event0}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif creed_number == "br00045":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_way_str()}
, {inx_way_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_term_str()}
)"""
        values_clause = f"""
VALUES
  ('{event2}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event5}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif creed_number == "br00113":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_name_str()}
, {inx_name_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event9}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event9}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif creed_number == "br00115":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_title_str()}
, {inx_title_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif creed_number == "br00116":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_label_str()}
, {inx_label_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif creed_number == "br00117":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_way_str()}
, {inx_way_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor.execute(insert_sqlstr)


def test_brick_valid_tables_to_pidgin_prime_raw_tables_PopulatesTables():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event9 = 9
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        br00113_str = "br00113"
        br00043_str = "br00043"
        br00115_str = "br00115"
        br00042_str = "br00042"
        br00116_str = "br00116"
        br00044_str = "br00044"
        br00117_str = "br00117"
        br00045_str = "br00045"
        create_brick_valid_table(cursor, br00113_str)
        create_brick_valid_table(cursor, br00043_str)
        create_brick_valid_table(cursor, br00115_str)
        create_brick_valid_table(cursor, br00042_str)
        create_brick_valid_table(cursor, br00116_str)
        create_brick_valid_table(cursor, br00044_str)
        create_brick_valid_table(cursor, br00117_str)
        create_brick_valid_table(cursor, br00045_str)
        populate_brick_valid_table(cursor, br00113_str)
        populate_brick_valid_table(cursor, br00043_str)
        populate_brick_valid_table(cursor, br00115_str)
        populate_brick_valid_table(cursor, br00042_str)
        populate_brick_valid_table(cursor, br00116_str)
        populate_brick_valid_table(cursor, br00044_str)
        populate_brick_valid_table(cursor, br00117_str)
        populate_brick_valid_table(cursor, br00045_str)
        br00113_tablename = f"{brick_valid_str()}_{br00113_str}"
        br00043_tablename = f"{brick_valid_str()}_{br00043_str}"
        br00115_tablename = f"{brick_valid_str()}_{br00115_str}"
        br00042_tablename = f"{brick_valid_str()}_{br00042_str}"
        br00116_tablename = f"{brick_valid_str()}_{br00116_str}"
        br00044_tablename = f"{brick_valid_str()}_{br00044_str}"
        br00117_tablename = f"{brick_valid_str()}_{br00117_str}"
        br00045_tablename = f"{brick_valid_str()}_{br00045_str}"
        assert get_row_count(cursor, br00113_tablename) == 2
        assert get_row_count(cursor, br00043_tablename) == 3
        assert get_row_count(cursor, br00115_tablename) == 3
        assert get_row_count(cursor, br00042_tablename) == 3
        assert get_row_count(cursor, br00116_tablename) == 2
        assert get_row_count(cursor, br00044_tablename) == 3
        assert get_row_count(cursor, br00117_tablename) == 2
        assert get_row_count(cursor, br00045_tablename) == 5
        pidgin_raw_title_tablename = "pidgin_title_raw"
        pidgin_raw_name_tablename = "pidgin_name_raw"
        pidgin_raw_label_tablename = "pidgin_label_raw"
        pidgin_raw_way_tablename = "pidgin_way_raw"
        create_pidgin_prime_tables(cursor)
        assert get_row_count(cursor, pidgin_raw_title_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_name_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_label_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_way_tablename) == 0

        # WHEN
        brick_valid_tables_to_pidgin_prime_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_raw_title_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_name_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_label_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_way_tablename) == 7
        pidtitl_raw_cols = get_table_columns(cursor, pidgin_raw_title_tablename)
        pidname_raw_cols = get_table_columns(cursor, pidgin_raw_name_tablename)
        pidlabe_raw_cols = get_table_columns(cursor, pidgin_raw_label_tablename)
        pidwayy_raw_cols = get_table_columns(cursor, pidgin_raw_way_tablename)
        lab_table = pidgin_raw_title_tablename
        nam_table = pidgin_raw_name_tablename
        label_table = pidgin_raw_label_tablename
        roa_table = pidgin_raw_way_tablename
        select_pidtitl = create_select_query(cursor, lab_table, pidtitl_raw_cols)
        select_pidname = create_select_query(cursor, nam_table, pidname_raw_cols)
        select_pidlabe = create_select_query(cursor, label_table, pidlabe_raw_cols)
        select_pidwayy = create_select_query(cursor, roa_table, pidwayy_raw_cols)
        cursor.execute(select_pidtitl)
        lab_rows = cursor.fetchall()
        cursor.execute(select_pidname)
        nam_rows = cursor.fetchall()
        cursor.execute(select_pidlabe)
        label_rows = cursor.fetchall()
        cursor.execute(select_pidwayy)
        roa_rows = cursor.fetchall()
        assert len(lab_rows) == 5
        assert len(nam_rows) == 5
        assert len(label_rows) == 5
        assert len(roa_rows) == 7

        br00115_str = "br00115"
        br00042_str = "br00042"
        row0 = (br00042_str, event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        row1 = (br00042_str, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        row2 = (br00042_str, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        row3 = (br00115_str, event1, sue_str, bob_str, bob_inx, None, None, None, None)
        row4 = (br00115_str, event1, sue_str, yao_str, yao_inx, None, None, None, None)
        assert lab_rows[0] == row0
        assert lab_rows[1] == row1
        assert lab_rows[2] == row2
        assert lab_rows[3] == row3
        assert lab_rows[4] == row4

        br00113_str = "br00113"
        br00043_str = "br00043"
        row0 = (br00043_str, event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        row1 = (br00043_str, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        row2 = (br00043_str, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        row3 = (br00113_str, event9, sue_str, bob_str, bob_inx, None, None, None, None)
        row4 = (br00113_str, event9, sue_str, yao_str, yao_inx, None, None, None, None)
        assert nam_rows[0] == row0
        assert nam_rows[1] == row1
        assert nam_rows[2] == row2
        assert nam_rows[3] == row3
        assert nam_rows[4] == row4

        br00116_str = "br00116"
        br00044_str = "br00044"
        row0 = (br00044_str, event0, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        row1 = (br00044_str, event0, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        row2 = (br00044_str, event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        row3 = (br00116_str, event1, sue_str, bob_str, bob_inx, None, None, None, None)
        row4 = (br00116_str, event1, sue_str, yao_str, yao_inx, None, None, None, None)
        assert label_rows[0] == row0
        assert label_rows[1] == row1
        assert label_rows[2] == row2
        assert label_rows[3] == row3
        assert label_rows[4] == row4

        br00117_str = "br00117"
        br00045_str = "br00045"
        row0 = (br00045_str, event1, yao_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        row1 = (br00045_str, event1, yao_str, sue_str, sue_str, rdx, rdx, ukx, None)
        row2 = (br00045_str, event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx, None)
        row3 = (br00045_str, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None)
        row4 = (br00045_str, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None)
        row5 = (br00117_str, event1, sue_str, bob_str, bob_inx, None, None, None, None)
        row6 = (br00117_str, event1, sue_str, yao_str, yao_inx, None, None, None, None)
        print(f"{roa_rows[0]=}")
        print(f"       {row0=}")
        assert roa_rows[0] == row0
        assert roa_rows[1] == row1
        assert roa_rows[2] == row2
        assert roa_rows[3] == row3
        assert roa_rows[4] == row4
        assert roa_rows[5] == row5
        assert roa_rows[6] == row6


def populate_pidgin_raw_tables(cursor: sqlite_Cursor):
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    a23_str = "accord23"
    a45_str = "accord45"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event9 = 9
    raw_lab_table = "pidgin_title_raw"
    raw_nam_table = "pidgin_name_raw"
    raw_label_table = "pidgin_label_raw"
    raw_roa_table = "pidgin_way_raw"
    br00113_str = "br00113"
    br00043_str = "br00043"
    br00115_str = "br00115"
    br00042_str = "br00042"
    br00116_str = "br00116"
    br00044_str = "br00044"
    br00117_str = "br00117"
    br00045_str = "br00045"

    raw_nam_insert_into_clause = f"""INSERT INTO {raw_nam_table} ({creed_number_str()},{event_int_str()},{face_name_str()},{otx_name_str()},{inx_name_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_term_str()})"""
    raw_lab_insert_into_clause = f"""INSERT INTO {raw_lab_table} ({creed_number_str()},{event_int_str()},{face_name_str()},{otx_title_str()},{inx_title_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_term_str()})"""
    raw_label_insert_into_clause = f"""INSERT INTO {raw_label_table} ({creed_number_str()},{event_int_str()},{face_name_str()},{otx_label_str()},{inx_label_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_term_str()})"""
    raw_roa_insert_into_clause = f"""INSERT INTO {raw_roa_table} ({creed_number_str()},{event_int_str()},{face_name_str()},{otx_way_str()},{inx_way_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_term_str()})"""
    raw_nam_values_clause = f"""
VALUES     
  ('{br00042_str}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00042_str}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00042_str}', {event1}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00115_str}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ('{br00115_str}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
;
"""
    raw_lab_values_clause = f"""
VALUES     
  ('{br00043_str}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00043_str}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00043_str}', {event1}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00113_str}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ('{br00113_str}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
;
"""
    raw_label_values_clause = f"""
VALUES     
  ('{br00044_str}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00044_str}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00044_str}', {event1}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00116_str}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ('{br00116_str}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ('{br00116_str}', {event9}, '{yao_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
;
"""
    raw_roa_values_clause = f"""
VALUES     
  ('{br00045_str}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00045_str}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00045_str}', {event1}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{br00117_str}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
;
"""
    nam_insert_sqlstr = f"{raw_nam_insert_into_clause} {raw_nam_values_clause}"
    lab_insert_sqlstr = f"{raw_lab_insert_into_clause} {raw_lab_values_clause}"
    label_insert_sqlstr = f"{raw_label_insert_into_clause} {raw_label_values_clause}"
    roa_insert_sqlstr = f"{raw_roa_insert_into_clause} {raw_roa_values_clause}"
    cursor.execute(nam_insert_sqlstr)
    cursor.execute(lab_insert_sqlstr)
    cursor.execute(label_insert_sqlstr)
    cursor.execute(roa_insert_sqlstr)
