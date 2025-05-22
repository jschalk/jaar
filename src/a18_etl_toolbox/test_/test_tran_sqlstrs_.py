from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    get_create_table_sqlstr,
    create_table2table_agg_insert_query,
    get_table_columns,
    required_columns_exist,
    create_select_query,
)
from src.a02_finance_logic._utils.strs_a02 import (
    fisc_label_str,
    owner_name_str,
    deal_time_str,
    tran_time_str,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    event_int_str,
    face_name_str,
)
from src.a07_calendar_logic._utils.str_a07 import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a08_bud_atom_logic.atom_config import get_bud_dimens, get_delete_key_name
from src.a15_fisc_logic._utils.str_a15 import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a15_fisc_logic.fisc_config import get_fisc_dimens
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_title_str,
    pidgin_name_str,
    pidgin_way_str,
    pidgin_label_str,
    pidgin_core_str,
)
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import (
    get_idea_sqlite_types,
    get_idea_config_dict,
    get_idea_numbers,
)
from src.a17_idea_logic.idea_db_tool import (
    get_pragma_table_fetchall,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    get_dimen_abbv7,
    create_prime_tablename,
    create_all_idea_tables,
    create_sound_and_voice_tables,
    get_idea_stageble_put_dimens,
    IDEA_STAGEBLE_DEL_DIMENS,
    CREATE_FISC_EVENT_TIME_AGG_SQLSTR,
    INSERT_FISC_EVENT_TIME_AGG_SQLSTR,
    UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR,
    CREATE_FISC_OTE1_AGG_SQLSTR,
    INSERT_FISC_OTE1_AGG_FROM_VOICE_SQLSTR,
)
from sqlite3 import connect as sqlite3_connect


