from src.a00_data_toolbox.dict_toolbox import create_csv
from src.a01_term_logic.term import BeliefLabel, PartnerName, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, RespectNum, get_net
from src.a03_group_logic.group import AwardLink, MemberShip
from src.a03_group_logic.partner import PartnerUnit
from src.a04_reason_logic.reason_plan import (
    FactUnit,
    PremiseUnit,
    ReasonUnit,
    factunits_get_from_dict,
)
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer import BelieverUnit


def believerunit_exists(x_believer: BelieverUnit) -> bool:
    return x_believer is not None


def believer_partnerunit_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_partner_name = jkeys.get("partner_name")
    return False if x_believer is None else x_believer.partner_exists(x_partner_name)


def believer_partner_membership_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_partner_name = jkeys.get("partner_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        believer_partnerunit_exists(x_believer, jkeys)
        and x_believer.get_partner(x_partner_name).membership_exists(x_group_title)
    )


def believer_planunit_exists(x_believer: BelieverUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    return False if x_believer is None else bool(x_believer.plan_exists(x_rope))


def believer_plan_awardlink_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        believer_planunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope).awardlink_exists(x_awardee_title)
    )


def believer_plan_reasonunit_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_r_context = jkeys.get("r_context")
    return bool(
        believer_planunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope).reasonunit_exists(x_r_context)
    )


def believer_plan_reason_premiseunit_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_r_context = jkeys.get("r_context")
    x_p_state = jkeys.get("p_state")
    return bool(
        believer_plan_reasonunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope)
        .get_reasonunit(x_r_context)
        .premise_exists(x_p_state)
    )


def believer_plan_laborlink_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_labor_title = jkeys.get("labor_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        believer_planunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope).laborunit.laborlink_exists(x_labor_title)
    )


def believer_plan_healerlink_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("plan_rope")
    return bool(
        believer_planunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope).healerlink.healer_name_exists(x_healer_name)
    )


