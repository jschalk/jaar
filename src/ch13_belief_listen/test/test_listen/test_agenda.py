from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_belief_listen.listen_main import (
    create_empty_belief_from_belief,
    listen_to_speaker_agenda,
)


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_str = "Yao"
    yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_beliefunit, zia_beliefunit)

    # THEN
    assertion_fail_str = f"listener '{yao_str}' belief is assumed to have {zia_beliefunit.belief_name} voiceunit."
    assert str(excinfo.value) == assertion_fail_str


def test_listen_to_speaker_agenda_ReturnsEqualBelief():
    # ESTABLISH
    yao_str = "Yao"
    yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    yao_beliefunit.add_voiceunit(zia_str)
    yao_beliefunit.set_voice_respect(100)
    zia_beliefunit = beliefunit_shop(zia_str)

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(yao_beliefunit, zia_beliefunit)

    # THEN
    assert after_yao_beliefunit == yao_beliefunit


def test_listen_to_speaker_agenda_ReturnsSingletaskBelief():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_beliefunit.add_voiceunit(zia_str)
    yao_voice_voice_debt_lumen = 77
    before_yao_beliefunit.set_voice_respect(yao_voice_voice_debt_lumen)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, pledge=True)
    zia_clean_planunit.laborunit.add_party(yao_str)
    zia_beliefunit = beliefunit_shop(zia_str)
    zia_beliefunit.add_voiceunit(yao_str)
    zia_beliefunit.set_l1_plan(zia_clean_planunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(yao_str)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 1
    print(f"{zia_yao_beliefunit.get_agenda_dict()=}")

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    yao_clean_planunit = after_yao_beliefunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.star=}")
    assert yao_clean_planunit.star != zia_clean_planunit.star
    assert yao_clean_planunit.star == yao_voice_voice_debt_lumen
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2taskBelief():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_beliefunit.add_voiceunit(zia_str)
    yao_voice_debt_lumen = 77
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)
    zia_beliefunit = beliefunit_shop(zia_str)
    zia_beliefunit.add_voiceunit(yao_str)
    clean_str = "clean"
    zia_clean_planunit = planunit_shop(clean_str, pledge=True)
    zia_clean_planunit.laborunit.add_party(yao_str)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    zia_beliefunit.set_plan(zia_clean_planunit, casa_rope)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(yao_str)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 1
    print(f"{zia_yao_beliefunit.get_agenda_dict()=}")

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_rope(casa_rope, clean_str)
    yao_clean_planunit = after_yao_beliefunit.get_plan_obj(clean_rope)
    print(f"{yao_clean_planunit.star=}")
    assert yao_clean_planunit.star != zia_clean_planunit.star
    assert yao_clean_planunit.star == yao_voice_debt_lumen
    after_casa_planunit = after_yao_beliefunit.get_plan_obj(casa_rope)
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == yao_voice_debt_lumen
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2taskBelief():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_beliefunit.add_voiceunit(zia_str)
    yao_voice_debt_lumen = 55
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)

    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    zia_beliefunit.add_voiceunit(yao_str)
    clean_str = "clean"
    cook_str = "cook"
    fly_str = "fly"
    yao_clean_planunit = planunit_shop(clean_str, pledge=True)
    yao_clean_planunit.laborunit.add_party(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, pledge=True)
    yao_cook_planunit.laborunit.add_party(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, pledge=True)
    yao_fly_planunit.laborunit.add_party(yao_str)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    fly_rope = zia_beliefunit.make_l1_rope(fly_str)
    zia_beliefunit.set_plan(yao_clean_planunit, casa_rope)
    zia_beliefunit.set_plan(yao_cook_planunit, casa_rope)
    zia_beliefunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(yao_str)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_rope(casa_rope, clean_str)
    cook_rope = zia_beliefunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_beliefunit.get_plan_obj(cook_rope)
    after_clean_planunit = after_yao_beliefunit.get_plan_obj(clean_rope)
    after_casa_planunit = after_yao_beliefunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_beliefunit.get_plan_obj(fly_rope)
    print(f"{after_clean_planunit.star=}")
    assert after_clean_planunit.star != yao_clean_planunit.star
    assert after_clean_planunit.star == 19
    print(f"{after_cook_planunit.star=}")
    assert after_cook_planunit.star != yao_cook_planunit.star
    assert after_cook_planunit.star == 18
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == 37
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 3
    assert after_fly_planunit.star != 1
    assert after_fly_planunit.star == 18


