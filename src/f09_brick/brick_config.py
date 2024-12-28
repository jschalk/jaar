from src.f00_instrument.file import open_file, create_path
from src.f00_instrument.dict_toolbox import get_dict_from_json
from src.f01_road.jaar_config import get_json_filename
from src.f02_bud.bud_tool import budunit_str
from src.f07_deal.deal_config import dealunit_str
from src.f08_pidgin.pidgin_config import pidginunit_str
from src.f09_brick.examples.brick_env import src_brick_dir
from os import getcwd as os_getcwd


def get_brick_config_file_name() -> str:
    return "brick_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "f09_brick")


def get_brick_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_brick_config_file_name())
    )


def brick_number_str() -> str:
    return "brick_number"


def brick_type_str() -> str:
    return "brick_type"


def get_brick_types() -> set[str]:
    return {budunit_str(), dealunit_str(), pidginunit_str()}


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
    return create_path(src_brick_dir(), "brick_formats")


# def brick_format_00000_dealunit_v0_0_0()->str: return "brick_format_00000_dealunit_v0_0_0"
# def brick_format_00001_deal_purview_episode_v0_0_0()->str: return "brick_format_00001_deal_purview_episode_v0_0_0"
# def brick_format_00002_deal_cashbook_v0_0_0()->str: return "brick_format_00002_deal_cashbook_v0_0_0"
# def brick_format_00003_deal_timeline_hour_v0_0_0()->str: return "brick_format_00003_deal_timeline_hour_v0_0_0"
# def brick_format_00004_deal_timeline_month_v0_0_0()->str: return "brick_format_00004_deal_timeline_month_v0_0_0"
# def brick_format_00005_deal_timeline_weekday_v0_0_0()->str: return "brick_format_00005_deal_timeline_weekday_v0_0_0"


def brick_format_00000_dealunit_v0_0_0() -> str:
    return "brick_format_00000_dealunit_v0_0_0"


def brick_format_00001_deal_purview_episode_v0_0_0() -> str:
    return "brick_format_00001_deal_purview_episode_v0_0_0"


def brick_format_00002_deal_cashbook_v0_0_0() -> str:
    return "brick_format_00002_deal_cashbook_v0_0_0"


def brick_format_00003_deal_timeline_hour_v0_0_0() -> str:
    return "brick_format_00003_deal_timeline_hour_v0_0_0"


def brick_format_00004_deal_timeline_month_v0_0_0() -> str:
    return "brick_format_00004_deal_timeline_month_v0_0_0"


def brick_format_00005_deal_timeline_weekday_v0_0_0() -> str:
    return "brick_format_00005_deal_timeline_weekday_v0_0_0"


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


def brick_format_00040_map_otx2inx_v0_0_0() -> str:
    return "brick_format_00040_map_otx2inx_v0_0_0"


def brick_format_00042_map_group_id_v0_0_0() -> str:
    return "brick_format_00042_map_group_id_v0_0_0"


def brick_format_00043_map_acct_name_v0_0_0() -> str:
    return "brick_format_00043_map_acct_name_v0_0_0"


def brick_format_00044_map_idea_v0_0_0() -> str:
    return "brick_format_00044_map_idea_v0_0_0"


def brick_format_00045_map_road_v0_0_0() -> str:
    return "brick_format_00045_map_road_v0_0_0"


def brick_format_00113_acct_map1_v0_0_0() -> str:
    return "brick_format_00113_acct_map1_v0_0_0"


def brick_format_00115_group_map1_v0_0_0() -> str:
    return "brick_format_00115_group_map1_v0_0_0"


def brick_format_00116_idea_map1_v0_0_0() -> str:
    return "brick_format_00116_idea_map1_v0_0_0"


def brick_format_00117_road_map1_v0_0_0() -> str:
    return "brick_format_00117_road_map1_v0_0_0"


