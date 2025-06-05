from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a13_bud_listen_logic._test_util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_bud_listen_logic._test_util.example_listen import (
    casa_str,
    casa_way,
    clean_str,
    clean_way,
    cook_str,
    cook_way,
    eat_str,
    eat_way,
    full_str,
    full_way,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    hungry_str,
    hungry_way,
)
from src.a13_bud_listen_logic._test_util.example_listen_hub import get_texas_hubunit
from src.a13_bud_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
    listen_to_facts_duty_vision,
)


def test_listen_to_facts_duty_vision_SetsSingleFactUnit_v1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_vision = get_example_zia_speaker()
    sue_texas_hubunit.save_vision_bud(zia_vision)
    print(f"         {sue_texas_hubunit.vision_path(zia_str)=}")

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None


def test_listen_to_facts_duty_vision_SetsSingleFactUnitWithDifferentChore(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    yao_credit_belief = 47
    yao_debtit_belief = 41
    yao_pool = 87
    zia_str = "Zia"
    yao_duty.add_acctunit(zia_str, yao_credit_belief, yao_debtit_belief)
    yao_duty.set_acct_respect(yao_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    clean_conceptunit = zia_vision.get_concept_obj(clean_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    sue_texas_hubunit.save_vision_bud(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is not None
    assert new_yao_vision.get_fact(eat_way()) is None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_way()) is not None


def test_listen_to_facts_duty_vision_GetsFactsFromSrcBudSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has fact eat_way = full
    # yao_vision has fact eat_way = hungry
    # new_yao_vision fstates yao_duty fact eat_way = full
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_way(), full_way())
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)
    print(f"{sue_texas_hubunit.duty_path(yao_duty)=}")
    assert yao_duty.get_fact(eat_way()).fstate == full_way()

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_way()).fstate == hungry_way()
    sue_texas_hubunit.save_vision_bud(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_way()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_way()) is not None
    assert new_yao_vision.get_fact(eat_way()).fstate == full_way()


def test_listen_to_facts_duty_vision_ConfirmNoFactfstateedFromOwnersSpeakerDirBud_v1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_way())
    assert yao_duty.get_fact(eat_way()) is None
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_way(), eat_way())
    assert zia_vision.get_fact(eat_way()).fstate == eat_way()
    sue_texas_hubunit.save_vision_bud(zia_vision)

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(eat_way()).fstate == hungry_way()
    sue_texas_hubunit.save_vision_bud(old_yao_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_way()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    print(f"{new_yao_vision.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_vision.conceptroot.factunits.keys()=}")
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_way()) is None
    assert zia_vision.get_fact(eat_way()).fstate == eat_way()
    assert old_yao_vision.get_fact(eat_way()).fstate == hungry_way()
    assert new_yao_vision.get_fact(eat_way()).fstate == eat_way()


def test_listen_to_facts_duty_vision_SetsPrioritizesSelfFactsOverSpeakers(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_way(), full_way())
    assert yao_duty.get_fact(eat_way()).fstate == full_way()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(eat_way(), hungry_way())
    assert zia_vision.get_fact(eat_way()).fstate == hungry_way()
    sue_texas_hubunit.save_vision_bud(zia_vision)

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(eat_way()) is None
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision, sue_texas_hubunit)
    assert new_yao_vision.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision, sue_texas_hubunit)

    # THEN
    assert new_yao_vision.get_fact(eat_way()) is not None
    assert new_yao_vision.get_fact(eat_way()).fstate == full_way()


def test_listen_to_facts_duty_vision_ConfirmNoFactfstateedFromOwnersSpeakerDirBud_v2(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    zia_str = zia_vision.owner_name
    zia_vision.add_fact(eat_way(), eat_way())
    assert zia_vision.get_fact(eat_way()).fstate == eat_way()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_vision_bud(zia_vision)

    bob_vision = get_example_bob_speaker()
    bob_str = bob_vision.owner_name
    assert bob_vision.get_fact(eat_way()).fstate == hungry_way()
    sue_texas_hubunit.save_vision_bud(bob_vision)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_way())
    assert yao_duty.get_fact(eat_way()) is None
    sue_texas_hubunit.save_duty_bud(yao_duty)

    new_yao_vision1 = create_listen_basis(yao_duty)
    assert new_yao_vision1.get_fact(eat_way()) is None
    assert new_yao_vision1.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_vision(new_yao_vision1, sue_texas_hubunit)
    print(f"{new_yao_vision1.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_vision1.conceptroot.factunits.keys()=}")
    assert new_yao_vision1.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_vision(new_yao_vision1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_way()) is None
    zia_acctunit = new_yao_vision1.get_acct(zia_str)
    bob_acctunit = new_yao_vision1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert bob_vision.get_fact(eat_way()).fstate == hungry_way()
    assert zia_vision.get_fact(eat_way()).fstate == eat_way()
    assert new_yao_vision1.get_fact(eat_way()).fstate == hungry_way()

    # WHEN
    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_duty.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_duty.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_duty.set_acct_respect(100)
    new_yao_vision2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision2, sue_texas_hubunit)
    listen_to_facts_duty_vision(new_yao_vision2, sue_texas_hubunit)

    # THEN
    zia_acctunit = new_yao_vision2.get_acct(zia_str)
    bob_acctunit = new_yao_vision2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    assert bob_vision.get_fact(eat_way()).fstate == hungry_way()
    assert zia_vision.get_fact(eat_way()).fstate == eat_way()
    assert new_yao_vision2.get_fact(eat_way()).fstate == eat_way()


