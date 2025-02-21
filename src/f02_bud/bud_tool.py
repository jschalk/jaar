from src.f00_instrument.dict_toolbox import create_csv
from src.f01_road.finance import FundNum, get_net, RespectNum
from src.f01_road.road import AcctName, FiscTitle, RoadUnit
from src.f02_bud.acct import AcctUnit
from src.f02_bud.group import MemberShip, AwardLink
from src.f02_bud.item import ItemUnit
from src.f02_bud.reason_item import (
    ReasonUnit,
    FactUnit,
    PremiseUnit,
    factunits_get_from_dict,
)
from src.f02_bud.bud import BudUnit


def budunit_str() -> str:
    return "budunit"


def bud_acctunit_str() -> str:
    return "bud_acctunit"


def bud_acct_membership_str() -> str:
    return "bud_acct_membership"


def bud_itemunit_str() -> str:
    return "bud_itemunit"


def bud_item_awardlink_str() -> str:
    return "bud_item_awardlink"


def bud_item_reasonunit_str() -> str:
    return "bud_item_reasonunit"


def bud_item_reason_premiseunit_str() -> str:
    return "bud_item_reason_premiseunit"


def bud_item_teamlink_str() -> str:
    return "bud_item_teamlink"


def bud_item_healerlink_str() -> str:
    return "bud_item_healerlink"


def bud_item_factunit_str() -> str:
    return "bud_item_factunit"


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
    x_road = jkeys.get("road")
    return False if x_bud is None else bool(x_bud.item_exists(x_road))


def bud_item_awardlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_tag = jkeys.get("awardee_tag")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).awardlink_exists(x_awardee_tag)
    )


def bud_item_reasonunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).reasonunit_exists(x_base)
    )


def bud_item_reason_premiseunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    x_need = jkeys.get("need")
    return bool(
        bud_item_reasonunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).get_reasonunit(x_base).premise_exists(x_need)
    )


def bud_item_teamlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_team_tag = jkeys.get("team_tag")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).teamunit.teamlink_exists(x_team_tag)
    )


def bud_item_healerlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).healerlink.healer_name_exists(x_healer_name)
    )


def bud_item_factunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).factunit_exists(x_base)
    )


def bud_attr_exists(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == budunit_str():
        return budunit_exists(x_bud)
    elif x_dimen == bud_acctunit_str():
        return bud_acctunit_exists(x_bud, jkeys)
    elif x_dimen == bud_acct_membership_str():
        return bud_acct_membership_exists(x_bud, jkeys)
    elif x_dimen == bud_itemunit_str():
        return bud_itemunit_exists(x_bud, jkeys)
    elif x_dimen == bud_item_awardlink_str():
        return bud_item_awardlink_exists(x_bud, jkeys)
    elif x_dimen == bud_item_reasonunit_str():
        return bud_item_reasonunit_exists(x_bud, jkeys)
    elif x_dimen == bud_item_reason_premiseunit_str():
        return bud_item_reason_premiseunit_exists(x_bud, jkeys)
    elif x_dimen == bud_item_teamlink_str():
        return bud_item_teamlink_exists(x_bud, jkeys)
    elif x_dimen == bud_item_healerlink_str():
        return bud_item_healerlink_exists(x_bud, jkeys)
    elif x_dimen == bud_item_factunit_str():
        return bud_item_factunit_exists(x_bud, jkeys)
    return True


def bud_acctunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_bud.get_acct(jkeys.get("acct_name"))


def bud_acct_membership_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> MemberShip:
    x_acct_name = jkeys.get("acct_name")
    x_group_label = jkeys.get("group_label")
    return x_bud.get_acct(x_acct_name).get_membership(x_group_label)


def bud_itemunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ItemUnit:
    x_road = jkeys.get("road")
    return x_bud.get_item_obj(x_road)


def bud_item_awardlink_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AwardLink:
    x_road = jkeys.get("road")
    x_awardee_tag = jkeys.get("awardee_tag")
    return x_bud.get_item_obj(x_road).get_awardlink(x_awardee_tag)


def bud_item_reasonunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ReasonUnit:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    return x_bud.get_item_obj(x_road).get_reasonunit(x_base)


def bud_item_reason_premiseunit_get_obj(
    x_bud: BudUnit, jkeys: dict[str, any]
) -> PremiseUnit:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    x_need = jkeys.get("need")
    return x_bud.get_item_obj(x_road).get_reasonunit(x_base).get_premise(x_need)


def bud_item_factunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> FactUnit:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    return x_bud.get_item_obj(x_road).factunits.get(x_base)


def bud_get_obj(x_dimen: str, x_bud: BudUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == budunit_str():
        return x_bud

    x_dimens = {
        bud_acctunit_str(): bud_acctunit_get_obj,
        bud_acct_membership_str(): bud_acct_membership_get_obj,
        bud_itemunit_str(): bud_itemunit_get_obj,
        bud_item_awardlink_str(): bud_item_awardlink_get_obj,
        bud_item_reasonunit_str(): bud_item_reasonunit_get_obj,
        bud_item_reason_premiseunit_str(): bud_item_reason_premiseunit_get_obj,
        bud_item_factunit_str(): bud_item_factunit_get_obj,
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


def get_acct_agenda_ledger(
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


def get_bud_root_facts_dict(x_bud: BudUnit) -> dict[RoadUnit, dict[str,]]:
    return x_bud.get_factunits_dict()


def set_factunits_to_bud(x_bud: BudUnit, x_facts_dict: dict[RoadUnit, dict]):
    factunits_dict = factunits_get_from_dict(x_facts_dict)
    missing_fact_bases = set(x_bud.get_missing_fact_bases().keys())
    not_missing_fact_bases = set(x_bud.get_factunits_dict().keys())
    bud_fact_bases = not_missing_fact_bases.union(missing_fact_bases)
    for factunit in factunits_dict.values():
        if factunit.base in bud_fact_bases:
            x_bud.add_fact(
                factunit.base,
                factunit.pick,
                factunit.fopen,
                factunit.fnigh,
                create_missing_items=True,
            )
