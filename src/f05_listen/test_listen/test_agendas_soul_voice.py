from src.f00_instrument.file import delete_dir, save_file
from src.f01_road.jaar_config import get_json_filename
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.listen import create_listen_basis, listen_to_agendas_soul_voice
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_hubunit,
)
from src.f05_listen.examples.example_listen import (
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


def test_listen_to_agendas_soul_voice_AddsTasksToBudWhenNo_teamlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_soul = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_soul.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_soul.set_acct_respect(zia_pool)
    a23_str = "accord23"
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    yao_hubunit.save_soul_bud(yao_soul)

    zia_voice = budunit_shop(zia_str)
    zia_voice.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_voice.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    zia_hubunit.save_voice_bud(zia_voice)

    new_yao_voice = create_listen_basis(yao_soul)
    assert len(new_yao_voice.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_voice.get_item_dict())=}")
    listen_to_agendas_soul_voice(new_yao_voice, yao_hubunit)

    # THEN
    assert len(new_yao_voice.get_agenda_dict()) == 2


def test_listen_to_agendas_soul_voice_AddsTasksToBud(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_soul = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_soul.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_soul.set_acct_respect(zia_pool)
    a23_str = "accord23"
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    yao_hubunit.save_soul_bud(yao_soul)

    zia_voice = budunit_shop(zia_str)
    zia_voice.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_voice.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_voice.get_item_obj(clean_road())
    cook_itemunit = zia_voice.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    zia_hubunit.save_voice_bud(zia_voice)
    new_yao_voice = create_listen_basis(yao_soul)
    assert len(new_yao_voice.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_voice.get_item_dict())=}")
    listen_to_agendas_soul_voice(new_yao_voice, yao_hubunit)

    # THEN
    assert len(new_yao_voice.get_agenda_dict()) == 2


