from src._road.finance import default_fund_pool
from src._road.road import RoadUnit
from src.bud.acct import acctunit_shop
from src.bud.group import awardlink_shop, awardline_shop
from src.bud.examples.example_buds import (
    budunit_v001,
    budunit_v001_with_large_agenda,
    get_budunit_with7amCleanTableReason,
    get_budunit_with_4_levels,
)
from src.bud.bud import BudUnit, budunit_shop
from src.bud.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass


def test_BudUnit_settle_bud_Sets_ideaunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_budunit = get_budunit_with7amCleanTableReason()
    casa_road = x_budunit.make_l1_road("casa")
    catt_road = x_budunit.make_l1_road("cat have dinner")
    week_road = x_budunit.make_l1_road("weekdays")
    x_budunit._idearoot._fund_onset = 13
    x_budunit._idearoot._fund_cease = 13
    x_budunit.get_idea_obj(casa_road)._fund_onset = 13
    x_budunit.get_idea_obj(casa_road)._fund_cease = 13
    x_budunit.get_idea_obj(catt_road)._fund_onset = 13
    x_budunit.get_idea_obj(catt_road)._fund_cease = 13
    x_budunit.get_idea_obj(week_road)._fund_onset = 13
    x_budunit.get_idea_obj(week_road)._fund_cease = 13

    assert x_budunit._idearoot._fund_onset == 13
    assert x_budunit._idearoot._fund_cease == 13
    assert x_budunit.get_idea_obj(casa_road)._fund_onset == 13
    assert x_budunit.get_idea_obj(casa_road)._fund_cease == 13
    assert x_budunit.get_idea_obj(catt_road)._fund_onset == 13
    assert x_budunit.get_idea_obj(catt_road)._fund_cease == 13
    assert x_budunit.get_idea_obj(week_road)._fund_onset == 13
    assert x_budunit.get_idea_obj(week_road)._fund_cease == 13

    # WHEN
    x_budunit.settle_bud()

    # THEN
    assert x_budunit._idearoot._fund_onset != 13
    assert x_budunit._idearoot._fund_cease != 13
    assert x_budunit.get_idea_obj(casa_road)._fund_onset != 13
    assert x_budunit.get_idea_obj(casa_road)._fund_cease != 13
    assert x_budunit.get_idea_obj(catt_road)._fund_onset != 13
    assert x_budunit.get_idea_obj(catt_road)._fund_cease != 13
    assert x_budunit.get_idea_obj(week_road)._fund_onset != 13
    assert x_budunit.get_idea_obj(week_road)._fund_cease != 13


