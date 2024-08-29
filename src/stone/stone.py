from src._instrument.file import open_file, create_file_path
from src._instrument.python_tool import (
    get_dict_from_json,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_filtered_csv_dict,
)
from src._road.road import RealID, OwnerID
from src._road.jaar_config import get_json_filename
from src.bud.bud import BudUnit
from src.gift.atom import atom_insert, atom_update, atom_delete, atomunit_shop, AtomUnit
from src.gift.atom_config import (
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_grouphold_text,
    bud_idea_healerhold_text,
    bud_idea_factunit_text,
    real_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    acct_pool_str,
    debtit_score_str,
    credit_score_str,
    debtit_vote_str,
    credit_vote_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    begin_str,
    close_str,
    addin_str,
    numor_str,
    denom_str,
    morph_str,
    gogo_want_str,
    stop_want_str,
)
from src.gift.change import changeunit_shop, get_filtered_changeunit, ChangeUnit
from src.gift.gift import giftunit_shop
from src.listen.hubunit import hubunit_shop
from src.stone.examples.stone_env import src_stone_dir
from pandas import DataFrame, read_csv
import csv
from dataclasses import dataclass


def column_order_str() -> str:
    return "column_order"


def sort_order_str() -> str:
    return "sort_order"


def atom_category_str() -> str:
    return "atom_category"


def attributes_str() -> str:
    return "attributes"


def must_be_roadnode_str() -> str:
    return "must_be_RoadNode"


def must_be_roadunit_str() -> str:
    return "must_be_RoadUnit"


def must_be_str() -> str:
    return "must_be_str"


def must_be_number_str() -> str:
    return "must_be_number"


def must_be_bool_str() -> str:
    return "must_be_bool"


def get_stone_formats_dir() -> str:
    return f"{src_stone_dir()}/stone_formats"


def stone_format_00001_acct_v0_0_0() -> str:
    return "stone_format_00001_acct_v0_0_0"


def stone_format_00002_membership_v0_0_0() -> str:
    return "stone_format_00002_membership_v0_0_0"


def stone_format_00003_ideaunit_v0_0_0() -> str:
    return "stone_format_00003_ideaunit_v0_0_0"


def stone_format_00019_ideaunit_v0_0_0() -> str:
    return "stone_format_00019_ideaunit_v0_0_0"


def get_stone_filenames() -> set[str]:
    return {
        stone_format_00001_acct_v0_0_0(),
        stone_format_00002_membership_v0_0_0(),
        stone_format_00003_ideaunit_v0_0_0(),
        stone_format_00019_ideaunit_v0_0_0(),
    }


@dataclass
class StoneColumn:
    attribute_key: str
    column_order: int
    sort_order: int = None


@dataclass
class StoneRef:
    stone_name: str = None
    atom_category: str = None
    _stonecolumns: dict[str:StoneColumn] = None

    def set_stonecolumn(self, x_stonecolumn: StoneColumn):
        self._stonecolumns[x_stonecolumn.attribute_key] = x_stonecolumn

    def get_headers_list(self) -> list[str]:
        x_list = list(self._stonecolumns.values())
        x_list = sorted(x_list, key=lambda x: x.column_order)
        return [x_stonecolumn.attribute_key for x_stonecolumn in x_list]

    def get_stonecolumn(self, x_attribute_key: str) -> StoneColumn:
        return self._stonecolumns.get(x_attribute_key)


def stoneref_shop(x_stone_name: str, x_atom_category: str) -> StoneRef:
    return StoneRef(
        stone_name=x_stone_name, atom_category=x_atom_category, _stonecolumns={}
    )


def get_stoneref(stone_name: str) -> StoneRef:
    stoneref_filename = get_json_filename(stone_name)
    stoneref_json = open_file(get_stone_formats_dir(), stoneref_filename)
    stoneref_dict = get_dict_from_json(stoneref_json)
    x_stoneref = stoneref_shop(stone_name, stoneref_dict.get(atom_category_str()))
    x_attributes_dict = stoneref_dict.get(attributes_str())
    x_stonecolumns = {}
    for x_key, x_stonecolumn in x_attributes_dict.items():
        x_column_order = x_stonecolumn.get(column_order_str())
        x_sort_order = x_stonecolumn.get(sort_order_str())
        x_stonecolumn = StoneColumn(x_key, x_column_order, x_sort_order)
        x_stonecolumns[x_stonecolumn.attribute_key] = x_stonecolumn
    x_stoneref._stonecolumns = x_stonecolumns
    return x_stoneref


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def _get_headers_list(stone_name: str) -> list[str]:
    return get_stoneref(stone_name).get_headers_list()


def _generate_stone_dataframe(d2_list: list[list[str]], stone_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(stone_name))


def create_stone_df(x_budunit: BudUnit, stone_name: str) -> DataFrame:
    x_changeunit = changeunit_shop()
    x_changeunit.add_all_atomunits(x_budunit)
    x_stoneref = get_stoneref(stone_name)
    x_real_id = x_budunit._real_id
    x_owner_id = x_budunit._owner_id
    sorted_atomunits = _get_sorted_atom_insert_atomunits(x_changeunit, x_stoneref)
    d2_list = _create_d2_list(sorted_atomunits, x_stoneref, x_real_id, x_owner_id)
    d2_list = _change_all_pledge_values(d2_list, x_stoneref)
    x_stone = _generate_stone_dataframe(d2_list, stone_name)
    sorting_columns = x_stoneref.get_headers_list()
    return _sort_dataframe(x_stone, sorting_columns)


