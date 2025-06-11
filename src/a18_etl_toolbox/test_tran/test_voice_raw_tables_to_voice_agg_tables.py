from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    credit_score_str,
    debt_score_str,
    plan_acctunit_str,
)
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a15_vow_logic.vow_config import get_vow_dimens
from src.a17_idea_logic._test_util.a17_str import idea_category_str
from src.a17_idea_logic.idea_config import get_default_sorted_list, get_idea_config_dict
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    get_dimen_abbv7,
    get_insert_voice_agg_sqlstrs,
)
from src.a18_etl_toolbox.transformers import etl_voice_raw_tables_to_voice_agg_tables


def test_get_insert_voice_agg_sqlstrs_ReturnsObj_CheckVowDimen():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    insert_voice_agg_sqlstrs = get_insert_voice_agg_sqlstrs()

    # THEN
    assert get_vow_dimens().issubset(set(insert_voice_agg_sqlstrs.keys()))
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "vow"
    }
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            raw_tablename = prime_tbl(x_dimen, "v", "raw")
            agg_tablename = prime_tbl(x_dimen, "v", "agg")
            raw_columns = get_table_columns(cursor, raw_tablename)
            agg_columns = get_table_columns(cursor, agg_tablename)
            raw_columns = {raw_col for raw_col in raw_columns if raw_col[-3:] != "otx"}
            raw_columns.remove(f"{face_name_str()}_inx")
            raw_columns.remove(event_int_str())
            raw_columns.remove("error_message")
            raw_columns = get_default_sorted_list(raw_columns)

            raw_columns_str = ", ".join(raw_columns)
            agg_columns_str = ", ".join(agg_columns)
            # print(f"{raw_columns_str=}")
            # print(f"{agg_columns_str=}")
            expected_table2table_agg_insert_sqlstr = f"""
INSERT INTO {agg_tablename} ({agg_columns_str})
SELECT {raw_columns_str}
FROM {raw_tablename}
GROUP BY {raw_columns_str}
"""
            dimen_abbv7 = get_dimen_abbv7(x_dimen)
            # print(f'"{x_dimen}": {dimen_abbv7.upper()}_VOICE_AGG_INSERT_SQLSTR,')
            print(
                f'{dimen_abbv7.upper()}_VOICE_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            )
            gen_sqlstr = insert_voice_agg_sqlstrs.get(x_dimen)
            assert gen_sqlstr == expected_table2table_agg_insert_sqlstr


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_PlanDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    plan_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "plan"
    }

    # WHEN
    insert_voice_agg_sqlstrs = get_insert_voice_agg_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for plan_dimen in plan_dimens_config:
            # print(f"{plan_dimen=}")
            v_raw_put_tablename = prime_tbl(plan_dimen, "v", "raw", "put")
            v_raw_del_tablename = prime_tbl(plan_dimen, "v", "raw", "del")
            v_agg_put_tablename = prime_tbl(plan_dimen, "v", "agg", "put")
            v_agg_del_tablename = prime_tbl(plan_dimen, "v", "agg", "del")
            v_raw_put_cols = get_table_columns(cursor, v_raw_put_tablename)
            v_raw_del_cols = get_table_columns(cursor, v_raw_del_tablename)
            v_agg_put_cols = get_table_columns(cursor, v_agg_put_tablename)
            v_agg_del_cols = get_table_columns(cursor, v_agg_del_tablename)
            v_raw_put_cols = {col for col in v_raw_put_cols if col[-3:] != "otx"}
            v_raw_del_cols = {col for col in v_raw_del_cols if col[-3:] != "otx"}
            v_raw_put_cols = get_default_sorted_list(v_raw_put_cols)
            v_raw_del_cols = get_default_sorted_list(v_raw_del_cols)
            v_raw_put_columns_str = ", ".join(v_raw_put_cols)
            v_raw_put_cols.remove("pidgin_event_int")
            v_raw_del_cols.remove("pidgin_event_int")
            v_raw_put_columns_str = ", ".join(v_raw_put_cols)
            v_raw_del_columns_str = ", ".join(v_raw_del_cols)
            v_agg_put_columns_str = ", ".join(v_agg_put_cols)
            v_agg_del_columns_str = ", ".join(v_agg_del_cols)
            expected_agg_put_insert_sqlstr = f"""
INSERT INTO {v_agg_put_tablename} ({v_agg_put_columns_str})
SELECT {v_raw_put_columns_str}
FROM {v_raw_put_tablename}
GROUP BY {v_raw_put_columns_str}
"""
            expected_agg_del_insert_sqlstr = f"""
INSERT INTO {v_agg_del_tablename} ({v_agg_del_columns_str})
SELECT {v_raw_del_columns_str}
FROM {v_raw_del_tablename}
GROUP BY {v_raw_del_columns_str}
"""
            abbv7 = get_dimen_abbv7(plan_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_AGG_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_AGG_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= """{expected_agg_put_insert_sqlstr}"""')
            print(f'{del_sqlstr_ref}= """{expected_agg_del_insert_sqlstr}"""')
            # print(f"'{v_agg_put_tablename}': {put_sqlstr_ref},")
            # print(f"'{v_agg_del_tablename}': {del_sqlstr_ref},")
            insert_v_agg_put_sqlstr = insert_voice_agg_sqlstrs.get(v_agg_put_tablename)
            insert_v_agg_del_sqlstr = insert_voice_agg_sqlstrs.get(v_agg_del_tablename)
            assert insert_v_agg_put_sqlstr == expected_agg_put_insert_sqlstr
            assert insert_v_agg_del_sqlstr == expected_agg_del_insert_sqlstr


def test_get_insert_voice_agg_sqlstrs_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        planacct_v_raw_put_tablename = prime_tbl(plan_acctunit_str(), "v", "raw", "put")
        print(f"{get_table_columns(cursor, planacct_v_raw_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {planacct_v_raw_put_tablename} (
  {event_int_str()}
, {face_name_str()}_inx
, {vow_label_str()}_inx
, {owner_name_str()}_inx
, {acct_name_str()}_inx
, {credit_score_str()}
, {debt_score_str()}
)
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(insert_into_clause)
        assert get_row_count(cursor, planacct_v_raw_put_tablename) == 5
        planacct_v_agg_put_tablename = prime_tbl(plan_acctunit_str(), "v", "agg", "put")
        assert get_row_count(cursor, planacct_v_agg_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_voice_agg_sqlstrs().get(planacct_v_agg_put_tablename)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, planacct_v_agg_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {planacct_v_agg_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, sue_str, a23_str, yao_str, yao_inx, 44.0, 22.0),
            (event2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (event5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (event7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_voice_raw_tables_to_voice_agg_tables_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        planacct_v_raw_put_tablename = prime_tbl(plan_acctunit_str(), "v", "raw", "put")
        print(f"{get_table_columns(cursor, planacct_v_raw_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {planacct_v_raw_put_tablename} (
  {event_int_str()}
, {face_name_str()}_inx
, {vow_label_str()}_inx
, {owner_name_str()}_inx
, {acct_name_str()}_inx
, {credit_score_str()}
, {debt_score_str()}
)
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(insert_into_clause)
        assert get_row_count(cursor, planacct_v_raw_put_tablename) == 5
        planacct_v_agg_put_tablename = prime_tbl(plan_acctunit_str(), "v", "agg", "put")
        assert get_row_count(cursor, planacct_v_agg_put_tablename) == 0

        # WHEN
        etl_voice_raw_tables_to_voice_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, planacct_v_agg_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {planacct_v_agg_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, sue_str, a23_str, yao_str, yao_inx, 44.0, 22.0),
            (event2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (event5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (event7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]
