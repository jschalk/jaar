from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.ch09_belief_atom_logic.atom_config import get_delete_key_name
from src.ch17_idea.idea_config import (
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.ch17_idea.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ch18_world_etl.tran_sqlstrs import (
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
from src.ref.ch18_keywords import Ch18Keywords as wx


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())
    x_set = {len(dimen) for dimen in ALL_DIMEN_ABBV7}
    assert x_set == {7}


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    blrunit_dimen = wx.beliefunit
    blrpern_dimen = wx.belief_voiceunit
    blrmemb_dimen = wx.belief_voice_membership
    blrgrou_dimen = wx.belief_groupunit
    blrplan_dimen = wx.belief_planunit
    blrawar_dimen = wx.belief_plan_awardunit
    blrreas_dimen = wx.belief_plan_reasonunit
    blrprem_dimen = wx.belief_plan_reason_caseunit
    blrlabo_dimen = wx.belief_plan_partyunit
    blrheal_dimen = wx.belief_plan_healerunit
    blrfact_dimen = wx.belief_plan_factunit
    blfunit_dimen = wx.momentunit
    blfpayy_dimen = wx.moment_paybook
    blfbudd_dimen = wx.moment_budunit
    blfhour_dimen = wx.moment_timeline_hour
    blfmont_dimen = wx.moment_timeline_month
    blfweek_dimen = wx.moment_timeline_weekday
    blfoffi_dimen = wx.moment_timeoffi
    trlname_dimen = wx.translate_name
    trllabe_dimen = wx.translate_label
    trlrope_dimen = wx.translate_rope
    trltitl_dimen = wx.translate_title
    trlcore_dimen = wx.translate_core
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
    trlname_s_agg_table = create_prime_tablename("trlname", "s", agg_str)
    trllabe_s_agg_table = create_prime_tablename("trllabe", "s", agg_str)
    trlrope_s_agg_table = create_prime_tablename("trlrope", "s", agg_str)
    trltitl_s_agg_table = create_prime_tablename("trltitl", "s", agg_str)
    trltitl_h_agg_table = create_prime_tablename("trltitl", "h", agg_str)
    trltitl_s_raw_table = create_prime_tablename("trltitl", "s", raw_str)
    trltitl_s_val_table = create_prime_tablename("trltitl", "s", vld_str)
    trlcore_s_raw_table = create_prime_tablename("trlcore", "s", raw_str)
    trlcore_s_agg_table = create_prime_tablename("trlcore", "s", agg_str)
    blrpern_job_table = create_prime_tablename("blrpern", wx.job, None)
    x_blrpern_raw = create_prime_tablename("blrpern", "k", raw_str)
    blrgrou_job_table = create_prime_tablename("blrgrou", wx.job, None)

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
    assert trlname_s_agg_table == f"{trlname_dimen}_s_agg"
    assert trllabe_s_agg_table == f"{trllabe_dimen}_s_agg"
    assert trlrope_s_agg_table == f"{trlrope_dimen}_s_agg"
    assert trltitl_s_agg_table == f"{trltitl_dimen}_s_agg"
    assert trltitl_h_agg_table == f"{trltitl_dimen}_h_agg"
    assert trltitl_s_raw_table == f"{trltitl_dimen}_s_raw"
    assert trltitl_s_val_table == f"{trltitl_dimen}_s_vld"
    assert trlcore_s_raw_table == f"{trlcore_dimen}_s_raw"
    assert trlcore_s_agg_table == f"{trlcore_dimen}_s_agg"
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
        if dimen_config.get(wx.idea_category) != "translate"
        # if dimen_config.get(wx.idea_category) == "moment"
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
        if dimen_config.get(wx.idea_category) != "translate"
        # if dimen_config.get(wx.idea_category) == "moment"
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
CREATE TABLE IF NOT EXISTS {wx.moment_event_time_agg} (
  {wx.moment_label} TEXT
, {wx.event_int} INTEGER
, agg_time INTEGER
, {wx.error_message} TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_MOMENT_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO {wx.moment_event_time_agg} ({wx.moment_label}, {wx.event_int}, agg_time)
SELECT {wx.moment_label}, {wx.event_int}, agg_time
FROM (
    SELECT {wx.moment_label}, {wx.event_int}, {wx.tran_time} as agg_time
    FROM moment_paybook_raw
    GROUP BY {wx.moment_label}, {wx.event_int}, {wx.tran_time}
    UNION 
    SELECT {wx.moment_label}, {wx.event_int}, {wx.bud_time} as agg_time
    FROM moment_budunit_raw
    GROUP BY {wx.moment_label}, {wx.event_int}, {wx.bud_time}
)
ORDER BY {wx.moment_label}, {wx.event_int}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_MOMENT_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {wx.moment_label}, {wx.event_int}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {wx.moment_label} ORDER BY {wx.event_int}) AS prev_agg_time
    FROM {wx.moment_event_time_agg}
)
UPDATE {wx.moment_event_time_agg}
SET {wx.error_message} = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{wx.event_int} = {wx.moment_event_time_agg}.{wx.event_int}
    AND EventTimeOrdered.{wx.moment_label} = {wx.moment_event_time_agg}.{wx.moment_label}
    AND EventTimeOrdered.agg_time = {wx.moment_event_time_agg}.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_MOMENT_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_MOMENT_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {wx.moment_ote1_agg} (
  {wx.moment_label} TEXT
, {wx.belief_name} TEXT
, {wx.event_int} INTEGER
, {wx.bud_time} INTEGER
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
    momentbud_h_raw_tablename = create_prime_tablename(wx.moment_budunit, "h", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO {wx.moment_ote1_agg} ({wx.moment_label}, {wx.belief_name}, {wx.event_int}, {wx.bud_time})
SELECT {wx.moment_label}, {wx.belief_name}, {wx.event_int}, {wx.bud_time}
FROM (
    SELECT 
      {wx.moment_label}_inx {wx.moment_label}
    , {wx.belief_name}_inx {wx.belief_name}
    , {wx.event_int}
    , {wx.bud_time}
    FROM {momentbud_h_raw_tablename}
    GROUP BY {wx.moment_label}_inx, {wx.belief_name}_inx, {wx.event_int}, {wx.bud_time}
)
ORDER BY {wx.moment_label}, {wx.belief_name}, {wx.event_int}, {wx.bud_time}
;
"""
    # WHEN / THEN
    assert INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR == expected_INSERT_sqlstr


def test_CREATE_MOMENT_VOICE_NETS_SQLSTR_Exists():
    # ESTABLISH
    sqlite_types = get_idea_sqlite_types()
    sqlite_types[wx.belief_net_amount] = "REAL"
    expected_create_table_sqlstr = get_create_table_sqlstr(
        tablename=wx.moment_voice_nets,
        columns_list=[
            wx.moment_label,
            wx.belief_name,
            wx.belief_net_amount,
        ],
        column_types=sqlite_types,
    )

    # WHEN / THEN
    assert CREATE_MOMENT_VOICE_NETS_SQLSTR == expected_create_table_sqlstr