# def test_listen_to_facts_duty_vision_SetsFact(env_dir_setup_cleanup):
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     sue_speaker = budunit_shop(yao_str)
#     casa_str = "casa"
#     casa_way = sue_speaker.make_l1_way(casa_str)
#     status_str = "status"
#     status_way = sue_speaker.make_way(casa_way, status_str)
#     clean_str = "clean"
#     clean_way = sue_speaker.make_way(status_way, clean_str)
#     dirty_str = "dirty"
#     dirty_way = sue_speaker.make_way(status_way, dirty_str)
#     sweep_str = "sweep"
#     sweep_way = sue_speaker.make_way(casa_way, sweep_str)

#     sue_speaker.add_acctunit(yao_str)
#     sue_speaker.set_acct_respect(20)
#     sue_speaker.set_concept(conceptunit_shop(clean_str), status_way)
#     sue_speaker.set_concept(conceptunit_shop(dirty_str), status_way)
#     sue_speaker.set_concept(conceptunit_shop(sweep_str, task=True), casa_way)
#     sue_speaker.edit_concept_attr(
#         sweep_way, reason_rcontext=status_way, reason_premise=dirty_way
#     )
#     sweep_concept = sue_speaker.get_concept_obj(sweep_way)
#     sweep_concept.laborunit.set_laborlink(yao_str)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_vision_bud(sue_str, sue_speaker.get_json(), True)
#     yao_duty = budunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.add_acctunit(sue_str)
#     new_yao_vision = create_listen_basis(yao_duty)
#     print(f"{new_yao_vision.get_concept_dict().keys()=}")
#     # assert new_yao_vision.get_missing_fact_rcontexts().get(status_way) is None
#     listen_to_agendas_duty_vision(new_yao_vision, texas_hubunit)
#     print(f"{new_yao_vision.get_concept_dict().keys()=}")
#     assert new_yao_vision.get_missing_fact_rcontexts().get(status_way) is not None

#     # assert new_yao_vision.get_missing_fact_rcontexts().keys() == {status_way}
#     # sue_speaker.add_fact(status_way, clean_way, create_missing_concepts=True)

#     # # WHEN
#     # listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fcontexts)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_rcontexts().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_vision_DoesNotOverrideFact():
#     # ESTABLISH
#     yao_str = "Yao"
#     yao_duty = budunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.set_acct_respect(20)
#     casa_str = "casa"
#     casa_way = yao_duty.make_l1_way(casa_str)
#     status_str = "status"
#     status_way = yao_duty.make_way(casa_way, status_str)
#     clean_str = "clean"
#     clean_way = yao_duty.make_way(status_way, clean_str)
#     dirty_str = "dirty"
#     dirty_way = yao_duty.make_way(status_way, dirty_str)
#     sweep_str = "sweep"
#     sweep_way = yao_duty.make_way(casa_way, sweep_str)
#     fridge_str = "fridge"
#     fridge_way = yao_duty.make_way(casa_way, fridge_str)
#     running_str = "running"
#     running_way = yao_duty.make_way(fridge_way, running_str)

#     yao_duty.set_concept(conceptunit_shop(running_str), fridge_way)
#     yao_duty.set_concept(conceptunit_shop(clean_str), status_way)
#     yao_duty.set_concept(conceptunit_shop(dirty_str), status_way)
#     yao_duty.set_concept(conceptunit_shop(sweep_str, task=True), casa_way)
#     yao_duty.edit_concept_attr(
#         sweep_way, reason_rcontext=status_way, reason_premise=dirty_way
#     )
#     yao_duty.edit_concept_attr(
#         sweep_way, reason_rcontext=fridge_way, reason_premise=running_way
#     )
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 2
#     yao_duty.add_fact(status_way, dirty_way)
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 1
#     assert yao_duty.get_fact(status_way).fstate == dirty_way

#     # WHEN
#     yao_vision = budunit_shop(yao_str)
#     yao_vision.add_fact(status_way, clean_way, create_missing_concepts=True)
#     yao_vision.add_fact(fridge_way, running_way, create_missing_concepts=True)
#     missing_fact_fcontexts = list(yao_duty.get_missing_fact_rcontexts().keys())
#     listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fcontexts)

#     # THEN
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_way).fstate == dirty_way
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_way).fstate == running_way
