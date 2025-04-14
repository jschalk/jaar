from src.a00_data_toolboxs.file_toolbox import open_json, create_path
from src.a00_data_toolboxs.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd


def timeline_str() -> str:
    return "timeline"


def offi_time_str() -> str:
    return "offi_time"


def brokerunits_str() -> str:
    return "brokerunits"


def cashbook_str() -> str:
    return "cashbook"


def amount_str() -> str:
    return "amount"


def month_title_str() -> str:
    return "month_title"


def hour_title_str() -> str:
    return "hour_title"


def cumlative_minute_str() -> str:
    return "cumlative_minute"


def cumlative_day_str() -> str:
    return "cumlative_day"


def weekday_title_str() -> str:
    return "weekday_title"


def weekday_order_str() -> str:
    return "weekday_order"


def get_fisc_config_filename() -> str:
    return "fisc_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f08_fisc")


# def fiscunit_str()-> str: return "fiscunit"
# def fisc_dealunit_str()-> str: return "fisc_dealunit"
# def fisc_cashbook_str()-> str: return "fisc_cashbook"
# def fisc_timeline_hour_str()-> str: return "fisc_timeline_hour"
# def fisc_timeline_month_str()-> str: return "fisc_timeline_month"
# def fisc_timeline_weekday_str()-> str: return "fisc_timeline_weekday"
def fiscunit_str() -> str:
    return "fiscunit"


def fisc_dealunit_str() -> str:
    return "fisc_dealunit"


def fisc_cashbook_str() -> str:
    return "fisc_cashbook"


def fisc_timeline_hour_str() -> str:
    return "fisc_timeline_hour"


def fisc_timeline_month_str() -> str:
    return "fisc_timeline_month"


def fisc_timeline_weekday_str() -> str:
    return "fisc_timeline_weekday"


def fisc_timeoffi_str() -> str:
    return "fisc_timeoffi"


def get_fisc_config_dict() -> dict:
    return open_json(config_file_dir(), get_fisc_config_filename())


def get_fisc_dimens() -> set[str]:
    return {
        "fiscunit",
        "fisc_dealunit",
        "fisc_cashbook",
        "fisc_timeline_hour",
        "fisc_timeline_month",
        "fisc_timeline_weekday",
        "fisc_timeoffi",
    }


def get_fisc_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_fisc_config_dict(), jkeys_key_list)


def get_fisc_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_fisc_config_dict(), jvalues_key_list)


def get_fisc_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_fisc_config_jkeys(x_dimen)
    args_dict.update(get_fisc_config_jvalues(x_dimen))
    return args_dict


def get_fisc_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for fisc_dimen in get_fisc_config_dict().keys():
        args_set = set(get_fisc_config_args(fisc_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = set()
            x_dimen_set = x_dict.get(x_arg)
            x_dimen_set.add(fisc_dimen)
            x_dict[x_arg] = x_dimen_set
    return x_dict


def get_fisc_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "NameUnit",
        "amount": "float",
        "bridge": "str",
        "celldepth": "int",
        "c400_number": "int",
        "cumlative_day": "int",
        "cumlative_minute": "int",
        "deal_time": "TimeLinePoint",
        "hour_title": "TitleUnit",
        "fisc_title": "TitleUnit",
        "fund_coin": "float",
        "month_title": "TitleUnit",
        "monthday_distortion": "int",
        "penny": "float",
        "offi_time": "TimeLinePoint",
        "owner_name": "NameUnit",
        "quota": "int",
        "plan_listen_rotations": "int",
        "respect_bit": "float",
        "tran_time": "TimeLinePoint",
        "timeline_title": "TitleUnit",
        "weekday_title": "TitleUnit",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_fisc_args_set() -> set[str]:
    return {
        "acct_name",
        "amount",
        "bridge",
        "c400_number",
        "celldepth",
        "cumlative_day",
        "cumlative_minute",
        "deal_time",
        "hour_title",
        "fisc_title",
        "fund_coin",
        "month_title",
        "monthday_distortion",
        "plan_listen_rotations",
        "penny",
        "offi_time",
        "owner_name",
        "quota",
        "respect_bit",
        "tran_time",
        "timeline_title",
        "weekday_title",
        "weekday_order",
        "yr1_jan1_offset",
    }