def _get_sorted_atom_insert_atomunits(
    x_changeunit: ChangeUnit, x_stoneref: StoneRef
) -> list[AtomUnit]:
    category_set = {x_stoneref.atom_category}
    curd_set = {atom_insert()}
    filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
    return filtered_change.get_category_sorted_atomunits_list()


def _create_d2_list(
    sorted_atomunits: list[AtomUnit],
    x_stoneref: StoneRef,
    x_real_id: RealID,
    x_owner_id: OwnerID,
):
    d2_list = []
    for x_atomunit in sorted_atomunits:
        d1_list = []
        for x_stonecolumn in x_stoneref.get_headers_list():
            if x_stonecolumn == real_id_str():
                d1_list.append(x_real_id)
            elif x_stonecolumn == owner_id_str():
                d1_list.append(x_owner_id)
            else:
                d1_list.append(x_atomunit.get_value(x_stonecolumn))
        d2_list.append(d1_list)
    return d2_list


def _change_all_pledge_values(d2_list: list[list], x_stoneref: StoneRef) -> list[list]:
    for x_column_header, x_stonecolumn in x_stoneref._stonecolumns.items():
        if x_column_header == pledge_str():
            pledge_column_number = x_stonecolumn.column_order
            for x_row in d2_list:
                if x_row[pledge_column_number] is True:
                    x_row[pledge_column_number] = "Yes"
                else:
                    x_row[pledge_column_number] = ""
    return d2_list


def _sort_dataframe(x_stone: DataFrame, sorting_columns: list[str]) -> DataFrame:
    ascending_bools = get_ascending_bools(sorting_columns)
    x_stone.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_stone.reset_index(inplace=True)
    x_stone.drop(columns=["index"], inplace=True)
    return x_stone


def save_stone_csv(x_stonename: str, x_budunit: BudUnit, x_dir: str, x_filename: str):
    x_dataframe = create_stone_df(x_budunit, x_stonename)
    x_dataframe.to_csv(create_file_path(x_dir, x_filename), index=False)


def open_stone_csv(x_file_dir: str, x_filename: str) -> DataFrame:
    return read_csv(create_file_path(x_file_dir, x_filename))


def create_changeunit(x_csv: str, x_stonename: str) -> ChangeUnit:
    x_changeunit = changeunit_shop()
    title_row, headerless_csv = extract_csv_headers(x_csv)
    x_reader = csv.reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        if x_stonename == stone_format_00001_acct_v0_0_0():
            x_atomunit = atomunit_shop(bud_acctunit_text(), atom_insert())
            x_atomunit.set_arg(title_row[2], row[2])
            x_atomunit.set_arg(title_row[3], float(row[3]))
            x_atomunit.set_arg(title_row[4], float(row[4]))
            x_changeunit.set_atomunit(x_atomunit)
        elif x_stonename == stone_format_00002_membership_v0_0_0():
            x_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
            x_atomunit.set_arg(title_row[2], row[2])
            x_atomunit.set_arg(title_row[3], row[3])
            x_atomunit.set_arg(title_row[4], float(row[4]))
            x_atomunit.set_arg(title_row[5], float(row[5]))
            x_changeunit.set_atomunit(x_atomunit)
        elif x_stonename == stone_format_00003_ideaunit_v0_0_0():
            x_atomunit = atomunit_shop(bud_ideaunit_text(), atom_insert())
            pledge_bool = False
            if row[2] == "Yes":
                pledge_bool = True
            x_atomunit.set_arg(title_row[2], pledge_bool)
            x_atomunit.set_arg(title_row[3], row[3])
            x_atomunit.set_arg(title_row[4], int(row[4]))
            x_atomunit.set_arg(title_row[5], row[5])
            x_changeunit.set_atomunit(x_atomunit)
    return x_changeunit


def load_stone_csv(reals_dir: str, x_stonename: str, x_file_dir: str, x_filename: str):
    x_csv = open_file(x_file_dir, x_filename)
    title_row, headerless_csv = extract_csv_headers(x_csv)
    x_reader = csv.reader(headerless_csv.splitlines(), delimiter=",")

    for row in x_reader:
        x_real_id = row[0]
        x_owner_id = row[1]

    x_hubunit = hubunit_shop(reals_dir, real_id=x_real_id, owner_id=x_owner_id)
    x_hubunit.initialize_gift_voice_files()
    x_changeunit = create_changeunit(x_csv, x_stonename)
    x_giftunit = giftunit_shop(x_owner_id, x_real_id)
    x_giftunit.set_changeunit(x_changeunit)
    x_hubunit.save_gift_file(x_giftunit)
    x_hubunit._create_voice_from_gifts()


def get_csv_real_id_owner_id_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def real_id_owner_id_filtered_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, str]]:
    return create_filtered_csv_dict(headerless_csv, delimiter)
