from src.f0_instrument.file import delete_dir, save_file
from src.f1_road.jaar_config import get_json_filename
from src.f2_bud.idea import ideaunit_shop
from src.f2_bud.bud import budunit_shop
from src.f5_listen.hubunit import hubunit_shop
from src.f5_listen.listen import create_listen_basis, listen_to_agendas_voice_final
from src.f5_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_hubunit,
)
from src.f5_listen.examples.example_listen import (
    cook_str,
    clean_str,
    run_str,
    casa_road,
    cook_road,
    eat_road,
    hungry_road,
    full_road,
    clean_road,
    run_road,
    get_example_yao_speaker,
    get_example_zia_speaker,
    get_example_bob_speaker,
)
from os.path import exists as os_path_exists


def test_listen_to_agendas_voice_final_AddsTasksToBudWhenNo_teamlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_voice = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_voice.set_acct_respect(zia_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    yao_hubunit.save_voice_bud(yao_voice)

    zia_final = budunit_shop(zia_str)
    zia_final.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_road())
    zia_final.set_idea(ideaunit_shop(cook_str(), pledge=True), casa_road())
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    zia_hubunit.save_final_bud(zia_final)

    new_yao_final = create_listen_basis(yao_voice)
    assert len(new_yao_final.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_final.get_idea_dict())=}")
    listen_to_agendas_voice_final(new_yao_final, yao_hubunit)

    # THEN
    assert len(new_yao_final.get_agenda_dict()) == 2


def test_listen_to_agendas_voice_final_AddsTasksToBud(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_voice = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_voice.set_acct_respect(zia_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    yao_hubunit.save_voice_bud(yao_voice)

    zia_final = budunit_shop(zia_str)
    zia_final.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_road())
    zia_final.set_idea(ideaunit_shop(cook_str(), pledge=True), casa_road())
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    clean_ideaunit = zia_final.get_idea_obj(clean_road())
    cook_ideaunit = zia_final.get_idea_obj(cook_road())
    clean_ideaunit.teamunit.set_teamlink(yao_str)
    cook_ideaunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    zia_hubunit.save_final_bud(zia_final)
    new_yao_final = create_listen_basis(yao_voice)
    assert len(new_yao_final.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_final.get_idea_dict())=}")
    listen_to_agendas_voice_final(new_yao_final, yao_hubunit)

    # THEN
    assert len(new_yao_final.get_agenda_dict()) == 2