def test_listen_to_speaker_agenda_Returns2AgendaPlansLevel2taskBeliefWhereAnPlanUnitExistsInAdvance():
    # ESTABLISH
    yao_str = "Yao"
    before_yao_beliefunit = beliefunit_shop(yao_str)
    zia_str = "Zia"
    before_yao_beliefunit.add_voiceunit(zia_str)
    yao_voice_debt_lumen = 55
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    zia_beliefunit.add_voiceunit(yao_str)
    dish_str = "dish"
    cook_str = "cook"
    fly_str = "fly"
    yao_dish_planunit = planunit_shop(dish_str, pledge=True)
    yao_dish_planunit.laborunit.add_party(yao_str)
    yao_cook_planunit = planunit_shop(cook_str, pledge=True)
    yao_cook_planunit.laborunit.add_party(yao_str)
    yao_fly_planunit = planunit_shop(fly_str, pledge=True)
    yao_fly_planunit.laborunit.add_party(yao_str)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    dish_rope = zia_beliefunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_beliefunit.make_l1_rope(fly_str)
    before_yao_dish_planunit = planunit_shop(dish_str, pledge=True)
    before_yao_dish_planunit.laborunit.add_party(yao_str)
    before_yao_beliefunit.set_plan(before_yao_dish_planunit, casa_rope)
    before_yao_beliefunit.edit_plan_attr(dish_rope, star=1000)
    zia_beliefunit.set_plan(yao_dish_planunit, casa_rope)
    zia_beliefunit.set_plan(yao_cook_planunit, casa_rope)
    zia_beliefunit.set_l1_plan(yao_fly_planunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(yao_str)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    cook_rope = zia_beliefunit.make_rope(casa_rope, cook_str)
    after_cook_planunit = after_yao_beliefunit.get_plan_obj(cook_rope)
    after_dish_planunit = after_yao_beliefunit.get_plan_obj(dish_rope)
    after_casa_planunit = after_yao_beliefunit.get_plan_obj(casa_rope)
    after_fly_planunit = after_yao_beliefunit.get_plan_obj(fly_rope)
    print(f"{after_dish_planunit.star=}")
    assert after_dish_planunit.star != yao_dish_planunit.star
    assert after_dish_planunit.star == 1018
    print(f"{after_cook_planunit.star=}")
    assert after_cook_planunit.star != yao_cook_planunit.star
    assert after_cook_planunit.star == 19
    print(f"{after_casa_planunit.star=}")
    assert after_casa_planunit.star != 1
    assert after_casa_planunit.star == 38
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 3
    assert after_fly_planunit.star != 1
    assert after_fly_planunit.star == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalBelief():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_str = "Sue"
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_duty.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_duty.set_voice_respect(yao_pool)

    sue_beliefunit = beliefunit_shop(sue_str)
    sue_beliefunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_beliefunit.make_l1_rope(vacuum_str)
    sue_beliefunit.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = sue_beliefunit.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.add_party(yao_str)

    egg_str = "egg first"
    egg_rope = sue_beliefunit.make_l1_rope(egg_str)
    sue_beliefunit.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_beliefunit.make_l1_rope(chicken_str)
    sue_beliefunit.set_l1_plan(planunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_beliefunit.edit_plan_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        plan_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_beliefunit.edit_plan_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        plan_active_requisite=False,
    )
    sue_beliefunit.cashout()
    assert sue_beliefunit.rational is False
    assert len(sue_beliefunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_belief_from_belief(yao_duty, yao_str)
    yao_vision.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_vision.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_vision.set_voice_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_beliefunit)
    yao_vision.cashout()

    # THEN irrational belief is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_voiceunit = yao_vision.get_voice(zia_str)
    sue_voiceunit = yao_vision.get_voice(sue_str)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 51


def test_listen_to_speaker_agenda_ProcessesBarrenBelief():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_str = "Sue"
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_duty.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_duty.set_voice_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_belief_from_belief(yao_duty, sue_str)
    yao_vision = create_empty_belief_from_belief(yao_duty, yao_str)
    yao_vision.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_vision.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_vision.set_voice_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational belief is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_voiceunit = yao_vision.get_voice(zia_str)
    sue_voiceunit = yao_vision.get_voice(sue_str)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert zia_voiceunit.inallocable_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.inallocable_voice_debt_lumen == 51