def abbv(tablename: str) -> str:
    abbrevions = {
        f"{bud_acct_membership_str()}_put_agg": "BUDMEMB_PUT_AGG",
        f"{bud_acct_membership_str()}_put_raw": "BUDMEMB_PUT_RAW",
        f"{bud_acctunit_str()}_put_agg": "BUDACCT_PUT_AGG",
        f"{bud_acctunit_str()}_put_raw": "BUDACCT_PUT_RAW",
        f"{bud_concept_awardlink_str()}_put_agg": "BUDAWAR_PUT_AGG",
        f"{bud_concept_awardlink_str()}_put_raw": "BUDAWAR_PUT_RAW",
        f"{bud_concept_factunit_str()}_put_agg": "BUDFACT_PUT_AGG",
        f"{bud_concept_factunit_str()}_put_raw": "BUDFACT_PUT_RAW",
        f"{bud_concept_healerlink_str()}_put_agg": "BUDHEAL_PUT_AGG",
        f"{bud_concept_healerlink_str()}_put_raw": "BUDHEAL_PUT_RAW",
        f"{bud_concept_reason_premiseunit_str()}_put_agg": "BUDPREM_PUT_AGG",
        f"{bud_concept_reason_premiseunit_str()}_put_raw": "BUDPREM_PUT_RAW",
        f"{bud_concept_reasonunit_str()}_put_agg": "BUDREAS_PUT_AGG",
        f"{bud_concept_reasonunit_str()}_put_raw": "BUDREAS_PUT_RAW",
        f"{bud_concept_laborlink_str()}_put_agg": "BUDLABO_PUT_AGG",
        f"{bud_concept_laborlink_str()}_put_raw": "BUDLABO_PUT_RAW",
        f"{bud_conceptunit_str()}_put_agg": "BUDCONC_PUT_AGG",
        f"{bud_conceptunit_str()}_put_raw": "BUDCONC_PUT_RAW",
        f"{budunit_str()}_put_agg": "BUDUNIT_PUT_AGG",
        f"{budunit_str()}_put_raw": "BUDUNIT_PUT_RAW",
        f"{bud_acct_membership_str()}_del_agg": "BUDMEMB_DEL_AGG",
        f"{bud_acct_membership_str()}_del_raw": "BUDMEMB_DEL_RAW",
        f"{bud_acctunit_str()}_del_agg": "BUDACCT_DEL_AGG",
        f"{bud_acctunit_str()}_del_raw": "BUDACCT_DEL_RAW",
        f"{bud_concept_awardlink_str()}_del_agg": "BUDAWAR_DEL_AGG",
        f"{bud_concept_awardlink_str()}_del_raw": "BUDAWAR_DEL_RAW",
        f"{bud_concept_factunit_str()}_del_agg": "BUDFACT_DEL_AGG",
        f"{bud_concept_factunit_str()}_del_raw": "BUDFACT_DEL_RAW",
        f"{bud_concept_healerlink_str()}_del_agg": "BUDHEAL_DEL_AGG",
        f"{bud_concept_healerlink_str()}_del_raw": "BUDHEAL_DEL_RAW",
        f"{bud_concept_reason_premiseunit_str()}_del_agg": "BUDPREM_DEL_AGG",
        f"{bud_concept_reason_premiseunit_str()}_del_raw": "BUDPREM_DEL_RAW",
        f"{bud_concept_reasonunit_str()}_del_agg": "BUDREAS_DEL_AGG",
        f"{bud_concept_reasonunit_str()}_del_raw": "BUDREAS_DEL_RAW",
        f"{bud_concept_laborlink_str()}_del_agg": "BUDLABO_DEL_AGG",
        f"{bud_concept_laborlink_str()}_del_raw": "BUDLABO_DEL_RAW",
        f"{bud_conceptunit_str()}_del_agg": "BUDCONC_DEL_AGG",
        f"{bud_conceptunit_str()}_del_raw": "BUDCONC_DEL_RAW",
        f"{budunit_str()}_del_agg": "BUDUNIT_DEL_AGG",
        f"{budunit_str()}_del_raw": "BUDUNIT_DEL_RAW",
    }
    return abbrevions.get(tablename)


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    budunit_dimen = budunit_str()
    budacct_dimen = bud_acctunit_str()
    budmemb_dimen = bud_acct_membership_str()
    budconc_dimen = bud_conceptunit_str()
    budawar_dimen = bud_concept_awardlink_str()
    budreas_dimen = bud_concept_reasonunit_str()
    budprem_dimen = bud_concept_reason_premiseunit_str()
    budlabor_dimen = bud_concept_laborlink_str()
    budheal_dimen = bud_concept_healerlink_str()
    budfact_dimen = bud_concept_factunit_str()
    fisunit_dimen = fiscunit_str()
    fiscash_dimen = fisc_cashbook_str()
    fisdeal_dimen = fisc_dealunit_str()
    fishour_dimen = fisc_timeline_hour_str()
    fismont_dimen = fisc_timeline_month_str()
    fisweek_dimen = fisc_timeline_weekday_str()
    fisoffi_dimen = fisc_timeoffi_str()
    pidname_dimen = pidgin_name_str()
    pidlabe_dimen = pidgin_label_str()
    pidwayy_dimen = pidgin_way_str()
    pidtitl_dimen = pidgin_title_str()
    pidcore_dimen = pidgin_core_str()
    raw_str = "raw"
    agg_str = "agg"
    vld_str = "vld"
    put_str = "put"
    del_str = "del"

    # WHEN
    budunit_s_agg_table = create_prime_tablename("budunit", "s", agg_str, put_str)
    budacct_s_agg_table = create_prime_tablename("budacct", "s", agg_str, put_str)
    budmemb_s_agg_table = create_prime_tablename("budmemb", "s", agg_str, put_str)
    budconc_s_agg_table = create_prime_tablename("budconc", "s", agg_str, put_str)
    budawar_s_agg_table = create_prime_tablename("budawar", "s", agg_str, put_str)
    budreas_s_agg_table = create_prime_tablename("budreas", "s", agg_str, put_str)
    budprem_s_agg_table = create_prime_tablename("budprem", "s", agg_str, put_str)
    budlabor_s_agg_table = create_prime_tablename("BUDLABO", "s", agg_str, put_str)
    budheal_s_agg_table = create_prime_tablename("budheal", "s", agg_str, put_str)
    budfact_s_agg_table = create_prime_tablename("budfact", "s", agg_str, put_str)
    budfact_s_del_table = create_prime_tablename("budfact", "s", agg_str, del_str)
    fisunit_s_agg_table = create_prime_tablename("fisunit", "s", agg_str)
    fiscash_s_agg_table = create_prime_tablename("fiscash", "s", agg_str)
    fisdeal_s_agg_table = create_prime_tablename("fisdeal", "s", agg_str)
    fishour_s_agg_table = create_prime_tablename("fishour", "s", agg_str)
    fismont_s_agg_table = create_prime_tablename("fismont", "s", agg_str)
    fisweek_s_agg_table = create_prime_tablename("fisweek", "s", agg_str)
    fisoffi_s_agg_table = create_prime_tablename("fisoffi", "s", agg_str)
    pidname_s_agg_table = create_prime_tablename("pidname", "s", agg_str)
    pidlabe_s_agg_table = create_prime_tablename("pidlabe", "s", agg_str)
    pidwayy_s_agg_table = create_prime_tablename("pidwayy", "s", agg_str)
    pidtitl_s_agg_table = create_prime_tablename("pidtitl", "s", agg_str)
    pidtitl_v_agg_table = create_prime_tablename("pidtitl", "v", agg_str)
    pidtitl_s_raw_table = create_prime_tablename("pidtitl", "s", raw_str)
    pidtitl_s_val_table = create_prime_tablename("pidtitl", "s", vld_str)
    pidcore_s_raw_table = create_prime_tablename("pidcore", "s", raw_str)
    pidcore_s_agg_table = create_prime_tablename("pidcore", "s", agg_str)

    # THEN
    assert budunit_s_agg_table == f"{budunit_dimen}_s_put_agg"
    assert budacct_s_agg_table == f"{budacct_dimen}_s_put_agg"
    assert budmemb_s_agg_table == f"{budmemb_dimen}_s_put_agg"
    assert budconc_s_agg_table == f"{budconc_dimen}_s_put_agg"
    assert budawar_s_agg_table == f"{budawar_dimen}_s_put_agg"
    assert budreas_s_agg_table == f"{budreas_dimen}_s_put_agg"
    assert budprem_s_agg_table == f"{budprem_dimen}_s_put_agg"
    assert budlabor_s_agg_table == f"{budlabor_dimen}_s_put_agg"
    assert budheal_s_agg_table == f"{budheal_dimen}_s_put_agg"
    assert budfact_s_agg_table == f"{budfact_dimen}_s_put_agg"
    assert budfact_s_del_table == f"{budfact_dimen}_s_del_agg"
    assert fisunit_s_agg_table == f"{fisunit_dimen}_s_agg"
    assert fiscash_s_agg_table == f"{fiscash_dimen}_s_agg"
    assert fisdeal_s_agg_table == f"{fisdeal_dimen}_s_agg"
    assert fishour_s_agg_table == f"{fishour_dimen}_s_agg"
    assert fismont_s_agg_table == f"{fismont_dimen}_s_agg"
    assert fisweek_s_agg_table == f"{fisweek_dimen}_s_agg"
    assert fisoffi_s_agg_table == f"{fisoffi_dimen}_s_agg"
    assert pidname_s_agg_table == f"{pidname_dimen}_s_agg"
    assert pidlabe_s_agg_table == f"{pidlabe_dimen}_s_agg"
    assert pidwayy_s_agg_table == f"{pidwayy_dimen}_s_agg"
    assert pidtitl_s_agg_table == f"{pidtitl_dimen}_s_agg"
    assert pidtitl_v_agg_table == f"{pidtitl_dimen}_v_agg"
    assert pidtitl_s_raw_table == f"{pidtitl_dimen}_s_raw"
    assert pidtitl_s_val_table == f"{pidtitl_dimen}_s_vld"
    assert pidcore_s_raw_table == f"{pidcore_dimen}_s_raw"
    assert pidcore_s_agg_table == f"{pidcore_dimen}_s_agg"


