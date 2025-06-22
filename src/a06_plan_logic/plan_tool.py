from src.a00_data_toolbox.dict_toolbox import create_csv
from src.a01_term_logic.term import AcctName, BeliefLabel, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, RespectNum, get_net
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardLink, MemberShip
from src.a04_reason_logic.reason_concept import (
    FactUnit,
    PremiseUnit,
    ReasonUnit,
    factunits_get_from_dict,
)
from src.a05_concept_logic.concept import ConceptUnit
from src.a06_plan_logic.plan import PlanUnit


def planunit_exists(x_plan: PlanUnit) -> bool:
    return x_plan is not None


def plan_acctunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    return False if x_plan is None else x_plan.acct_exists(x_acct_name)


def plan_acct_membership_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        plan_acctunit_exists(x_plan, jkeys)
        and x_plan.get_acct(x_acct_name).membership_exists(x_group_title)
    )


def plan_conceptunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("concept_rope")
    return False if x_plan is None else bool(x_plan.concept_exists(x_rope))


def plan_concept_awardlink_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("concept_rope")
    return bool(
        plan_conceptunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope).awardlink_exists(x_awardee_title)
    )


def plan_concept_reasonunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("concept_rope")
    x_rcontext = jkeys.get("rcontext")
    return bool(
        plan_conceptunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope).reasonunit_exists(x_rcontext)
    )


def plan_concept_reason_premiseunit_exists(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("concept_rope")
    x_rcontext = jkeys.get("rcontext")
    x_pstate = jkeys.get("pstate")
    return bool(
        plan_concept_reasonunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope)
        .get_reasonunit(x_rcontext)
        .premise_exists(x_pstate)
    )


def plan_concept_laborlink_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_labor_title = jkeys.get("labor_title")
    x_rope = jkeys.get("concept_rope")
    return bool(
        plan_conceptunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope).laborunit.laborlink_exists(x_labor_title)
    )


def plan_concept_healerlink_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("concept_rope")
    return bool(
        plan_conceptunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope).healerlink.healer_name_exists(x_healer_name)
    )


def plan_concept_factunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("concept_rope")
    x_fcontext = jkeys.get("fcontext")
    return bool(
        plan_conceptunit_exists(x_plan, jkeys)
        and x_plan.get_concept_obj(x_rope).factunit_exists(x_fcontext)
    )


