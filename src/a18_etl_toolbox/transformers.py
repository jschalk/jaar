from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    save_file,
    open_file,
    save_json,
    open_json,
    get_level1_dirs,
)
from src.a00_data_toolbox.csv_toolbox import open_csv_with_types
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    save_to_split_csvs,
    get_db_tables,
    create_select_query,
    create_insert_into_clause_str,
    _get_grouping_groupby_clause,
    get_table_columns,
    create_table_from_columns,
)
from src.a01_word_logic.road import FaceName, EventInt, OwnerName, FiscTag
from src.a06_bud_logic.bud import budunit_shop, BudUnit
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a08_bud_atom_logic.atom_config import get_bud_dimens
from src.a09_pack_logic.delta import get_minimal_buddelta
from src.a09_pack_logic.pack import packunit_shop, get_packunit_from_json, PackUnit
from src.a12_hub_tools.hub_path import (
    create_gut_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    create_owner_event_dir_path,
    create_budevent_path,
)
from src.a12_hub_tools.hub_tool import (
    collect_owner_event_dir_sets,
    get_owners_downhill_event_ints,
    open_bud_file,
)
from src.a15_fisc_logic.fisc import (
    get_from_default_path as fiscunit_get_from_default_path,
)
from src.a15_fisc_logic.fisc_tool import (
    create_fisc_owners_cell_trees,
    set_cell_trees_found_facts,
    set_cell_trees_decrees,
    set_cell_tree_cell_mandates,
    create_deal_mandate_ledgers,
)
from src.a15_fisc_logic.fisc_config import get_fisc_dimens
from src.a16_pidgin_logic.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.a16_pidgin_logic.pidgin_config import get_quick_pidgens_column_ref
from src.a17_idea_logic.idea_config import (
    get_idea_numbers,
    get_idea_format_filename,
    get_idea_dimen_ref,
    get_idea_config_dict,
    get_idea_sqlite_types,
    get_idearef_from_file,
)
from src.a17_idea_logic.idea import get_idearef_obj
from src.a17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    create_idea_sorted_table,
    upsert_sheet,
    split_excel_into_dirs,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    get_brick_raw_grouping_with_all_values_equal_df,
    get_grouping_with_all_values_equal_sql_query,
    translate_all_columns_dataframe,
    insert_idea_csv,
    save_table_to_csv,
    get_ordered_csv,
    get_idea_into_dimen_raw_query,
)
from src.a17_idea_logic.pidgin_toolbox import init_pidginunit_from_dir
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
    sound_raw_update_inconsist_error_message_sqlstr,
    get_bud_prime_create_table_sqlstrs,
    create_pidgin_prime_tables,
    create_fisc_prime_tables,
    create_bud_prime_tables,
    get_pidgin_update_inconsist_error_message_sqlstrs,
    get_fisc_update_inconsist_error_message_sqlstrs,
    get_fisc_insert_agg_from_raw_sqlstrs,
    get_bud_put_update_inconsist_error_message_sqlstrs,
    get_bud_insert_put_agg_from_raw_sqlstrs,
    get_bud_insert_del_agg_from_raw_sqlstrs,
    get_idea_stageble_put_dimens,
    CREATE_FISC_EVENT_TIME_AGG_SQLSTR,
    INSERT_FISC_EVENT_TIME_AGG_SQLSTR,
    UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR,
    CREATE_FISC_OTE1_AGG_SQLSTR,
    INSERT_FISC_OTE1_AGG_SQLSTR,
)
from src.a18_etl_toolbox.db_obj_tool import get_fisc_dict_from_db
from src.a18_etl_toolbox.idea_collector import get_all_idea_dataframes, IdeaFileRef
from src.a18_etl_toolbox.pidgin_agg import (
    pidginheartbook_shop,
    PidginHeartRow,
    PidginHeartBook,
    pidginbodybook_shop,
    PidginBodyRow,
    PidginBodyBook,
)
from pandas import (
    read_excel as pandas_read_excel,
    concat as pandas_concat,
    DataFrame,
    read_sql_query as pandas_read_sql_query,
)
from os.path import exists as os_path_exists
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy


class not_given_pidgin_dimen_Exception(Exception):
    pass


MAPS_DIMENS = {
    "pidgin_name": "NameUnit",
    "pidgin_label": "LabelUnit",
    "pidgin_tag": "TagUnit",
    "pidgin_road": "RoadUnit",
}

CLASS_TYPES = {
    "NameUnit": {
        "raw": "name_raw",
        "agg": "name_agg",
        "csv_filename": "name.csv",
        "otx_obj": "otx_name",
        "inx_obj": "inx_name",
    },
    "LabelUnit": {
        "raw": "label_raw",
        "agg": "label_agg",
        "csv_filename": "label.csv",
        "otx_obj": "otx_label",
        "inx_obj": "inx_label",
    },
    "TagUnit": {
        "raw": "tag_raw",
        "agg": "tag_agg",
        "csv_filename": "tag.csv",
        "otx_obj": "otx_tag",
        "inx_obj": "inx_tag",
    },
    "RoadUnit": {
        "raw": "road_raw",
        "agg": "road_agg",
        "csv_filename": "road.csv",
        "otx_obj": "otx_road",
        "inx_obj": "inx_road",
    },
}


