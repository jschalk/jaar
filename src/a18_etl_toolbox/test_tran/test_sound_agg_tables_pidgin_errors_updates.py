from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic.pidgin import (
    default_bridge_if_None,
    default_unknown_term_if_None,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_label_str,
    pidgin_way_str,
    pidgin_name_str,
    pidgin_title_str,
    pidgin_core_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_label_str,
    otx_label_str,
    inx_way_str,
    otx_way_str,
    inx_name_str,
    otx_name_str,
    inx_title_str,
    otx_title_str,
    unknown_term_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
    CREATE_PIDLABE_SOUND_AGG_SQLSTR,
    CREATE_PIDWAYY_SOUND_AGG_SQLSTR,
    CREATE_PIDNAME_SOUND_AGG_SQLSTR,
    CREATE_PIDTITL_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_RAW_SQLSTR,
    CREATE_PIDCORE_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_update_pidgin_sound_agg_inconsist_sqlstr,
    create_update_pidlabe_sound_agg_bridge_error_sqlstr,
    create_update_pidwayy_sound_agg_bridge_error_sqlstr,
    create_update_pidname_sound_agg_bridge_error_sqlstr,
    create_update_pidtitl_sound_agg_bridge_error_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    insert_pidgin_sound_agg_into_pidgin_core_raw_table,
    insert_pidgin_core_agg_to_pidgin_core_vld_table,
    update_inconsistency_pidgin_core_raw_table,
    insert_pidgin_core_raw_to_pidgin_core_agg_table,
    update_pidgin_sound_agg_inconsist_errors,
    update_pidgin_sound_agg_bridge_errors,
    insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table,
    etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables,
)
from sqlite3 import connect as sqlite3_connect


# def test_create_insert_into_pidgin_core_raw_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
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
#         cursor.execute(CREATE_PIDWAYY_SOUND_AGG_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
#         pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
#         assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 0

#         # WHEN
#         sqlstr = create_insert_into_pidgin_core_raw_sqlstr(pidwayy_dimen)
#         print(f"{sqlstr=}")
#         cursor.execute(sqlstr)

