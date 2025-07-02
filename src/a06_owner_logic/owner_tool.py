from src.a00_data_toolbox.dict_toolbox import create_csv
from src.a01_term_logic.term import AcctName, BeliefLabel, RopeTerm
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, RespectNum, get_net
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardLink, MemberShip
from src.a04_reason_logic.reason_plan import (
    FactUnit,
    PremiseUnit,
    ReasonUnit,
    factunits_get_from_dict,
)
from src.a05_plan_logic.plan import PlanUnit
from src.a06_owner_logic.owner import OwnerUnit


def ownerunit_exists(x_owner: OwnerUnit) -> bool:
    return x_owner is not None


def owner_acctunit_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    return False if x_owner is None else x_owner.acct_exists(x_acct_name)


def owner_acct_membership_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        owner_acctunit_exists(x_owner, jkeys)
        and x_owner.get_acct(x_acct_name).membership_exists(x_group_title)
    )


def owner_planunit_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    return False if x_owner is None else bool(x_owner.plan_exists(x_rope))


def owner_plan_awardlink_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        owner_planunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope).awardlink_exists(x_awardee_title)
    )


def owner_plan_reasonunit_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_rcontext = jkeys.get("rcontext")
    return bool(
        owner_planunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope).reasonunit_exists(x_rcontext)
    )


def owner_plan_reason_premiseunit_exists(
    x_owner: OwnerUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_rcontext = jkeys.get("rcontext")
    x_pstate = jkeys.get("pstate")
    return bool(
        owner_plan_reasonunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope)
        .get_reasonunit(x_rcontext)
        .premise_exists(x_pstate)
    )


def owner_plan_laborlink_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_labor_title = jkeys.get("labor_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        owner_planunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope).laborunit.laborlink_exists(x_labor_title)
    )


def owner_plan_healerlink_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("plan_rope")
    return bool(
        owner_planunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope).healerlink.healer_name_exists(x_healer_name)
    )


