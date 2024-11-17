from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import get_dict_from_json
from src.f01_road.jaar_config import get_json_filename
from src.f02_bud.bud_tool import budunit_str
from src.f07_fiscal.fiscal_config import fiscalunit_str
from src.f08_pidgin.pidgin_config import pidginunit_str
from src.f09_brick.examples.brick_env import src_brick_dir
from os import getcwd as os_getcwd


def get_brick_config_file_name() -> str:
    return "brick_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/f09_brick"


def get_brick_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_brick_config_file_name())
    )


def brick_number_str() -> str:
    return "brick_number"


def brick_type_str() -> str:
    return "brick_type"


def get_brick_types() -> set[str]:
    return {budunit_str(), fiscalunit_str(), pidginunit_str()}


def allowed_crud_str() -> str:
    return "allowed_crud"


def categorys_str() -> str:
    return "categorys"


def otx_key_str() -> str:
    return "otx_key"


def attributes_str() -> str:
    return "attributes"


def insert_one_time_str() -> str:
    return "INSERT_ONE_TIME"


def insert_mulitple_str() -> str:
    return "INSERT_MULITPLE"


def delete_insert_update_str() -> str:
    return "DELETE_INSERT_UPDATE"


def insert_update_str() -> str:
    return "INSERT_UPDATE"


def delete_insert_str() -> str:
    return "DELETE_INSERT"


def delete_update_str() -> str:
    return "DELETE_UPDATE"


def build_order_str() -> str:
    return "build_order"


def get_allowed_curds() -> set[str]:
    return {
        "INSERT_ONE_TIME",
        "INSERT_MULITPLE",
        "DELETE_INSERT_UPDATE",
        "INSERT_UPDATE",
        "DELETE_INSERT",
        "DELETE_UPDATE",
        "UPDATE",
        "DELETE",
        "INSERT",
    }


def get_brick_formats_dir() -> str:
    return f"{src_brick_dir()}/brick_formats"


# def brick_format_00000_fiscalunit_v0_0_0()->str: return "brick_format_00000_fiscalunit_v0_0_0"
# def brick_format_00001_fiscal_purview_episode_v0_0_0()->str: return "brick_format_00001_fiscal_purview_episode_v0_0_0"
# def brick_format_00002_fiscal_cashbook_v0_0_0()->str: return "brick_format_00002_fiscal_cashbook_v0_0_0"
# def brick_format_00003_fiscal_timeline_hour_v0_0_0()->str: return "brick_format_00003_fiscal_timeline_hour_v0_0_0"
# def brick_format_00004_fiscal_timeline_month_v0_0_0()->str: return "brick_format_00004_fiscal_timeline_month_v0_0_0"
# def brick_format_00005_fiscal_timeline_weekday_v0_0_0()->str: return "brick_format_00005_fiscal_timeline_weekday_v0_0_0"


def brick_format_00000_fiscalunit_v0_0_0() -> str:
    return "brick_format_00000_fiscalunit_v0_0_0"


def brick_format_00001_fiscal_purview_episode_v0_0_0() -> str:
    return "brick_format_00001_fiscal_purview_episode_v0_0_0"


def brick_format_00002_fiscal_cashbook_v0_0_0() -> str:
    return "brick_format_00002_fiscal_cashbook_v0_0_0"


def brick_format_00003_fiscal_timeline_hour_v0_0_0() -> str:
    return "brick_format_00003_fiscal_timeline_hour_v0_0_0"


def brick_format_00004_fiscal_timeline_month_v0_0_0() -> str:
    return "brick_format_00004_fiscal_timeline_month_v0_0_0"


def brick_format_00005_fiscal_timeline_weekday_v0_0_0() -> str:
    return "brick_format_00005_fiscal_timeline_weekday_v0_0_0"


def brick_format_00011_acct_v0_0_0() -> str:
    return "brick_format_00011_acct_v0_0_0"


def brick_format_00012_membership_v0_0_0() -> str:
    return "brick_format_00012_membership_v0_0_0"


def brick_format_00013_itemunit_v0_0_0() -> str:
    return "brick_format_00013_itemunit_v0_0_0"


def brick_format_00019_itemunit_v0_0_0() -> str:
    return "brick_format_00019_itemunit_v0_0_0"


def brick_format_00036_problem_healer_v0_0_0() -> str:
    return "brick_format_00036_problem_healer_v0_0_0"


