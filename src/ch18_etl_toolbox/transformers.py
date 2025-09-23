from copy import copy as copy_copy, deepcopy as copy_deepcopy
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from src.ch01_data_toolbox.csv_toolbox import open_csv_with_types
from src.ch01_data_toolbox.db_toolbox import (
    _get_grouping_groupby_clause,
    create_insert_into_clause_str,
    create_select_query,
    create_table_from_columns,
    create_type_reference_insert_sqlstr,
    create_update_inconsistency_error_query,
    db_table_exists,
    get_create_table_sqlstr,
    get_db_tables,
    get_grouping_with_all_values_equal_sql_query,
    get_nonconvertible_columns,
    get_row_count,
    get_table_columns,
    save_to_split_csvs,
)
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_file,
    open_json,
    save_file,
    save_json,
)
from src.ch02_rope_logic.term import EventInt, FaceName
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch09_belief_atom_logic.atom_config import get_belief_dimens
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic.delta import get_minimal_beliefdelta
from src.ch10_pack_logic.pack import PackUnit, get_packunit_from_json, packunit_shop
from src.ch11_bud_logic.bud import TranBook
from src.ch12_hub_toolbox.ch12_path import (
    create_belief_event_dir_path,
    create_beliefevent_path,
    create_event_all_pack_path,
    create_gut_path,
    create_moment_json_path,
)
from src.ch12_hub_toolbox.hub_tool import (
    collect_belief_event_dir_sets,
    get_beliefs_downhill_event_ints,
    open_belief_file,
    open_job_file,
)
from src.ch15_moment_logic.moment_cell import (
    create_bud_mandate_ledgers,
    create_moment_beliefs_cell_trees,
    set_cell_tree_cell_mandates,
    set_cell_trees_decrees,
    set_cell_trees_found_facts,
)
from src.ch15_moment_logic.moment_main import get_default_path_momentunit
from src.ch16_pidgin_logic.pidgin_config import (
    get_pidgin_args_class_types,
    get_pidgin_LabelTerm_args,
    get_pidgin_NameTerm_args,
    get_pidgin_RopeTerm_args,
    get_pidgin_TitleTerm_args,
    get_quick_pidgens_column_ref,
)
from src.ch16_pidgin_logic.pidgin_main import (
    default_knot_if_None,
    default_unknown_str_if_None,
)
from src.ch17_idea_logic.idea_config import (
    get_idea_dimen_ref,
    get_idea_format_filename,
    get_idea_numbers,
    get_idea_sqlite_types,
    get_idearef_from_file,
)
from src.ch17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    split_excel_into_dirs,
)
from src.ch17_idea_logic.idea_main import get_idearef_obj
from src.ch18_etl_toolbox.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from src.ch18_etl_toolbox.db_obj_belief_tool import insert_job_obj
from src.ch18_etl_toolbox.db_obj_moment_tool import get_moment_dict_from_heard_tables
from src.ch18_etl_toolbox.idea_collector import IdeaFileRef, get_all_idea_dataframes
from src.ch18_etl_toolbox.tran_sqlstrs import (
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_insert_missing_face_name_into_pidgin_core_vld_sqlstr,
    create_insert_pidgin_core_agg_into_vld_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
    create_job_tables,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
    create_sound_agg_insert_sqlstrs,
    create_sound_and_heard_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
    create_update_pidgin_sound_agg_inconsist_sqlstr,
    create_update_pidlabe_sound_agg_knot_error_sqlstr,
    create_update_pidname_sound_agg_knot_error_sqlstr,
    create_update_pidrope_sound_agg_knot_error_sqlstr,
    create_update_pidtitl_sound_agg_knot_error_sqlstr,
    get_belief_heard_agg_tablenames,
    get_insert_heard_agg_sqlstrs,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_belief_sound_agg_tablenames,
)


