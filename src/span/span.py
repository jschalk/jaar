from src._instrument.file import open_file, delete_dir, create_file_path
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src.bud.bud import BudUnit
from src.gift.atom import atom_insert, atom_update, atom_delete, atomunit_shop
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
)
from src.gift.change import changeunit_shop, get_filtered_changeunit, ChangeUnit
from src.gift.gift import giftunit_shop
from src.listen.hubunit import hubunit_shop
from src.span.examples.span_env import src_span_dir
from pandas import DataFrame, read_csv
import csv
from dataclasses import dataclass
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


def real_id_str() -> str:
    return "real_id"


def owner_id_str() -> str:
    return "owner_id"


def acct_id_str() -> str:
    return "acct_id"


def group_id_str() -> str:
    return "group_id"


def acct_pool_str() -> str:
    return "acct_pool"


def debtit_score_str() -> str:
    return "debtit_score"


def credit_score_str() -> str:
    return "credit_score"


def debtit_vote_str() -> str:
    return "debtit_vote"


def credit_vote_str() -> str:
    return "credit_vote"


def road_str() -> str:
    return "road"


def parent_road_str() -> str:
    return "parent_road"


def label_str() -> str:
    return "label"


def mass_str() -> str:
    return "mass"


def pledge_str() -> str:
    return "pledge"


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


def get_span_formats_dir() -> str:
    return f"{src_span_dir()}/span_formats"


def jaar_format_00001_acct_v0_0_0() -> str:
    return "jaar_format_00001_acct_v0_0_0"


def jaar_format_00002_membership_v0_0_0() -> str:
    return "jaar_format_00002_membership_v0_0_0"


def jaar_format_00003_ideaunit_v0_0_0() -> str:
    return "jaar_format_00003_ideaunit_v0_0_0"


def get_span_filenames() -> set[str]:
    return {
        jaar_format_00001_acct_v0_0_0(),
        jaar_format_00002_membership_v0_0_0(),
        jaar_format_00003_ideaunit_v0_0_0(),
    }


@dataclass
class SpanColumn:
    attribute_key: str
    column_order: int
    sort_order: int = None


@dataclass
class SpanRef:
    span_name: str = None
    atom_category: str = None
    _spancolumns: dict[str:SpanColumn] = None

    def set_spancolumn(self, x_spancolumn: SpanColumn):
        self._spancolumns[x_spancolumn.attribute_key] = x_spancolumn

    def get_headers_list(self) -> list[str]:
        x_list = list(self._spancolumns.values())
        x_list = sorted(x_list, key=lambda x: x.column_order)
        return [x_spancolumn.attribute_key for x_spancolumn in x_list]

    def get_spancolumn(self, x_attribute_key: str) -> SpanColumn:
        return self._spancolumns.get(x_attribute_key)


def spanref_shop(x_span_name: str, x_atom_category: str) -> SpanRef:
    return SpanRef(
        span_name=x_span_name, atom_category=x_atom_category, _spancolumns={}
    )


def get_spanref(span_name: str) -> SpanRef:
    spanref_filename = get_json_filename(span_name)
    spanref_json = open_file(get_span_formats_dir(), spanref_filename)
    spanref_dict = get_dict_from_json(spanref_json)
    x_spanref = spanref_shop(span_name, spanref_dict.get(atom_category_str()))
    x_attributes_dict = spanref_dict.get(attributes_str())
    x_spancolumns = {}
    for x_key, x_spancolumn in x_attributes_dict.items():
        x_column_order = x_spancolumn.get(column_order_str())
        x_sort_order = x_spancolumn.get(sort_order_str())
        x_spancolumn = SpanColumn(x_key, x_column_order, x_sort_order)
        x_spancolumns[x_spancolumn.attribute_key] = x_spancolumn
    x_spanref._spancolumns = x_spancolumns
    return x_spanref


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def _get_headers_list(span_name: str) -> list[str]:
    return get_spanref(span_name).get_headers_list()


def _generate_span_dataframe(d2_list: list[list[str]], span_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(span_name))