def get_brick_format_filenames() -> set[str]:
    return {
        brick_format_00000_dealunit_v0_0_0(),
        brick_format_00001_deal_purview_episode_v0_0_0(),
        brick_format_00002_deal_cashbook_v0_0_0(),
        brick_format_00003_deal_timeline_hour_v0_0_0(),
        brick_format_00004_deal_timeline_month_v0_0_0(),
        brick_format_00005_deal_timeline_weekday_v0_0_0(),
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
        brick_format_00042_map_group_id_v0_0_0(),
        brick_format_00043_map_acct_name_v0_0_0(),
        brick_format_00044_map_idea_v0_0_0(),
        brick_format_00045_map_road_v0_0_0(),
        brick_format_00113_acct_map1_v0_0_0(),
        brick_format_00115_group_map1_v0_0_0(),
        brick_format_00116_idea_map1_v0_0_0(),
        brick_format_00117_road_map1_v0_0_0(),
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
        "br00042",
        "br00043",
        "br00044",
        "br00045",
        "br00113",
        "br00115",
        "br00116",
        "br00117",
    }


def get_brick_format_filename(brick_number: str) -> str:
    brick_number_substring = brick_number[2:]
    for brick_format_filename in get_brick_format_filenames():
        if brick_format_filename[13:18] == brick_number_substring:
            return brick_format_filename


def get_brick_format_headers() -> dict[str, list[str]]:
    return {
        "bridge,c400_number,current_time,deal_id,fund_coin,monthday_distortion,penny,respect_bit,timeline_idea,yr1_jan1_offset": brick_format_00000_dealunit_v0_0_0(),
        "acct_name,deal_id,owner_name,quota,time_int": brick_format_00001_deal_purview_episode_v0_0_0(),
        "acct_name,amount,deal_id,owner_name,time_int": brick_format_00002_deal_cashbook_v0_0_0(),
        "cumlative_minute,deal_id,hour_idea": brick_format_00003_deal_timeline_hour_v0_0_0(),
        "cumlative_day,deal_id,month_idea": brick_format_00004_deal_timeline_month_v0_0_0(),
        "deal_id,weekday_idea,weekday_order": brick_format_00005_deal_timeline_weekday_v0_0_0(),
        "acct_name,deal_id,owner_name": brick_format_00011_acct_v0_0_0(),
        "acct_name,deal_id,group_id,owner_name": brick_format_00012_membership_v0_0_0(),
        "deal_id,lx,mass,owner_name,parent_road,pledge": brick_format_00013_itemunit_v0_0_0(),
        "addin,begin,close,deal_id,denom,gogo_want,lx,morph,numor,owner_name,parent_road,stop_want": brick_format_00019_itemunit_v0_0_0(),
        "acct_name,credit_vote,deal_id,debtit_vote,group_id,owner_name": brick_format_00020_bud_acct_membership_v0_0_0(),
        "acct_name,credit_belief,deal_id,debtit_belief,owner_name": brick_format_00021_bud_acctunit_v0_0_0(),
        "awardee_id,deal_id,give_force,owner_name,road,take_force": brick_format_00022_bud_item_awardlink_v0_0_0(),
        "base,deal_id,fnigh,fopen,owner_name,pick,road": brick_format_00023_bud_item_factunit_v0_0_0(),
        "deal_id,owner_name,road,team_id": brick_format_00024_bud_item_teamlink_v0_0_0(),
        "deal_id,healer_name,owner_name,road": brick_format_00025_bud_item_healerlink_v0_0_0(),
        "base,deal_id,divisor,need,nigh,open,owner_name,road": brick_format_00026_bud_item_reason_premiseunit_v0_0_0(),
        "base,base_item_active_requisite,deal_id,owner_name,road": brick_format_00027_bud_item_reasonunit_v0_0_0(),
        "addin,begin,close,deal_id,denom,gogo_want,lx,mass,morph,numor,owner_name,parent_road,pledge,problem_bool,stop_want": brick_format_00028_bud_itemunit_v0_0_0(),
        "credor_respect,deal_id,debtor_respect,fund_coin,fund_pool,max_tree_traverse,owner_name,penny,purview_time_int,respect_bit,tally": brick_format_00029_budunit_v0_0_0(),
        "deal_id,healer_name,lx,owner_name,parent_road,problem_bool": brick_format_00036_problem_healer_v0_0_0(),
        "inx_bridge,inx_group_id,otx_bridge,otx_group_id,unknown_word": brick_format_00042_map_group_id_v0_0_0(),
        "inx_acct_name,inx_bridge,otx_acct_name,otx_bridge,unknown_word": brick_format_00043_map_acct_name_v0_0_0(),
        "inx_bridge,inx_idea,otx_bridge,otx_idea,unknown_word": brick_format_00044_map_idea_v0_0_0(),
        "inx_bridge,inx_road,otx_bridge,otx_road,unknown_word": brick_format_00045_map_road_v0_0_0(),
        "acct_name,deal_id,inx_acct_name,otx_acct_name,owner_name": brick_format_00113_acct_map1_v0_0_0(),
        "acct_name,deal_id,inx_group_id,otx_group_id,owner_name": brick_format_00115_group_map1_v0_0_0(),
        "acct_name,deal_id,inx_idea,otx_idea,owner_name": brick_format_00116_idea_map1_v0_0_0(),
        "acct_name,deal_id,inx_road,otx_road,owner_name": brick_format_00117_road_map1_v0_0_0(),
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
        "face_name",
        "event_int",
        "deal_id",
        "owner_name",
        "acct_name",
        "group_id",
        "parent_road",
        "lx",
        "road",
        "base",
        "need",
        "pick",
        "team_id",
        "awardee_id",
        "healer_name",
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
        "purview_time_int",
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
        "current_time",
        "amount",
        "month_idea",
        "hour_idea",
        "cumlative_minute",
        "cumlative_day",
        "weekday_idea",
        "weekday_order",
        "otx_idea",
        "inx_idea",
        "otx_road",
        "inx_road",
        "otx_acct_name",
        "inx_acct_name",
        "otx_group_id",
        "inx_group_id",
        "otx_bridge",
        "inx_bridge",
        "bridge",
        "unknown_word",
        "c400_number",
        "yr1_jan1_offset",
        "quota",
        "monthday_distortion",
        "timeline_idea",
    ]


