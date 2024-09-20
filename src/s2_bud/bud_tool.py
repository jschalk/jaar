from src.s0_instrument.python_tool import create_csv
from src.s1_road.road import FiscalID, OwnerID
from src.s2_bud.acct import AcctUnit
from src.s2_bud.group import MemberShip, AwardLink
from src.s2_bud.idea import IdeaUnit
from src.s2_bud.reason_idea import ReasonUnit, FactUnit, PremiseUnit
from src.s2_bud.bud import BudUnit
from dataclasses import dataclass


def budunit_str() -> str:
    return "budunit"


def bud_acctunit_str() -> str:
    return "bud_acctunit"


def bud_acct_membership_str() -> str:
    return "bud_acct_membership"


def bud_ideaunit_str() -> str:
    return "bud_ideaunit"


def bud_idea_awardlink_str() -> str:
    return "bud_idea_awardlink"


def bud_idea_reasonunit_str() -> str:
    return "bud_idea_reasonunit"


def bud_idea_reason_premiseunit_str() -> str:
    return "bud_idea_reason_premiseunit"


def bud_idea_teamlink_str() -> str:
    return "bud_idea_teamlink"


def bud_idea_healerlink_str() -> str:
    return "bud_idea_healerlink"


def bud_idea_factunit_str() -> str:
    return "bud_idea_factunit"


def budunit_exists(x_bud: BudUnit) -> bool:
    return x_bud is not None


def bud_acctunit_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_acct_id = required_args.get("acct_id")
    return False if x_bud is None else x_bud.acct_exists(x_acct_id)


def bud_acct_membership_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_acct_id = required_args.get("acct_id")
    x_group_id = required_args.get("group_id")
    return bool(
        bud_acctunit_exists(x_bud, required_args)
        and x_bud.get_acct(x_acct_id).membership_exists(x_group_id)
    )


def bud_ideaunit_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    return False if x_bud is None else bool(x_bud.idea_exists(x_road))


def bud_idea_awardlink_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_group_id = required_args.get("group_id")
    x_road = required_args.get("road")
    return bool(
        bud_ideaunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).awardlink_exists(x_group_id)
    )


def bud_idea_reasonunit_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return bool(
        bud_ideaunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).reasonunit_exists(x_base)
    )


def bud_idea_reason_premiseunit_exists(
    x_bud: BudUnit, required_args: dict[str, any]
) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    x_need = required_args.get("need")
    return bool(
        bud_idea_reasonunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).get_reasonunit(x_base).premise_exists(x_need)
    )


def bud_idea_teamlink_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_group_id = required_args.get("group_id")
    x_road = required_args.get("road")
    return bool(
        bud_ideaunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).teamunit.teamlink_exists(x_group_id)
    )


def bud_idea_healerlink_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_healer_id = required_args.get("healer_id")
    x_road = required_args.get("road")
    return bool(
        bud_ideaunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).healerlink.healer_id_exists(x_healer_id)
    )


def bud_idea_factunit_exists(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return bool(
        bud_ideaunit_exists(x_bud, required_args)
        and x_bud.get_idea_obj(x_road).factunit_exists(x_base)
    )


def bud_attr_exists(
    x_category: str, x_bud: BudUnit, required_args: dict[str, any]
) -> bool:
    if x_category == budunit_str():
        return budunit_exists(x_bud)
    elif x_category == bud_acctunit_str():
        return bud_acctunit_exists(x_bud, required_args)
    elif x_category == bud_acct_membership_str():
        return bud_acct_membership_exists(x_bud, required_args)
    elif x_category == bud_ideaunit_str():
        return bud_ideaunit_exists(x_bud, required_args)
    elif x_category == bud_idea_awardlink_str():
        return bud_idea_awardlink_exists(x_bud, required_args)
    elif x_category == bud_idea_reasonunit_str():
        return bud_idea_reasonunit_exists(x_bud, required_args)
    elif x_category == bud_idea_reason_premiseunit_str():
        return bud_idea_reason_premiseunit_exists(x_bud, required_args)
    elif x_category == bud_idea_teamlink_str():
        return bud_idea_teamlink_exists(x_bud, required_args)
    elif x_category == bud_idea_healerlink_str():
        return bud_idea_healerlink_exists(x_bud, required_args)
    elif x_category == bud_idea_factunit_str():
        return bud_idea_factunit_exists(x_bud, required_args)
    return True


def bud_acctunit_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> AcctUnit:
    return x_bud.get_acct(required_args.get("acct_id"))


def bud_acct_membership_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> MemberShip:
    x_acct_id = required_args.get("acct_id")
    x_group_id = required_args.get("group_id")
    return x_bud.get_acct(x_acct_id).get_membership(x_group_id)


def bud_ideaunit_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> IdeaUnit:
    x_road = required_args.get("road")
    return x_bud.get_idea_obj(x_road)


def bud_idea_awardlink_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> AwardLink:
    x_road = required_args.get("road")
    x_group_id = required_args.get("group_id")
    return x_bud.get_idea_obj(x_road).get_awardlink(x_group_id)


def bud_idea_reasonunit_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> ReasonUnit:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return x_bud.get_idea_obj(x_road).get_reasonunit(x_base)


def bud_idea_reason_premiseunit_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> PremiseUnit:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    x_need = required_args.get("need")
    return x_bud.get_idea_obj(x_road).get_reasonunit(x_base).get_premise(x_need)


def bud_idea_factunit_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> FactUnit:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return x_bud.get_idea_obj(x_road).factunits.get(x_base)


def bud_get_obj(x_category: str, x_bud: BudUnit, required_args: dict[str, any]) -> any:
    if x_category == budunit_str():
        return x_bud

    x_categorys = {
        bud_acctunit_str(): bud_acctunit_get_obj,
        bud_acct_membership_str(): bud_acct_membership_get_obj,
        bud_ideaunit_str(): bud_ideaunit_get_obj,
        bud_idea_awardlink_str(): bud_idea_awardlink_get_obj,
        bud_idea_reasonunit_str(): bud_idea_reasonunit_get_obj,
        bud_idea_reason_premiseunit_str(): bud_idea_reason_premiseunit_get_obj,
        bud_idea_factunit_str(): bud_idea_factunit_get_obj,
    }
    if x_func := x_categorys.get(x_category):
        return x_func(x_bud, required_args)


@dataclass
class BudEvent:
    fiscal_id: FiscalID = None
    owner_id: OwnerID = None
    timestamp: int = None
    _bud: BudUnit = None
    _money_magnitude: int = None
    _money_desc: str = None


def budevent_shop(fiscal_id: FiscalID, owner_id: OwnerID) -> BudEvent:
    return BudEvent(fiscal_id=fiscal_id, owner_id=owner_id)


def get_bud_outlay_array(x_bud: BudUnit) -> list[list]:
    x_list = []
    for x_acct in x_bud._accts.values():
        x_list.append([x_acct.acct_id, x_acct._fund_take, x_acct._fund_give])
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_bud_outlay_csv(x_bud: BudUnit) -> str:
    x_outlay_array = get_bud_outlay_array(x_bud)
    x_headers = ["acct_id", "fund_take", "fund_give"]
    return create_csv(x_headers, x_outlay_array)
