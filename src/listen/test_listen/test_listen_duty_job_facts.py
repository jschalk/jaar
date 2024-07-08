from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.listen import (
    create_listen_basis,
    listen_to_facts_duty_job,
    listen_to_agendas_duty_job,
)
from src.listen.examples.listen_env import get_texas_hubunit, env_dir_setup_cleanup
from src.listen.examples.example_listen import (
    casa_text,
    cook_text,
    eat_text,
    hungry_text,
    full_text,
    clean_text,
    casa_road,
    cook_road,
    eat_road,
    hungry_road,
    full_road,
    clean_road,
    get_example_zia_speaker,
    get_example_yao_speaker,
    get_example_bob_speaker,
)


def test_listen_to_facts_duty_job_SetsSingleFactUnit_v1(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_duty = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_duty.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.set_char_pool(zia_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)

    zia_job = get_example_zia_speaker()
    sue_texas_hubunit.save_job_world(zia_job)
    print(f"         {sue_texas_hubunit.job_path(zia_text)=}")

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) != None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None


def test_listen_to_facts_duty_job_SetsSingleFactUnitWithDifferentTask(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_duty = worldunit_shop(yao_text)
    yao_credor_weight = 47
    yao_debtor_weight = 41
    yao_pool = 87
    zia_text = "Zia"
    yao_duty.add_charunit(zia_text, yao_credor_weight, yao_debtor_weight)
    yao_duty.set_char_pool(yao_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    clean_ideaunit._cultureunit.set_belieflink(yao_text)
    sue_texas_hubunit.save_job_world(zia_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) != None
    assert new_yao_job.get_fact(eat_road()) is None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) != None


def test_listen_to_facts_duty_job_GetsFactsFromSrcWorldSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_duty has fact eat_road = full
    # yao_job has fact eat_road = hungry
    # new_yao_job picks yao_duty fact eat_road = full
    yao_duty = get_example_yao_speaker()
    yao_duty.set_fact(eat_road(), full_road())
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)
    print(f"{sue_texas_hubunit.duty_path(yao_duty)=}")
    assert yao_duty.get_fact(eat_road()).pick == full_road()

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_world(old_yao_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) != None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) != None
    assert new_yao_job.get_fact(eat_road()).pick == full_road()


def test_listen_to_facts_duty_job_ConfirmNoFactPickedFromOwnersSpeakerDirWorld_v1(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_road())
    assert yao_duty.get_fact(eat_road()) is None
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.set_fact(eat_road(), eat_road())
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    sue_texas_hubunit.save_job_world(zia_job)

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_world(old_yao_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    print(f"{new_yao_job.get_missing_fact_bases().keys()=}")
    print(f"{new_yao_job._idearoot._factunits.keys()=}")
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) != None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_road()) is None
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    assert old_yao_job.get_fact(eat_road()).pick == hungry_road()
    assert new_yao_job.get_fact(eat_road()).pick == eat_road()


def test_listen_to_facts_duty_job_SetsPrioritizesSelfFactsOverSpeakers(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_duty = get_example_yao_speaker()
    yao_duty.set_fact(eat_road(), full_road())
    assert yao_duty.get_fact(eat_road()).pick == full_road()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.set_fact(eat_road(), hungry_road())
    assert zia_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_world(zia_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) != None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) != None
    assert new_yao_job.get_fact(eat_road()).pick == full_road()


