from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.a02_finance_logic._util.a02_str import (
    bud_time_str,
    owner_name_str,
    tran_time_str,
    vow_label_str,
)
from src.a06_plan_logic._util.a06_str import (
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.atom_config import get_delete_key_name
from src.a09_pack_logic._util.a09_str import event_int_str
from src.a10_plan_calc._util.a10_str import plan_groupunit_str
from src.a12_hub_toolbox._util.a12_str import job_str, vow_ote1_agg_str
from src.a15_vow_logic._util.a15_str import (
    vow_budunit_str,
    vow_paybook_str,
    vow_timeline_hour_str,
    vow_timeline_month_str,
    vow_timeline_weekday_str,
    vow_timeoffi_str,
    vowunit_str,
)
from src.a16_pidgin_logic._util.a16_str import (
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
)
from src.a17_idea_logic._util.a17_str import brick_raw, idea_category_str
from src.a17_idea_logic.idea_config import (
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.a17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.a18_etl_toolbox._util.a18_str import (
    owner_net_amount_str,
    vow_acct_nets_str,
    vow_event_time_agg_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    CREATE_VOW_ACCT_NETS_SQLSTR,
    CREATE_VOW_EVENT_TIME_AGG_SQLSTR,
    CREATE_VOW_OTE1_AGG_SQLSTR,
    IDEA_STAGEBLE_DEL_DIMENS,
    INSERT_VOW_EVENT_TIME_AGG_SQLSTR,
    INSERT_VOW_OTE1_AGG_FROM_VOICE_SQLSTR,
    UPDATE_ERROR_MESSAGE_VOW_EVENT_TIME_AGG_SQLSTR,
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
    planunit_dimen = planunit_str()
    plnacct_dimen = plan_acctunit_str()
    plnmemb_dimen = plan_acct_membership_str()
    plngrou_dimen = plan_groupunit_str()
    plnconc_dimen = plan_conceptunit_str()
    plnawar_dimen = plan_concept_awardlink_str()
    plnreas_dimen = plan_concept_reasonunit_str()
    plnprem_dimen = plan_concept_reason_premiseunit_str()
    plnlabo_dimen = plan_concept_laborlink_str()
    plnheal_dimen = plan_concept_healerlink_str()
    plnfact_dimen = plan_concept_factunit_str()
    vowunit_dimen = vowunit_str()
    vowpayy_dimen = vow_paybook_str()
    vowbudd_dimen = vow_budunit_str()
    vowhour_dimen = vow_timeline_hour_str()
    vowmont_dimen = vow_timeline_month_str()
    vowweek_dimen = vow_timeline_weekday_str()
    vowoffi_dimen = vow_timeoffi_str()
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
    planunit_s_agg_table = create_prime_tablename("planunit", "s", agg_str, put_str)
    plnacct_s_agg_table = create_prime_tablename("plnacct", "s", agg_str, put_str)
    plnmemb_s_agg_table = create_prime_tablename("plnmemb", "s", agg_str, put_str)
    plnconc_s_agg_table = create_prime_tablename("plnconc", "s", agg_str, put_str)
    plnawar_s_agg_table = create_prime_tablename("plnawar", "s", agg_str, put_str)
    plnreas_s_agg_table = create_prime_tablename("plnreas", "s", agg_str, put_str)
    plnprem_s_agg_table = create_prime_tablename("plnprem", "s", agg_str, put_str)
    plnlabo_s_agg_table = create_prime_tablename("PLNLABO", "s", agg_str, put_str)
    plnheal_s_agg_table = create_prime_tablename("plnheal", "s", agg_str, put_str)
    plnfact_s_agg_table = create_prime_tablename("plnfact", "s", agg_str, put_str)
    plnfact_s_del_table = create_prime_tablename("plnfact", "s", agg_str, del_str)
    vowunit_s_agg_table = create_prime_tablename("vowunit", "s", agg_str)
    vowpayy_s_agg_table = create_prime_tablename("vowpayy", "s", agg_str)
    vowbudd_s_agg_table = create_prime_tablename("vowbudd", "s", agg_str)
    vowhour_s_agg_table = create_prime_tablename("vowhour", "s", agg_str)
    vowmont_s_agg_table = create_prime_tablename("vowmont", "s", agg_str)
    vowweek_s_agg_table = create_prime_tablename("vowweek", "s", agg_str)
    vowoffi_s_agg_table = create_prime_tablename("vowoffi", "s", agg_str)
    pidname_s_agg_table = create_prime_tablename("pidname", "s", agg_str)
    pidlabe_s_agg_table = create_prime_tablename("pidlabe", "s", agg_str)
    pidrope_s_agg_table = create_prime_tablename("pidrope", "s", agg_str)
    pidtitl_s_agg_table = create_prime_tablename("pidtitl", "s", agg_str)
    pidtitl_v_agg_table = create_prime_tablename("pidtitl", "v", agg_str)
    pidtitl_s_raw_table = create_prime_tablename("pidtitl", "s", raw_str)
    pidtitl_s_val_table = create_prime_tablename("pidtitl", "s", vld_str)
    pidcore_s_raw_table = create_prime_tablename("pidcore", "s", raw_str)
    pidcore_s_agg_table = create_prime_tablename("pidcore", "s", agg_str)
    plnacct_job_table = create_prime_tablename("plnacct", job_str(), None)
    x_plnacct_raw = create_prime_tablename("plnacct", "k", raw_str)
    plngrou_job_table = create_prime_tablename("plngrou", job_str(), None)

    # THEN
    assert planunit_s_agg_table == f"{planunit_dimen}_s_put_agg"
    assert plnacct_s_agg_table == f"{plnacct_dimen}_s_put_agg"
    assert plnmemb_s_agg_table == f"{plnmemb_dimen}_s_put_agg"
    assert plnconc_s_agg_table == f"{plnconc_dimen}_s_put_agg"
    assert plnawar_s_agg_table == f"{plnawar_dimen}_s_put_agg"
    assert plnreas_s_agg_table == f"{plnreas_dimen}_s_put_agg"
    assert plnprem_s_agg_table == f"{plnprem_dimen}_s_put_agg"
    assert plnlabo_s_agg_table == f"{plnlabo_dimen}_s_put_agg"
    assert plnheal_s_agg_table == f"{plnheal_dimen}_s_put_agg"
    assert plnfact_s_agg_table == f"{plnfact_dimen}_s_put_agg"
    assert plnfact_s_del_table == f"{plnfact_dimen}_s_del_agg"
    assert vowunit_s_agg_table == f"{vowunit_dimen}_s_agg"
    assert vowpayy_s_agg_table == f"{vowpayy_dimen}_s_agg"
    assert vowbudd_s_agg_table == f"{vowbudd_dimen}_s_agg"
    assert vowhour_s_agg_table == f"{vowhour_dimen}_s_agg"
    assert vowmont_s_agg_table == f"{vowmont_dimen}_s_agg"
    assert vowweek_s_agg_table == f"{vowweek_dimen}_s_agg"
    assert vowoffi_s_agg_table == f"{vowoffi_dimen}_s_agg"
    assert pidname_s_agg_table == f"{pidname_dimen}_s_agg"
    assert pidlabe_s_agg_table == f"{pidlabe_dimen}_s_agg"
    assert pidrope_s_agg_table == f"{pidrope_dimen}_s_agg"
    assert pidtitl_s_agg_table == f"{pidtitl_dimen}_s_agg"
    assert pidtitl_v_agg_table == f"{pidtitl_dimen}_v_agg"
    assert pidtitl_s_raw_table == f"{pidtitl_dimen}_s_raw"
    assert pidtitl_s_val_table == f"{pidtitl_dimen}_s_vld"
    assert pidcore_s_raw_table == f"{pidcore_dimen}_s_raw"
    assert pidcore_s_agg_table == f"{pidcore_dimen}_s_agg"
    assert plnacct_job_table == f"{plnacct_dimen}_job"
    assert plngrou_job_table == f"{plngrou_dimen}_job"
    assert x_plnacct_raw == "plan_acctunit_raw"


def test_create_all_idea_tables_CreatesVowRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
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
        # if dimen_config.get(idea_category_str()) == "vow"
    }
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
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
    print(f"{expected_idea_slabelable_dimens=}")
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
        # if dimen_config.get(idea_category_str()) == "vow"
    }
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
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


def test_CREATE_VOW_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {vow_event_time_agg_str()} (
  {vow_label_str()} TEXT
, {event_int_str()} INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_VOW_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_VOW_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO {vow_event_time_agg_str()} ({vow_label_str()}, {event_int_str()}, agg_time)
SELECT {vow_label_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {vow_label_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM vow_paybook_raw
    GROUP BY {vow_label_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {vow_label_str()}, {event_int_str()}, {bud_time_str()} as agg_time
    FROM vow_budunit_raw
    GROUP BY {vow_label_str()}, {event_int_str()}, {bud_time_str()}
)
ORDER BY {vow_label_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_VOW_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_VOW_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {vow_label_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {vow_label_str()} ORDER BY {event_int_str()}) AS prev_agg_time
    FROM {vow_event_time_agg_str()}
)
UPDATE {vow_event_time_agg_str()}
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{event_int_str()} = {vow_event_time_agg_str()}.{event_int_str()}
    AND EventTimeOrdered.{vow_label_str()} = {vow_event_time_agg_str()}.{vow_label_str()}
    AND EventTimeOrdered.agg_time = {vow_event_time_agg_str()}.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_VOW_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_VOW_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {vow_ote1_agg_str()} (
  {vow_label_str()} TEXT
, {owner_name_str()} TEXT
, {event_int_str()} INTEGER
, {bud_time_str()} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_VOW_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# TODO create test to prove this insert should grab minimun event_int instead of just event_int
# TODO create test to prove this insert should never grab when error message is not null in source table
def test_INSERT_VOW_OTE1_AGG_FROM_VOICE_SQLSTR_Exists():
    # ESTABLISH
    vowbud_v_raw_tablename = create_prime_tablename(vow_budunit_str(), "v", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO {vow_ote1_agg_str()} ({vow_label_str()}, {owner_name_str()}, {event_int_str()}, {bud_time_str()})
SELECT {vow_label_str()}, {owner_name_str()}, {event_int_str()}, {bud_time_str()}
FROM (
    SELECT 
      {vow_label_str()}_inx {vow_label_str()}
    , {owner_name_str()}_inx {owner_name_str()}
    , {event_int_str()}
    , {bud_time_str()}
    FROM {vowbud_v_raw_tablename}
    GROUP BY {vow_label_str()}_inx, {owner_name_str()}_inx, {event_int_str()}, {bud_time_str()}
)
ORDER BY {vow_label_str()}, {owner_name_str()}, {event_int_str()}, {bud_time_str()}
;
"""
    # WHEN / THEN
    assert INSERT_VOW_OTE1_AGG_FROM_VOICE_SQLSTR == expected_INSERT_sqlstr


def test_CREATE_VOW_ACCT_NETS_SQLSTR_Exists():
    # ESTABLISH
    sqlite_types = get_idea_sqlite_types()
    sqlite_types[owner_net_amount_str()] = "REAL"
    expected_create_table_sqlstr = get_create_table_sqlstr(
        tablename=vow_acct_nets_str(),
        columns_list=[vow_label_str(), owner_name_str(), owner_net_amount_str()],
        column_types=sqlite_types,
    )

    # WHEN / THEN
    assert CREATE_VOW_ACCT_NETS_SQLSTR == expected_create_table_sqlstr
