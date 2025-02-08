from src.f00_instrument.file import open_file, create_path
from src.f00_instrument.dict_toolbox import get_dict_from_json
from src.f01_road.jaar_config import get_json_filename
from src.f02_bud.bud_tool import budunit_str
from src.f07_fiscal.fiscal_config import fiscalunit_str
from src.f08_pidgin.pidgin_config import pidginunit_str
from src.f09_idea.examples.idea_env import src_idea_dir
from os import getcwd as os_getcwd


def get_idea_config_filename() -> str:
    return "idea_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f09_idea")


def get_idea_config_dict() -> dict:
    return get_dict_from_json(open_file(config_file_dir(), get_idea_config_filename()))


def idea_number_str() -> str:
    return "idea_number"


def idea_category_str() -> str:
    return "idea_category"


def get_idea_categorys() -> set[str]:
    return {"bud", "fiscal", "pidgin"}


def allowed_crud_str() -> str:
    return "allowed_crud"


def dimens_str() -> str:
    return "dimens"


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


def get_idea_formats_dir() -> str:
    idea_dir = create_path("src", "f09_idea")
    return create_path(idea_dir, "idea_formats")


def get_idea_elements_sort_order() -> list[str]:
    return [
        "idea_number",
        "face_name",
        "event_int",
        "fiscal_title",
        "owner_name",
        "owner_name_ERASE",
        "acct_name",
        "acct_name_ERASE",
        "group_label",
        "group_label_ERASE",
        "parent_road",
        "parent_road_ERASE",
        "item_title",
        "item_title_ERASE",
        "road",
        "road_ERASE",
        "base",
        "base_ERASE",
        "base_EXCISE",
        "need",
        "need_ERASE",
        "pick",
        "team_tag",
        "team_tag_ERASE",
        "awardee_tag",
        "awardee_tag_ERASE",
        "healer_name",
        "healer_name_ERASE",
        "time_int",
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
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
        "present_time",
        "amount",
        "month_title",
        "hour_title",
        "cumlative_minute",
        "cumlative_day",
        "weekday_title",
        "weekday_order",
        "otx_title",
        "inx_title",
        "otx_road",
        "inx_road",
        "otx_name",
        "inx_name",
        "otx_label",
        "inx_label",
        "otx_bridge",
        "inx_bridge",
        "bridge",
        "unknown_word",
        "c400_number",
        "yr1_jan1_offset",
        "quota",
        "ledger_depth",
        "monthday_distortion",
        "timeline_title",
        "error_message",
    ]


