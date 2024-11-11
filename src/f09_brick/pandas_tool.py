from src.f00_instrument.file import (
    save_file,
    create_file_path,
    get_all_filenames,
    get_dir_file_strs,
    open_file,
)
from src.f00_instrument.db_toolbox import get_grouping_with_all_values_equal_sql_query
from src.f04_gift.atom_config import get_atom_args_obj_classs
from src.f08_filter.filter import (
    BridgeUnit,
    FilterUnit,
    filterable_atom_args,
    get_filterunit_from_json,
)
from src.f09_brick.brick_config import get_brick_elements_sort_order
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
    return pandas_read_csv(create_file_path(x_file_dir, x_filename))


def get_all_excel_sheet_names(
    dir: str, sub_strs: set[str] = None
) -> set[(str, str, str)]:
    if sub_strs is None:
        sub_strs = set()
    excel_files = get_all_filenames(dir, {"xlsx"})
    sheet_names = set()
    for relative_dir, filename in excel_files:
        absolute_dir = create_file_path(dir, relative_dir)
        absolute_path = create_file_path(absolute_dir, filename)
        file_sheet_names = openpyxl_load_workbook(absolute_path).sheetnames
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


def get_grouping_with_all_values_equal_df(
    x_df: DataFrame, group_by_list: list
) -> DataFrame:
    df_columns = set(x_df.columns)
    grouping_columns = get_new_sorting_columns(df_columns, group_by_list)
    value_columns = df_columns.difference(grouping_columns)

    if grouping_columns == []:
        return x_df
    with sqlite3_connect(":memory:") as conn:
        zoo_str = "zoo"
        x_df.to_sql(zoo_str, conn, index=False)
        query_str = get_grouping_with_all_values_equal_sql_query(
            x_table=zoo_str,
            group_by_columns=grouping_columns,
            value_columns=value_columns,
        )
        return pandas_read_sql_query(query_str, conn)


def get_dataframe_filterable_columns(x_df: DataFrame) -> set[str]:
    return {x_column for x_column in x_df.columns if x_column in filterable_atom_args()}


def filter_single_column_dataframe(
    x_df: DataFrame, x_bridgeunit: BridgeUnit, column_name: str
) -> DataFrame:
    if column_name in x_df:
        row_count = len(x_df)
        for cur_row in range(row_count):
            otx_value = x_df.iloc[cur_row][column_name]
            inx_value = x_bridgeunit.get_create_inx(otx_value)
            x_df.at[cur_row, column_name] = inx_value
    return x_df


def filter_all_columns_dataframe(x_df: DataFrame, x_filterunit: FilterUnit):
    column_names = set(x_df.columns)
    filterable_columns = column_names.intersection(filterable_atom_args())
    for filterable_column in filterable_columns:
        obj_class = get_atom_args_obj_classs().get(filterable_column)
        x_bridgeunit = x_filterunit.get_bridgeunit(obj_class)
        filter_single_column_dataframe(x_df, x_bridgeunit, filterable_column)


def filter_face_dir_files(face_dir: str):
    otx_dir = f"{face_dir}/otx"
    inx_dir = f"{face_dir}/inx"
    bridge_filename = "bridge.json"
    filterunit_json = open_file(face_dir, bridge_filename)
    face_filterunit = get_filterunit_from_json(filterunit_json)
    otx_dir_files = get_dir_file_strs(otx_dir, delete_extensions=False)
    for x_file_name in otx_dir_files.keys():
        x_df = open_csv(otx_dir, x_file_name)
        filter_all_columns_dataframe(x_df, face_filterunit)
        save_dataframe_to_csv(x_df, inx_dir, x_file_name)
