from src.ch06_plan_logic._ref.ch06_keywords import *


def BeliefName_str() -> str:
    return "BeliefName"


def ancestors_str() -> str:
    return "ancestors"


def attributes_str() -> str:
    return "attributes"


def belief_groupunit_str() -> str:
    """Is not saved to raw data beliefunit json"""
    return "belief_groupunit"


def belief_plan_awardunit_str() -> str:
    return "belief_plan_awardunit"


def belief_plan_factunit_str() -> str:
    return "belief_plan_factunit"


def belief_plan_healerunit_str() -> str:
    return "belief_plan_healerunit"


def belief_plan_partyunit_str() -> str:
    return "belief_plan_partyunit"


def belief_plan_reason_caseunit_str() -> str:
    return "belief_plan_reason_caseunit"


def belief_plan_reasonunit_str() -> str:
    return "belief_plan_reasonunit"


def belief_planunit_str() -> str:
    return "belief_planunit"


def belief_voice_membership_str() -> str:
    return "belief_voice_membership"


def belief_voiceunit_str() -> str:
    return "belief_voiceunit"


def beliefunit_str() -> str:
    return "beliefunit"


def class_type_str() -> str:
    return "class_type"


def credor_respect_str() -> str:
    return "credor_respect"


def debtor_respect_str() -> str:
    return "debtor_respect"


def dimen_str() -> str:
    return "dimen"


def dimens_str() -> str:
    return "dimens"


def jkeys_str() -> str:
    return "jkeys"


def jvalues_str() -> str:
    return "jvalues"


def keeps_buildable_str() -> str:
    return "keeps_buildable"


def keeps_justified_str() -> str:
    return "keeps_justified"


def last_pack_id_str() -> str:
    return "last_pack_id"


def mandate_str() -> str:
    return "mandate"


def max_tree_traverse_str() -> str:
    return "max_tree_traverse"


def offtrack_fund_str() -> str:
    return "offtrack_fund"


def offtrack_kids_star_set_str() -> str:
    return "offtrack_kids_star_set"


def planroot_str() -> str:
    return "planroot"


def reason_contexts_str() -> str:
    return "reason_contexts"


def sum_healerunit_share_str() -> str:
    return "sum_healerunit_share"


def tally_str() -> str:
    return "tally"


def voice_pool_str() -> str:
    return "voice_pool"


def voices_str() -> str:
    return "voices"