#         # THEN
#         assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 3
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         assert cursor.fetchall() == [
#             (pidgin_way_s_agg_tablename, "Sue", None, None, None, None),
#             (pidgin_way_s_agg_tablename, "Sue", ":", ":", "Unknown", None),
#             (pidgin_way_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
#         ]


# def test_insert_pidgin_sound_agg_into_pidgin_core_raw_table_PopulatesTable_Scenario0():
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
#         cursor.execute(CREATE_PIDWAYY_SOUND_AGG_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event7}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")

#         cursor.execute(CREATE_PIDNAME_SOUND_AGG_SQLSTR)
#         pidname_dimen = pidgin_name_str()
#         pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_name_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_name_str()}
# , {inx_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")

#         create_sound_and_voice_tables(cursor)
#         pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
#         assert get_row_count(cursor, pidgin_way_s_agg_tablename) == 3
#         assert get_row_count(cursor, pidgin_name_s_agg_tablename) == 2
#         assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 0

#         # WHEN
#         insert_pidgin_sound_agg_into_pidgin_core_raw_table(cursor)

#         # THEN
#         assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 4
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         assert rows == [
#             (pidgin_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
#             (pidgin_name_s_agg_tablename, "Sue", None, None, None, None),
#             (pidgin_way_s_agg_tablename, "Sue", None, None, None, None),
#             (pidgin_way_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
#         ]


# def test_update_inconsistency_pidgin_core_raw_table_UpdatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         pidname_dimen = pidgin_name_str()
#         pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
#         pidcore_dimen = pidgin_core_str()
#         pidgin_core_s_raw_tablename = create_prime_tablename(pidcore_dimen, "s", "raw")
#         insert_into_clause = f"""INSERT INTO {pidgin_core_s_raw_tablename} (
#   source_dimen
# , {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# , error_message
# )"""
#         values_clause = f"""
# VALUES
#   ('{pidgin_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
# , ('{pidgin_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', NULL)
# , ('{pidgin_way_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_bridge}', NULL)
# , ('{pidgin_way_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")

#         create_sound_and_voice_tables(cursor)
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_core_s_raw_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         update_inconsistency_pidgin_core_raw_table(cursor)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 2
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         error_message = "Inconsistent data"
#         assert rows == [
#             (pidgin_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
#             (pidgin_name_s_agg_tablename, "Sue", None, None, ":", error_message),
#             (pidgin_way_s_agg_tablename, "Sue", None, None, "/", error_message),
#             (pidgin_way_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
#         ]


# def test_insert_pidgin_core_raw_to_pidgin_core_agg_table_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     error_message = "Inconsistent data"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         pidname_dimen = pidgin_name_str()
#         pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
#         pidcore_dimen = pidgin_core_str()
#         pidgin_core_s_raw_tablename = create_prime_tablename(pidcore_dimen, "s", "raw")
#         insert_into_clause = f"""INSERT INTO {pidgin_core_s_raw_tablename} (
#   source_dimen
# , {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# , error_message
# )"""
#         values_clause = f"""
# VALUES
#   ('{pidgin_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
# , ('{pidgin_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', '{error_message}')
# , ('{pidgin_way_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_bridge}', '{error_message}')
# , ('{pidgin_way_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")

#         create_sound_and_voice_tables(cursor)
#         pidgin_core_s_agg_tablename = create_prime_tablename(pidcore_dimen, "s", "agg")
#         assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 0

#         # WHEN
#         insert_pidgin_core_raw_to_pidgin_core_agg_table(cursor)

#         # THEN
#         assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 2
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         assert rows == [(bob_str, rdx, rdx, ukx), (yao_str, rdx, rdx, ukx)]


# def test_insert_pidgin_core_agg_to_pidgin_core_vld_table_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "zia"
#     colon_bridge = ":"
#     slash_bridge = "/"
#     other_bridge = "="
#     unknown_str = "Unknown"
#     huh_str = "Huh"
#     default_bridge = default_bridge_if_None()
#     default_unknown = default_unknown_term_if_None()

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDCORE_SOUND_AGG_SQLSTR)
#         pidcore_dimen = pidgin_core_str()
#         pidgin_core_s_agg_tablename = create_prime_tablename(pidcore_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_core_s_agg_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ("{bob_str}", "{colon_bridge}", "{slash_bridge}", "{unknown_str}")
# , ("{sue_str}", NULL, NULL, NULL)
# , ("{yao_str}", NULL, '{colon_bridge}', '{huh_str}')
# , ("{zia_str}", "{colon_bridge}", "{colon_bridge}", "{huh_str}")
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename(pidcore_dimen, "s", "vld")
#         assert get_row_count(cursor, pidgin_core_s_vld_tablename) == 0

#         # WHEN
#         insert_pidgin_core_agg_to_pidgin_core_vld_table(cursor)

#         # THEN
#         assert get_row_count(cursor, pidgin_core_s_vld_tablename) == 4
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_vld_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         assert rows == [
#             (bob_str, colon_bridge, slash_bridge, unknown_str),
#             (sue_str, default_bridge, default_bridge, default_unknown),
#             (yao_str, default_bridge, colon_bridge, huh_str),
#             (zia_str, colon_bridge, colon_bridge, huh_str),
#         ]


# def test_create_update_pidgin_sound_agg_inconsist_sqlstr_PopulatesTable_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     error_message = "Inconsistent pidgin core data"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDWAYY_SOUND_AGG_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         print(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_into_clause = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_way_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         sqlstr = create_update_pidgin_sound_agg_inconsist_sqlstr(pidwayy_dimen)
#         print(f"{sqlstr=}")
#         cursor.execute(sqlstr)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_way_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (1, sue_str, yao_str, yao_inx, None, None, None, error_message),
#             (1, sue_str, bob_str, bob_inx, None, None, None, error_message),
#             (1, sue_str, bob_str, bob_str, None, "/", None, error_message),
#             (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_message),
#             (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_message),
#             (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
#         ]


# def test_update_pidgin_sound_agg_inconsist_errors_PopulatesTable_Scenario1():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     error_message = "Inconsistent pidgin core data"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_into_clause = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_way_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         update_pidgin_sound_agg_inconsist_errors(cursor)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
#         select_core_raw_sqlstr = f"SELECT * FROM {pidgin_way_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (1, sue_str, yao_str, yao_inx, None, None, None, error_message),
#             (1, sue_str, bob_str, bob_inx, None, None, None, error_message),
#             (1, sue_str, bob_str, bob_str, None, "/", None, error_message),
#             (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_message),
#             (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_message),
#             (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
#         ]


# def test_create_update_pidlabe_sound_agg_bridge_error_sqlstr_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     yao_str = "Yao"
#     ski_str = "Ski"
#     run_str = "Run"
#     fly_str = "Fly"
#     fly_inx = "fli"
#     ski_inx = "Skiito"
#     rdx = ":"
#     run_rdx_run = f"{run_str}{rdx}{run_str}"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     event9 = 9
#     error_message = "Bridge cannot exist in LabelStr"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDLABE_SOUND_AGG_SQLSTR)
#         pidlabe_dimen = pidgin_label_str()
#         pidlabe_s_agg_tablename = create_prime_tablename(pidlabe_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidlabe_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_label_str()}
# , {inx_label_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{bob_str}', '{fly_str}', '{fly_inx}')
# , ({event1}, '{bob_str}', '{ski_str}{rdx}', '{ski_str}')
# , ({event2}, '{bob_str}', '{run_rdx_run}', '{run_str}')
# , ({event5}, '{yao_str}', '{ski_str}', '{ski_inx}{rdx}')
# , ({event7}, '{yao_str}', '{fly_str}', '{fly_inx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )
# VALUES
#   ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
# , ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(insert_sqlstr)
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidlabe_s_agg_tablename} WHERE error_message IS NOT NULL;"

#         testing_select_sqlstr = """
#   SELECT label_agg.rowid, label_agg.otx_label, label_agg.inx_label, *
#   FROM pidgin_label_s_agg label_agg
#   JOIN pidgin_core_s_vld core_vld ON core_vld.face_name = label_agg.face_name
#   WHERE label_agg.otx_label LIKE '%' || core_vld.otx_bridge || '%'
#       OR label_agg.inx_label LIKE '%' || core_vld.inx_bridge || '%'
# """
#         print(cursor.execute(testing_select_sqlstr).fetchall())

#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         sqlstr = create_update_pidlabe_sound_agg_bridge_error_sqlstr()
#         print(sqlstr)
#         cursor.execute(sqlstr)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
#         select_core_raw_sqlstr = f"SELECT * FROM {pidlabe_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         error_x = error_message
#         exp_row0 = (1, bob_str, fly_str, fly_inx, None, None, None, None)
#         exp_row1 = (1, bob_str, f"{ski_str}{rdx}", ski_str, None, None, None, error_x)
#         exp_row2 = (2, bob_str, run_rdx_run, run_str, None, None, None, error_x)
#         exp_row3 = (5, yao_str, ski_str, f"{ski_inx}{rdx}", None, None, None, error_x)
#         exp_row4 = (7, yao_str, fly_str, fly_inx, None, None, None, None)
#         assert rows[0] == exp_row0
#         assert rows[1] == exp_row1
#         assert rows[2] == exp_row2
#         assert rows[3] == exp_row3
#         assert rows[4] == exp_row4
#         assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


# def test_create_update_pidwayy_sound_agg_bridge_error_sqlstr_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     yao_str = "Yao"
#     rdx = ":"
#     ski_str = f"{rdx}Ski"
#     spt_run_str = f"{rdx}sports{rdx}Run"
#     spt_fly_str = f"{rdx}sports{rdx}Fly"
#     bad_fly_str = f"sports{rdx}fli"
#     bad_ski_str = "Skiito"
#     bad_run_str = f"run{rdx}run"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     event9 = 9
#     error_message = "Bridge must exist in WayStr"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDWAYY_SOUND_AGG_SQLSTR)
#         pidwayy_dimen = pidgin_way_str()
#         pidwayy_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidwayy_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{bob_str}', '{spt_run_str}', '{spt_run_str}')
# , ({event1}, '{bob_str}', '{spt_fly_str}', '{bad_fly_str}')
# , ({event2}, '{bob_str}', '{bad_fly_str}', '{spt_fly_str}')
# , ({event5}, '{yao_str}', '{bad_ski_str}', '{bad_ski_str}')
# , ({event7}, '{yao_str}', '{spt_run_str}', '{bad_run_str}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )
# VALUES
#   ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
# , ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(insert_sqlstr)
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidwayy_s_agg_tablename} WHERE error_message IS NOT NULL;"