def believer_plan_factunit_exists(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_f_context = jkeys.get("f_context")
    return bool(
        believer_planunit_exists(x_believer, jkeys)
        and x_believer.get_plan_obj(x_rope).factunit_exists(x_f_context)
    )


def believer_attr_exists(
    x_dimen: str, x_believer: BelieverUnit, jkeys: dict[str, any]
) -> bool:
    if x_dimen == "believer_partner_membership":
        return believer_partner_membership_exists(x_believer, jkeys)
    elif x_dimen == "believer_partnerunit":
        return believer_partnerunit_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_awardlink":
        return believer_plan_awardlink_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_factunit":
        return believer_plan_factunit_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_healerlink":
        return believer_plan_healerlink_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_reason_premiseunit":
        return believer_plan_reason_premiseunit_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_reasonunit":
        return believer_plan_reasonunit_exists(x_believer, jkeys)
    elif x_dimen == "believer_plan_laborlink":
        return believer_plan_laborlink_exists(x_believer, jkeys)
    elif x_dimen == "believer_planunit":
        return believer_planunit_exists(x_believer, jkeys)
    elif x_dimen == "believerunit":
        return believerunit_exists(x_believer)
    return True


def believer_partnerunit_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> PartnerUnit:
    return x_believer.get_partner(jkeys.get("partner_name"))


def believer_partner_membership_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> MemberShip:
    x_partner_name = jkeys.get("partner_name")
    x_group_title = jkeys.get("group_title")
    return x_believer.get_partner(x_partner_name).get_membership(x_group_title)


def believer_planunit_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> PlanUnit:
    x_rope = jkeys.get("plan_rope")
    return x_believer.get_plan_obj(x_rope)


def believer_plan_awardlink_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> AwardLink:
    x_rope = jkeys.get("plan_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_believer.get_plan_obj(x_rope).get_awardlink(x_awardee_title)


def believer_plan_reasonunit_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> ReasonUnit:
    x_rope = jkeys.get("plan_rope")
    x_r_context = jkeys.get("r_context")
    return x_believer.get_plan_obj(x_rope).get_reasonunit(x_r_context)


def believer_plan_reason_premiseunit_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_rope = jkeys.get("plan_rope")
    x_r_context = jkeys.get("r_context")
    x_p_state = jkeys.get("p_state")
    return (
        x_believer.get_plan_obj(x_rope)
        .get_reasonunit(x_r_context)
        .get_premise(x_p_state)
    )


def believer_plan_factunit_get_obj(
    x_believer: BelieverUnit, jkeys: dict[str, any]
) -> FactUnit:
    x_rope = jkeys.get("plan_rope")
    x_f_context = jkeys.get("f_context")
    return x_believer.get_plan_obj(x_rope).factunits.get(x_f_context)


def believer_get_obj(
    x_dimen: str, x_believer: BelieverUnit, jkeys: dict[str, any]
) -> any:
    if x_dimen == "believerunit":
        return x_believer

    x_dimens = {
        "believer_partnerunit": believer_partnerunit_get_obj,
        "believer_partner_membership": believer_partner_membership_get_obj,
        "believer_planunit": believer_planunit_get_obj,
        "believer_plan_awardlink": believer_plan_awardlink_get_obj,
        "believer_plan_reasonunit": believer_plan_reasonunit_get_obj,
        "believer_plan_reason_premiseunit": believer_plan_reason_premiseunit_get_obj,
        "believer_plan_factunit": believer_plan_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_believer, jkeys)


def get_believer_partner_agenda_award_array(
    x_believer: BelieverUnit, settle_believer: bool = None
) -> list[list]:
    if settle_believer:
        x_believer.settle_believer()

    x_list = [
        [
            x_partner.partner_name,
            x_partner._fund_agenda_take,
            x_partner._fund_agenda_give,
        ]
        for x_partner in x_believer.partners.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_believer_partner_agenda_award_csv(
    x_believer: BelieverUnit, settle_believer: bool = None
) -> str:
    x_partner_agenda_award_array = get_believer_partner_agenda_award_array(
        x_believer, settle_believer
    )
    x_headers = ["partner_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_partner_agenda_award_array)


def get_partner_mandate_ledger(
    x_believer: BelieverUnit, settle_believer: bool = None
) -> dict[PartnerName, FundNum]:
    if not x_believer:
        return {}
    if len(x_believer.partners) == 0:
        return {x_believer.believer_name: x_believer.fund_pool}

    if settle_believer:
        x_believer.settle_believer()
    believer_partners = x_believer.partners.values()
    mandates = {
        x_partner.partner_name: x_partner._fund_agenda_give
        for x_partner in believer_partners
    }
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_believer.penny)
    if mandate_sum != x_believer.fund_pool:
        mandates = allot_scale(mandates, x_believer.fund_pool, x_believer.fund_iota)
    return mandates


def reset_mandates_to_minimum(
    mandates: dict[PartnerName, FundNum], penny: FundNum
) -> dict[PartnerName, FundNum]:
    """Reset all mandates to the minimum value (penny)."""

    partner_names = set(mandates.keys())
    for partner_name in partner_names:
        mandates[partner_name] = penny
    return mandates


def get_partner_agenda_net_ledger(
    x_believer: BelieverUnit, settle_believer: bool = None
) -> dict[PartnerName, FundNum]:
    if settle_believer:
        x_believer.settle_believer()

    x_dict = {}
    for x_partner in x_believer.partners.values():
        settle_net = get_net(x_partner._fund_agenda_give, x_partner._fund_agenda_take)
        if settle_net != 0:
            x_dict[x_partner.partner_name] = settle_net
    return x_dict


def get_credit_ledger(x_believer: BelieverUnit) -> dict[PartnerUnit, RespectNum]:
    credit_ledger, debt_ledger = x_believer.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_believer_root_facts_dict(
    x_believer: BelieverUnit,
) -> dict[RopeTerm, dict[str,]]:
    return x_believer.get_factunits_dict()


def set_factunits_to_believer(
    x_believer: BelieverUnit, x_facts_dict: dict[RopeTerm, dict]
):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_r_contexts = set(x_believer.get_missing_fact_r_contexts().keys())
    not_missing_fact_r_contexts = set(x_believer.get_factunits_dict().keys())
    believer_fact_r_contexts = not_missing_fact_r_contexts.union(
        missing_fact_r_contexts
    )
    for factunit in factunits_dict.values():
        if factunit.f_context in believer_fact_r_contexts:
            x_believer.add_fact(
                factunit.f_context,
                factunit.f_state,
                factunit.f_lower,
                factunit.f_upper,
                create_missing_plans=True,
            )


def clear_factunits_from_believer(x_believer: BelieverUnit):
    for fact_r_context in get_believer_root_facts_dict(x_believer).keys():
        x_believer.del_fact(fact_r_context)
