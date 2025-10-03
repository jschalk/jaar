from src.ch01_data_toolbox.dict_toolbox import create_csv
from src.ch03_finance_logic.allot import allot_scale
from src.ch04_voice_logic.group import AwardUnit, MemberShip
from src.ch04_voice_logic.voice import VoiceUnit, calc_give_take_net
from src.ch05_reason_logic.reason import (
    CaseUnit,
    FactUnit,
    ReasonUnit,
    get_factunits_from_dict,
)
from src.ch06_plan_logic.plan import PlanUnit
from src.ch07_belief_logic._ref.ch07_semantic_types import (
    FundNum,
    RespectNum,
    RopeTerm,
    VoiceName,
)
from src.ch07_belief_logic.belief_main import BeliefUnit


def beliefunit_exists(x_belief: BeliefUnit) -> bool:
    return x_belief is not None


def belief_voiceunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_voice_name = jkeys.get("voice_name")
    return False if x_belief is None else x_belief.voice_exists(x_voice_name)


def belief_voice_membership_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_voice_name = jkeys.get("voice_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        belief_voiceunit_exists(x_belief, jkeys)
        and x_belief.get_voice(x_voice_name).membership_exists(x_group_title)
    )


def belief_planunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    return False if x_belief is None else bool(x_belief.plan_exists(x_rope))


def belief_plan_awardunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        belief_planunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope).awardunit_exists(x_awardee_title)
    )


def belief_plan_reasonunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    return bool(
        belief_planunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope).reasonunit_exists(x_reason_context)
    )


def belief_plan_reason_caseunit_exists(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return bool(
        belief_plan_reasonunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .case_exists(x_reason_state)
    )


def belief_plan_partyunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_party_title = jkeys.get("party_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        belief_planunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope).laborunit.partyunit_exists(x_party_title)
    )


def belief_plan_healerunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("plan_rope")
    return bool(
        belief_planunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope).healerunit.healer_name_exists(x_healer_name)
    )