#         testing_select_sqlstr = """
#   SELECT way_agg.rowid, way_agg.otx_way, way_agg.inx_way
#   FROM pidgin_way_s_agg way_agg
#   JOIN pidgin_core_s_vld core_vld ON core_vld.face_name = way_agg.face_name
#   WHERE NOT way_agg.otx_way LIKE core_vld.otx_bridge || '%'
#      OR NOT way_agg.inx_way LIKE core_vld.inx_bridge || '%'
#   """

#         print(cursor.execute(testing_select_sqlstr).fetchall())

#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         sqlstr = create_update_pidwayy_sound_agg_bridge_error_sqlstr()
#         print(sqlstr)
#         cursor.execute(sqlstr)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
#         select_core_raw_sqlstr = f"SELECT * FROM {pidwayy_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         error_x = error_message
#         exp_row0 = (1, bob_str, spt_run_str, spt_run_str, None, None, None, None)
#         exp_row1 = (1, bob_str, spt_fly_str, bad_fly_str, None, None, None, error_x)
#         exp_row2 = (2, bob_str, bad_fly_str, spt_fly_str, None, None, None, error_x)
#         exp_row3 = (5, yao_str, bad_ski_str, bad_ski_str, None, None, None, error_x)
#         exp_row4 = (7, yao_str, spt_run_str, bad_run_str, None, None, None, error_x)
#         assert rows[0] == exp_row0
#         assert rows[1] == exp_row1
#         assert rows[2] == exp_row2
#         assert rows[3] == exp_row3
#         assert rows[4] == exp_row4
#         assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