def etl_input_dfs_to_brick_raw_tables(cursor: sqlite3_Cursor, input_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()

    for ref in get_all_idea_dataframes(input_dir):
        x_file_path = create_path(ref.file_dir, ref.filename)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        idea_sorting_columns = get_default_sorted_list(set(df.columns))
        df = df.reindex(columns=idea_sorting_columns)
        df.sort_values(idea_sorting_columns, inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=["index"], inplace=True)
        df.insert(0, "file_dir", ref.file_dir)
        df.insert(1, "filename", ref.filename)
        df.insert(2, "sheet_name", ref.sheet_name)
        x_tablename = f"{ref.idea_number}_brick_raw"
        column_names = list(df.columns)
        column_names.append("error_message")
        create_table_sqlstr = get_create_table_sqlstr(
            x_tablename, column_names, idea_sqlite_types
        )
        cursor.execute(create_table_sqlstr)

        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            nonconvertible_columns = get_nonconvertible_columns(
                row_dict, idea_sqlite_types
            )
            error_message = None
            if nonconvertible_columns:
                error_message = ""
                for issue_col, issue_value in nonconvertible_columns.items():
                    if error_message:
                        error_message += ", "
                    error_message += f"{issue_col}: {issue_value}"
                error_message = f"Conversion errors: {error_message}"
            row_values = list(row)
            row_values.append(error_message)
            # Set value to None for non-convertible columns
            for x_index, col in enumerate(column_names):
                if nonconvertible_columns.get(col):
                    row_values[x_index] = None
            insert_sqlstr = create_type_reference_insert_sqlstr(
                x_tablename, column_names, row_values
            )
            cursor.execute(insert_sqlstr)


def get_max_brick_agg_event_int(cursor: sqlite3_Cursor) -> int:
    agg_tables = get_db_tables(cursor, "brick_agg")
    brick_aggs_max_event_int = 0
    for agg_table in agg_tables:
        if agg_table.startswith("br") and agg_table.endswith("brick_agg"):
            sqlstr = f"SELECT MAX(event_int) FROM {agg_table}"
            table_max_event_int = cursor.execute(sqlstr).fetchone()[0] or 1
            if table_max_event_int > brick_aggs_max_event_int:
                brick_aggs_max_event_int = table_max_event_int
    return brick_aggs_max_event_int


def get_existing_excel_idea_file_refs(x_dir: str) -> list[IdeaFileRef]:
    existing_excel_idea_filepaths = []
    for idea_number in sorted(get_idea_numbers()):
        idea_filename = f"{idea_number}.xlsx"
        x_idea_path = create_path(x_dir, idea_filename)
        if os_path_exists(x_idea_path):
            x_fileref = IdeaFileRef(
                file_dir=x_dir, filename=idea_filename, idea_number=idea_number
            )
            existing_excel_idea_filepaths.append(x_fileref)
    return existing_excel_idea_filepaths


def etl_brick_raw_tables_to_brick_agg_tables(conn_or_cursor: sqlite3_Connection):
    brick_raw_dict = {f"{idea}_brick_raw": idea for idea in get_idea_numbers()}
    brick_raw_tables = set(brick_raw_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in brick_raw_tables:
            idea_number = brick_raw_dict.get(x_tablename)
            idea_filename = get_idea_format_filename(idea_number)
            idearef = get_idearef_obj(idea_filename)
            key_columns_set = set(idearef.get_otx_keys_list())
            idea_columns_set = set(idearef._attributes.keys())
            value_columns_set = idea_columns_set.difference(key_columns_set)
            idea_columns = get_default_sorted_list(idea_columns_set)
            key_columns_list = get_default_sorted_list(key_columns_set, idea_columns)
            value_columns_list = get_default_sorted_list(
                value_columns_set, idea_columns
            )
            agg_tablename = f"{idea_number}_brick_agg"
            if not db_table_exists(conn_or_cursor, agg_tablename):
                create_idea_sorted_table(conn_or_cursor, agg_tablename, idea_columns)
            select_sqlstr = get_grouping_with_all_values_equal_sql_query(
                x_table=x_tablename,
                groupby_columns=key_columns_list,
                value_columns=value_columns_list,
                where_clause="WHERE error_message IS NULL",
            )
            insert_clause_sqlstr = create_insert_into_clause_str(
                conn_or_cursor,
                agg_tablename,
                columns_set=set(idearef._attributes.keys()),
            )
            insert_from_select_sqlstr = f"""
{insert_clause_sqlstr}
{select_sqlstr};"""
            conn_or_cursor.execute(insert_from_select_sqlstr)


def etl_brick_agg_tables_to_brick_valid_tables(conn_or_cursor: sqlite3_Connection):
    idea_sqlite_types = get_idea_sqlite_types()
    brick_agg_dict = {f"{idea}_brick_agg": idea for idea in get_idea_numbers()}
    brick_agg_tables = set(brick_agg_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in brick_agg_tables:
            idea_number = brick_agg_dict.get(x_tablename)
            valid_tablename = f"{idea_number}_brick_valid"
            agg_columns = get_table_columns(conn_or_cursor, x_tablename)
            create_table_from_columns(
                conn_or_cursor,
                tablename=valid_tablename,
                columns_list=agg_columns,
                column_types=idea_sqlite_types,
            )
            agg_cols_dict = {agg_col: None for agg_col in agg_columns}
            insert_clause_str = create_insert_into_clause_str(
                conn_or_cursor, valid_tablename, agg_cols_dict
            )
            select_sqlstr = create_select_query(
                conn_or_cursor, x_tablename, agg_columns
            )
            select_sqlstr = select_sqlstr.replace("event_int", "agg.event_int")
            select_sqlstr = select_sqlstr.replace("face_name", "agg.face_name")
            select_sqlstr = select_sqlstr.replace(x_tablename, f"{x_tablename} agg")
            join_clause_str = """JOIN events_brick_valid valid_events ON valid_events.event_int = agg.event_int"""
            insert_select_into_sqlstr = f"""
{insert_clause_str}
{select_sqlstr}{join_clause_str}
"""
            conn_or_cursor.execute(insert_select_into_sqlstr)


def etl_brick_agg_tables_to_events_brick_agg_table(conn_or_cursor: sqlite3_Cursor):
    brick_events_tablename = "events_brick_agg"
    if not db_table_exists(conn_or_cursor, brick_events_tablename):
        brick_events_columns = [
            "idea_number",
            "face_name",
            "event_int",
            "error_message",
        ]
        create_idea_sorted_table(
            conn_or_cursor, brick_events_tablename, brick_events_columns
        )

    brick_agg_tables = {f"{idea}_brick_agg": idea for idea in get_idea_numbers()}
    for agg_tablename in get_db_tables(conn_or_cursor):
        if agg_tablename in brick_agg_tables:
            idea_number = brick_agg_tables.get(agg_tablename)
            insert_from_select_sqlstr = f"""
INSERT INTO {brick_events_tablename} (idea_number, event_int, face_name)
SELECT '{idea_number}', event_int, face_name 
FROM {agg_tablename}
GROUP BY event_int, face_name
;
"""
            conn_or_cursor.execute(insert_from_select_sqlstr)

    update_error_message_sqlstr = f"""
UPDATE {brick_events_tablename}
SET error_message = 'invalid because of conflicting event_int'
WHERE event_int IN (
    SELECT event_int 
    FROM {brick_events_tablename} 
    GROUP BY event_int 
    HAVING MAX(face_name) <> MIN(face_name)
)
;
"""
    conn_or_cursor.execute(update_error_message_sqlstr)


def etl_events_brick_agg_table_to_events_brick_valid_table(
    conn_or_cursor: sqlite3_Cursor,
):
    valid_events_tablename = "events_brick_valid"
    if not db_table_exists(conn_or_cursor, valid_events_tablename):
        brick_events_columns = ["event_int", "face_name"]
        create_idea_sorted_table(
            conn_or_cursor, valid_events_tablename, brick_events_columns
        )
    insert_select_sqlstr = f"""
INSERT INTO {valid_events_tablename} (event_int, face_name)
SELECT event_int, face_name 
FROM events_brick_agg
WHERE error_message IS NULL
;
"""
    conn_or_cursor.execute(insert_select_sqlstr)


def etl_events_brick_agg_db_to_event_dict(
    conn_or_cursor: sqlite3_Cursor,
) -> dict[EventInt, FaceName]:
    select_sqlstr = """
SELECT event_int, face_name 
FROM events_brick_valid
;
"""
    conn_or_cursor.execute(select_sqlstr)
    return {int(row[0]): row[1] for row in conn_or_cursor.fetchall()}


def get_brick_valid_tables(cursor: sqlite3_Cursor) -> dict[str, str]:
    possible_brick_valid_tables = {
        f"brick_valid_{idea}": idea for idea in get_idea_numbers()
    }
    active_tables = get_db_tables(cursor)
    return {
        active_table: possible_brick_valid_tables.get(active_table)
        for active_table in active_tables
        if active_table in possible_brick_valid_tables
    }


def brick_valid_tables_to_pidgin_prime_raw_tables(cursor: sqlite3_Cursor):
    brick_valid_tables = get_brick_valid_tables(cursor)
    idea_dimen_ref = {
        pidgin_dimen: idea_numbers
        for pidgin_dimen, idea_numbers in get_idea_dimen_ref().items()
        if pidgin_dimen[:6] == "pidgin"
    }
    pidgin_raw_tables = {}
    for pidgin_dimen in idea_dimen_ref:
        idea_numbers = idea_dimen_ref.get(pidgin_dimen)
        raw_tablename = f"{pidgin_dimen}_raw"
        pidgin_raw_tables[raw_tablename] = idea_numbers

    for brick_valid_table, idea_number in brick_valid_tables.items():
        for raw_tablename, idea_numbers in pidgin_raw_tables.items():
            if idea_number in idea_numbers:
                etl_brick_valid_table_into_old_prime_table(
                    cursor, brick_valid_table, raw_tablename, idea_number
                )


def get_sound_raw_tablenames(
    cursor: sqlite3_Cursor, dimens: list[str], brick_valid_tablename: str
) -> set[str]:
    valid_columns = set(get_table_columns(cursor, brick_valid_tablename))
    s_raw_tables = set()
    for dimen in dimens:
        if dimen.lower().startswith("belief"):
            belief_del_tablename = create_prime_tablename(dimen, "s", "raw", "del")
            belief_del_columns = get_table_columns(cursor, belief_del_tablename)
            delete_key = belief_del_columns[-1]
            if delete_key in valid_columns:
                s_raw_tables.add(belief_del_tablename)
            else:
                s_raw_tables.add(create_prime_tablename(dimen, "s", "raw", "put"))
        else:
            s_raw_tables.add(create_prime_tablename(dimen, "s", "raw"))
    return s_raw_tables


def etl_brick_valid_tables_to_sound_raw_tables(cursor: sqlite3_Cursor):
    create_sound_and_heard_tables(cursor)
    brick_valid_tablenames = get_db_tables(cursor, "_brick_valid", "br")
    for brick_valid_tablename in brick_valid_tablenames:
        idea_number = brick_valid_tablename[:7]
        idearef_filename = get_idea_format_filename(idea_number)
        idearef = get_idearef_from_file(idearef_filename)
        dimens = idearef.get("dimens")
        s_raw_tables = get_sound_raw_tablenames(cursor, dimens, brick_valid_tablename)
        for sound_raw_table in s_raw_tables:
            etl_brick_valid_table_into_prime_table(
                cursor, brick_valid_tablename, sound_raw_table, idea_number
            )


def set_sound_raw_tables_error_message(cursor: sqlite3_Cursor):
    for dimen in get_idea_dimen_ref().keys():
        sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(cursor, dimen)
        cursor.execute(sqlstr)


def insert_sound_raw_selects_into_sound_agg_tables(cursor: sqlite3_Cursor):
    for dimen in get_idea_dimen_ref().keys():
        sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)
        for sqlstr in sqlstrs:
            cursor.execute(sqlstr)


def etl_sound_raw_tables_to_sound_agg_tables(cursor: sqlite3_Cursor):
    set_sound_raw_tables_error_message(cursor)
    insert_sound_raw_selects_into_sound_agg_tables(cursor)


def insert_pidgin_sound_agg_into_pidgin_core_raw_table(cursor: sqlite3_Cursor):
    for dimen in get_quick_pidgens_column_ref():
        cursor.execute(create_insert_into_pidgin_core_raw_sqlstr(dimen))


def insert_pidgin_core_agg_to_pidgin_core_vld_table(cursor: sqlite3_Cursor):
    knot = default_knot_if_None()
    unknown = default_unknown_str_if_None()
    insert_sqlstr = create_insert_pidgin_core_agg_into_vld_sqlstr(knot, unknown)
    cursor.execute(insert_sqlstr)


def update_inconsistency_pidgin_core_raw_table(cursor: sqlite3_Cursor):
    pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
    sqlstr = create_update_inconsistency_error_query(
        cursor,
        x_tablename=pidgin_core_s_raw_tablename,
        focus_columns={"face_name"},
        exclude_columns={"source_dimen"},
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )

    cursor.execute(sqlstr)


def insert_pidgin_core_raw_to_pidgin_core_agg_table(cursor: sqlite3_Cursor):
    pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
    pidgin_core_s_agg_tablename = create_prime_tablename("pidcore", "s", "agg")
    sqlstr = f"""
INSERT INTO {pidgin_core_s_agg_tablename} (face_name, otx_knot, inx_knot, unknown_str)
SELECT face_name, MAX(otx_knot), MAX(inx_knot), MAX(unknown_str)
FROM {pidgin_core_s_raw_tablename}
WHERE error_message IS NULL
GROUP BY face_name
"""
    cursor.execute(sqlstr)


def update_pidgin_sound_agg_inconsist_errors(cursor: sqlite3_Cursor):
    for dimen in get_quick_pidgens_column_ref():
        cursor.execute(create_update_pidgin_sound_agg_inconsist_sqlstr(dimen))


def update_pidgin_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    cursor.execute(create_update_pidlabe_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_pidrope_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_pidname_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_pidtitl_sound_agg_knot_error_sqlstr())


def insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table(cursor: sqlite3_Cursor):
    for dimen in get_quick_pidgens_column_ref():
        cursor.execute(create_insert_pidgin_sound_vld_table_sqlstr(dimen))


def set_moment_belief_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    pidgin_label_args = get_pidgin_LabelTerm_args()
    pidgin_name_args = get_pidgin_NameTerm_args()
    pidgin_title_args = get_pidgin_TitleTerm_args()
    pidgin_rope_args = get_pidgin_RopeTerm_args()
    pidgin_args = copy_copy(pidgin_label_args)
    pidgin_args.update(pidgin_name_args)
    pidgin_args.update(pidgin_title_args)
    pidgin_args.update(pidgin_rope_args)
    pidginable_tuples = get_moment_belief_sound_agg_pidginable_columns(
        cursor, pidgin_args
    )
    for heard_raw_tablename, pidginable_columnname in pidginable_tuples:
        error_update_sqlstr = None
        if pidginable_columnname in pidgin_label_args:
            error_update_sqlstr = create_knot_exists_in_label_error_update_sqlstr(
                heard_raw_tablename, pidginable_columnname
            )
        if pidginable_columnname in pidgin_name_args:
            error_update_sqlstr = create_knot_exists_in_name_error_update_sqlstr(
                heard_raw_tablename, pidginable_columnname
            )
        if error_update_sqlstr:
            cursor.execute(error_update_sqlstr)


def get_moment_belief_sound_agg_pidginable_columns(
    cursor: sqlite3_Cursor, pidgin_args: set[str]
) -> set[tuple[str, str]]:
    pidgin_columns = set()
    for x_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        x_tablename = x_tablename.replace("_h_", "_s_")
        x_tablename = x_tablename.replace("_raw", "_agg")
        for columnname in get_table_columns(cursor, x_tablename):
            if columnname in pidgin_args:
                pidgin_columns.add((x_tablename, columnname))
    return pidgin_columns


def populate_pidgin_core_vld_with_missing_face_names(cursor: sqlite3_Cursor):
    for agg_tablename in get_moment_belief_sound_agg_tablenames():
        insert_sqlstr = create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
            default_knot=default_knot_if_None(),
            default_unknown=default_unknown_str_if_None(),
            moment_belief_sound_agg_tablename=agg_tablename,
        )
        cursor.execute(insert_sqlstr)


def etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor: sqlite3_Cursor):
    insert_pidgin_sound_agg_into_pidgin_core_raw_table(cursor)
    update_inconsistency_pidgin_core_raw_table(cursor)
    insert_pidgin_core_raw_to_pidgin_core_agg_table(cursor)
    insert_pidgin_core_agg_to_pidgin_core_vld_table(cursor)
    populate_pidgin_core_vld_with_missing_face_names(cursor)
    update_pidgin_sound_agg_inconsist_errors(cursor)
    update_pidgin_sound_agg_knot_errors(cursor)
    insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table(cursor)


