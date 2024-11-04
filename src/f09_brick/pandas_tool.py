from src.f00_instrument.file import save_file, create_file_path, get_all_filenames
from pandas import DataFrame, read_csv as pandas_read_csv
from openpyxl import load_workbook as openpyxl_load_workbook


def get_brick_elements_sort_order() -> list[str]:
    return [
        "face_id",
        "eon_id",
        "fiscal_id",
        "obj_class",
        "owner_id",
        "acct_id",
        "group_id",
        "parent_road",
        "label",
        "road",
        "base",
        "need",
        "pick",
        "team_id",
        "awardee_id",
        "healer_id",
        "time_id",
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "base_item_active_requisite",
        "credit_belief",
        "debtit_belief",
        "credit_vote",
        "debtit_vote",
        "credor_respect",
        "debtor_respect",
        "fopen",
        "fnigh",
        "fund_pool",
        "give_force",
        "mass",
        "max_tree_traverse",
        "nigh",
        "open",
        "divisor",
        "pledge",
        "problem_bool",
        "purview_time_id",
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
        "current_time",
        "amount",
        "month_label",
        "hour_label",
        "cumlative_minute",
        "cumlative_day",
        "weekday_label",
        "weekday_order",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
        "otx_label",
        "inx_label",
        "road_delimiter",
        "c400_number",
        "yr1_jan1_offset",
        "quota",
        "monthday_distortion",
        "timeline_label",
    ]


def get_brick_sqlite_type() -> dict[str, str]:
    return {
        "face_id": "TEXT",
        "eon_id": "INTEGER",
        "fiscal_id": "TEXT",
        "obj_class": "TEXT",
        "owner_id": "TEXT",
        "acct_id": "TEXT",
        "group_id": "TEXT",
        "parent_road": "TEXT",
        "label": "TEXT",
        "road": "TEXT",
        "base": "TEXT",
        "need": "TEXT",
        "pick": "TEXT",
        "team_id": "TEXT",
        "awardee_id": "TEXT",
        "healer_id": "TEXT",
        "time_id": "INTEGER",
        "begin": "REAL",
        "close": "REAL",
        "addin": "REAL",
        "numor": "REAL",
        "denom": "REAL",
        "morph": "INTEGER",
        "gogo_want": "REAL",
        "stop_want": "REAL",
        "base_item_active_requisite": "TEXT",
        "credit_belief": "REAL",
        "debtit_belief": "REAL",
        "credit_vote": "REAL",
        "debtit_vote": "REAL",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fopen": "REAL",
        "fnigh": "REAL",
        "fund_pool": "REAL",
        "give_force": "REAL",
        "mass": "REAL",
        "max_tree_traverse": "INT",
        "nigh": "REAL",
        "open": "REAL",
        "divisor": "REAL",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "purview_time_id": "INTEGER",
        "take_force": "REAL",
        "tally": "REAL",
        "fund_coin": "REAL",
        "penny": "REAL",
        "respect_bit": "REAL",
        "current_time": "INTEGER",
        "amount": "REAL",
        "month_label": "TEXT",
        "hour_label": "TEXT",
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_label": "TEXT",
        "weekday_order": "INTEGER",
        "otx_road_delimiter": "TEXT",
        "inx_road_delimiter": "TEXT",
        "unknown_word": "TEXT",
        "otx_word": "TEXT",
        "inx_word": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "road_delimiter": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "monthday_distortion": "INTEGER",
        "timeline_label": "TEXT",
    }


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
