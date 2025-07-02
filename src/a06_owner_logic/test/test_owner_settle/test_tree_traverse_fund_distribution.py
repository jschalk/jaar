from dataclasses import dataclass
from pytest import raises as pytest_raises
from src.a01_term_logic.rope import RopeTerm, to_rope
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import awardline_shop, awardlink_shop
from src.a05_plan_logic.plan import PlanUnit, planunit_shop
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with7amCleanTableReason,
    get_ownerunit_with_4_levels,
    ownerunit_v001,
    ownerunit_v001_with_large_agenda,
)


def test_OwnerUnit_settle_owner_Sets_planunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_ownerunit = get_ownerunit_with7amCleanTableReason()
    casa_rope = x_ownerunit.make_l1_rope("casa")
    catt_rope = x_ownerunit.make_l1_rope("cat have dinner")
    wk_rope = x_ownerunit.make_l1_rope("wkdays")
    x_ownerunit.planroot._fund_onset = 13
    x_ownerunit.planroot._fund_cease = 13
    x_ownerunit.get_plan_obj(casa_rope)._fund_onset = 13
    x_ownerunit.get_plan_obj(casa_rope)._fund_cease = 13
    x_ownerunit.get_plan_obj(catt_rope)._fund_onset = 13
    x_ownerunit.get_plan_obj(catt_rope)._fund_cease = 13
    x_ownerunit.get_plan_obj(wk_rope)._fund_onset = 13
    x_ownerunit.get_plan_obj(wk_rope)._fund_cease = 13

    assert x_ownerunit.planroot._fund_onset == 13
    assert x_ownerunit.planroot._fund_cease == 13
    assert x_ownerunit.get_plan_obj(casa_rope)._fund_onset == 13
    assert x_ownerunit.get_plan_obj(casa_rope)._fund_cease == 13
    assert x_ownerunit.get_plan_obj(catt_rope)._fund_onset == 13
    assert x_ownerunit.get_plan_obj(catt_rope)._fund_cease == 13
    assert x_ownerunit.get_plan_obj(wk_rope)._fund_onset == 13
    assert x_ownerunit.get_plan_obj(wk_rope)._fund_cease == 13

    # WHEN
    x_ownerunit.settle_owner()

    # THEN
    assert x_ownerunit.planroot._fund_onset != 13
    assert x_ownerunit.planroot._fund_cease != 13
    assert x_ownerunit.get_plan_obj(casa_rope)._fund_onset != 13
    assert x_ownerunit.get_plan_obj(casa_rope)._fund_cease != 13
    assert x_ownerunit.get_plan_obj(catt_rope)._fund_onset != 13
    assert x_ownerunit.get_plan_obj(catt_rope)._fund_cease != 13
    assert x_ownerunit.get_plan_obj(wk_rope)._fund_onset != 13
    assert x_ownerunit.get_plan_obj(wk_rope)._fund_cease != 13


