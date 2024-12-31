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


def month_idea_str() -> str:
    return "month_idea"


def hour_idea_str() -> str:
    return "hour_idea"


def cumlative_minute_str() -> str:
    return "cumlative_minute"


def cumlative_day_str() -> str:
    return "cumlative_day"


def weekday_idea_str() -> str:
    return "weekday_idea"


def weekday_order_str() -> str:
    return "weekday_order"


def get_gov_config_file_name() -> str:
    return "gov_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f07_gov")


# def govunit_str()-> str: return "govunit"
# def gov_deallog_str()-> str: return "gov_deallog"
# def gov_deal_episode_str()-> str: return "gov_deal_episode"
# def gov_cashbook_str()-> str: return "gov_cashbook"
# def gov_timeline_hour_str()-> str: return "gov_timeline_hour"
# def gov_timeline_month_str()-> str: return "gov_timeline_month"
# def gov_timeline_weekday_str()-> str: return "gov_timeline_weekday"
def govunit_str() -> str:
    return "govunit"


def gov_deallog_str() -> str:
    return "gov_deallog"


def gov_deal_episode_str() -> str:
    return "gov_deal_episode"


def gov_cashbook_str() -> str:
    return "gov_cashbook"


def gov_timeline_hour_str() -> str:
    return "gov_timeline_hour"


def gov_timeline_month_str() -> str:
    return "gov_timeline_month"


def gov_timeline_weekday_str() -> str:
    return "gov_timeline_weekday"


def get_gov_config_dict() -> dict:
    return get_dict_from_json(open_file(config_file_dir(), get_gov_config_file_name()))


def get_gov_categorys() -> set[str]:
    return set(get_gov_config_dict().keys())


def get_gov_config_jkeys(x_cat: str) -> dict:
    jkeys_key_list = [x_cat, "jkeys"]
    return get_from_nested_dict(get_gov_config_dict(), jkeys_key_list)


def get_gov_config_jvalues(x_cat: str) -> dict:
    jvalues_key_list = [x_cat, "jvalues"]
    return get_from_nested_dict(get_gov_config_dict(), jvalues_key_list)


def get_gov_config_args(x_category: str) -> dict[str, dict]:
    args_dict = get_gov_config_jkeys(x_category)
    args_dict.update(get_gov_config_jvalues(x_category))
    return args_dict


def get_gov_args_category_mapping() -> dict[str, str]:
    x_dict = {}
    for gov_category in get_gov_config_dict().keys():
        args_set = set(get_gov_config_args(gov_category))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {gov_category}
            else:
                x_category_set = x_dict.get(x_arg)
                x_category_set.add(gov_category)
                x_dict[x_arg] = x_category_set
    return x_dict


def get_gov_args_jaar_types() -> dict[str, str]:
    return {
        "acct_name": "AcctName",
        "amount": "float",
        "c400_number": "int",
        "cumlative_day": "int",
        "cumlative_minute": "int",
        "current_time": "int",
        "hour_idea": "IdeaUnit",
        "gov_idea": "IdeaUnit",
        "fund_coin": "float",
        "month_idea": "IdeaUnit",
        "monthday_distortion": "int",
        "penny": "float",
        "owner_name": "AcctName",
        "quota": "int",
        "respect_bit": "float",
        "time_int": "TimeLinePoint",
        "timeline_idea": "IdeaUnit",
        "weekday_idea": "IdeaUnit",
        "weekday_order": "int",
        "bridge": "str",
        "yr1_jan1_offset": "int",
    }