def test_BudUnit_settle_bud_Sets_ideaunit_fund_onset_fund_cease_Scenario1():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", _tally=10)

    auto_text = "auto"
    auto_road = yao_budunit.make_l1_road(auto_text)
    auto_idea = ideaunit_shop(auto_text, _mass=10)
    yao_budunit.set_l1_idea(auto_idea)

    barn_text = "barn"
    barn_road = yao_budunit.make_l1_road(barn_text)
    barn_idea = ideaunit_shop(barn_text, _mass=60)
    yao_budunit.set_l1_idea(barn_idea)
    lamb_text = "lambs"
    lamb_road = yao_budunit.make_road(barn_road, lamb_text)
    lamb_idea = ideaunit_shop(lamb_text, _mass=1)
    yao_budunit.set_idea(lamb_idea, parent_road=barn_road)
    duck_text = "ducks"
    duck_road = yao_budunit.make_road(barn_road, duck_text)
    duck_idea = ideaunit_shop(duck_text, _mass=2)
    yao_budunit.set_idea(duck_idea, parent_road=barn_road)

    coal_text = "coal"
    coal_road = yao_budunit.make_l1_road(coal_text)
    coal_idea = ideaunit_shop(coal_text, _mass=30)
    yao_budunit.set_l1_idea(coal_idea)

    assert yao_budunit._idearoot._fund_onset is None
    assert yao_budunit._idearoot._fund_cease is None
    assert yao_budunit.get_idea_obj(auto_road)._fund_onset is None
    assert yao_budunit.get_idea_obj(auto_road)._fund_cease is None
    assert yao_budunit.get_idea_obj(barn_road)._fund_onset is None
    assert yao_budunit.get_idea_obj(barn_road)._fund_cease is None
    assert yao_budunit.get_idea_obj(coal_road)._fund_onset is None
    assert yao_budunit.get_idea_obj(coal_road)._fund_cease is None
    lamb_before = yao_budunit.get_idea_obj(road=lamb_road)
    assert lamb_before._fund_onset is None
    assert lamb_before._fund_cease is None
    duck_before = yao_budunit.get_idea_obj(road=duck_road)
    assert duck_before._fund_onset is None
    assert duck_before._fund_cease is None

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit._idearoot._fund_onset == 0.0
    assert yao_budunit._idearoot._fund_cease == default_fund_pool()
    assert yao_budunit.get_idea_obj(auto_road)._fund_onset == 0.0
    assert yao_budunit.get_idea_obj(auto_road)._fund_cease == default_fund_pool() * 0.1
    assert yao_budunit.get_idea_obj(barn_road)._fund_onset == default_fund_pool() * 0.1
    assert yao_budunit.get_idea_obj(barn_road)._fund_cease == default_fund_pool() * 0.7
    assert yao_budunit.get_idea_obj(coal_road)._fund_onset == default_fund_pool() * 0.7
    assert yao_budunit.get_idea_obj(coal_road)._fund_cease == default_fund_pool() * 1.0

    duck_after = yao_budunit.get_idea_obj(road=duck_road)
    assert duck_after._fund_onset == default_fund_pool() * 0.1
    assert duck_after._fund_cease == default_fund_pool() * 0.5
    lamb_after = yao_budunit.get_idea_obj(road=lamb_road)
    assert lamb_after._fund_onset == default_fund_pool() * 0.5
    assert lamb_after._fund_cease == default_fund_pool() * 0.7


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeIdeasOfZero_massScenario0():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    sue_bud.set_idea(floor_idea, casa_road)
    sue_bud.set_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_text)
    sue_bud.set_idea(ideaunit_shop(status_text, _mass=0), casa_road)

    non_text = "not clean"
    yes_text = "yes clean"
    non_road = sue_bud.make_road(status_road, non_text)
    yes_road = sue_bud.make_road(status_road, yes_text)
    sue_bud.set_idea(ideaunit_shop(non_text), status_road)
    sue_bud.set_idea(ideaunit_shop(yes_text, _mass=2), status_road)

    assert sue_bud.get_idea_obj(casa_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(status_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(non_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(yes_road)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._fund_pool=}")
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(status_road)._fund_ratio == 0.0
    assert sue_bud.get_idea_obj(non_road)._fund_ratio == 0.0
    assert sue_bud.get_idea_obj(yes_road)._fund_ratio == 0.0


def test_BudUnit_settle_bud_Sets_fund_ratio_WithSomeIdeasOfZero_massScenario1():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    sue_bud.set_idea(floor_idea, casa_road)
    sue_bud.set_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_text)
    sue_bud.set_idea(ideaunit_shop(status_text), casa_road)

    status_idea = sue_bud.get_idea_obj(status_road)
    print(f"{status_idea._mass=}")
    print("This should raise error: 'Ideaunit._'")

    clean_text = "clean"
    clean_road = sue_bud.make_road(status_road, clean_text)
    very_text = "very_much"
    mod_text = "moderately"
    dirty_text = "dirty"

    sue_bud.set_idea(ideaunit_shop(clean_text, _mass=0), status_road)
    sue_bud.set_idea(ideaunit_shop(very_text), clean_road)
    sue_bud.set_idea(ideaunit_shop(mod_text, _mass=2), clean_road)
    sue_bud.set_idea(ideaunit_shop(dirty_text), clean_road)

    very_road = sue_bud.make_road(clean_road, very_text)
    mod_road = sue_bud.make_road(clean_road, mod_text)
    dirty_road = sue_bud.make_road(clean_road, dirty_text)
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(status_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(clean_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(very_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(mod_road)._fund_ratio is None
    assert sue_bud.get_idea_obj(dirty_road)._fund_ratio is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._fund_pool=}")
    assert sue_bud.get_idea_obj(casa_road)._fund_ratio == 0.5
    assert sue_bud.get_idea_obj(floor_road)._fund_ratio == 0.25
    assert sue_bud.get_idea_obj(status_road)._fund_ratio == 0.25
    assert sue_bud.get_idea_obj(clean_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(very_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(mod_road)._fund_ratio == 0
    assert sue_bud.get_idea_obj(dirty_road)._fund_ratio == 0


def test_BudUnit_settle_bud_WhenIdeaUnitHasFundsBut_kidsHaveNoMassDistributeFundsToAcctUnits_scenario0():
    sue_budunit = budunit_shop("Sue")
    yao_text = "Yao"
    sue_budunit.add_acctunit(yao_text)
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text, _mass=1)

    swim_text = "swimming"
    swim_road = sue_budunit.make_road(casa_road, swim_text)
    swim_idea = ideaunit_shop(swim_text, _mass=8)

    clean_text = "cleaning"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    clean_idea = ideaunit_shop(clean_text, _mass=2)
    sue_budunit.set_idea(ideaunit_shop(clean_text), casa_road)

    sweep_text = "sweep"
    sweep_road = sue_budunit.make_road(clean_road, sweep_text)
    sweep_idea = ideaunit_shop(sweep_text, _mass=0)
    vaccum_text = "vaccum"
    vaccum_road = sue_budunit.make_road(clean_road, vaccum_text)
    vaccum_idea = ideaunit_shop(vaccum_text, _mass=0)

    sue_budunit.set_l1_idea(casa_idea)
    sue_budunit.set_idea(swim_idea, casa_road)
    sue_budunit.set_idea(clean_idea, casa_road)
    sue_budunit.set_idea(sweep_idea, clean_road)  # _mass=0
    sue_budunit.set_idea(vaccum_idea, clean_road)  # _mass=0

    assert sue_budunit.get_idea_obj(casa_road)._fund_ratio is None
    assert sue_budunit.get_idea_obj(swim_road)._fund_ratio is None
    assert sue_budunit.get_idea_obj(clean_road)._fund_ratio is None
    assert sue_budunit.get_idea_obj(sweep_road)._fund_ratio is None
    assert sue_budunit.get_idea_obj(vaccum_road)._fund_ratio is None
    assert sue_budunit.get_groupbox(yao_text) is None

    assert not sue_budunit._offtrack_fund
    assert sue_budunit.get_acct(yao_text)._fund_give == 0
    assert sue_budunit.get_acct(yao_text)._fund_take == 0

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    print(f"{sue_budunit._fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_budunit.get_idea_obj(casa_road)._fund_ratio == 1
    assert sue_budunit.get_idea_obj(swim_road)._fund_ratio == 0.8
    assert sue_budunit.get_idea_obj(clean_road)._fund_ratio == clean_fund_ratio
    assert sue_budunit.get_idea_obj(sweep_road)._fund_ratio == 0
    assert sue_budunit.get_idea_obj(vaccum_road)._fund_ratio == 0
    assert sue_budunit.get_groupbox(yao_text)._fund_give == 0
    assert sue_budunit.get_groupbox(yao_text)._fund_take == 0

    assert sue_budunit._offtrack_fund == clean_fund_ratio * default_fund_pool()
    assert sue_budunit.get_acct(yao_text)._fund_give == default_fund_pool()
    assert sue_budunit.get_acct(yao_text)._fund_take == default_fund_pool()


def test_BudUnit_settle_bud_TreeTraverseSetsAwardLine_fundFromRootCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # idea tree has no awardlinks
    assert sue_bud._idearoot._awardlines == {}
    sue_text = "Sue"
    week_text = "weekdays"
    nation_text = "nation-state"
    sue_awardlink = awardlink_shop(group_id=sue_text)
    sue_bud.add_acctunit(acct_id=sue_text)
    sue_bud._idearoot.set_awardlink(awardlink=sue_awardlink)
    # idea tree has awardlines
    assert sue_bud._idearoot._awardheirs.get(sue_text) is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._idearoot._awardheirs.get(sue_text) is not None
    assert sue_bud._idearoot._awardheirs.get(sue_text).group_id == sue_text
    assert sue_bud._idearoot._awardlines != {}
    root_idea = sue_bud.get_idea_obj(road=sue_bud._idearoot._label)
    sue_awardline = sue_bud._idearoot._awardlines.get(sue_text)
    print(f"{sue_awardline._fund_give=} {root_idea._fund_ratio=} ")
    print(f"  {sue_awardline._fund_take=} {root_idea._fund_ratio=} ")
    sum_x = 0
    cat_road = sue_bud.make_l1_road("cat have dinner")
    cat_idea = sue_bud.get_idea_obj(cat_road)
    week_road = sue_bud.make_l1_road(week_text)
    week_idea = sue_bud.get_idea_obj(week_road)
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    nation_road = sue_bud.make_l1_road(nation_text)
    nation_idea = sue_bud.get_idea_obj(nation_road)
    sum_x = cat_idea._fund_ratio
    print(f"{cat_idea._fund_ratio=} {sum_x} ")
    sum_x += week_idea._fund_ratio
    print(f"{week_idea._fund_ratio=} {sum_x} ")
    sum_x += casa_idea._fund_ratio
    print(f"{casa_idea._fund_ratio=} {sum_x} ")
    sum_x += nation_idea._fund_ratio
    print(f"{nation_idea._fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._fund_ratio
    #     print(f"  {kid_idea._fund_ratio=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sue_awardline._fund_give, 15) == default_fund_pool()
    assert round(sue_awardline._fund_take, 15) == default_fund_pool()
    x_awardline = awardline_shop(sue_text, default_fund_pool(), default_fund_pool())
    assert sue_bud._idearoot._awardlines == {x_awardline.group_id: x_awardline}


def test_BudUnit_settle_bud_TreeTraverseSets_awardlines_ToRootIdeaUnitFromNonRootIdeaUnit():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    sue_text = "Sue"
    sue_bud.add_acctunit(sue_text)
    casa_road = sue_bud.make_l1_road("casa")
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(group_id=sue_text))
    assert sue_bud._idearoot._awardlines == {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._idearoot._awardlines != {}
    print(f"{sue_bud._idearoot._awardlines=}")
    x_awardline = awardline_shop(
        group_id=sue_text,
        _fund_give=0.230769231 * default_fund_pool(),
        _fund_take=0.230769231 * default_fund_pool(),
    )
    assert sue_bud._idearoot._awardlines == {x_awardline.group_id: x_awardline}
    casa_ideaunit = sue_bud.get_idea_obj(casa_road)
    assert casa_ideaunit._awardlines != {}
    assert casa_ideaunit._awardlines == {x_awardline.group_id: x_awardline}


def test_BudUnit_settle_bud_WithRootLevelAwardLinkSetsGroupBox_fund_give_fund_take():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    sue_bud.set_acctunit(acctunit_shop(yao_text))
    sue_bud.set_acctunit(acctunit_shop(zia_text))
    sue_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_text, give_force=10)
    x_idearoot = sue_bud.get_idea_obj(sue_bud._real_id)
    x_idearoot.set_awardlink(awardlink=yao_awardlink)
    x_idearoot.set_awardlink(awardlink=zia_awardlink)
    x_idearoot.set_awardlink(awardlink=xio_awardlink)
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    yao_groupbox = sue_bud.get_groupbox(yao_text)
    zia_groupbox = sue_bud.get_groupbox(zia_text)
    xio_groupbox = sue_bud.get_groupbox(xio_text)
    assert yao_groupbox._fund_give == 0.5 * default_fund_pool()
    assert yao_groupbox._fund_take == 0.75 * default_fund_pool()
    assert zia_groupbox._fund_give == 0.25 * default_fund_pool()
    assert zia_groupbox._fund_take == 0.125 * default_fund_pool()
    assert xio_groupbox._fund_give == 0.25 * default_fund_pool()
    assert xio_groupbox._fund_take == 0.125 * default_fund_pool()
    cred_sum1 = yao_groupbox._fund_give
    cred_sum1 += zia_groupbox._fund_give + xio_groupbox._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupbox._fund_take
    debt_sum1 += zia_groupbox._fund_take + xio_groupbox._fund_take
    assert debt_sum1 == 1 * default_fund_pool()

    # ESTABLISH
    sue_bud.set_acctunit(acctunit_shop(sue_text))
    sue_awardlink = awardlink_shop(sue_text, give_force=37)
    x_idearoot.set_awardlink(sue_awardlink)
    assert len(x_idearoot._awardlinks) == 4
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 4

    # WHEN
    sue_bud.settle_bud()

    # THEN
    yao_groupbox = sue_bud.get_groupbox(yao_text)
    zia_groupbox = sue_bud.get_groupbox(zia_text)
    xio_groupbox = sue_bud.get_groupbox(xio_text)
    sue_groupbox = sue_bud.get_groupbox(sue_text)
    assert yao_groupbox._fund_give != 0.5 * default_fund_pool()
    assert yao_groupbox._fund_take != 0.75 * default_fund_pool()
    assert zia_groupbox._fund_give != 0.25 * default_fund_pool()
    assert zia_groupbox._fund_take != 0.125 * default_fund_pool()
    assert xio_groupbox._fund_give != 0.25 * default_fund_pool()
    assert xio_groupbox._fund_take != 0.125 * default_fund_pool()
    assert sue_groupbox._fund_give is not None
    assert sue_groupbox._fund_take is not None
    cred_sum1 = yao_groupbox._fund_give + zia_groupbox._fund_give
    cred_sum1 += xio_groupbox._fund_give + sue_groupbox._fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupbox._fund_take + zia_groupbox._fund_take
    debt_sum1 += xio_groupbox._fund_take + sue_groupbox._fund_take
    assert round(debt_sum1) == 1 * default_fund_pool()


def test_BudUnit_settle_bud_WithLevel3AwardLinkSetsGroupBox_fund_give_fund_take():
    # ESTABLISH
    bob_text = "bob"
    x_bud = budunit_shop(bob_text)
    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)
    x_bud.set_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_text, give_force=10)
    swim_idea = x_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(xio_awardlink)
    assert len(x_bud.get_acctunit_group_ids_dict()) == 3

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_groupbox = x_bud.get_groupbox(yao_text)
    zia_groupbox = x_bud.get_groupbox(zia_text)
    xio_groupbox = x_bud.get_groupbox(xio_text)
    assert yao_groupbox._fund_give == 0.5 * default_fund_pool()
    assert yao_groupbox._fund_take == 0.75 * default_fund_pool()
    assert zia_groupbox._fund_give == 0.25 * default_fund_pool()
    assert zia_groupbox._fund_take == 0.125 * default_fund_pool()
    assert xio_groupbox._fund_give == 0.25 * default_fund_pool()
    assert xio_groupbox._fund_take == 0.125 * default_fund_pool()
    groupbox_fund_give_sum = (
        yao_groupbox._fund_give + zia_groupbox._fund_give + xio_groupbox._fund_give
    )
    groupbox_fund_take_sum = (
        yao_groupbox._fund_take + zia_groupbox._fund_take + xio_groupbox._fund_take
    )
    assert groupbox_fund_give_sum == 1 * default_fund_pool()
    assert groupbox_fund_take_sum == 1 * default_fund_pool()


def test_BudUnit_settle_bud_CreatesNewGroupBoxAndSets_fund_give_fund_take():
    # ESTABLISH
    yao_text = "yao"
    x_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)
    x_bud.set_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    # x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_text, give_force=10)
    swim_idea = x_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(xio_awardlink)
    assert len(x_bud.get_acctunit_group_ids_dict()) == 2

    # WHEN
    x_bud.settle_bud()

    # THEN
    yao_groupbox = x_bud.get_groupbox(yao_text)
    zia_groupbox = x_bud.get_groupbox(zia_text)
    xio_groupbox = x_bud.get_groupbox(xio_text)
    assert len(x_bud.get_acctunit_group_ids_dict()) != len(x_bud._groupboxs)
    assert yao_groupbox._fund_give == 0.5 * default_fund_pool()
    assert yao_groupbox._fund_take == 0.75 * default_fund_pool()
    assert zia_groupbox._fund_give == 0.25 * default_fund_pool()
    assert zia_groupbox._fund_take == 0.125 * default_fund_pool()
    assert xio_groupbox._fund_give == 0.25 * default_fund_pool()
    assert xio_groupbox._fund_take == 0.125 * default_fund_pool()
    groupbox_fund_give_sum = (
        yao_groupbox._fund_give + zia_groupbox._fund_give + xio_groupbox._fund_give
    )
    groupbox_fund_take_sum = (
        yao_groupbox._fund_take + zia_groupbox._fund_take + xio_groupbox._fund_take
    )
    assert groupbox_fund_give_sum == 1 * default_fund_pool()
    assert groupbox_fund_take_sum == 1 * default_fund_pool()


def test_BudUnit_settle_bud_WithLevel3AwardLinkAndEmptyAncestorsSetsGroupBox_fund_give_fund_take():
    # ESTABLISH
    yao_text = "yao"
    x_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = x_bud.make_l1_road(swim_text)
    x_bud.set_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    x_bud.set_acctunit(acctunit_shop(yao_text))
    x_bud.set_acctunit(acctunit_shop(zia_text))
    x_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_text, give_force=10)
    swim_idea = x_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(xio_awardlink)

    # no awardlinks attached to this one
    x_bud.set_l1_idea(ideaunit_shop("hunt", _mass=3))

    # WHEN
    x_bud.settle_bud()

    # THEN
    x_idearoot = x_bud.get_idea_obj(x_bud._real_id)
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._awardlinks[xio_text]
    assert str(excinfo.value) == f"'{xio_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_idearoot._kids["hunt"]._awardheirs[xio_text]
    assert str(excinfo.value) == f"'{xio_text}'"

    # THEN
    yao_groupbox = x_bud.get_groupbox(yao_text)
    zia_groupbox = x_bud.get_groupbox(zia_text)
    xio_groupbox = x_bud.get_groupbox(xio_text)
    assert yao_groupbox._fund_give == 0.125 * default_fund_pool()
    assert yao_groupbox._fund_take == 0.1875 * default_fund_pool()
    assert zia_groupbox._fund_give == 0.0625 * default_fund_pool()
    assert zia_groupbox._fund_take == 0.03125 * default_fund_pool()
    assert xio_groupbox._fund_give == 0.0625 * default_fund_pool()
    assert xio_groupbox._fund_take == 0.03125 * default_fund_pool()
    assert (
        yao_groupbox._fund_give + zia_groupbox._fund_give + xio_groupbox._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        yao_groupbox._fund_take + zia_groupbox._fund_take + xio_groupbox._fund_take
        == 0.25 * default_fund_pool()
    )


def test_BudUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkBudFund():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_bud.set_acctunit(acctunit_shop(yao_text))
    sue_bud.set_acctunit(acctunit_shop(zia_text))
    sue_bud.set_acctunit(acctunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    Xio_awardlink = awardlink_shop(Xio_text, give_force=10)
    sue_bud._idearoot.set_awardlink(yao_awardlink)
    sue_bud._idearoot.set_awardlink(zia_awardlink)
    sue_bud._idearoot.set_awardlink(Xio_awardlink)
    assert len(sue_bud._idearoot._awardlinks) == 3

    # WHEN
    idea_dict = sue_bud.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_bob = idea_dict.get(sue_bud._real_id)
    assert len(idea_bob._awardheirs) == 3

    bheir_yao = idea_bob._awardheirs.get(yao_text)
    bheir_zia = idea_bob._awardheirs.get(zia_text)
    bheir_Xio = idea_bob._awardheirs.get(Xio_text)
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
    # for group in x_bud._idearoot._awardheirs.values():
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
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_force=5)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=sue_awardlink)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=bob_awardlink)
    yao_bud.edit_idea_attr(yao_bud._real_id, awardlink=zia_awardlink)

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
    sue_sue_membership = sue_acctunit.get_membership(sue_text)
    bob_bob_membership = bob_acctunit.get_membership(bob_text)
    zia_zia_membership = zia_acctunit.get_membership(zia_text)
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
    xio_text = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_text))
    yao_bud._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_force=13))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    xio_groupbox = yao_bud.get_groupbox(xio_text)
    xio_xio_membership = xio_groupbox.get_membership(xio_text)
    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
    sue_sue_membership = sue_acctunit.get_membership(sue_text)
    bob_bob_membership = bob_acctunit.get_membership(bob_text)
    zia_zia_membership = zia_acctunit.get_membership(zia_text)
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
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.set_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    bl_sue = awardlink_shop(sue_text, 20, take_force=40)
    bl_bob = awardlink_shop(bob_text, 10, take_force=5)
    bl_zia = awardlink_shop(zia_text, 10, take_force=5)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_sue)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_bob)
    yao_bud.get_idea_obj(swim_road).set_awardlink(bl_zia)

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)

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
    xio_text = "Xio"
    yao_bud.set_acctunit(acctunit_shop(xio_text))
    yao_bud._idearoot.set_awardlink(awardlink_shop(xio_text, 20, take_force=10))
    yao_bud.settle_bud()

    # THEN
    xio_acctunit = yao_bud.get_acct(xio_text)

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
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.set_l1_idea(ideaunit_shop(swim_text))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_awardlink = awardlink_shop(sue_text, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_text, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_text, 10, take_force=5)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(sue_awardlink)
    swim_idea.set_awardlink(bob_awardlink)
    swim_idea.set_awardlink(zia_awardlink)

    # no awardlinks attached to this one
    hunt_text = "hunt"
    yao_bud.set_l1_idea(ideaunit_shop(hunt_text, _mass=3))

    # WHEN
    yao_bud.settle_bud()

    # THEN
    sue_groupbox = yao_bud.get_groupbox(sue_text)
    bob_groupbox = yao_bud.get_groupbox(bob_text)
    zia_groupbox = yao_bud.get_groupbox(zia_text)
    assert sue_groupbox._fund_give != 0.5 * default_fund_pool()
    assert sue_groupbox._fund_take != 0.8 * default_fund_pool()
    assert bob_groupbox._fund_give != 0.25 * default_fund_pool()
    assert bob_groupbox._fund_take != 0.1 * default_fund_pool()
    assert zia_groupbox._fund_give != 0.25 * default_fund_pool()
    assert zia_groupbox._fund_take != 0.1 * default_fund_pool()
    assert (
        sue_groupbox._fund_give + bob_groupbox._fund_give + zia_groupbox._fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        sue_groupbox._fund_take + bob_groupbox._fund_take + zia_groupbox._fund_take
        == 0.25 * default_fund_pool()
    )

    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)

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