# def test_create_update_pidname_sound_agg_bridge_error_sqlstr_PopulatesTable_Scenario0():
#     # ESTABLISH
#     rdx = ":"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     sue_otx = "Sue"
#     sue_inx = "Susy"
#     bad_sue_inx = f"Susy{rdx}"
#     zia_otx = "Zia"
#     bad_zia_otx = f"{rdx}Zia"
#     zia_inx = "Ziaita"
#     bad_zia_inx = f"Zia{rdx}"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     event9 = 9
#     error_message = "Bridge cannot exist in NameStr"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDNAME_SOUND_AGG_SQLSTR)
#         pidname_dimen = pidgin_name_str()
#         pidname_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidname_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_name_str()}
# , {inx_name_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
# , ({event1}, '{bob_str}', '{sue_otx}', '{bad_sue_inx}')
# , ({event2}, '{bob_str}', '{zia_otx}', '{bad_zia_inx}')
# , ({event5}, '{yao_str}', '{bad_zia_otx}', '{bad_zia_inx}')
# , ({event7}, '{yao_str}', '{bad_zia_otx}', '{zia_inx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )
# VALUES
#   ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
# , ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# ;
# """
#         cursor.execute(insert_sqlstr)
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidname_s_agg_tablename} WHERE error_message IS NOT NULL;"

