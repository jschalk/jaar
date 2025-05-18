from src.a00_data_toolbox.dict_toolbox import create_csv
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, get_net, RespectNum
from src.a01_way_logic.way import AcctName, FiscLabel, WayStr
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import MemberShip, AwardLink
from src.a05_idea_logic.idea import IdeaUnit
from src.a04_reason_logic.reason_idea import (
    ReasonUnit,
    FactUnit,
    PremiseUnit,
    factunits_get_from_dict,
)
from src.a06_bud_logic.bud import BudUnit


def budunit_exists(x_bud: BudUnit) -> bool:
    return x_bud is not None


def bud_acctunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    return False if x_bud is None else x_bud.acct_exists(x_acct_name)


def bud_acct_membership_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        bud_acctunit_exists(x_bud, jkeys)
        and x_bud.get_acct(x_acct_name).membership_exists(x_group_title)
    )


def bud_ideaunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("idea_way")
    return False if x_bud is None else bool(x_bud.idea_exists(x_way))


def bud_idea_awardlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_way = jkeys.get("idea_way")
    return bool(
        bud_ideaunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way).awardlink_exists(x_awardee_title)
    )


def bud_idea_reasonunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("idea_way")
    x_rcontext = jkeys.get("rcontext")
    return bool(
        bud_ideaunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way).reasonunit_exists(x_rcontext)
    )


def bud_idea_reason_premiseunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("idea_way")
    x_rcontext = jkeys.get("rcontext")
    x_pbranch = jkeys.get("pbranch")
    return bool(
        bud_idea_reasonunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way)
        .get_reasonunit(x_rcontext)
        .premise_exists(x_pbranch)
    )


def bud_idea_laborlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_labor_title = jkeys.get("labor_title")
    x_way = jkeys.get("idea_way")
    return bool(
        bud_ideaunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way).laborunit.laborlink_exists(x_labor_title)
    )


def bud_idea_healerlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_way = jkeys.get("idea_way")
    return bool(
        bud_ideaunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way).healerlink.healer_name_exists(x_healer_name)
    )


def bud_idea_factunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("idea_way")
    x_fcontext = jkeys.get("fcontext")
    return bool(
        bud_ideaunit_exists(x_bud, jkeys)
        and x_bud.get_idea_obj(x_way).factunit_exists(x_fcontext)
    )


