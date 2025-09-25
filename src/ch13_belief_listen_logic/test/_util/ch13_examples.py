from src.ch02_rope_logic.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch02_rope_logic.term import MomentLabel
from src.ch05_reason_logic.reason import FactUnit, factunit_shop
from src.ch06_plan_logic.plan import get_default_moment_label, planunit_shop
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_pack_logic.pack import PackUnit, packunit_shop
from src.ch12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.ch12_hub_toolbox.test._util.ch12_examples import get_texas_rope
from src.ch13_belief_listen_logic._ref.ch13_keywords import (
    INSERT_str,
    belief_plan_factunit_str,
    belief_planunit_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    parent_rope_str,
    plan_label_str,
    plan_rope_str,
)
from src.ch13_belief_listen_logic.test._util.ch13_env import get_chapter_temp_dir


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


def a23_casa_rope() -> RopeTerm:
    return create_rope("amy23", casa_str())


def a23_cook_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), cook_str())


def a23_eat_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), eat_str())


def a23_hungry_rope() -> RopeTerm:
    return create_rope(a23_eat_rope(), hungry_str())


def a23_full_rope() -> RopeTerm:
    return create_rope(a23_eat_rope(), full_str())


def a23_clean_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), clean_str())


def a23_run_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), run_str())


def get_example_zia_speaker() -> BeliefUnit:
    zia_str = "Zia"
    a23_str = "amy23"
    zia_speaker = beliefunit_shop(zia_str, a23_str)
    zia_speaker.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    zia_speaker.set_plan(planunit_shop(hungry_str()), a23_eat_rope())
    zia_speaker.set_plan(planunit_shop(full_str()), a23_eat_rope())
    yao_str = "Yao"
    zia_speaker.add_voiceunit(yao_str, voice_debt_points=12)
    cook_planunit = zia_speaker.get_plan_obj(a23_cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    zia_speaker.edit_plan_attr(
        a23_cook_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    zia_speaker.add_fact(a23_eat_rope(), a23_full_rope())
    zia_speaker.set_voice_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> BeliefUnit:
    bob_str = "Bob"
    a23_str = "amy23"
    bob_speaker = beliefunit_shop(bob_str, a23_str)
    bob_speaker.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    bob_speaker.set_plan(planunit_shop(hungry_str()), a23_eat_rope())
    bob_speaker.set_plan(planunit_shop(full_str()), a23_eat_rope())
    yao_str = "Yao"
    bob_speaker.add_voiceunit(yao_str, voice_debt_points=12)
    cook_planunit = bob_speaker.get_plan_obj(a23_cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    bob_speaker.edit_plan_attr(
        a23_cook_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    bob_speaker.add_fact(a23_eat_rope(), a23_hungry_rope())
    bob_speaker.set_voice_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> BeliefUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    a23_str = "amy23"
    yao_speaker = beliefunit_shop(yao_str, a23_str)
    yao_speaker.add_voiceunit(yao_str, voice_debt_points=12)
    yao_speaker.add_voiceunit(zia_str, voice_debt_points=36)
    yao_speaker.add_voiceunit(bob_str, voice_debt_points=48)
    yao_speaker.set_voice_respect(100)
    yao_speaker.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    yao_speaker.set_plan(planunit_shop(hungry_str()), a23_eat_rope())
    yao_speaker.set_plan(planunit_shop(full_str()), a23_eat_rope())
    cook_planunit = yao_speaker.get_plan_obj(a23_cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    yao_speaker.edit_plan_attr(
        a23_cook_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    yao_speaker.add_fact(a23_eat_rope(), a23_hungry_rope())
    return yao_speaker


def get_texas_hubunit() -> HubUnit:
    moment_label = get_default_moment_label()
    return hubunit_shop(
        get_chapter_temp_dir(),
        moment_label,
        belief_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_dakota_rope() -> RopeTerm:
    moment_label = get_default_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_rope_from_labels([moment_label, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    moment_label = get_default_moment_label()
    return hubunit_shop(
        get_chapter_temp_dir(),
        moment_label,
        belief_name="Sue",
        keep_rope=get_dakota_rope(),
        # pipeline_duty_vision_str(),
    )


def get_fund_breakdown_belief() -> BeliefUnit:
    sue_belief = beliefunit_shop(belief_name="Sue")

    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    cat_str = "cat status"
    cat_rope = sue_belief.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_belief.set_l1_plan(planunit_shop(casa_str, star=30))
    sue_belief.set_plan(planunit_shop(cat_str, star=30), casa_rope)
    sue_belief.set_plan(planunit_shop(hun_n_str, star=30), cat_rope)
    sue_belief.set_plan(planunit_shop(hun_y_str, star=30), cat_rope)
    sue_belief.set_plan(planunit_shop(clean_str, star=30), casa_rope)
    sue_belief.set_plan(planunit_shop(sweep_str, star=30, pledge=True), clean_rope)
    sue_belief.set_plan(planunit_shop(dish_str, star=30, pledge=True), clean_rope)

    cat_str = "cat have dinner"
    sue_belief.set_l1_plan(planunit_shop(cat_str, star=30, pledge=True))

    # week_str = "weekdays"
    # week_rope = sue_belief.make_l1_rope(week_str)
    # plan_kid_weekdays = planunit_shop(week_str, star=25)
    # sue_belief.set_l1_plan(plan_kid_weekdays)

    # sun_str = "Sunday"
    # mon_str = "Monday"
    # tue_str = "Tuesday"
    # wed_str = "Wednesday"
    # thu_str = "Thursday"
    # fri_str = "Friday"
    # sat_str = "Saturday"
    # plan_grandkidU = planunit_shop(sun_str, star=20)
    # plan_grandkidM = planunit_shop(mon_str, star=20)
    # plan_grandkidT = planunit_shop(tue_str, star=20)
    # plan_grandkidW = planunit_shop(wed_str, star=20)
    # plan_grandkidR = planunit_shop(thu_str, star=30)
    # plan_grandkidF = planunit_shop(fri_str, star=40)
    # plan_grandkidA = planunit_shop(sat_str, star=50)
    # sue_belief.set_plan(plan_grandkidU, week_rope)
    # sue_belief.set_plan(plan_grandkidM, week_rope)
    # sue_belief.set_plan(plan_grandkidT, week_rope)
    # sue_belief.set_plan(plan_grandkidW, week_rope)
    # sue_belief.set_plan(plan_grandkidR, week_rope)
    # sue_belief.set_plan(plan_grandkidF, week_rope)
    # sue_belief.set_plan(plan_grandkidA, week_rope)

    # nation_str = "nation"
    # nation_rope = sue_belief.make_l1_rope(nation_str)
    # plan_kid_nation = planunit_shop(nation_str, star=30)
    # sue_belief.set_l1_plan(plan_kid_nation)

    # usa_str = "USA"
    # usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    # france_str = "France"
    # brazil_str = "Brazil"
    # plan_grandkid_usa = planunit_shop(usa_str, star=50)
    # plan_grandkid_france = planunit_shop(france_str, star=50)
    # plan_grandkid_brazil = planunit_shop(brazil_str, star=50)
    # sue_belief.set_plan(plan_grandkid_france, nation_rope)
    # sue_belief.set_plan(plan_grandkid_brazil, nation_rope)
    # sue_belief.set_plan(plan_grandkid_usa, nation_rope)

    # texas_str = "Texas"
    # oregon_str = "Oregon"
    # plan_grandgrandkid_usa_texas = planunit_shop(texas_str, star=50)
    # plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, star=50)
    # sue_belief.set_plan(plan_grandgrandkid_usa_texas, usa_rope)
    # sue_belief.set_plan(plan_grandgrandkid_usa_oregon, usa_rope)
    return sue_belief