class Ch07Keywords(str, Enum):
    BeliefName = "BeliefName"
    BitNum = "BitNum"
    FundIota = "FundIota"
    FundNum = "FundNum"
    GrainFloat = "GrainFloat"
    GroupTitle = "GroupTitle"
    HealerName = "HealerName"
    INSERT = "INSERT"
    KnotTerm = "KnotTerm"
    LabelTerm = "LabelTerm"
    MomentLabel = "MomentLabel"
    MoneyUnit = "MoneyUnit"
    NameTerm = "NameTerm"
    NexusLabel = "NexusLabel"
    PennyNum = "PennyNum"
    RespectNum = "RespectNum"
    RopeTerm = "RopeTerm"
    TitleTerm = "TitleTerm"
    UPDATE = "UPDATE"
    VoiceName = "VoiceName"
    active = "active"
    active_hx = "active_hx"
    addin = "addin"
    all_voice_cred = "all_voice_cred"
    all_voice_debt = "all_voice_debt"
    ancestors = "ancestors"
    attributes = "attributes"
    awardee_title = "awardee_title"
    awardheirs = "awardheirs"
    awardlines = "awardlines"
    awardunits = "awardunits"
    begin = "begin"
    belief_groupunit = "belief_groupunit"
    belief_name = "belief_name"
    belief_plan_awardunit = "belief_plan_awardunit"
    belief_plan_factunit = "belief_plan_factunit"
    belief_plan_healerunit = "belief_plan_healerunit"
    belief_plan_partyunit = "belief_plan_partyunit"
    belief_plan_reason_caseunit = "belief_plan_reason_caseunit"
    belief_plan_reasonunit = "belief_plan_reasonunit"
    belief_planunit = "belief_planunit"
    belief_voice_membership = "belief_voice_membership"
    belief_voiceunit = "belief_voiceunit"
    beliefunit = "beliefunit"
    cases = "cases"
    class_type = "class_type"
    close = "close"
    credor_pool = "credor_pool"
    credor_respect = "credor_respect"
    debtor_pool = "debtor_pool"
    debtor_respect = "debtor_respect"
    denom = "denom"
    descendant_pledge_count = "descendant_pledge_count"
    dimen = "dimen"
    dimens = "dimens"
    fact_context = "fact_context"
    fact_lower = "fact_lower"
    fact_state = "fact_state"
    fact_upper = "fact_upper"
    factheirs = "factheirs"
    factunits = "factunits"
    fund_agenda_give = "fund_agenda_give"
    fund_agenda_ratio_give = "fund_agenda_ratio_give"
    fund_agenda_ratio_take = "fund_agenda_ratio_take"
    fund_agenda_take = "fund_agenda_take"
    fund_cease = "fund_cease"
    fund_give = "fund_give"
    fund_iota = "fund_iota"
    fund_onset = "fund_onset"
    fund_pool = "fund_pool"
    fund_ratio = "fund_ratio"
    fund_share = "fund_share"
    fund_take = "fund_take"
    give_force = "give_force"
    gogo_calc = "gogo_calc"
    gogo_want = "gogo_want"
    group_cred_points = "group_cred_points"
    group_debt_points = "group_debt_points"
    group_title = "group_title"
    groupunits = "groupunits"
    healer_name = "healer_name"
    healerunit = "healerunit"
    healerunit_ratio = "healerunit_ratio"
    inallocable_voice_debt_points = "inallocable_voice_debt_points"
    irrational_voice_debt_points = "irrational_voice_debt_points"
    is_expanded = "is_expanded"
    jkeys = "jkeys"
    jvalues = "jvalues"
    keeps_buildable = "keeps_buildable"
    keeps_justified = "keeps_justified"
    kids = "kids"
    knot = "knot"
    laborheir = "laborheir"
    laborunit = "laborunit"
    last_pack_id = "last_pack_id"
    magnitude = "magnitude"
    mandate = "mandate"
    max_tree_traverse = "max_tree_traverse"
    memberships = "memberships"
    moment_label = "moment_label"
    morph = "morph"
    numor = "numor"
    offtrack_fund = "offtrack_fund"
    offtrack_kids_star_set = "offtrack_kids_star_set"
    parent_rope = "parent_rope"
    parent_solo = "parent_solo"
    party_title = "party_title"
    penny = "penny"
    plan_label = "plan_label"
    plan_rope = "plan_rope"
    planroot = "planroot"
    pledge = "pledge"
    problem_bool = "problem_bool"
    range_evaluated = "range_evaluated"
    rational = "rational"
    reason_active_requisite = "reason_active_requisite"
    reason_context = "reason_context"
    reason_contexts = "reason_contexts"
    reason_divisor = "reason_divisor"
    reason_lower = "reason_lower"
    reason_state = "reason_state"
    reason_upper = "reason_upper"
    reasonheirs = "reasonheirs"
    reasonunits = "reasonunits"
    respect_bit = "respect_bit"
    solo = "solo"
    sqlite_datatype = "sqlite_datatype"
    star = "star"
    status = "status"
    stop_calc = "stop_calc"
    stop_want = "stop_want"
    sum_healerunit_share = "sum_healerunit_share"
    take_force = "take_force"
    tally = "tally"
    task = "task"
    tree_level = "tree_level"
    tree_traverse_count = "tree_traverse_count"
    uid = "uid"
    voice_cred_points = "voice_cred_points"
    voice_debt_points = "voice_debt_points"
    voice_name = "voice_name"
    voice_pool = "voice_pool"
    voices = "voices"