# def brick_format_00020_bud_acct_membership_v0_0_0()-> str: return "brick_format_00020_bud_acct_membership_v0_0_0"
# def brick_format_00021_bud_acctunit_v0_0_0()-> str: return "brick_format_00021_bud_acctunit_v0_0_0"
# def brick_format_00022_bud_item_awardlink_v0_0_0()-> str: return "brick_format_00022_bud_item_awardlink_v0_0_0"
# def brick_format_00023_bud_item_factunit_v0_0_0()-> str: return "brick_format_00023_bud_item_factunit_v0_0_0"
# def brick_format_00024_bud_item_teamlink_v0_0_0()-> str: return "brick_format_00024_bud_item_teamlink_v0_0_0"
# def brick_format_00025_bud_item_healerlink_v0_0_0()-> str: return "brick_format_00025_bud_item_healerlink_v0_0_0"
# def brick_format_00026_bud_item_reason_premiseunit_v0_0_0()-> str: return "brick_format_00026_bud_item_reason_premiseunit_v0_0_0"
# def brick_format_00027_bud_item_reasonunit_v0_0_0()-> str: return "brick_format_00027_bud_item_reasonunit_v0_0_0"
# def brick_format_00028_bud_itemunit_v0_0_0()-> str: return "brick_format_00028_bud_itemunit_v0_0_0"
# def brick_format_00029_budunit_v0_0_0()-> str: return "brick_format_00029_budunit_v0_0_0"


def brick_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "brick_format_00020_bud_acct_membership_v0_0_0"


def brick_format_00021_bud_acctunit_v0_0_0() -> str:
    return "brick_format_00021_bud_acctunit_v0_0_0"


def brick_format_00022_bud_item_awardlink_v0_0_0() -> str:
    return "brick_format_00022_bud_item_awardlink_v0_0_0"


def brick_format_00023_bud_item_factunit_v0_0_0() -> str:
    return "brick_format_00023_bud_item_factunit_v0_0_0"


def brick_format_00024_bud_item_teamlink_v0_0_0() -> str:
    return "brick_format_00024_bud_item_teamlink_v0_0_0"


def brick_format_00025_bud_item_healerlink_v0_0_0() -> str:
    return "brick_format_00025_bud_item_healerlink_v0_0_0"


def brick_format_00026_bud_item_reason_premiseunit_v0_0_0() -> str:
    return "brick_format_00026_bud_item_reason_premiseunit_v0_0_0"


def brick_format_00027_bud_item_reasonunit_v0_0_0() -> str:
    return "brick_format_00027_bud_item_reasonunit_v0_0_0"


def brick_format_00028_bud_itemunit_v0_0_0() -> str:
    return "brick_format_00028_bud_itemunit_v0_0_0"


def brick_format_00029_budunit_v0_0_0() -> str:
    return "brick_format_00029_budunit_v0_0_0"


def brick_format_00040_bridge_otx2inx_v0_0_0() -> str:
    return "brick_format_00040_bridge_otx2inx_v0_0_0"


def brick_format_00041_bridge_nub_label_v0_0_0() -> str:
    return "brick_format_00041_bridge_nub_label_v0_0_0"


def brick_format_00113_acct_otx2inx_v0_0_0() -> str:
    return "brick_format_00113_acct_otx2inx_v0_0_0"


def get_brick_format_filenames() -> set[str]:
    return {
        brick_format_00000_fiscalunit_v0_0_0(),
        brick_format_00001_fiscal_purview_episode_v0_0_0(),
        brick_format_00002_fiscal_cashbook_v0_0_0(),
        brick_format_00003_fiscal_timeline_hour_v0_0_0(),
        brick_format_00004_fiscal_timeline_month_v0_0_0(),
        brick_format_00005_fiscal_timeline_weekday_v0_0_0(),
        brick_format_00011_acct_v0_0_0(),
        brick_format_00012_membership_v0_0_0(),
        brick_format_00013_itemunit_v0_0_0(),
        brick_format_00019_itemunit_v0_0_0(),
        brick_format_00020_bud_acct_membership_v0_0_0(),
        brick_format_00021_bud_acctunit_v0_0_0(),
        brick_format_00022_bud_item_awardlink_v0_0_0(),
        brick_format_00023_bud_item_factunit_v0_0_0(),
        brick_format_00024_bud_item_teamlink_v0_0_0(),
        brick_format_00025_bud_item_healerlink_v0_0_0(),
        brick_format_00026_bud_item_reason_premiseunit_v0_0_0(),
        brick_format_00027_bud_item_reasonunit_v0_0_0(),
        brick_format_00028_bud_itemunit_v0_0_0(),
        brick_format_00029_budunit_v0_0_0(),
        brick_format_00036_problem_healer_v0_0_0(),
        brick_format_00040_bridge_otx2inx_v0_0_0(),
        brick_format_00041_bridge_nub_label_v0_0_0(),
        brick_format_00113_acct_otx2inx_v0_0_0(),
    }


