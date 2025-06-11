from src.a01_term_logic.way import LabelTerm, WayTerm, create_way
from src.a05_concept_logic.concept import conceptunit_shop, get_default_vow_label
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a12_hub_tools.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_job_file,
    save_gut_file,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_plan_listen_logic._test_util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_plan_listen_logic._test_util.example_listen_hub import get_texas_hubunit
from src.a13_plan_listen_logic.listen import (
    create_vision_file_from_duty_file,
    listen_to_owner_visions,
)


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


def sanitation_str() -> str:
    return "sanitation"


def clean_str() -> str:
    return "clean"


def dirty_str() -> str:
    return "dirty"


def sweep_str() -> str:
    return "sweep"


def run_str() -> str:
    return "run"


def casa_way() -> WayTerm:
    return create_way(get_default_vow_label(), casa_str())


def cook_way() -> WayTerm:
    return create_way(casa_way(), cook_str())


def eat_way() -> WayTerm:
    return create_way(casa_way(), eat_str())


def hungry_way() -> WayTerm:
    return create_way(eat_way(), hungry_str())


def full_way() -> WayTerm:
    return create_way(eat_way(), full_str())


def sanitation_way() -> WayTerm:
    return create_way(casa_way(), sanitation_str())


def clean_way() -> WayTerm:
    return create_way(sanitation_way(), clean_str())


def dirty_way() -> WayTerm:
    return create_way(sanitation_way(), dirty_str())


def sweep_way() -> WayTerm:
    return create_way(casa_way(), sweep_str())


def run_way() -> WayTerm:
    return create_way(casa_way(), run_str())


def get_example_yao_plan() -> PlanUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    yao_speaker = planunit_shop(yao_str, get_default_vow_label())
    yao_speaker.set_concept(conceptunit_shop(run_str()), casa_way())
    yao_speaker.add_acctunit(yao_str, debt_score=10)
    yao_speaker.add_acctunit(zia_str, debt_score=30)
    yao_speaker.add_acctunit(bob_str, debt_score=40)
    yao_speaker.set_acct_respect(80)
    return yao_speaker


def get_example_yao_vision1_speaker() -> PlanUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_concept_obj(run_way())
    yao_speaker.set_acct_respect(40)
    yao_speaker.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    yao_speaker.set_concept(conceptunit_shop(hungry_str()), eat_way())
    yao_speaker.set_concept(conceptunit_shop(full_str()), eat_way())
    cook_conceptunit = yao_speaker.get_concept_obj(cook_way())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_speaker.edit_reason(cook_way(), eat_way(), hungry_way())
    yao_speaker.add_fact(eat_way(), hungry_way())
    return yao_speaker


def get_example_yao_vision2_speaker() -> PlanUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_concept_obj(run_way())
    yao_speaker.set_acct_respect(30)
    yao_speaker.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    yao_speaker.set_concept(conceptunit_shop(hungry_str()), eat_way())
    yao_speaker.set_concept(conceptunit_shop(full_str()), eat_way())
    cook_conceptunit = yao_speaker.get_concept_obj(cook_way())
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_speaker.edit_reason(cook_way(), eat_way(), hungry_way())
    yao_speaker.add_fact(eat_way(), hungry_way())

    yao_speaker.set_concept(conceptunit_shop(sweep_str(), task=True), casa_way())
    yao_speaker.set_concept(conceptunit_shop(dirty_str()), sanitation_way())
    yao_speaker.set_concept(conceptunit_shop(clean_str()), sanitation_way())
    yao_speaker.edit_reason(sweep_way(), sanitation_way(), dirty_way())
    yao_speaker.add_fact(sweep_way(), dirty_way())
    return yao_speaker


def get_example_yao_vision3_speaker() -> PlanUnit:
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_concept_obj(run_way())
    yao_speaker.set_acct_respect(10)
    yao_speaker.set_concept(conceptunit_shop(sweep_str(), task=True), casa_way())
    yao_speaker.set_concept(conceptunit_shop(dirty_str()), sanitation_way())
    yao_speaker.set_concept(conceptunit_shop(clean_str()), sanitation_way())
    yao_speaker.edit_reason(sweep_way(), sanitation_way(), dirty_way())
    yao_speaker.add_fact(sweep_way(), dirty_way())
    return yao_speaker


def get_usa_way() -> WayTerm:
    return create_way(get_default_vow_label(), "USA")


def get_iowa_str() -> LabelTerm:
    return "Iowa"