def etl_sound_agg_tables_to_sound_vld_tables(cursor: sqlite3_Cursor):
    for sqlstr in get_insert_into_sound_vld_sqlstrs().values():
        cursor.execute(sqlstr)


def etl_sound_vld_tables_to_heard_raw_tables(cursor: sqlite3_Cursor):
    for sqlstr in get_insert_into_heard_raw_sqlstrs().values():
        cursor.execute(sqlstr)
    set_all_heard_raw_inx_columns(cursor)


def set_all_heard_raw_inx_columns(cursor: sqlite3_Cursor):
    pidgin_args = get_pidgin_args_class_types()
    for heard_raw_tablename, otx_columnname in get_all_heard_raw_otx_columns(cursor):
        columnname_without_otx = otx_columnname[:-4]
        x_arg = copy_copy(columnname_without_otx)
        if x_arg[-5:] == "ERASE":
            x_arg = x_arg[:-6]
        arg_class_type = pidgin_args.get(x_arg)
        set_heard_raw_inx_column(
            cursor, heard_raw_tablename, columnname_without_otx, arg_class_type
        )


def get_all_heard_raw_otx_columns(cursor: sqlite3_Cursor) -> set[tuple[str, str]]:
    otx_columns = set()
    for heard_raw_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        for columnname in get_table_columns(cursor, heard_raw_tablename):
            if columnname[-3:] in {"otx"}:
                otx_columns.add((heard_raw_tablename, columnname))
    return otx_columns


