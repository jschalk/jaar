from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a13_bud_listen_logic.listen import (
    create_listen_basis,
    listen_to_facts_duty_plan,
    listen_to_agendas_duty_plan,
)
from src.a13_bud_listen_logic._utils.example_listen_hub import get_texas_hubunit
from src.a13_bud_listen_logic._utils.env_a13 import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from src.a13_bud_listen_logic._utils.example_listen import (
    casa_str,
    cook_str,
    eat_str,
    hungry_str,
    full_str,
    clean_str,
    casa_way,
    cook_way,
    eat_way,
    hungry_way,
    full_way,
    clean_way,
    get_example_zia_speaker,
    get_example_yao_speaker,
    get_example_bob_speaker,
)


def test_listen_to_facts_duty_plan_SetsSingleFactUnit_v1(env_dir_setup_cleanup):
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

    zia_plan = get_example_zia_speaker()
    sue_texas_hubunit.save_plan_bud(zia_plan)
    print(f"         {sue_texas_hubunit.plan_path(zia_str)=}")

    new_yao_plan = create_listen_basis(yao_duty)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan, sue_texas_hubunit)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan, sue_texas_hubunit)

    # THEN
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None


def test_listen_to_facts_duty_plan_SetsSingleFactUnitWithDifferentTask(
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

    zia_plan = get_example_zia_speaker()
    zia_plan.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_way())
    clean_ideaunit = zia_plan.get_idea_obj(clean_way())
    clean_ideaunit.teamunit.set_teamlink(yao_str)
    sue_texas_hubunit.save_plan_bud(zia_plan)

    new_yao_plan = create_listen_basis(yao_duty)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan, sue_texas_hubunit)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is not None
    assert new_yao_plan.get_fact(eat_way()) is None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan, sue_texas_hubunit)

    # THEN
    assert new_yao_plan.get_fact(eat_way()) is not None


def test_listen_to_facts_duty_plan_GetsFactsFromSrcBudSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has fact eat_way = full
    # yao_plan has fact eat_way = hungry
    # new_yao_plan fbranchs yao_duty fact eat_way = full
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_way(), full_way())
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)
    print(f"{sue_texas_hubunit.duty_path(yao_duty)=}")
    assert yao_duty.get_fact(eat_way()).fbranch == full_way()

    old_yao_plan = get_example_yao_speaker()
    assert old_yao_plan.get_fact(eat_way()).fbranch == hungry_way()
    sue_texas_hubunit.save_plan_bud(old_yao_plan)

    new_yao_plan = create_listen_basis(yao_duty)
    assert new_yao_plan.get_fact(eat_way()) is None
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan, sue_texas_hubunit)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan, sue_texas_hubunit)

    # THEN
    assert new_yao_plan.get_fact(eat_way()) is not None
    assert new_yao_plan.get_fact(eat_way()).fbranch == full_way()


def test_listen_to_facts_duty_plan_ConfirmNoFactfbranchedFromOwnersSpeakerDirBud_v1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_way())
    assert yao_duty.get_fact(eat_way()) is None
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_plan = get_example_zia_speaker()
    zia_plan.add_fact(eat_way(), eat_way())
    assert zia_plan.get_fact(eat_way()).fbranch == eat_way()
    sue_texas_hubunit.save_plan_bud(zia_plan)

    old_yao_plan = get_example_yao_speaker()
    assert old_yao_plan.get_fact(eat_way()).fbranch == hungry_way()
    sue_texas_hubunit.save_plan_bud(old_yao_plan)

    new_yao_plan = create_listen_basis(yao_duty)
    assert new_yao_plan.get_fact(eat_way()) is None
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan, sue_texas_hubunit)
    print(f"{new_yao_plan.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_plan.idearoot.factunits.keys()=}")
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_way()) is None
    assert zia_plan.get_fact(eat_way()).fbranch == eat_way()
    assert old_yao_plan.get_fact(eat_way()).fbranch == hungry_way()
    assert new_yao_plan.get_fact(eat_way()).fbranch == eat_way()


def test_listen_to_facts_duty_plan_SetsPrioritizesSelfFactsOverSpeakers(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(eat_way(), full_way())
    assert yao_duty.get_fact(eat_way()).fbranch == full_way()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)

    zia_plan = get_example_zia_speaker()
    zia_plan.add_fact(eat_way(), hungry_way())
    assert zia_plan.get_fact(eat_way()).fbranch == hungry_way()
    sue_texas_hubunit.save_plan_bud(zia_plan)

    new_yao_plan = create_listen_basis(yao_duty)
    assert new_yao_plan.get_fact(eat_way()) is None
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan, sue_texas_hubunit)
    assert new_yao_plan.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan, sue_texas_hubunit)

    # THEN
    assert new_yao_plan.get_fact(eat_way()) is not None
    assert new_yao_plan.get_fact(eat_way()).fbranch == full_way()