#         testing_select_sqlstr = """
#   SELECT name_agg.rowid, name_agg.otx_name, name_agg.inx_name
#   FROM pidgin_name_s_agg name_agg
#   JOIN pidgin_core_s_vld core_vld ON core_vld.face_name = name_agg.face_name
#   WHERE NOT name_agg.otx_name LIKE core_vld.otx_bridge || '%'
#      OR NOT name_agg.inx_name LIKE core_vld.inx_bridge || '%'
#   """

#         print(cursor.execute(testing_select_sqlstr).fetchall())

#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         sqlstr = create_update_pidname_sound_agg_bridge_error_sqlstr()
#         print(sqlstr)
#         cursor.execute(sqlstr)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
#         select_core_raw_sqlstr = f"SELECT * FROM {pidname_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         error_x = error_message
#         exp_row0 = (1, bob_str, sue_otx, sue_inx, None, None, None, None)
#         exp_row1 = (1, bob_str, sue_otx, bad_sue_inx, None, None, None, error_x)
#         exp_row2 = (2, bob_str, zia_otx, bad_zia_inx, None, None, None, error_x)
#         exp_row3 = (5, yao_str, bad_zia_otx, bad_zia_inx, None, None, None, error_x)
#         exp_row4 = (7, yao_str, bad_zia_otx, zia_inx, None, None, None, error_x)
#         assert rows[0] == exp_row0
#         assert rows[1] == exp_row1
#         assert rows[2] == exp_row2
#         assert rows[3] == exp_row3
#         assert rows[4] == exp_row4
#         assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


# def test_create_update_pidtitl_sound_agg_bridge_error_sqlstr_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     yao_str = "Yao"
#     rdx_inx = ":"
#     rdx_otx = "<"
#     sue_inx = "Sue"
#     sue_otx = "Suzy"
#     bad_sue_otx = f"{rdx_otx}Suzy"
#     swim_inx = f"{rdx_inx}swimmers"
#     swim_otx = f"{rdx_otx}swimmers"
#     bad_swim_otx = "swimmers"
#     bad_swim_inx = "swimmers"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     event9 = 9
#     error_message = "Otx and inx titles must match bridge property."

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDTITL_SOUND_AGG_SQLSTR)
#         pidtitl_dimen = pidgin_title_str()
#         pidtitl_s_agg_tablename = create_prime_tablename(pidtitl_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidtitl_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_title_str()}
# , {inx_title_str()}
# )"""
#         # TODO create values where errors will appear: groups should map to groups,
#         values_clause = f"""
# VALUES
#   ({event1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
# , ({event1}, '{yao_str}', '{bad_sue_otx}', '{sue_inx}')
# , ({event2}, '{bob_str}', '{swim_otx}', '{swim_inx}')
# , ({event5}, '{yao_str}', '{swim_otx}', '{bad_swim_inx}')
# , ({event7}, '{yao_str}', '{bad_swim_otx}', '{swim_inx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (
#   {face_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )
# VALUES
#   ('{bob_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
# , ('{yao_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
# ;
# """
#         cursor.execute(insert_sqlstr)
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidtitl_s_agg_tablename} WHERE error_message IS NOT NULL;"

#         testing_select_sqlstr = """
#   SELECT title_agg.rowid, title_agg.otx_title, title_agg.inx_title
#   FROM pidgin_title_s_agg title_agg
#   JOIN pidgin_core_s_vld core_vld ON core_vld.face_name = title_agg.face_name
#   WHERE NOT ((
#             title_agg.otx_title LIKE core_vld.otx_bridge || '%'
#         AND title_agg.inx_title LIKE core_vld.inx_bridge || '%')
#       OR (
#             NOT title_agg.otx_title LIKE core_vld.otx_bridge || '%'
#         AND NOT title_agg.inx_title LIKE core_vld.inx_bridge || '%'
#         ))
#         """

