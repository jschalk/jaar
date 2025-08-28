from src.a01_term_logic.rope import LabelTerm, RopeTerm, create_rope
from src.a05_plan_logic.plan import get_default_moment_label, planunit_shop
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import voices_str
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_job_file,
    save_gut_file,
)
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.keep_tool import save_duty_belief
from src.a13_belief_listen_logic.listen_main import (
    create_vision_file_from_duty_file,
    listen_to_belief_visions,
)
from src.a13_belief_listen_logic.test._util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_belief_listen_logic.test._util.example_listen_hub import get_texas_hubunit


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


def casa_rope() -> RopeTerm:
    return create_rope(get_default_moment_label(), casa_str())


def cook_rope() -> RopeTerm:
    return create_rope(casa_rope(), cook_str())


def eat_rope() -> RopeTerm:
    return create_rope(casa_rope(), eat_str())


def hungry_rope() -> RopeTerm:
    return create_rope(eat_rope(), hungry_str())


def full_rope() -> RopeTerm:
    return create_rope(eat_rope(), full_str())


def sanitation_rope() -> RopeTerm:
    return create_rope(casa_rope(), sanitation_str())


def clean_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), clean_str())


def dirty_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), dirty_str())


def sweep_rope() -> RopeTerm:
    return create_rope(casa_rope(), sweep_str())


def run_rope() -> RopeTerm:
    return create_rope(casa_rope(), run_str())


def get_example_yao_belief() -> BeliefUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    yao_speaker = beliefunit_shop(yao_str, get_default_moment_label())
    yao_speaker.set_plan(planunit_shop(run_str()), casa_rope())
    yao_speaker.add_voiceunit(yao_str, voice_debt_points=10)
    yao_speaker.add_voiceunit(zia_str, voice_debt_points=30)
    yao_speaker.add_voiceunit(bob_str, voice_debt_points=40)
    yao_speaker.set_voice_respect(80)
    return yao_speaker


def get_example_yao_vision1_speaker() -> BeliefUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_belief()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_voice_respect(40)
    yao_speaker.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_plan(planunit_shop(full_str()), eat_rope())
    cook_planunit = yao_speaker.get_plan_obj(cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    yao_speaker.edit_reason(cook_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())
    return yao_speaker


def get_example_yao_vision2_speaker() -> BeliefUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_belief()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_voice_respect(30)
    yao_speaker.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_plan(planunit_shop(full_str()), eat_rope())
    cook_planunit = yao_speaker.get_plan_obj(cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    yao_speaker.edit_reason(cook_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())

    yao_speaker.set_plan(planunit_shop(sweep_str(), task=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan(planunit_shop(clean_str()), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_example_yao_vision3_speaker() -> BeliefUnit:
    yao_speaker = get_example_yao_belief()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_voice_respect(10)
    yao_speaker.set_plan(planunit_shop(sweep_str(), task=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan(planunit_shop(clean_str()), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_usa_rope() -> RopeTerm:
    return create_rope(get_default_moment_label(), "USA")


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


def get_iowa_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_iowa_str())


def get_ohio_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_ohio_str())


def get_utah_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_utah_str())


def get_swim_rope() -> RopeTerm:
    return create_rope(get_default_moment_label(), get_swim_str())


def get_location_rope() -> RopeTerm:
    return create_rope(get_default_moment_label(), get_location_str())


def get_in_mer_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_in_mer_str())


def get_on_land_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_on_land_str())


def get_yao_ohio_hubunit() -> HubUnit:
    yao_belief = get_example_yao_belief()
    return hubunit_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name=yao_belief.belief_name,
        keep_rope=get_ohio_rope(),
        # pipeline_gut_job_str(),
    )


def get_yao_iowa_hubunit() -> HubUnit:
    yao_belief = get_example_yao_belief()
    return hubunit_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name=yao_belief.belief_name,
        keep_rope=get_iowa_rope(),
        # pipeline_gut_job_str(),
    )


def get_zia_utah_hubunit() -> HubUnit:
    yao_belief = get_example_yao_belief()
    return hubunit_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name="Zia",
        keep_rope=get_utah_rope(),
        # pipeline_gut_job_str(),
    )


def get_example_yao_gut_with_3_healers():
    yao_gut = get_example_yao_belief()
    yao_str = yao_gut.get_voice("Yao").voice_name
    bob_str = yao_gut.get_voice("Bob").voice_name
    zia_str = yao_gut.get_voice("Zia").voice_name
    iowa_plan = planunit_shop(get_iowa_str(), problem_bool=True)
    ohio_plan = planunit_shop(get_ohio_str(), problem_bool=True)
    utah_plan = planunit_shop(get_utah_str(), problem_bool=True)
    iowa_plan.healerunit.set_healer_name(get_yao_iowa_hubunit().belief_name)
    ohio_plan.healerunit.set_healer_name(get_yao_ohio_hubunit().belief_name)
    utah_plan.healerunit.set_healer_name(get_zia_utah_hubunit().belief_name)
    yao_gut.set_plan(iowa_plan, get_usa_rope())
    yao_gut.set_plan(ohio_plan, get_usa_rope())
    yao_gut.set_plan(utah_plan, get_usa_rope())

    return yao_gut


