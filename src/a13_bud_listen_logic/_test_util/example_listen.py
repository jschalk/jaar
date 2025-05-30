from src.a01_term_logic.way import WayTerm, create_way
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import BudUnit, budunit_shop


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


def clean_str() -> str:
    return "clean"


def run_str() -> str:
    return "run"


def casa_way() -> WayTerm:
    return create_way("accord23", casa_str())


def cook_way() -> WayTerm:
    return create_way(casa_way(), cook_str())


def eat_way() -> WayTerm:
    return create_way(casa_way(), eat_str())


def hungry_way() -> WayTerm:
    return create_way(eat_way(), hungry_str())


def full_way() -> WayTerm:
    return create_way(eat_way(), full_str())


def clean_way() -> WayTerm:
    return create_way(casa_way(), clean_str())


def run_way() -> WayTerm:
    return create_way(casa_way(), run_str())


def get_example_zia_speaker() -> BudUnit:
    zia_str = "Zia"
    a23_str = "accord23"
    zia_speaker = budunit_shop(zia_str, a23_str)
    zia_speaker.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_speaker.set_concept(conceptunit_shop(hungry_str()), eat_way())
    zia_speaker.set_concept(conceptunit_shop(full_str()), eat_way())
    yao_str = "Yao"
    zia_speaker.add_acctunit(yao_str, debtit_belief=12)
    cook_conceptunit = zia_speaker.get_concept_obj(cook_way())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    zia_speaker.edit_concept_attr(
        cook_way(), reason_rcontext=eat_way(), reason_premise=hungry_way()
    )
    zia_speaker.add_fact(eat_way(), full_way())
    zia_speaker.set_acct_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> BudUnit:
    bob_str = "Bob"
    a23_str = "accord23"
    bob_speaker = budunit_shop(bob_str, a23_str)
    bob_speaker.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    bob_speaker.set_concept(conceptunit_shop(hungry_str()), eat_way())
    bob_speaker.set_concept(conceptunit_shop(full_str()), eat_way())
    yao_str = "Yao"
    bob_speaker.add_acctunit(yao_str, debtit_belief=12)
    cook_conceptunit = bob_speaker.get_concept_obj(cook_way())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    bob_speaker.edit_concept_attr(
        cook_way(), reason_rcontext=eat_way(), reason_premise=hungry_way()
    )
    bob_speaker.add_fact(eat_way(), hungry_way())
    bob_speaker.set_acct_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> BudUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    a23_str = "accord23"
    yao_speaker = budunit_shop(yao_str, a23_str)
    yao_speaker.add_acctunit(yao_str, debtit_belief=12)
    yao_speaker.add_acctunit(zia_str, debtit_belief=36)
    yao_speaker.add_acctunit(bob_str, debtit_belief=48)
    yao_speaker.set_acct_respect(100)
    yao_speaker.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    yao_speaker.set_concept(conceptunit_shop(hungry_str()), eat_way())
    yao_speaker.set_concept(conceptunit_shop(full_str()), eat_way())
    cook_conceptunit = yao_speaker.get_concept_obj(cook_way())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_speaker.edit_concept_attr(
        cook_way(), reason_rcontext=eat_way(), reason_premise=hungry_way()
    )
    yao_speaker.add_fact(eat_way(), hungry_way())
    return yao_speaker


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    clean_way = create_way(casa_way, "clean")
    return factunit_shop(casa_way, clean_way)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    dirty_way = create_way(casa_way, "dirty")
    return factunit_shop(casa_way, dirty_way)


def example_casa_grimy_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    grimy_way = create_way(casa_way, "grimy")
    return factunit_shop(casa_way, grimy_way)


def example_sky_blue_factunit() -> FactUnit:
    a23_str = "accord23"
    sky_way = create_way(a23_str, "sky color")
    blue_way = create_way(sky_way, "blue")
    return factunit_shop(sky_way, blue_way)
