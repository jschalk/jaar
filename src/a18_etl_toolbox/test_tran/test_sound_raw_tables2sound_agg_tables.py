# from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
# from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
# from src.a06_bud_logic._utils.str_a06 import (
#     face_name_str,
#     acct_name_str,
#     event_int_str,
#     credit_belief_str,
#     debtit_belief_str,
# )
# from src.a16_pidgin_logic._utils.str_a16 import (
#     inx_bridge_str,
#     otx_bridge_str,
#     inx_road_str,
#     otx_road_str,
#     unknown_word_str,
# )
# from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
# from src.a17_idea_logic._utils.str_a17 import (
#     brick_valid_str,
#     idea_number_str,
# )
# from src.a18_etl_toolbox.tran_sqlstrs import (
#     create_prime_tablename,
#     create_sound_and_voice_tables,
#     CREATE_PIDROAD_SOUND_RAW_SQLSTR,
#     CREATE_PIDROAD_SOUND_AGG_SQLSTR,
#     CREATE_BUDACCT_SOUND_PUT_RAW_STR,
#     CREATE_BUDACCT_SOUND_PUT_AGG_STR,
# )
# from src.a18_etl_toolbox.transformers import etl_sound_raw_tables_to_sound_agg_tables
# from sqlite3 import connect as sqlite3_connect


# def test_etl_sound_raw_tables_to_sound_agg_tables_PopulatesValidTable_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDROAD_SOUND_RAW_SQLSTR)
#         pidroad_s_raw_tablename = create_prime_tablename("PIDROAD", "s", "raw")
#         insert_into_clause = f"""INSERT INTO {pidroad_s_raw_tablename} (
#   {idea_number_str()}
# , {event_int_str()}
# , {face_name_str()}
# , {otx_road_str()}
# , {inx_road_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_word_str()}
# , "error_message"
# )"""
#         b117 = "br00117"
#         b045 = "br00045"
#         values_clause = f"""
# VALUES
# , ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', None, None, None, None)
# , ('{b117}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', None, None, None, None)
# , ('{b045}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', None)
# , ('{b045}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', None)
# , ('{b045}', {event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', None)
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_BUDACCT_SOUND_PUT_RAW_STR)
#         budacct_s_put_raw_tblname = create_prime_tablename("BUDACCT", "s", "raw", "put")
#         insert_into_clause = f"""INSERT INTO {pidroad_s_raw_tablename} (
#   {idea_number_str()}
# , {event_int_str()}
# , {face_name_str()}
# , {fisc_tag_str()}
# , {owner_name_str()}
# , {acct_name_str()}
# , {credit_belief_str()}
# , {debtit_belief_str()}
# , "error_message"
# )"""
#         b117 = "br00117"
#         b045 = "br00045"

#         values_clause = f"""
# VALUES
#   '{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', NULL, NULL, NULL)
# , '{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
# ;
# """
#         cursor.execute(CREATE_PIDROAD_SOUND_AGG_SQLSTR)
#         cursor.execute(CREATE_BUDACCT_SOUND_PUT_AGG_STR)
#         pidroad_s_agg_tablename = create_prime_tablename("PIDROAD", "s", "agg")
#         budacct_s_put_agg_tblname = create_prime_tablename("BUDACCT", "s", "agg", "put")
#         assert get_row_count(cursor, pidroad_s_raw_tablename) == 5
#         assert get_row_count(cursor, budacct_s_put_raw_tblname) == 2
#         assert get_row_count(cursor, pidroad_s_agg_tablename) == 0
#         assert get_row_count(cursor, budacct_s_put_agg_tblname) == 0

#         # WHEN
#         etl_sound_raw_tables_to_sound_agg_tables(cursor)

#         # THEN
#         assert get_row_count(cursor, pidroad_s_agg_tablename) == 3
#         assert get_row_count(cursor, budacct_s_put_agg_tblname) == 3

#         select_agg_sqlstr = f"""SELECT * FROM {pidroad_s_agg_tablename};"""
#         cursor.execute(select_agg_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert len(rows) == 2
#         # TODO identify expected output
#         assert rows == [
#             # (b117, 1, sue_str, a23_str, bob_str, yao_str, None, None, None),
#             # (b117, 1, sue_str, a23_str, bob_str, bob_str, None, None, None),
#         ]

#         select_agg_sqlstr = f"""SELECT * FROM {budacct_s_put_agg_tblname};"""
#         cursor.execute(select_agg_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert len(rows) == 2
#         # TODO identify expected output
#         assert rows == [
#             (b117, 1, sue_str, a23_str, bob_str, yao_str, None, None, None),
#             (b117, 1, sue_str, a23_str, bob_str, bob_str, None, None, None),
#         ]