def test_listen_to_agendas_voice_final_AddsTasksToBudWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_final = get_example_zia_speaker()
    bob_final = get_example_bob_speaker()
    bob_final.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_final.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_final.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit.reasonunits) == 1
    assert len(bob_cook_ideaunit.reasonunits) == 0
    zia_str = zia_final._owner_id
    bob_str = bob_final._owner_id
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    bob_hubunit = hubunit_shop(env_dir(), None, bob_str)
    zia_hubunit.save_final_bud(zia_final)
    bob_hubunit.save_final_bud(bob_final)

    yao_voice = get_example_yao_speaker()
    yao_str = yao_voice._owner_id
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    yao_hubunit.save_voice_bud(yao_voice)

    new_yao_final1 = create_listen_basis(yao_voice)
    assert new_yao_final1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_voice_final(new_yao_final1, yao_hubunit)

    # THEN
    assert new_yao_final1.idea_exists(cook_road())
    new_cook_idea = new_yao_final1.get_idea_obj(cook_road())
    zia_acctunit = new_yao_final1.get_acct(zia_str)
    bob_acctunit = new_yao_final1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_voice.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_voice.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_voice.set_acct_respect(100)
    new_yao_final2 = create_listen_basis(yao_voice)
    assert new_yao_final2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_voice_final(new_yao_final2, yao_hubunit)

    # THEN
    assert new_yao_final2.idea_exists(cook_road())
    new_cook_idea = new_yao_final2.get_idea_obj(cook_road())
    zia_acctunit = new_yao_final2.get_acct(zia_str)
    bob_acctunit = new_yao_final2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_agendas_voice_final_ProcessesIrrationalBud(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_voice = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_voice.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_voice.set_acct_respect(yao_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    yao_hubunit.save_voice_bud(yao_voice)

    zia_str = "Zia"
    zia_final = budunit_shop(zia_str)
    zia_final.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_road())
    zia_final.set_idea(ideaunit_shop(cook_str(), pledge=True), casa_road())
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    clean_ideaunit = zia_final.get_idea_obj(clean_road())
    cook_ideaunit = zia_final.get_idea_obj(cook_road())
    clean_ideaunit.teamunit.set_teamlink(yao_str)
    cook_ideaunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    zia_hubunit.save_final_bud(zia_final)

    sue_final = budunit_shop(sue_str)
    sue_final.set_max_tree_traverse(5)
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_road = sue_final.make_l1_road(vacuum_str)
    sue_final.set_l1_idea(ideaunit_shop(vacuum_str, pledge=True))
    vacuum_ideaunit = sue_final.get_idea_obj(vacuum_road)
    vacuum_ideaunit.teamunit.set_teamlink(yao_str)

    egg_str = "egg first"
    egg_road = sue_final.make_l1_road(egg_str)
    sue_final.set_l1_idea(ideaunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_road = sue_final.make_l1_road(chicken_str)
    sue_final.set_l1_idea(ideaunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_final.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_idea_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_final.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_idea_active_requisite=False,
    )
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    sue_hubunit.save_final_bud(sue_final)

    # WHEN
    new_yao_final = create_listen_basis(yao_voice)
    listen_to_agendas_voice_final(new_yao_final, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_final.get_agenda_dict()) != 3
    assert len(new_yao_final.get_agenda_dict()) == 2
    zia_acctunit = new_yao_final.get_acct(zia_str)
    sue_acctunit = new_yao_final.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agendas_voice_final_ProcessesMissingDebtorBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    delete_dir(yao_hubunit.voice_file_path())  # don't know why I have to do this...
    print(f"{os_path_exists(yao_hubunit.voice_file_path())=}")
    yao_voice = budunit_shop(yao_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_credit_belief = 47
    sue_credit_belief = 57
    zia_debtit_belief = 41
    sue_debtit_belief = 51
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_voice.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_voice.set_acct_respect(yao_pool)
    yao_hubunit.save_voice_bud(yao_voice)

    zia_final = budunit_shop(zia_str)
    zia_final.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_road())
    zia_final.set_idea(ideaunit_shop(cook_str(), pledge=True), casa_road())
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    clean_ideaunit = zia_final.get_idea_obj(clean_road())
    cook_ideaunit = zia_final.get_idea_obj(cook_road())
    clean_ideaunit.teamunit.set_teamlink(yao_str)
    cook_ideaunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    zia_hubunit.save_final_bud(zia_final)

    # WHEN
    new_yao_final = create_listen_basis(yao_voice)
    listen_to_agendas_voice_final(new_yao_final, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_final.get_agenda_dict()) != 3
    assert len(new_yao_final.get_agenda_dict()) == 2
    zia_acctunit = new_yao_final.get_acct(zia_str)
    sue_acctunit = new_yao_final.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51


def test_listen_to_agendas_voice_final_ListensToOwner_voice_AndNotOwner_final(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_voice = budunit_shop(yao_str)
    yao_str = "Yao"
    yao_credit_belief = 57
    yao_debtit_belief = 51
    yao_voice.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_pool = 87
    yao_voice.set_acct_respect(yao_pool)
    # save yao without task to dutys
    yao_hubunit = hubunit_shop(env_dir(), None, yao_str)
    yao_hubunit.save_voice_bud(yao_voice)

    # Save Zia to final
    zia_str = "Zia"
    zia_final = budunit_shop(zia_str)
    zia_final.set_idea(ideaunit_shop(clean_str(), pledge=True), casa_road())
    zia_final.set_idea(ideaunit_shop(cook_str(), pledge=True), casa_road())
    zia_final.add_acctunit(yao_str, debtit_belief=12)
    clean_ideaunit = zia_final.get_idea_obj(clean_road())
    cook_ideaunit = zia_final.get_idea_obj(cook_road())
    clean_ideaunit.teamunit.set_teamlink(yao_str)
    cook_ideaunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_str)
    zia_hubunit.save_final_bud(zia_final)

    # save yao with task to dutys
    yao_old_final = budunit_shop(yao_str)
    vacuum_str = "vacuum"
    vacuum_road = yao_old_final.make_l1_road(vacuum_str)
    yao_old_final.set_l1_idea(ideaunit_shop(vacuum_str, pledge=True))
    vacuum_ideaunit = yao_old_final.get_idea_obj(vacuum_road)
    vacuum_ideaunit.teamunit.set_teamlink(yao_str)
    yao_hubunit.save_final_bud(yao_old_final)

    # WHEN
    new_yao_final = create_listen_basis(yao_voice)
    listen_to_agendas_voice_final(new_yao_final, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_final.get_agenda_dict()) != 3
    assert len(new_yao_final.get_agenda_dict()) == 2
