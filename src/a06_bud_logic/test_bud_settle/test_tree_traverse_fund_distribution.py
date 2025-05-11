from src.a01_way_logic.way import WayUnit, to_way
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import awardlink_shop, awardline_shop
from src.a05_item_logic.item import itemunit_shop, ItemUnit
from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a06_bud_logic._utils.example_buds import (
    budunit_v001,
    budunit_v001_with_large_agenda,
    get_budunit_with7amCleanTableReason,
    get_budunit_with_4_levels,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass


def test_BudUnit_settle_bud_Sets_itemunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_budunit = get_budunit_with7amCleanTableReason()
    casa_way = x_budunit.make_l1_way("casa")
    catt_way = x_budunit.make_l1_way("cat have dinner")
    week_way = x_budunit.make_l1_way("weekdays")
    x_budunit.itemroot._fund_onset = 13
    x_budunit.itemroot._fund_cease = 13
    x_budunit.get_item_obj(casa_way)._fund_onset = 13
    x_budunit.get_item_obj(casa_way)._fund_cease = 13
    x_budunit.get_item_obj(catt_way)._fund_onset = 13
    x_budunit.get_item_obj(catt_way)._fund_cease = 13
    x_budunit.get_item_obj(week_way)._fund_onset = 13
    x_budunit.get_item_obj(week_way)._fund_cease = 13

    assert x_budunit.itemroot._fund_onset == 13
    assert x_budunit.itemroot._fund_cease == 13
    assert x_budunit.get_item_obj(casa_way)._fund_onset == 13
    assert x_budunit.get_item_obj(casa_way)._fund_cease == 13
    assert x_budunit.get_item_obj(catt_way)._fund_onset == 13
    assert x_budunit.get_item_obj(catt_way)._fund_cease == 13
    assert x_budunit.get_item_obj(week_way)._fund_onset == 13
    assert x_budunit.get_item_obj(week_way)._fund_cease == 13

    # WHEN
    x_budunit.settle_bud()

    # THEN
    assert x_budunit.itemroot._fund_onset != 13
    assert x_budunit.itemroot._fund_cease != 13
    assert x_budunit.get_item_obj(casa_way)._fund_onset != 13
    assert x_budunit.get_item_obj(casa_way)._fund_cease != 13
    assert x_budunit.get_item_obj(catt_way)._fund_onset != 13
    assert x_budunit.get_item_obj(catt_way)._fund_cease != 13
    assert x_budunit.get_item_obj(week_way)._fund_onset != 13
    assert x_budunit.get_item_obj(week_way)._fund_cease != 13


def test_BudUnit_settle_bud_Sets_itemunit_fund_onset_fund_cease_Scenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_way = yao_budunit.make_l1_way(auto_str)
    auto_item = itemunit_shop(auto_str, mass=10)
    yao_budunit.set_l1_item(auto_item)

    carn_str = "carn"
    carn_way = yao_budunit.make_l1_way(carn_str)
    carn_item = itemunit_shop(carn_str, mass=60)
    yao_budunit.set_l1_item(carn_item)
    lamb_str = "lambs"
    lamb_way = yao_budunit.make_way(carn_way, lamb_str)
    lamb_item = itemunit_shop(lamb_str, mass=1)
    yao_budunit.set_item(lamb_item, parent_way=carn_way)
    duck_str = "ducks"
    duck_way = yao_budunit.make_way(carn_way, duck_str)
    duck_item = itemunit_shop(duck_str, mass=2)
    yao_budunit.set_item(duck_item, parent_way=carn_way)

    coal_str = "coal"
    coal_way = yao_budunit.make_l1_way(coal_str)
    coal_item = itemunit_shop(coal_str, mass=30)
    yao_budunit.set_l1_item(coal_item)

    assert yao_budunit.itemroot._fund_onset is None
    assert yao_budunit.itemroot._fund_cease is None
    assert yao_budunit.get_item_obj(auto_way)._fund_onset is None
    assert yao_budunit.get_item_obj(auto_way)._fund_cease is None
    assert yao_budunit.get_item_obj(carn_way)._fund_onset is None
    assert yao_budunit.get_item_obj(carn_way)._fund_cease is None
    assert yao_budunit.get_item_obj(coal_way)._fund_onset is None
    assert yao_budunit.get_item_obj(coal_way)._fund_cease is None
    lamb_before = yao_budunit.get_item_obj(way=lamb_way)
    assert lamb_before._fund_onset is None
    assert lamb_before._fund_cease is None
    duck_before = yao_budunit.get_item_obj(way=duck_way)
    assert duck_before._fund_onset is None
    assert duck_before._fund_cease is None

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit.itemroot._fund_onset == 0.0
    assert yao_budunit.itemroot._fund_cease == default_fund_pool()
    assert yao_budunit.get_item_obj(auto_way)._fund_onset == 0.0
    assert yao_budunit.get_item_obj(auto_way)._fund_cease == default_fund_pool() * 0.1
    assert yao_budunit.get_item_obj(carn_way)._fund_onset == default_fund_pool() * 0.1
    assert yao_budunit.get_item_obj(carn_way)._fund_cease == default_fund_pool() * 0.7
    assert yao_budunit.get_item_obj(coal_way)._fund_onset == default_fund_pool() * 0.7
    assert yao_budunit.get_item_obj(coal_way)._fund_cease == default_fund_pool() * 1.0

    duck_after = yao_budunit.get_item_obj(way=duck_way)
    assert duck_after._fund_onset == default_fund_pool() * 0.1
    assert duck_after._fund_cease == default_fund_pool() * 0.5
    lamb_after = yao_budunit.get_item_obj(way=lamb_way)
    assert lamb_after._fund_onset == default_fund_pool() * 0.5
    assert lamb_after._fund_cease == default_fund_pool() * 0.7


def test_BudUnit_settle_bud_Sets_itemunit_fund_onset_fund_cease_Scenario2_DifferentOrderOfItems():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_way = yao_budunit.make_l1_way(auto_str)
    auto_item = itemunit_shop(auto_str, mass=10)
    yao_budunit.set_l1_item(auto_item)

    yarn_str = "yarn"
    yarn_way = yao_budunit.make_l1_way(yarn_str)
    yarn_item = itemunit_shop(yarn_str, mass=60)
    yao_budunit.set_l1_item(yarn_item)
    lamb_str = "lambs"
    lamb_way = yao_budunit.make_way(yarn_way, lamb_str)
    lamb_item = itemunit_shop(lamb_str, mass=1)
    yao_budunit.set_item(lamb_item, parent_way=yarn_way)
    duck_str = "ducks"
    duck_way = yao_budunit.make_way(yarn_way, duck_str)
    duck_item = itemunit_shop(duck_str, mass=2)
    yao_budunit.set_item(duck_item, parent_way=yarn_way)

    coal_str = "coal"
    coal_way = yao_budunit.make_l1_way(coal_str)
    coal_item = itemunit_shop(coal_str, mass=30)
    yao_budunit.set_l1_item(coal_item)

    assert yao_budunit.itemroot._fund_onset is None
    assert yao_budunit.itemroot._fund_cease is None
    assert yao_budunit.get_item_obj(auto_way)._fund_onset is None
    assert yao_budunit.get_item_obj(auto_way)._fund_cease is None
    assert yao_budunit.get_item_obj(yarn_way)._fund_onset is None
    assert yao_budunit.get_item_obj(yarn_way)._fund_cease is None
    assert yao_budunit.get_item_obj(coal_way)._fund_onset is None
    assert yao_budunit.get_item_obj(coal_way)._fund_cease is None
    lamb_before = yao_budunit.get_item_obj(way=lamb_way)
    assert lamb_before._fund_onset is None
    assert lamb_before._fund_cease is None
    duck_before = yao_budunit.get_item_obj(way=duck_way)
    assert duck_before._fund_onset is None
    assert duck_before._fund_cease is None

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit.itemroot._fund_onset == 0.0
    assert yao_budunit.itemroot._fund_cease == default_fund_pool()
    assert yao_budunit.get_item_obj(auto_way)._fund_onset == 0.0
    assert yao_budunit.get_item_obj(auto_way)._fund_cease == default_fund_pool() * 0.1
    assert yao_budunit.get_item_obj(coal_way)._fund_onset == default_fund_pool() * 0.1
    assert yao_budunit.get_item_obj(coal_way)._fund_cease == default_fund_pool() * 0.4
    assert yao_budunit.get_item_obj(yarn_way)._fund_onset == default_fund_pool() * 0.4
    assert yao_budunit.get_item_obj(yarn_way)._fund_cease == default_fund_pool() * 1.0

    duck_after = yao_budunit.get_item_obj(way=duck_way)
    assert duck_after._fund_onset == default_fund_pool() * 0.4
    assert duck_after._fund_cease == default_fund_pool() * 0.8
    lamb_after = yao_budunit.get_item_obj(way=lamb_way)
    assert lamb_after._fund_onset == default_fund_pool() * 0.8
    assert lamb_after._fund_cease == default_fund_pool() * 1.0


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeItemsOfZero_massScenario0():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_bud.make_way(casa_way, floor_str)
    floor_item = itemunit_shop(floor_str, pledge=True)
    sue_bud.set_item(floor_item, casa_way)
    sue_bud.set_l1_item(itemunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_way = sue_bud.make_way(casa_way, status_str)
    sue_bud.set_item(itemunit_shop(status_str, mass=0), casa_way)

    non_str = "not clean"
    yes_str = "yes clean"
    non_way = sue_bud.make_way(status_way, non_str)
    yes_way = sue_bud.make_way(status_way, yes_str)
    sue_bud.set_item(itemunit_shop(non_str), status_way)
    sue_bud.set_item(itemunit_shop(yes_str, mass=2), status_way)

    assert sue_bud.get_item_obj(casa_way)._fund_ratio is None
    assert sue_bud.get_item_obj(floor_way)._fund_ratio is None
    assert sue_bud.get_item_obj(status_way)._fund_ratio is None
    assert sue_bud.get_item_obj(non_way)._fund_ratio is None
    assert sue_bud.get_item_obj(yes_way)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud.fund_pool=}")
    assert sue_bud.get_item_obj(casa_way)._fund_ratio == 0.5
    assert sue_bud.get_item_obj(floor_way)._fund_ratio == 0.5
    assert sue_bud.get_item_obj(status_way)._fund_ratio == 0.0
    assert sue_bud.get_item_obj(non_way)._fund_ratio == 0.0
    assert sue_bud.get_item_obj(yes_way)._fund_ratio == 0.0


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeItemsOfZero_massScenario1():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_bud.make_way(casa_way, floor_str)
    floor_item = itemunit_shop(floor_str, pledge=True)
    sue_bud.set_item(floor_item, casa_way)
    sue_bud.set_l1_item(itemunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_way = sue_bud.make_way(casa_way, status_str)
    sue_bud.set_item(itemunit_shop(status_str), casa_way)

    status_item = sue_bud.get_item_obj(status_way)
    print(f"{status_item.mass=}")
    print("This should raise error: 'Itemunit._'")

    clean_str = "clean"
    clean_way = sue_bud.make_way(status_way, clean_str)
    very_str = "very_much"
    mod_str = "moderately"
    dirty_str = "dirty"

    sue_bud.set_item(itemunit_shop(clean_str, mass=0), status_way)
    sue_bud.set_item(itemunit_shop(very_str), clean_way)
    sue_bud.set_item(itemunit_shop(mod_str, mass=2), clean_way)
    sue_bud.set_item(itemunit_shop(dirty_str), clean_way)

    very_way = sue_bud.make_way(clean_way, very_str)
    mod_way = sue_bud.make_way(clean_way, mod_str)
    dirty_way = sue_bud.make_way(clean_way, dirty_str)
    assert sue_bud.get_item_obj(casa_way)._fund_ratio is None
    assert sue_bud.get_item_obj(floor_way)._fund_ratio is None
    assert sue_bud.get_item_obj(status_way)._fund_ratio is None
    assert sue_bud.get_item_obj(clean_way)._fund_ratio is None
    assert sue_bud.get_item_obj(very_way)._fund_ratio is None
    assert sue_bud.get_item_obj(mod_way)._fund_ratio is None
    assert sue_bud.get_item_obj(dirty_way)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud.fund_pool=}")
    assert sue_bud.get_item_obj(casa_way)._fund_ratio == 0.5
    assert sue_bud.get_item_obj(floor_way)._fund_ratio == 0.25
    assert sue_bud.get_item_obj(status_way)._fund_ratio == 0.25
    assert sue_bud.get_item_obj(clean_way)._fund_ratio == 0
    assert sue_bud.get_item_obj(very_way)._fund_ratio == 0
    assert sue_bud.get_item_obj(mod_way)._fund_ratio == 0
    assert sue_bud.get_item_obj(dirty_way)._fund_ratio == 0


def test_BudUnit_settle_bud_WhenItemUnitHasFundsBut_kidsHaveNoMassDistributeFundsToAcctUnits_scenario0():
    sue_budunit = budunit_shop("Sue")
    yao_str = "Yao"
    sue_budunit.add_acctunit(yao_str)
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_item = itemunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_way = sue_budunit.make_way(casa_way, swim_str)
    swim_item = itemunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_way = sue_budunit.make_way(casa_way, clean_str)
    clean_item = itemunit_shop(clean_str, mass=2)
    sue_budunit.set_item(itemunit_shop(clean_str), casa_way)

    sweep_str = "sweep"
    sweep_way = sue_budunit.make_way(clean_way, sweep_str)
    sweep_item = itemunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_way = sue_budunit.make_way(clean_way, vaccum_str)
    vaccum_item = itemunit_shop(vaccum_str, mass=0)

    sue_budunit.set_l1_item(casa_item)
    sue_budunit.set_item(swim_item, casa_way)
    sue_budunit.set_item(clean_item, casa_way)
    sue_budunit.set_item(sweep_item, clean_way)  # _mass=0
    sue_budunit.set_item(vaccum_item, clean_way)  # _mass=0

    assert sue_budunit.get_item_obj(casa_way)._fund_ratio is None
    assert sue_budunit.get_item_obj(swim_way)._fund_ratio is None
    assert sue_budunit.get_item_obj(clean_way)._fund_ratio is None
    assert sue_budunit.get_item_obj(sweep_way)._fund_ratio is None
    assert sue_budunit.get_item_obj(vaccum_way)._fund_ratio is None
    assert sue_budunit.get_groupunit(yao_str) is None

    assert not sue_budunit._offtrack_fund
    assert sue_budunit.get_acct(yao_str)._fund_give == 0
    assert sue_budunit.get_acct(yao_str)._fund_take == 0

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    print(f"{sue_budunit.fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_budunit.get_item_obj(casa_way)._fund_ratio == 1
    assert sue_budunit.get_item_obj(swim_way)._fund_ratio == 0.8
    assert sue_budunit.get_item_obj(clean_way)._fund_ratio == clean_fund_ratio
    assert sue_budunit.get_item_obj(sweep_way)._fund_ratio == 0
    assert sue_budunit.get_item_obj(vaccum_way)._fund_ratio == 0
    assert sue_budunit.get_groupunit(yao_str)._fund_give == 0
    assert sue_budunit.get_groupunit(yao_str)._fund_take == 0

    assert sue_budunit._offtrack_fund == clean_fund_ratio * default_fund_pool()
    assert sue_budunit.get_acct(yao_str)._fund_give == default_fund_pool()
    assert sue_budunit.get_acct(yao_str)._fund_take == default_fund_pool()


def test_BudUnit_settle_bud_TreeTraverseSetsAwardLine_fundFromRootCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # item tree has no awardlinks
    assert sue_bud.itemroot._awardlines == {}
    sue_str = "Sue"
    week_str = "weekdays"
    nation_str = "nation-state"
    sue_awardlink = awardlink_shop(awardee_title=sue_str)
    sue_bud.add_acctunit(acct_name=sue_str)
    sue_bud.itemroot.set_awardlink(awardlink=sue_awardlink)
    # item tree has awardlines
    assert sue_bud.itemroot._awardheirs.get(sue_str) is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud.itemroot._awardheirs.get(sue_str) is not None
    assert sue_bud.itemroot._awardheirs.get(sue_str).awardee_title == sue_str
    assert sue_bud.itemroot._awardlines != {}
    root_way = to_way(sue_bud.itemroot.item_tag)
    root_item = sue_bud.get_item_obj(way=root_way)
    sue_awardline = sue_bud.itemroot._awardlines.get(sue_str)
    print(f"{sue_awardline._fund_give=} {root_item._fund_ratio=} ")
    print(f"  {sue_awardline._fund_take=} {root_item._fund_ratio=} ")
    sum_x = 0
    cat_way = sue_bud.make_l1_way("cat have dinner")
    cat_item = sue_bud.get_item_obj(cat_way)
    week_way = sue_bud.make_l1_way(week_str)
    week_item = sue_bud.get_item_obj(week_way)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    casa_item = sue_bud.get_item_obj(casa_way)
    nation_way = sue_bud.make_l1_way(nation_str)
    nation_item = sue_bud.get_item_obj(nation_way)
    sum_x = cat_item._fund_ratio
    print(f"{cat_item._fund_ratio=} {sum_x} ")
    sum_x += week_item._fund_ratio
    print(f"{week_item._fund_ratio=} {sum_x} ")
    sum_x += casa_item._fund_ratio
    print(f"{casa_item._fund_ratio=} {sum_x} ")
    sum_x += nation_item._fund_ratio
    print(f"{nation_item._fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_item in root_item._kids.values():
    #     sum_x += kid_item._fund_ratio
    #     print(f"  {kid_item._fund_ratio=} {sum_x=} {kid_item.get_item_way()=}")
    assert round(sue_awardline._fund_give, 15) == default_fund_pool()
    assert round(sue_awardline._fund_take, 15) == default_fund_pool()
    x_awardline = awardline_shop(sue_str, default_fund_pool(), default_fund_pool())
    assert sue_bud.itemroot._awardlines == {x_awardline.awardee_title: x_awardline}


def test_BudUnit_settle_bud_TreeTraverseSets_awardlines_ToRootItemUnitFromNonRootItemUnit():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    sue_str = "Sue"
    sue_bud.add_acctunit(sue_str)
    casa_way = sue_bud.make_l1_way("casa")
    sue_bud.get_item_obj(casa_way).set_awardlink(awardlink_shop(awardee_title=sue_str))
    assert sue_bud.itemroot._awardlines == {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud.itemroot._awardlines != {}
    print(f"{sue_bud.itemroot._awardlines=}")
    x_awardline = awardline_shop(
        awardee_title=sue_str,
        _fund_give=0.230769231 * default_fund_pool(),
        _fund_take=0.230769231 * default_fund_pool(),
    )
    assert sue_bud.itemroot._awardlines == {x_awardline.awardee_title: x_awardline}
    casa_itemunit = sue_bud.get_item_obj(casa_way)
    assert casa_itemunit._awardlines != {}
    assert casa_itemunit._awardlines == {x_awardline.awardee_title: x_awardline}


def test_BudUnit_settle_bud_WithRootLevelAwardLinkSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    sue_bud.set_acctunit(acctunit_shop(yao_str))
    sue_bud.set_acctunit(acctunit_shop(zia_str))
    sue_bud.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    root_way = to_way(sue_bud.itemroot.item_tag)
    x_itemroot = sue_bud.get_item_obj(root_way)
    x_itemroot.set_awardlink(awardlink=yao_awardlink)
    x_itemroot.set_awardlink(awardlink=zia_awardlink)
    x_itemroot.set_awardlink(awardlink=xio_awardlink)
    assert len(sue_bud.get_acctunit_group_labels_dict()) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    yao_groupunit = sue_bud.get_groupunit(yao_str)
    zia_groupunit = sue_bud.get_groupunit(zia_str)
    xio_groupunit = sue_bud.get_groupunit(xio_str)
    assert yao_groupunit._fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit._fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit._fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit._fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit._fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit._fund_take == 0.125 * default_fund_pool()
    cred_sum1 = yao_groupunit._fund_give
    cred_sum1 += zia_groupunit._fund_give + xio_groupunit._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupunit._fund_take
    debt_sum1 += zia_groupunit._fund_take + xio_groupunit._fund_take
    assert debt_sum1 == 1 * default_fund_pool()

    # ESTABLISH
    sue_bud.set_acctunit(acctunit_shop(sue_str))
    sue_awardlink = awardlink_shop(sue_str, give_force=37)
    x_itemroot.set_awardlink(sue_awardlink)
    assert len(x_itemroot.awardlinks) == 4
    assert len(sue_bud.get_acctunit_group_labels_dict()) == 4

    # WHEN
    sue_bud.settle_bud()

    # THEN
    yao_groupunit = sue_bud.get_groupunit(yao_str)
    zia_groupunit = sue_bud.get_groupunit(zia_str)
    xio_groupunit = sue_bud.get_groupunit(xio_str)
    sue_groupunit = sue_bud.get_groupunit(sue_str)
    assert yao_groupunit._fund_give != 0.5 * default_fund_pool()
    assert yao_groupunit._fund_take != 0.75 * default_fund_pool()
    assert zia_groupunit._fund_give != 0.25 * default_fund_pool()
    assert zia_groupunit._fund_take != 0.125 * default_fund_pool()
    assert xio_groupunit._fund_give != 0.25 * default_fund_pool()
    assert xio_groupunit._fund_take != 0.125 * default_fund_pool()
    assert sue_groupunit._fund_give is not None
    assert sue_groupunit._fund_take is not None
    cred_sum1 = yao_groupunit._fund_give + zia_groupunit._fund_give
    cred_sum1 += xio_groupunit._fund_give + sue_groupunit._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupunit._fund_take + zia_groupunit._fund_take
    debt_sum1 += xio_groupunit._fund_take + sue_groupunit._fund_take
    assert round(debt_sum1) == 1 * default_fund_pool()


def test_BudUnit_settle_bud_WithLevel3AwardLinkSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    x_bud = budunit_shop(bob_str)
    swim_str = "swim"
    swim_way = x_bud.make_l1_way(swim_str)
    x_bud.set_l1_item(itemunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_str))
    x_bud.set_acctunit(acctunit_shop(zia_str))
    x_bud.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_item = x_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(yao_awardlink)
    swim_item.set_awardlink(zia_awardlink)
    swim_item.set_awardlink(xio_awardlink)
    assert len(x_bud.get_acctunit_group_labels_dict()) == 3

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_groupunit = x_bud.get_groupunit(yao_str)
    zia_groupunit = x_bud.get_groupunit(zia_str)
    xio_groupunit = x_bud.get_groupunit(xio_str)
    assert yao_groupunit._fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit._fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit._fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit._fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit._fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit._fund_take == 0.125 * default_fund_pool()
    groupunit_fund_give_sum = (
        yao_groupunit._fund_give + zia_groupunit._fund_give + xio_groupunit._fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit._fund_take + zia_groupunit._fund_take + xio_groupunit._fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_fund_pool()
    assert groupunit_fund_take_sum == 1 * default_fund_pool()


def test_BudUnit_settle_bud_CreatesNewGroupUnitAndSets_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_way = x_bud.make_l1_way(swim_str)
    x_bud.set_l1_item(itemunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_str))
    x_bud.set_acctunit(acctunit_shop(zia_str))
    # x_bud.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_item = x_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(yao_awardlink)
    swim_item.set_awardlink(zia_awardlink)
    swim_item.set_awardlink(xio_awardlink)
    assert len(x_bud.get_acctunit_group_labels_dict()) == 2

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_groupunit = x_bud.get_groupunit(yao_str)
    zia_groupunit = x_bud.get_groupunit(zia_str)
    xio_groupunit = x_bud.get_groupunit(xio_str)
    assert len(x_bud.get_acctunit_group_labels_dict()) != len(x_bud._groupunits)
    assert yao_groupunit._fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit._fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit._fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit._fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit._fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit._fund_take == 0.125 * default_fund_pool()
    groupunit_fund_give_sum = (
        yao_groupunit._fund_give + zia_groupunit._fund_give + xio_groupunit._fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit._fund_take + zia_groupunit._fund_take + xio_groupunit._fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_fund_pool()
    assert groupunit_fund_take_sum == 1 * default_fund_pool()


def test_BudUnit_settle_bud_WithLevel3AwardLinkAndEmptyAncestorsSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_way = x_bud.make_l1_way(swim_str)
    x_bud.set_l1_item(itemunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_str))
    x_bud.set_acctunit(acctunit_shop(zia_str))
    x_bud.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_item = x_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(yao_awardlink)
    swim_item.set_awardlink(zia_awardlink)
    swim_item.set_awardlink(xio_awardlink)

    # no awardlinks attached to this one
    x_bud.set_l1_item(itemunit_shop("hunt", mass=3))

    # WHEN
    x_bud.settle_bud()

    # THEN
    x_itemroot = x_bud.get_item_obj(to_way(x_bud.fisc_tag))
    with pytest_raises(Exception) as excinfo:
        x_itemroot.awardlinks[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_itemroot.awardlinks[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_itemroot.awardlinks[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"
    with pytest_raises(Exception) as excinfo:
        x_itemroot._kids["hunt"]._awardheirs[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_itemroot._kids["hunt"]._awardheirs[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_itemroot._kids["hunt"]._awardheirs[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"

    # THEN
    yao_groupunit = x_bud.get_groupunit(yao_str)
    zia_groupunit = x_bud.get_groupunit(zia_str)
    xio_groupunit = x_bud.get_groupunit(xio_str)
    assert yao_groupunit._fund_give == 0.125 * default_fund_pool()
    assert yao_groupunit._fund_take == 0.1875 * default_fund_pool()
    assert zia_groupunit._fund_give == 0.0625 * default_fund_pool()
    assert zia_groupunit._fund_take == 0.03125 * default_fund_pool()
    assert xio_groupunit._fund_give == 0.0625 * default_fund_pool()
    assert xio_groupunit._fund_take == 0.03125 * default_fund_pool()
    assert (
        yao_groupunit._fund_give + zia_groupunit._fund_give + xio_groupunit._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        yao_groupunit._fund_take + zia_groupunit._fund_take + xio_groupunit._fund_take
        == 0.25 * default_fund_pool()
    )


def test_BudUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkBudFund():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_bud.set_acctunit(acctunit_shop(yao_str))
    sue_bud.set_acctunit(acctunit_shop(zia_str))
    sue_bud.set_acctunit(acctunit_shop(Xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    Xio_awardlink = awardlink_shop(Xio_str, give_force=10)
    sue_bud.itemroot.set_awardlink(yao_awardlink)
    sue_bud.itemroot.set_awardlink(zia_awardlink)
    sue_bud.itemroot.set_awardlink(Xio_awardlink)
    assert len(sue_bud.itemroot.awardlinks) == 3

    # WHEN
    item_dict = sue_bud.get_item_dict()

    # THEN
    print(f"{item_dict.keys()=}")
    item_bob = item_dict.get(to_way(sue_bud.fisc_tag))
    assert len(item_bob._awardheirs) == 3

    bheir_yao = item_bob._awardheirs.get(yao_str)
    bheir_zia = item_bob._awardheirs.get(zia_str)
    bheir_Xio = item_bob._awardheirs.get(Xio_str)
    assert bheir_yao._fund_give == 0.5 * default_fund_pool()
    assert bheir_yao._fund_take == 0.75 * default_fund_pool()
    assert bheir_zia._fund_give == 0.25 * default_fund_pool()
    assert bheir_zia._fund_take == 0.125 * default_fund_pool()
    assert bheir_Xio._fund_give == 0.25 * default_fund_pool()
    assert bheir_Xio._fund_take == 0.125 * default_fund_pool()
    assert (
        bheir_yao._fund_give + bheir_zia._fund_give + bheir_Xio._fund_give
        == 1 * default_fund_pool()
    )
    assert (
        bheir_yao._fund_take + bheir_zia._fund_take + bheir_Xio._fund_take
        == 1 * default_fund_pool()
    )

    # fund_give_sum = 0
    # fund_take_sum = 0
    # for group in x_bud.itemroot._awardheirs.values():
    #     print(f"{group=}")
    #     assert group._fund_give is not None
    #     assert group._fund_give in [0.25, 0.5]
    #     assert group._fund_take is not None
    #     assert group._fund_take in [0.75, 0.125]
    #     fund_give_sum += group._fund_give
    #     fund_take_sum += group._fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_BudUnit_settle_bud_CorrectlySetsGroupLinkBudCredAndDebt():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_str))
    yao_bud.set_acctunit(acctunit_shop(bob_str))
    yao_bud.set_acctunit(acctunit_shop(zia_str))
    sue_awardlink = awardlink_shop(sue_str, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_str, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_str, 10, take_force=5)
    root_way = to_way(yao_bud.fisc_tag)
    yao_bud.edit_item_attr(root_way, awardlink=sue_awardlink)
    yao_bud.edit_item_attr(root_way, awardlink=bob_awardlink)
    yao_bud.edit_item_attr(root_way, awardlink=zia_awardlink)

    sue_acctunit = yao_bud.get_acct(sue_str)
    bob_acctunit = yao_bud.get_acct(bob_str)
    zia_acctunit = yao_bud.get_acct(zia_str)
    sue_sue_membership = sue_acctunit.get_membership(sue_str)
    bob_bob_membership = bob_acctunit.get_membership(bob_str)
    zia_zia_membership = zia_acctunit.get_membership(zia_str)
    assert sue_sue_membership._fund_give is None
    assert sue_sue_membership._fund_take is None
    assert bob_bob_membership._fund_give is None
    assert bob_bob_membership._fund_take is None
    assert zia_zia_membership._fund_give is None
    assert zia_zia_membership._fund_take is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert sue_sue_membership._fund_give == 0.5 * default_fund_pool()
    assert sue_sue_membership._fund_take == 0.8 * default_fund_pool()
    assert bob_bob_membership._fund_give == 0.25 * default_fund_pool()
    assert bob_bob_membership._fund_take == 0.1 * default_fund_pool()
    assert zia_zia_membership._fund_give == 0.25 * default_fund_pool()
    assert zia_zia_membership._fund_take == 0.1 * default_fund_pool()

    membership_cred_sum = (
        sue_sue_membership._fund_give
        + bob_bob_membership._fund_give
        + zia_zia_membership._fund_give
    )
    assert membership_cred_sum == 1.0 * default_fund_pool()
    membership_debt_sum = (
        sue_sue_membership._fund_take
        + bob_bob_membership._fund_take
        + zia_zia_membership._fund_take
    )
    assert membership_debt_sum == 1.0 * default_fund_pool()

    # ESTABLISH another pledge, check metrics are as expected
    xio_str = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_str))
    yao_bud.itemroot.set_awardlink(awardlink_shop(xio_str, 20, take_force=13))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    xio_groupunit = yao_bud.get_groupunit(xio_str)
    xio_xio_membership = xio_groupunit.get_membership(xio_str)
    sue_acctunit = yao_bud.get_acct(sue_str)
    bob_acctunit = yao_bud.get_acct(bob_str)
    zia_acctunit = yao_bud.get_acct(zia_str)
    sue_sue_membership = sue_acctunit.get_membership(sue_str)
    bob_bob_membership = bob_acctunit.get_membership(bob_str)
    zia_zia_membership = zia_acctunit.get_membership(zia_str)
    assert sue_sue_membership._fund_give != 0.25 * default_fund_pool()
    assert sue_sue_membership._fund_take != 0.8 * default_fund_pool()
    assert bob_bob_membership._fund_give != 0.25 * default_fund_pool()
    assert bob_bob_membership._fund_take != 0.1 * default_fund_pool()
    assert zia_zia_membership._fund_give != 0.5 * default_fund_pool()
    assert zia_zia_membership._fund_take != 0.1 * default_fund_pool()
    assert xio_xio_membership._fund_give is not None
    assert xio_xio_membership._fund_take is not None

    x_fund_give_sum = (
        sue_sue_membership._fund_give
        + bob_bob_membership._fund_give
        + zia_zia_membership._fund_give
        + xio_xio_membership._fund_give
    )
    print(f"{x_fund_give_sum=}")
    assert x_fund_give_sum == 1.0 * default_fund_pool()
    x_fund_take_sum = (
        sue_sue_membership._fund_take
        + bob_bob_membership._fund_take
        + zia_zia_membership._fund_take
        + xio_xio_membership._fund_take
    )
    assert x_fund_take_sum == 1.0 * default_fund_pool()


def test_BudUnit_settle_bud_CorrectlySetsAcctUnitBud_fund():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)
    yao_bud.set_l1_item(itemunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_str))
    yao_bud.set_acctunit(acctunit_shop(bob_str))
    yao_bud.set_acctunit(acctunit_shop(zia_str))
    bl_sue = awardlink_shop(sue_str, 20, take_force=40)
    bl_bob = awardlink_shop(bob_str, 10, take_force=5)
    bl_zia = awardlink_shop(zia_str, 10, take_force=5)
    yao_bud.get_item_obj(swim_way).set_awardlink(bl_sue)
    yao_bud.get_item_obj(swim_way).set_awardlink(bl_bob)
    yao_bud.get_item_obj(swim_way).set_awardlink(bl_zia)

    sue_acctunit = yao_bud.get_acct(sue_str)
    bob_acctunit = yao_bud.get_acct(bob_str)
    zia_acctunit = yao_bud.get_acct(zia_str)

    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert sue_acctunit._fund_give == 0.5 * default_fund_pool()
    assert sue_acctunit._fund_take == 0.8 * default_fund_pool()
    assert bob_acctunit._fund_give == 0.25 * default_fund_pool()
    assert bob_acctunit._fund_take == 0.1 * default_fund_pool()
    assert zia_acctunit._fund_give == 0.25 * default_fund_pool()
    assert zia_acctunit._fund_take == 0.1 * default_fund_pool()

    assert (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )

    # WHEN another pledge, check metrics are as expected
    xio_str = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_str))
    yao_bud.itemroot.set_awardlink(awardlink_shop(xio_str, 20, take_force=10))
    yao_bud.settle_bud()

    # THEN
    xio_acctunit = yao_bud.get_acct(xio_str)

    assert sue_acctunit._fund_give != 0.5 * default_fund_pool()
    assert sue_acctunit._fund_take != 0.8 * default_fund_pool()
    assert bob_acctunit._fund_give != 0.25 * default_fund_pool()
    assert bob_acctunit._fund_take != 0.1 * default_fund_pool()
    assert zia_acctunit._fund_give != 0.25 * default_fund_pool()
    assert zia_acctunit._fund_take != 0.1 * default_fund_pool()
    assert xio_acctunit._fund_give is not None
    assert xio_acctunit._fund_take is not None

    sum_acctunit_fund_give = (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
    )
    assert sum_acctunit_fund_give < 1.0 * default_fund_pool()
    assert (
        sue_acctunit._fund_give
        + bob_acctunit._fund_give
        + zia_acctunit._fund_give
        + xio_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        < 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take
        + bob_acctunit._fund_take
        + zia_acctunit._fund_take
        + xio_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )


def test_BudUnit_settle_bud_CorrectlySetsPartGroupedLWAcctUnitBud_fund():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)
    yao_bud.set_l1_item(itemunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_str))
    yao_bud.set_acctunit(acctunit_shop(bob_str))
    yao_bud.set_acctunit(acctunit_shop(zia_str))
    sue_awardlink = awardlink_shop(sue_str, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_str, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_str, 10, take_force=5)
    swim_item = yao_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(sue_awardlink)
    swim_item.set_awardlink(bob_awardlink)
    swim_item.set_awardlink(zia_awardlink)

    # no awardlinks attached to this one
    hunt_str = "hunt"
    yao_bud.set_l1_item(itemunit_shop(hunt_str, mass=3))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    sue_groupunit = yao_bud.get_groupunit(sue_str)
    bob_groupunit = yao_bud.get_groupunit(bob_str)
    zia_groupunit = yao_bud.get_groupunit(zia_str)
    assert sue_groupunit._fund_give != 0.5 * default_fund_pool()
    assert sue_groupunit._fund_take != 0.8 * default_fund_pool()
    assert bob_groupunit._fund_give != 0.25 * default_fund_pool()
    assert bob_groupunit._fund_take != 0.1 * default_fund_pool()
    assert zia_groupunit._fund_give != 0.25 * default_fund_pool()
    assert zia_groupunit._fund_take != 0.1 * default_fund_pool()
    assert (
        sue_groupunit._fund_give + bob_groupunit._fund_give + zia_groupunit._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        sue_groupunit._fund_take + bob_groupunit._fund_take + zia_groupunit._fund_take
        == 0.25 * default_fund_pool()
    )

    sue_acctunit = yao_bud.get_acct(sue_str)
    bob_acctunit = yao_bud.get_acct(bob_str)
    zia_acctunit = yao_bud.get_acct(zia_str)

    assert sue_acctunit._fund_give == 0.375 * default_fund_pool()
    assert sue_acctunit._fund_take == 0.45 * default_fund_pool()
    assert bob_acctunit._fund_give == 0.3125 * default_fund_pool()
    assert bob_acctunit._fund_take == 0.275 * default_fund_pool()
    assert zia_acctunit._fund_give == 0.3125 * default_fund_pool()
    assert zia_acctunit._fund_take == 0.275 * default_fund_pool()

    assert (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
        == 1.0 * default_fund_pool()
    )


def test_BudUnit_settle_bud_CreatesNewGroupUnitAndSets_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    bob_bud = budunit_shop(bob_str)
    swim_str = "swim"
    swim_way = bob_bud.make_l1_way(swim_str)
    bob_bud.set_l1_item(itemunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    bob_bud.set_acctunit(acctunit_shop(yao_str))
    bob_bud.set_acctunit(acctunit_shop(zia_str))
    # bob_bud.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_item = bob_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(yao_awardlink)
    swim_item.set_awardlink(zia_awardlink)
    swim_item.set_awardlink(xio_awardlink)
    assert len(bob_bud.get_acctunit_group_labels_dict()) == 2

    # WHEN
    bob_bud.settle_bud()

    # THEN
    xio_groupunit = bob_bud.get_groupunit(xio_str)
    assert len(bob_bud.get_acctunit_group_labels_dict()) != len(bob_bud._groupunits)
    assert not bob_bud.acct_exists(xio_str)
    yao_acctunit = bob_bud.get_acct(yao_str)
    zia_acctunit = bob_bud.get_acct(zia_str)
    acctunit_fund_give_sum = yao_acctunit._fund_give + zia_acctunit._fund_give
    acctunit_fund_take_sum = yao_acctunit._fund_take + zia_acctunit._fund_take
    assert acctunit_fund_give_sum == default_fund_pool()
    assert acctunit_fund_take_sum == default_fund_pool()


def test_BudUnit_settle_bud_CorrectlySetsAcctUnit_fund_give_fund_take():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    yao_bud.set_l1_item(itemunit_shop("swim"))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_str, 8))
    yao_bud.set_acctunit(acctunit_shop(bob_str))
    yao_bud.set_acctunit(acctunit_shop(zia_str))
    sue_acctunit = yao_bud.get_acct(sue_str)
    bob_acctunit = yao_bud.get_acct(bob_str)
    zia_acctunit = yao_bud.get_acct(zia_str)
    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    fund_give_sum = (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
    )
    assert fund_give_sum == 1.0 * default_fund_pool()
    fund_take_sum = (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
    )
    assert fund_take_sum == 1.0 * default_fund_pool()


def clear_all_acctunits_groupunits_fund_agenda_give_take(x_bud: BudUnit):
    # DELETE bud_agenda_debt and bud_agenda_cred
    for groupunit_x in x_bud._groupunits.values():
        groupunit_x.clear_fund_give_take()
        # for membership_x in groupunit_x._accts.values():
        #     print(f"{groupunit_x.} {membership_x.}  {membership_x._fund_give:.6f} {membership_x.debtit_belief=} {membership__fund_take:t:.6f} {membership_x.} ")

    # DELETE bud_agenda_debt and bud_agenda_cred
    for x_acctunit in x_bud.accts.values():
        x_acctunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupunit_give: float = 0
    sum_groupunit_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_sums(self, x_bud: BudUnit):
        for x_groupunit in x_bud._groupunits.values():
            self.sum_groupunit_give += x_groupunit._fund_agenda_give
            self.sum_groupunit_take += x_groupunit._fund_agenda_take
            for membership_x in x_groupunit._memberships.values():
                self.sum_membership_cred += membership_x._fund_agenda_give
                self.sum_membership_debt += membership_x._fund_agenda_take
                self.membership_count += 1


@dataclass
class AcctAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_bud: BudUnit):
        for acctunit in x_bud.accts.values():
            self.sum_agenda_cred += acctunit._fund_agenda_give
            self.sum_agenda_debt += acctunit._fund_agenda_take
            self.sum_agenda_ratio_cred += acctunit._fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += acctunit._fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_bud_agenda_share = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_bud_i_sum = 0
    agenda_yes_bud_i_sum = 0

    def set_sums(self, agenda_dict: dict[WayUnit, ItemUnit]):
        for agenda_item in agenda_dict.values():
            self.sum_bud_agenda_share += agenda_item.get_fund_share()
            if agenda_item._awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_bud_i_sum += agenda_item.get_fund_share()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_bud_i_sum += agenda_item.get_fund_share()


def test_BudUnit_agenda_cred_debt_IsCorrectlySet():
    # ESTABLISH
    yao_bud = budunit_v001_with_large_agenda()
    clear_all_acctunits_groupunits_fund_agenda_give_take(yao_bud)

    # TEST bud_agenda_debt and bud_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_bud)
    assert x_groupagendametrics.sum_groupunit_give == 0
    assert x_groupagendametrics.sum_groupunit_take == 0
    assert x_groupagendametrics.sum_membership_cred == 0
    assert x_groupagendametrics.sum_membership_debt == 0

    # TEST bud_agenda_debt and bud_agenda_cred are empty
    x_acctagendametrics = AcctAgendaMetrics()
    x_acctagendametrics.set_sums(yao_bud)
    assert x_acctagendametrics.sum_agenda_cred == 0
    assert x_acctagendametrics.sum_agenda_debt == 0
    assert x_acctagendametrics.sum_agenda_ratio_cred == 0
    assert x_acctagendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = yao_bud.get_agenda_dict()
    # for item_way in yao_bud._item_dict.keys():
    #     print(f"{item_way=}")
    # for x_acct in yao_bud.accts.values():
    #     for x_membership in x_acct._memberships.values():
    #         print(f"{x_membership.group_label=}")

    # THEN
    assert len(agenda_dict) == 63
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_bud_agenda_share=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    predicted_agenda_no_bud_i_sum = int(0.004107582 * default_fund_pool())
    assert x_awardagendametrics.agenda_no_bud_i_sum == predicted_agenda_no_bud_i_sum
    predicted_agenda_yes_bud_i_sum = int(0.003065400 * default_fund_pool())
    assert x_awardagendametrics.agenda_yes_bud_i_sum == predicted_agenda_yes_bud_i_sum
    assert are_equal(
        x_awardagendametrics.agenda_no_bud_i_sum
        + x_awardagendametrics.agenda_yes_bud_i_sum,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    predicted_sum_bud_agenda_share = 0.007172982 * default_fund_pool()
    assert x_awardagendametrics.sum_bud_agenda_share == predicted_sum_bud_agenda_share

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_bud)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 3065400
    print(f"{x_groupagendametrics.sum_groupunit_give=}")
    assert are_equal(x_groupagendametrics.sum_groupunit_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupunit_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_bud_i_sum,
        x_groupagendametrics.sum_groupunit_give,
    )

    assert all_acctunits_have_legitimate_values(yao_bud)

    x_acctagendametrics = AcctAgendaMetrics()
    x_acctagendametrics.set_sums(yao_bud)
    assert are_equal(
        x_acctagendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert are_equal(
        x_acctagendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert are_equal(x_acctagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_acctagendametrics.sum_agenda_ratio_debt, 1)

    # acctunit_fund_give_sum = 0.0
    # acctunit_fund_take_sum = 0.0

    # assert acctunit_fund_give_sum == 1.0
    # assert acctunit_fund_take_sum > 0.9999999
    # assert acctunit_fund_take_sum < 1.00000001


def all_acctunits_have_legitimate_values(x_bud: BudUnit):
    return not any(
        (
            acctunit._fund_give is None
            or acctunit._fund_give in [0.25, 0.5]
            or acctunit._fund_take is None
            or acctunit._fund_take in [0.8, 0.1]
        )
        for acctunit in x_bud.accts.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_BudUnit_settle_bud_SetsAttrsWhenNoFactUnitsNoReasonUnitsEmpty_agenda_ratio_cred_debt():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    sue_acctunit = acctunit_shop(sue_str, 0.5, debtit_belief=2)
    bob_acctunit = acctunit_shop(bob_str, 1.5, debtit_belief=3)
    zia_acctunit = acctunit_shop(zia_str, 8, debtit_belief=5)
    yao_bud.set_acctunit(sue_acctunit)
    yao_bud.set_acctunit(bob_acctunit)
    yao_bud.set_acctunit(zia_acctunit)
    sue_acct = yao_bud.get_acct(sue_str)
    bob_acct = yao_bud.get_acct(bob_str)
    zia_acct = yao_bud.get_acct(zia_str)

    assert not sue_acct._fund_give
    assert not sue_acct._fund_take
    assert not bob_acct._fund_give
    assert not bob_acct._fund_take
    assert not zia_acct._fund_give
    assert not zia_acct._fund_take
    assert not sue_acct._fund_agenda_give
    assert not sue_acct._fund_agenda_take
    assert not bob_acct._fund_agenda_give
    assert not bob_acct._fund_agenda_take
    assert not zia_acct._fund_agenda_give
    assert not zia_acct._fund_agenda_take
    assert not sue_acct._fund_agenda_ratio_give
    assert not sue_acct._fund_agenda_ratio_take
    assert not bob_acct._fund_agenda_ratio_give
    assert not bob_acct._fund_agenda_ratio_take
    assert not zia_acct._fund_agenda_ratio_give
    assert not zia_acct._fund_agenda_ratio_take

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud._reason_bases == set()
    assert sue_acct._fund_give == 50000000
    assert sue_acct._fund_take == 200000000
    assert bob_acct._fund_give == 150000000
    assert bob_acct._fund_take == 300000000
    assert zia_acct._fund_give == 800000000
    assert zia_acct._fund_take == 500000000
    assert sue_acct._fund_agenda_give == 50000000
    assert sue_acct._fund_agenda_take == 200000000
    assert bob_acct._fund_agenda_give == 150000000
    assert bob_acct._fund_agenda_take == 300000000
    assert zia_acct._fund_agenda_give == 800000000
    assert zia_acct._fund_agenda_take == 500000000
    assert sue_acct._fund_agenda_give == sue_acct._fund_give
    assert sue_acct._fund_agenda_take == sue_acct._fund_take
    assert bob_acct._fund_agenda_give == bob_acct._fund_give
    assert bob_acct._fund_agenda_take == bob_acct._fund_take
    assert zia_acct._fund_agenda_give == zia_acct._fund_give
    assert zia_acct._fund_agenda_take == zia_acct._fund_take
    assert sue_acct._fund_agenda_ratio_give == 0.05
    assert sue_acct._fund_agenda_ratio_take == 0.2
    assert bob_acct._fund_agenda_ratio_give == 0.15
    assert bob_acct._fund_agenda_ratio_take == 0.3
    assert zia_acct._fund_agenda_ratio_give == 0.8
    assert zia_acct._fund_agenda_ratio_take == 0.5


def test_BudUnit_settle_bud_CreatesGroupUnitWith_budunit_v001():
    # ESTABLISH / WHEN
    yao_bud = budunit_v001()
    yao_bud.settle_bud()

    # THEN
    assert yao_bud._groupunits is not None
    assert len(yao_bud._groupunits) == 34
    everyone_accts_len = None
    everyone_group = yao_bud.get_groupunit(";Everyone")
    everyone_accts_len = len(everyone_group._memberships)
    assert everyone_accts_len == 22

    # WHEN
    yao_bud.settle_bud()
    item_dict = yao_bud._item_dict

    # THEN
    # print(f"{len(item_dict)=}")
    db_item = item_dict.get(yao_bud.make_l1_way("D&B"))
    assert len(db_item.awardlinks) == 3
    # for item_key in item_dict:
    #     print(f"{item_key=}")
    #     if item.item_tag == "D&B":
    #         print(f"{item.item_tag=} {item.awardlinks=}")
    #         db_awardlink_len = len(item.awardlinks)
    # assert db_awardlink_len == 3
