from src._instrument.file import open_file
from src._instrument.python_tool import get_dict_from_json
from src._road.jaar_config import get_json_filename
from src.stone.examples.stone_env import src_stone_dir


def column_order_str() -> str:
    return "column_order"


def sort_order_str() -> str:
    return "sort_order"


def atom_categorys_str() -> str:
    return "atom_categorys"


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


def get_stone_formats_dir() -> str:
    return f"{src_stone_dir()}/stone_formats"


def stone_format_00001_acct_v0_0_0() -> str:
    return "stone_format_00001_acct_v0_0_0"


def stone_format_00002_membership_v0_0_0() -> str:
    return "stone_format_00002_membership_v0_0_0"


def stone_format_00003_ideaunit_v0_0_0() -> str:
    return "stone_format_00003_ideaunit_v0_0_0"


def stone_format_00019_ideaunit_v0_0_0() -> str:
    return "stone_format_00019_ideaunit_v0_0_0"


def stone_format_00036_problem_healer_v0_0_0() -> str:
    return "stone_format_00036_problem_healer_v0_0_0"


# def stone_format_00020_bud_acct_membership_v0_0_0()-> str: return "stone_format_00020_bud_acct_membership_v0_0_0"
# def stone_format_00021_bud_acctunit_v0_0_0()-> str: return "stone_format_00021_bud_acctunit_v0_0_0"
# def stone_format_00022_bud_idea_awardlink_v0_0_0()-> str: return "stone_format_00022_bud_idea_awardlink_v0_0_0"
# def stone_format_00023_bud_idea_factunit_v0_0_0()-> str: return "stone_format_00023_bud_idea_factunit_v0_0_0"
# def stone_format_00024_bud_idea_teamlink_v0_0_0()-> str: return "stone_format_00024_bud_idea_teamlink_v0_0_0"
# def stone_format_00025_bud_idea_healerhold_v0_0_0()-> str: return "stone_format_00025_bud_idea_healerhold_v0_0_0"
# def stone_format_00026_bud_idea_reason_premiseunit_v0_0_0()-> str: return "stone_format_00026_bud_idea_reason_premiseunit_v0_0_0"
# def stone_format_00027_bud_idea_reasonunit_v0_0_0()-> str: return "stone_format_00027_bud_idea_reasonunit_v0_0_0"
# def stone_format_00028_bud_ideaunit_v0_0_0()-> str: return "stone_format_00028_bud_ideaunit_v0_0_0"
# def stone_format_00029_budunit_v0_0_0()-> str: return "stone_format_00029_budunit_v0_0_0"
def stone_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "stone_format_00020_bud_acct_membership_v0_0_0"


def stone_format_00021_bud_acctunit_v0_0_0() -> str:
    return "stone_format_00021_bud_acctunit_v0_0_0"


def stone_format_00022_bud_idea_awardlink_v0_0_0() -> str:
    return "stone_format_00022_bud_idea_awardlink_v0_0_0"


def stone_format_00023_bud_idea_factunit_v0_0_0() -> str:
    return "stone_format_00023_bud_idea_factunit_v0_0_0"


def stone_format_00024_bud_idea_teamlink_v0_0_0() -> str:
    return "stone_format_00024_bud_idea_teamlink_v0_0_0"


def stone_format_00025_bud_idea_healerhold_v0_0_0() -> str:
    return "stone_format_00025_bud_idea_healerhold_v0_0_0"


def stone_format_00026_bud_idea_reason_premiseunit_v0_0_0() -> str:
    return "stone_format_00026_bud_idea_reason_premiseunit_v0_0_0"


def stone_format_00027_bud_idea_reasonunit_v0_0_0() -> str:
    return "stone_format_00027_bud_idea_reasonunit_v0_0_0"


def stone_format_00028_bud_ideaunit_v0_0_0() -> str:
    return "stone_format_00028_bud_ideaunit_v0_0_0"


def stone_format_00029_budunit_v0_0_0() -> str:
    return "stone_format_00029_budunit_v0_0_0"


def get_stone_filenames() -> set[str]:
    return {
        stone_format_00001_acct_v0_0_0(),
        stone_format_00002_membership_v0_0_0(),
        stone_format_00003_ideaunit_v0_0_0(),
        stone_format_00019_ideaunit_v0_0_0(),
        stone_format_00020_bud_acct_membership_v0_0_0(),
        stone_format_00021_bud_acctunit_v0_0_0(),
        stone_format_00022_bud_idea_awardlink_v0_0_0(),
        stone_format_00023_bud_idea_factunit_v0_0_0(),
        stone_format_00024_bud_idea_teamlink_v0_0_0(),
        stone_format_00025_bud_idea_healerhold_v0_0_0(),
        stone_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        stone_format_00027_bud_idea_reasonunit_v0_0_0(),
        stone_format_00028_bud_ideaunit_v0_0_0(),
        stone_format_00029_budunit_v0_0_0(),
        stone_format_00036_problem_healer_v0_0_0(),
    }


def get_stone_format_headers() -> dict[str, list[str]]:
    return {
        "acct_id,owner_id,real_id": stone_format_00001_acct_v0_0_0(),
        "acct_id,group_id,owner_id,real_id": stone_format_00002_membership_v0_0_0(),
        "label,mass,owner_id,parent_road,pledge,real_id": stone_format_00003_ideaunit_v0_0_0(),
        "addin,begin,close,denom,gogo_want,label,morph,numor,owner_id,parent_road,real_id,stop_want": stone_format_00019_ideaunit_v0_0_0(),
        "acct_id,credit_vote,debtit_vote,group_id,owner_id,real_id": stone_format_00020_bud_acct_membership_v0_0_0(),
        "acct_id,credit_score,debtit_score,owner_id,real_id": stone_format_00021_bud_acctunit_v0_0_0(),
        "give_force,group_id,owner_id,real_id,road,take_force": stone_format_00022_bud_idea_awardlink_v0_0_0(),
        "base,fnigh,fopen,owner_id,pick,real_id,road": stone_format_00023_bud_idea_factunit_v0_0_0(),
        "group_id,owner_id,real_id,road": stone_format_00024_bud_idea_teamlink_v0_0_0(),
        "healer_id,owner_id,real_id,road": stone_format_00025_bud_idea_healerhold_v0_0_0(),
        "base,divisor,need,nigh,open,owner_id,real_id,road": stone_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        "base,base_idea_active_requisite,owner_id,real_id,road": stone_format_00027_bud_idea_reasonunit_v0_0_0(),
        "addin,begin,close,denom,gogo_want,label,mass,morph,numor,owner_id,parent_road,pledge,problem_bool,real_id,stop_want": stone_format_00028_bud_ideaunit_v0_0_0(),
        "bit,credor_respect,debtor_respect,fund_coin,fund_pool,max_tree_traverse,monetary_desc,owner_id,penny,real_id,tally": stone_format_00029_budunit_v0_0_0(),
        "healer_id,label,owner_id,parent_road,problem_bool,real_id": stone_format_00036_problem_healer_v0_0_0(),
    }


def get_stoneref_dict(stone_name) -> dict:
    stoneref_filename = get_json_filename(stone_name)
    stoneref_json = open_file(get_stone_formats_dir(), stoneref_filename)
    return get_dict_from_json(stoneref_json)