def test_listen_to_facts_duty_plan_ConfirmNoFactfbranchedFromOwnersSpeakerDirBud_v2(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_plan = get_example_zia_speaker()
    zia_str = zia_plan.owner_name
    zia_plan.add_fact(eat_way(), eat_way())
    assert zia_plan.get_fact(eat_way()).fbranch == eat_way()
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_plan_bud(zia_plan)

    bob_plan = get_example_bob_speaker()
    bob_str = bob_plan.owner_name
    assert bob_plan.get_fact(eat_way()).fbranch == hungry_way()
    sue_texas_hubunit.save_plan_bud(bob_plan)

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(eat_way())
    assert yao_duty.get_fact(eat_way()) is None
    sue_texas_hubunit.save_duty_bud(yao_duty)

    new_yao_plan1 = create_listen_basis(yao_duty)
    assert new_yao_plan1.get_fact(eat_way()) is None
    assert new_yao_plan1.get_missing_fact_rcontexts().get(eat_way()) is None
    listen_to_agendas_duty_plan(new_yao_plan1, sue_texas_hubunit)
    print(f"{new_yao_plan1.get_missing_fact_rcontexts().keys()=}")
    print(f"{new_yao_plan1.idearoot.factunits.keys()=}")
    assert new_yao_plan1.get_missing_fact_rcontexts().get(eat_way()) is not None

    # WHEN
    listen_to_facts_duty_plan(new_yao_plan1, sue_texas_hubunit)

    # THEN
    assert yao_duty.get_fact(eat_way()) is None
    zia_acctunit = new_yao_plan1.get_acct(zia_str)
    bob_acctunit = new_yao_plan1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert bob_plan.get_fact(eat_way()).fbranch == hungry_way()
    assert zia_plan.get_fact(eat_way()).fbranch == eat_way()
    assert new_yao_plan1.get_fact(eat_way()).fbranch == hungry_way()

    # WHEN
    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_duty.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_duty.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_duty.set_acct_respect(100)
    new_yao_plan2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_plan(new_yao_plan2, sue_texas_hubunit)
    listen_to_facts_duty_plan(new_yao_plan2, sue_texas_hubunit)

    # THEN
    zia_acctunit = new_yao_plan2.get_acct(zia_str)
    bob_acctunit = new_yao_plan2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    assert bob_plan.get_fact(eat_way()).fbranch == hungry_way()
    assert zia_plan.get_fact(eat_way()).fbranch == eat_way()
    assert new_yao_plan2.get_fact(eat_way()).fbranch == eat_way()


# def test_listen_to_facts_duty_plan_SetsFact(env_dir_setup_cleanup):
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
#     sue_speaker.set_idea(ideaunit_shop(clean_str), status_way)
#     sue_speaker.set_idea(ideaunit_shop(dirty_str), status_way)
#     sue_speaker.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_way)
#     sue_speaker.edit_idea_attr(
#         sweep_way, reason_rcontext=status_way, reason_premise=dirty_way
#     )
#     sweep_idea = sue_speaker.get_idea_obj(sweep_way)
#     sweep_idea.teamunit.set_teamlink(yao_str)

#     sue_texas_hubunit = get_texas_hubunit()
#     sue_texas_hubunit.save_plan_bud(sue_str, sue_speaker.get_json(), True)
#     yao_duty = budunit_shop(yao_str)
#     yao_duty.add_acctunit(yao_str)
#     yao_duty.add_acctunit(sue_str)
#     new_yao_plan = create_listen_basis(yao_duty)
#     print(f"{new_yao_plan.get_idea_dict().keys()=}")
#     # assert new_yao_plan.get_missing_fact_rcontexts().get(status_way) is None
#     listen_to_agendas_duty_plan(new_yao_plan, texas_hubunit)
#     print(f"{new_yao_plan.get_idea_dict().keys()=}")
#     assert new_yao_plan.get_missing_fact_rcontexts().get(status_way) is not None

#     # assert new_yao_plan.get_missing_fact_rcontexts().keys() == {status_way}
#     # sue_speaker.add_fact(status_way, clean_way, create_missing_ideas=True)

#     # # WHEN
#     # listen_to_facts_duty_plan(yao_duty, yao_plan, missing_fact_fcontexts)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_rcontexts().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_plan_DoesNotOverrideFact():
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

#     yao_duty.set_idea(ideaunit_shop(running_str), fridge_way)
#     yao_duty.set_idea(ideaunit_shop(clean_str), status_way)
#     yao_duty.set_idea(ideaunit_shop(dirty_str), status_way)
#     yao_duty.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_way)
#     yao_duty.edit_idea_attr(
#         sweep_way, reason_rcontext=status_way, reason_premise=dirty_way
#     )
#     yao_duty.edit_idea_attr(
#         sweep_way, reason_rcontext=fridge_way, reason_premise=running_way
#     )
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 2
#     yao_duty.add_fact(status_way, dirty_way)
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 1
#     assert yao_duty.get_fact(status_way).fbranch == dirty_way

#     # WHEN
#     yao_plan = budunit_shop(yao_str)
#     yao_plan.add_fact(status_way, clean_way, create_missing_ideas=True)
#     yao_plan.add_fact(fridge_way, running_way, create_missing_ideas=True)
#     missing_fact_fcontexts = list(yao_duty.get_missing_fact_rcontexts().keys())
#     listen_to_facts_duty_plan(yao_duty, yao_plan, missing_fact_fcontexts)

#     # THEN
#     assert len(yao_duty.get_missing_fact_rcontexts()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(status_way).fbranch == dirty_way
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_way).fbranch == running_way
