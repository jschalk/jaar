from src.f00_instrument.file import (
    save_file,
    create_path,
    get_dir_filenames,
    get_dir_file_strs,
    open_file,
)
from src.f00_instrument.db_toolbox import get_grouping_with_all_values_equal_sql_query
from src.f04_gift.atom_config import get_atom_args_jaar_types
from src.f08_pidgin.pidgin import (
    BridgeUnit,
    PidginUnit,
    pidginable_atom_args,
    get_pidginunit_from_json,
)
from src.f09_brick.brick_config import (
    get_brick_elements_sort_order,
    get_brick_category_ref,
    get_brick_format_filename,
)
from pandas import (
    DataFrame,
    read_csv as pandas_read_csv,
    read_sql_query as pandas_read_sql_query,
)
from openpyxl import load_workbook as openpyxl_load_workbook
from sqlite3 import connect as sqlite3_connect


def save_dataframe_to_csv(x_df: DataFrame, x_dir: str, x_filename: str):
    save_file(x_dir, x_filename, get_ordered_csv(x_df))


def get_new_sorting_columns(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_brick_elements_sort_order()
    sort_columns_in_existing = set(sorting_columns).intersection(existing_columns)
    return [
        sort_col for sort_col in sorting_columns if sort_col in sort_columns_in_existing
    ]


def get_ordered_csv(x_df: DataFrame, sorting_columns: list[str] = None) -> str:
    new_sorting_columns = get_new_sorting_columns(set(x_df.columns), sorting_columns)
    x_df.sort_values(new_sorting_columns, inplace=True)
    x_df.reset_index(inplace=True)
    x_df.drop(columns=["index"], inplace=True)
    return x_df.to_csv(index=False).replace("\r", "")


def open_csv(x_file_dir: str, x_filename: str) -> DataFrame:
    return pandas_read_csv(create_path(x_file_dir, x_filename))


def get_sheet_names(x_path: str) -> list[str]:
    return openpyxl_load_workbook(x_path).sheetnames


def get_all_excel_sheet_names(
    dir: str, sub_strs: set[str] = None
) -> set[(str, str, str)]:
    if sub_strs is None:
        sub_strs = set()
    excel_files = get_dir_filenames(dir, {"xlsx"})
    sheet_names = set()
    for relative_dir, filename in excel_files:
        absolute_dir = create_path(dir, relative_dir)
        absolute_path = create_path(absolute_dir, filename)
        file_sheet_names = get_sheet_names(absolute_path)
        for sheet_name in file_sheet_names:
            if not sub_strs:
                sheet_names.add((absolute_dir, filename, sheet_name))
            else:
                for sub_str in sub_strs:
                    if sheet_name.find(sub_str) >= 0:
                        sheet_names.add((absolute_dir, filename, sheet_name))
    return sheet_names


def get_relevant_columns_dataframe(
    src_df: DataFrame,
    relevant_columns: list[str] = None,
    relevant_columns_necessary: bool = True,
) -> DataFrame:
    if relevant_columns is None:
        relevant_columns = get_brick_elements_sort_order()
    current_columns = set(src_df.columns.to_list())
    relevant_columns_set = set(relevant_columns)
    current_relevant_columns = current_columns.intersection(relevant_columns_set)
    relevant_cols_in_order = [
        r_col for r_col in relevant_columns if r_col in current_relevant_columns
    ]
    print(f"{relevant_cols_in_order=}")
    return src_df[relevant_cols_in_order]


def get_zoo_staging_grouping_with_all_values_equal_df(
    x_df: DataFrame, group_by_list: list
) -> DataFrame:
    df_columns = set(x_df.columns)
    grouping_columns = get_new_sorting_columns(df_columns, group_by_list)
    value_columns = df_columns.difference(grouping_columns)

    if grouping_columns == []:
        return x_df
    with sqlite3_connect(":memory:") as conn:
        zoo_staging_str = "zoo_staging"
        x_df.to_sql(zoo_staging_str, conn, index=False)
        query_str = get_grouping_with_all_values_equal_sql_query(
            x_table=zoo_staging_str,
            group_by_columns=grouping_columns,
            value_columns=value_columns,
        )
        return pandas_read_sql_query(query_str, conn)


def get_dataframe_pidginable_columns(x_df: DataFrame) -> set[str]:
    return {x_column for x_column in x_df.columns if x_column in pidginable_atom_args()}


def pidgin_single_column_dataframe(
    x_df: DataFrame, x_bridgeunit: BridgeUnit, column_name: str
) -> DataFrame:
    if column_name in x_df:
        row_count = len(x_df)
        for cur_row in range(row_count):
            otx_value = x_df.iloc[cur_row][column_name]
            inx_value = x_bridgeunit.reveal_inx(otx_value)
            x_df.at[cur_row, column_name] = inx_value
    return x_df


def pidgin_all_columns_dataframe(x_df: DataFrame, x_pidginunit: PidginUnit):
    column_names = set(x_df.columns)
    pidginable_columns = column_names.intersection(pidginable_atom_args())
    for pidginable_column in pidginable_columns:
        jaar_type = get_atom_args_jaar_types().get(pidginable_column)
        x_bridgeunit = x_pidginunit.get_bridgeunit(jaar_type)
        pidgin_single_column_dataframe(x_df, x_bridgeunit, pidginable_column)


def move_otx_csvs_to_pidgin_inx(face_dir: str):
    otx_dir = f"{face_dir}/otx"
    inx_dir = f"{face_dir}/inx"
    bridge_filename = "bridge.json"
    pidginunit_json = open_file(face_dir, bridge_filename)
    face_pidginunit = get_pidginunit_from_json(pidginunit_json)
    otx_dir_files = get_dir_file_strs(otx_dir, delete_extensions=False)
    for x_file_name in otx_dir_files.keys():
        x_df = open_csv(otx_dir, x_file_name)
        pidgin_all_columns_dataframe(x_df, face_pidginunit)
        save_dataframe_to_csv(x_df, inx_dir, x_file_name)


def _get_pidgen_brick_format_filenames() -> set[str]:
    brick_numbers = set(get_brick_category_ref().get("bridge_otx2inx"))
    brick_numbers.update(set(get_brick_category_ref().get("bridge_nub_label")))
    return {f"{brick_number}.xlsx" for brick_number in brick_numbers}
