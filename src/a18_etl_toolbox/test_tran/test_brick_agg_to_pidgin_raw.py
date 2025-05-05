from src.a00_data_toolbox.file_toolbox import create_path
from src.a00_data_toolbox.db_toolbox import (
    create_select_query,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_tag_str,
    otx_tag_str,
    inx_road_str,
    otx_road_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
)
from src.a17_idea_logic._utils.str_a17 import (
    idea_number_str,
    brick_agg_str,
    brick_valid_str,
)
from src.a17_idea_logic.idea_db_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    create_idea_sorted_table,
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


def test_get_pidgen_idea_format_filenames_ReturnsObj():
    # ESTABLISH / WHEN
    pidgen_idea_filenames = _get_pidgen_idea_format_filenames()

    # THEN
    print(f"need examples for {pidgen_idea_filenames=}")
    assert pidgen_idea_filenames == {
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
        fisc_tag_str(),
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
        unknown_word_str(),
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
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(brick_dir, "br00042.xlsx")
    br00042_columns = [
        event_int_str(),
        face_name_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
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
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    br00044_file_path = create_path(brick_dir, "br00044.xlsx")
    br00044_columns = [
        event_int_str(),
        face_name_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
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
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(brick_dir, "br00045.xlsx")
    br00045_columns = [
        event_int_str(),
        face_name_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
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
    label_raw_str = "label_raw"
    name_raw_str = "name_raw"
    tag_raw_str = "tag_raw"
    road_raw_str = "road_raw"
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, tag_raw_str)
    assert sheet_exists(pidgin_path, road_raw_str)

    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_raw_str)
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_raw_str)
    gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)

    label_file_columns = PidginPrimeColumns().pidgin_label_raw_columns
    assert list(gen_label_df.columns) == label_file_columns
    assert len(gen_label_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

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

    tag_file_columns = [
        idea_number_str(),
        event_int_str(),
        face_name_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_tag_df.columns) == tag_file_columns
    assert len(gen_tag_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_tag3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_tag4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_tag_rows = [e1_tag3, e1_tag4]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_file_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)

    road_file_columns = [
        idea_number_str(),
        event_int_str(),
        face_name_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_df.columns) == road_file_columns
    assert len(gen_road_df) == 2
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road_rows = [e1_road3, e1_road4]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)


def create_brick_valid_table(cursor, idea_number: str):
    if idea_number == "br00113":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_name_str(),
            inx_name_str(),
        ]
    elif idea_number == "br00043":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_name_str(),
            inx_name_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00115":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_label_str(),
            inx_label_str(),
        ]
    elif idea_number == "br00042":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_label_str(),
            inx_label_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00116":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_tag_str(),
            inx_tag_str(),
        ]
    elif idea_number == "br00044":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_tag_str(),
            inx_tag_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00117":
        x_columns = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_road_str(),
            inx_road_str(),
        ]
    elif idea_number == "br00045":
        x_columns = [
            event_int_str(),
            face_name_str(),
            otx_road_str(),
            inx_road_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    agg_tablename = f"{brick_valid_str()}_{idea_number}"
    create_idea_sorted_table(cursor, agg_tablename, x_columns)


def populate_brick_valid_table(cursor, idea_number: str):
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
    agg_tablename = f"{brick_valid_str()}_{idea_number}"
    if idea_number == "br00042":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_label_str()}
, {inx_label_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event2}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event5}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00043":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event2}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event5}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00044":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_tag_str()}
, {inx_tag_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event0}', '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{event0}', '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{event1}', '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00045":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
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
    elif idea_number == "br00113":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
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
    elif idea_number == "br00115":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_label_str()}
, {inx_label_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00116":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_tag_str()}
, {inx_tag_str()}
)"""
        values_clause = f"""
VALUES     
  ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{event1}', '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00117":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_road_str()}
