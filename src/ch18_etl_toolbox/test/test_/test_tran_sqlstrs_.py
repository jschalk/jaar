from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.ch09_belief_atom_logic.atom_config import get_delete_key_name
from src.ch17_idea_logic.idea_config import (
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.ch17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    belief_groupunit_str,
    belief_name_str,
    belief_net_amount_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    belief_voice_membership_str,
    belief_voiceunit_str,
    beliefunit_str,
    bud_time_str,
    cumulative_minute_str,
    error_message_str,
    event_int_str,
    face_name_str,
    hour_label_str,
    idea_category_str,
    job_str,
    moment_budunit_str,
    moment_event_time_agg_str,
    moment_label_str,
    moment_ote1_agg_str,
    moment_paybook_str,
    moment_timeline_hour_str,
    moment_timeline_month_str,
    moment_timeline_weekday_str,
    moment_timeoffi_str,
    moment_voice_nets_str,
    momentunit_str,
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
    tran_time_str,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    CREATE_MOMENT_EVENT_TIME_AGG_SQLSTR,
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    IDEA_STAGEBLE_DEL_DIMENS,
    INSERT_MOMENT_EVENT_TIME_AGG_SQLSTR,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    UPDATE_ERROR_MESSAGE_MOMENT_EVENT_TIME_AGG_SQLSTR,
    create_all_idea_tables,
    create_prime_tablename,
    create_sound_and_heard_tables,
    get_idea_stageble_put_dimens,
)


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())
    x_set = {len(dimen) for dimen in ALL_DIMEN_ABBV7}
    assert x_set == {7}


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    blrunit_dimen = beliefunit_str()
    blrpern_dimen = belief_voiceunit_str()
    blrmemb_dimen = belief_voice_membership_str()
    blrgrou_dimen = belief_groupunit_str()
    blrplan_dimen = belief_planunit_str()
    blrawar_dimen = belief_plan_awardunit_str()
    blrreas_dimen = belief_plan_reasonunit_str()
    blrprem_dimen = belief_plan_reason_caseunit_str()
    blrlabo_dimen = belief_plan_partyunit_str()
    blrheal_dimen = belief_plan_healerunit_str()
    blrfact_dimen = belief_plan_factunit_str()
    blfunit_dimen = momentunit_str()
    blfpayy_dimen = moment_paybook_str()
    blfbudd_dimen = moment_budunit_str()
    blfhour_dimen = moment_timeline_hour_str()
    blfmont_dimen = moment_timeline_month_str()
    blfweek_dimen = moment_timeline_weekday_str()
    blfoffi_dimen = moment_timeoffi_str()
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
    blrunit_s_agg_table = create_prime_tablename("beliefunit", "s", agg_str, put_str)
    blrpern_s_agg_table = create_prime_tablename("blrpern", "s", agg_str, put_str)
    blrmemb_s_agg_table = create_prime_tablename("blrmemb", "s", agg_str, put_str)
    blrplan_s_agg_table = create_prime_tablename("blrplan", "s", agg_str, put_str)
    blrawar_s_agg_table = create_prime_tablename("blrawar", "s", agg_str, put_str)
    blrreas_s_agg_table = create_prime_tablename("blrreas", "s", agg_str, put_str)
    blrprem_s_agg_table = create_prime_tablename("blrprem", "s", agg_str, put_str)
    blrlabo_s_agg_table = create_prime_tablename("BLRLABO", "s", agg_str, put_str)
    blrheal_s_agg_table = create_prime_tablename("blrheal", "s", agg_str, put_str)
    blrfact_s_agg_table = create_prime_tablename("blrfact", "s", agg_str, put_str)
    blrfact_s_del_table = create_prime_tablename("blrfact", "s", agg_str, del_str)
    blfunit_s_agg_table = create_prime_tablename("blfunit", "s", agg_str)
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
    pidtitl_h_agg_table = create_prime_tablename("pidtitl", "h", agg_str)
    pidtitl_s_raw_table = create_prime_tablename("pidtitl", "s", raw_str)
    pidtitl_s_val_table = create_prime_tablename("pidtitl", "s", vld_str)
    pidcore_s_raw_table = create_prime_tablename("pidcore", "s", raw_str)
    pidcore_s_agg_table = create_prime_tablename("pidcore", "s", agg_str)
    blrpern_job_table = create_prime_tablename("blrpern", job_str(), None)
    x_blrpern_raw = create_prime_tablename("blrpern", "k", raw_str)
    blrgrou_job_table = create_prime_tablename("blrgrou", job_str(), None)

    # THEN
    assert blrunit_s_agg_table == f"{blrunit_dimen}_s_put_agg"
    assert blrpern_s_agg_table == f"{blrpern_dimen}_s_put_agg"
    assert blrmemb_s_agg_table == f"{blrmemb_dimen}_s_put_agg"
    assert blrplan_s_agg_table == f"{blrplan_dimen}_s_put_agg"
    assert blrawar_s_agg_table == f"{blrawar_dimen}_s_put_agg"
    assert blrreas_s_agg_table == f"{blrreas_dimen}_s_put_agg"
    assert blrprem_s_agg_table == f"{blrprem_dimen}_s_put_agg"
    assert blrlabo_s_agg_table == f"{blrlabo_dimen}_s_put_agg"
    assert blrheal_s_agg_table == f"{blrheal_dimen}_s_put_agg"
    assert blrfact_s_agg_table == f"{blrfact_dimen}_s_put_agg"
    assert blrfact_s_del_table == f"{blrfact_dimen}_s_del_agg"
    assert blfunit_s_agg_table == f"{blfunit_dimen}_s_agg"
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
    assert pidtitl_h_agg_table == f"{pidtitl_dimen}_h_agg"
    assert pidtitl_s_raw_table == f"{pidtitl_dimen}_s_raw"
    assert pidtitl_s_val_table == f"{pidtitl_dimen}_s_vld"
    assert pidcore_s_raw_table == f"{pidcore_dimen}_s_raw"
    assert pidcore_s_agg_table == f"{pidcore_dimen}_s_agg"
    assert blrpern_job_table == f"{blrpern_dimen}_job"
    assert blrgrou_job_table == f"{blrgrou_dimen}_job"
    assert x_blrpern_raw == "belief_voiceunit_raw"


