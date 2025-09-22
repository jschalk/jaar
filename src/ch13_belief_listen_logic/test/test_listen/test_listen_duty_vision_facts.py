from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch12_hub_toolbox.keep_tool import save_duty_belief
from src.ch13_belief_listen_logic.listen_main import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
    listen_to_facts_duty_vision,
)
from src.ch13_belief_listen_logic.test._util.ch13_env import env_dir_setup_cleanup
from src.ch13_belief_listen_logic.test._util.example_listen import (
    casa_rope,
    clean_rope,
    clean_str,
    eat_rope,
    full_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    hungry_rope,
)
from src.ch13_belief_listen_logic.test._util.example_listen_hub import get_texas_hubunit


def test_listen_to_facts_duty_vision_SetsSingleFactUnit_v1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    zia_pool = 87
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_duty.set_voice_respect(zia_pool)
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    sue_texas_hubunit.save_vision_belief(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None


def test_listen_to_facts_duty_vision_SetsSingleFactUnitWithDifferentChore(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str, a23_str)
    yao_voice_cred_points = 47
    yao_voice_debt_points = 41
    yao_pool = 87
    zia_str = "Zia"
    yao_duty.add_voiceunit(zia_str, yao_voice_cred_points, yao_voice_debt_points)
    yao_duty.set_voice_respect(yao_pool)
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    clean_planunit = zia_vision.get_plan_obj(clean_rope())
    clean_planunit.laborunit.add_party(yao_str)
    sue_texas_hubunit.save_vision_belief(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()) is None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None


def test_listen_to_facts_duty_vision_GetsFactsFromSrcBeliefSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has fact eat_rope = full
    # yao_vision has fact eat_rope = hungry
    # new_yao_vision fact_states yao_duty fact eat_rope = full
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_rope(), full_rope())
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    assert yao_duty.get_fact(eat_rope()).fact_state == full_rope()

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    sue_texas_hubunit.save_vision_belief(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()).fact_state == full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfact_stateedFromBeliefsSpeakerDirBelief_v1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_rope())
    assert yao_duty.get_fact(eat_rope()) is None
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_rope(), eat_rope())
    assert zia_vision.get_fact(eat_rope()).fact_state == eat_rope()
    sue_texas_hubunit.save_vision_belief(zia_vision)

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    sue_texas_hubunit.save_vision_belief(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    print(f"{new_yao_vision.get_missing_fact_reason_contexts().keys()=}")
    print(f"{new_yao_vision.planroot.factunits.keys()=}")
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_rope()) is None
    assert zia_vision.get_fact(eat_rope()).fact_state == eat_rope()
    assert old_yao_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    assert new_yao_vision.get_fact(eat_rope()).fact_state == eat_rope()


def test_listen_to_facts_duty_vision_SetsPrioritizesSelfFactsOverSpeakers(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_rope(), full_rope())
    assert yao_duty.get_fact(eat_rope()).fact_state == full_rope()
    sue_texas_hubunit = get_texas_hubunit()
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_rope(), hungry_rope())
    assert zia_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    sue_texas_hubunit.save_vision_belief(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()).fact_state == full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfact_stateedFromBeliefsSpeakerDirBelief_v2(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    zia_str = zia_vision.belief_name
    zia_vision.add_fact(eat_rope(), eat_rope())
    assert zia_vision.get_fact(eat_rope()).fact_state == eat_rope()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_vision_belief(zia_vision)

    bob_vision = get_example_bob_speaker()
    bob_str = bob_vision.belief_name
    assert bob_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    sue_texas_hubunit.save_vision_belief(bob_vision)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_rope())
    assert yao_duty.get_fact(eat_rope()) is None
    save_duty_belief(
        moment_mstr_dir=sue_texas_hubunit.moment_mstr_dir,
        belief_name=sue_texas_hubunit.belief_name,
        moment_label=sue_texas_hubunit.moment_label,
        keep_rope=sue_texas_hubunit.keep_rope,
        knot=None,
        duty_belief=yao_duty,
    )

    new_yao_vision1 = create_listen_basis(yao_duty)
    assert new_yao_vision1.get_fact(eat_rope()) is None
    assert new_yao_vision1.get_missing_fact_reason_contexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision1, sue_texas_hubunit)
    print(f"{new_yao_vision1.get_missing_fact_reason_contexts().keys()=}")
    print(f"{new_yao_vision1.planroot.factunits.keys()=}")
    assert (
        new_yao_vision1.get_missing_fact_reason_contexts().get(eat_rope()) is not None
    )

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_rope()) is None
    zia_voiceunit = new_yao_vision1.get_voice(zia_str)
    bob_voiceunit = new_yao_vision1.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_points < bob_voiceunit.voice_debt_points
    assert bob_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    assert zia_vision.get_fact(eat_rope()).fact_state == eat_rope()
    assert new_yao_vision1.get_fact(eat_rope()).fact_state == hungry_rope()

    # WHEN
    yao_zia_voice_debt_points = 15
    yao_bob_voice_debt_points = 5
    yao_duty.add_voiceunit(zia_str, None, yao_zia_voice_debt_points)
    yao_duty.add_voiceunit(bob_str, None, yao_bob_voice_debt_points)
    yao_duty.set_voice_respect(100)
    new_yao_vision2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision2, sue_texas_hubunit)
    listen_to_facts_duty_vision(new_yao_vision2, sue_texas_hubunit)

    # THEN
    zia_voiceunit = new_yao_vision2.get_voice(zia_str)
    bob_voiceunit = new_yao_vision2.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_points > bob_voiceunit.voice_debt_points
    assert bob_vision.get_fact(eat_rope()).fact_state == hungry_rope()
    assert zia_vision.get_fact(eat_rope()).fact_state == eat_rope()
    assert new_yao_vision2.get_fact(eat_rope()).fact_state == eat_rope()


