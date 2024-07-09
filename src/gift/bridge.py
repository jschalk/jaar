from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src._world.world import WorldUnit
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.atom_config import (
    worldunit_text,
    world_charunit_text,
    world_char_belieflink_text,
    world_ideaunit_text,
    world_idea_awardlink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_allyhold_text,
    world_idea_healerhold_text,
    world_idea_factunit_text,
)
from src.gift.atom_config import config_file_dir
from src.gift.change import changeunit_shop, get_filtered_changeunit
from pandas import DataFrame, concat


def real_id_str() -> str:
    return "real_id"


def owner_id_str() -> str:
    return "owner_id"


def char_id_str() -> str:
    return "char_id"


def belief_id_str() -> str:
    return "belief_id"


def char_pool_str() -> str:
    return "char_pool"


def debtor_weight_str() -> str:
    return "debtor_weight"


def credor_weight_str() -> str:
    return "credor_weight"


def parent_road_str() -> str:
    return "parent_road"


def label_str() -> str:
    return "label"


def weight_str() -> str:
    return "weight"


def pledge_str() -> str:
    return "pledge"


def column_order_str() -> str:
    return "column_order"


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


def get_bridge_formats_dir() -> str:
    return f"{config_file_dir()}/bridge_formats"


def jaar_format_0001_char_v0_0_0() -> str:
    return "jaar_format_0001_char_v0_0_0"


def jaar_format_0002_belieflink_v0_0_0() -> str:
    return "jaar_format_0002_belieflink_v0_0_0"


def jaar_format_0003_ideaunit_v0_0_0() -> str:
    return "jaar_format_0003_ideaunit_v0_0_0"


def get_bridge_filenames() -> set[str]:
    return {
        jaar_format_0001_char_v0_0_0(),
        jaar_format_0002_belieflink_v0_0_0(),
        jaar_format_0003_ideaunit_v0_0_0(),
    }


def get_bridge_format_dict(bridge_name: str) -> dict[str,]:
    bridge_filename = get_json_filename(bridge_name)
    bridge_json = open_file(get_bridge_formats_dir(), bridge_filename)
    return get_dict_from_json(bridge_json)


def get_bridge_atom_category(bridge_name: str) -> dict[str,]:
    return get_bridge_format_dict(bridge_name).get("atom_category")


def get_bridge_attribute_dict(bridge_name: str) -> dict[str,]:
    return get_bridge_format_dict(bridge_name).get("attributes")


def get_sorting_attributes(bridge_name: str) -> list[str]:
    bridge_format_dict = get_bridge_attribute_dict(bridge_name)
    x_list = []
    for x_attribute_name, x_attribute_dict in bridge_format_dict.items():
        sort_order = x_attribute_dict.get("sort_order")
        if sort_order != None:
            x_list.append(x_attribute_name)
    return x_list


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def get_column_ordered_bridge_attributes(bridge_name: str) -> list[str]:
    bridge_attribute_dict = get_bridge_attribute_dict(bridge_name)
    column_order_dict = {
        bridge_attribute: a_dict.get("column_order")
        for bridge_attribute, a_dict in bridge_attribute_dict.items()
    }
    return sorted(column_order_dict, key=column_order_dict.get)


def _get_headers_list(bridge_name: str) -> list[str]:
    return list(get_bridge_attribute_dict(bridge_name).keys())


def create_bridge_dataframe(d2_list: list[list[str]], bridge_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(bridge_name))


def create_bridge(x_worldunit: WorldUnit, bridge_name: str) -> DataFrame:
    x_changeunit = changeunit_shop()
    x_changeunit.add_all_atomunits(x_worldunit)
    category_set = {get_bridge_atom_category(bridge_name)}
    curd_set = {atom_insert()}
    filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
    sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
    d2_list = []
    ordered_columns = get_column_ordered_bridge_attributes(bridge_name)

    if bridge_name == jaar_format_0001_char_v0_0_0():
        d2_list = [
            [
                x_atomunit.get_value(char_id_str()),
                x_worldunit._char_debtor_pool,
                x_atomunit.get_value(credor_weight_str()),
                x_atomunit.get_value(debtor_weight_str()),
                x_worldunit._owner_id,
                x_worldunit._real_id,
            ]
            for x_atomunit in sorted_atomunits
        ]

    elif bridge_name == jaar_format_0002_belieflink_v0_0_0():
        d2_list = [
            [
                x_atomunit.get_value(belief_id_str()),
                x_atomunit.get_value(char_id_str()),
                x_atomunit.get_value(credor_weight_str()),
                x_atomunit.get_value(debtor_weight_str()),
                x_worldunit._owner_id,
                x_worldunit._real_id,
            ]
            for x_atomunit in sorted_atomunits
        ]
    elif bridge_name == jaar_format_0003_ideaunit_v0_0_0():
        for x_atomunit in sorted_atomunits:
            pledge_bool = x_atomunit.get_value("pledge")
            pledge_yes_str = ""
            if pledge_bool:
                pledge_yes_str = "Yes"
            d2_list.append(
                [
                    x_atomunit.get_value("label"),
                    x_worldunit._owner_id,
                    x_atomunit.get_value("parent_road"),
                    pledge_yes_str,
                    x_worldunit._real_id,
                    x_atomunit.get_value("_weight"),
                ]
            )

    x_bridge = create_bridge_dataframe(d2_list, bridge_name)
    sorting_columns = get_sorting_attributes(bridge_name)
    ascending_bools = get_ascending_bools(sorting_columns)
    x_bridge.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_bridge.reset_index(inplace=True)
    x_bridge.drop(columns=["index"], inplace=True)

    return x_bridge