def test_create_all_idea_tables_CreatesMomentRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
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
        # if dimen_config.get(idea_category_str()) == "moment"
    }
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_heard_tables(cursor)

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
                    existing_value_col = src_cols_set & (dimen_value_columns)
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
        # if dimen_config.get(idea_category_str()) == "moment"
    }
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_heard_tables(cursor)

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


def test_CREATE_MOMENT_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {moment_event_time_agg_str()} (
  {moment_label_str()} TEXT
, {event_int_str()} INTEGER
, agg_time INTEGER
, {error_message_str()} TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_MOMENT_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO {moment_event_time_agg_str()} ({moment_label_str()}, {event_int_str()}, agg_time)
SELECT {moment_label_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {moment_label_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM moment_paybook_raw
    GROUP BY {moment_label_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {moment_label_str()}, {event_int_str()}, {bud_time_str()} as agg_time
    FROM moment_budunit_raw
    GROUP BY {moment_label_str()}, {event_int_str()}, {bud_time_str()}
)
ORDER BY {moment_label_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_MOMENT_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {moment_label_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {moment_label_str()} ORDER BY {event_int_str()}) AS prev_agg_time
    FROM {moment_event_time_agg_str()}
)
UPDATE {moment_event_time_agg_str()}
SET {error_message_str()} = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{event_int_str()} = {moment_event_time_agg_str()}.{event_int_str()}
    AND EventTimeOrdered.{moment_label_str()} = {moment_event_time_agg_str()}.{moment_label_str()}
    AND EventTimeOrdered.agg_time = {moment_event_time_agg_str()}.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_MOMENT_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {moment_ote1_agg_str()} (
  {moment_label_str()} TEXT
, {belief_name_str()} TEXT
, {event_int_str()} INTEGER
, {bud_time_str()} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_MOMENT_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# TODO create test to prove this insert should grab minimun event_int instead of just event_int
# TODO create test to prove this insert should never grab when error message is not null in source table
def test_INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR_Exists():
    # ESTABLISH
    momentbud_h_raw_tablename = create_prime_tablename(moment_budunit_str(), "h", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO {moment_ote1_agg_str()} ({moment_label_str()}, {belief_name_str()}, {event_int_str()}, {bud_time_str()})
SELECT {moment_label_str()}, {belief_name_str()}, {event_int_str()}, {bud_time_str()}
FROM (
    SELECT 
      {moment_label_str()}_inx {moment_label_str()}
    , {belief_name_str()}_inx {belief_name_str()}
    , {event_int_str()}
    , {bud_time_str()}
    FROM {momentbud_h_raw_tablename}
    GROUP BY {moment_label_str()}_inx, {belief_name_str()}_inx, {event_int_str()}, {bud_time_str()}
)
ORDER BY {moment_label_str()}, {belief_name_str()}, {event_int_str()}, {bud_time_str()}
;
"""
    # WHEN / THEN
    assert INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR == expected_INSERT_sqlstr


def test_CREATE_MOMENT_VOICE_NETS_SQLSTR_Exists():
    # ESTABLISH
    sqlite_types = get_idea_sqlite_types()
    sqlite_types[belief_net_amount_str()] = "REAL"
    expected_create_table_sqlstr = get_create_table_sqlstr(
        tablename=moment_voice_nets_str(),
        columns_list=[
            moment_label_str(),
            belief_name_str(),
            belief_net_amount_str(),
        ],
        column_types=sqlite_types,
    )

    # WHEN / THEN
    assert CREATE_MOMENT_VOICE_NETS_SQLSTR == expected_create_table_sqlstr