def get_ohio_str() -> LabelTerm:
    return "Ohio"


def get_utah_str() -> LabelTerm:
    return "Utah"


def get_swim_str() -> LabelTerm:
    return "swim"


def get_location_str() -> LabelTerm:
    return "location"


def get_in_mer_str() -> LabelTerm:
    return "in_mer"


def get_on_land_str() -> LabelTerm:
    return "on_land"


def get_iowa_way() -> WayTerm:
    return create_way(get_usa_way(), get_iowa_str())


def get_ohio_way() -> WayTerm:
    return create_way(get_usa_way(), get_ohio_str())


def get_utah_way() -> WayTerm:
    return create_way(get_usa_way(), get_utah_str())


def get_swim_way() -> WayTerm:
    return create_way(get_default_vow_label(), get_swim_str())


def get_location_way() -> WayTerm:
    return create_way(get_default_vow_label(), get_location_str())


def get_in_mer_way() -> WayTerm:
    return create_way(get_location_way(), get_in_mer_str())


def get_on_land_way() -> WayTerm:
    return create_way(get_location_way(), get_on_land_str())


def get_yao_ohio_hubunit() -> HubUnit:
    yao_plan = get_example_yao_plan()
    return hubunit_shop(
        vow_mstr_dir=env_dir(),
        vow_label=yao_plan.vow_label,
        owner_name=yao_plan.owner_name,
        keep_way=get_ohio_way(),
        # pipeline_gut_job_str(),
    )


def get_yao_iowa_hubunit() -> HubUnit:
    yao_plan = get_example_yao_plan()
    return hubunit_shop(
        vow_mstr_dir=env_dir(),
        vow_label=yao_plan.vow_label,
        owner_name=yao_plan.owner_name,
        keep_way=get_iowa_way(),
        # pipeline_gut_job_str(),
    )


def get_zia_utah_hubunit() -> HubUnit:
    yao_plan = get_example_yao_plan()
    return hubunit_shop(
        vow_mstr_dir=env_dir(),
        vow_label=yao_plan.vow_label,
        owner_name="Zia",
        keep_way=get_utah_way(),
        # pipeline_gut_job_str(),
    )


def get_example_yao_gut_with_3_healers():
    yao_gut = get_example_yao_plan()
    yao_str = yao_gut.get_acct("Yao").acct_name
    bob_str = yao_gut.get_acct("Bob").acct_name
    zia_str = yao_gut.get_acct("Zia").acct_name
    iowa_concept = conceptunit_shop(get_iowa_str(), problem_bool=True)
    ohio_concept = conceptunit_shop(get_ohio_str(), problem_bool=True)
    utah_concept = conceptunit_shop(get_utah_str(), problem_bool=True)
    iowa_concept.healerlink.set_healer_name(get_yao_iowa_hubunit().owner_name)
    ohio_concept.healerlink.set_healer_name(get_yao_ohio_hubunit().owner_name)
    utah_concept.healerlink.set_healer_name(get_zia_utah_hubunit().owner_name)
    yao_gut.set_concept(iowa_concept, get_usa_way())
    yao_gut.set_concept(ohio_concept, get_usa_way())
    yao_gut.set_concept(utah_concept, get_usa_way())

    return yao_gut


