from os import getcwd as os_getcwd
from src.ch01_data_toolbox.dict_toolbox import get_from_nested_dict
from src.ch01_data_toolbox.file_toolbox import create_path, open_json
from src.ch09_belief_atom_logic.atom_config import get_all_belief_dimen_delete_keys


def pidgin_config_path() -> str:
    "Returns path: a16_pidgin_logic/pidgin_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_pidgin_logic")
    return create_path(chapter_dir, "pidgin_config.json")


def get_pidgin_filename() -> str:
    return "pidgin.json"


def get_pidgin_config_dict() -> dict:
    return open_json(pidgin_config_path())


def get_pidgin_dimens() -> set[str]:
    return set(get_pidgin_config_dict().keys())


def default_unknown_str() -> str:
    return "UNKNOWN"


def default_unknown_str_if_None(unknown_str: any = None) -> str:
    if unknown_str != unknown_str:
        unknown_str = None
    if unknown_str is None:
        unknown_str = default_unknown_str()
    return unknown_str


def get_pidgin_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_pidgin_config_dict(), jkeys_key_list)


def get_pidgin_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
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
        "voice_name": "NameTerm",
        "addin": "float",
        "amount": "float",
        "awardee_title": "TitleTerm",
        "begin": "float",
        "c400_number": "int",
        "celldepth": "int",
        "close": "float",
        "voice_cred_points": "float",
        "group_cred_points": "float",
        "credor_respect": "float",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "voice_debt_points": "float",
        "group_debt_points": "float",
        "debtor_respect": "float",
        "denom": "int",
        "face_name": "NameTerm",
        "fact_context": "RopeTerm",
        "moment_label": "LabelTerm",
        "fact_state": "RopeTerm",
        "fact_upper": "float",
        "fact_lower": "float",
        "fund_iota": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_title": "TitleTerm",
        "healer_name": "NameTerm",
        "hour_label": "LabelTerm",
        "plan_rope": "RopeTerm",
        "star": "int",
        "max_tree_traverse": "int",
        "month_label": "LabelTerm",
        "monthday_distortion": "int",
        "morph": "bool",
        "numor": "int",
        "offi_time": "TimeLinePoint",
        "belief_name": "NameTerm",
        "penny": "float",
        "job_listen_rotations": "int",
        "task": "bool",
        "problem_bool": "bool",
        "quota": "int",
        "reason_state": "RopeTerm",
        "reason_divisor": "int",
        "reason_lower": "float",
        "reason_upper": "float",
        "reason_context": "RopeTerm",
        "reason_active_requisite": "bool",
        "respect_bit": "float",
        "solo": "int",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "party_title": "TitleTerm",
        "tran_time": "TimeLinePoint",
        "bud_time": "TimeLinePoint",
        "timeline_label": "LabelTerm",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "knot": "str",
        "yr1_jan1_offset": "int",
    }


def get_quick_pidgens_column_ref() -> dict[str, set[str]]:
    """for each pidgin_config dimen contains the associated columns"""
    return {
        "pidgin_title": {
            "inx_title",
            "otx_title",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "pidgin_name": {
            "inx_name",
            "otx_name",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "pidgin_label": {
            "inx_label",
            "otx_label",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "pidgin_rope": {
            "inx_rope",
            "otx_rope",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
    }


def pidginable_class_types() -> set:
    return {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm"}


def get_pidginable_args() -> set:
    return {
        "voice_name",
        "awardee_title",
        "face_name",
        "fact_context",
        "moment_label",
        "fact_state",
        "group_title",
        "healer_name",
        "hour_label",
        "plan_rope",
        "month_label",
        "belief_name",
        "reason_state",
        "reason_context",
        "party_title",
        "timeline_label",
        "weekday_label",
    }


def find_set_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Pidginable" args replaced with "_otx" and "_inx" """
    all_pidginable = get_pidginable_args()
    all_pidginable.update(get_all_belief_dimen_delete_keys())
    all_pidginable.intersection_update(args)
    transformed_args = set()
    for arg in args:
        if arg in all_pidginable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args


def get_pidgin_NameTerm_args() -> set[str]:
    return {
        "voice_name",
        "face_name",
        "healer_name",
        "belief_name",
    }


def get_pidgin_TitleTerm_args() -> set[str]:
    return {
        "awardee_title",
        "group_title",
        "party_title",
    }


def get_pidgin_LabelTerm_args() -> set[str]:
    return {
        "moment_label",
        "hour_label",
        "month_label",
        "timeline_label",
        "weekday_label",
    }


def get_pidgin_RopeTerm_args() -> set[str]:
    return {
        "fact_state",
        "fact_context",
        "plan_rope",
        "reason_state",
        "reason_context",
    }
