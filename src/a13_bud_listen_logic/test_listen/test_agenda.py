from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a13_bud_listen_logic.listen import (
    listen_to_speaker_agenda,
    create_empty_bud_from_bud,
)
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
        == f"listener '{yao_str}' bud is assumed to have {zia_budunit.owner_name} acctunit."
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
    zia_clean_itemunit = itemunit_shop(clean_str, pledge=True)
    zia_clean_itemunit.teamunit.set_teamlink(yao_str)
    zia_budunit = budunit_shop(zia_str)
    zia_budunit.add_acctunit(yao_str)
    zia_budunit.set_l1_item(zia_clean_itemunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_name(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_str)
    yao_clean_itemunit = after_yao_budunit.get_item_obj(clean_road)
    print(f"{yao_clean_itemunit.mass=}")
    assert yao_clean_itemunit.mass != zia_clean_itemunit.mass
    assert yao_clean_itemunit.mass == yao_acct_debtit_belief
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
    zia_clean_itemunit = itemunit_shop(clean_str, pledge=True)
    zia_clean_itemunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    zia_budunit.set_item(zia_clean_itemunit, casa_road)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_name(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 1
    print(f"{zia_yao_budunit.get_agenda_dict()=}")

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_str)
    yao_clean_itemunit = after_yao_budunit.get_item_obj(clean_road)
    print(f"{yao_clean_itemunit.mass=}")
    assert yao_clean_itemunit.mass != zia_clean_itemunit.mass
    assert yao_clean_itemunit.mass == yao_debtit_belief
    after_casa_itemunit = after_yao_budunit.get_item_obj(casa_road)
    print(f"{after_casa_itemunit.mass=}")
    assert after_casa_itemunit.mass != 1
    assert after_casa_itemunit.mass == yao_debtit_belief
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaItemsLevel2TaskBud():
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
    yao_clean_itemunit = itemunit_shop(clean_str, pledge=True)
    yao_clean_itemunit.teamunit.set_teamlink(yao_str)
    yao_cook_itemunit = itemunit_shop(cook_str, pledge=True)
    yao_cook_itemunit.teamunit.set_teamlink(yao_str)
    yao_fly_itemunit = itemunit_shop(fly_str, pledge=True)
    yao_fly_itemunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    fly_road = zia_budunit.make_l1_road(fly_str)
    zia_budunit.set_item(yao_clean_itemunit, casa_road)
    zia_budunit.set_item(yao_cook_itemunit, casa_road)
    zia_budunit.set_l1_item(yao_fly_itemunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_name(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    clean_road = zia_budunit.make_road(casa_road, clean_str)
    cook_road = zia_budunit.make_road(casa_road, cook_str)
    after_cook_itemunit = after_yao_budunit.get_item_obj(cook_road)
    after_clean_itemunit = after_yao_budunit.get_item_obj(clean_road)
    after_casa_itemunit = after_yao_budunit.get_item_obj(casa_road)
    after_fly_itemunit = after_yao_budunit.get_item_obj(fly_road)
    print(f"{after_clean_itemunit.mass=}")
    assert after_clean_itemunit.mass != yao_clean_itemunit.mass
    assert after_clean_itemunit.mass == 19
    print(f"{after_cook_itemunit.mass=}")
    assert after_cook_itemunit.mass != yao_cook_itemunit.mass
    assert after_cook_itemunit.mass == 18
    print(f"{after_casa_itemunit.mass=}")
    assert after_casa_itemunit.mass != 1
    assert after_casa_itemunit.mass == 37
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_itemunit.mass != 1
    assert after_fly_itemunit.mass == 18


def test_listen_to_speaker_agenda_Returns2AgendaItemsLevel2TaskBudWhereAnItemUnitExistsInAdvance():
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
    yao_dish_itemunit = itemunit_shop(dish_str, pledge=True)
    yao_dish_itemunit.teamunit.set_teamlink(yao_str)
    yao_cook_itemunit = itemunit_shop(cook_str, pledge=True)
    yao_cook_itemunit.teamunit.set_teamlink(yao_str)
    yao_fly_itemunit = itemunit_shop(fly_str, pledge=True)
    yao_fly_itemunit.teamunit.set_teamlink(yao_str)
    casa_road = zia_budunit.make_l1_road("casa")
    dish_road = zia_budunit.make_road(casa_road, dish_str)
    fly_road = zia_budunit.make_l1_road(fly_str)
    before_yao_dish_itemunit = itemunit_shop(dish_str, pledge=True)
    before_yao_dish_itemunit.teamunit.set_teamlink(yao_str)
    before_yao_budunit.set_item(before_yao_dish_itemunit, casa_road)
    before_yao_budunit.edit_item_attr(dish_road, mass=1000)
    zia_budunit.set_item(yao_dish_itemunit, casa_road)
    zia_budunit.set_item(yao_cook_itemunit, casa_road)
    zia_budunit.set_l1_item(yao_fly_itemunit)
    assert len(zia_budunit.get_agenda_dict()) == 0
    zia_yao_budunit = copy_deepcopy(zia_budunit)
    zia_yao_budunit.set_owner_name(yao_str)
    assert len(zia_yao_budunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_budunit = listen_to_speaker_agenda(before_yao_budunit, zia_budunit)

    # THEN
    cook_road = zia_budunit.make_road(casa_road, cook_str)
    after_cook_itemunit = after_yao_budunit.get_item_obj(cook_road)
    after_dish_itemunit = after_yao_budunit.get_item_obj(dish_road)
    after_casa_itemunit = after_yao_budunit.get_item_obj(casa_road)
    after_fly_itemunit = after_yao_budunit.get_item_obj(fly_road)
    print(f"{after_dish_itemunit.mass=}")
    assert after_dish_itemunit.mass != yao_dish_itemunit.mass
    assert after_dish_itemunit.mass == 1018
    print(f"{after_cook_itemunit.mass=}")
    assert after_cook_itemunit.mass != yao_cook_itemunit.mass
    assert after_cook_itemunit.mass == 19
    print(f"{after_casa_itemunit.mass=}")
    assert after_casa_itemunit.mass != 1
    assert after_casa_itemunit.mass == 38
    assert after_yao_budunit == before_yao_budunit
    assert len(after_yao_budunit.get_agenda_dict()) == 3
    assert after_fly_itemunit.mass != 1
    assert after_fly_itemunit.mass == 18


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
    sue_budunit.set_l1_item(itemunit_shop(vacuum_str, pledge=True))
    vacuum_itemunit = sue_budunit.get_item_obj(vacuum_road)
    vacuum_itemunit.teamunit.set_teamlink(yao_str)

    egg_str = "egg first"
    egg_road = sue_budunit.make_l1_road(egg_str)
    sue_budunit.set_l1_item(itemunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_road = sue_budunit.make_l1_road(chicken_str)
    sue_budunit.set_l1_item(itemunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_budunit.edit_item_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_item_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_budunit.edit_item_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_item_active_requisite=False,
    )
    sue_budunit.settle_bud()
    assert sue_budunit._rational is False
    assert len(sue_budunit.get_agenda_dict()) == 3

    # WHEN
    yao_plan = create_empty_bud_from_bud(yao_duty, yao_str)
    yao_plan.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_plan.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_plan.set_acct_respect(yao_pool)
    yao_plan = listen_to_speaker_agenda(yao_plan, sue_budunit)
    yao_plan.settle_bud()

    # THEN irrational bud is ignored
    assert len(yao_plan.get_agenda_dict()) != 3
    assert len(yao_plan.get_agenda_dict()) == 0
    zia_acctunit = yao_plan.get_acct(zia_str)
    sue_acctunit = yao_plan.get_acct(sue_str)
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
    sue_plan = create_empty_bud_from_bud(yao_duty, sue_str)
    yao_plan = create_empty_bud_from_bud(yao_duty, yao_str)
    yao_plan.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_plan.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_plan.set_acct_respect(yao_pool)
    yao_plan = listen_to_speaker_agenda(yao_plan, speaker=sue_plan)

    # THEN irrational bud is ignored
    assert len(yao_plan.get_agenda_dict()) != 3
    assert len(yao_plan.get_agenda_dict()) == 0
    zia_acctunit = yao_plan.get_acct(zia_str)
    sue_acctunit = yao_plan.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51