def test_BudUnit_settle_bud_CreatesNewGroupBoxAndSets_fund_give_fund_take():
    # ESTABLISH
    bob_text = "bob"
    bob_bud = budunit_shop(bob_text)
    swim_text = "swim"
    swim_road = bob_bud.make_l1_road(swim_text)
    bob_bud.set_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    xio_text = "Xio"
    bob_bud.set_acctunit(acctunit_shop(yao_text))
    bob_bud.set_acctunit(acctunit_shop(zia_text))
    # bob_bud.set_acctunit(acctunit_shop(xio_text))
    yao_awardlink = awardlink_shop(yao_text, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_text, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_text, give_force=10)
    swim_idea = bob_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(yao_awardlink)
    swim_idea.set_awardlink(zia_awardlink)
    swim_idea.set_awardlink(xio_awardlink)
    assert len(bob_bud.get_acctunit_group_ids_dict()) == 2

    # WHEN
    bob_bud.settle_bud()

    # THEN
    xio_groupbox = bob_bud.get_groupbox(xio_text)
    assert len(bob_bud.get_acctunit_group_ids_dict()) != len(bob_bud._groupboxs)
    assert not bob_bud.acct_exists(xio_text)
    yao_acctunit = bob_bud.get_acct(yao_text)
    zia_acctunit = bob_bud.get_acct(zia_text)
    acctunit_fund_give_sum = yao_acctunit._fund_give + zia_acctunit._fund_give
    acctunit_fund_take_sum = yao_acctunit._fund_take + zia_acctunit._fund_take
    assert acctunit_fund_give_sum == default_fund_pool()
    assert acctunit_fund_take_sum == default_fund_pool()


