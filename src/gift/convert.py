from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src._world.world import WorldUnit
from src.gift.atom_config import config_file_dir


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


def get_convert_format_dict(convert_format_name: str) -> dict[str, str]:
    convert_format_filename = get_json_filename(convert_format_name)
    convert_format_json = open_file(get_convert_format_dir(), convert_format_filename)
    return get_dict_from_json(convert_format_json)


def _get_headers_list(convert_format_name) -> list[str]:
    return list(get_convert_format_dict(convert_format_name).keys())


def create_convert_format(
    x_worldunit: WorldUnit, convert_format_name: str
) -> list[list]:
    d1_list = []
    if convert_format_name == jaar_format_0001_char_v0_0_0():
        d1_list.append(_get_headers_list(convert_format_name))
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
        d1_list.append(_get_headers_list(convert_format_name))
        unsorted_charunits = list(x_worldunit._chars.values())
        sorted_charunits = sorted(unsorted_charunits, key=lambda x_char: x_char.char_id)
        for x_charunit in sorted_charunits:
            unsorted_beliefholds = list(x_charunit._beliefholds.values())
            sorted_beliefholds = sorted(
                unsorted_beliefholds, key=lambda x_beliefhold: x_beliefhold.belief_id
            )
            for x_beliefunit in sorted_beliefholds:
                d2_list = [
                    x_worldunit._real_id,
                    x_worldunit._owner_id,
                    x_charunit.char_id,
                    x_beliefunit.belief_id,
                    x_beliefunit.credor_weight,
                    x_beliefunit.debtor_weight,
                ]
                d1_list.append(d2_list)

    return d1_list