def test_listen_to_facts_duty_job_ConfirmNoFactPickedFromOwnersSpeakerDirWorld_v2(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_job = get_example_zia_speaker()
    zia_text = zia_job._owner_id
    zia_job.set_fact(eat_road(), eat_road())
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_job_world(zia_job)

    bob_job = get_example_bob_speaker()
    bob_text = bob_job._owner_id
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_world(bob_job)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_road())
    assert yao_duty.get_fact(eat_road()) is None
    sue_texas_hubunit.save_duty_world(yao_duty)

    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.get_fact(eat_road()) is None
    assert new_yao_job1.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job1, sue_texas_hubunit)
    print(f"{new_yao_job1.get_missing_fact_bases().keys()=}")
    print(f"{new_yao_job1._idearoot._factunits.keys()=}")
    assert new_yao_job1.get_missing_fact_bases().get(eat_road()) != None

    # WHEN
    listen_to_facts_duty_job(new_yao_job1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_road()) is None
    zia_charunit = new_yao_job1.get_char(zia_text)
    bob_charunit = new_yao_job1.get_char(bob_text)
    assert zia_charunit.debtor_weight < bob_charunit.debtor_weight
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    assert new_yao_job1.get_fact(eat_road()).pick == hungry_road()

    # WHEN
    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_duty.add_charunit(zia_text, None, yao_zia_debtor_weight)
    yao_duty.add_charunit(bob_text, None, yao_bob_debtor_weight)
    yao_duty.set_char_pool(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_job(new_yao_job2, sue_texas_hubunit)
    listen_to_facts_duty_job(new_yao_job2, sue_texas_hubunit)

    # THEN
    zia_charunit = new_yao_job2.get_char(zia_text)
    bob_charunit = new_yao_job2.get_char(bob_text)
    assert zia_charunit.debtor_weight > bob_charunit.debtor_weight
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    assert new_yao_job2.get_fact(eat_road()).pick == eat_road()


# def test_listen_to_facts_duty_job_SetsFact(env_dir_setup_cleanup):
#     # GIVEN
#     yao_text = "Yao"
#     sue_text = "Sue"
#     sue_speaker = worldunit_shop(yao_text)
#     casa_text = "casa"
#     casa_road = sue_speaker.make_l1_road(casa_text)
#     status_text = "status"
#     status_road = sue_speaker.make_road(casa_road, status_text)
#     clean_text = "clean"
#     clean_road = sue_speaker.make_road(status_road, clean_text)
#     dirty_text = "dirty"
#     dirty_road = sue_speaker.make_road(status_road, dirty_text)
#     sweep_text = "sweep"
#     sweep_road = sue_speaker.make_road(casa_road, sweep_text)

#     sue_speaker.add_charunit(yao_text)
#     sue_speaker.set_char_pool(20)
#     sue_speaker.add_idea(ideaunit_shop(clean_text), status_road)
#     sue_speaker.add_idea(ideaunit_shop(dirty_text), status_road)
#     sue_speaker.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
#     sue_speaker.edit_idea_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     sweep_idea = sue_speaker.get_idea_obj(sweep_road)
#     sweep_idea._cultureunit.set_belieflink(yao_text)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_job_world(sue_text, sue_speaker.get_json(), True)
#     yao_duty = worldunit_shop(yao_text)
#     yao_duty.add_charunit(yao_text)
#     yao_duty.add_charunit(sue_text)
#     new_yao_job = create_listen_basis(yao_duty)
#     print(f"{new_yao_job.get_idea_dict().keys()=}")
#     # assert new_yao_job.get_missing_fact_bases().get(status_road) is None
#     listen_to_agendas_duty_job(new_yao_job, texas_hubunit)
#     print(f"{new_yao_job.get_idea_dict().keys()=}")
#     assert new_yao_job.get_missing_fact_bases().get(status_road) != None

#     # assert new_yao_job.get_missing_fact_bases().keys() == {status_road}
#     # sue_speaker.set_fact(status_road, clean_road, create_missing_ideas=True)

#     # # WHEN
#     # listen_to_facts_duty_job(yao_duty, yao_job, missing_fact_bases)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_bases().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_job_DoesNotOverrideFact():
#     # GIVEN
#     yao_text = "Yao"
#     yao_duty = worldunit_shop(yao_text)
#     yao_duty.add_charunit(yao_text)
#     yao_duty.set_char_pool(20)
#     casa_text = "casa"
#     casa_road = yao_duty.make_l1_road(casa_text)
#     status_text = "status"
#     status_road = yao_duty.make_road(casa_road, status_text)
#     clean_text = "clean"
#     clean_road = yao_duty.make_road(status_road, clean_text)
#     dirty_text = "dirty"
#     dirty_road = yao_duty.make_road(status_road, dirty_text)
#     sweep_text = "sweep"
#     sweep_road = yao_duty.make_road(casa_road, sweep_text)
#     fridge_text = "fridge"
#     fridge_road = yao_duty.make_road(casa_road, fridge_text)
#     running_text = "running"
#     running_road = yao_duty.make_road(fridge_road, running_text)

#     yao_duty.add_idea(ideaunit_shop(running_text), fridge_road)
#     yao_duty.add_idea(ideaunit_shop(clean_text), status_road)
#     yao_duty.add_idea(ideaunit_shop(dirty_text), status_road)
#     yao_duty.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
#     yao_duty.edit_idea_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     yao_duty.edit_idea_attr(
#         sweep_road, reason_base=fridge_road, reason_premise=running_road
#     )
#     assert len(yao_duty.get_missing_fact_bases()) == 2
#     yao_duty.set_fact(status_road, dirty_road)
#     assert len(yao_duty.get_missing_fact_bases()) == 1
#     assert yao_duty.get_fact(status_road).pick == dirty_road

#     # WHEN
#     yao_job = worldunit_shop(yao_text)
#     yao_job.set_fact(status_road, clean_road, create_missing_ideas=True)
#     yao_job.set_fact(fridge_road, running_road, create_missing_ideas=True)
#     missing_fact_bases = list(yao_duty.get_missing_fact_bases().keys())
#     listen_to_facts_duty_job(yao_duty, yao_job, missing_fact_bases)

#     # THEN
#     assert len(yao_duty.get_missing_fact_bases()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_road).pick == dirty_road
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_road).pick == running_road