, {inx_road_str()}
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
        pidgin_raw_label_tablename = "pidgin_label_raw"
        pidgin_raw_name_tablename = "pidgin_name_raw"
        pidgin_raw_tag_tablename = "pidgin_tag_raw"
        pidgin_raw_road_tablename = "pidgin_road_raw"
        create_pidgin_prime_tables(cursor)
        assert get_row_count(cursor, pidgin_raw_label_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_name_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_tag_tablename) == 0
        assert get_row_count(cursor, pidgin_raw_road_tablename) == 0

        # WHEN
        brick_valid_tables_to_pidgin_prime_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_raw_label_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_name_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_tag_tablename) == 5
        assert get_row_count(cursor, pidgin_raw_road_tablename) == 7
        pidlabe_raw_cols = get_table_columns(cursor, pidgin_raw_label_tablename)
        pidname_raw_cols = get_table_columns(cursor, pidgin_raw_name_tablename)
        pidtagg_raw_cols = get_table_columns(cursor, pidgin_raw_tag_tablename)
        pidroad_raw_cols = get_table_columns(cursor, pidgin_raw_road_tablename)
        lab_table = pidgin_raw_label_tablename
        nam_table = pidgin_raw_name_tablename
        tag_table = pidgin_raw_tag_tablename
        roa_table = pidgin_raw_road_tablename
        select_pidlabe = create_select_query(cursor, lab_table, pidlabe_raw_cols)
        select_pidname = create_select_query(cursor, nam_table, pidname_raw_cols)
        select_pidtagg = create_select_query(cursor, tag_table, pidtagg_raw_cols)
        select_pidroad = create_select_query(cursor, roa_table, pidroad_raw_cols)
        cursor.execute(select_pidlabe)
        lab_rows = cursor.fetchall()
        cursor.execute(select_pidname)
        nam_rows = cursor.fetchall()
        cursor.execute(select_pidtagg)
        tag_rows = cursor.fetchall()
        cursor.execute(select_pidroad)
        roa_rows = cursor.fetchall()
        assert len(lab_rows) == 5
        assert len(nam_rows) == 5
        assert len(tag_rows) == 5
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
        assert tag_rows[0] == row0
        assert tag_rows[1] == row1
        assert tag_rows[2] == row2
        assert tag_rows[3] == row3
        assert tag_rows[4] == row4

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
    raw_lab_table = "pidgin_label_raw"
    raw_nam_table = "pidgin_name_raw"
    raw_tag_table = "pidgin_tag_raw"
    raw_roa_table = "pidgin_road_raw"
    br00113_str = "br00113"
    br00043_str = "br00043"
    br00115_str = "br00115"
    br00042_str = "br00042"
    br00116_str = "br00116"
    br00044_str = "br00044"
    br00117_str = "br00117"
    br00045_str = "br00045"

    raw_nam_insert_into_clause = f"""INSERT INTO {raw_nam_table} ({idea_number_str()},{event_int_str()},{face_name_str()},{otx_name_str()},{inx_name_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_word_str()})"""
    raw_lab_insert_into_clause = f"""INSERT INTO {raw_lab_table} ({idea_number_str()},{event_int_str()},{face_name_str()},{otx_label_str()},{inx_label_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_word_str()})"""
    raw_tag_insert_into_clause = f"""INSERT INTO {raw_tag_table} ({idea_number_str()},{event_int_str()},{face_name_str()},{otx_tag_str()},{inx_tag_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_word_str()})"""
    raw_roa_insert_into_clause = f"""INSERT INTO {raw_roa_table} ({idea_number_str()},{event_int_str()},{face_name_str()},{otx_road_str()},{inx_road_str()},{otx_bridge_str()},{inx_bridge_str()},{unknown_word_str()})"""
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
    raw_tag_values_clause = f"""
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
    tag_insert_sqlstr = f"{raw_tag_insert_into_clause} {raw_tag_values_clause}"
    roa_insert_sqlstr = f"{raw_roa_insert_into_clause} {raw_roa_values_clause}"
    cursor.execute(nam_insert_sqlstr)
    cursor.execute(lab_insert_sqlstr)
    cursor.execute(tag_insert_sqlstr)
    cursor.execute(roa_insert_sqlstr)
