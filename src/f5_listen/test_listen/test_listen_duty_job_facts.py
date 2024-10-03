from src.f2_bud.item import itemunit_shop
from src.f2_bud.bud import budunit_shop
from src.f5_listen.listen import (
    create_listen_basis,
    listen_to_facts_duty_job,
    listen_to_agendas_duty_job,
)
from src.f5_listen.examples.listen_env import get_texas_hubunit, env_dir_setup_cleanup
from src.f5_listen.examples.example_listen import (
    casa_str,
    cook_str,
    eat_str,
    hungry_str,
    full_str,
    clean_str,
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
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_job = get_example_zia_speaker()
    sue_texas_hubunit.save_job_bud(zia_job)
    print(f"         {sue_texas_hubunit.job_path(zia_str)=}")

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is not None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None


def test_listen_to_facts_duty_job_SetsSingleFactUnitWithDifferentTask(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    yao_credit_belief = 47
    yao_debtit_belief = 41
    yao_pool = 87
    zia_str = "Zia"
    yao_duty.add_acctunit(zia_str, yao_credit_belief, yao_debtit_belief)
    yao_duty.set_acct_respect(yao_pool)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    clean_itemunit = zia_job.get_item_obj(clean_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    sue_texas_hubunit.save_job_bud(zia_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is not None
    assert new_yao_job.get_fact(eat_road()) is None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) is not None


def test_listen_to_facts_duty_job_GetsFactsFromSrcBudSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has fact eat_road = full
    # yao_job has fact eat_road = hungry
    # new_yao_job picks yao_duty fact eat_road = full
    yao_duty = get_example_yao_speaker()
    yao_duty.set_fact(eat_road(), full_road())
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)
    print(f"{sue_texas_hubunit.duty_path(yao_duty)=}")
    assert yao_duty.get_fact(eat_road()).pick == full_road()

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_bud(old_yao_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is not None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) is not None
    assert new_yao_job.get_fact(eat_road()).pick == full_road()


def test_listen_to_facts_duty_job_ConfirmNoFactPickedFromOwnersSpeakerDirBud_v1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_road())
    assert yao_duty.get_fact(eat_road()) is None
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.set_fact(eat_road(), eat_road())
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    sue_texas_hubunit.save_job_bud(zia_job)

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_bud(old_yao_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    print(f"{new_yao_job.get_missing_fact_bases().keys()=}")
    print(f"{new_yao_job._itemroot.factunits.keys()=}")
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is not None

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
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.set_fact(eat_road(), full_road())
    assert yao_duty.get_fact(eat_road()).pick == full_road()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_job = get_example_zia_speaker()
    zia_job.set_fact(eat_road(), hungry_road())
    assert zia_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_bud(zia_job)

    new_yao_job = create_listen_basis(yao_duty)
    assert new_yao_job.get_fact(eat_road()) is None
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job, sue_texas_hubunit)
    assert new_yao_job.get_missing_fact_bases().get(eat_road()) is not None

    # WHEN
    listen_to_facts_duty_job(new_yao_job, sue_texas_hubunit)

    # THEN
    assert new_yao_job.get_fact(eat_road()) is not None
    assert new_yao_job.get_fact(eat_road()).pick == full_road()


def test_listen_to_facts_duty_job_ConfirmNoFactPickedFromOwnersSpeakerDirBud_v2(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_job = get_example_zia_speaker()
    zia_str = zia_job._owner_id
    zia_job.set_fact(eat_road(), eat_road())
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_job_bud(zia_job)

    bob_job = get_example_bob_speaker()
    bob_str = bob_job._owner_id
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    sue_texas_hubunit.save_job_bud(bob_job)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_road())
    assert yao_duty.get_fact(eat_road()) is None
    sue_texas_hubunit.save_duty_bud(yao_duty)

    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.get_fact(eat_road()) is None
    assert new_yao_job1.get_missing_fact_bases().get(eat_road()) is None
    listen_to_agendas_duty_job(new_yao_job1, sue_texas_hubunit)
    print(f"{new_yao_job1.get_missing_fact_bases().keys()=}")
    print(f"{new_yao_job1._itemroot.factunits.keys()=}")
    assert new_yao_job1.get_missing_fact_bases().get(eat_road()) is not None

    # WHEN
    listen_to_facts_duty_job(new_yao_job1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_road()) is None
    zia_acctunit = new_yao_job1.get_acct(zia_str)
    bob_acctunit = new_yao_job1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    assert new_yao_job1.get_fact(eat_road()).pick == hungry_road()

    # WHEN
    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_duty.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_duty.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_duty.set_acct_respect(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_job(new_yao_job2, sue_texas_hubunit)
    listen_to_facts_duty_job(new_yao_job2, sue_texas_hubunit)

    # THEN
    zia_acctunit = new_yao_job2.get_acct(zia_str)
    bob_acctunit = new_yao_job2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    assert bob_job.get_fact(eat_road()).pick == hungry_road()
    assert zia_job.get_fact(eat_road()).pick == eat_road()
    assert new_yao_job2.get_fact(eat_road()).pick == eat_road()


# def test_listen_to_facts_duty_job_SetsFact(env_dir_setup_cleanup):
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     sue_speaker = budunit_shop(yao_str)
#     casa_str = "casa"
#     casa_road = sue_speaker.make_l1_road(casa_str)
#     status_str = "status"
#     status_road = sue_speaker.make_road(casa_road, status_str)
#     clean_str = "clean"
#     clean_road = sue_speaker.make_road(status_road, clean_str)
#     dirty_str = "dirty"
#     dirty_road = sue_speaker.make_road(status_road, dirty_str)
#     sweep_str = "sweep"
#     sweep_road = sue_speaker.make_road(casa_road, sweep_str)

#     sue_speaker.add_acctunit(yao_str)
#     sue_speaker.set_acct_respect(20)
#     sue_speaker.set_item(itemunit_shop(clean_str), status_road)
#     sue_speaker.set_item(itemunit_shop(dirty_str), status_road)
#     sue_speaker.set_item(itemunit_shop(sweep_str, pledge=True), casa_road)
#     sue_speaker.edit_item_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     sweep_item = sue_speaker.get_item_obj(sweep_road)
#     sweep_item.teamunit.set_teamlink(yao_str)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_job_bud(sue_str, sue_speaker.get_json(), True)
#     yao_duty = budunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.add_acctunit(sue_str)
#     new_yao_job = create_listen_basis(yao_duty)
#     print(f"{new_yao_job.get_item_dict().keys()=}")
#     # assert new_yao_job.get_missing_fact_bases().get(status_road) is None
#     listen_to_agendas_duty_job(new_yao_job, texas_hubunit)
#     print(f"{new_yao_job.get_item_dict().keys()=}")
#     assert new_yao_job.get_missing_fact_bases().get(status_road) is not None

#     # assert new_yao_job.get_missing_fact_bases().keys() == {status_road}
#     # sue_speaker.set_fact(status_road, clean_road, create_missing_items=True)

#     # # WHEN
#     # listen_to_facts_duty_job(yao_duty, yao_job, missing_fact_bases)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_bases().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_job_DoesNotOverrideFact():
#     # ESTABLISH
#     yao_str = "Yao"
#     yao_duty = budunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.set_acct_respect(20)
#     casa_str = "casa"
#     casa_road = yao_duty.make_l1_road(casa_str)
#     status_str = "status"
#     status_road = yao_duty.make_road(casa_road, status_str)
#     clean_str = "clean"
#     clean_road = yao_duty.make_road(status_road, clean_str)
#     dirty_str = "dirty"
#     dirty_road = yao_duty.make_road(status_road, dirty_str)
#     sweep_str = "sweep"
#     sweep_road = yao_duty.make_road(casa_road, sweep_str)
#     fridge_str = "fridge"
#     fridge_road = yao_duty.make_road(casa_road, fridge_str)
#     running_str = "running"
#     running_road = yao_duty.make_road(fridge_road, running_str)

#     yao_duty.set_item(itemunit_shop(running_str), fridge_road)
#     yao_duty.set_item(itemunit_shop(clean_str), status_road)
#     yao_duty.set_item(itemunit_shop(dirty_str), status_road)
#     yao_duty.set_item(itemunit_shop(sweep_str, pledge=True), casa_road)
#     yao_duty.edit_item_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     yao_duty.edit_item_attr(
#         sweep_road, reason_base=fridge_road, reason_premise=running_road
#     )
#     assert len(yao_duty.get_missing_fact_bases()) == 2
#     yao_duty.set_fact(status_road, dirty_road)
#     assert len(yao_duty.get_missing_fact_bases()) == 1
#     assert yao_duty.get_fact(status_road).pick == dirty_road

#     # WHEN
#     yao_job = budunit_shop(yao_str)
#     yao_job.set_fact(status_road, clean_road, create_missing_items=True)
#     yao_job.set_fact(fridge_road, running_road, create_missing_items=True)
#     missing_fact_bases = list(yao_duty.get_missing_fact_bases().keys())
#     listen_to_facts_duty_job(yao_duty, yao_job, missing_fact_bases)

#     # THEN
#     assert len(yao_duty.get_missing_fact_bases()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_road).pick == dirty_road
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_road).pick == running_road
