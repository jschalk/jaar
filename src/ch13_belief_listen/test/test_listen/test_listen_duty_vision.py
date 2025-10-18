from src.ch02_rope.rope import LabelTerm, RopeTerm, create_rope
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop, planunit_shop
from src.ch10_lesson.lesson_filehandler import (
    LessonFileHandler,
    gut_file_exists,
    lessonfilehandler_shop,
    save_gut_file,
)
from src.ch11_bud.bud_filehandler import job_file_exists, open_job_file
from src.ch13_belief_listen.keep_tool import (
    get_vision_belief,
    save_duty_belief,
    vision_file_exists,
)
from src.ch13_belief_listen.listen_main import (
    create_vision_file_from_duty_file,
    listen_to_belief_visions,
)
from src.ch13_belief_listen.test._util.ch13_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch13_belief_listen.test._util.ch13_examples import (
    casa_str,
    ch13_example_moment_label,
    clean_str,
    cook_str,
    eat_str,
    full_str,
    get_texas_lessonfilehandler,
    get_texas_rope,
    hungry_str,
    run_str,
)
from src.ref.keywords import Ch13Keywords as kw


def sanitation_str() -> str:
    return "sanitation"


def dirty_str() -> str:
    return "dirty"


def sweep_str() -> str:
    return "sweep"


def casa_rope() -> RopeTerm:
    return create_rope(ch13_example_moment_label(), casa_str())


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
    yao_speaker = beliefunit_shop(yao_str, ch13_example_moment_label())
    yao_speaker.set_plan(planunit_shop(run_str()), casa_rope())
    yao_speaker.add_voiceunit(yao_str, voice_debt_lumen=10)
    yao_speaker.add_voiceunit(zia_str, voice_debt_lumen=30)
    yao_speaker.add_voiceunit(bob_str, voice_debt_lumen=40)
    yao_speaker.set_voice_respect(80)
    return yao_speaker


