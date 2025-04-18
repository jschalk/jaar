from src.a06_bud_logic.examples.example_buds import get_budunit_with_4_levels
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenBudUnit_Empty():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenSingleItemUnit_healerlink_any_group_label_exists_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.set_l1_item(itemunit_shop("Texas", healerlink=healerlink_shop({"Yao"})))
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})
    sue_bud.set_l1_item(
        itemunit_shop("Texas", healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})

    texas_str = "Texas"
    texas_road = sue_bud.make_l1_road(texas_str)
    sue_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_bud.set_item(itemunit_shop(ep_str, healerlink=yao_healerlink), texas_road)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    texas_road = sue_bud.make_l1_road(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_bud.set_l1_item(itemunit_shop(texas_str, healerlink=yao_healerlink))
    sue_bud.set_item(itemunit_shop("El Paso", problem_bool=True), texas_road)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_settle_bud_CorrectlyRaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    texas_road = sue_bud.make_l1_road(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_item = itemunit_shop(texas_str, healerlink=yao_healerlink)
    sue_bud.set_l1_item(texas_item)
    elpaso_item = itemunit_shop("El Paso", problem_bool=True)
    sue_bud.set_item(elpaso_item, texas_road)
    assert sue_bud._keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.settle_bud(keep_exceptions=True)
    assert (
        str(excinfo.value)
        == f"ItemUnit '{elpaso_item.get_road()}' cannot sponsor ancestor keeps."
    )


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_road = sue_bud.make_l1_road(texas_str)
    texas_item = itemunit_shop(texas_str, healerlink=yao_healerlink, problem_bool=True)
    sue_bud.set_l1_item(texas_item)
    elpaso_item = itemunit_shop("El Paso", healerlink=yao_healerlink, problem_bool=True)
    sue_bud.set_item(elpaso_item, texas_road)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_get_item_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_road = sue_bud.make_l1_road(texas_str)
    texas_item = itemunit_shop(texas_str, healerlink=yao_healerlink, problem_bool=True)
    sue_bud.set_l1_item(texas_item)
    elpaso_item = itemunit_shop("El Paso", healerlink=yao_healerlink, problem_bool=True)
    sue_bud.set_item(elpaso_item, texas_road)
    sue_bud.settle_bud()
    assert sue_bud._keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _keeps_justified={sue_bud._keeps_justified}."
    )
