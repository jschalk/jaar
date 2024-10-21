from src.f00_instrument.file import dir_files, open_file
from src.f00_instrument.pandas_tool import save_dataframe_to_csv, open_csv
from src.f04_gift.atom_config import get_atom_args_python_types
from src.f09_filter.bridge import (
    BridgeKind,
    BridgeUnit,
    filterable_atom_args,
    get_bridgeunit_from_json,
)
from pandas import DataFrame


def get_dataframe_filterable_columns(x_dt: DataFrame) -> set[str]:
    return {x_column for x_column in x_dt.columns if x_column in filterable_atom_args()}


def filter_single_column_dataframe(
    x_dt: DataFrame, x_bridgekind: BridgeKind, column_name: str
) -> DataFrame:
    if column_name in x_dt:
        row_count = len(x_dt)
        for cur_row in range(row_count):
            otx_value = x_dt.iloc[cur_row][column_name]
            inx_value = x_bridgekind.get_create_inx(otx_value)
            x_dt.at[cur_row, column_name] = inx_value
    return x_dt


def filter_all_columns_dataframe(x_dt: DataFrame, x_bridgeunit: BridgeUnit):
    column_names = set(x_dt.columns)
    filterable_columns = column_names.intersection(filterable_atom_args())
    for filterable_column in filterable_columns:
        python_type = get_atom_args_python_types().get(filterable_column)
        x_bridgekind = x_bridgeunit.get_bridgekind(python_type)
        filter_single_column_dataframe(x_dt, x_bridgekind, filterable_column)


def filter_face_dir_files(face_dir: str):
    otx_dir = f"{face_dir}/otx"
    inx_dir = f"{face_dir}/inx"
    bridge_filename = "bridge.json"
    bridgeunit_json = open_file(face_dir, bridge_filename)
    face_bridgeunit = get_bridgeunit_from_json(bridgeunit_json)
    otx_dir_files = dir_files(otx_dir, delete_extensions=False)
    for x_file_name in otx_dir_files.keys():
        x_dt = open_csv(otx_dir, x_file_name)
        filter_all_columns_dataframe(x_dt, face_bridgeunit)
        save_dataframe_to_csv(x_dt, inx_dir, x_file_name)
