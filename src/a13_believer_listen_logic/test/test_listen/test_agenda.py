from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a13_believer_listen_logic.listen_main import (
    create_empty_believer_from_believer,
    listen_to_speaker_agenda,
)


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_str = "Yao"
    yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_believerunit, zia_believerunit)
    assert (
        str(excinfo.value)
        == f"listener '{yao_str}' believer is assumed to have {zia_believerunit.believer_name} partnerunit."
    )


def test_listen_to_speaker_agenda_ReturnsEqualBeliever():
    # ESTABLISH
    yao_str = "Yao"
    yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    yao_believerunit.add_partnerunit(zia_str)
    yao_believerunit.set_partner_respect(100)
    zia_believerunit = believerunit_shop(zia_str)

    # WHEN
    after_yao_believerunit = listen_to_speaker_agenda(
        yao_believerunit, zia_believerunit
    )

    # THEN
    assert after_yao_believerunit == yao_believerunit


def test_listen_to_speaker_agenda_ReturnsSingleChoreBeliever():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_believerunit.add_partnerunit(zia_str)
    yao_partner_partner_debt_points = 77
    before_yao_believerunit.set_partner_respect(yao_partner_partner_debt_points)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, task=True)
    zia_clean_planunit.laborunit.add_partyunit(yao_str)
    zia_believerunit = believerunit_shop(zia_str)
    zia_believerunit.add_partnerunit(yao_str)
    zia_believerunit.set_l1_plan(zia_clean_planunit)
    assert len(zia_believerunit.get_agenda_dict()) == 0
    zia_yao_believerunit = copy_deepcopy(zia_believerunit)
    zia_yao_believerunit.set_believer_name(yao_str)
    assert len(zia_yao_believerunit.get_agenda_dict()) == 1
    print(f"{zia_yao_believerunit.get_agenda_dict()=}")

    # WHEN
    after_yao_believerunit = listen_to_speaker_agenda(
        before_yao_believerunit, zia_believerunit
    )

    # THEN
    clean_rope = zia_believerunit.make_l1_rope(clean_str)
    yao_clean_planunit = after_yao_believerunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.star=}")
    assert yao_clean_planunit.star != zia_clean_planunit.star
    assert yao_clean_planunit.star == yao_partner_partner_debt_points
    assert after_yao_believerunit == before_yao_believerunit
    assert len(after_yao_believerunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2ChoreBeliever():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_believerunit.add_partnerunit(zia_str)
    yao_partner_debt_points = 77
    before_yao_believerunit.set_partner_respect(yao_partner_debt_points)
    zia_believerunit = believerunit_shop(zia_str)
    zia_believerunit.add_partnerunit(yao_str)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, task=True)
    zia_clean_planunit.laborunit.add_partyunit(yao_str)
    casa_rope = zia_believerunit.make_l1_rope("casa")
    zia_believerunit.set_plan(zia_clean_planunit, casa_rope)
    assert len(zia_believerunit.get_agenda_dict()) == 0
    zia_yao_believerunit = copy_deepcopy(zia_believerunit)
    zia_yao_believerunit.set_believer_name(yao_str)
    assert len(zia_yao_believerunit.get_agenda_dict()) == 1
    print(f"{zia_yao_believerunit.get_agenda_dict()=}")

    # WHEN
    after_yao_believerunit = listen_to_speaker_agenda(
        before_yao_believerunit, zia_believerunit
    )

    # THEN
    clean_rope = zia_believerunit.make_rope(casa_rope, clean_str)
    yao_clean_planunit = after_yao_believerunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.star=}")
    assert yao_clean_planunit.star != zia_clean_planunit.star
    assert yao_clean_planunit.star == yao_partner_debt_points
    after_casa_planunit = after_yao_believerunit.get_plan_obj(casa_rope)
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == yao_partner_debt_points
    assert after_yao_believerunit == before_yao_believerunit
    assert len(after_yao_believerunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2ChoreBeliever():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_believerunit.add_partnerunit(zia_str)
    yao_partner_debt_points = 55
    before_yao_believerunit.set_partner_respect(yao_partner_debt_points)

    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    zia_believerunit.add_partnerunit(yao_str)
    clean_str = "clean"
    cook_str = "cook"
    fly_str = "fly"
    yao_clean_planunit = planunit_shop(clean_str, task=True)
    yao_clean_planunit.laborunit.add_partyunit(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, task=True)
    yao_cook_planunit.laborunit.add_partyunit(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, task=True)
    yao_fly_planunit.laborunit.add_partyunit(yao_str)
    casa_rope = zia_believerunit.make_l1_rope("casa")
    fly_rope = zia_believerunit.make_l1_rope(fly_str)
    zia_believerunit.set_plan(yao_clean_planunit, casa_rope)
    zia_believerunit.set_plan(yao_cook_planunit, casa_rope)
    zia_believerunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_believerunit.get_agenda_dict()) == 0
    zia_yao_believerunit = copy_deepcopy(zia_believerunit)
    zia_yao_believerunit.set_believer_name(yao_str)
    assert len(zia_yao_believerunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_believerunit = listen_to_speaker_agenda(
        before_yao_believerunit, zia_believerunit
    )

    # THEN
    clean_rope = zia_believerunit.make_rope(casa_rope, clean_str)
    cook_rope = zia_believerunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_believerunit.get_plan_obj(cook_rope)
    after_clean_planunit = after_yao_believerunit.get_plan_obj(clean_rope)
    after_casa_planunit = after_yao_believerunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_believerunit.get_plan_obj(fly_rope)
    print(f"{after_clean_planunit.star=}")
    assert after_clean_planunit.star != yao_clean_planunit.star
    assert after_clean_planunit.star == 19
    print(f"{after_cook_planunit.star=}")
    assert after_cook_planunit.star != yao_cook_planunit.star
    assert after_cook_planunit.star == 18
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == 37
    assert after_yao_believerunit == before_yao_believerunit
    assert len(after_yao_believerunit.get_agenda_dict()) == 3
    assert after_fly_planunit.star != 1
    assert after_fly_planunit.star == 18


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2ChoreBelieverWhereAnPlanUnitExistsInAdvance():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_believerunit = believerunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_believerunit.add_partnerunit(zia_str)
    yao_partner_debt_points = 55
    before_yao_believerunit.set_partner_respect(yao_partner_debt_points)
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    zia_believerunit.add_partnerunit(yao_str)
    dish_str = "dish"
    cook_str = "cook"
    fly_str = "fly"
    yao_dish_planunit = planunit_shop(dish_str, task=True)
    yao_dish_planunit.laborunit.add_partyunit(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, task=True)
    yao_cook_planunit.laborunit.add_partyunit(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, task=True)
    yao_fly_planunit.laborunit.add_partyunit(yao_str)
    casa_rope = zia_believerunit.make_l1_rope("casa")
    dish_rope = zia_believerunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_believerunit.make_l1_rope(fly_str)
    before_yao_dish_planunit = planunit_shop(dish_str, task=True)
    before_yao_dish_planunit.laborunit.add_partyunit(yao_str)
    before_yao_believerunit.set_plan(before_yao_dish_planunit, casa_rope)
    before_yao_believerunit.edit_plan_attr(dish_rope, star=1000)
    zia_believerunit.set_plan(yao_dish_planunit, casa_rope)
    zia_believerunit.set_plan(yao_cook_planunit, casa_rope)
    zia_believerunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_believerunit.get_agenda_dict()) == 0
    zia_yao_believerunit = copy_deepcopy(zia_believerunit)
    zia_yao_believerunit.set_believer_name(yao_str)
    assert len(zia_yao_believerunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_believerunit = listen_to_speaker_agenda(
        before_yao_believerunit, zia_believerunit
    )

    # THEN
    cook_rope = zia_believerunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_believerunit.get_plan_obj(cook_rope)
    after_dish_planunit = after_yao_believerunit.get_plan_obj(dish_rope)
    after_casa_planunit = after_yao_believerunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_believerunit.get_plan_obj(fly_rope)
    print(f"{after_dish_planunit.star=}")
    assert after_dish_planunit.star != yao_dish_planunit.star
    assert after_dish_planunit.star == 1018
    print(f"{after_cook_planunit.star=}")
    assert after_cook_planunit.star != yao_cook_planunit.star
    assert after_cook_planunit.star == 19
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == 38
    assert after_yao_believerunit == before_yao_believerunit
    assert len(after_yao_believerunit.get_agenda_dict()) == 3
    assert after_fly_planunit.star != 1
    assert after_fly_planunit.star == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalBeliever():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    sue_str = "Sue"
    sue_partner_cred_points = 57
    sue_partner_debt_points = 51
    yao_duty.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_duty.add_partnerunit(sue_str, sue_partner_cred_points, sue_partner_debt_points)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)

    sue_believerunit = believerunit_shop(sue_str)
    sue_believerunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_believerunit.make_l1_rope(vacuum_str)
    sue_believerunit.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = sue_believerunit.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.add_partyunit(yao_str)

    egg_str = "egg first"
    egg_rope = sue_believerunit.make_l1_rope(egg_str)
    sue_believerunit.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_believerunit.make_l1_rope(chicken_str)
    sue_believerunit.set_l1_plan(planunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_believerunit.edit_plan_attr(
        egg_rope,
        task=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_believerunit.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_context=egg_rope,
        reason_plan_active_requisite=False,
    )
    sue_believerunit.settle_believer()
    assert sue_believerunit._rational is False
    assert len(sue_believerunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_believer_from_believer(yao_duty, yao_str)
    yao_vision.add_partnerunit(
        zia_str, zia_partner_cred_points, zia_partner_debt_points
    )
    yao_vision.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    yao_vision.set_partner_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_believerunit)
    yao_vision.settle_believer()

    # THEN irrational believer is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_partnerunit = yao_vision.get_partner(zia_str)
    sue_partnerunit = yao_vision.get_partner(sue_str)
    print(f"{sue_partnerunit.partner_debt_points=}")
    print(f"{sue_partnerunit._irrational_partner_debt_points=}")
    assert zia_partnerunit._irrational_partner_debt_points == 0
    assert sue_partnerunit._irrational_partner_debt_points == 51


def test_listen_to_speaker_agenda_ProcessesBarrenBeliever():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    sue_str = "Sue"
    sue_partner_cred_points = 57
    sue_partner_debt_points = 51
    yao_duty.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_duty.add_partnerunit(sue_str, sue_partner_cred_points, sue_partner_debt_points)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_believer_from_believer(yao_duty, sue_str)
    yao_vision = create_empty_believer_from_believer(yao_duty, yao_str)
    yao_vision.add_partnerunit(
        zia_str, zia_partner_cred_points, zia_partner_debt_points
    )
    yao_vision.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    yao_vision.set_partner_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational believer is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_partnerunit = yao_vision.get_partner(zia_str)
    sue_partnerunit = yao_vision.get_partner(sue_str)
    print(f"{sue_partnerunit.partner_debt_points=}")
    print(f"{sue_partnerunit._irrational_partner_debt_points=}")
    assert zia_partnerunit._irrational_partner_debt_points == 0
    assert zia_partnerunit._inallocable_partner_debt_points == 0
    assert sue_partnerunit._irrational_partner_debt_points == 0
    assert sue_partnerunit._inallocable_partner_debt_points == 51