def plan_attr_exists(x_dimen: str, x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == "plan_acct_membership":
        return plan_acct_membership_exists(x_plan, jkeys)
    elif x_dimen == "plan_acctunit":
        return plan_acctunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_awardlink":
        return plan_concept_awardlink_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_factunit":
        return plan_concept_factunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_healerlink":
        return plan_concept_healerlink_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_reason_premiseunit":
        return plan_concept_reason_premiseunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_reasonunit":
        return plan_concept_reasonunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_concept_laborlink":
        return plan_concept_laborlink_exists(x_plan, jkeys)
    elif x_dimen == "plan_conceptunit":
        return plan_conceptunit_exists(x_plan, jkeys)
    elif x_dimen == "planunit":
        return planunit_exists(x_plan)
    return True


def plan_acctunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_plan.get_acct(jkeys.get("acct_name"))


def plan_acct_membership_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> MemberShip:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return x_plan.get_acct(x_acct_name).get_membership(x_group_title)


def plan_conceptunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> ConceptUnit:
    x_rope = jkeys.get("concept_rope")
    return x_plan.get_concept_obj(x_rope)


def plan_concept_awardlink_get_obj(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> AwardLink:
    x_rope = jkeys.get("concept_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_plan.get_concept_obj(x_rope).get_awardlink(x_awardee_title)


def plan_concept_reasonunit_get_obj(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> ReasonUnit:
    x_rope = jkeys.get("concept_rope")
    x_rcontext = jkeys.get("rcontext")
    return x_plan.get_concept_obj(x_rope).get_reasonunit(x_rcontext)


def plan_concept_reason_premiseunit_get_obj(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_rope = jkeys.get("concept_rope")
    x_rcontext = jkeys.get("rcontext")
    x_pstate = jkeys.get("pstate")
    return (
        x_plan.get_concept_obj(x_rope).get_reasonunit(x_rcontext).get_premise(x_pstate)
    )


def plan_concept_factunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> FactUnit:
    x_rope = jkeys.get("concept_rope")
    x_fcontext = jkeys.get("fcontext")
    return x_plan.get_concept_obj(x_rope).factunits.get(x_fcontext)


def plan_get_obj(x_dimen: str, x_plan: PlanUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "planunit":
        return x_plan

    x_dimens = {
        "plan_acctunit": plan_acctunit_get_obj,
        "plan_acct_membership": plan_acct_membership_get_obj,
        "plan_conceptunit": plan_conceptunit_get_obj,
        "plan_concept_awardlink": plan_concept_awardlink_get_obj,
        "plan_concept_reasonunit": plan_concept_reasonunit_get_obj,
        "plan_concept_reason_premiseunit": plan_concept_reason_premiseunit_get_obj,
        "plan_concept_factunit": plan_concept_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_plan, jkeys)


def get_plan_acct_agenda_award_array(
    x_plan: PlanUnit, settle_plan: bool = None
) -> list[list]:
    if settle_plan:
        x_plan.settle_plan()

    x_list = [
        [x_acct.acct_name, x_acct._fund_agenda_take, x_acct._fund_agenda_give]
        for x_acct in x_plan.accts.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_plan_acct_agenda_award_csv(x_plan: PlanUnit, settle_plan: bool = None) -> str:
    x_acct_agenda_award_array = get_plan_acct_agenda_award_array(x_plan, settle_plan)
    x_headers = ["acct_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_acct_agenda_award_array)


def get_acct_mandate_ledger(
    x_plan: PlanUnit, settle_plan: bool = None
) -> dict[AcctName, FundNum]:
    if not x_plan:
        return {}
    if len(x_plan.accts) == 0:
        return {x_plan.owner_name: x_plan.fund_pool}

    if settle_plan:
        x_plan.settle_plan()
    plan_accts = x_plan.accts.values()
    mandates = {x_acct.acct_name: x_acct._fund_agenda_give for x_acct in plan_accts}
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_plan.penny)
    if mandate_sum != x_plan.fund_pool:
        mandates = allot_scale(mandates, x_plan.fund_pool, x_plan.fund_iota)
    return mandates


def reset_mandates_to_minimum(
    mandates: dict[AcctName, FundNum], penny: FundNum
) -> dict[AcctName, FundNum]:
    """Reset all mandates to the minimum value (penny)."""

    acct_names = set(mandates.keys())
    for acct_name in acct_names:
        mandates[acct_name] = penny
    return mandates


def get_acct_agenda_net_ledger(
    x_plan: PlanUnit, settle_plan: bool = None
) -> dict[AcctName, FundNum]:
    if settle_plan:
        x_plan.settle_plan()

    x_dict = {}
    for x_acct in x_plan.accts.values():
        settle_net = get_net(x_acct._fund_agenda_give, x_acct._fund_agenda_take)
        if settle_net != 0:
            x_dict[x_acct.acct_name] = settle_net
    return x_dict


def get_credit_ledger(x_plan: PlanUnit) -> dict[AcctUnit, RespectNum]:
    credit_ledger, debt_ledger = x_plan.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_plan_root_facts_dict(x_plan: PlanUnit) -> dict[RopeTerm, dict[str,]]:
    return x_plan.get_factunits_dict()


def set_factunits_to_plan(x_plan: PlanUnit, x_facts_dict: dict[RopeTerm, dict]):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_rcontexts = set(x_plan.get_missing_fact_rcontexts().keys())
    not_missing_fact_rcontexts = set(x_plan.get_factunits_dict().keys())
    plan_fact_rcontexts = not_missing_fact_rcontexts.union(missing_fact_rcontexts)
    for factunit in factunits_dict.values():
        if factunit.fcontext in plan_fact_rcontexts:
            x_plan.add_fact(
                factunit.fcontext,
                factunit.fstate,
                factunit.fopen,
                factunit.fnigh,
                create_missing_concepts=True,
            )


def clear_factunits_from_plan(x_plan: PlanUnit):
    for fact_rcontext in get_plan_root_facts_dict(x_plan).keys():
        x_plan.del_fact(fact_rcontext)
