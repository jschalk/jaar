from src.a01_word_logic.road import create_road, get_default_fisc_title as root_title
from src.f02_bud.reason_item import reasonunit_shop, factunit_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.examples.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fisc_title_CorrectlySetsAttr():
    # ESTABLISH
    x_fisc_title = "accord45"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert sue_bud.fisc_title == root_title()

    # WHEN
    sue_bud.set_fisc_title(fisc_title=x_fisc_title)

    # THEN
    assert sue_bud.fisc_title == x_fisc_title


def test_BudUnit_set_item_CorrectlySetsfisc_title_AND_fund_coin():
    # ESTABLISH'
    x_fund_coin = 500
    sue_bud = get_budunit_with_4_levels()
    sue_bud.fund_coin = x_fund_coin
    bud_fisc_title = "Texas"
    sue_bud.set_fisc_title(bud_fisc_title)
    assert sue_bud.fisc_title == bud_fisc_title

    casa_road = sue_bud.make_l1_road("casa")
    clean_road = sue_bud.make_road(casa_road, "cleaning")
    cookery_str = "cookery to use"
    cookery_road = sue_bud.make_road(clean_road, cookery_str)

    # WHEN
    sue_bud.set_item(itemunit_shop(cookery_str), clean_road)

    # THEN
    cookery_item = sue_bud.get_item_obj(cookery_road)
    assert cookery_item.fisc_title == bud_fisc_title
    assert cookery_item.fund_coin == x_fund_coin


def test_bud_set_fisc_title_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    casa_str = "casa"
    old_casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    old_swim_road = yao_bud.make_road(old_casa_road, swim_str)
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    yao_bud.set_item(itemunit_shop(swim_str), parent_road=old_casa_road)
    assert yao_bud.owner_name == yao_str
    assert yao_bud.itemroot.item_title == yao_bud.fisc_title
    casa_item = yao_bud.get_item_obj(old_casa_road)
    assert casa_item.parent_road == yao_bud.fisc_title
    swim_item = yao_bud.get_item_obj(old_swim_road)
    assert swim_item.parent_road == old_casa_road
    assert yao_bud.fisc_title == yao_bud.fisc_title

    # WHEN
    x_fisc_title = "accord45"
    yao_bud.set_fisc_title(fisc_title=x_fisc_title)

    # THEN
    new_casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    new_swim_road = yao_bud.make_road(new_casa_road, swim_str)
    assert yao_bud.fisc_title == x_fisc_title
    assert yao_bud.itemroot.item_title == x_fisc_title
    casa_item = yao_bud.get_item_obj(new_casa_road)
    assert casa_item.parent_road == x_fisc_title
    swim_item = yao_bud.get_item_obj(new_swim_road)
    assert swim_item.parent_road == new_casa_road


def test_bud_set_bridge_RaisesErrorIfNew_bridge_IsAnItem_title():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    print(f"{zia_bud.max_tree_traverse=}")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_bud.set_item(itemunit_shop(casa_str), parent_road=casa_road)

    # WHEN / THEN
    casa_road = zia_bud.make_road(casa_road, casa_str)
    print(f"{casa_road=}")
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_bridge(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify bridge to '{slash_str}' because it exists an item item_title '{casa_road}'"
    )


def test_bud_set_bridge_CorrectlyModifies_parent_road():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    semicolon_casa_road = zia_bud.make_l1_road(casa_str)
    cook_str = "cook"
    zia_bud.set_item(itemunit_shop(cook_str), semicolon_casa_road)
    semicolon_cook_road = zia_bud.make_road(semicolon_casa_road, cook_str)
    cook_item = zia_bud.get_item_obj(semicolon_cook_road)
    semicolon_str = ";"
    assert zia_bud.bridge == semicolon_str
    semicolon_cook_road = zia_bud.make_road(semicolon_casa_road, cook_str)
    # print(f"{zia_bud.fisc_title=} {zia_bud.itemroot.item_title=} {casa_road=}")
    # print(f"{cook_item.parent_road=} {cook_item.item_title=}")
    # semicolon_casa_item = zia_bud.get_item_obj(semicolon_casa_road)
    # print(f"{semicolon_casa_item.parent_road=} {semicolon_casa_item.item_title=}")
    assert cook_item.get_road() == semicolon_cook_road

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    assert cook_item.get_road() != semicolon_cook_road
    zia_fisc_title = zia_bud.fisc_title
    slash_casa_road = create_road(zia_fisc_title, casa_str, bridge=slash_str)
    slash_cook_road = create_road(slash_casa_road, cook_str, bridge=slash_str)
    assert cook_item.get_road() == slash_cook_road


def test_bud_set_bridge_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    time_str = "time"
    semicolon_time_road = zia_bud.make_l1_road(time_str)
    _8am_str = "8am"
    semicolon_8am_road = zia_bud.make_road(semicolon_time_road, _8am_str)

    semicolon_time_reasonunit = reasonunit_shop(base=semicolon_time_road)
    semicolon_time_reasonunit.set_premise(semicolon_8am_road)

    semicolon_casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.edit_item_attr(road=semicolon_casa_road, reason=semicolon_time_reasonunit)
    casa_item = zia_bud.get_item_obj(semicolon_casa_road)
    assert casa_item.reasonunits.get(semicolon_time_road) is not None
    gen_time_reasonunit = casa_item.reasonunits.get(semicolon_time_road)
    assert gen_time_reasonunit.premises.get(semicolon_8am_road) is not None

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_road = zia_bud.make_l1_road(time_str)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_str)
    slash_casa_road = zia_bud.make_l1_road(casa_str)
    casa_item = zia_bud.get_item_obj(slash_casa_road)
    slash_time_road = zia_bud.make_l1_road(time_str)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_str)
    assert casa_item.reasonunits.get(slash_time_road) is not None
    gen_time_reasonunit = casa_item.reasonunits.get(slash_time_road)
    assert gen_time_reasonunit.premises.get(slash_8am_road) is not None

    assert casa_item.reasonunits.get(semicolon_time_road) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_road) is None


def test_bud_set_bridge_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    time_str = "time"
    semicolon_time_road = zia_bud.make_l1_road(time_str)
    _8am_str = "8am"
    semicolon_8am_road = zia_bud.make_road(semicolon_time_road, _8am_str)
    semicolon_time_factunit = factunit_shop(semicolon_time_road, semicolon_8am_road)

    semicolon_casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.edit_item_attr(semicolon_casa_road, factunit=semicolon_time_factunit)
    casa_item = zia_bud.get_item_obj(semicolon_casa_road)
    print(f"{casa_item.factunits=} {semicolon_time_road=}")
    assert casa_item.factunits.get(semicolon_time_road) is not None
    gen_time_factunit = casa_item.factunits.get(semicolon_time_road)

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_road = zia_bud.make_l1_road(time_str)
    slash_casa_road = zia_bud.make_l1_road(casa_str)
    casa_item = zia_bud.get_item_obj(slash_casa_road)
    slash_time_road = zia_bud.make_l1_road(time_str)
    slash_8am_road = zia_bud.make_road(slash_time_road, _8am_str)
    assert casa_item.factunits.get(slash_time_road) is not None
    gen_time_factunit = casa_item.factunits.get(slash_time_road)
    assert gen_time_factunit.base is not None
    assert gen_time_factunit.base == slash_time_road
    assert gen_time_factunit.pick is not None
    assert gen_time_factunit.pick == slash_8am_road

    assert casa_item.factunits.get(semicolon_time_road) is None
