from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a01_way_logic.way import create_way
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str, owner_name_str
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    bud_idea_awardlink_str,
    face_name_str,
    event_int_str,
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
    idea_way_str,
    awardee_label_str,
    give_force_str,
    take_force_str,
)
from src.a16_pidgin_logic.pidgin import (
    default_bridge_if_None,
    default_unknown_word_if_None,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_tag_str,
    pidgin_way_str,
    pidgin_name_str,
    pidgin_label_str,
    pidgin_core_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_tag_str,
    otx_tag_str,
    inx_way_str,
    otx_way_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    CREATE_PIDTAGG_SOUND_AGG_SQLSTR,
    CREATE_PIDWAYY_SOUND_AGG_SQLSTR,
    CREATE_PIDNAME_SOUND_VLD_SQLSTR,
    CREATE_PIDLABE_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_RAW_SQLSTR,
    CREATE_PIDCORE_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_update_pidgin_sound_agg_inconsist_sqlstr,
    create_update_pidtagg_sound_agg_bridge_error_sqlstr,
    create_update_pidwayy_sound_agg_bridge_error_sqlstr,
    create_update_pidname_sound_agg_bridge_error_sqlstr,
    create_update_pidlabe_sound_agg_bridge_error_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
    get_insert_into_voice_raw_sqlstrs,
    update_voice_raw_inx_name_col_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    etl_sound_agg_tables_to_voice_raw_tables,
)
from sqlite3 import connect as sqlite3_connect


# TODO create test for mapped_pidgin_events sqlstr (may have already been devloped at OTE1)
# must for be one type example: NameStr, one pidgin_event_int
# TODO create test for mapped_names sqlstr (link otx_)


def test_update_voice_raw_inx_name_col_sqlstr_UpdatesTable_Scenario0_EmptyPidginTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename} ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
VALUES
  ({event1}, '{sue_otx}', NULL)
, ({event2}, '{yao_otx}', NULL)
, ({event5}, '{sue_otx}', NULL)
, ({event7}, '{bob_otx}', NULL)
;
"""
        cursor.execute(insert_face_name_only_sqlstr)
        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = update_voice_raw_inx_name_col_sqlstr(
            budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_otx),
            (2, yao_otx, yao_otx),
            (5, sue_otx, sue_otx),
            (7, bob_otx, bob_otx),
        ]


def test_update_voice_raw_inx_name_col_sqlstr_UpdatesTable_Scenario1_FullPidginTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        # print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename} 
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{sue_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        cursor.execute(CREATE_PIDNAME_SOUND_VLD_SQLSTR)
        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename} 
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = update_voice_raw_inx_name_col_sqlstr(
            budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, yao_otx),
            (5, sue_otx, sue_inx),
            (7, bob_otx, bob_inx),
        ]


# TODO reactivate test
# def test_update_voice_raw_inx_name_col_sqlstr_UpdatesTable_Scenario1_FullPidginTables():
#     # ESTABLISH
#     bob_otx = "Bob"
#     bob_inx = "Bobby"
#     sue_otx = "Sue"
#     sue_inx = "Suzy"
#     yao_otx = "Yao"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         budawar_dimen = bud_idea_awardlink_str()
#         budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
#         # print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
#         insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
#         ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
#         VALUES
#           ({event1}, '{sue_otx}', NULL)
#         , ({event2}, '{yao_otx}', NULL)
#         , ({event5}, '{bob_otx}', NULL)
#         ;
#         """
#         cursor.execute(insert_face_name_only_sqlstr)

#         cursor.execute(CREATE_PIDNAME_SOUND_VLD_SQLSTR)
#         pidname_dimen = pidgin_name_str()
#         pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
#         print(f"{pidname_s_vld_tablename=}")
#         insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
#         ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
#         VALUES
#           ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
#         , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
#         ;
#         """
#         cursor.execute(insert_pidname_sqlstr)

#         face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
#         assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

#         # WHEN
#         update_sqlstr = update_voice_raw_inx_name_col_sqlstr(
#             budawar_v_raw_put_tablename, face_name_str()
#         )
#         print(update_sqlstr)
#         cursor.execute(update_sqlstr)

