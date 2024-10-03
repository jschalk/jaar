from src.f0_instrument.file import open_file
from src.f0_instrument.dict_tool import get_dict_from_json
from src.f1_road.jaar_config import get_json_filename
from src.f8_brick.examples.brick_env import src_brick_dir


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


def get_brick_formats_dir() -> str:
    return f"{src_brick_dir()}/brick_formats"


def brick_format_00001_acct_v0_0_0() -> str:
    return "brick_format_00001_acct_v0_0_0"


def brick_format_00002_membership_v0_0_0() -> str:
    return "brick_format_00002_membership_v0_0_0"


def brick_format_00003_ideaunit_v0_0_0() -> str:
    return "brick_format_00003_ideaunit_v0_0_0"


def brick_format_00019_ideaunit_v0_0_0() -> str:
    return "brick_format_00019_ideaunit_v0_0_0"


def brick_format_00036_problem_healer_v0_0_0() -> str:
    return "brick_format_00036_problem_healer_v0_0_0"


# def brick_format_00020_bud_acct_membership_v0_0_0()-> str: return "brick_format_00020_bud_acct_membership_v0_0_0"
# def brick_format_00021_bud_acctunit_v0_0_0()-> str: return "brick_format_00021_bud_acctunit_v0_0_0"
# def brick_format_00022_bud_idea_awardlink_v0_0_0()-> str: return "brick_format_00022_bud_idea_awardlink_v0_0_0"
# def brick_format_00023_bud_idea_factunit_v0_0_0()-> str: return "brick_format_00023_bud_idea_factunit_v0_0_0"
# def brick_format_00024_bud_idea_teamlink_v0_0_0()-> str: return "brick_format_00024_bud_idea_teamlink_v0_0_0"
# def brick_format_00025_bud_idea_healerlink_v0_0_0()-> str: return "brick_format_00025_bud_idea_healerlink_v0_0_0"
# def brick_format_00026_bud_idea_reason_premiseunit_v0_0_0()-> str: return "brick_format_00026_bud_idea_reason_premiseunit_v0_0_0"
# def brick_format_00027_bud_idea_reasonunit_v0_0_0()-> str: return "brick_format_00027_bud_idea_reasonunit_v0_0_0"
# def brick_format_00028_bud_ideaunit_v0_0_0()-> str: return "brick_format_00028_bud_ideaunit_v0_0_0"
# def brick_format_00029_budunit_v0_0_0()-> str: return "brick_format_00029_budunit_v0_0_0"
def brick_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "brick_format_00020_bud_acct_membership_v0_0_0"


def brick_format_00021_bud_acctunit_v0_0_0() -> str:
    return "brick_format_00021_bud_acctunit_v0_0_0"


def brick_format_00022_bud_idea_awardlink_v0_0_0() -> str:
    return "brick_format_00022_bud_idea_awardlink_v0_0_0"


def brick_format_00023_bud_idea_factunit_v0_0_0() -> str:
    return "brick_format_00023_bud_idea_factunit_v0_0_0"


def brick_format_00024_bud_idea_teamlink_v0_0_0() -> str:
    return "brick_format_00024_bud_idea_teamlink_v0_0_0"


def brick_format_00025_bud_idea_healerlink_v0_0_0() -> str:
    return "brick_format_00025_bud_idea_healerlink_v0_0_0"


def brick_format_00026_bud_idea_reason_premiseunit_v0_0_0() -> str:
    return "brick_format_00026_bud_idea_reason_premiseunit_v0_0_0"


def brick_format_00027_bud_idea_reasonunit_v0_0_0() -> str:
    return "brick_format_00027_bud_idea_reasonunit_v0_0_0"


def brick_format_00028_bud_ideaunit_v0_0_0() -> str:
    return "brick_format_00028_bud_ideaunit_v0_0_0"


def brick_format_00029_budunit_v0_0_0() -> str:
    return "brick_format_00029_budunit_v0_0_0"


def get_brick_filenames() -> set[str]:
    return {
        brick_format_00001_acct_v0_0_0(),
        brick_format_00002_membership_v0_0_0(),
        brick_format_00003_ideaunit_v0_0_0(),
        brick_format_00019_ideaunit_v0_0_0(),
        brick_format_00020_bud_acct_membership_v0_0_0(),
        brick_format_00021_bud_acctunit_v0_0_0(),
        brick_format_00022_bud_idea_awardlink_v0_0_0(),
        brick_format_00023_bud_idea_factunit_v0_0_0(),
        brick_format_00024_bud_idea_teamlink_v0_0_0(),
        brick_format_00025_bud_idea_healerlink_v0_0_0(),
        brick_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        brick_format_00027_bud_idea_reasonunit_v0_0_0(),
        brick_format_00028_bud_ideaunit_v0_0_0(),
        brick_format_00029_budunit_v0_0_0(),
        brick_format_00036_problem_healer_v0_0_0(),
    }


def get_brick_format_headers() -> dict[str, list[str]]:
    return {
        "acct_id,fiscal_id,owner_id": brick_format_00001_acct_v0_0_0(),
        "acct_id,fiscal_id,group_id,owner_id": brick_format_00002_membership_v0_0_0(),
        "fiscal_id,label,mass,owner_id,parent_road,pledge": brick_format_00003_ideaunit_v0_0_0(),
        "addin,begin,close,denom,fiscal_id,gogo_want,label,morph,numor,owner_id,parent_road,stop_want": brick_format_00019_ideaunit_v0_0_0(),
        "acct_id,credit_vote,debtit_vote,fiscal_id,group_id,owner_id": brick_format_00020_bud_acct_membership_v0_0_0(),
        "acct_id,credit_belief,debtit_belief,fiscal_id,owner_id": brick_format_00021_bud_acctunit_v0_0_0(),
        "fiscal_id,give_force,group_id,owner_id,road,take_force": brick_format_00022_bud_idea_awardlink_v0_0_0(),
        "base,fiscal_id,fnigh,fopen,owner_id,pick,road": brick_format_00023_bud_idea_factunit_v0_0_0(),
        "fiscal_id,group_id,owner_id,road": brick_format_00024_bud_idea_teamlink_v0_0_0(),
        "fiscal_id,healer_id,owner_id,road": brick_format_00025_bud_idea_healerlink_v0_0_0(),
        "base,divisor,fiscal_id,need,nigh,open,owner_id,road": brick_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        "base,base_idea_active_requisite,fiscal_id,owner_id,road": brick_format_00027_bud_idea_reasonunit_v0_0_0(),
        "addin,begin,close,denom,fiscal_id,gogo_want,label,mass,morph,numor,owner_id,parent_road,pledge,problem_bool,stop_want": brick_format_00028_bud_ideaunit_v0_0_0(),
        "credor_respect,debtor_respect,fiscal_id,fund_coin,fund_pool,max_tree_traverse,owner_id,penny,respect_bit,tally": brick_format_00029_budunit_v0_0_0(),
        "fiscal_id,healer_id,label,owner_id,parent_road,problem_bool": brick_format_00036_problem_healer_v0_0_0(),
    }


def get_brickref_dict(brick_name) -> dict:
    brickref_filename = get_json_filename(brick_name)
    brickref_json = open_file(get_brick_formats_dir(), brickref_filename)
    return get_dict_from_json(brickref_json)