def set_heard_raw_inx_column(
    cursor: sqlite3_Cursor,
    heard_raw_tablename: str,
    column_without_otx: str,
    arg_class_type: str,
):
    if arg_class_type in {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm"}:
        pidgin_type_abbv = ""
        if arg_class_type == "NameTerm":
            pidgin_type_abbv = "name"
        elif arg_class_type == "TitleTerm":
            pidgin_type_abbv = "title"
        elif arg_class_type == "LabelTerm":
            pidgin_type_abbv = "label"
        elif arg_class_type == "RopeTerm":
            pidgin_type_abbv = "rope"
        update_calc_inx_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            pidgin_type_abbv, heard_raw_tablename, column_without_otx
        )
        cursor.execute(update_calc_inx_sqlstr)
        update_empty_inx_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
            heard_raw_tablename, column_without_otx
        )
        cursor.execute(update_empty_inx_sqlstr)


def etl_heard_raw_tables_to_heard_agg_tables(cursor: sqlite3_Cursor):
    for insert_heard_agg_sqlstr in get_insert_heard_agg_sqlstrs().values():
        cursor.execute(insert_heard_agg_sqlstr)


def etl_heard_agg_tables_to_moment_jsons(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    select_moment_label_sqlstr = """SELECT moment_label FROM momentunit_h_agg;"""
    cursor.execute(select_moment_label_sqlstr)
    for moment_label_set in cursor.fetchall():
        moment_label = moment_label_set[0]
        moment_dict = get_moment_dict_from_heard_tables(cursor, moment_label)
        moment_json_path = create_moment_json_path(moment_mstr_dir, moment_label)
        save_json(moment_json_path, None, moment_dict)


def etl_brick_valid_table_into_prime_table(
    cursor: sqlite3_Cursor,
    brick_valid_table: str,
    raw_tablename: str,
    idea_number: str,
):
    lab_columns = set(get_table_columns(cursor, raw_tablename))
    valid_columns = set(get_table_columns(cursor, brick_valid_table))
    common_cols = lab_columns.intersection(valid_columns)
    common_cols = get_default_sorted_list(common_cols)
    select_str = create_select_query(cursor, brick_valid_table, common_cols)
    select_str = select_str.replace("SELECT", f"SELECT '{idea_number}',")
    common_cols.append("idea_number")
    common_cols = get_default_sorted_list(common_cols)
    x_dict = {common_col: None for common_col in common_cols}
    insert_clause_str = create_insert_into_clause_str(cursor, raw_tablename, x_dict)
    insert_select_sqlstr = f"{insert_clause_str}\n{select_str};"
    cursor.execute(insert_select_sqlstr)


def etl_brick_valid_table_into_old_prime_table(
    cursor: sqlite3_Cursor,
    brick_valid_table: str,
    raw_tablename: str,
    idea_number: str,
):
    lab_columns = set(get_table_columns(cursor, raw_tablename))
    valid_columns = set(get_table_columns(cursor, brick_valid_table))
    common_cols = lab_columns.intersection(valid_columns)
    common_cols = get_default_sorted_list(common_cols)
    select_str = create_select_query(cursor, brick_valid_table, common_cols)
    select_str = select_str.replace("SELECT", f"SELECT '{idea_number}',")
    group_by_clause_str = _get_grouping_groupby_clause(common_cols)
    common_cols.append("idea_number")
    common_cols = get_default_sorted_list(common_cols)
    x_dict = {common_col: None for common_col in common_cols}
    insert_clause_str = create_insert_into_clause_str(cursor, raw_tablename, x_dict)
    insert_select_sqlstr = f"{insert_clause_str}\n{select_str}{group_by_clause_str}"
    cursor.execute(insert_select_sqlstr)


def split_excel_into_events_dirs(pidgin_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(pidgin_file, face_dir, "event_int", "pidgin", sheet_name)


def get_most_recent_event_int(
    event_set: set[EventInt], max_event_int: EventInt
) -> EventInt:
    recent_event_ints = [e_id for e_id in event_set if e_id <= max_event_int]
    return max(recent_event_ints, default=None)


def etl_heard_raw_tables_to_moment_ote1_agg(conn_or_cursor: sqlite3_Connection):
    conn_or_cursor.execute(CREATE_MOMENT_OTE1_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR)


def etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    empty_ote1_csv_str = """moment_label,belief_name,event_int,bud_time,error_message
"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        ote1_csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_label)
        save_file(ote1_csv_path, None, empty_ote1_csv_str)

    save_to_split_csvs(conn_or_cursor, "moment_ote1_agg", ["moment_label"], moments_dir)


def etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir: str):
    idea_types = get_idea_sqlite_types()
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_label)
        csv_arrays = open_csv_with_types(csv_path, idea_types)
        x_dict = {}
        header_row = csv_arrays.pop(0)
        for row in csv_arrays:
            belief_name = row[1]
            event_int = row[2]
            bud_time = row[3]
            if x_dict.get(belief_name) is None:
                x_dict[belief_name] = {}
            belief_dict = x_dict.get(belief_name)
            belief_dict[int(bud_time)] = event_int
        json_path = create_moment_ote1_json_path(moment_mstr_dir, moment_label)
        save_json(json_path, None, x_dict)


def etl_create_buds_root_cells(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        moment_dir = create_path(moments_dir, moment_label)
        ote1_json_path = create_path(moment_dir, "moment_ote1_agg.json")
        if os_path_exists(ote1_json_path):
            ote1_dict = open_json(ote1_json_path)
            x_momentunit = get_default_path_momentunit(moment_mstr_dir, moment_label)
            x_momentunit.create_buds_root_cells(ote1_dict)


def etl_create_moment_cell_trees(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        create_moment_beliefs_cell_trees(moment_mstr_dir, moment_label)


def etl_set_cell_trees_found_facts(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        set_cell_trees_found_facts(moment_mstr_dir, moment_label)


def etl_set_cell_trees_decrees(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        set_cell_trees_decrees(moment_mstr_dir, moment_label)


def etl_set_cell_tree_cell_mandates(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        set_cell_tree_cell_mandates(moment_mstr_dir, moment_label)


def etl_create_bud_mandate_ledgers(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        create_bud_mandate_ledgers(moment_mstr_dir, moment_label)


def etl_heard_agg_to_event_belief_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for belief_table in get_belief_heard_agg_tablenames():
        if get_row_count(conn_or_cursor, belief_table) > 0:
            save_to_split_csvs(
                conn_or_cursor=conn_or_cursor,
                tablename=belief_table,
                key_columns=["moment_label", "belief_name", "event_int"],
                dst_dir=moments_dir,
                col1_prefix="beliefs",
                col2_prefix="events",
            )


def etl_event_belief_csvs_to_pack_json(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        moment_path = create_path(moments_dir, moment_label)
        beliefs_path = create_path(moment_path, "beliefs")
        for belief_name in get_level1_dirs(beliefs_path):
            belief_path = create_path(beliefs_path, belief_name)
            events_path = create_path(belief_path, "events")
            for event_int in get_level1_dirs(events_path):
                event_pack = packunit_shop(
                    belief_name=belief_name,
                    face_name=None,
                    moment_label=moment_label,
                    event_int=event_int,
                )
                event_dir = create_path(events_path, event_int)
                add_beliefatoms_from_csv(event_pack, event_dir)
                event_all_pack_path = create_event_all_pack_path(
                    moment_mstr_dir, moment_label, belief_name, event_int
                )
                save_file(event_all_pack_path, None, event_pack.get_json())


def add_beliefatoms_from_csv(event_pack: PackUnit, event_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()
    belief_dimens = get_belief_dimens()
    belief_dimens.remove("beliefunit")
    for belief_dimen in belief_dimens:
        belief_dimen_put_tablename = create_prime_tablename(
            belief_dimen, "h", "agg", "put"
        )
        belief_dimen_del_tablename = create_prime_tablename(
            belief_dimen, "h", "agg", "del"
        )
        belief_dimen_put_csv = f"{belief_dimen_put_tablename}.csv"
        belief_dimen_del_csv = f"{belief_dimen_del_tablename}.csv"
        put_path = create_path(event_dir, belief_dimen_put_csv)
        del_path = create_path(event_dir, belief_dimen_del_csv)
        if os_path_exists(put_path):
            put_rows = open_csv_with_types(put_path, idea_sqlite_types)
            headers = put_rows.pop(0)
            for put_row in put_rows:
                x_atom = beliefatom_shop(belief_dimen, "INSERT")
                for col_name, row_value in zip(headers, put_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "moment_label",
                        "belief_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                event_pack._beliefdelta.set_beliefatom(x_atom)

        if os_path_exists(del_path):
            del_rows = open_csv_with_types(del_path, idea_sqlite_types)
            headers = del_rows.pop(0)
            for del_row in del_rows:
                x_atom = beliefatom_shop(belief_dimen, "DELETE")
                for col_name, row_value in zip(headers, del_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "moment_label",
                        "belief_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                event_pack._beliefdelta.set_beliefatom(x_atom)


def etl_event_pack_json_to_event_inherited_beliefunits(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        moment_path = create_path(moments_dir, moment_label)
        beliefs_dir = create_path(moment_path, "beliefs")
        for belief_name in get_level1_dirs(beliefs_dir):
            belief_dir = create_path(beliefs_dir, belief_name)
            events_dir = create_path(belief_dir, "events")
            prev_event_int = None
            for event_int in get_level1_dirs(events_dir):
                prev_belief = _get_prev_event_int_beliefunit(
                    moment_mstr_dir, moment_label, belief_name, prev_event_int
                )
                beliefevent_path = create_beliefevent_path(
                    moment_mstr_dir, moment_label, belief_name, event_int
                )
                event_dir = create_belief_event_dir_path(
                    moment_mstr_dir, moment_label, belief_name, event_int
                )

                event_all_pack_path = create_event_all_pack_path(
                    moment_mstr_dir, moment_label, belief_name, event_int
                )
                event_pack = get_packunit_from_json(open_file(event_all_pack_path))
                sift_delta = get_minimal_beliefdelta(
                    event_pack._beliefdelta, prev_belief
                )
                curr_belief = event_pack.get_edited_belief(prev_belief)
                save_file(beliefevent_path, None, curr_belief.get_json())
                expressed_pack = copy_deepcopy(event_pack)
                expressed_pack.set_beliefdelta(sift_delta)
                save_file(event_dir, "expressed_pack.json", expressed_pack.get_json())
                prev_event_int = event_int


def _get_prev_event_int_beliefunit(
    moment_mstr_dir, moment_label, belief_name, prev_event_int
) -> BeliefUnit:
    if prev_event_int is None:
        return beliefunit_shop(belief_name, moment_label)
    prev_beliefevent_path = create_beliefevent_path(
        moment_mstr_dir, moment_label, belief_name, prev_event_int
    )
    return open_belief_file(prev_beliefevent_path)


def etl_event_inherited_beliefunits_to_moment_gut(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        belief_events = collect_belief_event_dir_sets(moment_mstr_dir, moment_label)
        beliefs_max_event_int_dict = get_beliefs_downhill_event_ints(belief_events)
        for belief_name, max_event_int in beliefs_max_event_int_dict.items():
            max_beliefevent_path = create_beliefevent_path(
                moment_mstr_dir, moment_label, belief_name, max_event_int
            )
            max_event_belief_json = open_file(max_beliefevent_path)
            gut_path = create_gut_path(moment_mstr_dir, moment_label, belief_name)
            save_file(gut_path, None, max_event_belief_json)


def add_moment_timeline_to_guts(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        x_momentunit = get_default_path_momentunit(moment_mstr_dir, moment_label)
        x_momentunit.add_timeline_to_guts()


def etl_moment_guts_to_moment_jobs(moment_mstr_dir: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        x_momentunit = get_default_path_momentunit(moment_mstr_dir, moment_label)
        x_momentunit.generate_all_jobs()


def etl_moment_job_jsons_to_job_tables(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    create_job_tables(cursor)
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        moment_path = create_path(moments_dir, moment_label)
        beliefs_dir = create_path(moment_path, "beliefs")
        for belief_name in get_level1_dirs(beliefs_dir):
            job_obj = open_job_file(moment_mstr_dir, moment_label, belief_name)
            insert_job_obj(cursor, job_obj)


def insert_tranunit_voices_net(cursor: sqlite3_Cursor, tranbook: TranBook):
    """
    Insert the net amounts for each voice in the tranbook into the specified table.

    :param cursor: SQLite cursor object
    :param tranbook: TranBook object containing transaction units
    :param dst_tablename: Name of the destination table
    """
    voices_net_array = tranbook._get_voices_net_array()
    cursor.executemany(
        f"INSERT INTO moment_voice_nets (moment_label, belief_name, belief_net_amount) VALUES ('{tranbook.moment_label}', ?, ?)",
        voices_net_array,
    )


def etl_moment_json_voice_nets_to_moment_voice_nets_table(
    cursor: sqlite3_Cursor, moment_mstr_dir: str
):
    cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        x_momentunit = get_default_path_momentunit(moment_mstr_dir, moment_label)
        x_momentunit.set_all_tranbook()
        insert_tranunit_voices_net(cursor, x_momentunit.all_tranbook)


def create_last_run_metrics_json(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    max_brick_agg_event_int = get_max_brick_agg_event_int(cursor)
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    last_run_metrics_dict = {"max_brick_agg_event_int": max_brick_agg_event_int}
    save_json(last_run_metrics_path, None, last_run_metrics_dict)