def test_listen_to_owner_visions_Pipeline_Scenario1_yao_gut_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao0_gut with 3 debotors of different credit_scores
    # yao_vision1 with 1 chore, fact that doesn't make that chore active
    # yao_vision2 with 2 chores, one is equal fact that makes chore active
    # yao_vision3 with 1 new chore, fact stays with it
    vow_mstr_dir = env_dir()
    vow_label = get_default_vow_label()
    yao_gut0 = get_example_yao_gut_with_3_healers()
    yao_gut0.set_l1_concept(conceptunit_shop(get_location_str()))
    yao_gut0.set_concept(conceptunit_shop(get_in_mer_str()), get_location_way())
    yao_gut0.set_concept(conceptunit_shop(get_on_land_str()), get_location_way())
    yao_gut0.set_l1_concept(conceptunit_shop(get_swim_str(), task=True))
    yao_gut0.edit_reason(get_swim_way(), get_location_way(), get_in_mer_way())
    yao_gut0.add_fact(get_location_way(), get_in_mer_way())
    print(f"{yao_gut0.get_fact(get_location_way())=}")
    yao_gut0.del_concept_obj(run_way())
    assert yao_gut0._keep_dict.get(get_iowa_way())
    assert yao_gut0._keep_dict.get(get_ohio_way())
    assert yao_gut0._keep_dict.get(get_utah_way())
    yao_gut0.settle_plan()
    assert len(yao_gut0._keep_dict) == 3
    # print(f"{yao_gut0._concept_dict.keys()=}")

    yao_str = yao_gut0.owner_name
    yao_vision1 = get_example_yao_vision1_speaker()
    yao_vision2 = get_example_yao_vision2_speaker()
    yao_vision3 = get_example_yao_vision3_speaker()
    yao_iowa_hubunit = get_yao_iowa_hubunit()
    yao_ohio_hubunit = get_yao_ohio_hubunit()
    zia_utah_hubunit = get_zia_utah_hubunit()
    # delete_dir(yao_iowa_hubunit.owners_dir())
    assert gut_file_exists(vow_mstr_dir, vow_label, yao_str) is False
    assert job_file_exists(vow_mstr_dir, vow_label, yao_str) is False
    assert yao_iowa_hubunit.vision_file_exists(yao_str) is False
    assert yao_ohio_hubunit.vision_file_exists(yao_str) is False
    assert zia_utah_hubunit.vision_file_exists(yao_str) is False
    print(f"{yao_gut0.get_fact(get_location_way())=}")
    save_gut_file(env_dir(), yao_gut0)
    # yao_iowa_hubunit.save_vision_plan(yao_vision1)
    # yao_ohio_hubunit.save_vision_plan(yao_vision2)
    # zia_utah_hubunit.save_vision_plan(yao_vision3)
    assert gut_file_exists(vow_mstr_dir, vow_label, yao_str)
    assert yao_iowa_hubunit.vision_file_exists(yao_str) is False
    assert yao_ohio_hubunit.vision_file_exists(yao_str) is False
    assert zia_utah_hubunit.vision_file_exists(yao_str) is False

    # WHEN
    assert job_file_exists(vow_mstr_dir, vow_label, yao_str) is False
    listen_to_owner_visions(yao_iowa_hubunit)
    assert job_file_exists(vow_mstr_dir, vow_label, yao_str)

    yao_job = open_job_file(vow_mstr_dir, vow_label, yao_str)
    yao_job.settle_plan()
    assert yao_job.accts.keys() == yao_gut0.accts.keys()
    assert yao_job.get_acct(yao_str)._irrational_debt_score == 0
    yao_job_accts = yao_job.get_dict().get("accts")
    yao_gut0_accts = yao_gut0.get_dict().get("accts")
    yao_job_bob = yao_job_accts.get("Bob")
    yao_gut0_bob = yao_gut0_accts.get("Bob")
    print(f"{yao_job_bob=}")
    print(f"{yao_gut0_bob=}")
    assert yao_job_bob == yao_gut0_bob
    assert yao_job_accts.keys() == yao_gut0_accts.keys()
    assert yao_job_accts == yao_gut0_accts
    assert len(yao_job.get_dict().get("accts")) == 3
    assert len(yao_job._concept_dict) == 4
    print(f"{yao_job._concept_dict.keys()=}")
    print(f"{yao_job.get_factunits_dict().keys()=}")
    assert yao_job.concept_exists(cook_way()) is False
    assert yao_job.concept_exists(clean_way()) is False
    assert yao_job.concept_exists(run_way()) is False
    assert yao_job.concept_exists(get_swim_way())
    assert yao_job.concept_exists(get_in_mer_way())
    assert yao_job.concept_exists(get_on_land_way()) is False
    assert yao_job.get_fact(get_location_way()) is not None
    assert yao_job.get_fact(get_location_way()).fstate == get_in_mer_way()
    assert len(yao_job.get_agenda_dict()) == 1
    assert len(yao_job.conceptroot.factunits) == 1
    assert yao_job != yao_gut0


def test_create_vision_file_from_duty_file_CreatesEmptyvision(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)
    assert sue_texas_hubunit.vision_file_exists(yao_str) is False

    # WHEN
    create_vision_file_from_duty_file(sue_texas_hubunit, yao_str)

    # ESTABLISH
    assert sue_texas_hubunit.vision_file_exists(yao_str)
    yao_vision = sue_texas_hubunit.get_vision_plan(yao_str)
    assert yao_vision.owner_name is not None
    assert yao_vision.owner_name == yao_str
    assert yao_vision.get_dict() == yao_duty.get_dict()
