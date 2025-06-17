from sqlite3 import connect as sqlite3_connect
from src.a02_finance_logic._util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic._util.a06_str import acct_name_str, plan_acctunit_str
from src.a09_pack_logic._util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic._util.a16_str import (
    inx_knot_str,
    otx_knot_str,
    unknown_str_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    CREATE_PLNACCT_SOUND_PUT_AGG_STR,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
)
from src.a18_etl_toolbox.transformers import set_vow_plan_sound_agg_knot_errors


def test_create_knot_exists_in_name_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
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
        cursor.execute(CREATE_PLNACCT_SOUND_PUT_AGG_STR)
        plnacct_dimen = plan_acctunit_str()
        plnacct_s_agg_put = create_prime_tablename(plnacct_dimen, "s", "agg", "put")
        insert_plnacct_sqlstr = f"""INSERT INTO {plnacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {vow_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_plnacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {plnacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_name_error_update_sqlstr(
            plnacct_s_agg_put, acct_name_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {plnacct_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {acct_name_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
        ]


def test_create_knot_exists_in_label_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
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
        cursor.execute(CREATE_PLNACCT_SOUND_PUT_AGG_STR)
        plnacct_dimen = plan_acctunit_str()
        plnacct_s_agg_put = create_prime_tablename(plnacct_dimen, "s", "agg", "put")
        insert_plnacct_sqlstr = f"""INSERT INTO {plnacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {vow_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_plnacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {plnacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_label_error_update_sqlstr(
            plnacct_s_agg_put, vow_label_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {plnacct_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        label_knot_str = f"Knot cannot exist in LabelTerm column {vow_label_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, None),
            (event1, sue_str, a45_str, yao_str, bob_str, None, None, label_knot_str),
        ]


def test_set_vow_plan_sound_agg_knot_errors_PopulatesTable_Scenario0():
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
        cursor.execute(CREATE_PLNACCT_SOUND_PUT_AGG_STR)
        plnacct_dimen = plan_acctunit_str()
        plnacct_s_agg_put = create_prime_tablename(plnacct_dimen, "s", "agg", "put")
        insert_plnacct_sqlstr = f"""INSERT INTO {plnacct_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {vow_label_str()}, {owner_name_str()}, {acct_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{yao_str}')
;
"""
        cursor.execute(insert_plnacct_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = (
            f"SELECT COUNT(*) FROM {plnacct_s_agg_put} WHERE error_message IS NOT NULL"
        )
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_vow_plan_sound_agg_knot_errors(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {plnacct_s_agg_put} ORDER BY {vow_label_str()}, {owner_name_str()}, {acct_name_str()}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {acct_name_str()}"
        label_knot_str = f"Knot cannot exist in LabelTerm column {vow_label_str()}"
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (event1, sue_str, a45_str, yao_str, yao_str, None, None, label_knot_str),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]
