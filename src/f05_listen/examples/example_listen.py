from src.f01_road.road import RoadUnit, create_road, get_default_cmty_idea
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop, BudUnit


def casa_str() -> str:
    return "casa"


def cook_str() -> str:
    return "cook"


def eat_str() -> str:
    return "eat"


def hungry_str() -> str:
    return "hungry"


def full_str() -> str:
    return "full"


def clean_str():
    return "clean"


def run_str():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_cmty_idea(), casa_str())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_str())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_str())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_str())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_str())


def clean_road() -> RoadUnit:
    return create_road(casa_road(), clean_str())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_str())


def get_example_zia_speaker() -> BudUnit:
    zia_str = "Zia"
    zia_speaker = budunit_shop(zia_str)
    zia_speaker.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_speaker.set_item(itemunit_shop(hungry_str()), eat_road())
    zia_speaker.set_item(itemunit_shop(full_str()), eat_road())
    yao_str = "Yao"
    zia_speaker.add_acctunit(yao_str, debtit_belief=12)
    cook_itemunit = zia_speaker.get_item_obj(cook_road())
    cook_itemunit.teamunit.set_teamlink(yao_str)
    zia_speaker.edit_item_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    zia_speaker.set_fact(eat_road(), full_road())
    zia_speaker.set_acct_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> BudUnit:
    bob_str = "Bob"
    bob_speaker = budunit_shop(bob_str)
    bob_speaker.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    bob_speaker.set_item(itemunit_shop(hungry_str()), eat_road())
    bob_speaker.set_item(itemunit_shop(full_str()), eat_road())
    yao_str = "Yao"
    bob_speaker.add_acctunit(yao_str, debtit_belief=12)
    cook_itemunit = bob_speaker.get_item_obj(cook_road())
    cook_itemunit.teamunit.set_teamlink(yao_str)
    bob_speaker.edit_item_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    bob_speaker.set_fact(eat_road(), hungry_road())
    bob_speaker.set_acct_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> BudUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_acctunit(yao_str, debtit_belief=12)
    yao_speaker.add_acctunit(zia_str, debtit_belief=36)
    yao_speaker.add_acctunit(bob_str, debtit_belief=48)
    yao_speaker.set_acct_respect(100)
    yao_speaker.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    yao_speaker.set_item(itemunit_shop(hungry_str()), eat_road())
    yao_speaker.set_item(itemunit_shop(full_str()), eat_road())
    cook_itemunit = yao_speaker.get_item_obj(cook_road())
    cook_itemunit.teamunit.set_teamlink(yao_str)
    yao_speaker.edit_item_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    yao_speaker.set_fact(eat_road(), hungry_road())
    return yao_speaker
