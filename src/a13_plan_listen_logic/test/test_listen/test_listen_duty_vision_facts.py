from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a13_plan_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
    listen_to_facts_duty_vision,
)
from src.a13_plan_listen_logic.test._util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_plan_listen_logic.test._util.example_listen import (
    casa_rope,
    casa_str,
    clean_rope,
    clean_str,
    cook_rope,
    cook_str,
    eat_rope,
    eat_str,
    full_rope,
    full_str,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    hungry_rope,
    hungry_str,
)
from src.a13_plan_listen_logic.test._util.example_listen_hub import get_texas_hubunit


def test_listen_to_facts_duty_vision_SetsSingleFactUnit_v1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_duty.set_acct_respect(zia_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)

    zia_vision = get_example_zia_speaker()
    sue_texas_hubunit.save_vision_plan(zia_vision)
    print(f"         {sue_texas_hubunit.vision_path(zia_str)=}")

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None


def test_listen_to_facts_duty_vision_SetsSingleFactUnitWithDifferentChore(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
    yao_credit_score = 47
    yao_debt_score = 41
    yao_pool = 87
    zia_str = "Zia"
    yao_duty.add_acctunit(zia_str, yao_credit_score, yao_debt_score)
    yao_duty.set_acct_respect(yao_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    clean_conceptunit = zia_vision.get_concept_obj(clean_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    sue_texas_hubunit.save_vision_plan(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()) is None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None


def test_listen_to_facts_duty_vision_GetsFactsFromSrcPlanSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has fact eat_rope = full
    # yao_vision has fact eat_rope = hungry
    # new_yao_vision fstates yao_duty fact eat_rope = full
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_rope(), full_rope())
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)
    print(f"{sue_texas_hubunit.duty_path(yao_duty)=}")
    assert yao_duty.get_fact(eat_rope()).fstate == full_rope()

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_rope()).fstate == hungry_rope()
    sue_texas_hubunit.save_vision_plan(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()).fstate == full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfstateedFromOwnersSpeakerDirPlan_v1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_rope())
    assert yao_duty.get_fact(eat_rope()) is None
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_rope(), eat_rope())
    assert zia_vision.get_fact(eat_rope()).fstate == eat_rope()
    sue_texas_hubunit.save_vision_plan(zia_vision)

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_rope()).fstate == hungry_rope()
    sue_texas_hubunit.save_vision_plan(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    print(f"{new_yao_vision.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_vision.conceptroot.factunits.keys()=}")
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_rope()) is None
    assert zia_vision.get_fact(eat_rope()).fstate == eat_rope()
    assert old_yao_vision.get_fact(eat_rope()).fstate == hungry_rope()
    assert new_yao_vision.get_fact(eat_rope()).fstate == eat_rope()


def test_listen_to_facts_duty_vision_SetsPrioritizesSelfFactsOverSpeakers(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_rope(), full_rope())
    assert yao_duty.get_fact(eat_rope()).fstate == full_rope()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_plan(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_rope(), hungry_rope())
    assert zia_vision.get_fact(eat_rope()).fstate == hungry_rope()
    sue_texas_hubunit.save_vision_plan(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_rope()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_rope()) is not None
    assert new_yao_vision.get_fact(eat_rope()).fstate == full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfstateedFromOwnersSpeakerDirPlan_v2(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    zia_str = zia_vision.owner_name
    zia_vision.add_fact(eat_rope(), eat_rope())
    assert zia_vision.get_fact(eat_rope()).fstate == eat_rope()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_vision_plan(zia_vision)

    bob_vision = get_example_bob_speaker()
    bob_str = bob_vision.owner_name
    assert bob_vision.get_fact(eat_rope()).fstate == hungry_rope()
    sue_texas_hubunit.save_vision_plan(bob_vision)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_rope())
    assert yao_duty.get_fact(eat_rope()) is None
    sue_texas_hubunit.save_duty_plan(yao_duty)

    new_yao_vision1 = create_listen_basis(yao_duty)
    assert new_yao_vision1.get_fact(eat_rope()) is None
    assert new_yao_vision1.get_missing_fact_rcontexts().get(eat_rope()) is None
    listen_to_agendas_duty_vision(new_yao_vision1, sue_texas_hubunit)
    print(f"{new_yao_vision1.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_vision1.conceptroot.factunits.keys()=}")
    assert new_yao_vision1.get_missing_fact_rcontexts().get(eat_rope()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_rope()) is None
    zia_acctunit = new_yao_vision1.get_acct(zia_str)
    bob_acctunit = new_yao_vision1.get_acct(bob_str)
    assert zia_acctunit.debt_score < bob_acctunit.debt_score
    assert bob_vision.get_fact(eat_rope()).fstate == hungry_rope()
    assert zia_vision.get_fact(eat_rope()).fstate == eat_rope()
    assert new_yao_vision1.get_fact(eat_rope()).fstate == hungry_rope()

    # WHEN
    yao_zia_debt_score = 15
    yao_bob_debt_score = 5
    yao_duty.add_acctunit(zia_str, None, yao_zia_debt_score)
    yao_duty.add_acctunit(bob_str, None, yao_bob_debt_score)
    yao_duty.set_acct_respect(100)
    new_yao_vision2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision2, sue_texas_hubunit)
    listen_to_facts_duty_vision(new_yao_vision2, sue_texas_hubunit)

    # THEN
    zia_acctunit = new_yao_vision2.get_acct(zia_str)
    bob_acctunit = new_yao_vision2.get_acct(bob_str)
    assert zia_acctunit.debt_score > bob_acctunit.debt_score
    assert bob_vision.get_fact(eat_rope()).fstate == hungry_rope()
    assert zia_vision.get_fact(eat_rope()).fstate == eat_rope()
    assert new_yao_vision2.get_fact(eat_rope()).fstate == eat_rope()


