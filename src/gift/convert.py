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
from pandas import DataFrame


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


def get_convert_format_dir() -> str:
    return f"{config_file_dir()}/convert_formats"


def jaar_format_0001_char_v0_0_0() -> str:
    return "jaar_format_0001_char_v0_0_0"


def jaar_format_0002_beliefhold_v0_0_0() -> str:
    return "jaar_format_0002_beliefhold_v0_0_0"


def jaar_format_0003_ideaunit_v0_0_0() -> str:
    return "jaar_format_0003_ideaunit_v0_0_0"


def get_convert_format_filenames() -> set[str]:
    return {
        jaar_format_0001_char_v0_0_0(),
        jaar_format_0002_beliefhold_v0_0_0(),
        jaar_format_0003_ideaunit_v0_0_0(),
    }


def get_convert_format_dict(convert_format_name: str) -> dict[str,]:
    convert_format_filename = get_json_filename(convert_format_name)
    convert_format_json = open_file(get_convert_format_dir(), convert_format_filename)
    return get_dict_from_json(convert_format_json)


def _get_headers_list(convert_format_name: str) -> list[str]:
    return list(get_convert_format_dict(convert_format_name).keys())


def create_convert_dataframe(convert_format_name: str) -> DataFrame:
    return DataFrame(columns=_get_headers_list(convert_format_name))


def create_convert_format(
    x_worldunit: WorldUnit, convert_format_name: str
) -> list[list]:
    d1_list = [_get_headers_list(convert_format_name)]

    if convert_format_name == jaar_format_0001_char_v0_0_0():
        unsorted_charunits = list(x_worldunit._chars.values())
        sorted_charunits = sorted(unsorted_charunits, key=lambda x_char: x_char.char_id)
        for x_charunit in sorted_charunits:
            d2_list = [
                x_worldunit._real_id,
                x_worldunit._owner_id,
                x_worldunit._char_debtor_pool,
                x_charunit.char_id,
                x_charunit.credor_weight,
                x_charunit.debtor_weight,
            ]
            d1_list.append(d2_list)

    elif convert_format_name == jaar_format_0002_beliefhold_v0_0_0():
        x_changeunit = changeunit_shop()
        x_changeunit.add_all_atomunits(x_worldunit)
        category_set = [world_char_beliefhold_text()]
        curd_set = [atom_insert()]
        filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
        sorted_atomunits = filtered_change.get_category_sorted_atomunits_list()
        for x_beliefhold_atomunit in sorted_atomunits:
            char_id_value = x_beliefhold_atomunit.get_value(char_id_str())
            belief_id_value = x_beliefhold_atomunit.get_value(belief_id_str())
            d1_list.append(
                [
                    x_worldunit._real_id,
                    x_worldunit._owner_id,
                    char_id_value,
                    belief_id_value,
                    x_beliefhold_atomunit.get_value(credor_weight_str()),
                    x_beliefhold_atomunit.get_value(debtor_weight_str()),
                ]
            )
    elif convert_format_name == jaar_format_0003_ideaunit_v0_0_0():
        x_changeunit = changeunit_shop()
        x_changeunit.add_all_atomunits(x_worldunit)
        category_set = [world_ideaunit_text()]
        curd_set = [atom_insert()]
        filtered_change = get_filtered_changeunit(x_changeunit, category_set, curd_set)
        sorted_idea_atomunits = filtered_change.get_category_sorted_atomunits_list()
        for x_idea_atomunit in sorted_idea_atomunits:
            parent_roadunit = x_idea_atomunit.get_value("parent_road")
            label_roadnode = x_idea_atomunit.get_value("label")
            idea_roadunit = x_worldunit.make_road(parent_roadunit, label_roadnode)
            pledge_bool = x_idea_atomunit.get_value("pledge")
            pledge_yes_str = ""
            if pledge_bool:
                pledge_yes_str = "Yes"
            d1_list.append(
                [
                    x_worldunit._real_id,
                    x_worldunit._owner_id,
                    idea_roadunit,
                    x_idea_atomunit.get_value("_weight"),
                    pledge_yes_str,
                ]
            )

    return d1_list