def get_custom_sorted_list(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_idea_elements_sort_order()
    sort_columns_in_existing = set(sorting_columns).intersection(existing_columns)
    return [
        sort_col for sort_col in sorting_columns if sort_col in sort_columns_in_existing
    ]


def get_idea_sqlite_types() -> dict[str, str]:
    return {
        "idea_number": "TEXT",
        "face_name": "TEXT",
        "event_int": "INTEGER",
        "fiscal_title": "TEXT",
        "owner_name": "TEXT",
        "owner_name_ERASE": "TEXT",
        "acct_name": "TEXT",
        "acct_name_ERASE": "TEXT",
        "group_label": "TEXT",
        "group_label_ERASE": "TEXT",
        "parent_road": "TEXT",
        "parent_road_ERASE": "TEXT",
        "item_title": "TEXT",
        "item_title_ERASE": "TEXT",
        "road": "TEXT",
        "road_ERASE": "TEXT",
        "base": "TEXT",
        "base_ERASE": "TEXT",
        "base_EXCISE": "TEXT",
        "need": "TEXT",
        "need_ERASE": "TEXT",
        "pick": "TEXT",
        "team_tag": "TEXT",
        "team_tag_ERASE": "TEXT",
        "awardee_tag": "TEXT",
        "awardee_tag_ERASE": "TEXT",
        "healer_name": "TEXT",
        "healer_name_ERASE": "TEXT",
        "time_int": "INTEGER",
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
        "take_force": "REAL",
        "tally": "REAL",
        "fund_coin": "REAL",
        "penny": "REAL",
        "respect_bit": "REAL",
        "present_time": "INTEGER",
        "amount": "REAL",
        "month_title": "TEXT",
        "hour_title": "TEXT",
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_title": "TEXT",
        "weekday_order": "INTEGER",
        "otx_bridge": "TEXT",
        "inx_bridge": "TEXT",
        "unknown_word": "TEXT",
        "otx_title": "TEXT",
        "inx_title": "TEXT",
        "otx_road": "TEXT",
        "inx_road": "TEXT",
        "otx_name": "TEXT",
        "inx_name": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "bridge": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "ledger_depth": "INT",
        "monthday_distortion": "INTEGER",
        "timeline_title": "TEXT",
        "error_message": "TEXT",
    }


# def idea_format_00000_fiscalunit_v0_0_0()->str: return "idea_format_00000_fiscalunit_v0_0_0"
# def idea_format_00001_fiscal_deal_episode_v0_0_0()->str: return "idea_format_00001_fiscal_deal_episode_v0_0_0"
# def idea_format_00002_fiscal_cashbook_v0_0_0()->str: return "idea_format_00002_fiscal_cashbook_v0_0_0"
# def idea_format_00003_fiscal_timeline_hour_v0_0_0()->str: return "idea_format_00003_fiscal_timeline_hour_v0_0_0"
# def idea_format_00004_fiscal_timeline_month_v0_0_0()->str: return "idea_format_00004_fiscal_timeline_month_v0_0_0"
# def idea_format_00005_fiscal_timeline_weekday_v0_0_0()->str: return "idea_format_00005_fiscal_timeline_weekday_v0_0_0"


def idea_format_00000_fiscalunit_v0_0_0() -> str:
    return "idea_format_00000_fiscalunit_v0_0_0"


def idea_format_00001_fiscal_deal_episode_v0_0_0() -> str:
    return "idea_format_00001_fiscal_deal_episode_v0_0_0"


def idea_format_00002_fiscal_cashbook_v0_0_0() -> str:
    return "idea_format_00002_fiscal_cashbook_v0_0_0"


def idea_format_00003_fiscal_timeline_hour_v0_0_0() -> str:
    return "idea_format_00003_fiscal_timeline_hour_v0_0_0"


def idea_format_00004_fiscal_timeline_month_v0_0_0() -> str:
    return "idea_format_00004_fiscal_timeline_month_v0_0_0"


def idea_format_00005_fiscal_timeline_weekday_v0_0_0() -> str:
    return "idea_format_00005_fiscal_timeline_weekday_v0_0_0"


def idea_format_00011_acct_v0_0_0() -> str:
    return "idea_format_00011_acct_v0_0_0"


def idea_format_00012_membership_v0_0_0() -> str:
    return "idea_format_00012_membership_v0_0_0"


def idea_format_00013_itemunit_v0_0_0() -> str:
    return "idea_format_00013_itemunit_v0_0_0"


def idea_format_00019_itemunit_v0_0_0() -> str:
    return "idea_format_00019_itemunit_v0_0_0"


# def idea_format_00020_bud_acct_membership_v0_0_0()-> str: return "idea_format_00020_bud_acct_membership_v0_0_0"
# def idea_format_00021_bud_acctunit_v0_0_0()-> str: return "idea_format_00021_bud_acctunit_v0_0_0"
# def idea_format_00022_bud_item_awardlink_v0_0_0()-> str: return "idea_format_00022_bud_item_awardlink_v0_0_0"
# def idea_format_00023_bud_item_factunit_v0_0_0()-> str: return "idea_format_00023_bud_item_factunit_v0_0_0"
# def idea_format_00024_bud_item_teamlink_v0_0_0()-> str: return "idea_format_00024_bud_item_teamlink_v0_0_0"
# def idea_format_00025_bud_item_healerlink_v0_0_0()-> str: return "idea_format_00025_bud_item_healerlink_v0_0_0"
# def idea_format_00026_bud_item_reason_premiseunit_v0_0_0()-> str: return "idea_format_00026_bud_item_reason_premiseunit_v0_0_0"
# def idea_format_00027_bud_item_reasonunit_v0_0_0()-> str: return "idea_format_00027_bud_item_reasonunit_v0_0_0"
# def idea_format_00028_bud_itemunit_v0_0_0()-> str: return "idea_format_00028_bud_itemunit_v0_0_0"
# def idea_format_00029_budunit_v0_0_0()-> str: return "idea_format_00029_budunit_v0_0_0"


def idea_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00020_bud_acct_membership_v0_0_0"


def idea_format_00021_bud_acctunit_v0_0_0() -> str:
    return "idea_format_00021_bud_acctunit_v0_0_0"


def idea_format_00022_bud_item_awardlink_v0_0_0() -> str:
    return "idea_format_00022_bud_item_awardlink_v0_0_0"


def idea_format_00023_bud_item_factunit_v0_0_0() -> str:
    return "idea_format_00023_bud_item_factunit_v0_0_0"


def idea_format_00024_bud_item_teamlink_v0_0_0() -> str:
    return "idea_format_00024_bud_item_teamlink_v0_0_0"


def idea_format_00025_bud_item_healerlink_v0_0_0() -> str:
    return "idea_format_00025_bud_item_healerlink_v0_0_0"


def idea_format_00026_bud_item_reason_premiseunit_v0_0_0() -> str:
    return "idea_format_00026_bud_item_reason_premiseunit_v0_0_0"


def idea_format_00027_bud_item_reasonunit_v0_0_0() -> str:
    return "idea_format_00027_bud_item_reasonunit_v0_0_0"


def idea_format_00028_bud_itemunit_v0_0_0() -> str:
    return "idea_format_00028_bud_itemunit_v0_0_0"


def idea_format_00029_budunit_v0_0_0() -> str:
    return "idea_format_00029_budunit_v0_0_0"


def idea_format_00036_problem_healer_v0_0_0() -> str:
    return "idea_format_00036_problem_healer_v0_0_0"


def idea_format_00040_map_otx2inx_v0_0_0() -> str:
    return "idea_format_00040_map_otx2inx_v0_0_0"


def idea_format_00042_map_label_v0_0_0() -> str:
    return "idea_format_00042_map_label_v0_0_0"


def idea_format_00043_map_name_v0_0_0() -> str:
    return "idea_format_00043_map_name_v0_0_0"


def idea_format_00044_map_title_v0_0_0() -> str:
    return "idea_format_00044_map_title_v0_0_0"


def idea_format_00045_map_road_v0_0_0() -> str:
    return "idea_format_00045_map_road_v0_0_0"


def idea_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_bud_acct_membership_v0_0_0"


def idea_format_00051_delete_bud_acctunit_v0_0_0() -> str:
    return "idea_format_00051_delete_bud_acctunit_v0_0_0"


def idea_format_00052_delete_bud_item_awardlink_v0_0_0() -> str:
    return "idea_format_00052_delete_bud_item_awardlink_v0_0_0"


def idea_format_00053_delete_bud_item_factunit_v0_0_0() -> str:
    return "idea_format_00053_delete_bud_item_factunit_v0_0_0"


def idea_format_00054_delete_bud_item_teamlink_v0_0_0() -> str:
    return "idea_format_00054_delete_bud_item_teamlink_v0_0_0"


def idea_format_00055_delete_bud_item_healerlink_v0_0_0() -> str:
    return "idea_format_00055_delete_bud_item_healerlink_v0_0_0"


def idea_format_00056_delete_bud_item_reason_premiseunit_v0_0_0() -> str:
    return "idea_format_00056_delete_bud_item_reason_premiseunit_v0_0_0"


def idea_format_00057_delete_bud_item_reasonunit_v0_0_0() -> str:
    return "idea_format_00057_delete_bud_item_reasonunit_v0_0_0"


def idea_format_00058_delete_bud_itemunit_v0_0_0() -> str:
    return "idea_format_00058_delete_bud_itemunit_v0_0_0"


def idea_format_00059_delete_budunit_v0_0_0() -> str:
    return "idea_format_00059_delete_budunit_v0_0_0"


def idea_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_bud_acct_membership_v0_0_0"


def idea_format_00113_acct_map1_v0_0_0() -> str:
    return "idea_format_00113_acct_map1_v0_0_0"


def idea_format_00115_group_map1_v0_0_0() -> str:
    return "idea_format_00115_group_map1_v0_0_0"


def idea_format_00116_title_map1_v0_0_0() -> str:
    return "idea_format_00116_title_map1_v0_0_0"


def idea_format_00117_road_map1_v0_0_0() -> str:
    return "idea_format_00117_road_map1_v0_0_0"


def get_idea_format_filenames() -> set[str]:
    return {
        idea_format_00000_fiscalunit_v0_0_0(),
        idea_format_00001_fiscal_deal_episode_v0_0_0(),
        idea_format_00002_fiscal_cashbook_v0_0_0(),
        idea_format_00003_fiscal_timeline_hour_v0_0_0(),
        idea_format_00004_fiscal_timeline_month_v0_0_0(),
        idea_format_00005_fiscal_timeline_weekday_v0_0_0(),
        idea_format_00011_acct_v0_0_0(),
        idea_format_00012_membership_v0_0_0(),
        idea_format_00013_itemunit_v0_0_0(),
        idea_format_00019_itemunit_v0_0_0(),
        idea_format_00020_bud_acct_membership_v0_0_0(),
        idea_format_00021_bud_acctunit_v0_0_0(),
        idea_format_00022_bud_item_awardlink_v0_0_0(),
        idea_format_00023_bud_item_factunit_v0_0_0(),
        idea_format_00024_bud_item_teamlink_v0_0_0(),
        idea_format_00025_bud_item_healerlink_v0_0_0(),
        idea_format_00026_bud_item_reason_premiseunit_v0_0_0(),
        idea_format_00027_bud_item_reasonunit_v0_0_0(),
        idea_format_00028_bud_itemunit_v0_0_0(),
        idea_format_00029_budunit_v0_0_0(),
        idea_format_00036_problem_healer_v0_0_0(),
        idea_format_00042_map_label_v0_0_0(),
        idea_format_00043_map_name_v0_0_0(),
        idea_format_00044_map_title_v0_0_0(),
        idea_format_00045_map_road_v0_0_0(),
        idea_format_00050_delete_bud_acct_membership_v0_0_0(),
        idea_format_00051_delete_bud_acctunit_v0_0_0(),
        idea_format_00052_delete_bud_item_awardlink_v0_0_0(),
        idea_format_00053_delete_bud_item_factunit_v0_0_0(),
        idea_format_00054_delete_bud_item_teamlink_v0_0_0(),
        idea_format_00055_delete_bud_item_healerlink_v0_0_0(),
        idea_format_00056_delete_bud_item_reason_premiseunit_v0_0_0(),
        idea_format_00057_delete_bud_item_reasonunit_v0_0_0(),
        idea_format_00058_delete_bud_itemunit_v0_0_0(),
        idea_format_00059_delete_budunit_v0_0_0(),
        idea_format_00113_acct_map1_v0_0_0(),
        idea_format_00115_group_map1_v0_0_0(),
        idea_format_00116_title_map1_v0_0_0(),
        idea_format_00117_road_map1_v0_0_0(),
    }


def get_idea_numbers() -> set[str]:
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
        "br00042",
        "br00043",
        "br00044",
        "br00045",
        "br00050",
        "br00051",
        "br00052",
        "br00053",
        "br00054",
        "br00055",
        "br00056",
        "br00057",
        "br00058",
        "br00059",
        "br00113",
        "br00115",
        "br00116",
        "br00117",
    }


