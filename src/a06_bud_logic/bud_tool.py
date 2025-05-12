from src.a00_data_toolbox.dict_toolbox import create_csv
from src.a02_finance_logic.allot import allot_scale
from src.a02_finance_logic.finance_config import FundNum, get_net, RespectNum
from src.a01_way_logic.way import AcctName, FiscTag, WayUnit
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import MemberShip, AwardLink
from src.a05_item_logic.item import ItemUnit
from src.a04_reason_logic.reason_item import (
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
    x_group_label = jkeys.get("group_label")
    return bool(
        bud_acctunit_exists(x_bud, jkeys)
        and x_bud.get_acct(x_acct_name).membership_exists(x_group_label)
    )


def bud_itemunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("item_way")
    return False if x_bud is None else bool(x_bud.item_exists(x_way))


def bud_item_awardlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_label = jkeys.get("awardee_label")
    x_way = jkeys.get("item_way")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).awardlink_exists(x_awardee_label)
    )


def bud_item_reasonunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("item_way")
    x_base = jkeys.get("base")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).reasonunit_exists(x_base)
    )


def bud_item_reason_premiseunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("item_way")
    x_base = jkeys.get("base")
    x_need = jkeys.get("need")
    return bool(
        bud_item_reasonunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).get_reasonunit(x_base).premise_exists(x_need)
    )


def bud_item_teamlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_team_label = jkeys.get("team_label")
    x_way = jkeys.get("item_way")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).teamunit.teamlink_exists(x_team_label)
    )


def bud_item_healerlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_way = jkeys.get("item_way")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).healerlink.healer_name_exists(x_healer_name)
    )


def bud_item_factunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_way = jkeys.get("item_way")
    x_fbase = jkeys.get("fbase")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_way).factunit_exists(x_fbase)
    )


def bud_attr_exists(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == "bud_acct_membership":
        return bud_acct_membership_exists(x_bud, jkeys)
    elif x_dimen == "bud_acctunit":
        return bud_acctunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_awardlink":
        return bud_item_awardlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_factunit":
        return bud_item_factunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_healerlink":
        return bud_item_healerlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_reason_premiseunit":
        return bud_item_reason_premiseunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_reasonunit":
        return bud_item_reasonunit_exists(x_bud, jkeys)
    elif x_dimen == "bud_item_teamlink":
        return bud_item_teamlink_exists(x_bud, jkeys)
    elif x_dimen == "bud_itemunit":
        return bud_itemunit_exists(x_bud, jkeys)
    elif x_dimen == "budunit":
        return budunit_exists(x_bud)
    return True


def bud_acctunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_bud.get_acct(jkeys.get("acct_name"))


def bud_acct_membership_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> MemberShip:
    x_acct_name = jkeys.get("acct_name")
    x_group_label = jkeys.get("group_label")
    return x_bud.get_acct(x_acct_name).get_membership(x_group_label)


def bud_itemunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ItemUnit:
    x_way = jkeys.get("item_way")
    return x_bud.get_item_obj(x_way)


def bud_item_awardlink_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AwardLink:
    x_way = jkeys.get("item_way")
    x_awardee_label = jkeys.get("awardee_label")
    return x_bud.get_item_obj(x_way).get_awardlink(x_awardee_label)


def bud_item_reasonunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ReasonUnit:
    x_way = jkeys.get("item_way")
    x_base = jkeys.get("base")
    return x_bud.get_item_obj(x_way).get_reasonunit(x_base)


def bud_item_reason_premiseunit_get_obj(
    x_bud: BudUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_way = jkeys.get("item_way")
    x_base = jkeys.get("base")
    x_need = jkeys.get("need")
    return x_bud.get_item_obj(x_way).get_reasonunit(x_base).get_premise(x_need)


def bud_item_factunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> FactUnit:
    x_way = jkeys.get("item_way")
    x_fbase = jkeys.get("fbase")
    print(f"{x_fbase=}")
    print(f"{x_bud.get_item_obj(x_way).factunits=}")
    return x_bud.get_item_obj(x_way).factunits.get(x_fbase)


def bud_get_obj(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "budunit":
        return x_bud

    x_dimens = {
        "bud_acctunit": bud_acctunit_get_obj,
        "bud_acct_membership": bud_acct_membership_get_obj,
        "bud_itemunit": bud_itemunit_get_obj,
        "bud_item_awardlink": bud_item_awardlink_get_obj,
        "bud_item_reasonunit": bud_item_reasonunit_get_obj,
        "bud_item_reason_premiseunit": bud_item_reason_premiseunit_get_obj,
        "bud_item_factunit": bud_item_factunit_get_obj,
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


def get_bud_root_facts_dict(x_bud: BudUnit) -> dict[WayUnit, dict[str,]]:
    return x_bud.get_factunits_dict()


def set_factunits_to_bud(x_bud: BudUnit, x_facts_dict: dict[WayUnit, dict]):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_bases = set(x_bud.get_missing_fact_bases().keys())
    not_missing_fact_bases = set(x_bud.get_factunits_dict().keys())
    bud_fact_bases = not_missing_fact_bases.union(missing_fact_bases)
    for factunit in factunits_dict.values():
        if factunit.fbase in bud_fact_bases:
            x_bud.add_fact(
                factunit.fbase,
                factunit.fneed,
                factunit.fopen,
                factunit.fnigh,
                create_missing_items=True,
            )


def clear_factunits_from_bud(x_bud: BudUnit):
    for fact_base in get_bud_root_facts_dict(x_bud).keys():
        x_bud.del_fact(fact_base)
