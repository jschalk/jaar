from src.f00_instrument.file import save_file, create_file_path, get_all_filenames
from src.f09_brick.brick_config import get_brick_elements_sort_order
from pandas import DataFrame, read_csv as pandas_read_csv
from openpyxl import load_workbook as openpyxl_load_workbook


def save_dataframe_to_csv(x_dt: DataFrame, x_dir: str, x_filename: str):
    save_file(x_dir, x_filename, get_ordered_csv(x_dt))


def get_new_sorting_columns(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_brick_elements_sort_order()
    sort_columns_in_existing = set(sorting_columns).intersection(existing_columns)
    return [
        sort_col for sort_col in sorting_columns if sort_col in sort_columns_in_existing
    ]


def get_ordered_csv(x_dt: DataFrame, sorting_columns: list[str] = None) -> str:
    new_sorting_columns = get_new_sorting_columns(set(x_dt.columns), sorting_columns)
    x_dt.sort_values(new_sorting_columns, inplace=True)
    x_dt.reset_index(inplace=True)
    x_dt.drop(columns=["index"], inplace=True)
    return x_dt.to_csv(index=False).replace("\r", "")


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
    src_dt: DataFrame,
    relevant_columns: list[str] = None,
    relevant_columns_necessary: bool = True,
) -> DataFrame:
    if relevant_columns is None:
        relevant_columns = get_brick_elements_sort_order()
    current_columns = set(src_dt.columns.to_list())
    relevant_columns_set = set(relevant_columns)
    current_relevant_columns = current_columns.intersection(relevant_columns_set)
    relevant_cols_in_order = [
        r_col for r_col in relevant_columns if r_col in current_relevant_columns
    ]
    print(f"{relevant_cols_in_order=}")
    return src_dt[relevant_cols_in_order]