def test_listen_to_agendas_soul_voice_AddsTasksToBudWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_voice = get_example_zia_speaker()
    bob_voice = get_example_bob_speaker()
    bob_voice.edit_item_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_itemunit = bob_voice.get_item_obj(cook_road())
    zia_cook_itemunit = zia_voice.get_item_obj(cook_road())
    assert bob_cook_itemunit != zia_cook_itemunit
    assert len(zia_cook_itemunit.reasonunits) == 1
    assert len(bob_cook_itemunit.reasonunits) == 0
    zia_str = zia_voice.owner_name
    bob_str = bob_voice.owner_name
    a23_str = "accord23"
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    bob_hubunit = hubunit_shop(env_dir(), a23_str, bob_str)
    zia_hubunit.save_voice_bud(zia_voice)
    bob_hubunit.save_voice_bud(bob_voice)

    yao_soul = get_example_yao_speaker()
    yao_str = yao_soul.owner_name
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    yao_hubunit.save_soul_bud(yao_soul)

    new_yao_voice1 = create_listen_basis(yao_soul)
    assert new_yao_voice1.item_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_soul_voice(new_yao_voice1, yao_hubunit)

    # THEN
    assert new_yao_voice1.item_exists(cook_road())
    new_cook_item = new_yao_voice1.get_item_obj(cook_road())
    zia_acctunit = new_yao_voice1.get_acct(zia_str)
    bob_acctunit = new_yao_voice1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert new_cook_item.get_reasonunit(eat_road()) is None

    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_soul.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_soul.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_soul.set_acct_respect(100)
    new_yao_voice2 = create_listen_basis(yao_soul)
    assert new_yao_voice2.item_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_soul_voice(new_yao_voice2, yao_hubunit)

    # THEN
    assert new_yao_voice2.item_exists(cook_road())
    new_cook_item = new_yao_voice2.get_item_obj(cook_road())
    zia_acctunit = new_yao_voice2.get_acct(zia_str)
    bob_acctunit = new_yao_voice2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_itemunit.get_reasonunit(eat_road())
    assert new_cook_item.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_agendas_soul_voice_ProcessesIrrationalBud(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_soul = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_soul.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_soul.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_soul.set_acct_respect(yao_pool)
    a23_str = "accord23"
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    yao_hubunit.save_soul_bud(yao_soul)

    zia_str = "Zia"
    zia_voice = budunit_shop(zia_str)
    zia_voice.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_voice.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_voice.get_item_obj(clean_road())
    cook_itemunit = zia_voice.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    zia_hubunit.save_voice_bud(zia_voice)

    sue_voice = budunit_shop(sue_str)
    sue_voice.set_max_tree_traverse(5)
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_road = sue_voice.make_l1_road(vacuum_str)
    sue_voice.set_l1_item(itemunit_shop(vacuum_str, pledge=True))
    vacuum_itemunit = sue_voice.get_item_obj(vacuum_road)
    vacuum_itemunit.teamunit.set_teamlink(yao_str)

    egg_str = "egg first"
    egg_road = sue_voice.make_l1_road(egg_str)
    sue_voice.set_l1_item(itemunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_road = sue_voice.make_l1_road(chicken_str)
    sue_voice.set_l1_item(itemunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_voice.edit_item_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_item_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_voice.edit_item_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_item_active_requisite=False,
    )
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    sue_hubunit.save_voice_bud(sue_voice)

    # WHEN
    new_yao_voice = create_listen_basis(yao_soul)
    listen_to_agendas_soul_voice(new_yao_voice, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_voice.get_agenda_dict()) != 3
    assert len(new_yao_voice.get_agenda_dict()) == 2
    zia_acctunit = new_yao_voice.get_acct(zia_str)
    sue_acctunit = new_yao_voice.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agendas_soul_voice_ProcessesMissingDebtorBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    a23_str = "accord23"
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    delete_dir(yao_hubunit._soul_file_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_hubunit._soul_file_path)=}")
    yao_soul = budunit_shop(yao_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_credit_belief = 47
    sue_credit_belief = 57
    zia_debtit_belief = 41
    sue_debtit_belief = 51
    yao_soul.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_soul.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_soul.set_acct_respect(yao_pool)
    yao_hubunit.save_soul_bud(yao_soul)

    zia_voice = budunit_shop(zia_str)
    zia_voice.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_voice.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_voice.get_item_obj(clean_road())
    cook_itemunit = zia_voice.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    zia_hubunit.save_voice_bud(zia_voice)

    # WHEN
    new_yao_voice = create_listen_basis(yao_soul)
    listen_to_agendas_soul_voice(new_yao_voice, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_voice.get_agenda_dict()) != 3
    assert len(new_yao_voice.get_agenda_dict()) == 2
    zia_acctunit = new_yao_voice.get_acct(zia_str)
    sue_acctunit = new_yao_voice.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51


def test_listen_to_agendas_soul_voice_ListensToOwner_soul_AndNotOwner_voice(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_soul = budunit_shop(yao_str)
    yao_str = "Yao"
    yao_credit_belief = 57
    yao_debtit_belief = 51
    yao_soul.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_soul.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_pool = 87
    yao_soul.set_acct_respect(yao_pool)
    # save yao without task to dutys
    a23_str = "accord23"
    yao_hubunit = hubunit_shop(env_dir(), a23_str, yao_str)
    yao_hubunit.save_soul_bud(yao_soul)

    # Save Zia to voice
    zia_str = "Zia"
    zia_voice = budunit_shop(zia_str)
    zia_voice.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_voice.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_voice.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_voice.get_item_obj(clean_road())
    cook_itemunit = zia_voice.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    zia_hubunit = hubunit_shop(env_dir(), a23_str, zia_str)
    zia_hubunit.save_voice_bud(zia_voice)

    # save yao with task to dutys
    yao_old_voice = budunit_shop(yao_str)
    vacuum_str = "vacuum"
    vacuum_road = yao_old_voice.make_l1_road(vacuum_str)
    yao_old_voice.set_l1_item(itemunit_shop(vacuum_str, pledge=True))
    vacuum_itemunit = yao_old_voice.get_item_obj(vacuum_road)
    vacuum_itemunit.teamunit.set_teamlink(yao_str)
    yao_hubunit.save_voice_bud(yao_old_voice)

    # WHEN
    new_yao_voice = create_listen_basis(yao_soul)
    listen_to_agendas_soul_voice(new_yao_voice, yao_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_voice.get_agenda_dict()) != 3
    assert len(new_yao_voice.get_agenda_dict()) == 2