def get_idea_format_filename(idea_number: str) -> str:
    idea_number_substring = idea_number[2:]
    for idea_format_filename in get_idea_format_filenames():
        if idea_format_filename[12:17] == idea_number_substring:
            return idea_format_filename


def get_idea_format_headers() -> dict[str, list[str]]:
    return {
        "fiscal_title,fund_coin,penny,respect_bit,present_time,bridge,c400_number,yr1_jan1_offset,monthday_distortion,timeline_title": idea_format_00000_fiscalunit_v0_0_0(),
        "fiscal_title,owner_name,time_int,quota,ledger_depth": idea_format_00001_fiscal_deal_episode_v0_0_0(),
        "fiscal_title,owner_name,acct_name,time_int,amount": idea_format_00002_fiscal_cashbook_v0_0_0(),
        "fiscal_title,hour_title,cumlative_minute": idea_format_00003_fiscal_timeline_hour_v0_0_0(),
        "fiscal_title,month_title,cumlative_day": idea_format_00004_fiscal_timeline_month_v0_0_0(),
        "fiscal_title,weekday_title,weekday_order": idea_format_00005_fiscal_timeline_weekday_v0_0_0(),
        "fiscal_title,owner_name,acct_name": idea_format_00011_acct_v0_0_0(),
        "fiscal_title,owner_name,acct_name,group_label": idea_format_00012_membership_v0_0_0(),
        "fiscal_title,owner_name,parent_road,item_title,mass,pledge": idea_format_00013_itemunit_v0_0_0(),
        "fiscal_title,owner_name,parent_road,item_title,begin,close,addin,numor,denom,morph,gogo_want,stop_want": idea_format_00019_itemunit_v0_0_0(),
        "fiscal_title,owner_name,acct_name,group_label,credit_vote,debtit_vote": idea_format_00020_bud_acct_membership_v0_0_0(),
        "fiscal_title,owner_name,acct_name,credit_belief,debtit_belief": idea_format_00021_bud_acctunit_v0_0_0(),
        "fiscal_title,owner_name,road,awardee_tag,give_force,take_force": idea_format_00022_bud_item_awardlink_v0_0_0(),
        "fiscal_title,owner_name,road,base,pick,fopen,fnigh": idea_format_00023_bud_item_factunit_v0_0_0(),
        "fiscal_title,owner_name,road,team_tag": idea_format_00024_bud_item_teamlink_v0_0_0(),
        "fiscal_title,owner_name,road,healer_name": idea_format_00025_bud_item_healerlink_v0_0_0(),
        "fiscal_title,owner_name,road,base,need,nigh,open,divisor": idea_format_00026_bud_item_reason_premiseunit_v0_0_0(),
        "fiscal_title,owner_name,road,base,base_item_active_requisite": idea_format_00027_bud_item_reasonunit_v0_0_0(),
        "fiscal_title,owner_name,parent_road,item_title,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,pledge,problem_bool": idea_format_00028_bud_itemunit_v0_0_0(),
        "fiscal_title,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_coin,penny,respect_bit": idea_format_00029_budunit_v0_0_0(),
        "fiscal_title,owner_name,parent_road,item_title,healer_name,problem_bool": idea_format_00036_problem_healer_v0_0_0(),
        "otx_label,inx_label,otx_bridge,inx_bridge,unknown_word": idea_format_00042_map_label_v0_0_0(),
        "otx_name,inx_name,otx_bridge,inx_bridge,unknown_word": idea_format_00043_map_name_v0_0_0(),
        "otx_title,inx_title,otx_bridge,inx_bridge,unknown_word": idea_format_00044_map_title_v0_0_0(),
        "otx_road,inx_road,otx_bridge,inx_bridge,unknown_word": idea_format_00045_map_road_v0_0_0(),
        "fiscal_title,owner_name,acct_name,group_label_ERASE": idea_format_00050_delete_bud_acct_membership_v0_0_0(),
        "fiscal_title,owner_name,acct_name_ERASE": idea_format_00051_delete_bud_acctunit_v0_0_0(),
        "fiscal_title,owner_name,road,awardee_tag_ERASE": idea_format_00052_delete_bud_item_awardlink_v0_0_0(),
        "fiscal_title,owner_name,road,base_EXCISE": idea_format_00053_delete_bud_item_factunit_v0_0_0(),
        "fiscal_title,owner_name,road,team_tag_ERASE": idea_format_00054_delete_bud_item_teamlink_v0_0_0(),
        "fiscal_title,owner_name,road,healer_name_ERASE": idea_format_00055_delete_bud_item_healerlink_v0_0_0(),
        "fiscal_title,owner_name,road,base,need_ERASE": idea_format_00056_delete_bud_item_reason_premiseunit_v0_0_0(),
        "fiscal_title,owner_name,road,base_ERASE": idea_format_00057_delete_bud_item_reasonunit_v0_0_0(),
        "fiscal_title,owner_name,parent_road,item_title_ERASE": idea_format_00058_delete_bud_itemunit_v0_0_0(),
        "fiscal_title,owner_name_ERASE": idea_format_00059_delete_budunit_v0_0_0(),
        "fiscal_title,owner_name,acct_name,otx_name,inx_name": idea_format_00113_acct_map1_v0_0_0(),
        "fiscal_title,owner_name,acct_name,otx_label,inx_label": idea_format_00115_group_map1_v0_0_0(),
        "fiscal_title,owner_name,acct_name,otx_title,inx_title": idea_format_00116_title_map1_v0_0_0(),
        "fiscal_title,owner_name,acct_name,otx_road,inx_road": idea_format_00117_road_map1_v0_0_0(),
    }


