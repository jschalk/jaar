from src.f00_instrument.dict_toolbox import create_csv
from src.f01_road.finance import FundNum, get_net
from src.f01_road.road import AcctID
from src.f02_bud.acct import AcctUnit
from src.f02_bud.group import MemberShip, AwardLink
from src.f02_bud.item import ItemUnit
from src.f02_bud.reason_item import ReasonUnit, FactUnit, PremiseUnit
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
    x_acct_id = jkeys.get("acct_id")
    return False if x_bud is None else x_bud.acct_exists(x_acct_id)


def bud_acct_membership_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_acct_id = jkeys.get("acct_id")
    x_group_id = jkeys.get("group_id")
    return bool(
        bud_acctunit_exists(x_bud, jkeys)
        and x_bud.get_acct(x_acct_id).membership_exists(x_group_id)
    )


def bud_itemunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_road = jkeys.get("road")
    return False if x_bud is None else bool(x_bud.item_exists(x_road))


def bud_item_awardlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_id = jkeys.get("awardee_id")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).awardlink_exists(x_awardee_id)
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
    x_team_id = jkeys.get("team_id")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).teamunit.teamlink_exists(x_team_id)
    )


def bud_item_healerlink_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_healer_id = jkeys.get("healer_id")
    x_road = jkeys.get("road")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).healerlink.healer_id_exists(x_healer_id)
    )


def bud_item_factunit_exists(x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    x_road = jkeys.get("road")
    x_base = jkeys.get("base")
    return bool(
        bud_itemunit_exists(x_bud, jkeys)
        and x_bud.get_item_obj(x_road).factunit_exists(x_base)
    )


def bud_attr_exists(x_category: str, x_bud: BudUnit, jkeys: dict[str, any]) -> bool:
    if x_category == budunit_str():
        return budunit_exists(x_bud)
    elif x_category == bud_acctunit_str():
        return bud_acctunit_exists(x_bud, jkeys)
    elif x_category == bud_acct_membership_str():
        return bud_acct_membership_exists(x_bud, jkeys)
    elif x_category == bud_itemunit_str():
        return bud_itemunit_exists(x_bud, jkeys)
    elif x_category == bud_item_awardlink_str():
        return bud_item_awardlink_exists(x_bud, jkeys)
    elif x_category == bud_item_reasonunit_str():
        return bud_item_reasonunit_exists(x_bud, jkeys)
    elif x_category == bud_item_reason_premiseunit_str():
        return bud_item_reason_premiseunit_exists(x_bud, jkeys)
    elif x_category == bud_item_teamlink_str():
        return bud_item_teamlink_exists(x_bud, jkeys)
    elif x_category == bud_item_healerlink_str():
        return bud_item_healerlink_exists(x_bud, jkeys)
    elif x_category == bud_item_factunit_str():
        return bud_item_factunit_exists(x_bud, jkeys)
    return True


def bud_acctunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AcctUnit:
    return x_bud.get_acct(jkeys.get("acct_id"))


def bud_acct_membership_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> MemberShip:
    x_acct_id = jkeys.get("acct_id")
    x_group_id = jkeys.get("group_id")
    return x_bud.get_acct(x_acct_id).get_membership(x_group_id)


def bud_itemunit_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> ItemUnit:
    x_road = jkeys.get("road")
    return x_bud.get_item_obj(x_road)


def bud_item_awardlink_get_obj(x_bud: BudUnit, jkeys: dict[str, any]) -> AwardLink:
    x_road = jkeys.get("road")
    x_awardee_id = jkeys.get("awardee_id")
    return x_bud.get_item_obj(x_road).get_awardlink(x_awardee_id)


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


def bud_get_obj(x_category: str, x_bud: BudUnit, jkeys: dict[str, any]) -> any:
    if x_category == budunit_str():
        return x_bud

    x_categorys = {
        bud_acctunit_str(): bud_acctunit_get_obj,
        bud_acct_membership_str(): bud_acct_membership_get_obj,
        bud_itemunit_str(): bud_itemunit_get_obj,
        bud_item_awardlink_str(): bud_item_awardlink_get_obj,
        bud_item_reasonunit_str(): bud_item_reasonunit_get_obj,
        bud_item_reason_premiseunit_str(): bud_item_reason_premiseunit_get_obj,
        bud_item_factunit_str(): bud_item_factunit_get_obj,
    }
    if x_func := x_categorys.get(x_category):
        return x_func(x_bud, jkeys)


def get_bud_purview_array(x_bud: BudUnit, settle_bud: bool = None) -> list[list]:
    if settle_bud:
        x_bud.settle_bud()

    x_list = [
        [x_acct.acct_id, x_acct._fund_take, x_acct._fund_give]
        for x_acct in x_bud._accts.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_bud_purview_csv(x_bud: BudUnit, settle_bud: bool = None) -> str:
    x_purview_array = get_bud_purview_array(x_bud, settle_bud)
    x_headers = ["acct_id", "fund_take", "fund_give"]
    return create_csv(x_headers, x_purview_array)


def get_bud_settle_acct_net_dict(
    x_bud: BudUnit, settle_bud: bool = None
) -> dict[AcctID, FundNum]:
    if settle_bud:
        x_bud.settle_bud()

    x_dict = {}
    for x_acct in x_bud._accts.values():
        settle_net = get_net(x_acct._fund_give, x_acct._fund_take)
        if settle_net != 0:
            x_dict[x_acct.acct_id] = settle_net
    return x_dict
