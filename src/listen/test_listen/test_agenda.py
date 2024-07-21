from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.listen import listen_to_speaker_agenda, create_empty_bud
from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_text = "Yao"
    yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_budunit, zia_budunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_text}' bud is assumed to have {zia_budunit._owner_id} acctunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualBud():
    # ESTABLISH
    yao_text = "Yao"
    yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    yao_budunit.add_acctunit(zia_text)
    yao_budunit.set_acct_respect(100)
    zia_budunit = budunit_shop(zia_text)

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(yao_budunit, zia_budunit)

    # THEN
    assert after_yao_budunit == yao_budunit


def test_listen_to_speaker_agenda_ReturnsSingleTaskBud():
    # ESTABLISH
    yao_text = "Yao"
    before_yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_budunit.add_acctunit(zia_text)
    yao_acct_debtor_weight = 77
    before_yao_budunit.set_acct_respect(yao_acct_debtor_weight)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._doerunit.set_lobbyhold(yao_text)
    zia_budunit = budunit_shop(zia_text)
    zia_budunit.add_acctunit(yao_text)
    zia_budunit.set_l1_idea(zia_clean_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_text)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_text)
    yao_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_acct_debtor_weight
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2TaskBud():
    # ESTABLISH
    yao_text = "Yao"
    before_yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_budunit.add_acctunit(zia_text)
    yao_debtor_weight = 77
    before_yao_budunit.set_acct_respect(yao_debtor_weight)
    zia_budunit = budunit_shop(zia_text)
    zia_budunit.add_acctunit(yao_text)
    clean_text = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    zia_clean_ideaunit._doerunit.set_lobbyhold(yao_text)
    casa_road = zia_budunit.make_l1_road("casa")
    zia_budunit.set_idea(zia_clean_ideaunit, casa_road)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_text)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_text)
    yao_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit._weight=}")
    assert yao_clean_ideaunit._weight != zia_clean_ideaunit._weight
    assert yao_clean_ideaunit._weight == yao_debtor_weight
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == yao_debtor_weight
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskBud():
    # ESTABLISH
    yao_text = "Yao"
    before_yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_budunit.add_acctunit(zia_text)
    yao_debtor_weight = 55
    before_yao_budunit.set_acct_respect(yao_debtor_weight)
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    zia_budunit.add_acctunit(yao_text)
    clean_text = "clean"
    cook_text = "cook"
    fly_text = "fly"
    yao_clean_ideaunit = ideaunit_shop(clean_text, pledge=True)
    yao_clean_ideaunit._doerunit.set_lobbyhold(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._doerunit.set_lobbyhold(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._doerunit.set_lobbyhold(yao_text)
    casa_road = zia_budunit.make_l1_road("casa")
    fly_road = zia_budunit.make_l1_road(fly_text)
    zia_budunit.set_idea(yao_clean_ideaunit, casa_road)
    zia_budunit.set_idea(yao_cook_ideaunit, casa_road)
    zia_budunit.set_l1_idea(yao_fly_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_text)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_text)
    cook_road = zia_budunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_budunit.get_idea_obj(cook_road)
    after_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_budunit.get_idea_obj(fly_road)
    print(f"{after_clean_ideaunit._weight=}")
    assert after_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert after_clean_ideaunit._weight == 13
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 14
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 27
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskBudWhereAnIdeaUnitAlreadyExists():
    # ESTABLISH
    yao_text = "Yao"
    before_yao_budunit = budunit_shop(yao_text)
    zia_text = "Zia"
    before_yao_budunit.add_acctunit(zia_text)
    yao_debtor_weight = 55
    before_yao_budunit.set_acct_respect(yao_debtor_weight)
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    zia_budunit.add_acctunit(yao_text)
    dish_text = "dish"
    cook_text = "cook"
    fly_text = "fly"
    yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    yao_dish_ideaunit._doerunit.set_lobbyhold(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, pledge=True)
    yao_cook_ideaunit._doerunit.set_lobbyhold(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, pledge=True)
    yao_fly_ideaunit._doerunit.set_lobbyhold(yao_text)
    casa_road = zia_budunit.make_l1_road("casa")
    dish_road = zia_budunit.make_road(casa_road, dish_text)
    fly_road = zia_budunit.make_l1_road(fly_text)
    before_yao_dish_ideaunit = ideaunit_shop(dish_text, pledge=True)
    before_yao_dish_ideaunit._doerunit.set_lobbyhold(yao_text)
    before_yao_budunit.set_idea(before_yao_dish_ideaunit, casa_road)
    before_yao_budunit.edit_idea_attr(dish_road, weight=1000)
    zia_budunit.set_idea(yao_dish_ideaunit, casa_road)
    zia_budunit.set_idea(yao_cook_ideaunit, casa_road)
    zia_budunit.set_l1_idea(yao_fly_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_text)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    cook_road = zia_budunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_budunit.get_idea_obj(cook_road)
    after_dish_ideaunit = after_yao_budunit.get_idea_obj(dish_road)
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_budunit.get_idea_obj(fly_road)
    print(f"{after_dish_ideaunit._weight=}")
    assert after_dish_ideaunit._weight != yao_dish_ideaunit._weight
    assert after_dish_ideaunit._weight == 1014
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 13
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 28
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_speaker_agenda_ProcessesIrrationalBud():
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_duty.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.add_acctunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    sue_budunit = budunit_shop(sue_text)
    sue_budunit.set_max_tree_traverse(6)
    vacuum_text = "vacuum"
    vacuum_road = sue_budunit.make_l1_road(vacuum_text)
    sue_budunit.set_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_budunit.get_idea_obj(vacuum_road)
    vacuum_ideaunit._doerunit.set_lobbyhold(yao_text)

    egg_text = "egg first"
    egg_road = sue_budunit.make_l1_road(egg_text)
    sue_budunit.set_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_budunit.make_l1_road(chicken_text)
    sue_budunit.set_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_budunit.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_idea_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_budunit.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_idea_active_requisite=False,
    )
    sue_budunit.settle_bud()
    assert sue_budunit._rational is False
    assert len(sue_budunit.get_agenda_dict()) == 3

    # WHEN
    yao_job = create_empty_bud(yao_duty, yao_text)
    yao_job.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_job.add_acctunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_job.set_acct_respect(yao_pool)
    yao_job = listen_to_speaker_agenda(yao_job, sue_budunit)
    yao_job.settle_bud()

    # THEN irrational bud is ignored
    assert len(yao_job.get_agenda_dict()) != 3
    assert len(yao_job.get_agenda_dict()) == 0
    zia_acctunit = yao_job.get_acct(zia_text)
    sue_acctunit = yao_job.get_acct(sue_text)
    print(f"{sue_acctunit.debtor_weight=}")
    print(f"{sue_acctunit._irrational_debtor_weight=}")
    assert zia_acctunit._irrational_debtor_weight == 0
    assert sue_acctunit._irrational_debtor_weight == 51


def test_listen_to_speaker_agenda_ProcessesBarrenBud():
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_duty.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.add_acctunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    # WHEN
    sue_job = create_empty_bud(yao_duty, sue_text)
    yao_job = create_empty_bud(yao_duty, yao_text)
    yao_job.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_job.add_acctunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_job.set_acct_respect(yao_pool)
    yao_job = listen_to_speaker_agenda(yao_job, speaker=sue_job)

    # THEN irrational bud is ignored
    assert len(yao_job.get_agenda_dict()) != 3
    assert len(yao_job.get_agenda_dict()) == 0
    zia_acctunit = yao_job.get_acct(zia_text)
    sue_acctunit = yao_job.get_acct(sue_text)
    print(f"{sue_acctunit.debtor_weight=}")
    print(f"{sue_acctunit._irrational_debtor_weight=}")
    assert zia_acctunit._irrational_debtor_weight == 0
    assert zia_acctunit._inallocable_debtor_weight == 0
    assert sue_acctunit._irrational_debtor_weight == 0
    assert sue_acctunit._inallocable_debtor_weight == 51
