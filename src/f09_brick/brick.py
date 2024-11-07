from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import (
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_l2nested_csv_dict,
    create_sorted_concatenated_str,
    get_positional_dict,
    add_headers_to_csv,
)
from src.f01_road.road import FiscalID, OwnerID
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import timelineunit_shop
from src.f04_gift.atom import atom_insert, atom_delete, AtomUnit, atomrow_shop
from src.f04_gift.atom_config import fiscal_id_str, owner_id_str, pledge_str
from src.f04_gift.delta import deltaunit_shop, get_categorys_cruds_deltaunit, DeltaUnit
from src.f04_gift.gift import giftunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_fiscal.fiscal import fiscalunit_shop, FiscalUnit
from src.f09_brick.brick_config import (
    get_brickref_dict,
    categorys_str,
    attributes_str,
    get_brick_format_headers,
)
from src.f09_brick.pandas_tool import save_dataframe_to_csv, get_new_sorting_columns
from pandas import DataFrame
from csv import reader as csv_reader
from dataclasses import dataclass


@dataclass
class BrickRef:
    brick_name: str = None
    categorys: str = None
    _attributes: set[str] = None

    def set_attribute(self, x_attribute: str):
        self._attributes.add(x_attribute)

    def get_headers_list(self) -> list[str]:
        return get_new_sorting_columns(self._attributes)


def brickref_shop(x_brick_name: str, x_categorys: list[str]) -> BrickRef:
    return BrickRef(brick_name=x_brick_name, categorys=x_categorys, _attributes=set())


def get_brickref(brick_name: str) -> BrickRef:
    brickref_dict = get_brickref_dict(brick_name)
    x_brickref = brickref_shop(brick_name, brickref_dict.get(categorys_str()))
    x_brickref._attributes = set(brickref_dict.get(attributes_str()))
    return x_brickref


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def _get_headers_list(brick_name: str) -> list[str]:
    return get_brickref(brick_name).get_headers_list()


def _generate_brick_dataframe(d2_list: list[list[str]], brick_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(brick_name))


def create_brick_df(x_budunit: BudUnit, brick_name: str) -> DataFrame:
    x_deltaunit = deltaunit_shop()
    x_deltaunit.add_all_atomunits(x_budunit)
    x_brickref = get_brickref(brick_name)
    x_fiscal_id = x_budunit._fiscal_id
    x_owner_id = x_budunit._owner_id
    sorted_atomunits = _get_sorted_atom_insert_atomunits(x_deltaunit, x_brickref)
    d2_list = _create_d2_list(sorted_atomunits, x_brickref, x_fiscal_id, x_owner_id)
    d2_list = _delta_all_pledge_values(d2_list, x_brickref)
    x_brick = _generate_brick_dataframe(d2_list, brick_name)
    sorting_columns = x_brickref.get_headers_list()
    return _sort_dataframe(x_brick, sorting_columns)


def _get_sorted_atom_insert_atomunits(
    x_deltaunit: DeltaUnit, x_brickref: BrickRef
) -> list[AtomUnit]:
    category_set = set(x_brickref.categorys)
    curd_set = {atom_insert()}
    limited_delta = get_categorys_cruds_deltaunit(x_deltaunit, category_set, curd_set)
    return limited_delta.get_category_sorted_atomunits_list()


def _create_d2_list(
    sorted_atomunits: list[AtomUnit],
    x_brickref: BrickRef,
    x_fiscal_id: FiscalID,
    x_owner_id: OwnerID,
):
    d2_list = []
    for x_atomunit in sorted_atomunits:
        d1_list = []
        for x_attribute in x_brickref.get_headers_list():
            if x_attribute == fiscal_id_str():
                d1_list.append(x_fiscal_id)
            elif x_attribute == owner_id_str():
                d1_list.append(x_owner_id)
            else:
                d1_list.append(x_atomunit.get_value(x_attribute))
        d2_list.append(d1_list)
    return d2_list


def _delta_all_pledge_values(d2_list: list[list], x_brickref: BrickRef) -> list[list]:
    if pledge_str() in x_brickref._attributes:
        for x_count, x_header in enumerate(x_brickref.get_headers_list()):
            if x_header == pledge_str():
                pledge_column_number = x_count
        for x_row in d2_list:
            if x_row[pledge_column_number] is True:
                x_row[pledge_column_number] = "Yes"
            else:
                x_row[pledge_column_number] = ""
    return d2_list


def _sort_dataframe(x_brick: DataFrame, sorting_columns: list[str]) -> DataFrame:
    ascending_bools = get_ascending_bools(sorting_columns)
    x_brick.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_brick.reset_index(inplace=True)
    x_brick.drop(columns=["index"], inplace=True)
    return x_brick


def save_brick_csv(x_brickname: str, x_budunit: BudUnit, x_dir: str, x_filename: str):
    x_dataframe = create_brick_df(x_budunit, x_brickname)
    save_dataframe_to_csv(x_dataframe, x_dir, x_filename)


def get_csv_brickref(title_row: list[str]) -> BrickRef:
    headers_str = create_sorted_concatenated_str(title_row)
    headers_str = headers_str.replace("face_id,", "")
    headers_str = headers_str.replace("eon_id,", "")
    x_brickname = get_brick_format_headers().get(headers_str)
    return get_brickref(x_brickname)


