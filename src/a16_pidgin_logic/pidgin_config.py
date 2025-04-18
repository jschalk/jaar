from src.a00_data_toolboxs.file_toolbox import open_json, create_path
from src.a00_data_toolboxs.dict_toolbox import get_from_nested_dict
from src.a08_bud_atom_logic.atom_config import jkeys_str, jvalues_str
from os import getcwd as os_getcwd


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a16_pidgin_logic")


def get_pidgin_config_filename() -> str:
    return "pidgin_config.json"


def get_pidgin_config_dict() -> dict:
    return open_json(config_file_dir(), get_pidgin_config_filename())


def get_pidgin_dimens() -> set[str]:
    return set(get_pidgin_config_dict().keys())


def pidginunit_str() -> str:
    return "pidginunit"


def pidgin_filename() -> str:
    return "pidgin.json"


def otx_bridge_str() -> str:
    return "otx_bridge"


def inx_bridge_str() -> str:
    return "inx_bridge"


def inx_label_str() -> str:
    return "inx_label"


def otx_label_str() -> str:
    return "otx_label"


def inx_name_str() -> str:
    return "inx_name"


def otx_name_str() -> str:
    return "otx_name"


def inx_title_str() -> str:
    return "inx_title"


def otx_title_str() -> str:
    return "otx_title"


def inx_road_str() -> str:
    return "inx_road"


def otx_road_str() -> str:
    return "otx_road"


def unknown_word_str() -> str:
    return "unknown_word"


def otx2inx_str() -> str:
    return "otx2inx"


def map_otx2inx_str() -> str:
    return "map_otx2inx"


def map_name_str() -> str:
    return "map_name"


def map_label_str() -> str:
    return "map_label"


def map_title_str() -> str:
    return "map_title"


def map_road_str() -> str:
    return "map_road"


def default_unknown_word() -> str:
    return "UNKNOWN"


def default_unknown_word_if_None(unknown_word: any = None) -> str:
    if unknown_word != unknown_word:
        unknown_word = None
    if unknown_word is None:
        unknown_word = default_unknown_word()
    return unknown_word


def get_pidgin_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, jkeys_str()]
    return get_from_nested_dict(get_pidgin_config_dict(), jkeys_key_list)


def get_pidgin_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, jvalues_str()]
    return get_from_nested_dict(get_pidgin_config_dict(), jvalues_key_list)


def get_pidgin_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_pidgin_config_jkeys(x_dimen)
    args_dict.update(get_pidgin_config_jvalues(x_dimen))
    return args_dict


def get_pidgin_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for pidgin_dimen in get_pidgin_config_dict().keys():
        args_set = set(get_pidgin_config_args(pidgin_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {pidgin_dimen}
            else:
                x_dimen_set = x_dict.get(x_arg)
                x_dimen_set.add(pidgin_dimen)
                x_dict[x_arg] = x_dimen_set
    return x_dict


def get_pidgin_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "NameUnit",
        "addin": "float",
        "amount": "float",
        "awardee_tag": "LabelUnit",
        "base": "RoadUnit",
        "base_item_active_requisite": "bool",
        "begin": "float",
        "c400_number": "int",
        "celldepth": "int",
        "close": "float",
        "credit_belief": "int",
        "credit_vote": "int",
        "credor_respect": "int",
        "cumlative_day": "int",
        "cumlative_minute": "int",
        "debtit_belief": "int",
        "debtit_vote": "int",
        "debtor_respect": "int",
        "denom": "int",
        "divisor": "int",
        "face_name": "NameUnit",
        "fisc_title": "TitleUnit",
        "fnigh": "float",
        "fopen": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_label": "LabelUnit",
        "healer_name": "NameUnit",
        "hour_title": "TitleUnit",
        "item_title": "TitleUnit",
        "mass": "int",
        "max_tree_traverse": "int",
        "month_title": "TitleUnit",
        "monthday_distortion": "int",
        "morph": "bool",
        "need": "RoadUnit",
        "nigh": "float",
        "numor": "int",
        "open": "float",
        "offi_time": "TimeLinePoint",
        "owner_name": "NameUnit",
        "parent_road": "RoadUnit",
        "penny": "float",
        "pick": "RoadUnit",
        "job_listen_rotations": "int",
        "pledge": "bool",
        "problem_bool": "bool",
        "quota": "int",
        "respect_bit": "float",
        "road": "RoadUnit",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "team_tag": "LabelUnit",
        "tran_time": "TimeLinePoint",
        "deal_time": "TimeLinePoint",
        "timeline_title": "TitleUnit",
        "weekday_title": "TitleUnit",
        "weekday_order": "int",
        "bridge": "str",
        "yr1_jan1_offset": "int",
    }


def get_quick_pidgens_column_ref() -> dict[str, set[str]]:
    """for each pidgin_config dimen contains the associated columns"""
    return {
        "map_label": {
            "inx_label",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_label",
        },
        "map_name": {
            "inx_name",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_name",
        },
        "map_title": {
            "inx_title",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_title",
        },
        "map_road": {
            "inx_road",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_road",
        },
    }
