from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src.bud.bud import BudUnit
from src.gift.atom import atom_insert, atom_update, atom_delete
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
from src.gift.atom_config import config_file_dir
from src.gift.change import changeunit_shop, get_filtered_changeunit
from pandas import DataFrame, concat
from dataclasses import dataclass


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


def debtit_weight_str() -> str:
    return "debtit_weight"


def credit_weight_str() -> str:
    return "credit_weight"


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
    return f"{config_file_dir()}/span_formats"


def jaar_format_0001_acct_v0_0_0() -> str:
    return "jaar_format_0001_acct_v0_0_0"


def jaar_format_0002_membership_v0_0_0() -> str:
    return "jaar_format_0002_membership_v0_0_0"


def jaar_format_0003_ideaunit_v0_0_0() -> str:
    return "jaar_format_0003_ideaunit_v0_0_0"


def get_span_filenames() -> set[str]:
    return {
        jaar_format_0001_acct_v0_0_0(),
        jaar_format_0002_membership_v0_0_0(),
        jaar_format_0003_ideaunit_v0_0_0(),
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


def create_span_dataframe(d2_list: list[list[str]], span_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(span_name))


def create_span(x_budunit: BudUnit, span_name: str) -> DataFrame:
    x_changeunit = changeunit_shop()
    x_changeunit.add_all_atomunits(x_budunit)
    x_spanref = get_spanref(span_name)
    category_set = {x_spanref.atom_category}
    curd_set = {atom_insert()}
    filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
    sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
    sorting_columns = x_spanref.get_headers_list()
    d2_list = []

    if span_name == jaar_format_0001_acct_v0_0_0():
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

    elif span_name == jaar_format_0002_membership_v0_0_0():
        d2_list = [
            [
                x_budunit._real_id,
                x_budunit._owner_id,
                x_atomunit.get_value(acct_id_str()),
                x_atomunit.get_value(group_id_str()),
                x_atomunit.get_value(credit_weight_str()),
                x_atomunit.get_value(debtit_weight_str()),
            ]
            for x_atomunit in sorted_atomunits
        ]
    elif span_name == jaar_format_0003_ideaunit_v0_0_0():
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

    x_span = create_span_dataframe(d2_list, span_name)
    ascending_bools = get_ascending_bools(sorting_columns)
    x_span.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_span.reset_index(inplace=True)
    x_span.drop(columns=["index"], inplace=True)

    return x_span
