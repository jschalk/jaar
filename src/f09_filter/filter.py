from src.f00_instrument.file import dir_files, open_file
from src.f04_gift.atom_config import get_atom_args_python_types, type_AcctID_str
from src.f08_brick.brick import open_brick_csv
from src.f09_filter.bridge import (
    BridgeKind,
    BridgeUnit,
    filterable_atom_args,
    get_bridgeunit_from_json,
)
from pandas import DataFrame
from os.path import exists as os_path_exists


def get_dataframe_filterable_columns(x_dt: DataFrame) -> set[str]:
    return {x_column for x_column in x_dt.columns if x_column in filterable_atom_args()}


def filter_single_column_dataframe(
    x_dt: DataFrame, x_bridgekind: BridgeKind, column_name: str
) -> DataFrame:
    if column_name in x_dt:
        row_count = len(x_dt)
        for cur_row in range(row_count):
            src_value = x_dt.iloc[cur_row][column_name]
            dst_value = x_bridgekind.get_create_dst(src_value)
            x_dt.at[cur_row, column_name] = dst_value
    return x_dt


def filter_all_columns_dataframe(x_dt: DataFrame, x_bridgeunit: BridgeUnit):
    column_names = set(x_dt.columns)
    filterable_columns = column_names.intersection(filterable_atom_args())
    for filterable_column in filterable_columns:
        python_type = get_atom_args_python_types().get(filterable_column)
        x_bridgekind = x_bridgeunit.get_bridgekind(python_type)
        filter_single_column_dataframe(x_dt, x_bridgekind, filterable_column)


def filter_files_from_src_dir_to_dst_dir(src_dir: str, dst_dir: str, bridge_dir: str):
    # if os_path_exists(src_dir)
    src_csvs = dir_files(src_dir, delete_extensions=True)
    for x_file_name, x_csv in src_csvs.items():
        x_dt = open_brick_csv(src_dir, f"{x_file_name}.csv")
        bridgeunit_json = open_file(bridge_dir, f"{x_file_name}.json")
        face_bridgeunit = get_bridgeunit_from_json(bridgeunit_json)
        dst_filename = face_bridgeunit._get_dst_value(type_AcctID_str(), x_file_name)
        filter_all_columns_dataframe(x_dt, face_bridgeunit)
        x_dt.to_csv(f"{dst_dir}/{dst_filename}.csv", index=False)