def get_class_type(pidgin_dimen: str) -> str:
    if pidgin_dimen not in MAPS_DIMENS:
        raise not_given_pidgin_dimen_Exception("not given pidgin_dimen")
    return MAPS_DIMENS[pidgin_dimen]


def get_sheet_raw_name(class_type: str) -> str:
    return CLASS_TYPES[class_type]["raw"]


def get_sheet_agg_name(class_type: str) -> str:
    return CLASS_TYPES[class_type]["agg"]


def get_otx_obj(class_type, x_row) -> str:
    return x_row[CLASS_TYPES[class_type]["otx_obj"]]


def get_inx_obj(class_type, x_row) -> str:
    return x_row[CLASS_TYPES[class_type]["inx_obj"]]


def etl_mud_dfs_to_brick_raw_tables(conn: sqlite3_Connection, mud_dir: str):
    for ref in get_all_idea_dataframes(mud_dir):
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
        df.to_sql(x_tablename, conn, index=False, if_exists="append")


def etl_brick_raw_db_to_brick_raw_df(conn: sqlite3_Connection, brick_dir: str):
    brick_raw_dict = {f"{idea}_brick_raw": idea for idea in get_idea_numbers()}
    brick_raw_tables = set(brick_raw_dict.keys())
    for table_name in get_db_tables(conn):
        if table_name in brick_raw_tables:
            idea_number = brick_raw_dict.get(table_name)
            brick_path = create_path(brick_dir, f"{idea_number}.xlsx")
            sqlstr = f"SELECT * FROM {table_name}"
            brick_raw_idea_df = pandas_read_sql_query(sqlstr, conn)
            upsert_sheet(brick_path, "brick_raw", brick_raw_idea_df)


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


def etl_brick_raw_db_to_brick_agg_df(brick_dir):
    for br_ref in get_existing_excel_idea_file_refs(brick_dir):
        brick_idea_path = create_path(br_ref.file_dir, br_ref.filename)
        brick_raw_df = pandas_read_excel(brick_idea_path, "brick_raw")
        otx_df = create_df_with_groupby_idea_columns(brick_raw_df, br_ref.idea_number)
        upsert_sheet(brick_idea_path, "brick_agg", otx_df)


