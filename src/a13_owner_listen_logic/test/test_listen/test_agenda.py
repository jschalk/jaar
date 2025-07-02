from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a13_owner_listen_logic.listen import (
    create_empty_owner_from_owner,
    listen_to_speaker_agenda,
)


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_str = "Yao"
    yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    zia_ownerunit = ownerunit_shop(zia_str)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_ownerunit, zia_ownerunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_str}' owner is assumed to have {zia_ownerunit.owner_name} acctunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualOwner():
    # ESTABLISH
    yao_str = "Yao"
    yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    yao_ownerunit.add_acctunit(zia_str)
    yao_ownerunit.set_acct_respect(100)
    zia_ownerunit = ownerunit_shop(zia_str)

    # WHEN
    after_yao_ownerunit = listen_to_speaker_agenda(yao_ownerunit, zia_ownerunit)

    # THEN
    assert after_yao_ownerunit == yao_ownerunit


def test_listen_to_speaker_agenda_ReturnsSingleChoreOwner():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_ownerunit.add_acctunit(zia_str)
    yao_acct_acct_debt_points = 77
    before_yao_ownerunit.set_acct_respect(yao_acct_acct_debt_points)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, task=True)
    zia_clean_planunit.laborunit.set_laborlink(yao_str)
    zia_ownerunit = ownerunit_shop(zia_str)
    zia_ownerunit.add_acctunit(yao_str)
    zia_ownerunit.set_l1_plan(zia_clean_planunit)
    assert len(zia_ownerunit.get_agenda_dict()) == 0
    zia_yao_ownerunit = copy_deepcopy(zia_ownerunit)
    zia_yao_ownerunit.set_owner_name(yao_str)
    assert len(zia_yao_ownerunit.get_agenda_dict()) == 1
    print(f"{zia_yao_ownerunit.get_agenda_dict()=}")

    # WHEN
    after_yao_ownerunit = listen_to_speaker_agenda(before_yao_ownerunit, zia_ownerunit)

    # THEN
    clean_rope = zia_ownerunit.make_l1_rope(clean_str)
    yao_clean_planunit = after_yao_ownerunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.mass=}")
    assert yao_clean_planunit.mass != zia_clean_planunit.mass
    assert yao_clean_planunit.mass == yao_acct_acct_debt_points
    assert after_yao_ownerunit == before_yao_ownerunit
    assert len(after_yao_ownerunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2ChoreOwner():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_ownerunit.add_acctunit(zia_str)
    yao_acct_debt_points = 77
    before_yao_ownerunit.set_acct_respect(yao_acct_debt_points)
    zia_ownerunit = ownerunit_shop(zia_str)
    zia_ownerunit.add_acctunit(yao_str)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, task=True)
    zia_clean_planunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_ownerunit.make_l1_rope("casa")
    zia_ownerunit.set_plan(zia_clean_planunit, casa_rope)
    assert len(zia_ownerunit.get_agenda_dict()) == 0
    zia_yao_ownerunit = copy_deepcopy(zia_ownerunit)
    zia_yao_ownerunit.set_owner_name(yao_str)
    assert len(zia_yao_ownerunit.get_agenda_dict()) == 1
    print(f"{zia_yao_ownerunit.get_agenda_dict()=}")

    # WHEN
    after_yao_ownerunit = listen_to_speaker_agenda(before_yao_ownerunit, zia_ownerunit)

    # THEN
    clean_rope = zia_ownerunit.make_rope(casa_rope, clean_str)
    yao_clean_planunit = after_yao_ownerunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.mass=}")
    assert yao_clean_planunit.mass != zia_clean_planunit.mass
    assert yao_clean_planunit.mass == yao_acct_debt_points
    after_casa_planunit = after_yao_ownerunit.get_plan_obj(casa_rope)
    print(f"{after_casa_planunit.mass=}")
    assert after_casa_planunit.mass != 1
    assert after_casa_planunit.mass == yao_acct_debt_points
    assert after_yao_ownerunit == before_yao_ownerunit
    assert len(after_yao_ownerunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2ChoreOwner():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_ownerunit.add_acctunit(zia_str)
    yao_acct_debt_points = 55
    before_yao_ownerunit.set_acct_respect(yao_acct_debt_points)

    zia_str = "Zia"
    zia_ownerunit = ownerunit_shop(zia_str)
    zia_ownerunit.add_acctunit(yao_str)
    clean_str = "clean"
    cook_str = "cook"
    fly_str = "fly"
    yao_clean_planunit = planunit_shop(clean_str, task=True)
    yao_clean_planunit.laborunit.set_laborlink(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, task=True)
    yao_cook_planunit.laborunit.set_laborlink(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, task=True)
    yao_fly_planunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_ownerunit.make_l1_rope("casa")
    fly_rope = zia_ownerunit.make_l1_rope(fly_str)
    zia_ownerunit.set_plan(yao_clean_planunit, casa_rope)
    zia_ownerunit.set_plan(yao_cook_planunit, casa_rope)
    zia_ownerunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_ownerunit.get_agenda_dict()) == 0
    zia_yao_ownerunit = copy_deepcopy(zia_ownerunit)
    zia_yao_ownerunit.set_owner_name(yao_str)
    assert len(zia_yao_ownerunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_ownerunit = listen_to_speaker_agenda(before_yao_ownerunit, zia_ownerunit)

    # THEN
    clean_rope = zia_ownerunit.make_rope(casa_rope, clean_str)
    cook_rope = zia_ownerunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_ownerunit.get_plan_obj(cook_rope)
    after_clean_planunit = after_yao_ownerunit.get_plan_obj(clean_rope)
    after_casa_planunit = after_yao_ownerunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_ownerunit.get_plan_obj(fly_rope)
    print(f"{after_clean_planunit.mass=}")
    assert after_clean_planunit.mass != yao_clean_planunit.mass
    assert after_clean_planunit.mass == 19
    print(f"{after_cook_planunit.mass=}")
    assert after_cook_planunit.mass != yao_cook_planunit.mass
    assert after_cook_planunit.mass == 18
    print(f"{after_casa_planunit.mass=}")
    assert after_casa_planunit.mass != 1
    assert after_casa_planunit.mass == 37
    assert after_yao_ownerunit == before_yao_ownerunit
    assert len(after_yao_ownerunit.get_agenda_dict()) == 3
    assert after_fly_planunit.mass != 1
    assert after_fly_planunit.mass == 18


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2ChoreOwnerWhereAnPlanUnitExistsInAdvance():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_ownerunit = ownerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_ownerunit.add_acctunit(zia_str)
    yao_acct_debt_points = 55
    before_yao_ownerunit.set_acct_respect(yao_acct_debt_points)
    zia_str = "Zia"
    zia_ownerunit = ownerunit_shop(zia_str)
    zia_ownerunit.add_acctunit(yao_str)
    dish_str = "dish"
    cook_str = "cook"
    fly_str = "fly"
    yao_dish_planunit = planunit_shop(dish_str, task=True)
    yao_dish_planunit.laborunit.set_laborlink(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, task=True)
    yao_cook_planunit.laborunit.set_laborlink(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, task=True)
    yao_fly_planunit.laborunit.set_laborlink(yao_str)
    casa_rope = zia_ownerunit.make_l1_rope("casa")
    dish_rope = zia_ownerunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_ownerunit.make_l1_rope(fly_str)
    before_yao_dish_planunit = planunit_shop(dish_str, task=True)
    before_yao_dish_planunit.laborunit.set_laborlink(yao_str)
    before_yao_ownerunit.set_plan(before_yao_dish_planunit, casa_rope)
    before_yao_ownerunit.edit_plan_attr(dish_rope, mass=1000)
    zia_ownerunit.set_plan(yao_dish_planunit, casa_rope)
    zia_ownerunit.set_plan(yao_cook_planunit, casa_rope)
    zia_ownerunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_ownerunit.get_agenda_dict()) == 0
    zia_yao_ownerunit = copy_deepcopy(zia_ownerunit)
    zia_yao_ownerunit.set_owner_name(yao_str)
    assert len(zia_yao_ownerunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_ownerunit = listen_to_speaker_agenda(before_yao_ownerunit, zia_ownerunit)

    # THEN
    cook_rope = zia_ownerunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_ownerunit.get_plan_obj(cook_rope)
    after_dish_planunit = after_yao_ownerunit.get_plan_obj(dish_rope)
    after_casa_planunit = after_yao_ownerunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_ownerunit.get_plan_obj(fly_rope)
    print(f"{after_dish_planunit.mass=}")
    assert after_dish_planunit.mass != yao_dish_planunit.mass
    assert after_dish_planunit.mass == 1018
    print(f"{after_cook_planunit.mass=}")
    assert after_cook_planunit.mass != yao_cook_planunit.mass
    assert after_cook_planunit.mass == 19
    print(f"{after_casa_planunit.mass=}")
    assert after_casa_planunit.mass != 1
    assert after_casa_planunit.mass == 38
    assert after_yao_ownerunit == before_yao_ownerunit
    assert len(after_yao_ownerunit.get_agenda_dict()) == 3
    assert after_fly_planunit.mass != 1
    assert after_fly_planunit.mass == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalOwner():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = ownerunit_shop(yao_str)
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

    sue_ownerunit = ownerunit_shop(sue_str)
    sue_ownerunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_ownerunit.make_l1_rope(vacuum_str)
    sue_ownerunit.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = sue_ownerunit.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_ownerunit.make_l1_rope(egg_str)
    sue_ownerunit.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_ownerunit.make_l1_rope(chicken_str)
    sue_ownerunit.set_l1_plan(planunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_ownerunit.edit_plan_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rplan_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_ownerunit.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rplan_active_requisite=False,
    )
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._rational is False
    assert len(sue_ownerunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_owner_from_owner(yao_duty, yao_str)
    yao_vision.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_vision.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_vision.set_acct_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_ownerunit)
    yao_vision.settle_owner()

    # THEN irrational owner is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_acctunit = yao_vision.get_acct(zia_str)
    sue_acctunit = yao_vision.get_acct(sue_str)
    print(f"{sue_acctunit.acct_debt_points=}")
    print(f"{sue_acctunit._irrational_acct_debt_points=}")
    assert zia_acctunit._irrational_acct_debt_points == 0
    assert sue_acctunit._irrational_acct_debt_points == 51


def test_listen_to_speaker_agenda_ProcessesBarrenOwner():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = ownerunit_shop(yao_str)
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
    sue_vision = create_empty_owner_from_owner(yao_duty, sue_str)
    yao_vision = create_empty_owner_from_owner(yao_duty, yao_str)
    yao_vision.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_vision.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_vision.set_acct_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational owner is ignored
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
