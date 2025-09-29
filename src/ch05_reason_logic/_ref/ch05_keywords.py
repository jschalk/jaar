from src.ch04_voice_logic._ref.ch04_keywords import *


def active_str() -> str:
    return "active"


def cases_str() -> str:
    return "cases"


def fact_context_str() -> str:
    return "fact_context"


def fact_lower_str() -> str:
    return "fact_lower"


def fact_state_str() -> str:
    return "fact_state"


def fact_upper_str() -> str:
    return "fact_upper"


def factheirs_str() -> str:
    return "factheirs"


def factunits_str() -> str:
    return "factunits"


def reason_active_requisite_str() -> str:
    return "reason_active_requisite"


def reason_context_str() -> str:
    return "reason_context"


def reason_divisor_str() -> str:
    return "reason_divisor"


def reason_lower_str() -> str:
    return "reason_lower"


def reason_state_str() -> str:
    return "reason_state"


def reason_upper_str() -> str:
    return "reason_upper"


def reasonunits_str() -> str:
    return "reasonunits"


def status_str() -> str:
    return "status"


def task_str() -> str:
    return "task"


class Ch05Keywords(str, Enum):
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
    awardee_title = "awardee_title"
    awardunits = "awardunits"
    belief_name = "belief_name"
    cases = "cases"
    credor_pool = "credor_pool"
    debtor_pool = "debtor_pool"
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
    fund_give = "fund_give"
    fund_iota = "fund_iota"
    fund_pool = "fund_pool"
    fund_take = "fund_take"
    give_force = "give_force"
    group_cred_points = "group_cred_points"
    group_debt_points = "group_debt_points"
    group_title = "group_title"
    groupunits = "groupunits"
    inallocable_voice_debt_points = "inallocable_voice_debt_points"
    irrational_voice_debt_points = "irrational_voice_debt_points"
    knot = "knot"
    laborheir = "laborheir"
    laborunit = "laborunit"
    magnitude = "magnitude"
    memberships = "memberships"
    parent_rope = "parent_rope"
    parent_solo = "parent_solo"
    party_title = "party_title"
    penny = "penny"
    rational = "rational"
    reason_active_requisite = "reason_active_requisite"
    reason_context = "reason_context"
    reason_divisor = "reason_divisor"
    reason_lower = "reason_lower"
    reason_state = "reason_state"
    reason_upper = "reason_upper"
    reasonunits = "reasonunits"
    respect_bit = "respect_bit"
    solo = "solo"
    sqlite_datatype = "sqlite_datatype"
    status = "status"
    take_force = "take_force"
    task = "task"
    voice_cred_points = "voice_cred_points"
    voice_debt_points = "voice_debt_points"
    voice_name = "voice_name"

    def __str__(self):
        return self.value
