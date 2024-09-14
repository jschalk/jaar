from src.s2_bud.idea import ideaunit_shop
from src.s2_bud.bud import budunit_shop
from src.s5_listen.listen import listen_to_speaker_agenda, create_empty_bud
from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_str = "Yao"
    yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_budunit, zia_budunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_str}' bud is assumed to have {zia_budunit._owner_id} acctunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualBud():
    # ESTABLISH
    yao_str = "Yao"
    yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    yao_budunit.add_acctunit(zia_str)
    yao_budunit.set_acct_respect(100)
    zia_budunit = budunit_shop(zia_str)

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(yao_budunit, zia_budunit)

    # THEN
    assert after_yao_budunit == yao_budunit


def test_listen_to_speaker_agenda_ReturnsSingleTaskBud():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_budunit.add_acctunit(zia_str)
    yao_acct_debtit_belief = 77
    before_yao_budunit.set_acct_respect(yao_acct_debtit_belief)
    clean_str = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_str, pledge=True)
    zia_clean_ideaunit.teamunit.set_teamlink(yao_str)
    zia_budunit = budunit_shop(zia_str)
    zia_budunit.add_acctunit(yao_str)
    zia_budunit.set_l1_idea(zia_clean_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_str)
    yao_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit.mass=}")
    assert yao_clean_ideaunit.mass != zia_clean_ideaunit.mass
    assert yao_clean_ideaunit.mass == yao_acct_debtit_belief
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2TaskBud():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_budunit.add_acctunit(zia_str)
    yao_debtit_belief = 77
    before_yao_budunit.set_acct_respect(yao_debtit_belief)
    zia_budunit = budunit_shop(zia_str)
    zia_budunit.add_acctunit(yao_str)
    clean_str = "clean"
    zia_clean_ideaunit = ideaunit_shop(clean_str, pledge=True)
    zia_clean_ideaunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    zia_budunit.set_idea(zia_clean_ideaunit, casa_road)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_str)
    yao_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    print(f"{yao_clean_ideaunit.mass=}")
    assert yao_clean_ideaunit.mass != zia_clean_ideaunit.mass
    assert yao_clean_ideaunit.mass == yao_debtit_belief
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    print(f"{after_casa_ideaunit.mass=}")
    assert after_casa_ideaunit.mass != 1
    assert after_casa_ideaunit.mass == yao_debtit_belief
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskBud():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_budunit.add_acctunit(zia_str)
    yao_debtit_belief = 55
    before_yao_budunit.set_acct_respect(yao_debtit_belief)

    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    zia_budunit.add_acctunit(yao_str)
    clean_str = "clean"
    cook_str = "cook"
    fly_str = "fly"
    yao_clean_ideaunit = ideaunit_shop(clean_str, pledge=True)
    yao_clean_ideaunit.teamunit.set_teamlink(yao_str)
    yao_cook_ideaunit = ideaunit_shop(cook_str, pledge=True)
    yao_cook_ideaunit.teamunit.set_teamlink(yao_str)
    yao_fly_ideaunit = ideaunit_shop(fly_str, pledge=True)
    yao_fly_ideaunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    fly_road = zia_budunit.make_l1_road(fly_str)
    zia_budunit.set_idea(yao_clean_ideaunit, casa_road)
    zia_budunit.set_idea(yao_cook_ideaunit, casa_road)
    zia_budunit.set_l1_idea(yao_fly_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_str)
    cook_road = zia_budunit.make_road(casa_road, cook_str)
    after_cook_ideaunit = after_yao_budunit.get_idea_obj(cook_road)
    after_clean_ideaunit = after_yao_budunit.get_idea_obj(clean_road)
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_budunit.get_idea_obj(fly_road)
    print(f"{after_clean_ideaunit.mass=}")
    assert after_clean_ideaunit.mass != yao_clean_ideaunit.mass
    assert after_clean_ideaunit.mass == 19
    print(f"{after_cook_ideaunit.mass=}")
    assert after_cook_ideaunit.mass != yao_cook_ideaunit.mass
    assert after_cook_ideaunit.mass == 18
    print(f"{after_casa_ideaunit.mass=}")
    assert after_casa_ideaunit.mass != 1
    assert after_casa_ideaunit.mass == 37
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit.mass != 1
    assert after_fly_ideaunit.mass == 18


