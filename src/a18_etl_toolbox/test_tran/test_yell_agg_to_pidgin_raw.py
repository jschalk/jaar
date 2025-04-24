from src.a00_data_toolboxs.file_toolbox import create_path
from src.a00_data_toolboxs.db_toolbox import (
    create_table_from_columns,
    db_table_exists,
    get_row_count,
)
from src.a02_finance_toolboxs.deal import owner_name_str, fisc_tag_str
from src.a08_bud_atom_logic.atom_config import (
    face_name_str,
    acct_name_str,
    event_int_str,
)
from src.a16_pidgin_logic.pidgin_config import (
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
from src.a17_idea_logic.idea_db_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    yell_agg_str,
)
from src.a18_etl_toolbox.tran_path import create_yell_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_yell_agg_df_to_yell_pidgin_raw_df,
    etl_yell_agg_db_to_yell_pidgin_raw_db,
)
from src.a18_etl_toolbox.examples.etl_env import (
    get_test_etl_dir as etl_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


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


def test_etl_yell_agg_df_to_yell_pidgin_raw_df_CreatesFile(env_dir_setup_cleanup):
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
    yell_dir = etl_dir()
    br00113_file_path = create_path(yell_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(yell_dir, "br00043.xlsx")
    br00043_columns = [
        face_name_str(),
        event_int_str(),
        otx_name_str(),
        inx_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, yell_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, yell_agg_str(), br00043_df)
    pidgin_path = create_yell_pidgin_path(yell_dir)

    br00115_file_path = create_path(yell_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(yell_dir, "br00042.xlsx")
    br00042_columns = [
        face_name_str(),
        event_int_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, yell_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, yell_agg_str(), br00042_df)

    br00116_file_path = create_path(yell_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    br00044_file_path = create_path(yell_dir, "br00044.xlsx")
    br00044_columns = [
        face_name_str(),
        event_int_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, yell_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, yell_agg_str(), br00044_df)

    br00117_file_path = create_path(yell_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(yell_dir, "br00045.xlsx")
    br00045_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, yell_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, yell_agg_str(), br00045_df)

    events = {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_yell_agg_df_to_yell_pidgin_raw_df(events, yell_dir)

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

    label_file_columns = PidginPrimeColumns().map_label_raw_columns
    assert list(gen_label_df.columns) == label_file_columns
    assert len(gen_label_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

    name_raw_columns = PidginPrimeColumns().map_name_raw_columns
    assert list(gen_name_df.columns) == name_raw_columns
    assert len(gen_name_df) == 2
    b3 = "br00113"
    b4 = "br00043"
    e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_name_rows = [e1_name3, e1_name4]
    e1_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

    tag_file_columns = [
        "src_idea",
        face_name_str(),
        event_int_str(),
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
    e1_tag3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_tag4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_tag_rows = [e1_tag3, e1_tag4]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_file_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)

    road_file_columns = [
        "src_idea",
        face_name_str(),
        event_int_str(),
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
    e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road_rows = [e1_road3, e1_road4]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)


def create_yell_agg_table(cursor, idea_number: str):
    if idea_number == "br00113":
        x_columns = [
            face_name_str(),
            event_int_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_name_str(),
            inx_name_str(),
        ]
    elif idea_number == "br00043":
        x_columns = [
            face_name_str(),
            event_int_str(),
            otx_name_str(),
            inx_name_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00115":
        x_columns = [
            face_name_str(),
            event_int_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_label_str(),
            inx_label_str(),
        ]
    elif idea_number == "br00042":
        x_columns = [
            face_name_str(),
            event_int_str(),
            otx_label_str(),
            inx_label_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00116":
        x_columns = [
            face_name_str(),
            event_int_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_tag_str(),
            inx_tag_str(),
        ]
    elif idea_number == "br00044":
        x_columns = [
            face_name_str(),
            event_int_str(),
            otx_tag_str(),
            inx_tag_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    elif idea_number == "br00117":
        x_columns = [
            face_name_str(),
            event_int_str(),
            fisc_tag_str(),
            owner_name_str(),
            acct_name_str(),
            otx_road_str(),
            inx_road_str(),
        ]
    elif idea_number == "br00045":
        x_columns = [
            face_name_str(),
            event_int_str(),
            otx_road_str(),
            inx_road_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
        ]
    x_types = {x_column: "TEXT" for x_column in x_columns}
    agg_tablename = f"{yell_agg_str()}_{idea_number}"
    create_table_from_columns(cursor, agg_tablename, x_columns, x_types)


def populate_yell_agg_table(cursor, idea_number: str):
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
    agg_tablename = f"{yell_agg_str()}_{idea_number}"
    if idea_number == "br00113":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_name_str()}
, {inx_name_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00043":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event2}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{sue_str}', '{event5}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{event1}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00115":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_label_str()}
, {inx_label_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00042":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {otx_label_str()}
, {inx_label_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event2}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{sue_str}', '{event5}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{event1}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00116":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_tag_str()}
, {inx_tag_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00044":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {otx_tag_str()}
, {inx_tag_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event2}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{sue_str}', '{event5}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{event1}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    elif idea_number == "br00117":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {otx_road_str()}
, {inx_road_str()}
)"""
        values_clause = f"""
VALUES     
  ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{yao_str}', '{yao_str}', '{yao_inx}')
, ('{sue_str}', '{event1}', '{m_str}', '{bob_str}', '{bob_str}', '{bob_str}', '{bob_inx}')
;
"""
    elif idea_number == "br00045":
        insert_into_clause = f"""
INSERT INTO {agg_tablename} (
  {face_name_str()}
, {event_int_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ('{sue_str}', '{event2}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{sue_str}', '{event5}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{event1}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor.execute(insert_sqlstr)


# def test_etl_yell_agg_db_to_yell_pidgin_raw_db_CreatesFile():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "accord23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         br00113_str = "br00113"
#         br00043_str = "br00043"
#         br00115_str = "br00115"
#         br00042_str = "br00042"
#         br00116_str = "br00116"
#         br00044_str = "br00044"
#         br00117_str = "br00117"
#         br00045_str = "br00045"
#         create_yell_agg_table(cursor, br00113_str)
#         create_yell_agg_table(cursor, br00043_str)
#         create_yell_agg_table(cursor, br00115_str)
#         create_yell_agg_table(cursor, br00042_str)
#         create_yell_agg_table(cursor, br00116_str)
#         create_yell_agg_table(cursor, br00044_str)
#         create_yell_agg_table(cursor, br00117_str)
#         create_yell_agg_table(cursor, br00045_str)
#         populate_yell_agg_table(cursor, br00113_str)
#         populate_yell_agg_table(cursor, br00043_str)
#         populate_yell_agg_table(cursor, br00115_str)
#         populate_yell_agg_table(cursor, br00042_str)
#         populate_yell_agg_table(cursor, br00116_str)
#         populate_yell_agg_table(cursor, br00044_str)
#         populate_yell_agg_table(cursor, br00117_str)
#         populate_yell_agg_table(cursor, br00045_str)
#         br00113_tablename = f"{yell_agg_str()}_{br00113_str}"
#         br00043_tablename = f"{yell_agg_str()}_{br00043_str}"
#         br00115_tablename = f"{yell_agg_str()}_{br00115_str}"
#         br00042_tablename = f"{yell_agg_str()}_{br00042_str}"
#         br00116_tablename = f"{yell_agg_str()}_{br00116_str}"
#         br00044_tablename = f"{yell_agg_str()}_{br00044_str}"
#         br00117_tablename = f"{yell_agg_str()}_{br00117_str}"
#         br00045_tablename = f"{yell_agg_str()}_{br00045_str}"
#         assert get_row_count(cursor, br00113_tablename) == 2
#         assert get_row_count(cursor, br00043_tablename) == 3
#         assert get_row_count(cursor, br00115_tablename) == 2
#         assert get_row_count(cursor, br00042_tablename) == 3
#         assert get_row_count(cursor, br00116_tablename) == 2
#         assert get_row_count(cursor, br00044_tablename) == 3
#         assert get_row_count(cursor, br00117_tablename) == 2
#         assert get_row_count(cursor, br00045_tablename) == 3

#         events = {event2: sue_str, event5: sue_str}

#         etl_yell_agg_db_to_yell_pidgin_raw_db(events, yell_dir)

#     # THEN
#     assert os_path_exists(pidgin_path)
#     label_raw_str = "label_raw"
#     name_raw_str = "name_raw"
#     tag_raw_str = "tag_raw"
#     road_raw_str = "road_raw"
#     assert sheet_exists(pidgin_path, name_raw_str)
#     assert sheet_exists(pidgin_path, label_raw_str)
#     assert sheet_exists(pidgin_path, tag_raw_str)
#     assert sheet_exists(pidgin_path, road_raw_str)

#     gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_raw_str)
#     gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_raw_str)
#     gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)

#     label_file_columns = PidginPrimeColumns().map_label_raw_columns
#     assert list(gen_label_df.columns) == label_file_columns
#     assert len(gen_label_df) == 2
#     b3 = "br00115"
#     b4 = "br00042"
#     e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_label_rows = [e1_label3, e1_label4]
#     e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
#     assert len(gen_label_df) == len(e1_label_df)
#     print(f"{gen_label_df.to_csv()=}")
#     print(f" {e1_label_df.to_csv()=}")
#     assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

#     name_raw_columns = PidginPrimeColumns().map_name_raw_columns
#     assert list(gen_name_df.columns) == name_raw_columns
#     assert len(gen_name_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_name_rows = [e1_name3, e1_name4]
#     e1_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
#     assert len(gen_name_df) == len(e1_name_df)
#     print(f"{gen_name_df.to_csv()=}")
#     print(f" {e1_name_df.to_csv()=}")
#     assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

#     tag_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_tag_str(),
#         inx_tag_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_tag_df.columns) == tag_file_columns
#     assert len(gen_tag_df) == 2
#     b3 = "br00116"
#     b4 = "br00044"
#     e1_tag3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_tag4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_tag_rows = [e1_tag3, e1_tag4]
#     e1_tag_df = DataFrame(e1_tag_rows, columns=tag_file_columns)
#     assert len(gen_tag_df) == len(e1_tag_df)
#     print(f"{gen_tag_df.to_csv()=}")
#     print(f" {e1_tag_df.to_csv()=}")
#     assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)

#     road_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     b3 = "br00117"
#     b4 = "br00045"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road_rows = [e1_road3, e1_road4]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
