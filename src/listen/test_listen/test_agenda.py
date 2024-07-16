from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.listen import listen_to_speaker_agenda, create_empty_world
from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # GIVEN
    yao_text = "Yao"
    yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_worldunit = worldunit_shop(zia_text)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_worldunit, zia_worldunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_text}' world is assumed to have {zia_worldunit._owner_id} charunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualWorld():
    # GIVEN
    yao_text = "Yao"
    yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    yao_worldunit.add_charunit(zia_text)
    yao_worldunit.set_char_respect(100)
    zia_worldunit = worldunit_shop(zia_text)

    # WHEN
    after_yao_worldunit = listen_to_speaker_agenda(yao_worldunit, zia_worldunit)

    # THEN
    assert after_yao_worldunit == yao_worldunit


def test_listen_to_speaker_agenda_ReturnsSingleTaskWorld():
    # GIVEN
    yao_text = "Yao"
    before_yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_worldunit.add_charunit(zia_text)
    yao_char_debtor_weight = 77
    before_yao_worldunit.set_char_respect(yao_char_debtor_weight)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._doerunit.set_beliefhold(yao_text)
    zia_worldunit = worldunit_shop(zia_text)
    zia_worldunit.add_charunit(yao_text)
    zia_worldunit.add_l1_idea(zia_clean_ideaunit)
    assert len(zia_worldunit.get_agenda_dict()) == 0
    zia_yao_worldunit = copy_deepcopy(zia_worldunit)
    zia_yao_worldunit.set_owner_id(yao_text)
    assert len(zia_yao_worldunit.get_agenda_dict()) == 1
    print(f"{zia_yao_worldunit.get_agenda_dict()=}")

    # WHEN
    after_yao_worldunit = listen_to_speaker_agenda(before_yao_worldunit, zia_worldunit)

    # THEN
    clean_road = zia_worldunit.make_l1_road(clean_text)
    yao_clean_ideaunit = after_yao_worldunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_char_debtor_weight
    assert after_yao_worldunit == before_yao_worldunit
    assert len(after_yao_worldunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2TaskWorld():
    # GIVEN
    yao_text = "Yao"
    before_yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_worldunit.add_charunit(zia_text)
    yao_debtor_weight = 77
    before_yao_worldunit.set_char_respect(yao_debtor_weight)
    zia_worldunit = worldunit_shop(zia_text)
    zia_worldunit.add_charunit(yao_text)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._doerunit.set_beliefhold(yao_text)
    casa_road = zia_worldunit.make_l1_road("casa")
    zia_worldunit.add_idea(zia_clean_ideaunit, casa_road)
    assert len(zia_worldunit.get_agenda_dict()) == 0
    zia_yao_worldunit = copy_deepcopy(zia_worldunit)
    zia_yao_worldunit.set_owner_id(yao_text)
    assert len(zia_yao_worldunit.get_agenda_dict()) == 1
    print(f"{zia_yao_worldunit.get_agenda_dict()=}")

    # WHEN
    after_yao_worldunit = listen_to_speaker_agenda(before_yao_worldunit, zia_worldunit)

    # THEN
    clean_road = zia_worldunit.make_road(casa_road, clean_text)
    yao_clean_ideaunit = after_yao_worldunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_debtor_weight
    after_casa_ideaunit = after_yao_worldunit.get_idea_obj(casa_road)
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == yao_debtor_weight
    assert after_yao_worldunit == before_yao_worldunit
    assert len(after_yao_worldunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskWorld():
    # GIVEN
    yao_text = "Yao"
    before_yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_worldunit.add_charunit(zia_text)
    yao_debtor_weight = 55
    before_yao_worldunit.set_char_respect(yao_debtor_weight)
    zia_text = "Zia"
    zia_worldunit = worldunit_shop(zia_text)
    zia_worldunit.add_charunit(yao_text)
    clean_text = "clean"
    cook_text = "cook"
    fly_text = "fly"
    yao_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    yao_clean_ideaunit._doerunit.set_beliefhold(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._doerunit.set_beliefhold(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._doerunit.set_beliefhold(yao_text)
    casa_road = zia_worldunit.make_l1_road("casa")
    fly_road = zia_worldunit.make_l1_road(fly_text)
    zia_worldunit.add_idea(yao_clean_ideaunit, casa_road)
    zia_worldunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_worldunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_worldunit.get_agenda_dict()) == 0
    zia_yao_worldunit = copy_deepcopy(zia_worldunit)
    zia_yao_worldunit.set_owner_id(yao_text)
    assert len(zia_yao_worldunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_worldunit = listen_to_speaker_agenda(before_yao_worldunit, zia_worldunit)

    # THEN
    clean_road = zia_worldunit.make_road(casa_road, clean_text)
    cook_road = zia_worldunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_worldunit.get_idea_obj(cook_road)
    after_clean_ideaunit = after_yao_worldunit.get_idea_obj(clean_road)
    after_casa_ideaunit = after_yao_worldunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_worldunit.get_idea_obj(fly_road)
    print(f"{after_clean_ideaunit._weight=}")
    assert after_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert after_clean_ideaunit._weight == 13
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 14
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 27
    assert after_yao_worldunit == before_yao_worldunit
    assert len(after_yao_worldunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskWorldWhereAnIdeaUnitAlreadyExists():
    # GIVEN
    yao_text = "Yao"
    before_yao_worldunit = worldunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_worldunit.add_charunit(zia_text)
    yao_debtor_weight = 55
    before_yao_worldunit.set_char_respect(yao_debtor_weight)
    zia_text = "Zia"
    zia_worldunit = worldunit_shop(zia_text)
    zia_worldunit.add_charunit(yao_text)
    dish_text = "dish"
    cook_text = "cook"
    fly_text = "fly"
    yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    yao_dish_ideaunit._doerunit.set_beliefhold(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._doerunit.set_beliefhold(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._doerunit.set_beliefhold(yao_text)
    casa_road = zia_worldunit.make_l1_road("casa")
    dish_road = zia_worldunit.make_road(casa_road, dish_text)
    fly_road = zia_worldunit.make_l1_road(fly_text)
    before_yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    before_yao_dish_ideaunit._doerunit.set_beliefhold(yao_text)
    before_yao_worldunit.add_idea(before_yao_dish_ideaunit, casa_road)
    before_yao_worldunit.edit_idea_attr(dish_road, weight=1000)
    zia_worldunit.add_idea(yao_dish_ideaunit, casa_road)
    zia_worldunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_worldunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_worldunit.get_agenda_dict()) == 0
    zia_yao_worldunit = copy_deepcopy(zia_worldunit)
    zia_yao_worldunit.set_owner_id(yao_text)
    assert len(zia_yao_worldunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_worldunit = listen_to_speaker_agenda(before_yao_worldunit, zia_worldunit)

    # THEN
    cook_road = zia_worldunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_worldunit.get_idea_obj(cook_road)
    after_dish_ideaunit = after_yao_worldunit.get_idea_obj(dish_road)
    after_casa_ideaunit = after_yao_worldunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_worldunit.get_idea_obj(fly_road)
    print(f"{after_dish_ideaunit._weight=}")
    assert after_dish_ideaunit._weight != yao_dish_ideaunit._weight
    assert after_dish_ideaunit._weight == 1014
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 13
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 28
    assert after_yao_worldunit == before_yao_worldunit
    assert len(after_yao_worldunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


# def test_listen_to_speaker_agenda_ProcessesIrrationalWorld():
#     # GIVEN
#     yao_text = "Yao"
#     yao_duty = worldunit_shop(yao_text)
#     zia_text = "Zia"
#     zia_credor_weight = 47
#     zia_debtor_weight = 41
#     sue_text = "Sue"
#     sue_credor_weight = 57
#     sue_debtor_weight = 51
#     yao_duty.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
#     yao_duty.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
#     yao_pool = 92
#     yao_duty.set_char_respect(yao_pool)

#     sue_worldunit = worldunit_shop(sue_text)
#     sue_worldunit.set_max_tree_traverse(5)
#     vacuum_text = "vacuum"
#     vacuum_road = sue_worldunit.make_l1_road(vacuum_text)
#     sue_worldunit.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
#     vacuum_ideaunit = sue_worldunit.get_idea_obj(vacuum_road)
#     vacuum_ideaunit._doerunit.set_beliefhold(yao_text)

#     egg_text = "egg first"
#     egg_road = sue_worldunit.make_l1_road(egg_text)
#     sue_worldunit.add_l1_idea(ideaunit_shop(egg_text))
#     chicken_text = "chicken first"
#     chicken_road = sue_worldunit.make_l1_road(chicken_text)
#     sue_worldunit.add_l1_idea(ideaunit_shop(chicken_text))
#     # set egg pledge is True when chicken first is False
#     sue_worldunit.edit_idea_attr(
#         road=egg_road,
#         pledge=True,
#         reason_base=chicken_road,
#         reason_base_idea_active_requisite=True,
#     )
#     # set chick pledge is True when egg first is False
#     sue_worldunit.edit_idea_attr(
#         road=chicken_road,
#         pledge=True,
#         reason_base=egg_road,
#         reason_base_idea_active_requisite=False,
#     )

#     # WHEN
#     yao_job = create_empty_world(yao_duty, yao_text)
#     yao_job.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
#     yao_job.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
#     yao_job.set_char_respect(yao_pool)
#     yao_job = listen_to_speaker_agenda(yao_job, sue_worldunit)
#     yao_job.calc_world_metrics()

#     # THEN irrational world is ignored
#     assert len(yao_job.get_agenda_dict()) != 3
#     assert len(yao_job.get_agenda_dict()) == 0
#     zia_charunit = yao_job.get_char(zia_text)
#     sue_charunit = yao_job.get_char(sue_text)
#     print(f"{sue_charunit.debtor_weight=}")
#     print(f"{sue_charunit._irrational_debtor_weight=}")
#     assert zia_charunit._irrational_debtor_weight == 0
#     assert sue_charunit._irrational_debtor_weight == 51


def test_listen_to_speaker_agenda_ProcessesBarrenWorld():
    # GIVEN
    yao_text = "Yao"
    yao_duty = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_duty.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_duty.set_char_respect(yao_pool)

    # WHEN
    sue_job = create_empty_world(yao_duty, sue_text)
    yao_job = create_empty_world(yao_duty, yao_text)
    yao_job.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_job.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_job.set_char_respect(yao_pool)
    yao_job = listen_to_speaker_agenda(yao_job, speaker=sue_job)

    # THEN irrational world is ignored
    assert len(yao_job.get_agenda_dict()) != 3
    assert len(yao_job.get_agenda_dict()) == 0
    zia_charunit = yao_job.get_char(zia_text)
    sue_charunit = yao_job.get_char(sue_text)
    print(f"{sue_charunit.debtor_weight=}")
    print(f"{sue_charunit._irrational_debtor_weight=}")
    assert zia_charunit._irrational_debtor_weight == 0
    assert zia_charunit._inallocable_debtor_weight == 0
    assert sue_charunit._irrational_debtor_weight == 0
    assert sue_charunit._inallocable_debtor_weight == 51