def test_listen_to_belief_visions_Pipeline_Scenario1_yao_gut_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    # yao0_gut with 3 debotors of different voice_cred_pointss
    # yao_vision1 with 1 chore, fact that doesn't make that chore active
    # yao_vision2 with 2 chores, one is equal fact that makes chore active
    # yao_vision3 with 1 new chore, fact stays with it
    moment_mstr_dir = env_dir()
    moment_label = get_default_moment_label()
    yao_gut0 = get_example_yao_gut_with_3_healers()
    yao_gut0.set_l1_plan(planunit_shop(get_location_str()))
    yao_gut0.set_plan(planunit_shop(get_in_mer_str()), get_location_rope())
    yao_gut0.set_plan(planunit_shop(get_on_land_str()), get_location_rope())
    yao_gut0.set_l1_plan(planunit_shop(get_swim_str(), task=True))
    yao_gut0.edit_reason(get_swim_rope(), get_location_rope(), get_in_mer_rope())
    yao_gut0.add_fact(get_location_rope(), get_in_mer_rope())
    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    yao_gut0.del_plan_obj(run_rope())
    assert yao_gut0._keep_dict.get(get_iowa_rope())
    assert yao_gut0._keep_dict.get(get_ohio_rope())
    assert yao_gut0._keep_dict.get(get_utah_rope())
    yao_gut0.cash_out()
    assert len(yao_gut0._keep_dict) == 3
    # print(f"{yao_gut0._plan_dict.keys()=}")

    yao_str = yao_gut0.belief_name
    yao_vision1 = get_example_yao_vision1_speaker()
    yao_vision2 = get_example_yao_vision2_speaker()
    yao_vision3 = get_example_yao_vision3_speaker()
    yao_iowa_hubunit = get_yao_iowa_hubunit()
    yao_ohio_hubunit = get_yao_ohio_hubunit()
    zia_utah_hubunit = get_zia_utah_hubunit()
    # delete_dir(yao_iowa_hubunit.beliefs_dir())
    assert gut_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    assert yao_iowa_hubunit.vision_file_exists(yao_str) is False
    assert yao_ohio_hubunit.vision_file_exists(yao_str) is False
    assert zia_utah_hubunit.vision_file_exists(yao_str) is False
    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    save_gut_file(env_dir(), yao_gut0)
    # yao_iowa_hubunit.save_vision_belief(yao_vision1)
    # yao_ohio_hubunit.save_vision_belief(yao_vision2)
    # zia_utah_hubunit.save_vision_belief(yao_vision3)
    assert gut_file_exists(moment_mstr_dir, moment_label, yao_str)
    assert yao_iowa_hubunit.vision_file_exists(yao_str) is False
    assert yao_ohio_hubunit.vision_file_exists(yao_str) is False
    assert zia_utah_hubunit.vision_file_exists(yao_str) is False

    # WHEN / THEN
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    listen_to_belief_visions(yao_iowa_hubunit)
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str)

    yao_job = open_job_file(moment_mstr_dir, moment_label, yao_str)
    yao_job.cash_out()
    assert yao_job.voices.keys() == yao_gut0.voices.keys()
    assert yao_job.get_voice(yao_str)._irrational_voice_debt_points == 0
    yao_job_voices = yao_job.to_dict().get(voices_str())
    yao_gut0_voices = yao_gut0.to_dict().get(voices_str())
    yao_job_bob = yao_job_voices.get("Bob")
    yao_gut0_bob = yao_gut0_voices.get("Bob")
    print(f"{yao_job_bob=}")
    print(f"{yao_gut0_bob=}")
    assert yao_job_bob == yao_gut0_bob
    assert yao_job_voices.keys() == yao_gut0_voices.keys()
    assert yao_job_voices == yao_gut0_voices
    assert len(yao_job.to_dict().get(voices_str())) == 3
    assert len(yao_job._plan_dict) == 4
    print(f"{yao_job._plan_dict.keys()=}")
    print(f"{yao_job.get_factunits_dict().keys()=}")
    assert yao_job.plan_exists(cook_rope()) is False
    assert yao_job.plan_exists(clean_rope()) is False
    assert yao_job.plan_exists(run_rope()) is False
    assert yao_job.plan_exists(get_swim_rope())
    assert yao_job.plan_exists(get_in_mer_rope())
    assert yao_job.plan_exists(get_on_land_rope()) is False
    assert yao_job.get_fact(get_location_rope()) is not None
    assert yao_job.get_fact(get_location_rope()).fact_state == get_in_mer_rope()
    assert len(yao_job.get_agenda_dict()) == 1
    assert len(yao_job.planroot.factunits) == 1
    assert yao_job != yao_gut0


def test_create_vision_file_from_duty_file_CreatesEmptyvision(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str)
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    assert sue_texas_hubunit.vision_file_exists(yao_str) is False

    # WHEN
    create_vision_file_from_duty_file(sue_texas_hubunit, yao_str)

    # THEN
    assert sue_texas_hubunit.vision_file_exists(yao_str)
    yao_vision = sue_texas_hubunit.get_vision_belief(yao_str)
    assert yao_vision.belief_name is not None
    assert yao_vision.belief_name == yao_str
    assert yao_vision.to_dict() == yao_duty.to_dict()