def test_BudUnit_settle_bud_CorrectlySetsAcctUnit_fund_give_fund_take():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    yao_bud.set_l1_idea(ideaunit_shop("swim"))
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_bud.set_acctunit(acctunit_shop(sue_text, 8))
    yao_bud.set_acctunit(acctunit_shop(bob_text))
    yao_bud.set_acctunit(acctunit_shop(zia_text))
    sue_acctunit = yao_bud.get_acct(sue_text)
    bob_acctunit = yao_bud.get_acct(bob_text)
    zia_acctunit = yao_bud.get_acct(zia_text)
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


def clear_all_acctunits_groupboxs_fund_agenda_give_take(x_bud: BudUnit):
    # DELETE bud_agenda_debt and bud_agenda_cred
    for groupbox_x in x_bud._groupboxs.values():
        groupbox_x.clear_fund_give_take()
        # for membership_x in groupbox_x._accts.values():
        #     print(f"{groupbox_x.} {membership_x.}  {membership_x._fund_give:.6f} {membership_x.debtit_score=} {membership__fund_take:t:.6f} {membership_x.} ")

    # DELETE bud_agenda_debt and bud_agenda_cred
    for x_acctunit in x_bud._accts.values():
        x_acctunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupbox_give: float = 0
    sum_groupbox_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_sums(self, x_bud: BudUnit):
        for x_groupbox in x_bud._groupboxs.values():
            self.sum_groupbox_give += x_groupbox._fund_agenda_give
            self.sum_groupbox_take += x_groupbox._fund_agenda_take
            for membership_x in x_groupbox._memberships.values():
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
        for acctunit in x_bud._accts.values():
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

    def set_sums(self, agenda_dict: dict[RoadUnit, IdeaUnit]):
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
    clear_all_acctunits_groupboxs_fund_agenda_give_take(yao_bud)

    # TEST bud_agenda_debt and bud_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_bud)
    assert x_groupagendametrics.sum_groupbox_give == 0
    assert x_groupagendametrics.sum_groupbox_take == 0
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
    # for idea_road in yao_bud._idea_dict.keys():
    #     print(f"{idea_road=}")
    # for x_acct in yao_bud._accts.values():
    #     for x_membership in x_acct._memberships.values():
    #         print(f"{x_membership.group_id=}")

    # THEN
    assert len(agenda_dict) == 63
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_bud_agenda_share=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    assert x_awardagendametrics.agenda_no_bud_i_sum == 0.003747268 * default_fund_pool()
    assert (
        x_awardagendametrics.agenda_yes_bud_i_sum == 0.002796504 * default_fund_pool()
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_bud_i_sum
        + x_awardagendametrics.agenda_yes_bud_i_sum,
        x_awardagendametrics.sum_bud_agenda_share,
    )
    assert (
        x_awardagendametrics.sum_bud_agenda_share == 0.006543772 * default_fund_pool()
    )

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_bud)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 2796504
    print(f"{x_groupagendametrics.sum_groupbox_give=}")
    assert are_equal(x_groupagendametrics.sum_groupbox_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupbox_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_bud_i_sum,
        x_groupagendametrics.sum_groupbox_give,
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
        for acctunit in x_bud._accts.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_BudUnit_agenda_ratio_cred_debt_IsCorrectlySetWhenBudIsEmpty():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    sue_acctunit = acctunit_shop(sue_text, 0.5, debtit_score=2)
    bob_acctunit = acctunit_shop(bob_text, 1.5, debtit_score=3)
    zia_acctunit = acctunit_shop(zia_text, 8, debtit_score=5)
    yao_bud.set_acctunit(sue_acctunit)
    yao_bud.set_acctunit(bob_acctunit)
    yao_bud.set_acctunit(zia_acctunit)
    yao_bud_sue_acct = yao_bud.get_acct(sue_text)
    yao_bud_bob_acct = yao_bud.get_acct(bob_text)
    yao_bud_zia_acct = yao_bud.get_acct(zia_text)

    assert yao_bud_sue_acct._fund_agenda_give in [0, None]
    assert yao_bud_sue_acct._fund_agenda_take in [0, None]
    assert yao_bud_bob_acct._fund_agenda_give in [0, None]
    assert yao_bud_bob_acct._fund_agenda_take in [0, None]
    assert yao_bud_zia_acct._fund_agenda_give in [0, None]
    assert yao_bud_zia_acct._fund_agenda_take in [0, None]
    assert yao_bud_sue_acct._fund_agenda_ratio_give != 0.05
    assert yao_bud_sue_acct._fund_agenda_ratio_take != 0.2
    assert yao_bud_bob_acct._fund_agenda_ratio_give != 0.15
    assert yao_bud_bob_acct._fund_agenda_ratio_take != 0.3
    assert yao_bud_zia_acct._fund_agenda_ratio_give != 0.8
    assert yao_bud_zia_acct._fund_agenda_ratio_take != 0.5

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud_sue_acct._fund_agenda_give == 0
    assert yao_bud_sue_acct._fund_agenda_take == 0
    assert yao_bud_bob_acct._fund_agenda_give == 0
    assert yao_bud_bob_acct._fund_agenda_take == 0
    assert yao_bud_zia_acct._fund_agenda_give == 0
    assert yao_bud_zia_acct._fund_agenda_take == 0
    assert yao_bud_sue_acct._fund_agenda_ratio_give == 0.05
    assert yao_bud_sue_acct._fund_agenda_ratio_take == 0.2
    assert yao_bud_bob_acct._fund_agenda_ratio_give == 0.15
    assert yao_bud_bob_acct._fund_agenda_ratio_take == 0.3
    assert yao_bud_zia_acct._fund_agenda_ratio_give == 0.8
    assert yao_bud_zia_acct._fund_agenda_ratio_take == 0.5


def test_BudUnit_settle_bud_CreatesGroupBoxWith_budunit_v001():
    # ESTABLISH / WHEN
    yao_bud = budunit_v001()
    yao_bud.settle_bud()

    # THEN
    assert yao_bud._groupboxs is not None
    assert len(yao_bud._groupboxs) == 34
    everyone_accts_len = None
    everyone_group = yao_bud.get_groupbox(";Everyone")
    everyone_accts_len = len(everyone_group._memberships)
    assert everyone_accts_len == 22

    # WHEN
    yao_bud.settle_bud()
    idea_dict = yao_bud._idea_dict

    # THEN
    # print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(yao_bud.make_l1_road("D&B"))
    assert len(db_idea._awardlinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._awardlinks=}")
    #         db_awardlink_len = len(idea._awardlinks)
    # assert db_awardlink_len == 3
