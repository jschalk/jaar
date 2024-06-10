from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.listen import listen_to_speaker_intent, create_empty_agenda
from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises


def test_listen_to_speaker_intent_RaisesErrorIfPoolIsNotSet():
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_intent(yao_agendaunit, zia_agendaunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_text}' agenda is assumed to have {zia_agendaunit._owner_id} partyunit."
    )


def test_listen_to_speaker_intent_ReturnsSameAgenda():
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    yao_agendaunit.add_partyunit(zia_text)
    yao_agendaunit.set_party_pool(100)
    zia_agendaunit = agendaunit_shop(zia_text)

    # WHEN
    after_yao_agendaunit = listen_to_speaker_intent(yao_agendaunit, zia_agendaunit)

    # THEN
    assert after_yao_agendaunit == yao_agendaunit


def test_listen_to_speaker_intent_ReturnsSingleTaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_agendaunit.add_partyunit(zia_text)
    yao_party_debtor_weight = 77
    before_yao_agendaunit.set_party_pool(yao_party_debtor_weight)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    zia_agendaunit.add_l1_idea(zia_clean_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 1
    print(f"{zia_yao_agendaunit.get_intent_dict()=}")

    # WHEN
    after_yao_agendaunit = listen_to_speaker_intent(
        before_yao_agendaunit, zia_agendaunit
    )

    # THEN
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    yao_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_party_debtor_weight
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 1


def test_listen_to_speaker_intent_ReturnsLevel2TaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_agendaunit.add_partyunit(zia_text)
    yao_debtor_weight = 77
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    zia_agendaunit.add_idea(zia_clean_ideaunit, casa_road)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 1
    print(f"{zia_yao_agendaunit.get_intent_dict()=}")

    # WHEN
    after_yao_agendaunit = listen_to_speaker_intent(
        before_yao_agendaunit, zia_agendaunit
    )

    # THEN
    clean_road = zia_agendaunit.make_road(casa_road, clean_text)
    yao_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_debtor_weight
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == yao_debtor_weight
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 1


def test_listen_to_speaker_intent_Returns2IntentIdeasLevel2TaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_agendaunit.add_partyunit(zia_text)
    yao_debtor_weight = 55
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    clean_text = "clean"
    cook_text = "cook"
    fly_text = "fly"
    yao_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    yao_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    fly_road = zia_agendaunit.make_l1_road(fly_text)
    zia_agendaunit.add_idea(yao_clean_ideaunit, casa_road)
    zia_agendaunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_agendaunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 3

    # WHEN
    after_yao_agendaunit = listen_to_speaker_intent(
        before_yao_agendaunit, zia_agendaunit
    )

    # THEN
    clean_road = zia_agendaunit.make_road(casa_road, clean_text)
    cook_road = zia_agendaunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_agendaunit.get_idea_obj(cook_road)
    after_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_agendaunit.get_idea_obj(fly_road)
    print(f"{after_clean_ideaunit._weight=}")
    assert after_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert after_clean_ideaunit._weight == 13
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 14
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 27
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_speaker_intent_Returns2IntentIdeasLevel2TaskAgendaWhereAnIdeaUnitAlreadyExists():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_agendaunit.add_partyunit(zia_text)
    yao_debtor_weight = 55
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    dish_text = "dish"
    cook_text = "cook"
    fly_text = "fly"
    yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    yao_dish_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    dish_road = zia_agendaunit.make_road(casa_road, dish_text)
    fly_road = zia_agendaunit.make_l1_road(fly_text)
    before_yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    before_yao_dish_ideaunit._assignedunit.set_suffgroup(yao_text)
    before_yao_agendaunit.add_idea(before_yao_dish_ideaunit, casa_road)
    before_yao_agendaunit.edit_idea_attr(dish_road, weight=1000)
    zia_agendaunit.add_idea(yao_dish_ideaunit, casa_road)
    zia_agendaunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_agendaunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 3

    # WHEN
    after_yao_agendaunit = listen_to_speaker_intent(
        before_yao_agendaunit, zia_agendaunit
    )

    # THEN
    cook_road = zia_agendaunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_agendaunit.get_idea_obj(cook_road)
    after_dish_ideaunit = after_yao_agendaunit.get_idea_obj(dish_road)
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_agendaunit.get_idea_obj(fly_road)
    print(f"{after_dish_ideaunit._weight=}")
    assert after_dish_ideaunit._weight != yao_dish_ideaunit._weight
    assert after_dish_ideaunit._weight == 1014
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 13
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 28
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_speaker_intent_ProcessesIrrationalAgenda():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_role.set_party_pool(yao_pool)

    sue_agendaunit = agendaunit_shop(sue_text)
    sue_agendaunit.set_max_tree_traverse(5)
    vacuum_text = "vacuum"
    vacuum_road = sue_agendaunit.make_l1_road(vacuum_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_agendaunit.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)

    egg_text = "egg first"
    egg_road = sue_agendaunit.make_l1_road(egg_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_agendaunit.make_l1_road(chicken_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_agendaunit.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_agendaunit.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )

    # WHEN
    yao_job = create_empty_agenda(yao_role, yao_text)
    yao_job.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_job.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_job.set_party_pool(yao_pool)
    yao_job = listen_to_speaker_intent(yao_job, sue_agendaunit)

    # THEN irrational agenda is ignored
    assert len(yao_job.get_intent_dict()) != 3
    assert len(yao_job.get_intent_dict()) == 0
    zia_partyunit = yao_job.get_party(zia_text)
    sue_partyunit = yao_job.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._irrational_debtor_weight=}")
    assert zia_partyunit._irrational_debtor_weight == 0
    assert sue_partyunit._irrational_debtor_weight == 51


def test_listen_to_speaker_intent_ProcessesBarrenAgenda():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_role.set_party_pool(yao_pool)

    # WHEN
    sue_job = create_empty_agenda(yao_role, sue_text)
    yao_job = create_empty_agenda(yao_role, yao_text)
    yao_job.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_job.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_job.set_party_pool(yao_pool)
    yao_job = listen_to_speaker_intent(yao_job, speaker=sue_job)

    # THEN irrational agenda is ignored
    assert len(yao_job.get_intent_dict()) != 3
    assert len(yao_job.get_intent_dict()) == 0
    zia_partyunit = yao_job.get_party(zia_text)
    sue_partyunit = yao_job.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._irrational_debtor_weight=}")
    assert zia_partyunit._irrational_debtor_weight == 0
    assert zia_partyunit._missing_job_debtor_weight == 0
    assert sue_partyunit._irrational_debtor_weight == 0
    assert sue_partyunit._missing_job_debtor_weight == 51