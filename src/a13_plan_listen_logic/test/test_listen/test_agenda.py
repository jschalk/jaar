from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a13_plan_listen_logic.listen import (
    create_empty_plan_from_plan,
    listen_to_speaker_agenda,
)


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_str = "Yao"
    yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_planunit, zia_planunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_str}' plan is assumed to have {zia_planunit.owner_name} acctunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualPlan():
    # ESTABLISH
    yao_str = "Yao"
    yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    yao_planunit.add_acctunit(zia_str)
    yao_planunit.set_acct_respect(100)
    zia_planunit = planunit_shop(zia_str)

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(yao_planunit, zia_planunit)

    # THEN
    assert after_yao_planunit == yao_planunit


def test_listen_to_speaker_agenda_ReturnsSingleChorePlan():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_planunit.add_acctunit(zia_str)
    yao_acct_acct_debt_points = 77
    before_yao_planunit.set_acct_respect(yao_acct_acct_debt_points)
    clean_str = "clean"
    zia_clean_conceptunit = conceptunit_shop(clean_str, task=True)
    zia_clean_conceptunit.laborunit.set_laborlink(yao_str)
    zia_planunit = planunit_shop(zia_str)
    zia_planunit.add_acctunit(yao_str)
    zia_planunit.set_l1_concept(zia_clean_conceptunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_owner_name(yao_str)
    assert len(zia_yao_planunit.get_agenda_dict()) == 1
    print(f"{zia_yao_planunit.get_agenda_dict()=}")

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_l1_rope(clean_str)
    yao_clean_conceptunit = after_yao_planunit.get_concept_obj(clean_rope)
    print(f"{yao_clean_conceptunit.mass=}")
    assert yao_clean_conceptunit.mass != zia_clean_conceptunit.mass
    assert yao_clean_conceptunit.mass == yao_acct_acct_debt_points
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2ChorePlan():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_planunit.add_acctunit(zia_str)
    yao_acct_debt_points = 77
    before_yao_planunit.set_acct_respect(yao_acct_debt_points)
    zia_planunit = planunit_shop(zia_str)
    zia_planunit.add_acctunit(yao_str)
    clean_str = "clean"
    zia_clean_conceptunit = conceptunit_shop(clean_str, task=True)
    zia_clean_conceptunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_planunit.make_l1_rope("casa")
    zia_planunit.set_concept(zia_clean_conceptunit, casa_rope)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_owner_name(yao_str)
    assert len(zia_yao_planunit.get_agenda_dict()) == 1
    print(f"{zia_yao_planunit.get_agenda_dict()=}")

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_rope(casa_rope, clean_str)
    yao_clean_conceptunit = after_yao_planunit.get_concept_obj(clean_rope)
    print(f"{yao_clean_conceptunit.mass=}")
    assert yao_clean_conceptunit.mass != zia_clean_conceptunit.mass
    assert yao_clean_conceptunit.mass == yao_acct_debt_points
    after_casa_conceptunit = after_yao_planunit.get_concept_obj(casa_rope)
    print(f"{after_casa_conceptunit.mass=}")
    assert after_casa_conceptunit.mass != 1
    assert after_casa_conceptunit.mass == yao_acct_debt_points
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaConceptsLevel2ChorePlan():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_planunit.add_acctunit(zia_str)
    yao_acct_debt_points = 55
    before_yao_planunit.set_acct_respect(yao_acct_debt_points)

    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)
    zia_planunit.add_acctunit(yao_str)
    clean_str = "clean"
    cook_str = "cook"
    fly_str = "fly"
    yao_clean_conceptunit = conceptunit_shop(clean_str, task=True)
    yao_clean_conceptunit.laborunit.set_laborlink(yao_str)
    yao_cook_conceptunit = conceptunit_shop(cook_str, task=True)
    yao_cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_fly_conceptunit = conceptunit_shop(fly_str, task=True)
    yao_fly_conceptunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_planunit.make_l1_rope("casa")
    fly_rope = zia_planunit.make_l1_rope(fly_str)
    zia_planunit.set_concept(yao_clean_conceptunit, casa_rope)
    zia_planunit.set_concept(yao_cook_conceptunit, casa_rope)
    zia_planunit.set_l1_concept(yao_fly_conceptunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_owner_name(yao_str)
    assert len(zia_yao_planunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_rope(casa_rope, clean_str)
    cook_rope = zia_planunit.make_rope(casa_rope, cook_str)
    after_cook_conceptunit = after_yao_planunit.get_concept_obj(cook_rope)
    after_clean_conceptunit = after_yao_planunit.get_concept_obj(clean_rope)
    after_casa_conceptunit = after_yao_planunit.get_concept_obj(casa_rope)
    after_fly_conceptunit = after_yao_planunit.get_concept_obj(fly_rope)
    print(f"{after_clean_conceptunit.mass=}")
    assert after_clean_conceptunit.mass != yao_clean_conceptunit.mass
    assert after_clean_conceptunit.mass == 19
    print(f"{after_cook_conceptunit.mass=}")
    assert after_cook_conceptunit.mass != yao_cook_conceptunit.mass
    assert after_cook_conceptunit.mass == 18
    print(f"{after_casa_conceptunit.mass=}")
    assert after_casa_conceptunit.mass != 1
    assert after_casa_conceptunit.mass == 37
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 3
    assert after_fly_conceptunit.mass != 1
    assert after_fly_conceptunit.mass == 18


def test_listen_to_speaker_agenda_Returns2AgendaConceptsLevel2ChorePlanWhereAnConceptUnitExistsInAdvance():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_planunit = planunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_planunit.add_acctunit(zia_str)
    yao_acct_debt_points = 55
    before_yao_planunit.set_acct_respect(yao_acct_debt_points)
    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)
    zia_planunit.add_acctunit(yao_str)
    dish_str = "dish"
    cook_str = "cook"
    fly_str = "fly"
    yao_dish_conceptunit = conceptunit_shop(dish_str, task=True)
    yao_dish_conceptunit.laborunit.set_laborlink(yao_str)
    yao_cook_conceptunit = conceptunit_shop(cook_str, task=True)
    yao_cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_fly_conceptunit = conceptunit_shop(fly_str, task=True)
    yao_fly_conceptunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_planunit.make_l1_rope("casa")
    dish_rope = zia_planunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_planunit.make_l1_rope(fly_str)
    before_yao_dish_conceptunit = conceptunit_shop(dish_str, task=True)
    before_yao_dish_conceptunit.laborunit.set_laborlink(yao_str)
    before_yao_planunit.set_concept(before_yao_dish_conceptunit, casa_rope)
    before_yao_planunit.edit_concept_attr(dish_rope, mass=1000)
    zia_planunit.set_concept(yao_dish_conceptunit, casa_rope)
    zia_planunit.set_concept(yao_cook_conceptunit, casa_rope)
    zia_planunit.set_l1_concept(yao_fly_conceptunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_owner_name(yao_str)
    assert len(zia_yao_planunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    cook_rope = zia_planunit.make_rope(casa_rope, cook_str)
    after_cook_conceptunit = after_yao_planunit.get_concept_obj(cook_rope)
    after_dish_conceptunit = after_yao_planunit.get_concept_obj(dish_rope)
    after_casa_conceptunit = after_yao_planunit.get_concept_obj(casa_rope)
    after_fly_conceptunit = after_yao_planunit.get_concept_obj(fly_rope)
    print(f"{after_dish_conceptunit.mass=}")
    assert after_dish_conceptunit.mass != yao_dish_conceptunit.mass
    assert after_dish_conceptunit.mass == 1018
    print(f"{after_cook_conceptunit.mass=}")
    assert after_cook_conceptunit.mass != yao_cook_conceptunit.mass
    assert after_cook_conceptunit.mass == 19
    print(f"{after_casa_conceptunit.mass=}")
    assert after_casa_conceptunit.mass != 1
    assert after_casa_conceptunit.mass == 38
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 3
    assert after_fly_conceptunit.mass != 1
    assert after_fly_conceptunit.mass == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalPlan():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    sue_str = "Sue"
    sue_acct_cred_points = 57
    sue_acct_debt_points = 51
    yao_duty.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_duty.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    sue_planunit = planunit_shop(sue_str)
    sue_planunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_planunit.make_l1_rope(vacuum_str)
    sue_planunit.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = sue_planunit.get_concept_obj(vacuum_rope)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_planunit.make_l1_rope(egg_str)
    sue_planunit.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_planunit.make_l1_rope(chicken_str)
    sue_planunit.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_planunit.edit_concept_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rconcept_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_planunit.edit_concept_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rconcept_active_requisite=False,
    )
    sue_planunit.settle_plan()
    assert sue_planunit._rational is False
    assert len(sue_planunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_plan_from_plan(yao_duty, yao_str)
    yao_vision.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_vision.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_vision.set_acct_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_planunit)
    yao_vision.settle_plan()

    # THEN irrational plan is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_acctunit = yao_vision.get_acct(zia_str)
    sue_acctunit = yao_vision.get_acct(sue_str)
    print(f"{sue_acctunit.acct_debt_points=}")
    print(f"{sue_acctunit._irrational_acct_debt_points=}")
    assert zia_acctunit._irrational_acct_debt_points == 0
    assert sue_acctunit._irrational_acct_debt_points == 51


def test_listen_to_speaker_agenda_ProcessesBarrenPlan():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    sue_str = "Sue"
    sue_acct_cred_points = 57
    sue_acct_debt_points = 51
    yao_duty.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_duty.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_plan_from_plan(yao_duty, sue_str)
    yao_vision = create_empty_plan_from_plan(yao_duty, yao_str)
    yao_vision.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_vision.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_vision.set_acct_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational plan is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_acctunit = yao_vision.get_acct(zia_str)
    sue_acctunit = yao_vision.get_acct(sue_str)
    print(f"{sue_acctunit.acct_debt_points=}")
    print(f"{sue_acctunit._irrational_acct_debt_points=}")
    assert zia_acctunit._irrational_acct_debt_points == 0
    assert zia_acctunit._inallocable_acct_debt_points == 0
    assert sue_acctunit._irrational_acct_debt_points == 0
    assert sue_acctunit._inallocable_acct_debt_points == 51
