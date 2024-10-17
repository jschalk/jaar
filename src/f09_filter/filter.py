from src.f09_filter.bridge import BridgeKind, filterable_atom_args
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