#         # THEN
#         select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
#         cursor.execute(select_face_name_only_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         # event5 does not link to event7 pidgin record's
#         assert rows == [
#             (event1, sue_otx, sue_inx),
#             (event2, yao_otx, yao_otx),
#             (event5, bob_otx, bob_otx),
#         ]
#         assert 1 == 2


# def test_update_voice_raw_inx_name_col_sqlstr_UpdatesTable_Scenario11_():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_otx = "Bob"
#     bob_inx = "Bobby"
#     sue_otx = "Sue"
#     sue_inx = "Suzy"
#     yao_otx = "Yao"
#     yao_inx = "Yaoito"
#     casa_way_otx = create_way(a23_str, "casa")
#     casa_way_inx = create_way(a23_str, "casita")
#     team_otx = "team12"
#     team_inx = "teamAB"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     x44_give = 44
#     x55_give = 55
#     x22_take = 22
#     x66_take = 66

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         budawar_dimen = bud_idea_awardlink_str()
#         budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
#         print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
#         insert_into_clause = f"""INSERT INTO {budawar_v_raw_put_tablename} (
#   {event_int_str()}
# , {face_name_str()}_otx
# , {face_name_str()}_inx
# , {fisc_tag_str()}_otx
# , {fisc_tag_str()}_inx
# , {owner_name_str()}_otx
# , {owner_name_str()}_inx
# , {idea_way_str()}_otx
# , {idea_way_str()}_inx
# , {awardee_label_str()}_otx
# , {awardee_label_str()}_inx
# , {give_force_str()}
# , {take_force_str()}
# )"""
#         values_clause = f"""
# VALUES
#   ({event1}, '{sue_otx}', NULL, '{a23_str}', NULL,'{yao_otx}', NULL, '{casa_way_otx}', NULL, '{team_otx}', NULL, {x44_give}, {x22_take})
# , ({event2}, '{yao_otx}', NULL, '{a23_str}', NULL,'{bob_otx}', NULL, '{casa_way_otx}', NULL, '{team_otx}', NULL, {x55_give}, {x22_take})
# , ({event5}, '{sue_otx}', NULL, '{a23_str}', NULL,'{bob_otx}', NULL, '{casa_way_otx}', NULL, '{team_otx}', NULL, {x55_give}, {x22_take})
# , ({event7}, '{bob_otx}', NULL, '{a23_str}', NULL,'{bob_otx}', NULL, '{casa_way_otx}', NULL, '{team_otx}', NULL, {x55_give}, {x66_take})
# ;
# """
#         cursor.execute(f"{insert_into_clause} {values_clause}")
#         face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
#         fisc_tag_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {fisc_tag_str()}_inx IS NOT NULL"
#         owner_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {owner_name_str()}_inx IS NOT NULL"
#         idea_way_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {idea_way_str()}_inx IS NOT NULL"
#         awardee_label_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {awardee_label_str()}_inx IS NOT NULL"
#         assert cursor.execute(face_name_inx_count_sql).fetchone() == (0,)
#         assert cursor.execute(owner_name_inx_count_sql).fetchone() == (0,)
#         assert cursor.execute(fisc_tag_inx_count_sql).fetchone() == (0,)
#         assert cursor.execute(idea_way_inx_count_sql).fetchone() == (0,)
#         assert cursor.execute(awardee_label_inx_count_sql).fetchone() == (0,)

#         # WHEN
#         update_sqlstr = update_voice_raw_inx_name_col_sqlstr(
#             budawar_v_raw_put_tablename, face_name_str()
#         )
#         print(update_sqlstr)
#         cursor.execute(update_sqlstr)

#         # THEN
#         assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
#         assert cursor.execute(owner_name_inx_count_sql).fetchone()[0] == 0
#         assert cursor.execute(awardee_label_inx_count_sql).fetchone()[0] == 0
#         assert cursor.execute(fisc_tag_inx_count_sql).fetchone()[0] == 0
#         assert cursor.execute(idea_way_inx_count_sql).fetchone()[0] == 0
#         select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
#         cursor.execute(select_face_name_only_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (1, sue_otx, sue_otx),
#             (2, yao_otx, yao_otx),
#             (5, sue_otx, sue_otx),
#             (7, bob_otx, bob_otx),
#         ]
#         assert 1 == 2
