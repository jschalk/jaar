from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_config import get_idea_sqlite_types
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a17_idea_logic._utils.str_a17 import brick_valid_str, sound_raw_str
from src.a18_etl_toolbox.transformers import etl_brick_valid_tables_to_sound_raw_tables
from sqlite3 import connect as sqlite3_connect

# get examples from tests for etl_brick_agg_dfs_to_pidgin_label_raw
# get examples from tests for etl_brick_agg_dfs_to_pidgin_road_raw
# get examples from tests for etl_brick_agg_dfs_to_pidgin__raw
# get examples from tests for etl_brick_agg_dfs_to_pidgin_road_raw


# def test_etl_brick_valid_tables_to_sound_raw_tables_PopulatesValidTable_Scenario0_Only_valid_events():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     event7 = 7
#     br00117_agg_tablename = f"br00003_{brick_valid_str()}"
#     br00117_columns = [
#         event_int_str(),
#         face_name_str(),
#         fisc_tag_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_idea_sorted_table(cursor, br00117_agg_tablename, br00117_columns)
#         insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {fisc_tag_str()}
# , {cumlative_minute_str()}
# , {hour_tag_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{a23_str}', '{minute_360}', '{hour6am}')
# , ({event3}, '{sue_str}', '{a23_str}', '{minute_420}', '{hour8am}')
# , ({event6}, '{sue_str}', '{a23_str}', '{minute_420}', '{hour8am}')
# ;
# """
#         insert_sqlstr = f"{insert_into_clause} {values_clause}"
#         cursor.execute(insert_sqlstr)
#         assert get_row_count(cursor, agg_br00003_tablename) == 3

#         valid_events_columns = [face_name_str(), event_int_str()]
#         valid_events_tablename = "events_brick_valid"
#         create_idea_sorted_table(cursor, valid_events_tablename, valid_events_columns)
#         insert_into_valid_events = f"""
# INSERT INTO {valid_events_tablename} ({event_int_str()}, {face_name_str()})
# VALUES
#   ({event1}, '{sue_str}')
# , ({event6}, '{sue_str}')
# ;
# """
#         cursor.execute(insert_into_valid_events)
#         assert get_row_count(cursor, valid_events_tablename) == 2

#         valid_br00003_tablename = f"br00003_{brick_valid_str()}"
#         assert not db_table_exists(cursor, valid_br00003_tablename)

#         # WHEN
#         etl_brick_valid_tables_to_sound_raw_tables(cursor)

#         # THEN
#         assert db_table_exists(cursor, valid_br00003_tablename)
#         assert get_table_columns(cursor, valid_br00003_tablename) == agg_br00003_columns
#         assert get_row_count(cursor, valid_br00003_tablename) == 2
#         select_agg_sqlstr = f"""SELECT * FROM {valid_br00003_tablename};"""
#         cursor.execute(select_agg_sqlstr)

#         rows = cursor.fetchall()
#         assert len(rows) == 2
#         row0 = (event1, sue_str, a23_str, minute_360, hour6am)
#         row1 = (event6, sue_str, a23_str, minute_420, hour8am)
#         assert rows[0] == row0
#         assert rows[1] == row1