def bud_attr_exists(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == "bud_acct_membership":
        return bud_acct_membership_exists(x_bud, jkeys)
    elif x_dimen == "bud_acctunit":
        return bud_acctunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_awardlink":
        return bud_idea_awardlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_factunit":
        return bud_idea_factunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_healerlink":
        return bud_idea_healerlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_reason_premiseunit":
        return bud_idea_reason_premiseunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_reasonunit":
        return bud_idea_reasonunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_idea_laborlink":
        return bud_idea_laborlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_ideaunit":
        return bud_ideaunit_exists(x_bud, jkeys)
    elif x_dimen == "budunit":
        return budunit_exists(x_bud)
    return True


def bud_acctunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_bud.get_acct(jkeys.get("acct_name"))


def bud_acct_membership_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> MemberShip:
    x_acct_name = jkeys.get("acct_name")
    x_group_title = jkeys.get("group_title")
    return x_bud.get_acct(x_acct_name).get_membership(x_group_title)


def bud_ideaunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> IdeaUnit:
    x_way = jkeys.get("idea_way")
    return x_bud.get_idea_obj(x_way)


def bud_idea_awardlink_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AwardLink:
    x_way = jkeys.get("idea_way")
    x_awardee_title = jkeys.get("awardee_title")
    return x_bud.get_idea_obj(x_way).get_awardlink(x_awardee_title)


def bud_idea_reasonunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ReasonUnit:
    x_way = jkeys.get("idea_way")
    x_rcontext = jkeys.get("rcontext")
    return x_bud.get_idea_obj(x_way).get_reasonunit(x_rcontext)


def bud_idea_reason_premiseunit_get_obj(
    x_bud: BudUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_way = jkeys.get("idea_way")
    x_rcontext = jkeys.get("rcontext")
    x_pbranch = jkeys.get("pbranch")
    return x_bud.get_idea_obj(x_way).get_reasonunit(x_rcontext).get_premise(x_pbranch)


def bud_idea_factunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> FactUnit:
    x_way = jkeys.get("idea_way")
    x_fcontext = jkeys.get("fcontext")
    print(f"{x_fcontext=}")
    print(f"{x_bud.get_idea_obj(x_way).factunits=}")
    return x_bud.get_idea_obj(x_way).factunits.get(x_fcontext)


def bud_get_obj(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "budunit":
        return x_bud

    x_dimens = {
        "bud_acctunit": bud_acctunit_get_obj,
        "bud_acct_membership": bud_acct_membership_get_obj,
        "bud_ideaunit": bud_ideaunit_get_obj,
        "bud_idea_awardlink": bud_idea_awardlink_get_obj,
        "bud_idea_reasonunit": bud_idea_reasonunit_get_obj,
        "bud_idea_reason_premiseunit": bud_idea_reason_premiseunit_get_obj,
        "bud_idea_factunit": bud_idea_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_bud, jkeys)


def get_bud_acct_agenda_award_array(
    x_bud: BudUnit, settle_bud: bool = None
) -> list[list]:
    if settle_bud:
        x_bud.settle_bud()

    x_list = [
        [x_acct.acct_name, x_acct._fund_agenda_take, x_acct._fund_agenda_give]
        for x_acct in x_bud.accts.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_bud_acct_agenda_award_csv(x_bud: BudUnit, settle_bud: bool = None) -> str:
    x_acct_agenda_award_array = get_bud_acct_agenda_award_array(x_bud, settle_bud)
    x_headers = ["acct_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_acct_agenda_award_array)


def get_acct_mandate_ledger(
    x_bud: BudUnit, settle_bud: bool = None
) -> dict[AcctName, FundNum]:
    if not x_bud:
        return {}
    if len(x_bud.accts) == 0:
        return {x_bud.owner_name: x_bud.fund_pool}

    if settle_bud:
        x_bud.settle_bud()
    bud_accts = x_bud.accts.values()
    mandates = {x_acct.acct_name: x_acct._fund_agenda_give for x_acct in bud_accts}
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = set_each_mandate_acct_to_penny_weight(mandates, x_bud.penny)
    if mandate_sum != x_bud.fund_pool:
        mandates = allot_scale(mandates, x_bud.fund_pool, x_bud.fund_coin)
    return mandates


def set_each_mandate_acct_to_penny_weight(
    mandates: dict[AcctName, FundNum], penny: FundNum
) -> dict[AcctName, FundNum]:
    acct_names = set(mandates.keys())
    for acct_name in acct_names:
        mandates[acct_name] = penny
    return mandates


def get_acct_agenda_net_ledger(
    x_bud: BudUnit, settle_bud: bool = None
) -> dict[AcctName, FundNum]:
    if settle_bud:
        x_bud.settle_bud()

    x_dict = {}
    for x_acct in x_bud.accts.values():
        settle_net = get_net(x_acct._fund_agenda_give, x_acct._fund_agenda_take)
        if settle_net != 0:
            x_dict[x_acct.acct_name] = settle_net
    return x_dict


def get_credit_ledger(x_bud: BudUnit) -> dict[AcctUnit, RespectNum]:
    credit_ledger, debtit_ledger = x_bud.get_credit_ledger_debtit_ledger()
    return credit_ledger


def get_bud_root_facts_dict(x_bud: BudUnit) -> dict[WayStr, dict[str,]]:
    return x_bud.get_factunits_dict()


def set_factunits_to_bud(x_bud: BudUnit, x_facts_dict: dict[WayStr, dict]):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_rcontexts = set(x_bud.get_missing_fact_rcontexts().keys())
    not_missing_fact_rcontexts = set(x_bud.get_factunits_dict().keys())
    bud_fact_rcontexts = not_missing_fact_rcontexts.union(missing_fact_rcontexts)
    for factunit in factunits_dict.values():
        if factunit.fcontext in bud_fact_rcontexts:
            x_bud.add_fact(
                factunit.fcontext,
                factunit.fbranch,
                factunit.fopen,
                factunit.fnigh,
                create_missing_ideas=True,
            )


def clear_factunits_from_bud(x_bud: BudUnit):
    for fact_rcontext in get_bud_root_facts_dict(x_bud).keys():
        x_bud.del_fact(fact_rcontext)