# def test_listen_to_facts_duty_vision_SetsFact(env_dir_setup_cleanup):
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     sue_speaker = beliefunit_shop(yao_str)
#     casa_str = "casa"
#     casa_rope = sue_speaker.make_l1_rope(casa_str)
#     status_str = "status"
#     status_rope = sue_speaker.make_rope(casa_rope, status_str)
#     clean_str = "clean"
#     clean_rope = sue_speaker.make_rope(status_rope, clean_str)
#     dirty_str = "dirty"
#     dirty_rope = sue_speaker.make_rope(status_rope, dirty_str)
#     sweep_str = "sweep"
#     sweep_rope = sue_speaker.make_rope(casa_rope, sweep_str)

#     sue_speaker.add_voiceunit(yao_str)
#     sue_speaker.set_voice_respect(20)
#     sue_speaker.set_plan(planunit_shop(clean_str), status_rope)
#     sue_speaker.set_plan(planunit_shop(dirty_str), status_rope)
#     sue_speaker.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
#     sue_speaker.edit_plan_attr(
#         sweep_rope, reason_context=status_rope, reason_case=dirty_rope
#     )
#     sweep_plan = sue_speaker.get_plan_obj(sweep_rope)
#     sweep_plan.laborunit.add_party(yao_str)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_vision_belief(sue_str, sue_speaker.get_json(), True)
#     yao_duty = beliefunit_shop(yao_str)
#     yao_duty.add_voiceunit(yao_str)
#     yao_duty.add_voiceunit(sue_str)
#     new_yao_vision = create_listen_basis(yao_duty)
#     print(f"{new_yao_vision.get_plan_dict().keys()=}")
#     # assert new_yao_vision.get_missing_fact_reason_contexts().get(status_rope) is None
#     listen_to_agendas_duty_vision(new_yao_vision, texas_hubunit)
#     print(f"{new_yao_vision.get_plan_dict().keys()=}")
#     assert new_yao_vision.get_missing_fact_reason_contexts().get(status_rope) is not None

#     # assert new_yao_vision.get_missing_fact_reason_contexts().keys() == {status_rope}
#     # sue_speaker.add_fact(status_rope, clean_rope, create_missing_plans=True)

#     # # WHEN
#     # listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fact_contexts)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_reason_contexts().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_vision_DoesNotOverrideFact():
#     # ESTABLISH
#     yao_str = "Yao"
#     yao_duty = beliefunit_shop(yao_str)
#     yao_duty.add_voiceunit(yao_str)
#     yao_duty.set_voice_respect(20)
#     casa_str = "casa"
#     casa_rope = yao_duty.make_l1_rope(casa_str)
#     status_str = "status"
#     status_rope = yao_duty.make_rope(casa_rope, status_str)
#     clean_str = "clean"
#     clean_rope = yao_duty.make_rope(status_rope, clean_str)
#     dirty_str = "dirty"
#     dirty_rope = yao_duty.make_rope(status_rope, dirty_str)
#     sweep_str = "sweep"
#     sweep_rope = yao_duty.make_rope(casa_rope, sweep_str)
#     fridge_str = "fridge"
#     fridge_rope = yao_duty.make_rope(casa_rope, fridge_str)
#     running_str = "running"
#     running_rope = yao_duty.make_rope(fridge_rope, running_str)

#     yao_duty.set_plan(planunit_shop(running_str), fridge_rope)
#     yao_duty.set_plan(planunit_shop(clean_str), status_rope)
#     yao_duty.set_plan(planunit_shop(dirty_str), status_rope)
#     yao_duty.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
#     yao_duty.edit_plan_attr(
#         sweep_rope, reason_context=status_rope, reason_case=dirty_rope
#     )
#     yao_duty.edit_plan_attr(
#         sweep_rope, reason_context=fridge_rope, reason_case=running_rope
#     )
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 2
#     yao_duty.add_fact(status_rope, dirty_rope)
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 1
#     assert yao_duty.get_fact(status_rope).fact_state == dirty_rope

#     # WHEN
#     yao_vision = beliefunit_shop(yao_str)
#     yao_vision.add_fact(status_rope, clean_rope, create_missing_plans=True)
#     yao_vision.add_fact(fridge_rope, running_rope, create_missing_plans=True)
#     missing_fact_fact_contexts = list(yao_duty.get_missing_fact_reason_contexts().keys())
#     listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fact_contexts)

#     # THEN
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_rope).fact_state == dirty_rope
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_rope).fact_state == running_rope