def belief_plan_factunit_exists(x_belief: BeliefUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_fact_context = jkeys.get("fact_context")
    return bool(
        belief_planunit_exists(x_belief, jkeys)
        and x_belief.get_plan_obj(x_rope).factunit_exists(x_fact_context)
    )


def belief_attr_exists(
    x_dimen: str, x_belief: BeliefUnit, jkeys: dict[str, any]
) -> bool:
    if x_dimen == "belief_voice_membership":
        return belief_voice_membership_exists(x_belief, jkeys)
    elif x_dimen == "belief_voiceunit":
        return belief_voiceunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_awardunit":
        return belief_plan_awardunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_factunit":
        return belief_plan_factunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_healerunit":
        return belief_plan_healerunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_reason_caseunit":
        return belief_plan_reason_caseunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_reasonunit":
        return belief_plan_reasonunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_plan_partyunit":
        return belief_plan_partyunit_exists(x_belief, jkeys)
    elif x_dimen == "belief_planunit":
        return belief_planunit_exists(x_belief, jkeys)
    elif x_dimen == "beliefunit":
        return beliefunit_exists(x_belief)
    return True


def belief_voiceunit_get_obj(x_belief: BeliefUnit, jkeys: dict[str, any]) -> VoiceUnit:
    return x_belief.get_voice(jkeys.get("voice_name"))


def belief_voice_membership_get_obj(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> MemberShip:
    x_voice_name = jkeys.get("voice_name")
    x_group_title = jkeys.get("group_title")
    return x_belief.get_voice(x_voice_name).get_membership(x_group_title)


def belief_planunit_get_obj(x_belief: BeliefUnit, jkeys: dict[str, any]) -> PlanUnit:
    x_rope = jkeys.get("plan_rope")
    return x_belief.get_plan_obj(x_rope)


def belief_plan_awardunit_get_obj(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> AwardUnit:
    x_rope = jkeys.get("plan_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_belief.get_plan_obj(x_rope).get_awardunit(x_awardee_title)


def belief_plan_reasonunit_get_obj(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> ReasonUnit:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    return x_belief.get_plan_obj(x_rope).get_reasonunit(x_reason_context)


def belief_plan_reason_caseunit_get_obj(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> CaseUnit:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return (
        x_belief.get_plan_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .get_case(x_reason_state)
    )


def belief_plan_factunit_get_obj(
    x_belief: BeliefUnit, jkeys: dict[str, any]
) -> FactUnit:
    x_rope = jkeys.get("plan_rope")
    x_fact_context = jkeys.get("fact_context")
    return x_belief.get_plan_obj(x_rope).factunits.get(x_fact_context)


def belief_get_obj(x_dimen: str, x_belief: BeliefUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "beliefunit":
        return x_belief

    x_dimens = {
        "belief_voiceunit": belief_voiceunit_get_obj,
        "belief_voice_membership": belief_voice_membership_get_obj,
        "belief_planunit": belief_planunit_get_obj,
        "belief_plan_awardunit": belief_plan_awardunit_get_obj,
        "belief_plan_reasonunit": belief_plan_reasonunit_get_obj,
        "belief_plan_reason_caseunit": belief_plan_reason_caseunit_get_obj,
        "belief_plan_factunit": belief_plan_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_belief, jkeys)


def get_belief_voice_agenda_award_array(
    x_belief: BeliefUnit, cashout: bool = None
) -> list[list]:
    if cashout:
        x_belief.cashout()

    x_list = [
        [
            x_voice.voice_name,
            x_voice.fund_agenda_take,
            x_voice.fund_agenda_give,
        ]
        for x_voice in x_belief.voices.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_belief_voice_agenda_award_csv(
    x_belief: BeliefUnit, cashout: bool = None
) -> str:
    x_voice_agenda_award_array = get_belief_voice_agenda_award_array(x_belief, cashout)
    x_headers = ["voice_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_voice_agenda_award_array)


def get_voice_mandate_ledger(
    x_belief: BeliefUnit, cashout: bool = None
) -> dict[VoiceName, FundNum]:
    if not x_belief:
        return {}
    if len(x_belief.voices) == 0:
        return {x_belief.belief_name: x_belief.fund_pool}

    if cashout:
        x_belief.cashout()
    belief_voices = x_belief.voices.values()
    mandates = {
        x_voice.voice_name: x_voice.fund_agenda_give for x_voice in belief_voices
    }
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_belief.money_grain)
    if mandate_sum != x_belief.fund_pool:
        mandates = allot_scale(mandates, x_belief.fund_pool, x_belief.fund_grain)
    return mandates


def reset_mandates_to_minimum(
    mandates: dict[VoiceName, FundNum], money_grain: FundNum
) -> dict[VoiceName, FundNum]:
    """Reset all mandates to the minimum value (money_grain)."""

    voice_names = set(mandates.keys())
    for voice_name in voice_names:
        mandates[voice_name] = money_grain
    return mandates


def get_voice_agenda_net_ledger(
    x_belief: BeliefUnit, cashout: bool = None
) -> dict[VoiceName, FundNum]:
    if cashout:
        x_belief.cashout()

    x_dict = {}
    for x_voice in x_belief.voices.values():
        settle_net = calc_give_take_net(
            x_voice.fund_agenda_give, x_voice.fund_agenda_take
        )
        if settle_net != 0:
            x_dict[x_voice.voice_name] = settle_net
    return x_dict


def get_credit_ledger(x_belief: BeliefUnit) -> dict[VoiceUnit, RespectNum]:
    credit_ledger, debt_ledger = x_belief.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_belief_root_facts_dict(
    x_belief: BeliefUnit,
) -> dict[RopeTerm, dict[str,]]:
    return x_belief.get_planroot_factunits_dict()


def set_factunits_to_belief(x_belief: BeliefUnit, x_facts_dict: dict[RopeTerm, dict]):
    factunits_dict = get_factunits_from_dict(x_facts_dict)
    missing_fact_reason_contexts = set(
        x_belief.get_missing_fact_reason_contexts().keys()
    )
    not_missing_fact_reason_contexts = set(
        x_belief.get_planroot_factunits_dict().keys()
    )
    belief_fact_reason_contexts = not_missing_fact_reason_contexts.union(
        missing_fact_reason_contexts
    )
    for factunit in factunits_dict.values():
        if factunit.fact_context in belief_fact_reason_contexts:
            x_belief.add_fact(
                factunit.fact_context,
                factunit.fact_state,
                factunit.fact_lower,
                factunit.fact_upper,
                create_missing_plans=True,
            )


def clear_factunits_from_belief(x_belief: BeliefUnit):
    for fact_reason_context in get_belief_root_facts_dict(x_belief).keys():
        x_belief.del_fact(fact_reason_context)


def set_case_attr(
    belief: BeliefUnit,
    plan_rope: RopeTerm,
    reason_context: RopeTerm,
    reason_case: RopeTerm,
):
    """Wrapper for method that edit beliefunit plan nodes reasonunits."""
    belief.edit_plan_attr(
        plan_rope=plan_rope, reason_context=reason_context, reason_case=reason_case
    )