def test_listen_to_speaker_agenda_Returns2AgendaIdeasLevel2TaskBudWhereAnIdeaUnitAlreadyExists():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_budunit = budunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_budunit.add_acctunit(zia_str)
    yao_debtit_belief = 55
    before_yao_budunit.set_acct_respect(yao_debtit_belief)
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    zia_budunit.add_acctunit(yao_str)
    dish_str = "dish"
    cook_str = "cook"
    fly_str = "fly"
    yao_dish_ideaunit = ideaunit_shop(dish_str, pledge=True)
    yao_dish_ideaunit.teamunit.set_teamlink(yao_str)
    yao_cook_ideaunit = ideaunit_shop(cook_str, pledge=True)
    yao_cook_ideaunit.teamunit.set_teamlink(yao_str)
    yao_fly_ideaunit = ideaunit_shop(fly_str, pledge=True)
    yao_fly_ideaunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    dish_road = zia_budunit.make_road(casa_road, dish_str)
    fly_road = zia_budunit.make_l1_road(fly_str)
    before_yao_dish_ideaunit = ideaunit_shop(dish_str, pledge=True)
    before_yao_dish_ideaunit.teamunit.set_teamlink(yao_str)
    before_yao_budunit.set_idea(before_yao_dish_ideaunit, casa_road)
    before_yao_budunit.edit_idea_attr(dish_road, mass=1000)
    zia_budunit.set_idea(yao_dish_ideaunit, casa_road)
    zia_budunit.set_idea(yao_cook_ideaunit, casa_road)
    zia_budunit.set_l1_idea(yao_fly_ideaunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_id(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    cook_road = zia_budunit.make_road(casa_road, cook_str)
    after_cook_ideaunit = after_yao_budunit.get_idea_obj(cook_road)
    after_dish_ideaunit = after_yao_budunit.get_idea_obj(dish_road)
    after_casa_ideaunit = after_yao_budunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_budunit.get_idea_obj(fly_road)
    print(f"{after_dish_ideaunit.mass=}")
    assert after_dish_ideaunit.mass != yao_dish_ideaunit.mass
    assert after_dish_ideaunit.mass == 1018
    print(f"{after_cook_ideaunit.mass=}")
    assert after_cook_ideaunit.mass != yao_cook_ideaunit.mass
    assert after_cook_ideaunit.mass == 19
    print(f"{after_casa_ideaunit.mass=}")
    assert after_casa_ideaunit.mass != 1
    assert after_casa_ideaunit.mass == 38
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_ideaunit.mass != 1
    assert after_fly_ideaunit.mass == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalBud():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    sue_budunit = budunit_shop(sue_str)
    sue_budunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_road = sue_budunit.make_l1_road(vacuum_str)
    sue_budunit.set_l1_idea(ideaunit_shop(vacuum_str, pledge=True))
    vacuum_ideaunit = sue_budunit.get_idea_obj(vacuum_road)
    vacuum_ideaunit.teamunit.set_teamlink(yao_str)

    egg_str = "egg first"
    egg_road = sue_budunit.make_l1_road(egg_str)
    sue_budunit.set_l1_idea(ideaunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_road = sue_budunit.make_l1_road(chicken_str)
    sue_budunit.set_l1_idea(ideaunit_shop(chicken_str))
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
    yao_job = create_empty_bud(yao_duty, yao_str)
    yao_job.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_job.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_job.set_acct_respect(yao_pool)
    yao_job = listen_to_speaker_agenda(yao_job, sue_budunit)
    yao_job.settle_bud()

    # THEN irrational bud is ignored
    assert len(yao_job.get_agenda_dict()) != 3
    assert len(yao_job.get_agenda_dict()) == 0
    zia_acctunit = yao_job.get_acct(zia_str)
    sue_acctunit = yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_speaker_agenda_ProcessesBarrenBud():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    # WHEN
    sue_job = create_empty_bud(yao_duty, sue_str)
    yao_job = create_empty_bud(yao_duty, yao_str)
    yao_job.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_job.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_job.set_acct_respect(yao_pool)
    yao_job = listen_to_speaker_agenda(yao_job, speaker=sue_job)

    # THEN irrational bud is ignored
    assert len(yao_job.get_agenda_dict()) != 3
    assert len(yao_job.get_agenda_dict()) == 0
    zia_acctunit = yao_job.get_acct(zia_str)
    sue_acctunit = yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51
