from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
)
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import get_idea_sqlite_types, get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.tran_sqlstrs import (
    get_pidgin_prime_create_table_sqlstrs,
    create_pidgin_prime_tables,
)
from sqlite3 import connect as sqlite3_connect


def short_abbv(dimen: str) -> str:
    return {
        "pidgin_label": "PIDLABE",
        "pidgin_name": "PIDNAME",
        "pidgin_road": "PIDROAD",
        "pidgin_tag": "PIDTAGG",
    }.get(dimen)


def test_get_pidgin_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_pidgin_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "pidgin"
    }
    sqlite_types = get_idea_sqlite_types()
    for x_dimen in idea_config:
        # print(f"{x_dimen} checking...")
        x_config = idea_config.get(x_dimen)

        raw_table = f"{x_dimen}_raw"
        raw_cols = set(x_config.get("jkeys").keys())
        raw_cols.update(set(x_config.get("jvalues").keys()))
        raw_cols.add("idea_number")
        raw_cols.add("error_message")
        raw_cols = get_default_sorted_list(raw_cols)
        ex_raw_sqlstr = get_create_table_sqlstr(raw_table, raw_cols, sqlite_types)
        raw_create_sqlstr = create_table_sqlstrs.get(raw_table)
        assert raw_create_sqlstr == ex_raw_sqlstr

        agg_table = f"{x_dimen}_agg"
        agg_cols = set(x_config.get("jkeys").keys())
        agg_cols.update(set(x_config.get("jvalues").keys()))
        agg_cols = get_default_sorted_list(agg_cols)
        ex_agg_sqlstr = get_create_table_sqlstr(agg_table, agg_cols, sqlite_types)
        agg_create_sqlstr = create_table_sqlstrs.get(agg_table)
        assert agg_create_sqlstr == ex_agg_sqlstr

        # abbv7 = short_abbv(x_dimen)
        # print(f'CREATE_{abbv7.upper()}_RAW_SQLSTR= """{ex_raw_sqlstr}"""')
        # print(f'CREATE_{abbv7.upper()}_AGG_SQLSTR= """{ex_agg_sqlstr}"""')
        # print(f'"{raw_table}": CREATE_{raw_table.upper()}_SQLSTR,')
        # print(f'"{agg_table}": CREATE_{agg_table.upper()}_SQLSTR,')


def test_get_bud_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    pidgin_create_table_sqlstrs = get_pidgin_prime_create_table_sqlstrs()

    # THEN
    assert pidgin_create_table_sqlstrs
    bud_dimens = get_pidgin_dimens()
    expected_bud_tablenames = {f"{x_dimen}_agg" for x_dimen in bud_dimens}
    expected_bud_tablenames.update({f"{x_dimen}_raw" for x_dimen in bud_dimens})
    print(f"{expected_bud_tablenames=}")
    assert set(pidgin_create_table_sqlstrs.keys()) == expected_bud_tablenames


