from src.f00_instrument.file import open_file
from src.f00_instrument.dict_tool import get_dict_from_json
from src.f01_road.jaar_config import get_json_filename
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


def time_id_str() -> str:
    return "time_id"


def brick_number_str() -> str:
    return "brick_number"


def allowed_crud_str() -> str:
    return "allowed_crud"


def column_order_str() -> str:
    return "column_order"


def sort_order_str() -> str:
    return "sort_order"


def categorys_str() -> str:
    return "categorys"


def attributes_str() -> str:
    return "attributes"


def must_be_roadnode_str() -> str:
    return "must_be_RoadNode"


def must_be_roadunit_str() -> str:
    return "must_be_RoadUnit"


def must_be_str() -> str:
    return "must_be_str"


def must_be_number_str() -> str:
    return "must_be_number"


def must_be_bool_str() -> str:
    return "must_be_bool"


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


def brick_format_00040_bridge_otx_to_inx_v0_0_0() -> str:
    return "brick_format_00040_bridge_otx_to_inx_v0_0_0"


def brick_format_00041_bridge_explicit_label_v0_0_0() -> str:
    return "brick_format_00041_bridge_explicit_label_v0_0_0"


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
        brick_format_00040_bridge_otx_to_inx_v0_0_0(),
        brick_format_00041_bridge_explicit_label_v0_0_0(),
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
    }


def get_brick_format_headers() -> dict[str, list[str]]:
    return {
        "c400_config,current_time,fiscal_id,fund_coin,monthday_distortion,penny,respect_bit,road_delimiter,timeline_label,yr1_jan1_offset": brick_format_00000_fiscalunit_v0_0_0(),
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
        "inx_road_delimiter,inx_word,otx_road_delimiter,otx_word,unknown_word": brick_format_00040_bridge_otx_to_inx_v0_0_0(),
        "inx_label,inx_road_delimiter,otx_label,otx_road_delimiter,unknown_word": brick_format_00041_bridge_explicit_label_v0_0_0(),
    }


def get_brickref_dict(brick_name) -> dict:
    brickref_filename = get_json_filename(brick_name)
    brickref_json = open_file(get_brick_formats_dir(), brickref_filename)
    return get_dict_from_json(brickref_json)
