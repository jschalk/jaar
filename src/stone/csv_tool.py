from src._instrument.python import (
    get_csv_column1_column2_metrics,
    create_filtered_csv_dict,
)
from src._road.road import RealID, OwnerID


def get_csv_real_id_owner_id_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def real_id_owner_id_filtered_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, str]]:
    return create_filtered_csv_dict(headerless_csv, delimiter)