def get_example_yao_vision1_speaker() -> BeliefUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_belief()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_voice_respect(40)
    yao_speaker.set_plan(planunit_shop(cook_str(), pledge=True), casa_rope())
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
    yao_speaker.set_plan(planunit_shop(cook_str(), pledge=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_plan(planunit_shop(full_str()), eat_rope())
    cook_planunit = yao_speaker.get_plan_obj(cook_rope())
    cook_planunit.laborunit.add_party(yao_str)
    yao_speaker.edit_reason(cook_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())

    yao_speaker.set_plan(planunit_shop(sweep_str(), pledge=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan(planunit_shop(clean_str()), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_example_yao_vision3_speaker() -> BeliefUnit:
    yao_speaker = get_example_yao_belief()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_voice_respect(10)
    yao_speaker.set_plan(planunit_shop(sweep_str(), pledge=True), casa_rope())
    yao_speaker.set_plan(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan(planunit_shop(clean_str()), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_usa_rope() -> RopeTerm:
    return create_rope(ch13_example_moment_label(), "USA")


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
    return create_rope(ch13_example_moment_label(), get_swim_str())


def get_location_rope() -> RopeTerm:
    return create_rope(ch13_example_moment_label(), get_location_str())


def get_in_mer_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_in_mer_str())


def get_on_land_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_on_land_str())


def get_yao_ohio_lessonfilehandler() -> LessonFileHandler:
    yao_belief = get_example_yao_belief()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name=yao_belief.belief_name,
    )


def get_yao_iowa_lessonfilehandler() -> LessonFileHandler:
    yao_belief = get_example_yao_belief()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name=yao_belief.belief_name,
    )


def get_zia_utah_lessonfilehandler() -> LessonFileHandler:
    yao_belief = get_example_yao_belief()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_label=yao_belief.moment_label,
        belief_name="Zia",
    )


def get_example_yao_gut_with_3_healers():
    yao_gut = get_example_yao_belief()
    yao_str = yao_gut.get_voice("Yao").voice_name
    bob_str = yao_gut.get_voice("Bob").voice_name
    zia_str = yao_gut.get_voice("Zia").voice_name
    iowa_plan = planunit_shop(get_iowa_str(), problem_bool=True)
    ohio_plan = planunit_shop(get_ohio_str(), problem_bool=True)
    utah_plan = planunit_shop(get_utah_str(), problem_bool=True)
    iowa_plan.healerunit.set_healer_name(get_yao_iowa_lessonfilehandler().belief_name)
    ohio_plan.healerunit.set_healer_name(get_yao_ohio_lessonfilehandler().belief_name)
    utah_plan.healerunit.set_healer_name(get_zia_utah_lessonfilehandler().belief_name)
    yao_gut.set_plan(iowa_plan, get_usa_rope())
    yao_gut.set_plan(ohio_plan, get_usa_rope())
    yao_gut.set_plan(utah_plan, get_usa_rope())

    return yao_gut


def test_listen_to_belief_visions_Pipeline_Scenario1_yao_gut_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    # yao0_gut with 3 debotors of different voice_cred_lumens
    # yao_vision1 with 1 task, fact that doesn't make that task active
    # yao_vision2 with 2 tasks, one is equal fact that makes task active
    # yao_vision3 with 1 new task, fact stays with it
    moment_mstr_dir = env_dir()
    moment_label = ch13_example_moment_label()
    yao_gut0 = get_example_yao_gut_with_3_healers()
    yao_gut0.set_l1_plan(planunit_shop(get_location_str()))
    yao_gut0.set_plan(planunit_shop(get_in_mer_str()), get_location_rope())
    yao_gut0.set_plan(planunit_shop(get_on_land_str()), get_location_rope())
    yao_gut0.set_l1_plan(planunit_shop(get_swim_str(), pledge=True))
    yao_gut0.edit_reason(get_swim_rope(), get_location_rope(), get_in_mer_rope())
    yao_gut0.add_fact(get_location_rope(), get_in_mer_rope())
    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    yao_gut0.del_plan_obj(run_rope())
    assert yao_gut0._keep_dict.get(get_iowa_rope())
    assert yao_gut0._keep_dict.get(get_ohio_rope())
    assert yao_gut0._keep_dict.get(get_utah_rope())
    yao_gut0.cashout()
    assert len(yao_gut0._keep_dict) == 3
    # print(f"{yao_gut0._plan_dict.keys()=}")

    yao_str = yao_gut0.belief_name
    yao_vision1 = get_example_yao_vision1_speaker()
    yao_vision2 = get_example_yao_vision2_speaker()
    yao_vision3 = get_example_yao_vision3_speaker()
    yao_iowa_lessonfilehandler = get_yao_iowa_lessonfilehandler()
    yao_ohio_lessonfilehandler = get_yao_ohio_lessonfilehandler()
    zia_utah_lessonfilehandler = get_zia_utah_lessonfilehandler()
    # delete_dir(yao_iowa_lessonfilehandler.beliefs_dir())
    assert gut_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.belief_name,
            yao_iowa_lessonfilehandler.moment_label,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.belief_name,
            yao_ohio_lessonfilehandler.moment_label,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.belief_name,
            zia_utah_lessonfilehandler.moment_label,
            get_utah_rope(),
            zia_utah_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )

    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    save_gut_file(env_dir(), yao_gut0)
    assert gut_file_exists(moment_mstr_dir, moment_label, yao_str)
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.belief_name,
            yao_iowa_lessonfilehandler.moment_label,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.belief_name,
            yao_ohio_lessonfilehandler.moment_label,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.belief_name,
            zia_utah_lessonfilehandler.moment_label,
            get_utah_rope(),
            zia_utah_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )
    # WHEN / THEN
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str) is False
    listen_to_belief_visions(yao_iowa_lessonfilehandler, get_iowa_rope())
    assert job_file_exists(moment_mstr_dir, moment_label, yao_str)

    yao_job = open_job_file(moment_mstr_dir, moment_label, yao_str)
    yao_job.cashout()
    assert yao_job.voices.keys() == yao_gut0.voices.keys()
    assert yao_job.get_voice(yao_str).irrational_voice_debt_lumen == 0
    yao_job_voices = yao_job.to_dict().get(kw.voices)
    yao_gut0_voices = yao_gut0.to_dict().get(kw.voices)
    yao_job_bob = yao_job_voices.get("Bob")
    yao_gut0_bob = yao_gut0_voices.get("Bob")
    print(f"{yao_job_bob=}")
    print(f"{yao_gut0_bob=}")
    assert yao_job_bob == yao_gut0_bob
    assert yao_job_voices.keys() == yao_gut0_voices.keys()
    assert yao_job_voices == yao_gut0_voices
    assert len(yao_job.to_dict().get(kw.voices)) == 3
    assert len(yao_job._plan_dict) == 4
    print(f"{yao_job._plan_dict.keys()=}")
    print(f"{yao_job.get_planroot_factunits_dict().keys()=}")
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
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler()
    save_duty_belief(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        belief_name=sue_texas_lessonfilehandler.belief_name,
        moment_label=sue_texas_lessonfilehandler.moment_label,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_belief=yao_duty,
    )

    assert (
        vision_file_exists(
            sue_texas_lessonfilehandler.moment_mstr_dir,
            sue_texas_lessonfilehandler.belief_name,
            sue_texas_lessonfilehandler.moment_label,
            get_texas_rope(),
            sue_texas_lessonfilehandler.knot,
            yao_str,
        )
        is False
    )

    # WHEN
    create_vision_file_from_duty_file(
        sue_texas_lessonfilehandler, yao_str, get_texas_rope()
    )

    # THEN
    assert vision_file_exists(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.belief_name,
        sue_texas_lessonfilehandler.moment_label,
        get_texas_rope(),
        sue_texas_lessonfilehandler.knot,
        yao_str,
    )
    yao_vision = get_vision_belief(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.belief_name,
        sue_texas_lessonfilehandler.moment_label,
        get_texas_rope(),
        sue_texas_lessonfilehandler.knot,
        yao_str,
    )
    assert yao_vision.belief_name is not None
    assert yao_vision.belief_name == yao_str
    assert yao_vision.to_dict() == yao_duty.to_dict()