def etl_brick_agg_tables_to_brick_agg_dfs(conn: sqlite3_Connection, brick_dir: str):
    brick_agg_dict = {f"{idea}_brick_agg": idea for idea in get_idea_numbers()}
    brick_agg_tables = set(brick_agg_dict.keys())
    for table_name in get_db_tables(conn):
        if table_name in brick_agg_tables:
            idea_number = brick_agg_dict.get(table_name)
            brick_path = create_path(brick_dir, f"{idea_number}.xlsx")
            sqlstr = f"SELECT * FROM {table_name}"
            brick_agg_idea_df = pandas_read_sql_query(sqlstr, conn)
            upsert_sheet(brick_path, "brick_agg", brick_agg_idea_df)


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
            )
            insert_clause_sqlstr = create_insert_into_clause_str(
                conn_or_cursor,
                agg_tablename,
                values_dict=idearef._attributes,
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


def create_df_with_groupby_idea_columns(
    brick_raw_df: DataFrame, idea_number: str
) -> DataFrame:
    idea_filename = get_idea_format_filename(idea_number)
    idearef = get_idearef_obj(idea_filename)
    required_columns = idearef.get_otx_keys_list()
    idea_columns_set = set(idearef._attributes.keys())
    idea_columns_list = get_default_sorted_list(idea_columns_set)
    brick_raw_df = brick_raw_df[idea_columns_list]
    return get_brick_raw_grouping_with_all_values_equal_df(
        brick_raw_df, required_columns, idea_number
    )


def etl_brick_agg_non_pidgin_ideas_to_brick_valid(
    brick_dir: str, legitimate_events: set[EventInt]
):
    """create brick_legit sheet with each idea's data that is of a legitimate event"""
    for br_ref in get_existing_excel_idea_file_refs(brick_dir):
        brick_idea_path = create_path(br_ref.file_dir, br_ref.filename)
        brick_agg = pandas_read_excel(brick_idea_path, "brick_agg")
        brick_valid_df = brick_agg[brick_agg["event_int"].isin(legitimate_events)]
        upsert_sheet(brick_idea_path, "brick_valid", brick_valid_df)


def etl_brick_raw_tables_to_events_brick_agg_table(conn_or_cursor: sqlite3_Cursor):
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
        if dimen[:3].lower() == "bud":
            bud_del_tablename = create_prime_tablename(dimen, "s", "raw", "del")
            bud_del_columns = get_table_columns(cursor, bud_del_tablename)
            delete_key = bud_del_columns[-1]
            if delete_key in valid_columns:
                s_raw_tables.add(bud_del_tablename)
            else:
                s_raw_tables.add(create_prime_tablename(dimen, "s", "raw", "put"))
        else:
            s_raw_tables.add(create_prime_tablename(dimen, "s", "raw"))
    return s_raw_tables


def etl_brick_valid_tables_to_sound_raw_tables(cursor: sqlite3_Cursor):
    create_sound_and_voice_tables(cursor)
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


def set_sound_tables_raw_error_message(cursor: sqlite3_Cursor):
    for dimen in get_idea_dimen_ref().keys():
        sqlstr = sound_raw_update_inconsist_error_message_sqlstr(cursor, dimen)
        cursor.execute(sqlstr)


def etl_sound_raw_tables_to_sound_agg_tables(cursor: sqlite3_Cursor):
    pass


def etl_brick_valid_table_into_prime_table(
    cursor: sqlite3_Cursor, brick_valid_table: str, raw_tablename: str, idea_number: str
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
    cursor: sqlite3_Cursor, brick_valid_table: str, raw_tablename: str, idea_number: str
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


def etl_brick_agg_df_to_brick_pidgin_raw_df(
    legitimate_events: set[EventInt], brick_dir: str
):
    etl_brick_agg_dfs_to_pidgin_name_raw(legitimate_events, brick_dir)
    etl_brick_agg_dfs_to_pidgin_label_raw(legitimate_events, brick_dir)
    etl_brick_agg_dfs_to_pidgin_tag_raw(legitimate_events, brick_dir)
    etl_brick_agg_dfs_to_pidgin_road_raw(legitimate_events, brick_dir)


def etl_brick_agg_dfs_to_pidgin_name_raw(
    legitimate_events: set[EventInt], brick_dir: str
):
    brick_agg_single_to_pidgin_raw("pidgin_name", legitimate_events, brick_dir)


def etl_brick_agg_dfs_to_pidgin_label_raw(
    legitimate_events: set[EventInt], brick_dir: str
):
    brick_agg_single_to_pidgin_raw("pidgin_label", legitimate_events, brick_dir)


def etl_brick_agg_dfs_to_pidgin_tag_raw(
    legitimate_events: set[EventInt], brick_dir: str
):
    brick_agg_single_to_pidgin_raw("pidgin_tag", legitimate_events, brick_dir)


def etl_brick_agg_dfs_to_pidgin_road_raw(
    legitimate_events: set[EventInt], brick_dir: str
):
    brick_agg_single_to_pidgin_raw("pidgin_road", legitimate_events, brick_dir)


def brick_agg_single_to_pidgin_raw(
    pidgin_dimen: str, legitimate_events: set[EventInt], brick_dir: str
):
    x_events = legitimate_events
    transformer = BrickAggToPidginRawTransformer(brick_dir, pidgin_dimen, x_events)
    transformer.transform()


class BrickAggToPidginRawTransformer:
    def __init__(
        self, brick_dir: str, pidgin_dimen: str, legitmate_events: set[EventInt]
    ):
        self.brick_dir = brick_dir
        self.legitmate_events = legitmate_events
        self.pidgin_dimen = pidgin_dimen
        self.class_type = get_class_type(pidgin_dimen)

    def transform(self):
        dimen_ideas = get_idea_dimen_ref().get(self.pidgin_dimen)
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
        pidgin_columns.update({"event_int", "face_name"})
        pidgin_columns = get_default_sorted_list(pidgin_columns)
        pidgin_columns.insert(0, "idea_number")
        # empty df with idea_number, event_int, face_name, idea_columns...
        pidgin_df = DataFrame(columns=pidgin_columns)
        for idea_number in sorted(dimen_ideas):
            idea_filename = f"{idea_number}.xlsx"
            brick_idea_path = create_path(self.brick_dir, idea_filename)
            if os_path_exists(brick_idea_path):
                self.insert_raw_rows(
                    pidgin_df, idea_number, brick_idea_path, pidgin_columns
                )
        pidgin_file_path = create_brick_pidgin_path(self.brick_dir)
        upsert_sheet(pidgin_file_path, get_sheet_raw_name(self.class_type), pidgin_df)

    def insert_raw_rows(
        self,
        raw_df: DataFrame,
        idea_number: str,
        brick_idea_path: str,
        df_columns: list[str],
    ):
        brick_agg_df = pandas_read_excel(brick_idea_path, sheet_name="brick_agg")
        df_missing_cols = set(df_columns).difference(brick_agg_df.columns)

        for index, x_row in brick_agg_df.iterrows():
            event_int = x_row["event_int"]
            if event_int in self.legitmate_events:
                face_name = x_row["face_name"]
                otx_bridge = None
                if "otx_bridge" not in df_missing_cols:
                    otx_bridge = x_row["otx_bridge"]
                inx_bridge = None
                if "inx_bridge" not in df_missing_cols:
                    inx_bridge = x_row["inx_bridge"]
                unknown_word = None
                if "unknown_word" not in df_missing_cols:
                    unknown_word = x_row["unknown_word"]
                df_len = len(raw_df.index)
                raw_df.loc[df_len] = [
                    idea_number,
                    event_int,
                    face_name,
                    get_otx_obj(self.class_type, x_row),
                    self.get_inx_obj(x_row, df_missing_cols),
                    otx_bridge,
                    inx_bridge,
                    unknown_word,
                ]

    def get_inx_obj(self, x_row, missing_col: set[str]) -> str:
        if self.class_type == "NameUnit" and "inx_name" not in missing_col:
            return x_row["inx_name"]
        elif self.class_type == "LabelUnit" and "inx_label" not in missing_col:
            return x_row["inx_label"]
        elif self.class_type == "TagUnit" and "inx_tag" not in missing_col:
            return x_row["inx_tag"]
        elif self.class_type == "RoadUnit" and "inx_road" not in missing_col:
            return x_row["inx_road"]
        return None


def etl_pidgin_name_raw_to_name_agg(brick_dir: str):
    etl_pidgin_single_raw_to_agg(brick_dir, "pidgin_name")


def etl_pidgin_label_raw_to_label_agg(brick_dir: str):
    etl_pidgin_single_raw_to_agg(brick_dir, "pidgin_label")


def etl_pidgin_road_raw_to_road_agg(brick_dir: str):
    etl_pidgin_single_raw_to_agg(brick_dir, "pidgin_road")


def etl_pidgin_tag_raw_to_tag_agg(brick_dir: str):
    etl_pidgin_single_raw_to_agg(brick_dir, "pidgin_tag")


def etl_pidgin_single_raw_to_agg(brick_dir: str, map_dimen: str):
    transformer = PidginRawToAggTransformer(brick_dir, map_dimen)
    transformer.transform()


def etl_brick_pidgin_raw_df_to_pidgin_agg_df(brick_dir):
    etl_pidgin_name_raw_to_name_agg(brick_dir)
    etl_pidgin_label_raw_to_label_agg(brick_dir)
    etl_pidgin_road_raw_to_road_agg(brick_dir)
    etl_pidgin_tag_raw_to_tag_agg(brick_dir)


class PidginRawToAggTransformer:
    def __init__(self, brick_dir: str, pidgin_dimen: str):
        self.brick_dir = brick_dir
        self.pidgin_dimen = pidgin_dimen
        self.file_path = create_brick_pidgin_path(self.brick_dir)
        self.class_type = get_class_type(self.pidgin_dimen)

    def transform(self):
        pidgin_columns = get_quick_pidgens_column_ref().get(self.pidgin_dimen)
        pidgin_columns.update({"event_int", "face_name"})
        pidgin_columns = get_default_sorted_list(pidgin_columns)
        pidgin_agg_df = DataFrame(columns=pidgin_columns)
        self.insert_agg_rows(pidgin_agg_df)
        upsert_sheet(self.file_path, get_sheet_agg_name(self.class_type), pidgin_agg_df)

    def insert_agg_rows(self, pidgin_agg_df: DataFrame):
        pidgin_file_path = create_brick_pidgin_path(self.brick_dir)
        raw_sheet_name = get_sheet_raw_name(self.class_type)
        raw_df = pandas_read_excel(pidgin_file_path, sheet_name=raw_sheet_name)
        x_pidginbodybook = self.get_validated_pidginbodybook(raw_df)
        for pidginbodylist in x_pidginbodybook.get_valid_pidginbodylists():
            pidgin_agg_df.loc[len(pidgin_agg_df)] = pidginbodylist

    def get_validated_pidginbodybook(self, raw_df: DataFrame) -> PidginBodyBook:
        x_pidginheartbook = self.get_validated_pidginheart(raw_df)
        x_pidginbodybook = pidginbodybook_shop(x_pidginheartbook)
        for index, x_row in raw_df.iterrows():
            x_pidginbodyrow = PidginBodyRow(
                event_int=x_row["event_int"],
                face_name=x_row["face_name"],
                otx_str=get_otx_obj(self.class_type, x_row),
                inx_str=get_inx_obj(self.class_type, x_row),
            )
            x_pidginbodybook.eval_pidginbodyrow(x_pidginbodyrow)
        return x_pidginbodybook

    def get_validated_pidginheart(self, raw_df: DataFrame) -> PidginHeartBook:
        x_pidginheartbook = pidginheartbook_shop()
        for index, x_row in raw_df.iterrows():
            x_pidginheartrow = PidginHeartRow(
                event_int=x_row["event_int"],
                face_name=x_row["face_name"],
                otx_bridge=x_row["otx_bridge"],
                inx_bridge=x_row["inx_bridge"],
                unknown_word=x_row["unknown_word"],
            )
            x_pidginheartbook.eval_pidginheartrow(x_pidginheartrow)
        return x_pidginheartbook


def etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df(brick_dir: str, faces_dir: str):
    agg_pidgin = create_brick_pidgin_path(brick_dir)
    for class_type in CLASS_TYPES.keys():
        agg_sheet_name = CLASS_TYPES[class_type]["agg"]
        if sheet_exists(agg_pidgin, agg_sheet_name):
            split_excel_into_dirs(
                input_file=agg_pidgin,
                output_dir=faces_dir,
                column_name="face_name",
                filename="pidgin",
                sheet_name=agg_sheet_name,
            )


def etl_face_pidgin_to_event_pidgins(face_dir: str):
    face_pidgin_path = create_brick_pidgin_path(face_dir)
    for class_type in CLASS_TYPES.keys():
        agg_sheet_name = CLASS_TYPES[class_type]["agg"]
        if sheet_exists(face_pidgin_path, agg_sheet_name):
            split_excel_into_events_dirs(face_pidgin_path, face_dir, agg_sheet_name)


def etl_otz_face_pidgins_df_to_otz_event_pidgins_df(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        etl_face_pidgin_to_event_pidgins(face_dir)


def split_excel_into_events_dirs(pidgin_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(pidgin_file, face_dir, "event_int", "pidgin", sheet_name)


def event_pidgin_to_pidgin_csv_files(event_pidgin_dir: str):
    event_pidgin_path = create_brick_pidgin_path(event_pidgin_dir)
    for class_type in CLASS_TYPES.keys():
        agg_sheet_name = CLASS_TYPES[class_type]["agg"]
        csv_filename = CLASS_TYPES[class_type]["csv_filename"]
        if sheet_exists(event_pidgin_path, agg_sheet_name):
            name_csv_path = create_path(event_pidgin_dir, csv_filename)
            name_df = pandas_read_excel(event_pidgin_path, agg_sheet_name)
            name_df.to_csv(name_csv_path, index=False)


def _get_all_syntax_otz_dir_event_dirs(faces_dir) -> list[str]:
    full_event_dirs = []
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        event_dirs = get_dir_file_strs(face_dir, include_dirs=True, include_files=False)
        full_event_dirs.extend(
            create_path(face_dir, event_dir) for event_dir in event_dirs.keys()
        )
    return full_event_dirs


def etl_otz_event_pidgins_to_otz_pidgin_csv_files(faces_dir: str):
    for event_pidgin_dir in _get_all_syntax_otz_dir_event_dirs(faces_dir):
        event_pidgin_to_pidgin_csv_files(event_pidgin_dir)


def etl_event_pidgin_csvs_to_pidgin_json(event_dir: str):
    pidginunit = init_pidginunit_from_dir(event_dir)
    save_file(event_dir, "pidgin.json", pidginunit.get_json(), replace=True)


def etl_otz_event_pidgins_csvs_to_otz_pidgin_jsons(faces_dir: str):
    for event_pidgin_dir in _get_all_syntax_otz_dir_event_dirs(faces_dir):
        etl_event_pidgin_csvs_to_pidgin_json(event_pidgin_dir)


def etl_pidgin_jsons_inherit_younger_pidgins(
    faces_dir: str, pidgin_events: dict[FaceName, set[EventInt]]
):
    old_pidginunit = None
    for face_name, pidgin_event_ints in pidgin_events.items():
        for pidgin_event_int in pidgin_event_ints:
            new_pidgin_path = get_event_pidgin_path(
                faces_dir, face_name, pidgin_event_int
            )
            new_pidginunit = get_pidginunit_from_json(open_file(new_pidgin_path))
            if old_pidginunit != None:
                new_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)
                save_file(new_pidgin_path, None, new_pidginunit.get_json())
            old_pidginunit = new_pidginunit


def get_event_pidgin_path(
    faces_dir: str, face_name: FaceName, pidgin_event_int: EventInt
):
    face_dir = create_path(faces_dir, face_name)
    event_dir = create_path(face_dir, pidgin_event_int)
    return create_path(event_dir, "pidgin.json")


def etl_brick_ideas_to_otz_face_ideas(brick_dir: str, faces_dir: str):
    for brick_br_ref in get_existing_excel_idea_file_refs(brick_dir):
        brick_idea_path = create_path(brick_dir, brick_br_ref.filename)
        if brick_br_ref.filename not in _get_pidgen_idea_format_filenames():
            split_excel_into_dirs(
                input_file=brick_idea_path,
                output_dir=faces_dir,
                column_name="face_name",
                filename=brick_br_ref.idea_number,
                sheet_name="brick_valid",
            )


def etl_otz_face_ideas_to_otz_event_otx_ideas(faces_dir: str):
    for face_name_dir in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name_dir)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_path = create_path(face_dir, face_br_ref.filename)
            split_excel_into_dirs(
                input_file=face_idea_path,
                output_dir=face_dir,
                column_name="event_int",
                filename=face_br_ref.idea_number,
                sheet_name="brick_valid",
            )


def get_pidgin_events_by_dirs(faces_dir: str) -> dict[FaceName, set[EventInt]]:
    pidgin_events = {}
    for face_name in get_level1_dirs(faces_dir):
        face_dir = create_path(faces_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_int)
            pidgin_path = create_path(event_dir, "pidgin.json")
            if os_path_exists(pidgin_path):
                if pidgin_events.get(face_name) is None:
                    pidgin_events[face_name] = {int(event_int)}
                else:
                    events_list = pidgin_events.get(face_name)
                    events_list.add(int(event_int))
    return pidgin_events


def get_most_recent_event_int(
    event_set: set[EventInt], max_event_int: EventInt
) -> EventInt:
    recent_event_ints = [e_id for e_id in event_set if e_id <= max_event_int]
    return max(recent_event_ints, default=None)


def etl_otz_event_ideas_to_inz_events(
    syntax_otz_dir: str, event_pidgins: dict[FaceName, set[EventInt]]
):
    for face_name in get_level1_dirs(syntax_otz_dir):
        face_pidgin_events = event_pidgins.get(face_name)
        if face_pidgin_events is None:
            face_pidgin_events = set()
        face_dir = create_path(syntax_otz_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_dir = create_path(face_dir, event_int)
            event_int = int(event_int)
            pidgin_event_int = get_most_recent_event_int(face_pidgin_events, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.filename)
                idea_df = pandas_read_excel(event_idea_path, "brick_valid")
                if pidgin_event_int != None:
                    pidgin_event_dir = create_path(face_dir, pidgin_event_int)
                    pidgin_path = create_path(pidgin_event_dir, "pidgin.json")
                    x_pidginunit = get_pidginunit_from_json(open_file(pidgin_path))
                    translate_all_columns_dataframe(idea_df, x_pidginunit)
                upsert_sheet(event_idea_path, "inx", idea_df)


def etl_otz_inx_event_ideas_to_inz_faces(syntax_otz_dir: str, syntax_inz_dir: str):
    for face_name in get_level1_dirs(syntax_otz_dir):
        face_dir = create_path(syntax_otz_dir, face_name)
        for event_int in get_level1_dirs(face_dir):
            event_int = int(event_int)
            event_dir = create_path(face_dir, event_int)
            for event_br_ref in get_existing_excel_idea_file_refs(event_dir):
                event_idea_path = create_path(event_dir, event_br_ref.filename)
                split_excel_into_dirs(
                    input_file=event_idea_path,
                    output_dir=syntax_inz_dir,
                    column_name="face_name",
                    filename=event_br_ref.idea_number,
                    sheet_name="inx",
                )


def etl_inz_face_ideas_to_csv_files(syntax_inz_dir: str):
    for face_name in get_level1_dirs(syntax_inz_dir):
        face_dir = create_path(syntax_inz_dir, face_name)
        for face_br_ref in get_existing_excel_idea_file_refs(face_dir):
            face_idea_excel_path = create_path(face_dir, face_br_ref.filename)
            idea_csv = get_ordered_csv(pandas_read_excel(face_idea_excel_path, "inx"))
            save_file(face_dir, face_br_ref.get_csv_filename(), idea_csv)


def etl_inz_face_csv_files2idea_raw_tables(
    conn_or_cursor: sqlite3_Connection, syntax_inz_dir: str
):
    for face_name in get_level1_dirs(syntax_inz_dir):
        face_dir = create_path(syntax_inz_dir, face_name)
        for idea_number in sorted(get_idea_numbers()):
            csv_filename = f"{idea_number}.csv"
            csv_path = create_path(face_dir, csv_filename)
            if os_path_exists(csv_path):
                insert_idea_csv(csv_path, conn_or_cursor, f"{idea_number}_raw")


def etl_idea_raw_to_pidgin_prime_tables(conn_or_cursor):
    create_pidgin_prime_tables(conn_or_cursor)
    brick_valid_tables_to_pidgin_prime_raw_tables(conn_or_cursor)
    set_pidgin_raw_error_message(conn_or_cursor)


def etl_idea_raw_to_fisc_prime_tables(conn_or_cursor):
    create_fisc_prime_tables(conn_or_cursor)
    idea_raw_tables2fisc_raw_tables(conn_or_cursor)
    set_fisc_raw_error_message(conn_or_cursor)
    fisc_raw_tables2fisc_agg_tables(conn_or_cursor)
    fisc_agg_tables2fisc_event_time_agg(conn_or_cursor)


def etl_idea_raw_to_bud_prime_tables(conn_or_cursor):
    create_bud_prime_tables(conn_or_cursor)
    idea_raw_tables2bud_raw_tables(conn_or_cursor)
    set_bud_raw_error_message(conn_or_cursor)
    bud_raw_tables2bud_agg_tables(conn_or_cursor)


def idea_raw_tables2fisc_raw_tables(conn_or_cursor: sqlite3_Connection):
    ideas_stageble_dimens = get_idea_stageble_put_dimens()
    idea_config_dict = get_idea_config_dict()
    for idea_number in get_idea_numbers():
        idea_raw = f"{idea_number}_raw"
        if db_table_exists(conn_or_cursor, idea_raw):
            # only inserts from pre-identified idea categorys
            stageble_dimens = ideas_stageble_dimens.get(idea_number)
            for x_dimen in stageble_dimens:
                dimen_config = idea_config_dict.get(x_dimen)
                if dimen_config.get("idea_category") == "fisc":
                    dimen_jkeys = set(dimen_config.get("jkeys").keys())
                    gen_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor, idea_number, x_dimen, dimen_jkeys
                    )
                    conn_or_cursor.execute(gen_sqlstr)

            # for x_dimen in fisc_dimens:
            #     dimen_config = idea_config_dict.get(x_dimen)
            #     dimen_jkeys = set(dimen_config.get("jkeys").keys())
            #     if required_columns_exist(conn_or_cursor, idea_raw, dimen_jkeys):
            #         gen_sqlstr = get_idea_into_dimen_raw_query(
            #             conn_or_cursor, idea_number, x_dimen, dimen_jkeys
            #         )
            #         conn_or_cursor.execute(gen_sqlstr)


def idea_raw_tables2bud_raw_tables(conn_or_cursor: sqlite3_Connection):
    idea_config_dict = get_idea_config_dict()

    for idea_number in get_idea_numbers():
        idea_raw = f"{idea_number}_raw"
        if db_table_exists(conn_or_cursor, idea_raw):
            # only inserts from pre-identified idea categorys
            stageble_dimens = get_idea_stageble_put_dimens().get(idea_number)
            for x_dimen in stageble_dimens:
                dimen_config = idea_config_dict.get(x_dimen)
                if dimen_config.get("idea_category") == "bud":
                    dimen_jkeys = set(dimen_config.get("jkeys").keys())
                    insert_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor, idea_number, x_dimen, dimen_jkeys, "put"
                    )
                    conn_or_cursor.execute(insert_sqlstr)

            # manually checks each idea categorys
            # for x_dimen in bud_dimens:
            #     dimen_config = idea_config_dict.get(x_dimen)
            #     dimen_jkeys = set(dimen_config.get("jkeys").keys())
            #     if required_columns_exist(conn_or_cursor, idea_raw, dimen_jkeys):
            #         insert_sqlstr = get_idea_into_dimen_raw_query(
            #             conn_or_cursor, idea_number, x_dimen, dimen_jkeys
            #         )
            #         conn_or_cursor.execute(insert_sqlstr)


def set_pidgin_raw_error_message(conn_or_cursor: sqlite3_Connection):
    for (
        set_error_sqlstr
    ) in get_pidgin_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def set_fisc_raw_error_message(conn_or_cursor: sqlite3_Connection):
    for set_error_sqlstr in get_fisc_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def set_bud_raw_error_message(conn_or_cursor: sqlite3_Connection):
    for (
        set_error_sqlstr
    ) in get_bud_put_update_inconsist_error_message_sqlstrs().values():
        conn_or_cursor.execute(set_error_sqlstr)


def fisc_agg_tables2fisc_event_time_agg(conn_or_cursor: sqlite3_Connection):
    conn_or_cursor.execute(CREATE_FISC_EVENT_TIME_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_FISC_EVENT_TIME_AGG_SQLSTR)
    conn_or_cursor.execute(UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR)


def etl_fisc_agg_tables_to_fisc_ote1_agg(conn_or_cursor: sqlite3_Connection):
    conn_or_cursor.execute(CREATE_FISC_OTE1_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_FISC_OTE1_AGG_SQLSTR)


def etl_fisc_table2fisc_ote1_agg_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    empty_ote1_csv_str = """fisc_tag,owner_name,event_int,deal_time,error_message
"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        ote1_csv_path = create_fisc_ote1_csv_path(fisc_mstr_dir, fisc_tag)
        save_file(ote1_csv_path, None, empty_ote1_csv_str)

    save_to_split_csvs(conn_or_cursor, "fisc_ote1_agg", ["fisc_tag"], fiscs_dir)


def etl_fisc_ote1_agg_csvs2jsons(fisc_mstr_dir: str):
    idea_types = get_idea_sqlite_types()
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        csv_path = create_fisc_ote1_csv_path(fisc_mstr_dir, fisc_tag)
        csv_arrays = open_csv_with_types(csv_path, idea_types)
        x_dict = {}
        header_row = csv_arrays.pop(0)
        for row in csv_arrays:
            owner_name = row[1]
            event_int = row[2]
            deal_time = row[3]
            if x_dict.get(owner_name) is None:
                x_dict[owner_name] = {}
            owner_dict = x_dict.get(owner_name)
            owner_dict[int(deal_time)] = event_int
        json_path = create_fisc_ote1_json_path(fisc_mstr_dir, fisc_tag)
        save_json(json_path, None, x_dict)


def etl_create_deals_root_cells(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        fisc_dir = create_path(fiscs_dir, fisc_tag)
        ote1_json_path = create_path(fisc_dir, "fisc_ote1_agg.json")
        if os_path_exists(ote1_json_path):
            ote1_dict = open_json(ote1_json_path)
            x_fiscunit = fiscunit_get_from_default_path(fisc_mstr_dir, fisc_tag)
            x_fiscunit.create_deals_root_cells(ote1_dict)


def etl_create_fisc_cell_trees(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        create_fisc_owners_cell_trees(fisc_mstr_dir, fisc_tag)


def etl_set_cell_trees_found_facts(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        set_cell_trees_found_facts(fisc_mstr_dir, fisc_tag)


def etl_set_cell_trees_decrees(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        set_cell_trees_decrees(fisc_mstr_dir, fisc_tag)


def etl_set_cell_tree_cell_mandates(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        set_cell_tree_cell_mandates(fisc_mstr_dir, fisc_tag)


def etl_create_deal_mandate_ledgers(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        create_deal_mandate_ledgers(fisc_mstr_dir, fisc_tag)


def fisc_raw_tables2fisc_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_fisc_insert_agg_from_raw_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def bud_raw_tables2bud_agg_tables(conn_or_cursor: sqlite3_Connection):
    for x_sqlstr in get_bud_insert_put_agg_from_raw_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)
    for x_sqlstr in get_bud_insert_del_agg_from_raw_sqlstrs().values():
        conn_or_cursor.execute(x_sqlstr)


def etl_bud_tables_to_event_bud_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for bud_table in get_bud_prime_create_table_sqlstrs():
        if get_row_count(conn_or_cursor, bud_table) > 0:
            save_to_split_csvs(
                conn_or_cursor=conn_or_cursor,
                tablename=bud_table,
                key_columns=["fisc_tag", "owner_name", "event_int"],
                output_dir=fiscs_dir,
                col1_prefix="owners",
                col2_prefix="events",
            )


def etl_fisc_raw_tables_to_fisc_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    for fisc_dimen in get_fisc_dimens():
        raw_tablename = f"{fisc_dimen}_raw"
        save_table_to_csv(conn_or_cursor, fisc_mstr_dir, raw_tablename)


def etl_fisc_agg_tables_to_fisc_csvs(
    conn_or_cursor: sqlite3_Connection, fisc_mstr_dir: str
):
    for fisc_dimen in get_fisc_dimens():
        save_table_to_csv(conn_or_cursor, fisc_mstr_dir, f"{fisc_dimen}_agg")


def etl_fisc_agg_tables_to_fisc_jsons(cursor: sqlite3_Cursor, fisc_mstr_dir: str):
    fisc_filename = "fisc.json"
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    select_fisc_tag_sqlstr = """SELECT fisc_tag FROM fiscunit_agg;"""
    cursor.execute(select_fisc_tag_sqlstr)
    for fisc_tag_set in cursor.fetchall():
        fisc_tag = fisc_tag_set[0]
        fisc_dict = get_fisc_dict_from_db(cursor, fisc_tag)
        fiscunit_dir = create_path(fiscs_dir, fisc_tag)
        save_json(fiscunit_dir, fisc_filename, fisc_dict)


def etl_event_bud_csvs_to_pack_json(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_tag)
        owners_path = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_path):
            owner_path = create_path(owners_path, owner_name)
            events_path = create_path(owner_path, "events")
            for event_int in get_level1_dirs(events_path):
                event_path = create_path(events_path, event_int)
                event_pack = packunit_shop(
                    owner_name=owner_name,
                    face_name=None,
                    fisc_tag=fisc_tag,
                    event_int=event_int,
                )
                add_budatoms_from_csv(event_pack, event_path)
                save_file(event_path, "all_pack.json", event_pack.get_json())


def add_budatoms_from_csv(owner_pack: PackUnit, owner_path: str):
    idea_sqlite_types = get_idea_sqlite_types()
    bud_dimens = get_bud_dimens()
    bud_dimens.remove("budunit")
    for bud_dimen in bud_dimens:
        bud_dimen_put_csv = f"{bud_dimen}_put_agg.csv"
        bud_dimen_del_csv = f"{bud_dimen}_del_agg.csv"
        put_path = create_path(owner_path, bud_dimen_put_csv)
        del_path = create_path(owner_path, bud_dimen_del_csv)
        if os_path_exists(put_path):
            put_rows = open_csv_with_types(put_path, idea_sqlite_types)
            headers = put_rows.pop(0)
            for put_row in put_rows:
                x_atom = budatom_shop(bud_dimen, "INSERT")
                for col_name, row_value in zip(headers, put_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "fisc_tag",
                        "owner_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                owner_pack._buddelta.set_budatom(x_atom)

        if os_path_exists(del_path):
            del_rows = open_csv_with_types(del_path, idea_sqlite_types)
            headers = del_rows.pop(0)
            for del_row in del_rows:
                x_atom = budatom_shop(bud_dimen, "DELETE")
                for col_name, row_value in zip(headers, del_row):
                    if col_name not in {
                        "face_name",
                        "event_int",
                        "fisc_tag",
                        "owner_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                owner_pack._buddelta.set_budatom(x_atom)


def etl_event_pack_json_to_event_inherited_budunits(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        fisc_path = create_path(fiscs_dir, fisc_tag)
        owners_dir = create_path(fisc_path, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            events_dir = create_path(owner_dir, "events")
            prev_event_int = None
            for event_int in get_level1_dirs(events_dir):
                prev_bud = _get_prev_event_int_budunit(
                    fisc_mstr_dir, fisc_tag, owner_name, prev_event_int
                )
                budevent_path = create_budevent_path(
                    fisc_mstr_dir, fisc_tag, owner_name, event_int
                )
                event_dir = create_owner_event_dir_path(
                    fisc_mstr_dir, fisc_tag, owner_name, event_int
                )
                pack_path = create_path(event_dir, "all_pack.json")
                event_pack = get_packunit_from_json(open_file(pack_path))
                sift_delta = get_minimal_buddelta(event_pack._buddelta, prev_bud)
                curr_bud = event_pack.get_edited_bud(prev_bud)
                save_file(budevent_path, None, curr_bud.get_json())
                expressed_pack = copy_deepcopy(event_pack)
                expressed_pack.set_buddelta(sift_delta)
                save_file(event_dir, "expressed_pack.json", expressed_pack.get_json())
                prev_event_int = event_int


def _get_prev_event_int_budunit(
    fisc_mstr_dir, fisc_tag, owner_name, prev_event_int
) -> BudUnit:
    if prev_event_int is None:
        return budunit_shop(owner_name, fisc_tag)
    prev_budevent_path = create_budevent_path(
        fisc_mstr_dir, fisc_tag, owner_name, prev_event_int
    )
    return open_bud_file(prev_budevent_path)


def etl_event_inherited_budunits_to_fisc_gut(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        owner_events = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_tag)
        owners_max_event_int_dict = get_owners_downhill_event_ints(owner_events)
        for owner_name, max_event_int in owners_max_event_int_dict.items():
            max_budevent_path = create_budevent_path(
                fisc_mstr_dir, fisc_tag, owner_name, max_event_int
            )
            max_event_bud_json = open_file(max_budevent_path)
            gut_path = create_gut_path(fisc_mstr_dir, fisc_tag, owner_name)
            save_file(gut_path, None, max_event_bud_json)


def etl_fisc_gut_to_fisc_job(fisc_mstr_dir: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_tag in get_level1_dirs(fiscs_dir):
        x_fiscunit = fiscunit_get_from_default_path(fisc_mstr_dir, fisc_tag)
        x_fiscunit.generate_all_jobs()