def owner_plan_factunit_exists(x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_fcontext = jkeys.get("fcontext")
    return bool(
        owner_planunit_exists(x_owner, jkeys)
        and x_owner.get_plan_obj(x_rope).factunit_exists(x_fcontext)
    )


def owner_attr_exists(x_dimen: str, x_owner: OwnerUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == "owner_acct_membership":
        return owner_acct_membership_exists(x_owner, jkeys)
    elif x_dimen == "owner_acctunit":
        return owner_acctunit_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_awardlink":
        return owner_plan_awardlink_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_factunit":
        return owner_plan_factunit_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_healerlink":
        return owner_plan_healerlink_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_reason_premiseunit":
        return owner_plan_reason_premiseunit_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_reasonunit":
        return owner_plan_reasonunit_exists(x_owner, jkeys)
    elif x_dimen == "owner_plan_laborlink":
        return owner_plan_laborlink_exists(x_owner, jkeys)
    elif x_dimen == "owner_planunit":
        return owner_planunit_exists(x_owner, jkeys)
    elif x_dimen == "ownerunit":
        return ownerunit_exists(x_owner)
    return True


def owner_acctunit_get_obj(x_owner: OwnerUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_owner.get_acct(jkeys.get("acct_name"))


def owner_acct_membership_get_obj(
    x_owner: OwnerUnit, jkeys: dict[str, any]
) -> MemberShip:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return x_owner.get_acct(x_acct_name).get_membership(x_group_title)


def owner_planunit_get_obj(x_owner: OwnerUnit, jkeys: dict[str, any]) -> PlanUnit:
    x_rope = jkeys.get("plan_rope")
    return x_owner.get_plan_obj(x_rope)


def owner_plan_awardlink_get_obj(
    x_owner: OwnerUnit, jkeys: dict[str, any]
) -> AwardLink:
    x_rope = jkeys.get("plan_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_owner.get_plan_obj(x_rope).get_awardlink(x_awardee_title)


def owner_plan_reasonunit_get_obj(
    x_owner: OwnerUnit, jkeys: dict[str, any]
) -> ReasonUnit:
    x_rope = jkeys.get("plan_rope")
    x_rcontext = jkeys.get("rcontext")
    return x_owner.get_plan_obj(x_rope).get_reasonunit(x_rcontext)


def owner_plan_reason_premiseunit_get_obj(
    x_owner: OwnerUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_rope = jkeys.get("plan_rope")
    x_rcontext = jkeys.get("rcontext")
    x_pstate = jkeys.get("pstate")
    return x_owner.get_plan_obj(x_rope).get_reasonunit(x_rcontext).get_premise(x_pstate)


def owner_plan_factunit_get_obj(x_owner: OwnerUnit, jkeys: dict[str, any]) -> FactUnit:
    x_rope = jkeys.get("plan_rope")
    x_fcontext = jkeys.get("fcontext")
    return x_owner.get_plan_obj(x_rope).factunits.get(x_fcontext)


def owner_get_obj(x_dimen: str, x_owner: OwnerUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "ownerunit":
        return x_owner

    x_dimens = {
        "owner_acctunit": owner_acctunit_get_obj,
        "owner_acct_membership": owner_acct_membership_get_obj,
        "owner_planunit": owner_planunit_get_obj,
        "owner_plan_awardlink": owner_plan_awardlink_get_obj,
        "owner_plan_reasonunit": owner_plan_reasonunit_get_obj,
        "owner_plan_reason_premiseunit": owner_plan_reason_premiseunit_get_obj,
        "owner_plan_factunit": owner_plan_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_owner, jkeys)


def get_owner_acct_agenda_award_array(
    x_owner: OwnerUnit, settle_owner: bool = None
) -> list[list]:
    if settle_owner:
        x_owner.settle_owner()

    x_list = [
        [x_acct.acct_name, x_acct._fund_agenda_take, x_acct._fund_agenda_give]
        for x_acct in x_owner.accts.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_owner_acct_agenda_award_csv(
    x_owner: OwnerUnit, settle_owner: bool = None
) -> str:
    x_acct_agenda_award_array = get_owner_acct_agenda_award_array(x_owner, settle_owner)
    x_headers = ["acct_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_acct_agenda_award_array)


def get_acct_mandate_ledger(
    x_owner: OwnerUnit, settle_owner: bool = None
) -> dict[AcctName, FundNum]:
    if not x_owner:
        return {}
    if len(x_owner.accts) == 0:
        return {x_owner.owner_name: x_owner.fund_pool}

    if settle_owner:
        x_owner.settle_owner()
    owner_accts = x_owner.accts.values()
    mandates = {x_acct.acct_name: x_acct._fund_agenda_give for x_acct in owner_accts}
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_owner.penny)
    if mandate_sum != x_owner.fund_pool:
        mandates = allot_scale(mandates, x_owner.fund_pool, x_owner.fund_iota)
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
    x_owner: OwnerUnit, settle_owner: bool = None
) -> dict[AcctName, FundNum]:
    if settle_owner:
        x_owner.settle_owner()

    x_dict = {}
    for x_acct in x_owner.accts.values():
        settle_net = get_net(x_acct._fund_agenda_give, x_acct._fund_agenda_take)
        if settle_net != 0:
            x_dict[x_acct.acct_name] = settle_net
    return x_dict


def get_credit_ledger(x_owner: OwnerUnit) -> dict[AcctUnit, RespectNum]:
    credit_ledger, debt_ledger = x_owner.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_owner_root_facts_dict(x_owner: OwnerUnit) -> dict[RopeTerm, dict[str,]]:
    return x_owner.get_factunits_dict()


def set_factunits_to_owner(x_owner: OwnerUnit, x_facts_dict: dict[RopeTerm, dict]):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_rcontexts = set(x_owner.get_missing_fact_rcontexts().keys())
    not_missing_fact_rcontexts = set(x_owner.get_factunits_dict().keys())
    owner_fact_rcontexts = not_missing_fact_rcontexts.union(missing_fact_rcontexts)
    for factunit in factunits_dict.values():
        if factunit.fcontext in owner_fact_rcontexts:
            x_owner.add_fact(
                factunit.fcontext,
                factunit.fstate,
                factunit.fopen,
                factunit.fnigh,
                create_missing_plans=True,
            )


def clear_factunits_from_owner(x_owner: OwnerUnit):
    for fact_rcontext in get_owner_root_facts_dict(x_owner).keys():
        x_owner.del_fact(fact_rcontext)