def make_deltaunit(x_csv: str) -> DeltaUnit:
    title_row, headerless_csv = extract_csv_headers(x_csv)
    x_brickref = get_csv_brickref(title_row)

    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(title_row)
    x_deltaunit = deltaunit_shop()
    for row in x_reader:
        x_atomrow = atomrow_shop(x_brickref.categorys, atom_insert())
        for x_header in title_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_atomunit in x_atomrow.get_atomunits():
            x_deltaunit.set_atomunit(x_atomunit)
    return x_deltaunit


def _load_individual_brick_csv(
    complete_csv: str, fiscals_dir: str, x_fiscal_id: FiscalID, x_owner_id: OwnerID
):
    x_hubunit = hubunit_shop(fiscals_dir, x_fiscal_id, x_owner_id)
    x_hubunit.initialize_gift_voice_files()
    x_voice = x_hubunit.get_voice_bud()
    x_deltaunit = make_deltaunit(complete_csv)
    # x_deltaunit = sift_deltaunit(x_deltaunit, x_voice)
    x_giftunit = giftunit_shop(x_owner_id, x_fiscal_id)
    x_giftunit.set_deltaunit(x_deltaunit)
    x_hubunit.save_gift_file(x_giftunit)
    x_hubunit._create_voice_from_gifts()


def load_brick_csv(fiscals_dir: str, x_file_dir: str, x_filename: str):
    x_csv = open_file(x_file_dir, x_filename)
    headers_list, headerless_csv = extract_csv_headers(x_csv)
    print(f"{headers_list=}")
    print(f"{headerless_csv=}")
    nested_csv = fiscal_id_owner_id_nested_csv_dict(headerless_csv, delimiter=",")
    for x_fiscal_id, fiscal_dict in nested_csv.items():
        for x_owner_id, owner_csv in fiscal_dict.items():
            complete_csv = add_headers_to_csv(headers_list, owner_csv)
            _load_individual_brick_csv(
                complete_csv, fiscals_dir, x_fiscal_id, x_owner_id
            )


def get_csv_fiscal_id_owner_id_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscalID, dict[OwnerID, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def fiscal_id_owner_id_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscalID, dict[OwnerID, str]]:
    return create_l2nested_csv_dict(headerless_csv, delimiter)


def fiscal_build_from_df(
    br00000_df: DataFrame,
    br00001_df: DataFrame,
    br00002_df: DataFrame,
    br00003_df: DataFrame,
    br00004_df: DataFrame,
    br00005_df: DataFrame,
    x_fund_coin,
    x_respect_bit,
    x_penny,
    x_fiscals_dir,
    slash_text,
) -> dict[FiscalID, FiscalUnit]:
    # 00003_hour
    fiscal_hours_dict = {}
    for y_fiscal_id in br00003_df.fiscal_id.unique():
        x_hours_list = []
        query_str = f"fiscal_id == '{y_fiscal_id}'"
        for index, row in br00003_df.query(query_str).iterrows():
            x_hours_list.append([row["hour_label"], row["cumlative_minute"]])
        fiscal_hours_dict[y_fiscal_id] = x_hours_list

    # 00004_month
    fiscal_months_dict = {}
    for y_fiscal_id in br00004_df.fiscal_id.unique():
        x_months_list = []
        query_str = f"fiscal_id == '{y_fiscal_id}'"
        for index, row in br00004_df.query(query_str).iterrows():
            x_months_list.append([row["month_label"], row["cumlative_day"]])
        fiscal_months_dict[y_fiscal_id] = x_months_list

    # 00005_weekday
    fiscal_weekdays_dict = {}
    for y_fiscal_id in br00005_df.fiscal_id.unique():
        x_weekdays_list = []
        query_str = f"fiscal_id == '{y_fiscal_id}'"
        for index, row in br00005_df.query(query_str).iterrows():
            x_weekdays_list.append(row["weekday_label"])
        fiscal_weekdays_dict[y_fiscal_id] = x_weekdays_list

    fiscalunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_fiscal_id = row["fiscal_id"]
        x_timeline_config = {
            "c400_number": row["c400_number"],
            "hours_config": fiscal_hours_dict.get(x_fiscal_id),
            "months_config": fiscal_months_dict.get(x_fiscal_id),
            "monthday_distortion": row["monthday_distortion"],
            "timeline_label": row["timeline_label"],
            "weekdays_config": fiscal_weekdays_dict.get(x_fiscal_id),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_timeline = timelineunit_shop(x_timeline_config)
        x_fiscalunit = fiscalunit_shop(
            fiscal_id=x_fiscal_id,
            fiscals_dir=x_fiscals_dir,
            timeline=x_timeline,
            current_time=row["current_time"],
            # in_memory_journal=row["in_memory_journal"],
            road_delimiter=row["road_delimiter"],
            fund_coin=x_fund_coin,
            respect_bit=x_respect_bit,
            penny=x_penny,
        )
        print(f"{x_fiscalunit.fiscal_id=}")
        fiscalunit_dict[x_fiscalunit.fiscal_id] = x_fiscalunit

    return fiscalunit_dict