def get_brick_numbers() -> set[str]:
    return {
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        "br00011",
        "br00012",
        "br00013",
        "br00019",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00036",
        "br00040",
        "br00041",
        "br00113",
    }


def get_brick_format_filename(brick_number: str) -> str:
    brick_number_substring = brick_number[2:]
    for brick_format_filename in get_brick_format_filenames():
        if brick_format_filename[13:18] == brick_number_substring:
            return brick_format_filename


def get_brick_format_headers() -> dict[str, list[str]]:
    return {
        "c400_number,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,road_delimiter,timeline_label,yr1_jan1_offset": brick_format_00000_fiscalunit_v0_0_0(),
        "acct_id,fiscal_id,owner_id,quota,time_id": brick_format_00001_fiscal_purview_episode_v0_0_0(),
        "acct_id,amount,fiscal_id,owner_id,time_id": brick_format_00002_fiscal_cashbook_v0_0_0(),
        "cumlative_minute,fiscal_id,hour_label": brick_format_00003_fiscal_timeline_hour_v0_0_0(),
        "cumlative_day,fiscal_id,month_label": brick_format_00004_fiscal_timeline_month_v0_0_0(),
        "fiscal_id,weekday_label,weekday_order": brick_format_00005_fiscal_timeline_weekday_v0_0_0(),
        "acct_id,fiscal_id,owner_id": brick_format_00011_acct_v0_0_0(),
        "acct_id,fiscal_id,group_id,owner_id": brick_format_00012_membership_v0_0_0(),
        "fiscal_id,label,mass,owner_id,parent_road,pledge": brick_format_00013_itemunit_v0_0_0(),
        "addin,begin,close,denom,fiscal_id,gogo_want,label,morph,numor,owner_id,parent_road,stop_want": brick_format_00019_itemunit_v0_0_0(),
        "acct_id,credit_vote,debtit_vote,fiscal_id,group_id,owner_id": brick_format_00020_bud_acct_membership_v0_0_0(),
        "acct_id,credit_belief,debtit_belief,fiscal_id,owner_id": brick_format_00021_bud_acctunit_v0_0_0(),
        "awardee_id,fiscal_id,give_force,owner_id,road,take_force": brick_format_00022_bud_item_awardlink_v0_0_0(),
        "base,fiscal_id,fnigh,fopen,owner_id,pick,road": brick_format_00023_bud_item_factunit_v0_0_0(),
        "fiscal_id,owner_id,road,team_id": brick_format_00024_bud_item_teamlink_v0_0_0(),
        "fiscal_id,healer_id,owner_id,road": brick_format_00025_bud_item_healerlink_v0_0_0(),
        "base,divisor,fiscal_id,need,nigh,open,owner_id,road": brick_format_00026_bud_item_reason_premiseunit_v0_0_0(),
        "base,base_item_active_requisite,fiscal_id,owner_id,road": brick_format_00027_bud_item_reasonunit_v0_0_0(),
        "addin,begin,close,denom,fiscal_id,gogo_want,label,mass,morph,numor,owner_id,parent_road,pledge,problem_bool,stop_want": brick_format_00028_bud_itemunit_v0_0_0(),
        "credor_respect,debtor_respect,fiscal_id,fund_coin,fund_pool,max_tree_traverse,owner_id,penny,purview_time_id,respect_bit,tally": brick_format_00029_budunit_v0_0_0(),
        "fiscal_id,healer_id,label,owner_id,parent_road,problem_bool": brick_format_00036_problem_healer_v0_0_0(),
        "inx_road_delimiter,inx_word,jaar_type,otx_road_delimiter,otx_word,unknown_word": brick_format_00040_bridge_otx2inx_v0_0_0(),
        "inx_label,inx_road_delimiter,otx_label,otx_road_delimiter,unknown_word": brick_format_00041_bridge_nub_label_v0_0_0(),
        "acct_id,fiscal_id,inx_word,jaar_type,otx_word,owner_id": brick_format_00113_acct_otx2inx_v0_0_0(),
    }


def get_brickref_from_file(brick_format_filename: str) -> dict:
    brickref_filename = get_json_filename(brick_format_filename)
    brickref_json = open_file(get_brick_formats_dir(), brickref_filename)
    return get_dict_from_json(brickref_json)


