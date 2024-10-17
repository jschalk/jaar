from src.f04_gift.atom_config import get_atom_args_python_types
from src.f09_filter.bridge import BridgeKind, BridgeUnit, filterable_atom_args
from pandas import DataFrame


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
