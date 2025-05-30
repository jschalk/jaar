from src.a02_finance_logic._test_util.a02_str import owner_name_str, fisc_label_str
from src.a06_bud_logic._test_util.a06_str import (
    face_name_str,
    event_int_str,
    acct_name_str,
    bud_acctunit_str,
)
from src.a16_pidgin_logic.pidgin import (
    default_bridge_if_None,
    default_unknown_str_if_None,
)
from src.a16_pidgin_logic._test_util.a16_str import (
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
    unknown_str_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    CREATE_BUDACCT_SOUND_PUT_AGG_STR,
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    create_bridge_exists_in_name_error_update_sqlstr,
    create_bridge_exists_in_label_error_update_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    set_fisc_bud_sound_agg_bridge_errors,
)
from sqlite3 import connect as sqlite3_connect


def test_create_bridge_exists_in_name_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    comma = ","
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BUDACCT_SOUND_PUT_AGG_STR)
        budacct_dimen = bud_acctunit_str()
        budacct_s_agg_put = create_prime_tablename(budacct_dimen, "s", "agg", "put")
        insert_budacct_sqlstr = f"""INSERT INTO {budacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {fisc_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_budacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_bridge_str()}, {inx_bridge_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {budacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_bridge_exists_in_name_error_update_sqlstr(
            budacct_s_agg_put, acct_name_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {budacct_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        name_bridge_str = f"Bridge cannot exist in NameTerm column {acct_name_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_bridge_str),
        ]


def test_create_bridge_exists_in_label_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    a23_str = "accord23"
    a45_str = f"{colon}accord45"
    comma = ","
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BUDACCT_SOUND_PUT_AGG_STR)
        budacct_dimen = bud_acctunit_str()
        budacct_s_agg_put = create_prime_tablename(budacct_dimen, "s", "agg", "put")
        insert_budacct_sqlstr = f"""INSERT INTO {budacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {fisc_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_budacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_bridge_str()}, {inx_bridge_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {budacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_bridge_exists_in_label_error_update_sqlstr(
            budacct_s_agg_put, fisc_label_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {budacct_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        label_bridge_str = f"Bridge cannot exist in LabelTerm column {fisc_label_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, None),
            (event1, sue_str, a45_str, yao_str, bob_str, None, None, label_bridge_str),
        ]


def test_set_fisc_bud_sound_agg_bridge_errors_PopulatesTable_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    a23_str = "accord23"
    a45_str = f"{colon}accord45"
    comma = ","
    ukx = "Unknown"
    event1 = 1
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BUDACCT_SOUND_PUT_AGG_STR)
        budacct_dimen = bud_acctunit_str()
        budacct_s_agg_put = create_prime_tablename(budacct_dimen, "s", "agg", "put")
        insert_budacct_sqlstr = f"""INSERT INTO {budacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {fisc_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{yao_str}')
;
"""
        cursor.execute(insert_budacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_bridge_str()}, {inx_bridge_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {budacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_fisc_bud_sound_agg_bridge_errors(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {budacct_s_agg_put} ORDER BY {fisc_label_str()}, {owner_name_str()}, {acct_name_str()}"
        cursor.execute(select_core_raw_sqlstr)
        name_bridge_str = f"Bridge cannot exist in NameTerm column {acct_name_str()}"
        label_bridge_str = f"Bridge cannot exist in LabelTerm column {fisc_label_str()}"
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (event1, sue_str, a45_str, yao_str, yao_str, None, None, label_bridge_str),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_bridge_str),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]