#         print(cursor.execute(testing_select_sqlstr).fetchall())

#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         sqlstr = create_update_pidtitl_sound_agg_bridge_error_sqlstr()
#         print(sqlstr)
#         cursor.execute(sqlstr)

#         # THEN
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
#         select_core_raw_sqlstr = f"SELECT * FROM {pidtitl_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         error_x = error_message
#         exp_row0 = (1, bob_str, sue_otx, sue_inx, None, None, None, None)
#         exp_row1 = (1, yao_str, bad_sue_otx, sue_inx, None, None, None, error_x)
#         exp_row2 = (2, bob_str, swim_otx, swim_inx, None, None, None, None)
#         exp_row3 = (5, yao_str, swim_otx, bad_swim_inx, None, None, None, error_x)
#         exp_row4 = (7, yao_str, bad_swim_otx, swim_inx, None, None, None, error_x)
#         assert rows[0] == exp_row0
#         assert rows[1] == exp_row1
#         print(f" {rows[2]=}")
#         print(f"{exp_row2=}")
#         assert rows[2] == exp_row2
#         assert rows[3] == exp_row3
#         assert rows[4] == exp_row4
#         assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


# def test_update_pidgin_sound_agg_bridge_errors_UpdatesTables_Scenario0():
#     # ESTABLISH
#     bob_str = "bob"
#     casa_str = "Casa"
#     rdx = ":"
#     ukx = "Unknown"
#     sue_inx = "Sue"
#     bad_sue_otx = f"{rdx}Suzy"
#     event1 = 1

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_PIDLABE_SOUND_AGG_SQLSTR)
#         cursor.execute(CREATE_PIDWAYY_SOUND_AGG_SQLSTR)
#         cursor.execute(CREATE_PIDNAME_SOUND_AGG_SQLSTR)
#         cursor.execute(CREATE_PIDTITL_SOUND_AGG_SQLSTR)
#         pidlabe_s_agg_tablename = create_prime_tablename(pidgin_label_str(), "s", "agg")
#         pidwayy_s_agg_tablename = create_prime_tablename(pidgin_way_str(), "s", "agg")
#         pidname_s_agg_tablename = create_prime_tablename(pidgin_name_str(), "s", "agg")
#         pidtitl_s_agg_tablename = create_prime_tablename(pidgin_title_str(), "s", "agg")
#         insert_pidlabe_sqlstr = f"""
# INSERT INTO {pidlabe_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         insert_pidwayy_sqlstr = f"""
# INSERT INTO {pidwayy_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_way_str()}, {inx_way_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         insert_pidname_sqlstr = f"""
# INSERT INTO {pidname_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         insert_pidtitl_sqlstr = f"""
# INSERT INTO {pidtitl_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_title_str()}, {inx_title_str()})
# VALUES ({event1}, '{bob_str}', '{bad_sue_otx}', '{sue_inx}');"""
#         cursor.execute(insert_pidlabe_sqlstr)
#         cursor.execute(insert_pidwayy_sqlstr)
#         cursor.execute(insert_pidname_sqlstr)
#         cursor.execute(insert_pidtitl_sqlstr)

#         pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
#         insert_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
# {face_name_str()}, {otx_bridge_str()}, {inx_bridge_str()}, {unknown_term_str()})
# VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
#         cursor.execute(insert_sqlstr)
#         pidlabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidlabe_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         pidwayy_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidwayy_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         pidname_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidname_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         pidtitl_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidtitl_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(pidlabe_error_count_sqlstr).fetchone()[0] == 0
#         assert cursor.execute(pidwayy_error_count_sqlstr).fetchone()[0] == 0
#         assert cursor.execute(pidname_error_count_sqlstr).fetchone()[0] == 0
#         assert cursor.execute(pidtitl_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         update_pidgin_sound_agg_bridge_errors(cursor)

