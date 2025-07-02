from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.a06_believer_logic.test._util.a06_str import (
    believer_acct_membership_str,
    believer_acctunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_premiseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
)
from src.a08_believer_atom_logic.atom_config import get_delete_key_name
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a10_believer_calc.test._util.a10_str import believer_groupunit_str
from src.a11_bud_logic.test._util.a11_str import (
    belief_label_str,
    believer_name_str,
    bud_time_str,
    tran_time_str,
)
from src.a12_hub_toolbox.test._util.a12_str import belief_ote1_agg_str, job_str
from src.a15_belief_logic.test._util.a15_str import (
    belief_budunit_str,
    belief_paybook_str,
    belief_timeline_hour_str,
    belief_timeline_month_str,
    belief_timeline_weekday_str,
    belief_timeoffi_str,
    beliefunit_str,
)
from src.a16_pidgin_logic.test._util.a16_str import (
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
)
from src.a17_idea_logic.idea_config import (
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.a17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.a17_idea_logic.test._util.a17_str import error_message_str, idea_category_str
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_acct_nets_str,
    belief_event_time_agg_str,
    believer_net_amount_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    CREATE_BELIEF_ACCT_NETS_SQLSTR,
    CREATE_BELIEF_EVENT_TIME_AGG_SQLSTR,
    CREATE_BELIEF_OTE1_AGG_SQLSTR,
    IDEA_STAGEBLE_DEL_DIMENS,
    INSERT_BELIEF_EVENT_TIME_AGG_SQLSTR,
    INSERT_BELIEF_OTE1_AGG_FROM_VOICE_SQLSTR,
    UPDATE_ERROR_MESSAGE_BELIEF_EVENT_TIME_AGG_SQLSTR,
    create_all_idea_tables,
    create_prime_tablename,
    create_sound_and_voice_tables,
    get_idea_stageble_put_dimens,
)


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())
    x_set = {len(dimen) for dimen in ALL_DIMEN_ABBV7}
    assert x_set == {7}


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    believerunit_dimen = believerunit_str()
    onracct_dimen = believer_acctunit_str()
    onrmemb_dimen = believer_acct_membership_str()
    onrgrou_dimen = believer_groupunit_str()
    onrplan_dimen = believer_planunit_str()
    onrawar_dimen = believer_plan_awardlink_str()
    onrreas_dimen = believer_plan_reasonunit_str()
    onrprem_dimen = believer_plan_reason_premiseunit_str()
    onrlabo_dimen = believer_plan_laborlink_str()
    onrheal_dimen = believer_plan_healerlink_str()
    onrfact_dimen = believer_plan_factunit_str()
    beliefunit_dimen = beliefunit_str()
    blfpayy_dimen = belief_paybook_str()
    blfbudd_dimen = belief_budunit_str()
    blfhour_dimen = belief_timeline_hour_str()
    blfmont_dimen = belief_timeline_month_str()
    blfweek_dimen = belief_timeline_weekday_str()
    blfoffi_dimen = belief_timeoffi_str()
    pidname_dimen = pidgin_name_str()
    pidlabe_dimen = pidgin_label_str()
    pidrope_dimen = pidgin_rope_str()
    pidtitl_dimen = pidgin_title_str()
    pidcore_dimen = pidgin_core_str()
    raw_str = "raw"
    agg_str = "agg"
    vld_str = "vld"
    put_str = "put"
    del_str = "del"

    # WHEN
    believerunit_s_agg_table = create_prime_tablename(
        "believerunit", "s", agg_str, put_str
    )
    onracct_s_agg_table = create_prime_tablename("onracct", "s", agg_str, put_str)
    onrmemb_s_agg_table = create_prime_tablename("onrmemb", "s", agg_str, put_str)
    onrplan_s_agg_table = create_prime_tablename("onrplan", "s", agg_str, put_str)
    onrawar_s_agg_table = create_prime_tablename("onrawar", "s", agg_str, put_str)
    onrreas_s_agg_table = create_prime_tablename("onrreas", "s", agg_str, put_str)
    onrprem_s_agg_table = create_prime_tablename("onrprem", "s", agg_str, put_str)
    onrlabo_s_agg_table = create_prime_tablename("ONRLABO", "s", agg_str, put_str)
    onrheal_s_agg_table = create_prime_tablename("onrheal", "s", agg_str, put_str)
    onrfact_s_agg_table = create_prime_tablename("onrfact", "s", agg_str, put_str)
    onrfact_s_del_table = create_prime_tablename("onrfact", "s", agg_str, del_str)
    beliefunit_s_agg_table = create_prime_tablename("beliefunit", "s", agg_str)
    blfpayy_s_agg_table = create_prime_tablename("blfpayy", "s", agg_str)
    blfbudd_s_agg_table = create_prime_tablename("blfbudd", "s", agg_str)
    blfhour_s_agg_table = create_prime_tablename("blfhour", "s", agg_str)
    blfmont_s_agg_table = create_prime_tablename("blfmont", "s", agg_str)
    blfweek_s_agg_table = create_prime_tablename("blfweek", "s", agg_str)
    blfoffi_s_agg_table = create_prime_tablename("blfoffi", "s", agg_str)
    pidname_s_agg_table = create_prime_tablename("pidname", "s", agg_str)
    pidlabe_s_agg_table = create_prime_tablename("pidlabe", "s", agg_str)
    pidrope_s_agg_table = create_prime_tablename("pidrope", "s", agg_str)
    pidtitl_s_agg_table = create_prime_tablename("pidtitl", "s", agg_str)
    pidtitl_v_agg_table = create_prime_tablename("pidtitl", "v", agg_str)
    pidtitl_s_raw_table = create_prime_tablename("pidtitl", "s", raw_str)
    pidtitl_s_val_table = create_prime_tablename("pidtitl", "s", vld_str)
    pidcore_s_raw_table = create_prime_tablename("pidcore", "s", raw_str)
    pidcore_s_agg_table = create_prime_tablename("pidcore", "s", agg_str)
    onracct_job_table = create_prime_tablename("onracct", job_str(), None)
    x_onracct_raw = create_prime_tablename("onracct", "k", raw_str)
    onrgrou_job_table = create_prime_tablename("onrgrou", job_str(), None)

    # THEN
    assert believerunit_s_agg_table == f"{believerunit_dimen}_s_put_agg"
    assert onracct_s_agg_table == f"{onracct_dimen}_s_put_agg"
    assert onrmemb_s_agg_table == f"{onrmemb_dimen}_s_put_agg"
    assert onrplan_s_agg_table == f"{onrplan_dimen}_s_put_agg"
    assert onrawar_s_agg_table == f"{onrawar_dimen}_s_put_agg"
    assert onrreas_s_agg_table == f"{onrreas_dimen}_s_put_agg"
    assert onrprem_s_agg_table == f"{onrprem_dimen}_s_put_agg"
    assert onrlabo_s_agg_table == f"{onrlabo_dimen}_s_put_agg"
    assert onrheal_s_agg_table == f"{onrheal_dimen}_s_put_agg"
    assert onrfact_s_agg_table == f"{onrfact_dimen}_s_put_agg"
    assert onrfact_s_del_table == f"{onrfact_dimen}_s_del_agg"
    assert beliefunit_s_agg_table == f"{beliefunit_dimen}_s_agg"
    assert blfpayy_s_agg_table == f"{blfpayy_dimen}_s_agg"
    assert blfbudd_s_agg_table == f"{blfbudd_dimen}_s_agg"
    assert blfhour_s_agg_table == f"{blfhour_dimen}_s_agg"
    assert blfmont_s_agg_table == f"{blfmont_dimen}_s_agg"
    assert blfweek_s_agg_table == f"{blfweek_dimen}_s_agg"
    assert blfoffi_s_agg_table == f"{blfoffi_dimen}_s_agg"
    assert pidname_s_agg_table == f"{pidname_dimen}_s_agg"
    assert pidlabe_s_agg_table == f"{pidlabe_dimen}_s_agg"
    assert pidrope_s_agg_table == f"{pidrope_dimen}_s_agg"
    assert pidtitl_s_agg_table == f"{pidtitl_dimen}_s_agg"
    assert pidtitl_v_agg_table == f"{pidtitl_dimen}_v_agg"
    assert pidtitl_s_raw_table == f"{pidtitl_dimen}_s_raw"
    assert pidtitl_s_val_table == f"{pidtitl_dimen}_s_vld"
    assert pidcore_s_raw_table == f"{pidcore_dimen}_s_raw"
    assert pidcore_s_agg_table == f"{pidcore_dimen}_s_agg"
    assert onracct_job_table == f"{onracct_dimen}_job"
    assert onrgrou_job_table == f"{onrgrou_dimen}_job"
    assert x_onracct_raw == "believer_acctunit_raw"


