from src.a00_data_toolbox.file_toolbox import open_json, create_path
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a08_bud_atom_logic._utils.str_a08 import jkeys_str, jvalues_str
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
        "awardee_label": "LabelUnit",
        "context": "WayUnit",
        "context_idea_active_requisite": "bool",
        "begin": "float",
        "c400_number": "int",
        "celldepth": "int",
        "close": "float",
        "credit_belief": "float",
        "credit_vote": "float",
        "credor_respect": "float",
        "cumlative_day": "int",
        "cumlative_minute": "int",
        "debtit_belief": "float",
        "debtit_vote": "float",
        "debtor_respect": "float",
        "denom": "int",
        "divisor": "int",
        "face_name": "NameUnit",
        "fcontext": "WayUnit",
        "fisc_tag": "TagUnit",
        "fneed": "WayUnit",
        "fnigh": "float",
        "fopen": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_label": "LabelUnit",
        "healer_name": "NameUnit",
        "hour_tag": "TagUnit",
        "mass": "int",
        "max_tree_traverse": "int",
        "month_tag": "TagUnit",
        "monthday_distortion": "int",
        "morph": "bool",
        "need": "WayUnit",
        "nigh": "float",
        "numor": "int",
        "open": "float",
        "offi_time": "TimeLinePoint",
        "owner_name": "NameUnit",
        "penny": "float",
        "job_listen_rotations": "int",
        "pledge": "bool",
        "problem_bool": "bool",
        "quota": "int",
        "respect_bit": "float",
        "idea_way": "WayUnit",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "team_label": "LabelUnit",
        "tran_time": "TimeLinePoint",
        "deal_time": "TimeLinePoint",
        "timeline_tag": "TagUnit",
        "weekday_tag": "TagUnit",
        "weekday_order": "int",
        "bridge": "str",
        "yr1_jan1_offset": "int",
    }


def get_quick_pidgens_column_ref() -> dict[str, set[str]]:
    """for each pidgin_config dimen contains the associated columns"""
    return {
        "pidgin_label": {
            "inx_label",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_label",
        },
        "pidgin_name": {
            "inx_name",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_name",
        },
        "pidgin_tag": {
            "inx_tag",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_tag",
        },
        "pidgin_way": {
            "inx_way",
            "unknown_word",
            "inx_bridge",
            "otx_bridge",
            "otx_way",
        },
    }