# def test_listen_to_facts_duty_vision_SetsFact(env_dir_setup_cleanup):
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     sue_speaker = planunit_shop(yao_str)
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

#     sue_speaker.add_acctunit(yao_str)
#     sue_speaker.set_acct_respect(20)
#     sue_speaker.set_concept(conceptunit_shop(clean_str), status_rope)
#     sue_speaker.set_concept(conceptunit_shop(dirty_str), status_rope)
#     sue_speaker.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
#     sue_speaker.edit_concept_attr(
#         sweep_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
#     )
#     sweep_concept = sue_speaker.get_concept_obj(sweep_rope)
#     sweep_concept.laborunit.set_laborlink(yao_str)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_vision_plan(sue_str, sue_speaker.get_json(), True)
#     yao_duty = planunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.add_acctunit(sue_str)
#     new_yao_vision = create_listen_basis(yao_duty)
#     print(f"{new_yao_vision.get_concept_dict().keys()=}")
#     # assert new_yao_vision.get_missing_fact_rcontexts().get(status_rope) is None
#     listen_to_agendas_duty_vision(new_yao_vision, texas_hubunit)
#     print(f"{new_yao_vision.get_concept_dict().keys()=}")
#     assert new_yao_vision.get_missing_fact_rcontexts().get(status_rope) is not None

#     # assert new_yao_vision.get_missing_fact_rcontexts().keys() == {status_rope}
#     # sue_speaker.add_fact(status_rope, clean_rope, create_missing_concepts=True)

#     # # WHEN
#     # listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fcontexts)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_rcontexts().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_vision_DoesNotOverrideFact():
#     # ESTABLISH
#     yao_str = "Yao"
#     yao_duty = planunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.set_acct_respect(20)
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

#     yao_duty.set_concept(conceptunit_shop(running_str), fridge_rope)
#     yao_duty.set_concept(conceptunit_shop(clean_str), status_rope)
#     yao_duty.set_concept(conceptunit_shop(dirty_str), status_rope)
#     yao_duty.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
#     yao_duty.edit_concept_attr(
#         sweep_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
#     )
#     yao_duty.edit_concept_attr(
#         sweep_rope, reason_rcontext=fridge_rope, reason_premise=running_rope
#     )
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 2
#     yao_duty.add_fact(status_rope, dirty_rope)
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 1
#     assert yao_duty.get_fact(status_rope).fstate == dirty_rope

#     # WHEN
#     yao_vision = planunit_shop(yao_str)
#     yao_vision.add_fact(status_rope, clean_rope, create_missing_concepts=True)
#     yao_vision.add_fact(fridge_rope, running_rope, create_missing_concepts=True)
#     missing_fact_fcontexts = list(yao_duty.get_missing_fact_rcontexts().keys())
#     listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fcontexts)

#     # THEN
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_rope).fstate == dirty_rope
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_rope).fstate == running_rope