def get_quick_bricks_column_ref() -> dict[str, set[str]]:
    brick_number_dict = {}
    for brick_format_filename in get_brick_format_filenames():
        brickref_dict = get_brickref_from_file(brick_format_filename)
        brick_number = brickref_dict.get("brick_number")
        brick_number_dict[brick_number] = set(brickref_dict.get("attributes").keys())
    return brick_number_dict


def get_brick_elements_sort_order() -> list[str]:
    return [
        "face_id",
        "event_id",
        "fiscal_id",
        "jaar_type",
        "owner_id",
        "acct_id",
        "group_id",
        "parent_road",
        "label",
        "road",
        "base",
        "need",
        "pick",
        "team_id",
        "awardee_id",
        "healer_id",
        "time_id",
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "base_item_active_requisite",
        "credit_belief",
        "debtit_belief",
        "credit_vote",
        "debtit_vote",
        "credor_respect",
        "debtor_respect",
        "fopen",
        "fnigh",
        "fund_pool",
        "give_force",
        "mass",
        "max_tree_traverse",
        "nigh",
        "open",
        "divisor",
        "pledge",
        "problem_bool",
        "purview_time_id",
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
        "current_time",
        "amount",
        "month_label",
        "hour_label",
        "cumlative_minute",
        "cumlative_day",
        "weekday_label",
        "weekday_order",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
        "otx_label",
        "inx_label",
        "road_delimiter",
        "c400_number",
        "yr1_jan1_offset",
        "quota",
        "monthday_distortion",
        "timeline_label",
    ]


def get_brick_sqlite_type() -> dict[str, str]:
    return {
        "face_id": "TEXT",
        "event_id": "INTEGER",
        "fiscal_id": "TEXT",
        "jaar_type": "TEXT",
        "owner_id": "TEXT",
        "acct_id": "TEXT",
        "group_id": "TEXT",
        "parent_road": "TEXT",
        "label": "TEXT",
        "road": "TEXT",
        "base": "TEXT",
        "need": "TEXT",
        "pick": "TEXT",
        "team_id": "TEXT",
        "awardee_id": "TEXT",
        "healer_id": "TEXT",
        "time_id": "INTEGER",
        "begin": "REAL",
        "close": "REAL",
        "addin": "REAL",
        "numor": "REAL",
        "denom": "REAL",
        "morph": "INTEGER",
        "gogo_want": "REAL",
        "stop_want": "REAL",
        "base_item_active_requisite": "TEXT",
        "credit_belief": "REAL",
        "debtit_belief": "REAL",
        "credit_vote": "REAL",
        "debtit_vote": "REAL",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fopen": "REAL",
        "fnigh": "REAL",
        "fund_pool": "REAL",
        "give_force": "REAL",
        "mass": "REAL",
        "max_tree_traverse": "INTEGER",
        "nigh": "REAL",
        "open": "REAL",
        "divisor": "REAL",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "purview_time_id": "INTEGER",
        "take_force": "REAL",
        "tally": "REAL",
        "fund_coin": "REAL",
        "penny": "REAL",
        "respect_bit": "REAL",
        "current_time": "INTEGER",
        "amount": "REAL",
        "month_label": "TEXT",
        "hour_label": "TEXT",
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_label": "TEXT",
        "weekday_order": "INTEGER",
        "otx_road_delimiter": "TEXT",
        "inx_road_delimiter": "TEXT",
        "unknown_word": "TEXT",
        "otx_word": "TEXT",
        "inx_word": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "road_delimiter": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "monthday_distortion": "INTEGER",
        "timeline_label": "TEXT",
    }


def get_brick_category_ref() -> dict[str, set[str]]:
    return {
        "fiscalunit": ["br00000"],
        "fiscal_purview_episode": ["br00001"],
        "fiscal_cashbook": ["br00002"],
        "fiscal_timeline_hour": ["br00003"],
        "fiscal_timeline_month": ["br00004"],
        "fiscal_timeline_weekday": ["br00005"],
        "bud_acctunit": ["br00011", "br00021", "br00113"],
        "bud_acct_membership": ["br00012", "br00020"],
        "bud_itemunit": ["br00013", "br00019", "br00028", "br00036"],
        "bud_item_awardlink": ["br00022"],
        "bud_item_factunit": ["br00023"],
        "bud_item_teamlink": ["br00024"],
        "bud_item_healerlink": ["br00025", "br00036"],
        "bud_item_reason_premiseunit": ["br00026"],
        "bud_item_reasonunit": ["br00027"],
        "budunit": ["br00029"],
        "bridge_otx2inx": ["br00040", "br00113"],
        "bridge_nub_label": ["br00041"],
    }
