from src.a01_road_logic.road import (
    create_road,
    get_default_fisc_tag as root_tag,
    to_road,
)
from src.a04_reason_logic.reason_item import reasonunit_shop, factunit_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fisc_tag_CorrectlySetsAttr():
    # ESTABLISH
    x_fisc_tag = "accord45"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert sue_bud.fisc_tag == root_tag()

    # WHEN
    sue_bud.set_fisc_tag(fisc_tag=x_fisc_tag)

    # THEN
    assert sue_bud.fisc_tag == x_fisc_tag


def test_BudUnit_set_item_CorrectlySetsfisc_tag_AND_fund_coin():
    # ESTABLISH'
    x_fund_coin = 500
    sue_bud = get_budunit_with_4_levels()
    sue_bud.fund_coin = x_fund_coin
    bud_fisc_tag = "Texas"
    sue_bud.set_fisc_tag(bud_fisc_tag)
    assert sue_bud.fisc_tag == bud_fisc_tag

    casa_road = sue_bud.make_l1_road("casa")
    clean_road = sue_bud.make_road(casa_road, "cleaning")
    cookery_str = "cookery to use"
    cookery_road = sue_bud.make_road(clean_road, cookery_str)

    # WHEN
    sue_bud.set_item(itemunit_shop(cookery_str), clean_road)

    # THEN
    cookery_item = sue_bud.get_item_obj(cookery_road)
    assert cookery_item.fisc_tag == bud_fisc_tag
    assert cookery_item.fund_coin == x_fund_coin


def test_bud_set_fisc_tag_CorrectlySetsAttr():
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
    assert yao_bud.itemroot.item_tag == yao_bud.fisc_tag
    casa_item = yao_bud.get_item_obj(old_casa_road)
    assert casa_item.parent_road == to_road(yao_bud.fisc_tag)
    swim_item = yao_bud.get_item_obj(old_swim_road)
    assert swim_item.parent_road == old_casa_road
    assert yao_bud.fisc_tag == yao_bud.fisc_tag

    # WHEN
    x_fisc_tag = "accord45"
    yao_bud.set_fisc_tag(fisc_tag=x_fisc_tag)

    # THEN
    new_casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    new_swim_road = yao_bud.make_road(new_casa_road, swim_str)
    assert yao_bud.fisc_tag == x_fisc_tag
    assert yao_bud.itemroot.item_tag == x_fisc_tag
    casa_item = yao_bud.get_item_obj(new_casa_road)
    assert casa_item.parent_road == to_road(x_fisc_tag)
    swim_item = yao_bud.get_item_obj(new_swim_road)
    assert swim_item.parent_road == new_casa_road


def test_bud_set_bridge_RaisesErrorIfNew_bridge_IsAnItem_tag():
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
        == f"Cannot modify bridge to '{slash_str}' because it exists an item item_tag '{casa_road}'"
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
    # print(f"{zia_bud.fisc_tag=} {zia_bud.itemroot.item_tag=} {casa_road=}")
    # print(f"{cook_item.parent_road=} {cook_item.item_tag=}")
    # semicolon_casa_item = zia_bud.get_item_obj(semicolon_casa_road)
    # print(f"{semicolon_casa_item.parent_road=} {semicolon_casa_item.item_tag=}")
    assert cook_item.get_road() == semicolon_cook_road

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    assert cook_item.get_road() != semicolon_cook_road
    zia_fisc_tag = zia_bud.fisc_tag
    slash_casa_road = create_road(zia_fisc_tag, casa_str, bridge=slash_str)
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
    assert gen_time_factunit.fbase is not None
    assert gen_time_factunit.fbase == slash_time_road
    assert gen_time_factunit.fneed is not None
    assert gen_time_factunit.fneed == slash_8am_road

    assert casa_item.factunits.get(semicolon_time_road) is None


def test_BudUnit_set_bridge_CorrectlySetsAttr():
    # ESTABLISH
    x_fisc_tag = "accord45"
    slash_bridge = "/"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, x_fisc_tag, bridge=slash_bridge)
    assert sue_bud.bridge == slash_bridge

    # WHEN
    at_tag_bridge = "@"
    sue_bud.set_bridge(new_bridge=at_tag_bridge)

    # THEN
    assert sue_bud.bridge == at_tag_bridge
