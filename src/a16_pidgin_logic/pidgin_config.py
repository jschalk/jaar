from src.a00_data_toolbox.file_toolbox import open_json, create_path
from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a08_bud_atom_logic._utils.str_a08 import jkeys_str, jvalues_str
from src.a08_bud_atom_logic.atom_config import get_all_bud_dimen_delete_keys
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


def default_unknown_term() -> str:
    return "UNKNOWN"


def default_unknown_term_if_None(unknown_term: any = None) -> str:
    if unknown_term != unknown_term:
        unknown_term = None
    if unknown_term is None:
        unknown_term = default_unknown_term()
    return unknown_term


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
        "acct_name": "NameStr",
        "addin": "float",
        "amount": "float",
        "awardee_title": "TitleStr",
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
        "face_name": "NameStr",
        "fcontext": "WayStr",
        "fisc_label": "LabelStr",
        "fstate": "WayStr",
        "fnigh": "float",
        "fopen": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_title": "TitleStr",
        "healer_name": "NameStr",
        "hour_label": "LabelStr",
        "concept_way": "WayStr",
        "mass": "int",
        "max_tree_traverse": "int",
        "month_label": "LabelStr",
        "monthday_distortion": "int",
        "morph": "bool",
        "numor": "int",
        "offi_time": "TimeLinePoint",
        "owner_name": "NameStr",
        "penny": "float",
        "job_listen_rotations": "int",
        "pledge": "bool",
        "problem_bool": "bool",
        "quota": "int",
        "pstate": "WayStr",
        "pdivisor": "int",
        "popen": "float",
        "pnigh": "float",
        "rcontext": "WayStr",
        "rcontext_concept_active_requisite": "bool",
        "respect_bit": "float",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "labor_title": "TitleStr",
        "tran_time": "TimeLinePoint",
        "deal_time": "TimeLinePoint",
        "timeline_label": "LabelStr",
        "weekday_label": "LabelStr",
        "weekday_order": "int",
        "bridge": "str",
        "yr1_jan1_offset": "int",
    }


def get_quick_pidgens_column_ref() -> dict[str, set[str]]:
    """for each pidgin_config dimen contains the associated columns"""
    return {
        "pidgin_title": {
            "inx_title",
            "otx_title",
            "inx_bridge",
            "otx_bridge",
            "unknown_term",
        },
        "pidgin_name": {
            "inx_name",
            "otx_name",
            "inx_bridge",
            "otx_bridge",
            "unknown_term",
        },
        "pidgin_label": {
            "inx_label",
            "otx_label",
            "inx_bridge",
            "otx_bridge",
            "unknown_term",
        },
        "pidgin_way": {
            "inx_way",
            "otx_way",
            "inx_bridge",
            "otx_bridge",
            "unknown_term",
        },
    }


def pidginable_class_types() -> set:
    return {"NameStr", "TitleStr", "LabelStr", "WayStr"}


def get_pidginable_args() -> set:
    return {
        "acct_name",
        "awardee_title",
        "face_name",
        "fcontext",
        "fisc_label",
        "fstate",
        "group_title",
        "healer_name",
        "hour_label",
        "concept_way",
        "month_label",
        "owner_name",
        "pstate",
        "rcontext",
        "labor_title",
        "timeline_label",
        "weekday_label",
    }


def find_set_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Pidginable" args replaced with "_otx" and "_inx" """
    all_pidginable = get_pidginable_args()
    all_pidginable.update(get_all_bud_dimen_delete_keys())
    all_pidginable.intersection_update(args)
    transformed_args = set()
    for arg in args:
        if arg in all_pidginable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args


def get_pidgin_NameStr_args() -> set[str]:
    return {
        "acct_name",
        "face_name",
        "healer_name",
        "owner_name",
    }


def get_pidgin_TitleStr_args() -> set[str]:
    return {
        "awardee_title",
        "group_title",
        "labor_title",
    }


def get_pidgin_LabelStr_args() -> set[str]:
    return {
        "fisc_label",
        "hour_label",
        "month_label",
        "timeline_label",
        "weekday_label",
    }


def get_pidgin_WayStr_args() -> set[str]:
    return {
        "fstate",
        "fcontext",
        "concept_way",
        "pstate",
        "rcontext",
    }
