from src.f00_instrument.file import open_file, create_path
from src.f00_instrument.dict_toolbox import get_dict_from_json, get_from_nested_dict
from os import getcwd as os_getcwd


def timeline_str() -> str:
    return "timeline"


def current_time_str() -> str:
    return "current_time"


def deallogs_str() -> str:
    return "deallogs"


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


def get_fiscal_config_file_name() -> str:
    return "fiscal_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f07_fiscal")


# def fiscalunit_str()-> str: return "fiscalunit"
# def fiscal_deal_episode_str()-> str: return "fiscal_deal_episode"
# def fiscal_cashbook_str()-> str: return "fiscal_cashbook"
# def fiscal_timeline_hour_str()-> str: return "fiscal_timeline_hour"
# def fiscal_timeline_month_str()-> str: return "fiscal_timeline_month"
# def fiscal_timeline_weekday_str()-> str: return "fiscal_timeline_weekday"
def fiscalunit_str() -> str:
    return "fiscalunit"


def fiscal_deal_episode_str() -> str:
    return "fiscal_deal_episode"


def fiscal_cashbook_str() -> str:
    return "fiscal_cashbook"


def fiscal_timeline_hour_str() -> str:
    return "fiscal_timeline_hour"


def fiscal_timeline_month_str() -> str:
    return "fiscal_timeline_month"


def fiscal_timeline_weekday_str() -> str:
    return "fiscal_timeline_weekday"


def get_fiscal_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_fiscal_config_file_name())
    )


def get_fiscal_categorys() -> set[str]:
    return set(get_fiscal_config_dict().keys())


def get_fiscal_config_jkeys(x_cat: str) -> dict:
    jkeys_key_list = [x_cat, "jkeys"]
    return get_from_nested_dict(get_fiscal_config_dict(), jkeys_key_list)


def get_fiscal_config_jvalues(x_cat: str) -> dict:
    jvalues_key_list = [x_cat, "jvalues"]
    return get_from_nested_dict(get_fiscal_config_dict(), jvalues_key_list)


def get_fiscal_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_fiscal_config_jkeys(x_category)
    args_dict.update(get_fiscal_config_jvalues(x_category))
    return args_dict


def get_fiscal_args_category_mapping() -> dict[str, str]:
    x_dict = {}
    for fiscal_category in get_fiscal_config_dict().keys():
        args_set = set(get_fiscal_config_args(fiscal_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {fiscal_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(fiscal_category)
                x_dict[x_arg] = x_category_set
    return x_dict


def get_fiscal_args_class_types() -> dict[str, str]:
    return {
        "acct_name": "AcctName",
        "amount": "float",
        "bridge": "str",
        "c400_number": "int",
        "cumlative_day": "int",
        "cumlative_minute": "int",
        "current_time": "int",
        "hour_title": "TitleUnit",
        "fiscal_title": "TitleUnit",
        "fund_coin": "float",
        "month_title": "TitleUnit",
        "monthday_distortion": "int",
        "penny": "float",
        "owner_name": "AcctName",
        "quota": "int",
        "respect_bit": "float",
        "time_int": "TimeLinePoint",
        "timeline_title": "TitleUnit",
        "weekday_title": "TitleUnit",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_fiscal_args_set() -> set[str]:
    return {
        "acct_name",
        "amount",
        "bridge",
        "c400_number",
        "cumlative_day",
        "cumlative_minute",
        "current_time",
        "hour_title",
        "fiscal_title",
        "fund_coin",
        "month_title",
        "monthday_distortion",
        "penny",
        "owner_name",
        "quota",
        "respect_bit",
        "time_int",
        "timeline_title",
        "weekday_title",
        "weekday_order",
        "yr1_jan1_offset",
    }