#         # THEN
#         assert cursor.execute(pidlabe_error_count_sqlstr).fetchone()[0] == 1
#         assert cursor.execute(pidwayy_error_count_sqlstr).fetchone()[0] == 1
#         assert cursor.execute(pidname_error_count_sqlstr).fetchone()[0] == 1
#         assert cursor.execute(pidtitl_error_count_sqlstr).fetchone()[0] == 1
#         assert get_row_count(cursor, pidtitl_s_agg_tablename) == 1
#         select_core_raw_sqlstr = f"SELECT {event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()} FROM {pidlabe_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
#         assert rows[0] == exp_row0
#         assert rows == [exp_row0]


# def test_create_insert_pidgin_sound_vld_table_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     error_message = "Inconsistent pidgin core data"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# , error_message
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_message}')
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_message}')
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL, '{error_message}')
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
# , ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
# , ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         pidgin_way_s_vld_tablename = create_prime_tablename("pidwayy", "s", "vld")
#         assert get_row_count(cursor, pidgin_way_s_agg_tablename) == 8
#         assert get_row_count(cursor, pidgin_way_s_vld_tablename) == 0

#         # WHEN
#         sqlstr = create_insert_pidgin_sound_vld_table_sqlstr(pidwayy_dimen)
#         print(sqlstr)
#         cursor.execute(sqlstr)

#         # THEN
#         assert get_row_count(cursor, pidgin_way_s_vld_tablename) == 3
#         select_pidgin_way_s_vld_sqlstr = f"SELECT * FROM {pidgin_way_s_vld_tablename}"
#         cursor.execute(select_pidgin_way_s_vld_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (event1, yao_str, yao_str, yao_str),
#             (event7, bob_str, bob_str, bob_inx),
#             (event7, yao_str, yao_str, yao_inx),
#         ]


# def test_insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table_PopulatesTable_Scenario0():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     error_message = "Inconsistent pidgin core data"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidwayy_dimen = pidgin_way_str()
#         pidgin_way_s_agg_tablename = create_prime_tablename(pidwayy_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_way_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_way_str()}
# , {inx_way_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# , error_message
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_message}')
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_message}')
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL, '{error_message}')
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
# , ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
# , ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         pidgin_way_s_vld_tablename = create_prime_tablename("pidwayy", "s", "vld")
#         assert get_row_count(cursor, pidgin_way_s_agg_tablename) == 8
#         assert get_row_count(cursor, pidgin_way_s_vld_tablename) == 0

#         # WHEN
#         insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table(cursor)

#         # THEN
#         assert get_row_count(cursor, pidgin_way_s_vld_tablename) == 3
#         select_pidgin_way_s_vld_sqlstr = f"SELECT * FROM {pidgin_way_s_vld_tablename}"
#         cursor.execute(select_pidgin_way_s_vld_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (event1, yao_str, yao_str, yao_str),
#             (event7, bob_str, bob_str, bob_inx),
#             (event7, yao_str, yao_str, yao_inx),
#         ]


# def test_etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables_Scenario0_PopulatesTable():
#     # ESTABLISH
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     other_bridge = "/"
#     ukx = "Unknown"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidname_dimen = pidgin_name_str()
#         pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
#         insert_into_clause = f"""INSERT INTO {pidgin_name_s_agg_tablename} (
#   {event_int_str()}
# , {face_name_str()}
# , {otx_name_str()}
# , {inx_name_str()}
# , {otx_bridge_str()}
# , {inx_bridge_str()}
# , {unknown_term_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
# , ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
# , ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
# , ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
# , ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}')
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', NULL)
# , ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
# , ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
# , ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         insert_pidgin_sound_agg_into_pidgin_core_raw_table(cursor)
#         pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
#         pidgin_core_s_agg_tablename = create_prime_tablename("pidcore", "s", "agg")
#         pidgin_name_s_vld_tablename = create_prime_tablename("pidname", "s", "vld")
#         assert get_row_count(cursor, pidgin_name_s_agg_tablename) == 10
#         select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_name_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0
#         assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 6
#         assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 0
#         assert get_row_count(cursor, pidgin_name_s_vld_tablename) == 0

