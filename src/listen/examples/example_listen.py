from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop, BudUnit


def casa_text() -> str:
    return "casa"


def cook_text() -> str:
    return "cook"


def eat_text() -> str:
    return "eat"


def hungry_text() -> str:
    return "hungry"


def full_text() -> str:
    return "full"


def clean_text():
    return "clean"


def run_text():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), casa_text())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_text())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_text())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_text())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_text())


def clean_road() -> RoadUnit:
    return create_road(casa_road(), clean_text())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_text())


def get_example_zia_speaker() -> BudUnit:
    zia_text = "Zia"
    zia_speaker = budunit_shop(zia_text)
    zia_speaker.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_speaker.set_idea(ideaunit_shop(hungry_text()), eat_road())
    zia_speaker.set_idea(ideaunit_shop(full_text()), eat_road())
    yao_text = "Yao"
    zia_speaker.add_acctunit(yao_text, debtit_score=12)
    cook_ideaunit = zia_speaker.get_idea_obj(cook_road())
    cook_ideaunit._doerunit.set_grouphold(yao_text)
    zia_speaker.edit_idea_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    zia_speaker.set_fact(eat_road(), full_road())
    zia_speaker.set_acct_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> BudUnit:
    bob_text = "Bob"
    bob_speaker = budunit_shop(bob_text)
    bob_speaker.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    bob_speaker.set_idea(ideaunit_shop(hungry_text()), eat_road())
    bob_speaker.set_idea(ideaunit_shop(full_text()), eat_road())
    yao_text = "Yao"
    bob_speaker.add_acctunit(yao_text, debtit_score=12)
    cook_ideaunit = bob_speaker.get_idea_obj(cook_road())
    cook_ideaunit._doerunit.set_grouphold(yao_text)
    bob_speaker.edit_idea_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    bob_speaker.set_fact(eat_road(), hungry_road())
    bob_speaker.set_acct_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> BudUnit:
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    yao_speaker = budunit_shop(yao_text)
    yao_speaker.add_acctunit(yao_text, debtit_score=12)
    yao_speaker.add_acctunit(zia_text, debtit_score=36)
    yao_speaker.add_acctunit(bob_text, debtit_score=48)
    yao_speaker.set_acct_respect(100)
    yao_speaker.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.set_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.set_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._doerunit.set_grouphold(yao_text)
    yao_speaker.edit_idea_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    yao_speaker.set_fact(eat_road(), hungry_road())
    return yao_speaker