def test_create_all_idea_tables_CreatesBeliefRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as belief_db_conn:
        cursor = belief_db_conn.cursor()
        for idea_number in idea_numbers:
            assert db_table_exists(cursor, f"{idea_number}_raw") is False

        # WHEN
        create_all_idea_tables(cursor)

        # THEN
        for idea_number in idea_numbers:
            print(f"{idea_number} checking...")
            assert db_table_exists(cursor, f"{idea_number}_raw")


def test_get_idea_stageble_put_dimens_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "belief"
    }
    with sqlite3_connect(":memory:") as belief_db_conn:
        cursor = belief_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_voice_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        expected_idea_slabelable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_value_columns = set(dimen_config.get("jvalues").keys())
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_slabelable = dimen_key_columns.issubset(src_columns)
                if idea_number == "br00036":
                    print(f"{x_dimen} {idea_number} checking... {src_columns}")
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_slabelable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    expected_idea_slabelable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set.intersection(dimen_value_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    # print(
                    #     f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
                    # )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""

    idea_stageble_dimen_list = sorted(list(expected_idea_slabelable_dimens))
    print(expected_idea_slabelable_dimens)
    assert idea_dimen_combo_checked_count == 680
    assert idea_raw2dimen_count == 109
    assert get_idea_stageble_put_dimens() == expected_idea_slabelable_dimens


def test_IDEA_STAGEBLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "belief"
    }
    with sqlite3_connect(":memory:") as belief_db_conn:
        cursor = belief_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_voice_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        x_idea_slabelable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_key_columns = get_default_sorted_list(dimen_key_columns)
            dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
            dimen_key_columns = set(dimen_key_columns)
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_slabelable = dimen_key_columns.issubset(src_columns)
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_slabelable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    x_idea_slabelable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
                    )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""
    expected_idea_slabelable_dimens = {
        x_idea_number: slabelable_dimens
        for x_idea_number, slabelable_dimens in x_idea_slabelable_dimens.items()
        if slabelable_dimens != []
    }
    idea_stageble_dimen_list = sorted(list(expected_idea_slabelable_dimens))
    print(f"{expected_idea_slabelable_dimens=}")
    assert idea_dimen_combo_checked_count == 680
    assert idea_raw2dimen_count == 10
    assert IDEA_STAGEBLE_DEL_DIMENS == expected_idea_slabelable_dimens