#         # WHEN
#         etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor)

#         # THEN
#         pidgin_name_s_agg_select = f"SELECT * FROM {pidgin_name_s_agg_tablename};"
#         print(f"{cursor.execute(pidgin_name_s_agg_select).fetchall()=}\n")
#         pidgin_core_s_raw_select = f"SELECT * FROM {pidgin_core_s_raw_tablename};"
#         print(f"{cursor.execute(pidgin_core_s_raw_select).fetchall()=}\n")
#         pidgin_core_s_agg_select = f"SELECT * FROM {pidgin_core_s_agg_tablename};"
#         print(f"{cursor.execute(pidgin_core_s_agg_select).fetchall()=}\n")
#         assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
#         assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 2
#         assert get_row_count(cursor, pidgin_name_s_vld_tablename) == 3
#         select_pidgin_name_s_vld_sqlstr = f"SELECT * FROM {pidgin_name_s_vld_tablename}"
#         cursor.execute(select_pidgin_name_s_vld_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (event1, yao_str, yao_str, yao_str),
#             (event7, bob_str, bob_str, bob_inx),
#             (event7, yao_str, yao_str, yao_inx),
#         ]


# def test_etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables_Scenario1_UpdatesErrors():
#     # ESTABLISH
#     bob_str = "bob"
#     casa_str = "Casa"
#     mop_str = "Mop"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     casa_inx = "Casaito"
#     rdx = ":"
#     mop_rdx_mop = f"{mop_str}{rdx}{mop_str}"
#     ukx = "Unknown"
#     event1 = 1
#     error_message = "Bridge cannot exist in LabelStr"

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidlabe_s_agg_tablename = create_prime_tablename(pidgin_label_str(), "s", "agg")
#         pidwayy_s_agg_tablename = create_prime_tablename(pidgin_way_str(), "s", "agg")
#         pidname_s_agg_tablename = create_prime_tablename(pidgin_name_str(), "s", "agg")
#         insert_pidlabe_sqlstr = f"""
# INSERT INTO {pidlabe_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         insert_pidwayy_sqlstr = f"""
# INSERT INTO {pidwayy_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_way_str()}, {inx_way_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         insert_pidname_sqlstr = f"""
# INSERT INTO {pidname_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
# VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
#         cursor.execute(insert_pidlabe_sqlstr)
#         cursor.execute(insert_pidwayy_sqlstr)
#         cursor.execute(insert_pidname_sqlstr)

#         pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
#         insert_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
# {face_name_str()}, {otx_bridge_str()}, {inx_bridge_str()}, {unknown_term_str()})
# VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
#         cursor.execute(insert_sqlstr)
#         pidlabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidlabe_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         pidwayy_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidwayy_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         pidname_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidname_s_agg_tablename} WHERE error_message IS NOT NULL;"
#         assert cursor.execute(pidlabe_error_count_sqlstr).fetchone()[0] == 0
#         assert cursor.execute(pidwayy_error_count_sqlstr).fetchone()[0] == 0
#         assert cursor.execute(pidname_error_count_sqlstr).fetchone()[0] == 0

#         # WHEN
#         etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor)

#         # THEN
#         assert cursor.execute(pidlabe_error_count_sqlstr).fetchone()[0] == 1
#         assert cursor.execute(pidwayy_error_count_sqlstr).fetchone()[0] == 1
#         assert cursor.execute(pidname_error_count_sqlstr).fetchone()[0] == 1
#         select_core_raw_sqlstr = f"SELECT {event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()} FROM {pidlabe_s_agg_tablename}"
#         cursor.execute(select_core_raw_sqlstr)
#         rows = cursor.fetchall()
#         exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
#         assert rows[0] == exp_row0
#         assert rows == [exp_row0]