def get_brick_sqlite_type() -> dict[str, str]:
    return {
        "face_name": "TEXT",
        "event_int": "INTEGER",
        "deal_id": "TEXT",
        "owner_name": "TEXT",
        "acct_name": "TEXT",
        "group_id": "TEXT",
        "parent_road": "TEXT",
        "lx": "TEXT",
        "road": "TEXT",
        "base": "TEXT",
        "need": "TEXT",
        "pick": "TEXT",
        "team_id": "TEXT",
        "awardee_id": "TEXT",
        "healer_name": "TEXT",
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
        "purview_time_int": "INTEGER",
        "take_force": "REAL",
        "tally": "REAL",
        "fund_coin": "REAL",
        "penny": "REAL",
        "respect_bit": "REAL",
        "current_time": "INTEGER",
        "amount": "REAL",
        "month_idea": "TEXT",
        "hour_idea": "TEXT",
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_idea": "TEXT",
        "weekday_order": "INTEGER",
        "otx_bridge": "TEXT",
        "inx_bridge": "TEXT",
        "unknown_word": "TEXT",
        "otx_idea": "TEXT",
        "inx_idea": "TEXT",
        "otx_road": "TEXT",
        "inx_road": "TEXT",
        "otx_acct_name": "TEXT",
        "inx_acct_name": "TEXT",
        "otx_group_id": "TEXT",
        "inx_group_id": "TEXT",
        "bridge": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "monthday_distortion": "INTEGER",
        "timeline_idea": "TEXT",
    }


def get_brick_category_ref() -> dict[str, set[str]]:
    return {
        "dealunit": ["br00000"],
        "deal_purview_episode": ["br00001"],
        "deal_cashbook": ["br00002"],
        "deal_timeline_hour": ["br00003"],
        "deal_timeline_month": ["br00004"],
        "deal_timeline_weekday": ["br00005"],
        "bud_acctunit": [
            "br00011",
            "br00021",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        ],
        "bud_acct_membership": ["br00012", "br00020"],
        "bud_itemunit": ["br00013", "br00019", "br00028", "br00036"],
        "bud_item_awardlink": ["br00022"],
        "bud_item_factunit": ["br00023"],
        "bud_item_teamlink": ["br00024"],
        "bud_item_healerlink": ["br00025", "br00036"],
        "bud_item_reason_premiseunit": ["br00026"],
        "bud_item_reasonunit": ["br00027"],
        "budunit": ["br00029"],
        "map_group_id": ["br00042", "br00115"],
        "map_acct_name": ["br00043", "br00113"],
        "map_idea": ["br00044", "br00116"],
        "map_road": ["br00045", "br00117"],
    }
