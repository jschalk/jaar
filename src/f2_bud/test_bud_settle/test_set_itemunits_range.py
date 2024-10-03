from src.f2_bud.examples.example_buds import get_budunit_with_4_levels_and_2reasons
from src.f2_bud.item import itemunit_shop
from src.f2_bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyBudUnit():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    assert not root_item.begin
    assert not root_item.close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not root_item.begin
    assert not root_item.close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_DoesNotErrorWhenNoMathNodes():
    # ESTABLISH
    yao_bud = get_budunit_with_4_levels_and_2reasons()
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    assert not root_item._gogo_calc

    # WHEM
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not root_item._gogo_calc


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_SimpleNode():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    yao_bud.edit_item_attr(yao_bud._fiscal_id, begin=time0_begin, close=time0_close)
    yao_bud._set_item_dict()
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item._gogo_calc == time0_begin
    assert root_item._stop_calc == time0_close


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_NodeWith_denom():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 21
    time0_denom = 3
    yao_bud.edit_item_attr(
        yao_bud._fiscal_id,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
    )
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item.denom == time0_denom
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item._gogo_calc == time0_begin / time0_denom
    assert root_item._stop_calc == time0_close / time0_denom
    assert root_item._gogo_calc == 2
    assert root_item._stop_calc == 7


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_NodeWith_denom_numor():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_numor = 7
    time0_denom = 3
    yao_bud.edit_item_attr(
        yao_bud._fiscal_id,
        begin=time0_begin,
        close=time0_close,
        numor=time0_numor,
        denom=time0_denom,
    )
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item.numor == time0_numor
    assert root_item.denom == time0_denom
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item._gogo_calc == (time0_begin * time0_numor) / time0_denom
    assert root_item._stop_calc == (time0_close * time0_numor) / time0_denom
    assert root_item._gogo_calc == 14
    assert root_item._stop_calc == 42


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_addin = 7
    yao_bud.edit_item_attr(
        yao_bud._fiscal_id,
        begin=time0_begin,
        close=time0_close,
        addin=time0_addin,
    )
    yao_bud._set_item_dict()
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item.addin == time0_addin
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item._gogo_calc == time0_begin + time0_addin
    assert root_item._stop_calc == time0_close + time0_addin
    assert root_item._gogo_calc == 13
    assert root_item._stop_calc == 25


def test_BudUnit_set_itemtree_range_attrs_SetsInitialItem_gogo_calc_stop_calc_NodeWith_denom_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 6
    time0_close = 18
    time0_denom = 3
    time0_addin = 60
    yao_bud.edit_item_attr(
        yao_bud._fiscal_id,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
        addin=time0_addin,
    )
    yao_bud._set_item_dict()
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item.denom == time0_denom
    assert root_item.addin == time0_addin
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert root_item._gogo_calc == (time0_begin + time0_addin) / time0_denom
    assert root_item._stop_calc == (time0_close + time0_addin) / time0_denom
    assert root_item._gogo_calc == 22
    assert root_item._stop_calc == 26