def test_OwnerUnit_settle_owner_Sets_planunit_fund_onset_fund_cease_Scenario1():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_ownerunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, mass=10)
    yao_ownerunit.set_l1_plan(auto_plan)

    carn_str = "carn"
    carn_rope = yao_ownerunit.make_l1_rope(carn_str)
    carn_plan = planunit_shop(carn_str, mass=60)
    yao_ownerunit.set_l1_plan(carn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_ownerunit.make_rope(carn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, mass=1)
    yao_ownerunit.set_plan(lamb_plan, parent_rope=carn_rope)
    duck_str = "ducks"
    duck_rope = yao_ownerunit.make_rope(carn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, mass=2)
    yao_ownerunit.set_plan(duck_plan, parent_rope=carn_rope)

    coal_str = "coal"
    coal_rope = yao_ownerunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, mass=30)
    yao_ownerunit.set_l1_plan(coal_plan)

    assert yao_ownerunit.planroot._fund_onset is None
    assert yao_ownerunit.planroot._fund_cease is None
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_cease is None
    assert yao_ownerunit.get_plan_obj(carn_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(carn_rope)._fund_cease is None
    assert yao_ownerunit.get_plan_obj(coal_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(coal_rope)._fund_cease is None
    lamb_before = yao_ownerunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before._fund_onset is None
    assert lamb_before._fund_cease is None
    duck_before = yao_ownerunit.get_plan_obj(rope=duck_rope)
    assert duck_before._fund_onset is None
    assert duck_before._fund_cease is None

    # WHEN
    yao_ownerunit.settle_owner()

    # THEN
    assert yao_ownerunit.planroot._fund_onset == 0.0
    assert yao_ownerunit.planroot._fund_cease == default_fund_pool()
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_onset == 0.0
    assert (
        yao_ownerunit.get_plan_obj(auto_rope)._fund_cease == default_fund_pool() * 0.1
    )
    assert (
        yao_ownerunit.get_plan_obj(carn_rope)._fund_onset == default_fund_pool() * 0.1
    )
    assert (
        yao_ownerunit.get_plan_obj(carn_rope)._fund_cease == default_fund_pool() * 0.7
    )
    assert (
        yao_ownerunit.get_plan_obj(coal_rope)._fund_onset == default_fund_pool() * 0.7
    )
    assert (
        yao_ownerunit.get_plan_obj(coal_rope)._fund_cease == default_fund_pool() * 1.0
    )

    duck_after = yao_ownerunit.get_plan_obj(rope=duck_rope)
    assert duck_after._fund_onset == default_fund_pool() * 0.1
    assert duck_after._fund_cease == default_fund_pool() * 0.5
    lamb_after = yao_ownerunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after._fund_onset == default_fund_pool() * 0.5
    assert lamb_after._fund_cease == default_fund_pool() * 0.7


def test_OwnerUnit_settle_owner_Sets_planunit_fund_onset_fund_cease_Scenario2_DifferentOrderOfPlans():
    # ESTABLISH
    yao_ownerunit = ownerunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_ownerunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, mass=10)
    yao_ownerunit.set_l1_plan(auto_plan)

    yarn_str = "yarn"
    yarn_rope = yao_ownerunit.make_l1_rope(yarn_str)
    yarn_plan = planunit_shop(yarn_str, mass=60)
    yao_ownerunit.set_l1_plan(yarn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_ownerunit.make_rope(yarn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, mass=1)
    yao_ownerunit.set_plan(lamb_plan, parent_rope=yarn_rope)
    duck_str = "ducks"
    duck_rope = yao_ownerunit.make_rope(yarn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, mass=2)
    yao_ownerunit.set_plan(duck_plan, parent_rope=yarn_rope)

    coal_str = "coal"
    coal_rope = yao_ownerunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, mass=30)
    yao_ownerunit.set_l1_plan(coal_plan)

    assert yao_ownerunit.planroot._fund_onset is None
    assert yao_ownerunit.planroot._fund_cease is None
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_cease is None
    assert yao_ownerunit.get_plan_obj(yarn_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(yarn_rope)._fund_cease is None
    assert yao_ownerunit.get_plan_obj(coal_rope)._fund_onset is None
    assert yao_ownerunit.get_plan_obj(coal_rope)._fund_cease is None
    lamb_before = yao_ownerunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before._fund_onset is None
    assert lamb_before._fund_cease is None
    duck_before = yao_ownerunit.get_plan_obj(rope=duck_rope)
    assert duck_before._fund_onset is None
    assert duck_before._fund_cease is None

    # WHEN
    yao_ownerunit.settle_owner()

    # THEN
    assert yao_ownerunit.planroot._fund_onset == 0.0
    assert yao_ownerunit.planroot._fund_cease == default_fund_pool()
    assert yao_ownerunit.get_plan_obj(auto_rope)._fund_onset == 0.0
    assert (
        yao_ownerunit.get_plan_obj(auto_rope)._fund_cease == default_fund_pool() * 0.1
    )
    assert (
        yao_ownerunit.get_plan_obj(coal_rope)._fund_onset == default_fund_pool() * 0.1
    )
    assert (
        yao_ownerunit.get_plan_obj(coal_rope)._fund_cease == default_fund_pool() * 0.4
    )
    assert (
        yao_ownerunit.get_plan_obj(yarn_rope)._fund_onset == default_fund_pool() * 0.4
    )
    assert (
        yao_ownerunit.get_plan_obj(yarn_rope)._fund_cease == default_fund_pool() * 1.0
    )

    duck_after = yao_ownerunit.get_plan_obj(rope=duck_rope)
    assert duck_after._fund_onset == default_fund_pool() * 0.4
    assert duck_after._fund_cease == default_fund_pool() * 0.8
    lamb_after = yao_ownerunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after._fund_onset == default_fund_pool() * 0.8
    assert lamb_after._fund_cease == default_fund_pool() * 1.0


def test_OwnerUnit_settle_owner_Sets_fund_ratio_WithSomePlansOfZero_massScenario0():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_owner.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_owner.set_plan(floor_plan, casa_rope)
    sue_owner.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_owner.make_rope(casa_rope, status_str)
    sue_owner.set_plan(planunit_shop(status_str, mass=0), casa_rope)

    non_str = "not clean"
    yes_str = "yes clean"
    non_rope = sue_owner.make_rope(status_rope, non_str)
    yes_rope = sue_owner.make_rope(status_rope, yes_str)
    sue_owner.set_plan(planunit_shop(non_str), status_rope)
    sue_owner.set_plan(planunit_shop(yes_str, mass=2), status_rope)

    assert sue_owner.get_plan_obj(casa_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(floor_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(status_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(non_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(yes_rope)._fund_ratio is None

    # WHEN
    sue_owner.settle_owner()

    # THEN
    print(f"{sue_owner.fund_pool=}")
    assert sue_owner.get_plan_obj(casa_rope)._fund_ratio == 0.5
    assert sue_owner.get_plan_obj(floor_rope)._fund_ratio == 0.5
    assert sue_owner.get_plan_obj(status_rope)._fund_ratio == 0.0
    assert sue_owner.get_plan_obj(non_rope)._fund_ratio == 0.0
    assert sue_owner.get_plan_obj(yes_rope)._fund_ratio == 0.0


def test_OwnerUnit_settle_owner_Sets_fund_ratio_WithSomePlansOfZero_massScenario1():
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_owner.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_owner.set_plan(floor_plan, casa_rope)
    sue_owner.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_owner.make_rope(casa_rope, status_str)
    sue_owner.set_plan(planunit_shop(status_str), casa_rope)

    status_plan = sue_owner.get_plan_obj(status_rope)
    print(f"{status_plan.mass=}")
    print("This should raise error: 'Planunit._'")

    clean_str = "clean"
    clean_rope = sue_owner.make_rope(status_rope, clean_str)
    very_str = "very_much"
    mod_str = "moderately"
    dirty_str = "dirty"

    sue_owner.set_plan(planunit_shop(clean_str, mass=0), status_rope)
    sue_owner.set_plan(planunit_shop(very_str), clean_rope)
    sue_owner.set_plan(planunit_shop(mod_str, mass=2), clean_rope)
    sue_owner.set_plan(planunit_shop(dirty_str), clean_rope)

    very_rope = sue_owner.make_rope(clean_rope, very_str)
    mod_rope = sue_owner.make_rope(clean_rope, mod_str)
    dirty_rope = sue_owner.make_rope(clean_rope, dirty_str)
    assert sue_owner.get_plan_obj(casa_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(floor_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(status_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(clean_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(very_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(mod_rope)._fund_ratio is None
    assert sue_owner.get_plan_obj(dirty_rope)._fund_ratio is None

    # WHEN
    sue_owner.settle_owner()

    # THEN
    print(f"{sue_owner.fund_pool=}")
    assert sue_owner.get_plan_obj(casa_rope)._fund_ratio == 0.5
    assert sue_owner.get_plan_obj(floor_rope)._fund_ratio == 0.25
    assert sue_owner.get_plan_obj(status_rope)._fund_ratio == 0.25
    assert sue_owner.get_plan_obj(clean_rope)._fund_ratio == 0
    assert sue_owner.get_plan_obj(very_rope)._fund_ratio == 0
    assert sue_owner.get_plan_obj(mod_rope)._fund_ratio == 0
    assert sue_owner.get_plan_obj(dirty_rope)._fund_ratio == 0


def test_OwnerUnit_settle_owner_WhenPlanUnitHasFundsBut_kidsHaveNoMassDistributeFundsToAcctUnits_scenario0():
    sue_ownerunit = ownerunit_shop("Sue")
    yao_str = "Yao"
    sue_ownerunit.add_acctunit(yao_str)
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    casa_plan = planunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_rope = sue_ownerunit.make_rope(casa_rope, swim_str)
    swim_plan = planunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_rope = sue_ownerunit.make_rope(casa_rope, clean_str)
    clean_plan = planunit_shop(clean_str, mass=2)
    sue_ownerunit.set_plan(planunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_ownerunit.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_rope = sue_ownerunit.make_rope(clean_rope, vaccum_str)
    vaccum_plan = planunit_shop(vaccum_str, mass=0)

    sue_ownerunit.set_l1_plan(casa_plan)
    sue_ownerunit.set_plan(swim_plan, casa_rope)
    sue_ownerunit.set_plan(clean_plan, casa_rope)
    sue_ownerunit.set_plan(sweep_plan, clean_rope)  # _mass=0
    sue_ownerunit.set_plan(vaccum_plan, clean_rope)  # _mass=0

    assert sue_ownerunit.get_plan_obj(casa_rope)._fund_ratio is None
    assert sue_ownerunit.get_plan_obj(swim_rope)._fund_ratio is None
    assert sue_ownerunit.get_plan_obj(clean_rope)._fund_ratio is None
    assert sue_ownerunit.get_plan_obj(sweep_rope)._fund_ratio is None
    assert sue_ownerunit.get_plan_obj(vaccum_rope)._fund_ratio is None
    assert sue_ownerunit.get_groupunit(yao_str) is None

    assert not sue_ownerunit._offtrack_fund
    assert sue_ownerunit.get_acct(yao_str)._fund_give == 0
    assert sue_ownerunit.get_acct(yao_str)._fund_take == 0

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    print(f"{sue_ownerunit.fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_ownerunit.get_plan_obj(casa_rope)._fund_ratio == 1
    assert sue_ownerunit.get_plan_obj(swim_rope)._fund_ratio == 0.8
    assert sue_ownerunit.get_plan_obj(clean_rope)._fund_ratio == clean_fund_ratio
    assert sue_ownerunit.get_plan_obj(sweep_rope)._fund_ratio == 0
    assert sue_ownerunit.get_plan_obj(vaccum_rope)._fund_ratio == 0
    assert sue_ownerunit.get_groupunit(yao_str)._fund_give == 0
    assert sue_ownerunit.get_groupunit(yao_str)._fund_take == 0

    assert sue_ownerunit._offtrack_fund == clean_fund_ratio * default_fund_pool()
    assert sue_ownerunit.get_acct(yao_str)._fund_give == default_fund_pool()
    assert sue_ownerunit.get_acct(yao_str)._fund_take == default_fund_pool()


def test_OwnerUnit_settle_owner_TreeTraverseSetsAwardLine_fundFromRootCorrectly():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    sue_owner.settle_owner()
    # plan tree has no awardlinks
    assert sue_owner.planroot._awardlines == {}
    sue_str = "Sue"
    wk_str = "wkdays"
    nation_str = "nation"
    sue_awardlink = awardlink_shop(awardee_title=sue_str)
    sue_owner.add_acctunit(acct_name=sue_str)
    sue_owner.planroot.set_awardlink(awardlink=sue_awardlink)
    # plan tree has awardlines
    assert sue_owner.planroot._awardheirs.get(sue_str) is None

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner.planroot._awardheirs.get(sue_str) is not None
    assert sue_owner.planroot._awardheirs.get(sue_str).awardee_title == sue_str
    assert sue_owner.planroot._awardlines != {}
    root_rope = to_rope(sue_owner.planroot.plan_label)
    root_plan = sue_owner.get_plan_obj(rope=root_rope)
    sue_awardline = sue_owner.planroot._awardlines.get(sue_str)
    print(f"{sue_awardline._fund_give=} {root_plan._fund_ratio=} ")
    print(f"  {sue_awardline._fund_take=} {root_plan._fund_ratio=} ")
    sum_x = 0
    cat_rope = sue_owner.make_l1_rope("cat have dinner")
    cat_plan = sue_owner.get_plan_obj(cat_rope)
    wk_rope = sue_owner.make_l1_rope(wk_str)
    wk_plan = sue_owner.get_plan_obj(wk_rope)
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    casa_plan = sue_owner.get_plan_obj(casa_rope)
    nation_rope = sue_owner.make_l1_rope(nation_str)
    nation_plan = sue_owner.get_plan_obj(nation_rope)
    sum_x = cat_plan._fund_ratio
    print(f"{cat_plan._fund_ratio=} {sum_x} ")
    sum_x += wk_plan._fund_ratio
    print(f"{wk_plan._fund_ratio=} {sum_x} ")
    sum_x += casa_plan._fund_ratio
    print(f"{casa_plan._fund_ratio=} {sum_x} ")
    sum_x += nation_plan._fund_ratio
    print(f"{nation_plan._fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_plan in root_plan._kids.values():
    #     sum_x += kid_plan._fund_ratio
    #     print(f"  {kid_plan._fund_ratio=} {sum_x=} {kid_plan.get_plan_rope()=}")
    assert round(sue_awardline._fund_give, 15) == default_fund_pool()
    assert round(sue_awardline._fund_take, 15) == default_fund_pool()
    x_awardline = awardline_shop(sue_str, default_fund_pool(), default_fund_pool())
    assert sue_owner.planroot._awardlines == {x_awardline.awardee_title: x_awardline}


def test_OwnerUnit_settle_owner_TreeTraverseSets_awardlines_ToRootPlanUnitFromNonRootPlanUnit():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    sue_owner.settle_owner()
    sue_str = "Sue"
    sue_owner.add_acctunit(sue_str)
    casa_rope = sue_owner.make_l1_rope("casa")
    sue_owner.get_plan_obj(casa_rope).set_awardlink(
        awardlink_shop(awardee_title=sue_str)
    )
    assert sue_owner.planroot._awardlines == {}

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner.planroot._awardlines != {}
    print(f"{sue_owner.planroot._awardlines=}")
    x_awardline = awardline_shop(
        awardee_title=sue_str,
        _fund_give=0.230769231 * default_fund_pool(),
        _fund_take=0.230769231 * default_fund_pool(),
    )
    assert sue_owner.planroot._awardlines == {x_awardline.awardee_title: x_awardline}
    casa_planunit = sue_owner.get_plan_obj(casa_rope)
    assert casa_planunit._awardlines != {}
    assert casa_planunit._awardlines == {x_awardline.awardee_title: x_awardline}


def test_OwnerUnit_settle_owner_WithRootLevelAwardLinkSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    sue_str = "Sue"
    sue_owner = ownerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    sue_owner.set_acctunit(acctunit_shop(yao_str))
    sue_owner.set_acctunit(acctunit_shop(zia_str))
    sue_owner.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    root_rope = to_rope(sue_owner.planroot.plan_label)
    x_planroot = sue_owner.get_plan_obj(root_rope)
    x_planroot.set_awardlink(awardlink=yao_awardlink)
    x_planroot.set_awardlink(awardlink=zia_awardlink)
    x_planroot.set_awardlink(awardlink=xio_awardlink)
    assert len(sue_owner.get_acctunit_group_titles_dict()) == 3

    # WHEN
    sue_owner.settle_owner()

    # THEN
    yao_groupunit = sue_owner.get_groupunit(yao_str)
    zia_groupunit = sue_owner.get_groupunit(zia_str)
    xio_groupunit = sue_owner.get_groupunit(xio_str)
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
    sue_owner.set_acctunit(acctunit_shop(sue_str))
    sue_awardlink = awardlink_shop(sue_str, give_force=37)
    x_planroot.set_awardlink(sue_awardlink)
    assert len(x_planroot.awardlinks) == 4
    assert len(sue_owner.get_acctunit_group_titles_dict()) == 4

    # WHEN
    sue_owner.settle_owner()

    # THEN
    yao_groupunit = sue_owner.get_groupunit(yao_str)
    zia_groupunit = sue_owner.get_groupunit(zia_str)
    xio_groupunit = sue_owner.get_groupunit(xio_str)
    sue_groupunit = sue_owner.get_groupunit(sue_str)
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


def test_OwnerUnit_settle_owner_WithLevel3AwardLinkSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    x_owner = ownerunit_shop(bob_str)
    swim_str = "swim"
    swim_rope = x_owner.make_l1_rope(swim_str)
    x_owner.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_owner.set_acctunit(acctunit_shop(yao_str))
    x_owner.set_acctunit(acctunit_shop(zia_str))
    x_owner.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_plan = x_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(yao_awardlink)
    swim_plan.set_awardlink(zia_awardlink)
    swim_plan.set_awardlink(xio_awardlink)
    assert len(x_owner.get_acctunit_group_titles_dict()) == 3

    # WHEN
    x_owner.settle_owner()

    # THEN
    yao_groupunit = x_owner.get_groupunit(yao_str)
    zia_groupunit = x_owner.get_groupunit(zia_str)
    xio_groupunit = x_owner.get_groupunit(xio_str)
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


def test_OwnerUnit_settle_owner_CreatesNewGroupUnitAndSetsGroup_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_owner = ownerunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = x_owner.make_l1_rope(swim_str)
    x_owner.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_owner.set_acctunit(acctunit_shop(yao_str))
    x_owner.set_acctunit(acctunit_shop(zia_str))
    # x_owner.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_plan = x_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(yao_awardlink)
    swim_plan.set_awardlink(zia_awardlink)
    swim_plan.set_awardlink(xio_awardlink)
    assert len(x_owner.get_acctunit_group_titles_dict()) == 2

    # WHEN
    x_owner.settle_owner()

    # THEN
    yao_groupunit = x_owner.get_groupunit(yao_str)
    zia_groupunit = x_owner.get_groupunit(zia_str)
    xio_groupunit = x_owner.get_groupunit(xio_str)
    assert len(x_owner.get_acctunit_group_titles_dict()) != len(x_owner._groupunits)
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


def test_OwnerUnit_settle_owner_WithLevel3AwardLinkAndEmptyAncestorsSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_owner = ownerunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = x_owner.make_l1_rope(swim_str)
    x_owner.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_owner.set_acctunit(acctunit_shop(yao_str))
    x_owner.set_acctunit(acctunit_shop(zia_str))
    x_owner.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_plan = x_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(yao_awardlink)
    swim_plan.set_awardlink(zia_awardlink)
    swim_plan.set_awardlink(xio_awardlink)

    # no awardlinks attached to this one
    x_owner.set_l1_plan(planunit_shop("hunt", mass=3))

    # WHEN
    x_owner.settle_owner()

    # THEN
    x_planroot = x_owner.get_plan_obj(to_rope(x_owner.belief_label))
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardlinks[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardlinks[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardlinks[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot._kids["hunt"]._awardheirs[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot._kids["hunt"]._awardheirs[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot._kids["hunt"]._awardheirs[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"

    # THEN
    yao_groupunit = x_owner.get_groupunit(yao_str)
    zia_groupunit = x_owner.get_groupunit(zia_str)
    xio_groupunit = x_owner.get_groupunit(xio_str)
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


def test_OwnerUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkOwnerFund():
    # ESTABLISH
    sue_str = "Sue"
    sue_owner = ownerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_owner.set_acctunit(acctunit_shop(yao_str))
    sue_owner.set_acctunit(acctunit_shop(zia_str))
    sue_owner.set_acctunit(acctunit_shop(Xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    Xio_awardlink = awardlink_shop(Xio_str, give_force=10)
    sue_owner.planroot.set_awardlink(yao_awardlink)
    sue_owner.planroot.set_awardlink(zia_awardlink)
    sue_owner.planroot.set_awardlink(Xio_awardlink)
    assert len(sue_owner.planroot.awardlinks) == 3

    # WHEN
    plan_dict = sue_owner.get_plan_dict()

    # THEN
    print(f"{plan_dict.keys()=}")
    plan_bob = plan_dict.get(to_rope(sue_owner.belief_label))
    assert len(plan_bob._awardheirs) == 3

    bheir_yao = plan_bob._awardheirs.get(yao_str)
    bheir_zia = plan_bob._awardheirs.get(zia_str)
    bheir_Xio = plan_bob._awardheirs.get(Xio_str)
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
    # for group in x_owner.planroot._awardheirs.values():
    #     print(f"{group=}")
    #     assert group._fund_give is not None
    #     assert group._fund_give in [0.25, 0.5]
    #     assert group._fund_take is not None
    #     assert group._fund_take in [0.75, 0.125]
    #     fund_give_sum += group._fund_give
    #     fund_take_sum += group._fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_OwnerUnit_settle_owner_CorrectlySetsGroupLinkOwnerCredAndDebt():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_owner.set_acctunit(acctunit_shop(sue_str))
    yao_owner.set_acctunit(acctunit_shop(bob_str))
    yao_owner.set_acctunit(acctunit_shop(zia_str))
    sue_awardlink = awardlink_shop(sue_str, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_str, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_str, 10, take_force=5)
    root_rope = to_rope(yao_owner.belief_label)
    yao_owner.edit_plan_attr(root_rope, awardlink=sue_awardlink)
    yao_owner.edit_plan_attr(root_rope, awardlink=bob_awardlink)
    yao_owner.edit_plan_attr(root_rope, awardlink=zia_awardlink)

    sue_acctunit = yao_owner.get_acct(sue_str)
    bob_acctunit = yao_owner.get_acct(bob_str)
    zia_acctunit = yao_owner.get_acct(zia_str)
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
    yao_owner.settle_owner()

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

    # ESTABLISH another task, check metrics are as expected
    xio_str = "Xio"
    yao_owner.set_acctunit(acctunit_shop(xio_str))
    yao_owner.planroot.set_awardlink(awardlink_shop(xio_str, 20, take_force=13))

    # WHEN
    yao_owner.settle_owner()

    # THEN
    xio_groupunit = yao_owner.get_groupunit(xio_str)
    xio_xio_membership = xio_groupunit.get_membership(xio_str)
    sue_acctunit = yao_owner.get_acct(sue_str)
    bob_acctunit = yao_owner.get_acct(bob_str)
    zia_acctunit = yao_owner.get_acct(zia_str)
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


def test_OwnerUnit_settle_owner_CorrectlySetsAcctUnitOwner_fund():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    swim_str = "swim"
    swim_rope = yao_owner.make_l1_rope(swim_str)
    yao_owner.set_l1_plan(planunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_owner.set_acctunit(acctunit_shop(sue_str))
    yao_owner.set_acctunit(acctunit_shop(bob_str))
    yao_owner.set_acctunit(acctunit_shop(zia_str))
    bl_sue = awardlink_shop(sue_str, 20, take_force=40)
    bl_bob = awardlink_shop(bob_str, 10, take_force=5)
    bl_zia = awardlink_shop(zia_str, 10, take_force=5)
    yao_owner.get_plan_obj(swim_rope).set_awardlink(bl_sue)
    yao_owner.get_plan_obj(swim_rope).set_awardlink(bl_bob)
    yao_owner.get_plan_obj(swim_rope).set_awardlink(bl_zia)

    sue_acctunit = yao_owner.get_acct(sue_str)
    bob_acctunit = yao_owner.get_acct(bob_str)
    zia_acctunit = yao_owner.get_acct(zia_str)

    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_owner.settle_owner()

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

    # WHEN another task, check metrics are as expected
    xio_str = "Xio"
    yao_owner.set_acctunit(acctunit_shop(xio_str))
    yao_owner.planroot.set_awardlink(awardlink_shop(xio_str, 20, take_force=10))
    yao_owner.settle_owner()

    # THEN
    xio_acctunit = yao_owner.get_acct(xio_str)

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


def test_OwnerUnit_settle_owner_CorrectlySetsPartGroupedLWAcctUnitOwner_fund():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    swim_str = "swim"
    swim_rope = yao_owner.make_l1_rope(swim_str)
    yao_owner.set_l1_plan(planunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_owner.set_acctunit(acctunit_shop(sue_str))
    yao_owner.set_acctunit(acctunit_shop(bob_str))
    yao_owner.set_acctunit(acctunit_shop(zia_str))
    sue_awardlink = awardlink_shop(sue_str, 20, take_force=40)
    bob_awardlink = awardlink_shop(bob_str, 10, take_force=5)
    zia_awardlink = awardlink_shop(zia_str, 10, take_force=5)
    swim_plan = yao_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(sue_awardlink)
    swim_plan.set_awardlink(bob_awardlink)
    swim_plan.set_awardlink(zia_awardlink)

    # no awardlinks attached to this one
    hunt_str = "hunt"
    yao_owner.set_l1_plan(planunit_shop(hunt_str, mass=3))

    # WHEN
    yao_owner.settle_owner()

    # THEN
    sue_groupunit = yao_owner.get_groupunit(sue_str)
    bob_groupunit = yao_owner.get_groupunit(bob_str)
    zia_groupunit = yao_owner.get_groupunit(zia_str)
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

    sue_acctunit = yao_owner.get_acct(sue_str)
    bob_acctunit = yao_owner.get_acct(bob_str)
    zia_acctunit = yao_owner.get_acct(zia_str)

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


def test_OwnerUnit_settle_owner_CreatesNewGroupUnitAndSetsAcct_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    bob_owner = ownerunit_shop(bob_str)
    swim_str = "swim"
    swim_rope = bob_owner.make_l1_rope(swim_str)
    bob_owner.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    bob_owner.set_acctunit(acctunit_shop(yao_str))
    bob_owner.set_acctunit(acctunit_shop(zia_str))
    # bob_owner.set_acctunit(acctunit_shop(xio_str))
    yao_awardlink = awardlink_shop(yao_str, give_force=20, take_force=6)
    zia_awardlink = awardlink_shop(zia_str, give_force=10, take_force=1)
    xio_awardlink = awardlink_shop(xio_str, give_force=10)
    swim_plan = bob_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(yao_awardlink)
    swim_plan.set_awardlink(zia_awardlink)
    swim_plan.set_awardlink(xio_awardlink)
    assert len(bob_owner.get_acctunit_group_titles_dict()) == 2

    # WHEN
    bob_owner.settle_owner()

    # THEN
    assert len(bob_owner.get_acctunit_group_titles_dict()) != len(bob_owner._groupunits)
    assert not bob_owner.acct_exists(xio_str)
    yao_acctunit = bob_owner.get_acct(yao_str)
    zia_acctunit = bob_owner.get_acct(zia_str)
    acctunit_fund_give_sum = yao_acctunit._fund_give + zia_acctunit._fund_give
    acctunit_fund_take_sum = yao_acctunit._fund_take + zia_acctunit._fund_take
    assert acctunit_fund_give_sum == default_fund_pool()
    assert acctunit_fund_take_sum == default_fund_pool()


def test_OwnerUnit_settle_owner_CorrectlySetsAcctUnit_fund_give_fund_take():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    yao_owner.set_l1_plan(planunit_shop("swim"))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_owner.set_acctunit(acctunit_shop(sue_str, 8))
    yao_owner.set_acctunit(acctunit_shop(bob_str))
    yao_owner.set_acctunit(acctunit_shop(zia_str))
    sue_acctunit = yao_owner.get_acct(sue_str)
    bob_acctunit = yao_owner.get_acct(bob_str)
    zia_acctunit = yao_owner.get_acct(zia_str)
    assert sue_acctunit._fund_give == 0
    assert sue_acctunit._fund_take == 0
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert zia_acctunit._fund_give == 0
    assert zia_acctunit._fund_take == 0

    # WHEN
    yao_owner.settle_owner()

    # THEN
    fund_give_sum = (
        sue_acctunit._fund_give + bob_acctunit._fund_give + zia_acctunit._fund_give
    )
    assert fund_give_sum == 1.0 * default_fund_pool()
    fund_take_sum = (
        sue_acctunit._fund_take + bob_acctunit._fund_take + zia_acctunit._fund_take
    )
    assert fund_take_sum == 1.0 * default_fund_pool()


def clear_all_acctunits_groupunits_fund_agenda_give_take(x_owner: OwnerUnit):
    # delete owner_agenda_debt and owner_agenda_cred
    for groupunit_x in x_owner._groupunits.values():
        groupunit_x.clear_fund_give_take()
        # for membership_x in groupunit_x._accts.values():
        #     print(f"{groupunit_x.} {membership_x.}  {membership_x._fund_give:.6f} {membership_x.acct_debt_points=} {membership__fund_take:t:.6f} {membership_x.} ")

    # delete owner_agenda_debt and owner_agenda_cred
    for x_acctunit in x_owner.accts.values():
        x_acctunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupunit_give: float = 0
    sum_groupunit_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_sums(self, x_owner: OwnerUnit):
        for x_groupunit in x_owner._groupunits.values():
            self.sum_groupunit_give += x_groupunit._fund_agenda_give
            self.sum_groupunit_take += x_groupunit._fund_agenda_take
            for membership_x in x_groupunit._memberships.values():
                self.sum_membership_cred += membership_x._fund_agenda_give
                self.sum_membership_debt += membership_x._fund_agenda_take
                self.membership_count += 1


@dataclass
class AcclabelendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_owner: OwnerUnit):
        for acctunit in x_owner.accts.values():
            self.sum_agenda_cred += acctunit._fund_agenda_give
            self.sum_agenda_debt += acctunit._fund_agenda_take
            self.sum_agenda_ratio_cred += acctunit._fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += acctunit._fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_owner_agenda_share = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_owner_i_sum = 0
    agenda_yes_owner_i_sum = 0

    def set_sums(self, agenda_dict: dict[RopeTerm, PlanUnit]):
        for agenda_plan in agenda_dict.values():
            self.sum_owner_agenda_share += agenda_plan.get_fund_share()
            if agenda_plan._awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_owner_i_sum += agenda_plan.get_fund_share()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_owner_i_sum += agenda_plan.get_fund_share()


def test_OwnerUnit_agenda_cred_debt_IsCorrectlySet():
    # ESTABLISH
    yao_owner = ownerunit_v001_with_large_agenda()
    clear_all_acctunits_groupunits_fund_agenda_give_take(yao_owner)

    # TEST owner_agenda_debt and owner_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_owner)
    assert x_groupagendametrics.sum_groupunit_give == 0
    assert x_groupagendametrics.sum_groupunit_take == 0
    assert x_groupagendametrics.sum_membership_cred == 0
    assert x_groupagendametrics.sum_membership_debt == 0

    # TEST owner_agenda_debt and owner_agenda_cred are empty
    x_acclabelendametrics = AcclabelendaMetrics()
    x_acclabelendametrics.set_sums(yao_owner)
    assert x_acclabelendametrics.sum_agenda_cred == 0
    assert x_acclabelendametrics.sum_agenda_debt == 0
    assert x_acclabelendametrics.sum_agenda_ratio_cred == 0
    assert x_acclabelendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = yao_owner.get_agenda_dict()
    # for plan_rope in yao_owner._plan_dict.keys():
    #     print(f"{plan_rope=}")
    # for x_acct in yao_owner.accts.values():
    #     for x_membership in x_acct._memberships.values():
    #         print(f"{x_membership.group_title=}")

    # THEN
    print(f"{yao_owner.get_reason_rcontexts()=}")
    assert len(agenda_dict) == 63
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_owner_agenda_share=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    predicted_agenda_no_owner_i_sum = int(0.004107582 * default_fund_pool())
    assert x_awardagendametrics.agenda_no_owner_i_sum == predicted_agenda_no_owner_i_sum
    predicted_agenda_yes_owner_i_sum = int(0.003065400 * default_fund_pool())
    assert (
        x_awardagendametrics.agenda_yes_owner_i_sum == predicted_agenda_yes_owner_i_sum
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_owner_i_sum
        + x_awardagendametrics.agenda_yes_owner_i_sum,
        x_awardagendametrics.sum_owner_agenda_share,
    )
    predicted_sum_owner_agenda_share = 0.007172982 * default_fund_pool()
    assert (
        x_awardagendametrics.sum_owner_agenda_share == predicted_sum_owner_agenda_share
    )

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_owner)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 3065400
    print(f"{x_groupagendametrics.sum_groupunit_give=}")
    assert are_equal(x_groupagendametrics.sum_groupunit_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupunit_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_owner_i_sum,
        x_groupagendametrics.sum_groupunit_give,
    )

    assert all_acctunits_have_legitimate_values(yao_owner)

    x_acclabelendametrics = AcclabelendaMetrics()
    x_acclabelendametrics.set_sums(yao_owner)
    assert are_equal(
        x_acclabelendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_owner_agenda_share,
    )
    assert are_equal(
        x_acclabelendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_owner_agenda_share,
    )
    assert are_equal(x_acclabelendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_acclabelendametrics.sum_agenda_ratio_debt, 1)

    # acctunit_fund_give_sum = 0.0
    # acctunit_fund_take_sum = 0.0

    # assert acctunit_fund_give_sum == 1.0
    # assert acctunit_fund_take_sum > 0.9999999
    # assert acctunit_fund_take_sum < 1.00000001


def all_acctunits_have_legitimate_values(x_owner: OwnerUnit):
    return not any(
        (
            acctunit._fund_give is None
            or acctunit._fund_give in [0.25, 0.5]
            or acctunit._fund_take is None
            or acctunit._fund_take in [0.8, 0.1]
        )
        for acctunit in x_owner.accts.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_OwnerUnit_settle_owner_SetsAttrsWhenNoFactUnitsNoReasonUnitsEmpty_agenda_ratio_cred_debt():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    sue_acctunit = acctunit_shop(sue_str, 0.5, acct_debt_points=2)
    bob_acctunit = acctunit_shop(bob_str, 1.5, acct_debt_points=3)
    zia_acctunit = acctunit_shop(zia_str, 8, acct_debt_points=5)
    yao_owner.set_acctunit(sue_acctunit)
    yao_owner.set_acctunit(bob_acctunit)
    yao_owner.set_acctunit(zia_acctunit)
    sue_acct = yao_owner.get_acct(sue_str)
    bob_acct = yao_owner.get_acct(bob_str)
    zia_acct = yao_owner.get_acct(zia_str)

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
    yao_owner.settle_owner()

    # THEN
    assert yao_owner._reason_rcontexts == set()
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


def test_OwnerUnit_settle_owner_CreatesGroupUnitWith_ownerunit_v001():
    # ESTABLISH / WHEN
    yao_owner = ownerunit_v001()
    yao_owner.settle_owner()

    # THEN
    assert yao_owner._groupunits is not None
    assert len(yao_owner._groupunits) == 34
    everyone_accts_len = None
    everyone_group = yao_owner.get_groupunit(";Everyone")
    everyone_accts_len = len(everyone_group._memberships)
    assert everyone_accts_len == 22

    # WHEN
    yao_owner.settle_owner()
    plan_dict = yao_owner._plan_dict

    # THEN
    # print(f"{len(plan_dict)=}")
    db_plan = plan_dict.get(yao_owner.make_l1_rope("D&B"))
    assert len(db_plan.awardlinks) == 3
    # for plan_key in plan_dict:
    #     print(f"{plan_key=}")
    #     if plan.plan_label == "D&B":
    #         print(f"{plan.plan_label=} {plan.awardlinks=}")
    #         db_awardlink_len = len(plan.awardlinks)
    # assert db_awardlink_len == 3
