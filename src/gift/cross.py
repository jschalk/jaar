from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src._world.world import WorldUnit
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.atom_config import (
    worldunit_text,
    world_charunit_text,
    world_char_lobbyship_text,
    world_ideaunit_text,
    world_idea_awardlink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_lobbyhold_text,
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


def lobby_id_str() -> str:
    return "lobby_id"


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


def get_cross_formats_dir() -> str:
    return f"{config_file_dir()}/cross_formats"


def jaar_format_0001_char_v0_0_0() -> str:
    return "jaar_format_0001_char_v0_0_0"


def jaar_format_0002_lobbyship_v0_0_0() -> str:
    return "jaar_format_0002_lobbyship_v0_0_0"


def jaar_format_0003_ideaunit_v0_0_0() -> str:
    return "jaar_format_0003_ideaunit_v0_0_0"


def get_cross_filenames() -> set[str]:
    return {
        jaar_format_0001_char_v0_0_0(),
        jaar_format_0002_lobbyship_v0_0_0(),
        jaar_format_0003_ideaunit_v0_0_0(),
    }


def get_cross_format_dict(cross_name: str) -> dict[str,]:
    cross_filename = get_json_filename(cross_name)
    cross_json = open_file(get_cross_formats_dir(), cross_filename)
    return get_dict_from_json(cross_json)


def get_cross_atom_category(cross_name: str) -> dict[str,]:
    return get_cross_format_dict(cross_name).get("atom_category")


def get_cross_attribute_dict(cross_name: str) -> dict[str,]:
    return get_cross_format_dict(cross_name).get("attributes")


def get_sorting_attributes(cross_name: str) -> list[str]:
    cross_format_dict = get_cross_attribute_dict(cross_name)
    x_list = []
    for x_attribute_name, x_attribute_dict in cross_format_dict.items():
        sort_order = x_attribute_dict.get("sort_order")
        if sort_order != None:
            x_list.append(x_attribute_name)
    return x_list


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def get_column_ordered_cross_attributes(cross_name: str) -> list[str]:
    cross_attribute_dict = get_cross_attribute_dict(cross_name)
    column_order_dict = {
        cross_attribute: a_dict.get("column_order")
        for cross_attribute, a_dict in cross_attribute_dict.items()
    }
    return sorted(column_order_dict, key=column_order_dict.get)


def _get_headers_list(cross_name: str) -> list[str]:
    return list(get_cross_attribute_dict(cross_name).keys())


def create_cross_dataframe(d2_list: list[list[str]], cross_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(cross_name))


def create_cross(x_worldunit: WorldUnit, cross_name: str) -> DataFrame:
    x_changeunit = changeunit_shop()
    x_changeunit.add_all_atomunits(x_worldunit)
    category_set = {get_cross_atom_category(cross_name)}
    curd_set = {atom_insert()}
    filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
    sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
    d2_list = []
    ordered_columns = get_column_ordered_cross_attributes(cross_name)

    if cross_name == jaar_format_0001_char_v0_0_0():
        d2_list = [
            [
                x_atomunit.get_value(char_id_str()),
                x_worldunit._debtor_respect,
                x_atomunit.get_value(credor_weight_str()),
                x_atomunit.get_value(debtor_weight_str()),
                x_worldunit._owner_id,
                x_worldunit._real_id,
            ]
            for x_atomunit in sorted_atomunits
        ]

    elif cross_name == jaar_format_0002_lobbyship_v0_0_0():
        d2_list = [
            [
                x_atomunit.get_value(char_id_str()),
                x_atomunit.get_value(credor_weight_str()),
                x_atomunit.get_value(debtor_weight_str()),
                x_atomunit.get_value(lobby_id_str()),
                x_worldunit._owner_id,
                x_worldunit._real_id,
            ]
            for x_atomunit in sorted_atomunits
        ]
    elif cross_name == jaar_format_0003_ideaunit_v0_0_0():
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

    x_cross = create_cross_dataframe(d2_list, cross_name)
    sorting_columns = get_sorting_attributes(cross_name)
    ascending_bools = get_ascending_bools(sorting_columns)
    x_cross.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_cross.reset_index(inplace=True)
    x_cross.drop(columns=["index"], inplace=True)

    return x_cross