def create_span_df(x_budunit: BudUnit, span_name: str) -> DataFrame:
    x_changeunit = changeunit_shop()
    x_changeunit.add_all_atomunits(x_budunit)
    x_spanref = get_spanref(span_name)
    category_set = {x_spanref.atom_category}
    curd_set = {atom_insert()}
    filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
    sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
    sorting_columns = x_spanref.get_headers_list()
    d2_list = []

    if span_name == jaar_format_00001_acct_v0_0_0():
        d2_list = [
            [
                x_budunit._real_id,
                x_budunit._owner_id,
                x_atomunit.get_value(acct_id_str()),
                x_atomunit.get_value(credit_score_str()),
                x_atomunit.get_value(debtit_score_str()),
            ]
            for x_atomunit in sorted_atomunits
        ]

    elif span_name == jaar_format_00002_membership_v0_0_0():
        d2_list = [
            [
                x_budunit._real_id,
                x_budunit._owner_id,
                x_atomunit.get_value(acct_id_str()),
                x_atomunit.get_value(group_id_str()),
                x_atomunit.get_value(credit_vote_str()),
                x_atomunit.get_value(debtit_vote_str()),
            ]
            for x_atomunit in sorted_atomunits
        ]
    elif span_name == jaar_format_00003_ideaunit_v0_0_0():
        for x_atomunit in sorted_atomunits:
            pledge_bool = x_atomunit.get_value("pledge")
            pledge_yes_str = ""
            if pledge_bool:
                pledge_yes_str = "Yes"
            d2_list.append(
                [
                    x_budunit._real_id,
                    x_budunit._owner_id,
                    pledge_yes_str,
                    x_atomunit.get_value(parent_road_str()),
                    x_atomunit.get_value(f"_{mass_str()}"),
                    x_atomunit.get_value(label_str()),
                ]
            )

    x_span = _generate_span_dataframe(d2_list, span_name)
    ascending_bools = get_ascending_bools(sorting_columns)
    x_span.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_span.reset_index(inplace=True)
    x_span.drop(columns=["index"], inplace=True)

    return x_span


def save_span_csv(x_spanname: str, x_budunit: BudUnit, x_dir: str, x_filename: str):
    x_dataframe = create_span_df(x_budunit, x_spanname)
    csv_path = create_file_path(x_dir, x_filename)
    x_dataframe.to_csv(csv_path, index=False)


def open_span_csv(x_file_dir: str, x_filename: str) -> DataFrame:
    return read_csv(create_file_path(x_file_dir, x_filename))


def create_changeunit(x_csv: str, x_spanname: str) -> ChangeUnit:
    x_changeunit = changeunit_shop()
    x_reader = csv.reader(x_csv.splitlines(), delimiter=",")

    x_count = 0
    for row in x_reader:
        if x_count == 0:
            title_row = copy_deepcopy(row)
        if x_spanname == jaar_format_00001_acct_v0_0_0() and x_count != 0:
            x_atomunit = atomunit_shop(bud_acctunit_text(), atom_insert())
            x_atomunit.set_arg(title_row[2], row[2])
            x_atomunit.set_arg(title_row[3], float(row[3]))
            x_atomunit.set_arg(title_row[4], float(row[4]))
            x_changeunit.set_atomunit(x_atomunit)
        elif x_spanname == jaar_format_00002_membership_v0_0_0() and x_count != 0:
            x_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
            x_atomunit.set_arg(title_row[2], row[2])
            x_atomunit.set_arg(title_row[3], row[3])
            x_atomunit.set_arg(title_row[4], float(row[4]))
            x_atomunit.set_arg(title_row[5], float(row[5]))
            x_changeunit.set_atomunit(x_atomunit)
        elif x_spanname == jaar_format_00003_ideaunit_v0_0_0() and x_count != 0:
            x_atomunit = atomunit_shop(bud_ideaunit_text(), atom_insert())
            # "real_id": "column_order": 0
            # "owner_id": "column_order": 1
            # "pledge": "column_order": 2
            # "parent_road":  "column_order": 3,
            # "mass":  "column_order": 4
            # "label":  "column_order": 5,
            pledge_bool = False
            if row[2] == "Yes":
                pledge_bool = True
            x_atomunit.set_arg(title_row[2], pledge_bool)
            x_atomunit.set_arg(title_row[3], row[3])
            x_atomunit.set_arg("_mass", int(row[4]))
            x_atomunit.set_arg(title_row[5], row[5])
            x_changeunit.set_atomunit(x_atomunit)
        x_count += 1
    return x_changeunit


def load_span_csv(reals_dir: str, x_spanname: str, x_file_dir: str, x_filename: str):
    span_dataframe = open_span_csv(x_file_dir, x_filename)
    # create_changeunit()
    x_giftunit = giftunit_shop()
    x_hubunit = hubunit_shop(reals_dir=reals_dir, real_id="x")
