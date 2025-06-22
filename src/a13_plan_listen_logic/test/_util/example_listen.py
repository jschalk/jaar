from src.a01_term_logic.rope import RopeTerm, create_rope
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import PlanUnit, planunit_shop


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


def casa_rope() -> RopeTerm:
    return create_rope("accord23", casa_str())


def cook_rope() -> RopeTerm:
    return create_rope(casa_rope(), cook_str())


def eat_rope() -> RopeTerm:
    return create_rope(casa_rope(), eat_str())


def hungry_rope() -> RopeTerm:
    return create_rope(eat_rope(), hungry_str())


def full_rope() -> RopeTerm:
    return create_rope(eat_rope(), full_str())


def clean_rope() -> RopeTerm:
    return create_rope(casa_rope(), clean_str())


def run_rope() -> RopeTerm:
    return create_rope(casa_rope(), run_str())


def get_example_zia_speaker() -> PlanUnit:
    zia_str = "Zia"
    a23_str = "accord23"
    zia_speaker = planunit_shop(zia_str, a23_str)
    zia_speaker.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_speaker.set_concept(conceptunit_shop(hungry_str()), eat_rope())
    zia_speaker.set_concept(conceptunit_shop(full_str()), eat_rope())
    yao_str = "Yao"
    zia_speaker.add_acctunit(yao_str, acct_debt_points=12)
    cook_conceptunit = zia_speaker.get_concept_obj(cook_rope())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    zia_speaker.edit_concept_attr(
        cook_rope(), reason_rcontext=eat_rope(), reason_premise=hungry_rope()
    )
    zia_speaker.add_fact(eat_rope(), full_rope())
    zia_speaker.set_acct_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> PlanUnit:
    bob_str = "Bob"
    a23_str = "accord23"
    bob_speaker = planunit_shop(bob_str, a23_str)
    bob_speaker.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    bob_speaker.set_concept(conceptunit_shop(hungry_str()), eat_rope())
    bob_speaker.set_concept(conceptunit_shop(full_str()), eat_rope())
    yao_str = "Yao"
    bob_speaker.add_acctunit(yao_str, acct_debt_points=12)
    cook_conceptunit = bob_speaker.get_concept_obj(cook_rope())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    bob_speaker.edit_concept_attr(
        cook_rope(), reason_rcontext=eat_rope(), reason_premise=hungry_rope()
    )
    bob_speaker.add_fact(eat_rope(), hungry_rope())
    bob_speaker.set_acct_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> PlanUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    a23_str = "accord23"
    yao_speaker = planunit_shop(yao_str, a23_str)
    yao_speaker.add_acctunit(yao_str, acct_debt_points=12)
    yao_speaker.add_acctunit(zia_str, acct_debt_points=36)
    yao_speaker.add_acctunit(bob_str, acct_debt_points=48)
    yao_speaker.set_acct_respect(100)
    yao_speaker.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    yao_speaker.set_concept(conceptunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_concept(conceptunit_shop(full_str()), eat_rope())
    cook_conceptunit = yao_speaker.get_concept_obj(cook_rope())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_speaker.edit_concept_attr(
        cook_rope(), reason_rcontext=eat_rope(), reason_premise=hungry_rope()
    )
    yao_speaker.add_fact(eat_rope(), hungry_rope())
    return yao_speaker


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    return factunit_shop(casa_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    dirty_rope = create_rope(casa_rope, "dirty")
    return factunit_shop(casa_rope, dirty_rope)


def example_casa_grimy_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_rope = create_rope(a23_str, "casa")
    grimy_rope = create_rope(casa_rope, "grimy")
    return factunit_shop(casa_rope, grimy_rope)


def example_sky_blue_factunit() -> FactUnit:
    a23_str = "accord23"
    sky_rope = create_rope(a23_str, "sky color")
    blue_rope = create_rope(sky_rope, "blue")
    return factunit_shop(sky_rope, blue_rope)