def test_create_all_idea_tables_CreatesFiscRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
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
        # if dimen_config.get(idea_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
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
        # if dimen_config.get(idea_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
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


def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  {fisc_label_str()} TEXT
, {event_int_str()} INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO fisc_event_time_agg ({fisc_label_str()}, {event_int_str()}, agg_time)
SELECT {fisc_label_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {fisc_label_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM fisc_cashbook_raw
    GROUP BY {fisc_label_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {fisc_label_str()}, {event_int_str()}, {deal_time_str()} as agg_time
    FROM fisc_dealunit_raw
    GROUP BY {fisc_label_str()}, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_label_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {fisc_label_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {fisc_label_str()} ORDER BY {event_int_str()}) AS prev_agg_time
    FROM fisc_event_time_agg
)
UPDATE fisc_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{event_int_str()} = fisc_event_time_agg.{event_int_str()}
    AND EventTimeOrdered.{fisc_label_str()} = fisc_event_time_agg.{fisc_label_str()}
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  {fisc_label_str()} TEXT
, {owner_name_str()} TEXT
, {event_int_str()} INTEGER
, {deal_time_str()} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# TODO create test to prove this insert should grab minimun event_int instead of just event_int
# TODO create test to prove this insert should never grab when error message is not null in source table
def test_INSERT_FISC_OTE1_AGG_FROM_VOICE_SQLSTR_Exists():
    # ESTABLISH
    fisdeal_v_raw_tablename = create_prime_tablename(fisc_dealunit_str(), "v", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO fisc_ote1_agg ({fisc_label_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()})
SELECT {fisc_label_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
FROM (
    SELECT 
      {fisc_label_str()}_inx {fisc_label_str()}
    , {owner_name_str()}_inx {owner_name_str()}
    , {event_int_str()}
    , {deal_time_str()}
    FROM {fisdeal_v_raw_tablename}
    GROUP BY {fisc_label_str()}_inx, {owner_name_str()}_inx, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_label_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
;
"""
    # WHEN / THEN
    assert INSERT_FISC_OTE1_AGG_FROM_VOICE_SQLSTR == expected_INSERT_sqlstr
