from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src._world.world import WorldUnit
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.atom_config import (
    worldunit_text,
    world_charunit_text,
    world_char_beliefhold_text,
    world_ideaunit_text,
    world_idea_fiscallink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_belieflink_text,
    world_idea_healerhold_text,
    world_idea_factunit_text,
)
from src.gift.change import changeunit_shop, get_filtered_changeunit
from src.gift.atom_config import config_file_dir
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


def road_str() -> str:
    return "road"


def weight_str() -> str:
    return "weight"


def pledge_str() -> str:
    return "pledge"


def validate_str() -> str:
    return "validate"


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


def jaar_format_0002_beliefhold_v0_0_0() -> str:
    return "jaar_format_0002_beliefhold_v0_0_0"


def jaar_format_0003_ideaunit_v0_0_0() -> str:
    return "jaar_format_0003_ideaunit_v0_0_0"


def get_bridge_filenames() -> set[str]:
    return {
        jaar_format_0001_char_v0_0_0(),
        jaar_format_0002_beliefhold_v0_0_0(),
        jaar_format_0003_ideaunit_v0_0_0(),
    }


def get_bridge_format_dict(bridge_name: str) -> dict[str,]:
    bridge_filename = get_json_filename(bridge_name)
    bridge_json = open_file(get_bridge_formats_dir(), bridge_filename)
    return get_dict_from_json(bridge_json)


def _get_headers_list(bridge_name: str) -> list[str]:
    return list(get_bridge_format_dict(bridge_name).keys())


def create_bridge_dataframe(bridge_name: str) -> DataFrame:
    return DataFrame(columns=_get_headers_list(bridge_name))


def create_bridge(x_worldunit: WorldUnit, bridge_name: str) -> DataFrame:
    x_bridge = create_bridge_dataframe(bridge_name)

    if bridge_name == jaar_format_0001_char_v0_0_0():
        x_changeunit = changeunit_shop()
        x_changeunit.add_all_atomunits(x_worldunit)
        category_set = {world_charunit_text()}
        curd_set = {atom_insert()}
        filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
        sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
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
        x_bridge = DataFrame(d2_list, columns=x_bridge.columns)
        x_bridge.sort_values([char_id_str()], ascending=[True], inplace=True)
        x_bridge.reset_index(inplace=True)
        x_bridge.drop(columns=["index"], inplace=True)

    elif bridge_name == jaar_format_0002_beliefhold_v0_0_0():
        x_changeunit = changeunit_shop()
        x_changeunit.add_all_atomunits(x_worldunit)
        category_set = {world_char_beliefhold_text()}
        curd_set = {atom_insert()}
        filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
        sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
        d2_list = []
        for x_atomunit in sorted_atomunits:
            char_id_value = x_atomunit.get_value(char_id_str())
            belief_id_value = x_atomunit.get_value(belief_id_str())
            d2_list.append(
                [
                    belief_id_value,
                    char_id_value,
                    x_atomunit.get_value(credor_weight_str()),
                    x_atomunit.get_value(debtor_weight_str()),
                    x_worldunit._owner_id,
                    x_worldunit._real_id,
                ]
            )
        x_bridge = DataFrame(d2_list, columns=x_bridge.columns)
        sorting_columns = [char_id_str(), belief_id_str()]
        x_bridge.sort_values(sorting_columns, ascending=[True, True], inplace=True)
        x_bridge.reset_index(inplace=True)
        x_bridge.drop(columns=["index"], inplace=True)

    elif bridge_name == jaar_format_0003_ideaunit_v0_0_0():
        x_changeunit = changeunit_shop()
        x_changeunit.add_all_atomunits(x_worldunit)
        category_set = [world_ideaunit_text()]
        curd_set = {atom_insert()}
        filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
        sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
        d2_list = []
        for x_atomunit in sorted_atomunits:
            parent_roadunit = x_atomunit.get_value("parent_road")
            label_roadnode = x_atomunit.get_value("label")
            idea_roadunit = x_worldunit.make_road(parent_roadunit, label_roadnode)
            pledge_bool = x_atomunit.get_value("pledge")
            pledge_yes_str = ""
            if pledge_bool:
                pledge_yes_str = "Yes"
            char_id_value = x_atomunit.get_value(char_id_str())
            belief_id_value = x_atomunit.get_value(belief_id_str())
            d2_list.append(
                [
                    x_worldunit._owner_id,
                    pledge_yes_str,
                    x_worldunit._real_id,
                    idea_roadunit,
                    x_atomunit.get_value("_weight"),
                ]
            )
        x_bridge = DataFrame(d2_list, columns=x_bridge.columns)
        sorting_columns = [road_str()]
        x_bridge.sort_values(sorting_columns, ascending=[True], inplace=True)
        x_bridge.reset_index(inplace=True)
        x_bridge.drop(columns=["index"], inplace=True)

    return x_bridge