def test_BudUnit_set_itemtree_range_attrs_SetsDescendentItem_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.set_item(itemunit_shop(time1_str), time0_road)
    time1_item = yao_bud.get_item_obj(time1_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert not time1_item._gogo_calc
    assert not time1_item._stop_calc
    assert yao_bud._range_inheritors == {}

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert not time1_item.begin
    assert not time1_item.close
    assert time1_item._gogo_calc == time0_begin
    assert time1_item._stop_calc == time0_close
    assert yao_bud._range_inheritors == {time1_road: time0_road}


def test_BudUnit_set_itemtree_range_attrs_SetsDescendentItem_gogo_calc_stop_calc_NodeWith_denom():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_denom = 7
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.set_item(itemunit_shop(time1_str, denom=time1_denom), time0_road)
    time1_item = yao_bud.get_item_obj(time1_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert not time1_item._gogo_calc
    assert not time1_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not time1_item.begin
    assert not time1_item.close
    assert time1_item._gogo_calc == time0_begin / time1_denom
    assert time1_item._stop_calc == time0_close / time1_denom
    assert time1_item._gogo_calc == 2
    assert time1_item._stop_calc == 5


def test_BudUnit_set_itemtree_range_attrs_SetsDescendentItem_gogo_calc_stop_calc_NodeWith_denom_numor():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_denom = 7
    time1_numor = 3
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_item = itemunit_shop(time1_str, numor=time1_numor, denom=time1_denom)
    yao_bud.set_item(temp_item, time0_road)
    time1_item = yao_bud.get_item_obj(time1_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert not time1_item._gogo_calc
    assert not time1_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not time1_item.begin
    assert not time1_item.close
    assert time1_item._gogo_calc == (time0_begin * time1_numor) / time1_denom
    assert time1_item._stop_calc == (time0_close * time1_numor) / time1_denom
    assert time1_item._gogo_calc == 6
    assert time1_item._stop_calc == 15


def test_BudUnit_set_itemtree_range_attrs_SetsDescendentItem_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_addin = 5
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_item = itemunit_shop(time1_str, addin=time1_addin)
    yao_bud.set_item(temp_item, time0_road)
    time1_item = yao_bud.get_item_obj(time1_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert time1_item.addin == time1_addin
    assert not time1_item._gogo_calc
    assert not time1_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not time1_item.begin
    assert not time1_item.close
    assert time1_item._gogo_calc == time0_item._gogo_calc + time1_addin
    assert time1_item._stop_calc == time0_item._stop_calc + time1_addin
    assert time1_item._gogo_calc == 8
    assert time1_item._stop_calc == 12


def test_BudUnit_set_itemtree_range_attrs_Sets2LevelsDescendentItem_gogo_calc_stop_calc_NodeWith_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_road = yao_bud.make_road(time0_road, time1_str)
    yao_bud.add_item(time1_road)
    time2_str = "time2"
    time2_road = yao_bud.make_road(time1_road, time2_str)
    time2_addin = 5
    x_time2_item = itemunit_shop(time2_str, addin=time2_addin)
    yao_bud.set_item(x_time2_item, time1_road)
    time2_item = yao_bud.get_item_obj(time2_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time2_item.begin != time0_begin
    assert time2_item.close != time0_close
    assert time2_item.addin == time2_addin
    assert not time2_item._gogo_calc
    assert not time2_item._stop_calc
    assert yao_bud._range_inheritors == {}

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not time2_item.begin
    assert not time2_item.close
    assert time2_item._gogo_calc == time0_item._gogo_calc + time2_addin
    assert time2_item._stop_calc == time0_item._stop_calc + time2_addin
    assert time2_item._gogo_calc == 8
    assert time2_item._stop_calc == 12
    assert yao_bud._range_inheritors == {time1_road: time0_road, time2_road: time0_road}


def test_BudUnit_set_itemtree_range_attrs_SetsDescendentItem_gogo_calc_stop_calc_NodeWith_denom_addin():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_str = "time0"
    time0_road = yao_bud.make_l1_road(time0_str)
    time0_begin = 21
    time0_close = 35
    time0_item = itemunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_bud.set_l1_item(time0_item)

    time1_str = "time1"
    time1_addin = 70
    time1_denom = 7
    time1_road = yao_bud.make_road(time0_road, time1_str)
    temp_item = itemunit_shop(time1_str, denom=time1_denom, addin=time1_addin)
    yao_bud.set_item(temp_item, time0_road)
    time1_item = yao_bud.get_item_obj(time1_road)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
    yao_bud._set_item_dict()
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert time0_item.begin == time0_begin
    assert time0_item.close == time0_close
    assert time1_item.begin != time0_begin
    assert time1_item.close != time0_close
    assert time1_item.addin == time1_addin
    assert not time1_item._gogo_calc
    assert not time1_item._stop_calc

    # WHEN
    yao_bud._set_itemtree_range_attrs()

    # THEN
    assert not time1_item.begin
    assert not time1_item.close
    assert time1_item._gogo_calc == (time0_item._gogo_calc + time1_addin) / time1_denom
    assert time1_item._stop_calc == (time0_item._stop_calc + time1_addin) / time1_denom
    assert time1_item._gogo_calc == 13
    assert time1_item._stop_calc == 15