def test_create_pidgin_prime_tables_CreatesPidginPrimeTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        pidname_raw_table = "pidgin_label_raw"
        pidname_agg_table = "pidgin_label_agg"
        pidtagg_raw_table = "pidgin_name_raw"
        pidtagg_agg_table = "pidgin_name_agg"
        pidroad_raw_table = "pidgin_road_raw"
        pidroad_agg_table = "pidgin_road_agg"
        pidlabe_raw_table = "pidgin_tag_raw"
        pidlabe_agg_table = "pidgin_tag_agg"
        cursor = fisc_db_conn.cursor()
        assert not db_table_exists(cursor, pidname_raw_table)
        assert not db_table_exists(cursor, pidname_agg_table)
        assert not db_table_exists(cursor, pidtagg_raw_table)
        assert not db_table_exists(cursor, pidtagg_agg_table)
        assert not db_table_exists(cursor, pidroad_raw_table)
        assert not db_table_exists(cursor, pidroad_agg_table)
        assert not db_table_exists(cursor, pidlabe_raw_table)
        assert not db_table_exists(cursor, pidlabe_agg_table)

        # WHEN
        create_pidgin_prime_tables(cursor)

        # THEN
        assert db_table_exists(cursor, pidname_raw_table)
        assert db_table_exists(cursor, pidname_agg_table)
        assert db_table_exists(cursor, pidtagg_raw_table)
        assert db_table_exists(cursor, pidtagg_agg_table)
        assert db_table_exists(cursor, pidroad_raw_table)
        assert db_table_exists(cursor, pidroad_agg_table)
        assert db_table_exists(cursor, pidlabe_raw_table)
        assert db_table_exists(cursor, pidlabe_agg_table)

        pidname_raw_columns = get_table_columns(cursor, pidname_raw_table)
        pidname_agg_columns = get_table_columns(cursor, pidname_agg_table)
        pidtagg_raw_columns = get_table_columns(cursor, pidtagg_raw_table)
        pidtagg_agg_columns = get_table_columns(cursor, pidtagg_agg_table)
        pidroad_raw_columns = get_table_columns(cursor, pidroad_raw_table)
        pidroad_agg_columns = get_table_columns(cursor, pidroad_agg_table)
        pidlabe_raw_columns = get_table_columns(cursor, pidlabe_raw_table)
        pidlabe_agg_columns = get_table_columns(cursor, pidlabe_agg_table)

        print(f"{pidname_raw_columns=}")
        print(f"{pidname_agg_columns=}")
        assert "error_message" in pidname_raw_columns
        assert "error_message" not in pidname_agg_columns
        assert "error_message" in pidtagg_raw_columns
        assert "error_message" not in pidtagg_agg_columns
        assert "error_message" in pidroad_raw_columns
        assert "error_message" not in pidroad_agg_columns
        assert "error_message" in pidlabe_raw_columns
        assert "error_message" not in pidlabe_agg_columns
        assert idea_number_str() in pidname_raw_columns
        assert idea_number_str() not in pidname_agg_columns
        assert idea_number_str() in pidtagg_raw_columns
        assert idea_number_str() not in pidtagg_agg_columns
        assert idea_number_str() in pidroad_raw_columns
        assert idea_number_str() not in pidroad_agg_columns
        assert idea_number_str() in pidlabe_raw_columns
        assert idea_number_str() not in pidlabe_agg_columns
        assert len(pidname_raw_columns) == 9
        assert len(pidname_agg_columns) == 7
        assert len(pidtagg_raw_columns) == 9
        assert len(pidtagg_agg_columns) == 7
        assert len(pidroad_raw_columns) == 9
        assert len(pidroad_agg_columns) == 7
        assert len(pidlabe_raw_columns) == 9
        assert len(pidlabe_agg_columns) == 7


# def test_get_fisc_inconsistency_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_inconsistency_sqlstrs = get_fisc_inconsistency_sqlstrs()

#     # THEN
#     assert fisc_inconsistency_sqlstrs.keys() == get_fisc_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         # if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "bud"
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }

#     exclude_cols = {
#         idea_number_str(),
#         face_name_str(),
#         event_int_str(),
#         "error_message",
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_fisc_prime_tables(cursor)

#         for x_dimen in sorted(idea_config):
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = fisc_inconsistency_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_select_inconsistency_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             print(f'{x_dimen}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""')
#             print(f'{x_sqlstr=}"""')
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_bud_inconsistency_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_inconsistency_sqlstrs = get_bud_inconsistency_sqlstrs()

#     # THEN
#     assert bud_inconsistency_sqlstrs.keys() == get_bud_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }

