from src.a00_data_toolbox.db_toolbox import get_table_columns
from src.a01_way_logic.way import create_way
from src.a02_finance_logic._utils.strs_a02 import owner_name_str
from src.a06_bud_logic._utils.str_a06 import (
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
from src.a15_fisc_logic._utils.str_a15 import (
    fisc_timeline_hour_str,
    hour_word_str,
    cumlative_minute_str,
)
from src.a16_pidgin_logic.pidgin import (
    default_bridge_if_None,
    default_unknown_term_if_None,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_word_str,
    pidgin_way_str,
    pidgin_name_str,
    pidgin_label_str,
    pidgin_core_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_word_str,
    otx_word_str,
    inx_way_str,
    otx_way_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    unknown_term_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    create_update_voice_raw_existing_inx_col_sqlstr,
    create_pidname_face_otx_event_sqlstr,
    create_pidlabe_face_otx_event_sqlstr,
    create_pidword_face_otx_event_sqlstr,
    create_pidwayy_face_otx_event_sqlstr,
    create_update_voice_raw_empty_inx_col_sqlstr,
)
from src.a18_etl_toolbox.transformers import set_all_voice_raw_inx_columns
from sqlite3 import connect as sqlite3_connect


# must for be one type example: NameStr, one pidgin_event_int
# TODO create test for mapped_names sqlstr (link otx_)


def test_create_pidlabe_face_otx_event_sqlstr_ReturnsObj_Scenario0_LabelStr():
    # ESTABLISH
    bob_otx = "Bob"
    yao_otx = "Yao"
    zia_otx = "Zia"
    run_otx = ";Runners"
    run_inx = ";Joggers"
    bob_run_inx = ";bobRunnersInx"
    fly_otx = ";flyer"
    fly_inx1 = ";pilots"
    fly_inx7 = ";planedrivers"
    swi_otx = ";swimmers"
    swi_inx = ";paddlers"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {awardee_label_str()}_otx, {awardee_label_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', '{fly_otx}', NULL)
        , ({event1}, '{bob_otx}', '{fly_otx}', NULL)
        , ({event2}, '{yao_otx}', '{swi_otx}', NULL)
        , ({event5}, '{bob_otx}', '{fly_otx}', NULL)
        , ({event7}, '{bob_otx}', '{fly_otx}', NULL)
        , ({event9}, '{bob_otx}', '{fly_otx}', NULL)
        ;
        """
        cursor.execute(insert_sqlstr)

        pidlabe_dimen = pidgin_label_str()
        pidlabe_s_vld_tablename = prime_tbl(pidlabe_dimen, "s", "vld")
        # print(f"{pidlabe_s_vld_tablename=}")
        insert_pidlabe_sqlstr = f"""INSERT INTO {pidlabe_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
        VALUES
          ({event1}, '{bob_otx}', '{fly_otx}', '{fly_inx1}')
        , ({event2}, '{yao_otx}', '{swi_otx}', '{swi_inx}')
        , ({event7}, '{bob_otx}', '{fly_otx}', '{fly_inx7}')
        , ({event7}, '{bob_otx}', '{run_otx}', '{bob_run_inx}')
        , ({event8}, '{zia_otx}', '{run_otx}', '{run_inx}')
        ;
        """
        cursor.execute(insert_pidlabe_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        pidname_face_otx_event_sqlstr = create_pidlabe_face_otx_event_sqlstr(
            budawar_v_raw_put_tablename, awardee_label_str()
        )
        cursor.execute(pidname_face_otx_event_sqlstr)

        # THEN
        static_select_pidlabe_sqlstr = """
SELECT
  raw_dim.rowid raw_rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.awardee_label_otx
, MAX(pid.event_int) pidgin_event_int
FROM bud_idea_awardlink_v_put_raw raw_dim
LEFT JOIN pidgin_label_s_vld pid ON pid.face_name = raw_dim.face_name_otx
    AND pid.otx_label = raw_dim.awardee_label_otx
    AND raw_dim.event_int >= pid.event_int
GROUP BY
  raw_dim.rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.awardee_label_otx
"""

        print(pidname_face_otx_event_sqlstr)
        print("")
        # print(static_select_pidlabe_sqlstr)
        assert static_select_pidlabe_sqlstr == pidname_face_otx_event_sqlstr
        cursor.execute(static_select_pidlabe_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (1, event0, bob_otx, fly_otx, None),
            (2, event1, bob_otx, fly_otx, event1),
            (3, event2, yao_otx, swi_otx, event2),
            (4, event5, bob_otx, fly_otx, event1),
            (5, event7, bob_otx, fly_otx, event7),
            (6, event9, bob_otx, fly_otx, event7),
        ]


def test_create_pidword_face_otx_event_sqlstr_ReturnsObj_Scenario0_WordStr():
    # ESTABLISH
    bob_otx = "Bob"
    yao_otx = "Yao"
    zia_otx = "Zia"
    hr7_otx = "hr7"
    hr7_inx = "Casita"
    bob_hr7_inx = ";bob_hr7Inx"
    hr8_otx = "hr8ts"
    hr8_inx1 = "hr8_v1"
    hr8_inx7 = "hr8_v7"
    hr2_otx = "hr2_v1"
    hr2_inx = "hr2_v2"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        fishour_dimen = fisc_timeline_hour_str()
        fishour_v_raw_tablename = prime_tbl(fishour_dimen, "v", "raw")
        print(f"{get_table_columns(cursor, fishour_v_raw_tablename)=}")
        insert_sqlstr = f"""INSERT INTO {fishour_v_raw_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {hour_word_str()}_otx, {hour_word_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', '{hr8_otx}', NULL)
        , ({event1}, '{bob_otx}', '{hr8_otx}', NULL)
        , ({event2}, '{yao_otx}', '{hr2_otx}', NULL)
        , ({event5}, '{bob_otx}', '{hr8_otx}', NULL)
        , ({event7}, '{bob_otx}', '{hr8_otx}', NULL)
        , ({event9}, '{bob_otx}', '{hr8_otx}', NULL)
        ;
        """
        cursor.execute(insert_sqlstr)

        pidword_dimen = pidgin_word_str()
        pidword_s_vld_tablename = prime_tbl(pidword_dimen, "s", "vld")
        # print(f"{pidword_s_vld_tablename=}")
        insert_pidword_sqlstr = f"""INSERT INTO {pidword_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_word_str()}, {inx_word_str()})
        VALUES
          ({event1}, '{bob_otx}', '{hr8_otx}', '{hr8_inx1}')
        , ({event2}, '{yao_otx}', '{hr2_otx}', '{hr2_inx}')
        , ({event7}, '{bob_otx}', '{hr8_otx}', '{hr8_inx7}')
        , ({event7}, '{bob_otx}', '{hr7_otx}', '{bob_hr7_inx}')
        , ({event8}, '{zia_otx}', '{hr7_otx}', '{hr7_inx}')
        ;
        """
        cursor.execute(insert_pidword_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {fishour_v_raw_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        pidname_face_otx_event_sqlstr = create_pidword_face_otx_event_sqlstr(
            fishour_v_raw_tablename, hour_word_str()
        )
        cursor.execute(pidname_face_otx_event_sqlstr)

        # THEN
        static_select_pidword_sqlstr = """
SELECT
  raw_dim.rowid raw_rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.hour_word_otx
, MAX(pid.event_int) pidgin_event_int
FROM fisc_timeline_hour_v_raw raw_dim
LEFT JOIN pidgin_word_s_vld pid ON pid.face_name = raw_dim.face_name_otx
    AND pid.otx_word = raw_dim.hour_word_otx
    AND raw_dim.event_int >= pid.event_int
GROUP BY
  raw_dim.rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.hour_word_otx
"""

        print(pidname_face_otx_event_sqlstr)
        print("")
        # print(static_select_pidword_sqlstr)
        assert static_select_pidword_sqlstr == pidname_face_otx_event_sqlstr
        cursor.execute(static_select_pidword_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (1, event0, bob_otx, hr8_otx, None),
            (2, event1, bob_otx, hr8_otx, event1),
            (3, event2, yao_otx, hr2_otx, event2),
            (4, event5, bob_otx, hr8_otx, event1),
            (5, event7, bob_otx, hr8_otx, event7),
            (6, event9, bob_otx, hr8_otx, event7),
        ]


def test_create_pidwayy_face_otx_event_sqlstr_ReturnsObj_Scenario0_WayStr():
    # ESTABLISH
    bob_otx = "Bob"
    yao_otx = "Yao"
    zia_otx = "Zia"
    casa_way_otx = create_way("casa")
    clean_way_otx = create_way(casa_way_otx, "clean")
    dirty_way_otx = create_way(casa_way_otx, "dirty")
    casa_way_inx = create_way("casita")
    clean_way_inx1 = create_way(casa_way_inx, "clean1")
    clean_way_inx7 = create_way(casa_way_inx, "clean7")
    dirty_way_inx = create_way(casa_way_inx, "dirty")
    sport_way_otx = create_way("sport")
    bball_way_otx = create_way(sport_way_otx, "bball")
    sport_way_inx = create_way("sport")
    bball_way_inx = create_way(sport_way_otx, "basketball")
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_put_dimen = bud_idea_awardlink_str()
        budawar_put_v_raw_tablename = prime_tbl(budawar_put_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_put_v_raw_tablename)=}")
        insert_sqlstr = f"""INSERT INTO {budawar_put_v_raw_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {idea_way_str()}_otx, {idea_way_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', '{clean_way_otx}', NULL)
        , ({event1}, '{bob_otx}', '{clean_way_otx}', NULL)
        , ({event2}, '{yao_otx}', '{bball_way_otx}', NULL)
        , ({event5}, '{bob_otx}', '{clean_way_otx}', NULL)
        , ({event7}, '{bob_otx}', '{clean_way_otx}', NULL)
        , ({event9}, '{bob_otx}', '{clean_way_otx}', NULL)
        ;
        """
        cursor.execute(insert_sqlstr)

        pidwayy_dimen = pidgin_way_str()
        pidwayy_s_vld_tablename = prime_tbl(pidwayy_dimen, "s", "vld")
        # print(f"{pidwayy_s_vld_tablename=}")
        insert_pidwayy_sqlstr = f"""INSERT INTO {pidwayy_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_way_str()}, {inx_way_str()})
        VALUES
          ({event1}, '{bob_otx}', '{clean_way_otx}', '{clean_way_inx1}')
        , ({event2}, '{yao_otx}', '{bball_way_otx}', '{bball_way_inx}')
        , ({event7}, '{bob_otx}', '{bball_way_otx}', '{bball_way_inx}')
        , ({event7}, '{bob_otx}', '{clean_way_otx}', '{clean_way_inx7}')
        , ({event8}, '{zia_otx}', '{dirty_way_otx}', '{dirty_way_inx}')
        ;
        """
        cursor.execute(insert_pidwayy_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_put_v_raw_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        pidname_face_otx_event_sqlstr = create_pidwayy_face_otx_event_sqlstr(
            budawar_put_v_raw_tablename, idea_way_str()
        )
        cursor.execute(pidname_face_otx_event_sqlstr)

        # THEN
        static_select_pidwayy_sqlstr = """
SELECT
  raw_dim.rowid raw_rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.idea_way_otx
, MAX(pid.event_int) pidgin_event_int
FROM bud_idea_awardlink_v_put_raw raw_dim
LEFT JOIN pidgin_way_s_vld pid ON pid.face_name = raw_dim.face_name_otx
    AND pid.otx_way = raw_dim.idea_way_otx
    AND raw_dim.event_int >= pid.event_int
GROUP BY
  raw_dim.rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.idea_way_otx
"""

        print(pidname_face_otx_event_sqlstr)
        print("")
        # print(static_select_pidwayy_sqlstr)
        assert static_select_pidwayy_sqlstr == pidname_face_otx_event_sqlstr
        cursor.execute(static_select_pidwayy_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (1, event0, bob_otx, clean_way_otx, None),
            (2, event1, bob_otx, clean_way_otx, event1),
            (3, event2, yao_otx, bball_way_otx, event2),
            (4, event5, bob_otx, clean_way_otx, event1),
            (5, event7, bob_otx, clean_way_otx, event7),
            (6, event9, bob_otx, clean_way_otx, event7),
        ]


def test_create_pidname_face_otx_event_sqlstr_ReturnsObj_Scenario2_NameStr():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx1 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        # print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', NULL)
        , ({event1}, '{bob_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        , ({event9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        # print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx1}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        pidname_face_otx_event_sqlstr = create_pidname_face_otx_event_sqlstr(
            budawar_v_raw_put_tablename, face_name_str()
        )
        cursor.execute(pidname_face_otx_event_sqlstr)

        # THEN
        select_pidname_face_otx_event_sqlstr = """
SELECT
  raw_dim.rowid raw_rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.face_name_otx
, MAX(pid.event_int) pidgin_event_int
FROM bud_idea_awardlink_v_put_raw raw_dim
LEFT JOIN pidgin_name_s_vld pid ON pid.face_name = raw_dim.face_name_otx
    AND pid.otx_name = raw_dim.face_name_otx
    AND raw_dim.event_int >= pid.event_int
GROUP BY
  raw_dim.rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.face_name_otx
"""

        # print(pidname_face_otx_event_sqlstr)
        # print("")
        # print(select_pidname_face_otx_event_sqlstr)
        assert select_pidname_face_otx_event_sqlstr == pidname_face_otx_event_sqlstr
        cursor.execute(select_pidname_face_otx_event_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (1, event0, bob_otx, bob_otx, None),
            (2, event1, bob_otx, bob_otx, event1),
            (3, event2, yao_otx, yao_otx, event2),
            (4, event5, bob_otx, bob_otx, event1),
            (5, event7, bob_otx, bob_otx, event7),
            (6, event9, bob_otx, bob_otx, event7),
        ]


def test_create_pidname_face_otx_event_sqlstr_ReturnsObj_Scenario1_SelectsMostRecentPidginEventPerRow():
    # ESTABLISH
    xio_str = "Xio"
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx1 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {owner_name_str()}_otx, {owner_name_str()}_inx)
        VALUES
          ({event0}, '{zia_str}', '{bob_otx}', NULL)
        , ({event1}, '{zia_str}', '{bob_otx}', NULL)
        , ({event2}, '{xio_str}', '{yao_otx}', NULL)
        , ({event5}, '{zia_str}', '{bob_otx}', NULL)
        , ({event7}, '{zia_str}', '{bob_otx}', NULL)
        , ({event9}, '{zia_str}', '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        # print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{zia_str}', '{bob_otx}', '{bob_inx1}')
        , ({event2}, '{xio_str}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{zia_str}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{zia_str}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{zia_str}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        pidname_face_otx_event_sqlstr = create_pidname_face_otx_event_sqlstr(
            budawar_v_raw_put_tablename, owner_name_str()
        )
        cursor.execute(pidname_face_otx_event_sqlstr)

        # THEN
        select_pidname_face_otx_event_sqlstr = """
SELECT
  raw_dim.rowid raw_rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.owner_name_otx
, MAX(pid.event_int) pidgin_event_int
FROM bud_idea_awardlink_v_put_raw raw_dim
LEFT JOIN pidgin_name_s_vld pid ON pid.face_name = raw_dim.face_name_otx
    AND pid.otx_name = raw_dim.owner_name_otx
    AND raw_dim.event_int >= pid.event_int
GROUP BY
  raw_dim.rowid
, raw_dim.event_int
, raw_dim.face_name_otx
, raw_dim.owner_name_otx
"""

        # print(pidname_face_otx_event_sqlstr)
        # print("")
        # print(select_pidname_face_otx_event_sqlstr)
        assert select_pidname_face_otx_event_sqlstr == pidname_face_otx_event_sqlstr
        cursor.execute(select_pidname_face_otx_event_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (1, event0, zia_str, bob_otx, None),
            (2, event1, zia_str, bob_otx, event1),
            (3, event2, xio_str, yao_otx, event2),
            (4, event5, zia_str, bob_otx, event1),
            (5, event7, zia_str, bob_otx, event7),
            (6, event9, zia_str, bob_otx, event7),
        ]


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario0_FullPidginTables():
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
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 3
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, None),
            (5, sue_otx, sue_inx),
            (7, bob_otx, bob_inx),
        ]


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario1_PartialPidginTables():
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
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)
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
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (event1, sue_otx, sue_inx),
            (event2, yao_otx, None),
            (event5, bob_otx, None),
        ]


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario2_Different_event_int_PidginMappings():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', NULL)
        , ({event1}, '{bob_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        , ({event9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (0, bob_otx, None),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]


def test_create_update_voice_raw_empty_inx_col_sqlstr_UpdatesTable_Scenario0_EmptyPidginTables():
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
        pidname_s_vld_tablename = prime_tbl(pidgin_name_str(), "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        print(f"{get_table_columns(cursor, pidname_s_vld_tablename)=}")

        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename} ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
VALUES
  ({event1}, '{sue_otx}', '{sue_inx}')
, ({event2}, '{yao_otx}', NULL)
, ({event5}, '{sue_otx}', NULL)
, ({event7}, '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_face_name_only_sqlstr)
        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 2

        # WHEN
        update_sqlstr = create_update_voice_raw_empty_inx_col_sqlstr(
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
            (5, sue_otx, sue_otx),
            (7, bob_otx, bob_inx),
        ]


def test_set_all_voice_raw_inx_columns_Scenario0_empty_tables():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_idea_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', NULL)
        , ({event1}, '{bob_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        , ({event9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        set_all_voice_raw_inx_columns(cursor)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (0, bob_otx, bob_otx),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]