def get_idearef_from_file(idea_format_filename: str) -> dict:
    idearef_filename = get_json_filename(idea_format_filename)
    idearef_json = open_file(get_idea_formats_dir(), idearef_filename)
    return get_dict_from_json(idearef_json)


def get_quick_ideas_column_ref() -> dict[str, set[str]]:
    idea_number_dict = {}
    for idea_format_filename in get_idea_format_filenames():
        idearef_dict = get_idearef_from_file(idea_format_filename)
        idea_number = idearef_dict.get("idea_number")
        idea_number_dict[idea_number] = set(idearef_dict.get("attributes").keys())
    return idea_number_dict


def get_idea_dimen_ref() -> dict[str, set[str]]:
    # return {
    #     "fiscalunit": ["br00000"],
    #     "fiscal_deal_episode": ["br00001"],
    #     "fiscal_cashbook": ["br00002"],
    #     "fiscal_timeline_hour": ["br00003"],
    #     "fiscal_timeline_month": ["br00004"],
    #     "fiscal_timeline_weekday": ["br00005"],
    #     "bud_acctunit": [
    #         "br00011",
    #         "br00021",
    #         "br00113",
    #         "br00115",
    #         "br00116",
    #         "br00117",
    #     ],
    #     "bud_acct_membership": ["br00012", "br00020", "br00050"],
    #     "bud_itemunit": ["br00013", "br00019", "br00028", "br00036"],
    #     "bud_item_awardlink": ["br00022"],
    #     "bud_item_factunit": ["br00023"],
    #     "bud_item_teamlink": ["br00024"],
    #     "bud_item_healerlink": ["br00025", "br00036"],
    #     "bud_item_reason_premiseunit": ["br00026"],
    #     "bud_item_reasonunit": ["br00027"],
    #     "budunit": ["br00029"],
    #     "map_label": ["br00042", "br00115"],
    #     "map_name": ["br00043", "br00113"],
    #     "map_title": ["br00044", "br00116"],
    #     "map_road": ["br00045", "br00117"],
    # }
    return {
        "fiscalunit": ["br00000"],
        "fiscal_deal_episode": ["br00001"],
        "fiscal_cashbook": ["br00002"],
        "fiscal_timeline_hour": ["br00003"],
        "fiscal_timeline_month": ["br00004"],
        "fiscal_timeline_weekday": ["br00005"],
        "bud_acctunit": [
            "br00011",
            "br00021",
            "br00051",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        ],
        "bud_acct_membership": ["br00012", "br00020", "br00050"],
        "bud_itemunit": ["br00013", "br00019", "br00028", "br00036", "br00058"],
        "bud_item_awardlink": ["br00022", "br00052"],
        "bud_item_factunit": ["br00023", "br00053"],
        "bud_item_teamlink": ["br00024", "br00054"],
        "bud_item_healerlink": ["br00025", "br00036", "br00055"],
        "bud_item_reason_premiseunit": ["br00026", "br00056"],
        "bud_item_reasonunit": ["br00027", "br00057"],
        "budunit": ["br00029", "br00059"],
        "map_label": ["br00042", "br00115"],
        "map_name": ["br00043", "br00113"],
        "map_title": ["br00044", "br00116"],
        "map_road": ["br00045", "br00117"],
    }
