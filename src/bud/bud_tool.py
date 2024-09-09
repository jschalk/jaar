from src._road.road import RoadUnit, AcctID, GroupID
from src.bud.acct import AcctUnit
from src.bud.group import MemberShip
from src.bud.bud import BudUnit


def budunit_text() -> str:
    return "budunit"


def bud_acctunit_text() -> str:
    return "bud_acctunit"


def bud_acct_membership_text() -> str:
    return "bud_acct_membership"


def bud_ideaunit_text() -> str:
    return "bud_ideaunit"


def bud_idea_awardlink_text() -> str:
    return "bud_idea_awardlink"


def bud_idea_reasonunit_text() -> str:
    return "bud_idea_reasonunit"


def bud_idea_reason_premiseunit_text() -> str:
    return "bud_idea_reason_premiseunit"


def bud_idea_teamlink_text() -> str:
    return "bud_idea_teamlink"


def bud_idea_healerlink_text() -> str:
    return "bud_idea_healerlink"


def bud_idea_factunit_text() -> str:
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
        and x_bud.get_idea_obj(x_road)._teamunit.teamlink_exists(x_group_id)
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
    if x_category == budunit_text():
        return budunit_exists(x_bud)
    elif x_category == bud_acctunit_text():
        return bud_acctunit_exists(x_bud, required_args)
    elif x_category == bud_acct_membership_text():
        return bud_acct_membership_exists(x_bud, required_args)
    elif x_category == bud_ideaunit_text():
        return bud_ideaunit_exists(x_bud, required_args)
    elif x_category == bud_idea_awardlink_text():
        return bud_idea_awardlink_exists(x_bud, required_args)
    elif x_category == bud_idea_reasonunit_text():
        return bud_idea_reasonunit_exists(x_bud, required_args)
    elif x_category == bud_idea_reason_premiseunit_text():
        return bud_idea_reason_premiseunit_exists(x_bud, required_args)
    elif x_category == bud_idea_teamlink_text():
        return bud_idea_teamlink_exists(x_bud, required_args)
    elif x_category == bud_idea_healerlink_text():
        return bud_idea_healerlink_exists(x_bud, required_args)
    elif x_category == bud_idea_factunit_text():
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


def bud_ideaunit_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    return x_bud.get_idea_obj(x_road)


def bud_idea_awardlink_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    x_group_id = required_args.get("group_id")
    return x_bud.get_idea_obj(x_road).get_awardlink(x_group_id)


def bud_idea_reasonunit_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return x_bud.get_idea_obj(x_road).get_reasonunit(x_base)


def bud_idea_reason_premiseunit_get_obj(
    x_bud: BudUnit, required_args: dict[str, any]
) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    x_need = required_args.get("need")
    return x_bud.get_idea_obj(x_road).get_reasonunit(x_base).get_premise(x_need)


def bud_idea_factunit_get_obj(x_bud: BudUnit, required_args: dict[str, any]) -> bool:
    x_road = required_args.get("road")
    x_base = required_args.get("base")
    return x_bud.get_idea_obj(x_road)._factunits.get(x_base)


def bud_get_obj(x_category: str, x_bud: BudUnit, required_args: dict[str, any]) -> any:
    if x_category == bud_acctunit_text():
        return bud_acctunit_get_obj(x_bud, required_args)
    elif x_category == bud_acct_membership_text():
        return bud_acct_membership_get_obj(x_bud, required_args)
    elif x_category == bud_ideaunit_text():
        return bud_ideaunit_get_obj(x_bud, required_args)
    elif x_category == bud_idea_awardlink_text():
        return bud_idea_awardlink_get_obj(x_bud, required_args)
    elif x_category == bud_idea_reasonunit_text():
        return bud_idea_reasonunit_get_obj(x_bud, required_args)
    elif x_category == bud_idea_reason_premiseunit_text():
        return bud_idea_reason_premiseunit_get_obj(x_bud, required_args)
    elif x_category == bud_idea_factunit_text():
        return bud_idea_factunit_get_obj(x_bud, required_args)


def bud_attr_different(
    x_category: str, x_bud: BudUnit, required_args: dict[str, any]
) -> bool:
    # if x_category == budunit_text():
    #     return budunit_exists(x_bud)
    # elif x_category == bud_acctunit_text():
    #     return bud_acctunit_exists(x_bud, required_args)
    # elif x_category == bud_acct_membership_text():
    #     return bud_acct_membership_exists(x_bud, required_args)
    # elif x_category == bud_ideaunit_text():
    #     return bud_ideaunit_exists(x_bud, required_args)
    # elif x_category == bud_idea_awardlink_text():
    #     return bud_idea_awardlink_exists(x_bud, required_args)
    # elif x_category == bud_idea_reasonunit_text():
    #     return bud_idea_reasonunit_exists(x_bud, required_args)
    # elif x_category == bud_idea_reason_premiseunit_text():
    #     return bud_idea_reason_premiseunit_exists(x_bud, required_args)
    # elif x_category == bud_idea_teamlink_text():
    #     return bud_idea_teamlink_exists(x_bud, required_args)
    # elif x_category == bud_idea_healerlink_text():
    #     return bud_idea_healerlink_exists(x_bud, required_args)
    # elif x_category == bud_idea_factunit_text():
    #     return bud_idea_factunit_exists(x_bud, required_args)
    return True
