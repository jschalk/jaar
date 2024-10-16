from src.f09_filter.bridge import BridgeUnit
from pandas import DataFrame


def filter_single_column_dataframe(
    x_dt: DataFrame, x_bridgeunit: BridgeUnit
) -> DataFrame:
    if x_bridgeunit.atom_arg in x_dt:
        row_count = len(x_dt)
        for cur_row in range(row_count):
            x_dt.loc[cur_row] = x_bridgeunit.get_create_dst(
                x_dt.iloc[cur_row][x_bridgeunit.atom_arg]
            )
    return x_dt