def test_CREATE_BELIEF_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {belief_event_time_agg_str()} (
  {belief_label_str()} TEXT
, {event_int_str()} INTEGER
, agg_time INTEGER
, {error_message_str()} TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_BELIEF_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_BELIEF_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO {belief_event_time_agg_str()} ({belief_label_str()}, {event_int_str()}, agg_time)
SELECT {belief_label_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {belief_label_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM belief_paybook_raw
    GROUP BY {belief_label_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {belief_label_str()}, {event_int_str()}, {bud_time_str()} as agg_time
    FROM belief_budunit_raw
    GROUP BY {belief_label_str()}, {event_int_str()}, {bud_time_str()}
)
ORDER BY {belief_label_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_BELIEF_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_BELIEF_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {belief_label_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {belief_label_str()} ORDER BY {event_int_str()}) AS prev_agg_time
    FROM {belief_event_time_agg_str()}
)
UPDATE {belief_event_time_agg_str()}
SET {error_message_str()} = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{event_int_str()} = {belief_event_time_agg_str()}.{event_int_str()}
    AND EventTimeOrdered.{belief_label_str()} = {belief_event_time_agg_str()}.{belief_label_str()}
    AND EventTimeOrdered.agg_time = {belief_event_time_agg_str()}.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_BELIEF_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_BELIEF_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {belief_ote1_agg_str()} (
  {belief_label_str()} TEXT
, {believer_name_str()} TEXT
, {event_int_str()} INTEGER
, {bud_time_str()} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_BELIEF_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# TODO create test to prove this insert should grab minimun event_int instead of just event_int
# TODO create test to prove this insert should never grab when error message is not null in source table
def test_INSERT_BELIEF_OTE1_AGG_FROM_VOICE_SQLSTR_Exists():
    # ESTABLISH
    beliefbud_v_raw_tablename = create_prime_tablename(belief_budunit_str(), "v", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO {belief_ote1_agg_str()} ({belief_label_str()}, {believer_name_str()}, {event_int_str()}, {bud_time_str()})
SELECT {belief_label_str()}, {believer_name_str()}, {event_int_str()}, {bud_time_str()}
FROM (
    SELECT 
      {belief_label_str()}_inx {belief_label_str()}
    , {believer_name_str()}_inx {believer_name_str()}
    , {event_int_str()}
    , {bud_time_str()}
    FROM {beliefbud_v_raw_tablename}
    GROUP BY {belief_label_str()}_inx, {believer_name_str()}_inx, {event_int_str()}, {bud_time_str()}
)
ORDER BY {belief_label_str()}, {believer_name_str()}, {event_int_str()}, {bud_time_str()}
;
"""
    # WHEN / THEN
    assert INSERT_BELIEF_OTE1_AGG_FROM_VOICE_SQLSTR == expected_INSERT_sqlstr


def test_CREATE_BELIEF_ACCT_NETS_SQLSTR_Exists():
    # ESTABLISH
    sqlite_types = get_idea_sqlite_types()
    sqlite_types[believer_net_amount_str()] = "REAL"
    expected_create_table_sqlstr = get_create_table_sqlstr(
        tablename=belief_acct_nets_str(),
        columns_list=[
            belief_label_str(),
            believer_name_str(),
            believer_net_amount_str(),
        ],
        column_types=sqlite_types,
    )

    # WHEN / THEN
    assert CREATE_BELIEF_ACCT_NETS_SQLSTR == expected_create_table_sqlstr