#     exclude_cols = {idea_number_str(), "error_message"}
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in sorted(idea_config):
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_put_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_select_inconsistency_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             print(
#                 f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""'
#             )
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_fisc_update_inconsist_error_message_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_update_error_sqlstrs = get_fisc_update_inconsist_error_message_sqlstrs()

#     # THEN
#     assert set(fisc_update_error_sqlstrs.keys()) == get_fisc_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }

#     exclude_cols = {
#         idea_number_str(),
#         face_name_str(),
#         event_int_str(),
#         "error_message",
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             x_sqlstr = fisc_update_error_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_update_inconsistency_error_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             # print(
#             #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
#             # )
#             # print(
#             #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
#             # )
#             # print(f"""            {x_sqlstr=}""")
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_bud_put_update_inconsist_error_message_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_update_error_sqlstrs = get_bud_put_update_inconsist_error_message_sqlstrs()

#     # THEN
#     assert set(bud_update_error_sqlstrs.keys()) == get_bud_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }

#     exclude_cols = {idea_number_str(), "error_message"}
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_put_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_update_inconsistency_error_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             print(
#                 f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
#             )
#             print(
#                 f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
#             )
#             print(f"""            {x_sqlstr=}""")
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_fisc_insert_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: extract-method, no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_insert_agg_sqlstrs = get_fisc_insert_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(fisc_insert_agg_sqlstrs.keys()) == get_fisc_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         face_name_str(),
#         event_int_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_fisc_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns.remove(event_int_str())
#             dimen_focus_columns.remove(face_name_str())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             raw_tablename = f"{x_dimen}_raw"
#             agg_tablename = f"{x_dimen}_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = fisc_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr

#         generated_fiscunit_sqlstr = create_table2table_agg_insert_query(
#             cursor,
#             src_table=f"{fiscunit_str()}_raw",
#             dst_table=f"{fiscunit_str()}_agg",
#             focus_cols=[fisc_tag_str()],
#             exclude_cols=x_exclude_cols,
#         )
#         assert FISUNIT_AGG_INSERT_SQLSTR == generated_fiscunit_sqlstr
#         columns_header = f"""{fisc_tag_str()}, {timeline_tag_str()}, {c400_number_str()}, {yr1_jan1_offset_str()}, {monthday_distortion_str()}, fund_coin, penny, respect_bit, bridge, job_listen_rotations"""
#         tablename = "fiscunit"
#         expected_fiscunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
# SELECT {fisc_tag_str()}, MAX({timeline_tag_str()}), MAX({c400_number_str()}), MAX({yr1_jan1_offset_str()}), MAX({monthday_distortion_str()}), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
# FROM {tablename}_raw
# WHERE error_message IS NULL
# GROUP BY {fisc_tag_str()}
# ;
# """
#         assert FISUNIT_AGG_INSERT_SQLSTR == expected_fiscunit_sqlstr

#     assert len(idea_config) == len(fisc_insert_agg_sqlstrs)


# def test_get_bud_insert_put_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_insert_agg_sqlstrs = get_bud_insert_put_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             raw_tablename = f"{x_dimen}_put_raw"
#             agg_tablename = f"{x_dimen}_put_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr


# def test_get_bud_insert_del_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_insert_agg_sqlstrs = get_bud_insert_del_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             dimen_focus_columns[-1] = get_delete_key_name(dimen_focus_columns[-1])
#             raw_tablename = f"{x_dimen}_del_raw"
#             agg_tablename = f"{x_dimen}_del_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{abbv(agg_tablename)}_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr


# def test_get_idea_stageble_put_dimens_HasAll_idea_numbersForAll_dimens():
#     # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     # THEN
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_all_idea_tables(cursor)
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         idea_raw2dimen_count = 0
#         idea_dimen_combo_checked_count = 0
#         sorted_idea_numbers = sorted(get_idea_numbers())
#         expected_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
#         for x_dimen in sorted(idea_config):
#             dimen_config = idea_config.get(x_dimen)
#             dimen_key_columns = set(dimen_config.get("jkeys").keys())
#             dimen_value_columns = set(dimen_config.get("jvalues").keys())
#             for idea_number in sorted_idea_numbers:
#                 src_columns = get_table_columns(cursor, f"{idea_number}_raw")
#                 expected_stagable = dimen_key_columns.issubset(src_columns)
#                 if idea_number == "br00050":
#                     print(f"{x_dimen} {idea_number} checking... {src_columns}")
#                 src_tablename = f"{idea_number}_raw"
#                 gen_stablable = required_columns_exist(
#                     cursor, src_tablename, dimen_key_columns
#                 )
#                 assert expected_stagable == gen_stablable

#                 idea_dimen_combo_checked_count += 1
#                 if required_columns_exist(cursor, src_tablename, dimen_key_columns):
#                     expected_idea_stagable_dimens.get(idea_number).append(x_dimen)
#                     idea_raw2dimen_count += 1
#                     src_cols_set = set(src_columns)
#                     existing_value_col = src_cols_set.intersection(dimen_value_columns)
#                     # print(
#                     #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
#                     # )
#                     # print(
#                     #     f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
#                     # )
#                     generated_sqlstr = get_idea_into_dimen_raw_query(
#                         conn_or_cursor=cursor,
#                         idea_number=idea_number,
#                         x_dimen=x_dimen,
#                         x_jkeys=dimen_key_columns,
#                     )
#                     # check sqlstr is correct?
#                     assert generated_sqlstr != ""

#     idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
#     print(f"{expected_idea_stagable_dimens=}")
#     assert idea_dimen_combo_checked_count == 680
#     assert idea_raw2dimen_count == 100
#     assert get_idea_stageble_put_dimens() == expected_idea_stagable_dimens


# def test_IDEA_STAGEBLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
#     # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     # THEN
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_all_idea_tables(cursor)
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         idea_raw2dimen_count = 0
#         idea_dimen_combo_checked_count = 0
#         sorted_idea_numbers = sorted(get_idea_numbers())
#         x_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
#         for x_dimen in sorted(idea_config):
#             dimen_config = idea_config.get(x_dimen)
#             dimen_key_columns = set(dimen_config.get("jkeys").keys())
#             dimen_key_columns = get_default_sorted_list(dimen_key_columns)
#             dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
#             dimen_key_columns = set(dimen_key_columns)
#             for idea_number in sorted_idea_numbers:
#                 src_columns = get_table_columns(cursor, f"{idea_number}_raw")
#                 expected_stagable = dimen_key_columns.issubset(src_columns)
#                 src_tablename = f"{idea_number}_raw"
#                 gen_stablable = required_columns_exist(
#                     cursor, src_tablename, dimen_key_columns
#                 )
#                 assert expected_stagable == gen_stablable

#                 idea_dimen_combo_checked_count += 1
#                 if required_columns_exist(cursor, src_tablename, dimen_key_columns):
#                     x_idea_stagable_dimens.get(idea_number).append(x_dimen)
#                     idea_raw2dimen_count += 1
#                     src_cols_set = set(src_columns)
#                     # print(
#                     #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
#                     # )
#                     print(
#                         f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
#                     )
#                     generated_sqlstr = get_idea_into_dimen_raw_query(
#                         conn_or_cursor=cursor,
#                         idea_number=idea_number,
#                         x_dimen=x_dimen,
#                         x_jkeys=dimen_key_columns,
#                     )
#                     # check sqlstr is correct?
#                     assert generated_sqlstr != ""
#     expected_idea_stagable_dimens = {
#         x_idea_number: stagable_dimens
#         for x_idea_number, stagable_dimens in x_idea_stagable_dimens.items()
#         if stagable_dimens != []
#     }
#     idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
#     print(f"{expected_idea_stagable_dimens=}")
#     assert idea_dimen_combo_checked_count == 680
#     assert idea_raw2dimen_count == 10
#     assert IDEA_STAGEBLE_DEL_DIMENS == expected_idea_stagable_dimens


# def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_create_table_sqlstr = f"""
# CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
#   {fisc_tag_str()} TEXT
# , {event_int_str()} INTEGER
# , agg_time INTEGER
# , error_message TEXT
# )
# ;
# """
#     # WHEN / THEN
#     assert CREATE_FISC_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


# def test_INSERT_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_INSERT_sqlstr = f"""
# INSERT INTO fisc_event_time_agg ({fisc_tag_str()}, {event_int_str()}, agg_time)
# SELECT {fisc_tag_str()}, {event_int_str()}, agg_time
# FROM (
#     SELECT {fisc_tag_str()}, {event_int_str()}, {tran_time_str()} as agg_time
#     FROM fisc_cashbook_raw
#     GROUP BY {fisc_tag_str()}, {event_int_str()}, {tran_time_str()}
#     UNION
#     SELECT {fisc_tag_str()}, {event_int_str()}, {deal_time_str()} as agg_time
#     FROM fisc_dealunit_raw
#     GROUP BY {fisc_tag_str()}, {event_int_str()}, {deal_time_str()}
# )
# ORDER BY {fisc_tag_str()}, {event_int_str()}, agg_time
# ;
# """
#     # WHEN / THEN
#     assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


# def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_UPDATE_sqlstr = f"""
# WITH EventTimeOrdered AS (
#     SELECT {fisc_tag_str()}, {event_int_str()}, agg_time,
#            LAG(agg_time) OVER (PARTITION BY {fisc_tag_str()} ORDER BY {event_int_str()}) AS prev_agg_time
#     FROM fisc_event_time_agg
# )
# UPDATE fisc_event_time_agg
# SET error_message = CASE
#          WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
#          THEN 'not sorted'
#          ELSE 'sorted'
#        END
# FROM EventTimeOrdered
# WHERE EventTimeOrdered.{event_int_str()} = fisc_event_time_agg.{event_int_str()}
#     AND EventTimeOrdered.{fisc_tag_str()} = fisc_event_time_agg.{fisc_tag_str()}
#     AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
# ;
# """
#     # WHEN / THEN
#     assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


# def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_create_table_sqlstr = f"""
# CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
#   {fisc_tag_str()} TEXT
# , {owner_name_str()} TEXT
# , {event_int_str()} INTEGER
# , {deal_time_str()} INTEGER
# , error_message TEXT
# )
# ;
# """
#     # WHEN / THEN
#     assert CREATE_FISC_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# def test_INSERT_FISC_OTE1_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_INSERT_sqlstr = f"""
# INSERT INTO fisc_ote1_agg ({fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()})
# SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# FROM (
#     SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
#     FROM fisc_dealunit_raw
#     GROUP BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# )
# ORDER BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# ;
# """
#     # WHEN / THEN
#     assert INSERT_FISC_OTE1_AGG_SQLSTR == expected_INSERT_sqlstr


# def test_get_fisc_fu1_select_sqlstrs_ReturnsObj_HasAllNeededKeys():
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(a23_str)

#     # THEN
#     assert fu1_select_sqlstrs
#     expected_fu1_select_dimens = set(get_fisc_dimens())
#     assert set(fu1_select_sqlstrs.keys()) == expected_fu1_select_dimens


# def test_get_fisc_fu1_select_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_tag=a23_str)

#     # THEN
#     gen_fiscash_sqlstr = fu1_select_sqlstrs.get(fisc_cashbook_str())
#     gen_fisdeal_sqlstr = fu1_select_sqlstrs.get(fisc_dealunit_str())
#     gen_fishour_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_hour_str())
#     gen_fismont_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_month_str())
#     gen_fisweek_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_weekday_str())
#     gen_fisoffi_sqlstr = fu1_select_sqlstrs.get(fisc_timeoffi_str())
#     gen_fiscunit_sqlstr = fu1_select_sqlstrs.get(fiscunit_str())
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_fisc_prime_tables(cursor)
#         fiscash_agg = f"{fisc_cashbook_str()}_agg"
#         fisdeal_agg = f"{fisc_dealunit_str()}_agg"
#         fishour_agg = f"{fisc_timeline_hour_str()}_agg"
#         fismont_agg = f"{fisc_timeline_month_str()}_agg"
#         fisweek_agg = f"{fisc_timeline_weekday_str()}_agg"
#         fisoffi_agg = f"{fisc_timeoffi_str()}_agg"
#         fiscunit_agg = f"{fiscunit_str()}_agg"
#         where_dict = {fisc_tag_str(): a23_str}
#         fiscash_sql = create_select_query(cursor, fiscash_agg, [], where_dict, True)
#         fisdeal_sql = create_select_query(cursor, fisdeal_agg, [], where_dict, True)
#         fishour_sql = create_select_query(cursor, fishour_agg, [], where_dict, True)
#         fismont_sql = create_select_query(cursor, fismont_agg, [], where_dict, True)
#         fisweek_sql = create_select_query(cursor, fisweek_agg, [], where_dict, True)
#         fisoffi_sql = create_select_query(cursor, fisoffi_agg, [], where_dict, True)
#         fiscunit_sql = create_select_query(cursor, fiscunit_agg, [], where_dict, True)
#         print(f"""FISUNIT_FU1_SELECT_SQLSTR = "{fiscunit_sql}\"""")
#         assert gen_fiscash_sqlstr == fiscash_sql
#         assert gen_fisdeal_sqlstr == fisdeal_sql
#         assert gen_fishour_sqlstr == fishour_sql
#         assert gen_fismont_sqlstr == fismont_sql
#         assert gen_fisweek_sqlstr == fisweek_sql
#         assert gen_fisoffi_sqlstr == fisoffi_sql
#         assert gen_fiscunit_sqlstr == fiscunit_sql
