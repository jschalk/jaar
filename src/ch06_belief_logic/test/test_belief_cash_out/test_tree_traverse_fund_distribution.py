from dataclasses import dataclass
from pytest import raises as pytest_raises
from src.ch01_rope_logic.rope import RopePointer, to_rope
from src.ch02_finance_logic.finance_config import default_fund_pool
from src.ch03_group_logic.group import awardline_shop, awardunit_shop
from src.ch03_group_logic.voice import voiceunit_shop
from src.ch05_plan_logic.plan import PlanUnit, planunit_shop
from src.ch06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch06_belief_logic.test._util.example_beliefs import (
    beliefunit_v001,
    beliefunit_v001_with_large_agenda,
    get_beliefunit_with7amCleanTableReason,
    get_beliefunit_with_4_levels,
)


def test_BeliefUnit_cashout_Sets_planunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_beliefunit = get_beliefunit_with7amCleanTableReason()
    casa_rope = x_beliefunit.make_l1_rope("casa")
    catt_rope = x_beliefunit.make_l1_rope("cat have dinner")
    wk_rope = x_beliefunit.make_l1_rope("sem_jours")
    x_beliefunit.planroot.fund_onset = 13
    x_beliefunit.planroot.fund_cease = 13
    x_beliefunit.get_plan_obj(casa_rope).fund_onset = 13
    x_beliefunit.get_plan_obj(casa_rope).fund_cease = 13
    x_beliefunit.get_plan_obj(catt_rope).fund_onset = 13
    x_beliefunit.get_plan_obj(catt_rope).fund_cease = 13
    x_beliefunit.get_plan_obj(wk_rope).fund_onset = 13
    x_beliefunit.get_plan_obj(wk_rope).fund_cease = 13

    assert x_beliefunit.planroot.fund_onset == 13
    assert x_beliefunit.planroot.fund_cease == 13
    assert x_beliefunit.get_plan_obj(casa_rope).fund_onset == 13
    assert x_beliefunit.get_plan_obj(casa_rope).fund_cease == 13
    assert x_beliefunit.get_plan_obj(catt_rope).fund_onset == 13
    assert x_beliefunit.get_plan_obj(catt_rope).fund_cease == 13
    assert x_beliefunit.get_plan_obj(wk_rope).fund_onset == 13
    assert x_beliefunit.get_plan_obj(wk_rope).fund_cease == 13

    # WHEN
    x_beliefunit.cashout()

    # THEN
    assert x_beliefunit.planroot.fund_onset != 13
    assert x_beliefunit.planroot.fund_cease != 13
    assert x_beliefunit.get_plan_obj(casa_rope).fund_onset != 13
    assert x_beliefunit.get_plan_obj(casa_rope).fund_cease != 13
    assert x_beliefunit.get_plan_obj(catt_rope).fund_onset != 13
    assert x_beliefunit.get_plan_obj(catt_rope).fund_cease != 13
    assert x_beliefunit.get_plan_obj(wk_rope).fund_onset != 13
    assert x_beliefunit.get_plan_obj(wk_rope).fund_cease != 13


def test_BeliefUnit_cashout_Sets_planunit_fund_onset_fund_cease_Scenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_beliefunit = beliefunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_beliefunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, star=10)
    yao_beliefunit.set_l1_plan(auto_plan)

    carn_str = "carn"
    carn_rope = yao_beliefunit.make_l1_rope(carn_str)
    carn_plan = planunit_shop(carn_str, star=60)
    yao_beliefunit.set_l1_plan(carn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_beliefunit.make_rope(carn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, star=1)
    yao_beliefunit.set_plan(lamb_plan, parent_rope=carn_rope)
    duck_str = "ducks"
    duck_rope = yao_beliefunit.make_rope(carn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, star=2)
    yao_beliefunit.set_plan(duck_plan, parent_rope=carn_rope)

    coal_str = "coal"
    coal_rope = yao_beliefunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, star=30)
    yao_beliefunit.set_l1_plan(coal_plan)

    assert yao_beliefunit.planroot.fund_onset is None
    assert yao_beliefunit.planroot.fund_cease is None
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_cease is None
    assert yao_beliefunit.get_plan_obj(carn_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(carn_rope).fund_cease is None
    assert yao_beliefunit.get_plan_obj(coal_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(coal_rope).fund_cease is None
    lamb_before = yao_beliefunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_beliefunit.get_plan_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_beliefunit.cashout()

    # THEN
    assert yao_beliefunit.planroot.fund_onset == 0.0
    assert yao_beliefunit.planroot.fund_cease == default_fund_pool()
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_onset == 0.0
    assert (
        yao_beliefunit.get_plan_obj(auto_rope).fund_cease == default_fund_pool() * 0.1
    )
    assert (
        yao_beliefunit.get_plan_obj(carn_rope).fund_onset == default_fund_pool() * 0.1
    )
    assert (
        yao_beliefunit.get_plan_obj(carn_rope).fund_cease == default_fund_pool() * 0.7
    )
    assert (
        yao_beliefunit.get_plan_obj(coal_rope).fund_onset == default_fund_pool() * 0.7
    )
    assert (
        yao_beliefunit.get_plan_obj(coal_rope).fund_cease == default_fund_pool() * 1.0
    )

    duck_after = yao_beliefunit.get_plan_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_fund_pool() * 0.1
    assert duck_after.fund_cease == default_fund_pool() * 0.5
    lamb_after = yao_beliefunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_fund_pool() * 0.5
    assert lamb_after.fund_cease == default_fund_pool() * 0.7


def test_BeliefUnit_cashout_Sets_planunit_fund_onset_fund_cease_Scenario2_DifferentOrderOfPlans():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_beliefunit = beliefunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_beliefunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, star=10)
    yao_beliefunit.set_l1_plan(auto_plan)

    yarn_str = "yarn"
    yarn_rope = yao_beliefunit.make_l1_rope(yarn_str)
    yarn_plan = planunit_shop(yarn_str, star=60)
    yao_beliefunit.set_l1_plan(yarn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_beliefunit.make_rope(yarn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, star=1)
    yao_beliefunit.set_plan(lamb_plan, parent_rope=yarn_rope)
    duck_str = "ducks"
    duck_rope = yao_beliefunit.make_rope(yarn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, star=2)
    yao_beliefunit.set_plan(duck_plan, parent_rope=yarn_rope)

    coal_str = "coal"
    coal_rope = yao_beliefunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, star=30)
    yao_beliefunit.set_l1_plan(coal_plan)

    assert yao_beliefunit.planroot.fund_onset is None
    assert yao_beliefunit.planroot.fund_cease is None
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_cease is None
    assert yao_beliefunit.get_plan_obj(yarn_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(yarn_rope).fund_cease is None
    assert yao_beliefunit.get_plan_obj(coal_rope).fund_onset is None
    assert yao_beliefunit.get_plan_obj(coal_rope).fund_cease is None
    lamb_before = yao_beliefunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_beliefunit.get_plan_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_beliefunit.cashout()

    # THEN
    assert yao_beliefunit.planroot.fund_onset == 0.0
    assert yao_beliefunit.planroot.fund_cease == default_fund_pool()
    assert yao_beliefunit.get_plan_obj(auto_rope).fund_onset == 0.0
    assert (
        yao_beliefunit.get_plan_obj(auto_rope).fund_cease == default_fund_pool() * 0.1
    )
    assert (
        yao_beliefunit.get_plan_obj(coal_rope).fund_onset == default_fund_pool() * 0.1
    )
    assert (
        yao_beliefunit.get_plan_obj(coal_rope).fund_cease == default_fund_pool() * 0.4
    )
    assert (
        yao_beliefunit.get_plan_obj(yarn_rope).fund_onset == default_fund_pool() * 0.4
    )
    assert (
        yao_beliefunit.get_plan_obj(yarn_rope).fund_cease == default_fund_pool() * 1.0
    )

    duck_after = yao_beliefunit.get_plan_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_fund_pool() * 0.4
    assert duck_after.fund_cease == default_fund_pool() * 0.8
    lamb_after = yao_beliefunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_fund_pool() * 0.8
    assert lamb_after.fund_cease == default_fund_pool() * 1.0


def test_BeliefUnit_cashout_Sets_fund_ratio_WithSomePlansOfZero_starScenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_belief.set_plan(floor_plan, casa_rope)
    sue_belief.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_belief.make_rope(casa_rope, status_str)
    sue_belief.set_plan(planunit_shop(status_str, star=0), casa_rope)

    non_str = "not clean"
    yes_str = "yes clean"
    non_rope = sue_belief.make_rope(status_rope, non_str)
    yes_rope = sue_belief.make_rope(status_rope, yes_str)
    sue_belief.set_plan(planunit_shop(non_str), status_rope)
    sue_belief.set_plan(planunit_shop(yes_str, star=2), status_rope)

    assert sue_belief.planroot.fund_ratio is None
    assert sue_belief.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(floor_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(status_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(non_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(yes_rope).fund_ratio is None

    # WHEN
    sue_belief.cashout()

    # THEN
    print(f"{sue_belief.fund_pool=}")
    assert sue_belief.planroot.fund_ratio == 1
    assert sue_belief.get_plan_obj(casa_rope).fund_ratio == 0.5
    assert sue_belief.get_plan_obj(floor_rope).fund_ratio == 0.5
    assert sue_belief.get_plan_obj(status_rope).fund_ratio == 0.0
    assert sue_belief.get_plan_obj(non_rope).fund_ratio == 0.0
    assert sue_belief.get_plan_obj(yes_rope).fund_ratio == 0.0


def test_BeliefUnit_cashout_Sets_fund_ratio_WithSomePlansOfZero_starScenario1():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    floor_str = "mop floor"
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, task=True)
    sue_belief.set_plan(floor_plan, casa_rope)
    sue_belief.set_l1_plan(planunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_rope = sue_belief.make_rope(casa_rope, status_str)
    sue_belief.set_plan(planunit_shop(status_str), casa_rope)

    status_plan = sue_belief.get_plan_obj(status_rope)
    print(f"{status_plan.star=}")
    print("This should raise error: 'Planunit._'")

    clean_str = "clean"
    clean_rope = sue_belief.make_rope(status_rope, clean_str)
    very_str = "very_much"
    mod_str = "moderately"
    dirty_str = "dirty"

    sue_belief.set_plan(planunit_shop(clean_str, star=0), status_rope)
    sue_belief.set_plan(planunit_shop(very_str), clean_rope)
    sue_belief.set_plan(planunit_shop(mod_str, star=2), clean_rope)
    sue_belief.set_plan(planunit_shop(dirty_str), clean_rope)

    very_rope = sue_belief.make_rope(clean_rope, very_str)
    mod_rope = sue_belief.make_rope(clean_rope, mod_str)
    dirty_rope = sue_belief.make_rope(clean_rope, dirty_str)
    assert sue_belief.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(floor_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(status_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(clean_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(very_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(mod_rope).fund_ratio is None
    assert sue_belief.get_plan_obj(dirty_rope).fund_ratio is None

    # WHEN
    sue_belief.cashout()

    # THEN
    print(f"{sue_belief.fund_pool=}")
    assert sue_belief.get_plan_obj(casa_rope).fund_ratio == 0.5
    assert sue_belief.get_plan_obj(floor_rope).fund_ratio == 0.25
    assert sue_belief.get_plan_obj(status_rope).fund_ratio == 0.25
    assert sue_belief.get_plan_obj(clean_rope).fund_ratio == 0
    assert sue_belief.get_plan_obj(very_rope).fund_ratio == 0
    assert sue_belief.get_plan_obj(mod_rope).fund_ratio == 0
    assert sue_belief.get_plan_obj(dirty_rope).fund_ratio == 0


def test_BeliefUnit_cashout_WhenPlanUnitHasFundsBut_kidsHaveNostarDistributeFundsToVoiceUnits_scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    yao_str = "Yao"
    sue_beliefunit.add_voiceunit(yao_str)
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_plan = planunit_shop(casa_str, star=1)

    swim_str = "swimming"
    swim_rope = sue_beliefunit.make_rope(casa_rope, swim_str)
    swim_plan = planunit_shop(swim_str, star=8)

    clean_str = "cleaning"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    clean_plan = planunit_shop(clean_str, star=2)
    sue_beliefunit.set_plan(planunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_beliefunit.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, star=0)
    vacuum_str = "vacuum"
    vacuum_rope = sue_beliefunit.make_rope(clean_rope, vacuum_str)
    vacuum_plan = planunit_shop(vacuum_str, star=0)

    sue_beliefunit.set_l1_plan(casa_plan)
    sue_beliefunit.set_plan(swim_plan, casa_rope)
    sue_beliefunit.set_plan(clean_plan, casa_rope)
    sue_beliefunit.set_plan(sweep_plan, clean_rope)  # _star=0
    sue_beliefunit.set_plan(vacuum_plan, clean_rope)  # _star=0

    assert sue_beliefunit.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_beliefunit.get_plan_obj(swim_rope).fund_ratio is None
    assert sue_beliefunit.get_plan_obj(clean_rope).fund_ratio is None
    assert sue_beliefunit.get_plan_obj(sweep_rope).fund_ratio is None
    assert sue_beliefunit.get_plan_obj(vacuum_rope).fund_ratio is None
    assert sue_beliefunit.get_groupunit(yao_str) is None

    assert not sue_beliefunit.offtrack_fund
    assert sue_beliefunit.get_voice(yao_str).fund_give == 0
    assert sue_beliefunit.get_voice(yao_str).fund_take == 0

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    print(f"{sue_beliefunit.fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_beliefunit.get_plan_obj(casa_rope).fund_ratio == 1
    assert sue_beliefunit.get_plan_obj(swim_rope).fund_ratio == 0.8
    assert sue_beliefunit.get_plan_obj(clean_rope).fund_ratio == clean_fund_ratio
    assert sue_beliefunit.get_plan_obj(sweep_rope).fund_ratio == 0
    assert sue_beliefunit.get_plan_obj(vacuum_rope).fund_ratio == 0
    assert sue_beliefunit.get_groupunit(yao_str).fund_give == 0
    assert sue_beliefunit.get_groupunit(yao_str).fund_take == 0

    assert sue_beliefunit.offtrack_fund == clean_fund_ratio * default_fund_pool()
    assert sue_beliefunit.get_voice(yao_str).fund_give == default_fund_pool()
    assert sue_beliefunit.get_voice(yao_str).fund_take == default_fund_pool()


def test_BeliefUnit_cashout_TreeTraverseSetsAwardLine_fundFromRoot():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.cashout()
    # plan tree has no awardunits
    assert sue_belief.planroot.awardlines == {}
    sue_str = "Sue"
    wk_str = "sem_jours"
    nation_str = "nation"
    sue_awardunit = awardunit_shop(awardee_title=sue_str)
    sue_belief.add_voiceunit(voice_name=sue_str)
    sue_belief.planroot.set_awardunit(awardunit=sue_awardunit)
    # plan tree has awardlines
    assert sue_belief.planroot.awardheirs.get(sue_str) is None

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.planroot.awardheirs.get(sue_str) is not None
    assert sue_belief.planroot.awardheirs.get(sue_str).awardee_title == sue_str
    assert sue_belief.planroot.awardlines != {}
    root_rope = to_rope(sue_belief.planroot.plan_label)
    root_plan = sue_belief.get_plan_obj(rope=root_rope)
    sue_awardline = sue_belief.planroot.awardlines.get(sue_str)
    print(f"{sue_awardline.fund_give=} {root_plan.fund_ratio=} ")
    print(f"  {sue_awardline.fund_take=} {root_plan.fund_ratio=} ")
    sum_x = 0
    cat_rope = sue_belief.make_l1_rope("cat have dinner")
    cat_plan = sue_belief.get_plan_obj(cat_rope)
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wk_plan = sue_belief.get_plan_obj(wk_rope)
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    nation_rope = sue_belief.make_l1_rope(nation_str)
    nation_plan = sue_belief.get_plan_obj(nation_rope)
    sum_x = cat_plan.fund_ratio
    print(f"{cat_plan.fund_ratio=} {sum_x} ")
    sum_x += wk_plan.fund_ratio
    print(f"{wk_plan.fund_ratio=} {sum_x} ")
    sum_x += casa_plan.fund_ratio
    print(f"{casa_plan.fund_ratio=} {sum_x} ")
    sum_x += nation_plan.fund_ratio
    print(f"{nation_plan.fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_plan in root_plan.kids.values():
    #     sum_x += kid_plan.fund_ratio
    #     print(f"  {kid_plan.fund_ratio=} {sum_x=} {kid_plan.get_plan_rope()=}")
    assert round(sue_awardline.fund_give, 15) == default_fund_pool()
    assert round(sue_awardline.fund_take, 15) == default_fund_pool()
    x_awardline = awardline_shop(sue_str, default_fund_pool(), default_fund_pool())
    assert sue_belief.planroot.awardlines == {x_awardline.awardee_title: x_awardline}


def test_BeliefUnit_cashout_TreeTraverseSets_awardlines_ToRootPlanUnitFromNon_RootPlanUnit():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.cashout()
    sue_str = "Sue"
    sue_belief.add_voiceunit(sue_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    sue_belief.get_plan_obj(casa_rope).set_awardunit(
        awardunit_shop(awardee_title=sue_str)
    )
    assert sue_belief.planroot.awardlines == {}

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.planroot.awardlines != {}
    print(f"{sue_belief.planroot.awardlines=}")
    x_awardline = awardline_shop(
        awardee_title=sue_str,
        fund_give=0.230769231 * default_fund_pool(),
        fund_take=0.230769231 * default_fund_pool(),
    )
    assert sue_belief.planroot.awardlines == {x_awardline.awardee_title: x_awardline}
    casa_planunit = sue_belief.get_plan_obj(casa_rope)
    assert casa_planunit.awardlines != {}
    assert casa_planunit.awardlines == {x_awardline.awardee_title: x_awardline}


def test_BeliefUnit_cashout_WithRootLevelAwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    sue_belief.set_voiceunit(voiceunit_shop(yao_str))
    sue_belief.set_voiceunit(voiceunit_shop(zia_str))
    sue_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(xio_str, give_force=10)
    root_rope = to_rope(sue_belief.planroot.plan_label)
    x_planroot = sue_belief.get_plan_obj(root_rope)
    x_planroot.set_awardunit(awardunit=yao_awardunit)
    x_planroot.set_awardunit(awardunit=zia_awardunit)
    x_planroot.set_awardunit(awardunit=xio_awardunit)
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 3

    # WHEN
    sue_belief.cashout()

    # THEN
    yao_groupunit = sue_belief.get_groupunit(yao_str)
    zia_groupunit = sue_belief.get_groupunit(zia_str)
    xio_groupunit = sue_belief.get_groupunit(xio_str)
    assert yao_groupunit.fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit.fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit.fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit.fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit.fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit.fund_take == 0.125 * default_fund_pool()
    cred_sum1 = yao_groupunit.fund_give
    cred_sum1 += zia_groupunit.fund_give + xio_groupunit.fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupunit.fund_take
    debt_sum1 += zia_groupunit.fund_take + xio_groupunit.fund_take
    assert debt_sum1 == 1 * default_fund_pool()

    # ESTABLISH
    sue_belief.set_voiceunit(voiceunit_shop(sue_str))
    sue_awardunit = awardunit_shop(sue_str, give_force=37)
    x_planroot.set_awardunit(sue_awardunit)
    assert len(x_planroot.awardunits) == 4
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 4

    # WHEN
    sue_belief.cashout()

    # THEN
    yao_groupunit = sue_belief.get_groupunit(yao_str)
    zia_groupunit = sue_belief.get_groupunit(zia_str)
    xio_groupunit = sue_belief.get_groupunit(xio_str)
    sue_groupunit = sue_belief.get_groupunit(sue_str)
    assert yao_groupunit.fund_give != 0.5 * default_fund_pool()
    assert yao_groupunit.fund_take != 0.75 * default_fund_pool()
    assert zia_groupunit.fund_give != 0.25 * default_fund_pool()
    assert zia_groupunit.fund_take != 0.125 * default_fund_pool()
    assert xio_groupunit.fund_give != 0.25 * default_fund_pool()
    assert xio_groupunit.fund_take != 0.125 * default_fund_pool()
    assert sue_groupunit.fund_give is not None
    assert sue_groupunit.fund_take is not None
    cred_sum1 = yao_groupunit.fund_give + zia_groupunit.fund_give
    cred_sum1 += xio_groupunit.fund_give + sue_groupunit.fund_give
    assert cred_sum1 == 1 * default_fund_pool()
    debt_sum1 = yao_groupunit.fund_take + zia_groupunit.fund_take
    debt_sum1 += xio_groupunit.fund_take + sue_groupunit.fund_take
    assert round(debt_sum1) == 1 * default_fund_pool()


def test_BeliefUnit_cashout_WithLevel3AwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    x_belief = beliefunit_shop(bob_str)
    swim_str = "swim"
    swim_rope = x_belief.make_l1_rope(swim_str)
    x_belief.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_belief.set_voiceunit(voiceunit_shop(yao_str))
    x_belief.set_voiceunit(voiceunit_shop(zia_str))
    x_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(xio_str, give_force=10)
    swim_plan = x_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(yao_awardunit)
    swim_plan.set_awardunit(zia_awardunit)
    swim_plan.set_awardunit(xio_awardunit)
    assert len(x_belief.get_voiceunit_group_titles_dict()) == 3

    # WHEN
    x_belief.cashout()

    # THEN
    yao_groupunit = x_belief.get_groupunit(yao_str)
    zia_groupunit = x_belief.get_groupunit(zia_str)
    xio_groupunit = x_belief.get_groupunit(xio_str)
    assert yao_groupunit.fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit.fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit.fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit.fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit.fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit.fund_take == 0.125 * default_fund_pool()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_fund_pool()
    assert groupunit_fund_take_sum == 1 * default_fund_pool()


def test_BeliefUnit_cashout_CreatesNewGroupUnitAndSetsGroup_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_belief = beliefunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = x_belief.make_l1_rope(swim_str)
    x_belief.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_belief.set_voiceunit(voiceunit_shop(yao_str))
    x_belief.set_voiceunit(voiceunit_shop(zia_str))
    # x_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(xio_str, give_force=10)
    swim_plan = x_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(yao_awardunit)
    swim_plan.set_awardunit(zia_awardunit)
    swim_plan.set_awardunit(xio_awardunit)
    assert len(x_belief.get_voiceunit_group_titles_dict()) == 2

    # WHEN
    x_belief.cashout()

    # THEN
    yao_groupunit = x_belief.get_groupunit(yao_str)
    zia_groupunit = x_belief.get_groupunit(zia_str)
    xio_groupunit = x_belief.get_groupunit(xio_str)
    assert len(x_belief.get_voiceunit_group_titles_dict()) != len(x_belief.groupunits)
    assert yao_groupunit.fund_give == 0.5 * default_fund_pool()
    assert yao_groupunit.fund_take == 0.75 * default_fund_pool()
    assert zia_groupunit.fund_give == 0.25 * default_fund_pool()
    assert zia_groupunit.fund_take == 0.125 * default_fund_pool()
    assert xio_groupunit.fund_give == 0.25 * default_fund_pool()
    assert xio_groupunit.fund_take == 0.125 * default_fund_pool()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_fund_pool()
    assert groupunit_fund_take_sum == 1 * default_fund_pool()


def test_BeliefUnit_cashout_WithLevel3AwardUnitAndEmptyAncestorsSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    yao_str = "Yao"
    x_belief = beliefunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = x_belief.make_l1_rope(swim_str)
    x_belief.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    x_belief.set_voiceunit(voiceunit_shop(yao_str))
    x_belief.set_voiceunit(voiceunit_shop(zia_str))
    x_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(xio_str, give_force=10)
    swim_plan = x_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(yao_awardunit)
    swim_plan.set_awardunit(zia_awardunit)
    swim_plan.set_awardunit(xio_awardunit)

    # no awardunits attached to this one
    x_belief.set_l1_plan(planunit_shop("hunt", star=3))

    # WHEN
    x_belief.cashout()

    # THEN
    x_planroot = x_belief.get_plan_obj(to_rope(x_belief.moment_label))
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[yao_str]
    assert str(excinfo.value) == f"'{yao_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[zia_str]
    assert str(excinfo.value) == f"'{zia_str}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[xio_str]
    assert str(excinfo.value) == f"'{xio_str}'"

    # THEN
    yao_groupunit = x_belief.get_groupunit(yao_str)
    zia_groupunit = x_belief.get_groupunit(zia_str)
    xio_groupunit = x_belief.get_groupunit(xio_str)
    assert yao_groupunit.fund_give == 0.125 * default_fund_pool()
    assert yao_groupunit.fund_take == 0.1875 * default_fund_pool()
    assert zia_groupunit.fund_give == 0.0625 * default_fund_pool()
    assert zia_groupunit.fund_take == 0.03125 * default_fund_pool()
    assert xio_groupunit.fund_give == 0.0625 * default_fund_pool()
    assert xio_groupunit.fund_take == 0.03125 * default_fund_pool()
    assert (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
        == 0.25 * default_fund_pool()
    )


def test_BeliefUnit_set_awardunit_CalculatesInheritedAwardUnitBeliefFund():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_belief.set_voiceunit(voiceunit_shop(yao_str))
    sue_belief.set_voiceunit(voiceunit_shop(zia_str))
    sue_belief.set_voiceunit(voiceunit_shop(Xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    Xio_awardunit = awardunit_shop(Xio_str, give_force=10)
    sue_belief.planroot.set_awardunit(yao_awardunit)
    sue_belief.planroot.set_awardunit(zia_awardunit)
    sue_belief.planroot.set_awardunit(Xio_awardunit)
    assert len(sue_belief.planroot.awardunits) == 3

    # WHEN
    plan_dict = sue_belief.get_plan_dict()

    # THEN
    print(f"{plan_dict.keys()=}")
    plan_bob = plan_dict.get(to_rope(sue_belief.moment_label))
    assert len(plan_bob.awardheirs) == 3

    bheir_yao = plan_bob.awardheirs.get(yao_str)
    bheir_zia = plan_bob.awardheirs.get(zia_str)
    bheir_Xio = plan_bob.awardheirs.get(Xio_str)
    assert bheir_yao.fund_give == 0.5 * default_fund_pool()
    assert bheir_yao.fund_take == 0.75 * default_fund_pool()
    assert bheir_zia.fund_give == 0.25 * default_fund_pool()
    assert bheir_zia.fund_take == 0.125 * default_fund_pool()
    assert bheir_Xio.fund_give == 0.25 * default_fund_pool()
    assert bheir_Xio.fund_take == 0.125 * default_fund_pool()
    assert (
        bheir_yao.fund_give + bheir_zia.fund_give + bheir_Xio.fund_give
        == 1 * default_fund_pool()
    )
    assert (
        bheir_yao.fund_take + bheir_zia.fund_take + bheir_Xio.fund_take
        == 1 * default_fund_pool()
    )

    # fund_give_sum = 0
    # fund_take_sum = 0
    # for group in x_belief.planroot.awardheirs.values():
    #     print(f"{group=}")
    #     assert group.fund_give is not None
    #     assert group.fund_give in [0.25, 0.5]
    #     assert group.fund_take is not None
    #     assert group.fund_take in [0.75, 0.125]
    #     fund_give_sum += group.fund_give
    #     fund_take_sum += group.fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_BeliefUnit_cashout_SetsGroupLinkBeliefCredAndDebt():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_belief.set_voiceunit(voiceunit_shop(sue_str))
    yao_belief.set_voiceunit(voiceunit_shop(bob_str))
    yao_belief.set_voiceunit(voiceunit_shop(zia_str))
    sue_awardunit = awardunit_shop(sue_str, 20, take_force=40)
    bob_awardunit = awardunit_shop(bob_str, 10, take_force=5)
    zia_awardunit = awardunit_shop(zia_str, 10, take_force=5)
    root_rope = to_rope(yao_belief.moment_label)
    yao_belief.edit_plan_attr(root_rope, awardunit=sue_awardunit)
    yao_belief.edit_plan_attr(root_rope, awardunit=bob_awardunit)
    yao_belief.edit_plan_attr(root_rope, awardunit=zia_awardunit)

    sue_voiceunit = yao_belief.get_voice(sue_str)
    bob_voiceunit = yao_belief.get_voice(bob_str)
    zia_voiceunit = yao_belief.get_voice(zia_str)
    sue_sue_membership = sue_voiceunit.get_membership(sue_str)
    bob_bob_membership = bob_voiceunit.get_membership(bob_str)
    zia_zia_membership = zia_voiceunit.get_membership(zia_str)
    assert sue_sue_membership.fund_give is None
    assert sue_sue_membership.fund_take is None
    assert bob_bob_membership.fund_give is None
    assert bob_bob_membership.fund_take is None
    assert zia_zia_membership.fund_give is None
    assert zia_zia_membership.fund_take is None

    # WHEN
    yao_belief.cashout()

    # THEN
    assert sue_sue_membership.fund_give == 0.5 * default_fund_pool()
    assert sue_sue_membership.fund_take == 0.8 * default_fund_pool()
    assert bob_bob_membership.fund_give == 0.25 * default_fund_pool()
    assert bob_bob_membership.fund_take == 0.1 * default_fund_pool()
    assert zia_zia_membership.fund_give == 0.25 * default_fund_pool()
    assert zia_zia_membership.fund_take == 0.1 * default_fund_pool()

    membership_cred_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
    )
    assert membership_cred_sum == 1.0 * default_fund_pool()
    membership_debt_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
    )
    assert membership_debt_sum == 1.0 * default_fund_pool()

    # ESTABLISH another task, check metrics are as expected
    xio_str = "Xio"
    yao_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_belief.planroot.set_awardunit(awardunit_shop(xio_str, 20, take_force=13))

    # WHEN
    yao_belief.cashout()

    # THEN
    xio_groupunit = yao_belief.get_groupunit(xio_str)
    xio_xio_membership = xio_groupunit.get_membership(xio_str)
    sue_voiceunit = yao_belief.get_voice(sue_str)
    bob_voiceunit = yao_belief.get_voice(bob_str)
    zia_voiceunit = yao_belief.get_voice(zia_str)
    sue_sue_membership = sue_voiceunit.get_membership(sue_str)
    bob_bob_membership = bob_voiceunit.get_membership(bob_str)
    zia_zia_membership = zia_voiceunit.get_membership(zia_str)
    assert sue_sue_membership.fund_give != 0.25 * default_fund_pool()
    assert sue_sue_membership.fund_take != 0.8 * default_fund_pool()
    assert bob_bob_membership.fund_give != 0.25 * default_fund_pool()
    assert bob_bob_membership.fund_take != 0.1 * default_fund_pool()
    assert zia_zia_membership.fund_give != 0.5 * default_fund_pool()
    assert zia_zia_membership.fund_take != 0.1 * default_fund_pool()
    assert xio_xio_membership.fund_give is not None
    assert xio_xio_membership.fund_take is not None

    x_fund_give_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
        + xio_xio_membership.fund_give
    )
    print(f"{x_fund_give_sum=}")
    assert x_fund_give_sum == 1.0 * default_fund_pool()
    x_fund_take_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
        + xio_xio_membership.fund_take
    )
    assert x_fund_take_sum == 1.0 * default_fund_pool()


def test_BeliefUnit_cashout_SetsVoiceUnitBelief_fund():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)
    yao_belief.set_l1_plan(planunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_belief.set_voiceunit(voiceunit_shop(sue_str))
    yao_belief.set_voiceunit(voiceunit_shop(bob_str))
    yao_belief.set_voiceunit(voiceunit_shop(zia_str))
    bl_sue = awardunit_shop(sue_str, 20, take_force=40)
    bl_bob = awardunit_shop(bob_str, 10, take_force=5)
    bl_zia = awardunit_shop(zia_str, 10, take_force=5)
    yao_belief.get_plan_obj(swim_rope).set_awardunit(bl_sue)
    yao_belief.get_plan_obj(swim_rope).set_awardunit(bl_bob)
    yao_belief.get_plan_obj(swim_rope).set_awardunit(bl_zia)

    sue_voiceunit = yao_belief.get_voice(sue_str)
    bob_voiceunit = yao_belief.get_voice(bob_str)
    zia_voiceunit = yao_belief.get_voice(zia_str)

    assert sue_voiceunit.fund_give == 0
    assert sue_voiceunit.fund_take == 0
    assert bob_voiceunit.fund_give == 0
    assert bob_voiceunit.fund_take == 0
    assert zia_voiceunit.fund_give == 0
    assert zia_voiceunit.fund_take == 0

    # WHEN
    yao_belief.cashout()

    # THEN
    assert sue_voiceunit.fund_give == 0.5 * default_fund_pool()
    assert sue_voiceunit.fund_take == 0.8 * default_fund_pool()
    assert bob_voiceunit.fund_give == 0.25 * default_fund_pool()
    assert bob_voiceunit.fund_take == 0.1 * default_fund_pool()
    assert zia_voiceunit.fund_give == 0.25 * default_fund_pool()
    assert zia_voiceunit.fund_take == 0.1 * default_fund_pool()

    assert (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        == 1.0 * default_fund_pool()
    )

    # WHEN another task, check metrics are as expected
    xio_str = "Xio"
    yao_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_belief.planroot.set_awardunit(awardunit_shop(xio_str, 20, take_force=10))
    yao_belief.cashout()

    # THEN
    xio_voiceunit = yao_belief.get_voice(xio_str)

    assert sue_voiceunit.fund_give != 0.5 * default_fund_pool()
    assert sue_voiceunit.fund_take != 0.8 * default_fund_pool()
    assert bob_voiceunit.fund_give != 0.25 * default_fund_pool()
    assert bob_voiceunit.fund_take != 0.1 * default_fund_pool()
    assert zia_voiceunit.fund_give != 0.25 * default_fund_pool()
    assert zia_voiceunit.fund_take != 0.1 * default_fund_pool()
    assert xio_voiceunit.fund_give is not None
    assert xio_voiceunit.fund_take is not None

    sum_voiceunit_fund_give = (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
    )
    assert sum_voiceunit_fund_give < 1.0 * default_fund_pool()
    assert (
        sue_voiceunit.fund_give
        + bob_voiceunit.fund_give
        + zia_voiceunit.fund_give
        + xio_voiceunit.fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        < 1.0 * default_fund_pool()
    )
    assert (
        sue_voiceunit.fund_take
        + bob_voiceunit.fund_take
        + zia_voiceunit.fund_take
        + xio_voiceunit.fund_take
        == 1.0 * default_fund_pool()
    )


def test_BeliefUnit_cashout_SetsPartGroupedLWVoiceUnitBelief_fund():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)
    yao_belief.set_l1_plan(planunit_shop(swim_str))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_belief.set_voiceunit(voiceunit_shop(sue_str))
    yao_belief.set_voiceunit(voiceunit_shop(bob_str))
    yao_belief.set_voiceunit(voiceunit_shop(zia_str))
    sue_awardunit = awardunit_shop(sue_str, 20, take_force=40)
    bob_awardunit = awardunit_shop(bob_str, 10, take_force=5)
    zia_awardunit = awardunit_shop(zia_str, 10, take_force=5)
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(sue_awardunit)
    swim_plan.set_awardunit(bob_awardunit)
    swim_plan.set_awardunit(zia_awardunit)

    # no awardunits attached to this one
    hunt_str = "hunt"
    yao_belief.set_l1_plan(planunit_shop(hunt_str, star=3))

    # WHEN
    yao_belief.cashout()

    # THEN
    sue_groupunit = yao_belief.get_groupunit(sue_str)
    bob_groupunit = yao_belief.get_groupunit(bob_str)
    zia_groupunit = yao_belief.get_groupunit(zia_str)
    assert sue_groupunit.fund_give != 0.5 * default_fund_pool()
    assert sue_groupunit.fund_take != 0.8 * default_fund_pool()
    assert bob_groupunit.fund_give != 0.25 * default_fund_pool()
    assert bob_groupunit.fund_take != 0.1 * default_fund_pool()
    assert zia_groupunit.fund_give != 0.25 * default_fund_pool()
    assert zia_groupunit.fund_take != 0.1 * default_fund_pool()
    assert (
        sue_groupunit.fund_give + bob_groupunit.fund_give + zia_groupunit.fund_give
        == 0.25 * default_fund_pool()
    )
    assert (
        sue_groupunit.fund_take + bob_groupunit.fund_take + zia_groupunit.fund_take
        == 0.25 * default_fund_pool()
    )

    sue_voiceunit = yao_belief.get_voice(sue_str)
    bob_voiceunit = yao_belief.get_voice(bob_str)
    zia_voiceunit = yao_belief.get_voice(zia_str)

    assert sue_voiceunit.fund_give == 0.375 * default_fund_pool()
    assert sue_voiceunit.fund_take == 0.45 * default_fund_pool()
    assert bob_voiceunit.fund_give == 0.3125 * default_fund_pool()
    assert bob_voiceunit.fund_take == 0.275 * default_fund_pool()
    assert zia_voiceunit.fund_give == 0.3125 * default_fund_pool()
    assert zia_voiceunit.fund_take == 0.275 * default_fund_pool()

    assert (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
        == 1.0 * default_fund_pool()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        == 1.0 * default_fund_pool()
    )


def test_BeliefUnit_cashout_CreatesNewGroupUnitAndSetsVoice_fund_give_fund_take():
    # ESTABLISH
    bob_str = "Bob"
    bob_belief = beliefunit_shop(bob_str)
    swim_str = "swim"
    swim_rope = bob_belief.make_l1_rope(swim_str)
    bob_belief.set_l1_plan(planunit_shop(swim_str))

    yao_str = "Yao"
    zia_str = "Zia"
    xio_str = "Xio"
    bob_belief.set_voiceunit(voiceunit_shop(yao_str))
    bob_belief.set_voiceunit(voiceunit_shop(zia_str))
    # bob_belief.set_voiceunit(voiceunit_shop(xio_str))
    yao_awardunit = awardunit_shop(yao_str, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(zia_str, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(xio_str, give_force=10)
    swim_plan = bob_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(yao_awardunit)
    swim_plan.set_awardunit(zia_awardunit)
    swim_plan.set_awardunit(xio_awardunit)
    assert len(bob_belief.get_voiceunit_group_titles_dict()) == 2

    # WHEN
    bob_belief.cashout()

    # THEN
    assert len(bob_belief.get_voiceunit_group_titles_dict()) != len(
        bob_belief.groupunits
    )
    assert not bob_belief.voice_exists(xio_str)
    yao_voiceunit = bob_belief.get_voice(yao_str)
    zia_voiceunit = bob_belief.get_voice(zia_str)
    voiceunit_fund_give_sum = yao_voiceunit.fund_give + zia_voiceunit.fund_give
    voiceunit_fund_take_sum = yao_voiceunit.fund_take + zia_voiceunit.fund_take
    assert voiceunit_fund_give_sum == default_fund_pool()
    assert voiceunit_fund_take_sum == default_fund_pool()


def test_BeliefUnit_cashout_SetsVoiceUnit_fund_give_fund_take():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    yao_belief.set_l1_plan(planunit_shop("swim"))
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_belief.set_voiceunit(voiceunit_shop(sue_str, 8))
    yao_belief.set_voiceunit(voiceunit_shop(bob_str))
    yao_belief.set_voiceunit(voiceunit_shop(zia_str))
    sue_voiceunit = yao_belief.get_voice(sue_str)
    bob_voiceunit = yao_belief.get_voice(bob_str)
    zia_voiceunit = yao_belief.get_voice(zia_str)
    assert sue_voiceunit.fund_give == 0
    assert sue_voiceunit.fund_take == 0
    assert bob_voiceunit.fund_give == 0
    assert bob_voiceunit.fund_take == 0
    assert zia_voiceunit.fund_give == 0
    assert zia_voiceunit.fund_take == 0

    # WHEN
    yao_belief.cashout()

    # THEN
    fund_give_sum = (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
    )
    assert fund_give_sum == 1.0 * default_fund_pool()
    fund_take_sum = (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
    )
    assert fund_take_sum == 1.0 * default_fund_pool()


def clear_all_voiceunits_groupunits_fund_agenda_give_take(x_belief: BeliefUnit):
    # delete belief_agenda_debt and belief_agenda_cred
    for groupunit_x in x_belief.groupunits.values():
        groupunit_x.clear_fund_give_take()
        # for membership_x in groupunit_x._voices.values():
        #     print(f"{groupunit_x.} {membership_x.}  {membership_x.fund_give:.6f} {membership_x.voice_debt_points=} {membership_fund_take:t:.6f} {membership_x.} ")

    # delete belief_agenda_debt and belief_agenda_cred
    for x_voiceunit in x_belief.voices.values():
        x_voiceunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupunit_give: float = 0
    sum_groupunit_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_sums(self, x_belief: BeliefUnit):
        for x_groupunit in x_belief.groupunits.values():
            self.sum_groupunit_give += x_groupunit.fund_agenda_give
            self.sum_groupunit_take += x_groupunit.fund_agenda_take
            for membership_x in x_groupunit.memberships.values():
                self.sum_membership_cred += membership_x.fund_agenda_give
                self.sum_membership_debt += membership_x.fund_agenda_take
                self.membership_count += 1


@dataclass
class AcclabelendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_belief: BeliefUnit):
        for voiceunit in x_belief.voices.values():
            self.sum_agenda_cred += voiceunit.fund_agenda_give
            self.sum_agenda_debt += voiceunit.fund_agenda_take
            self.sum_agenda_ratio_cred += voiceunit.fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += voiceunit.fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_belief_agenda_share = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_belief_i_sum = 0
    agenda_yes_belief_i_sum = 0

    def set_sums(self, agenda_dict: dict[RopePointer, PlanUnit]):
        for agenda_plan in agenda_dict.values():
            self.sum_belief_agenda_share += agenda_plan.get_fund_share()
            if agenda_plan.awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_belief_i_sum += agenda_plan.get_fund_share()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_belief_i_sum += agenda_plan.get_fund_share()


def test_BeliefUnit_agenda_cred_debt_SetAttrs():
    # ESTABLISH
    yao_belief = beliefunit_v001_with_large_agenda()
    clear_all_voiceunits_groupunits_fund_agenda_give_take(yao_belief)

    # TEST belief_agenda_debt and belief_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_belief)
    assert x_groupagendametrics.sum_groupunit_give == 0
    assert x_groupagendametrics.sum_groupunit_take == 0
    assert x_groupagendametrics.sum_membership_cred == 0
    assert x_groupagendametrics.sum_membership_debt == 0

    # TEST belief_agenda_debt and belief_agenda_cred are empty
    x_acclabelendametrics = AcclabelendaMetrics()
    x_acclabelendametrics.set_sums(yao_belief)
    assert x_acclabelendametrics.sum_agenda_cred == 0
    assert x_acclabelendametrics.sum_agenda_debt == 0
    assert x_acclabelendametrics.sum_agenda_ratio_cred == 0
    assert x_acclabelendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = yao_belief.get_agenda_dict()
    # for plan_rope in yao_belief._plan_dict.keys():
    #     print(f"{plan_rope=}")
    # for x_voice in yao_belief.voices.values():
    #     for x_membership in x_voice.memberships.values():
    #         print(f"{x_membership.group_title=}")

    # THEN
    print(f"{yao_belief.get_reason_contexts()=}")
    assert len(agenda_dict) == 63
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_belief_agenda_share=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    predicted_agenda_no_belief_i_sum = int(0.004107582 * default_fund_pool())
    assert (
        x_awardagendametrics.agenda_no_belief_i_sum == predicted_agenda_no_belief_i_sum
    )
    predicted_agenda_yes_belief_i_sum = int(0.003065400 * default_fund_pool())
    assert (
        x_awardagendametrics.agenda_yes_belief_i_sum
        == predicted_agenda_yes_belief_i_sum
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_belief_i_sum
        + x_awardagendametrics.agenda_yes_belief_i_sum,
        x_awardagendametrics.sum_belief_agenda_share,
    )
    predicted_sum_belief_agenda_share = 0.007172982 * default_fund_pool()
    assert (
        x_awardagendametrics.sum_belief_agenda_share
        == predicted_sum_belief_agenda_share
    )

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_sums(yao_belief)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 3065400
    print(f"{x_groupagendametrics.sum_groupunit_give=}")
    assert are_equal(x_groupagendametrics.sum_groupunit_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupunit_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_belief_i_sum,
        x_groupagendametrics.sum_groupunit_give,
    )

    assert all_voiceunits_have_legitimate_values(yao_belief)

    x_acclabelendametrics = AcclabelendaMetrics()
    x_acclabelendametrics.set_sums(yao_belief)
    assert are_equal(
        x_acclabelendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_belief_agenda_share,
    )
    assert are_equal(
        x_acclabelendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_belief_agenda_share,
    )
    assert are_equal(x_acclabelendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_acclabelendametrics.sum_agenda_ratio_debt, 1)

    # voiceunit_fund_give_sum = 0.0
    # voiceunit_fund_take_sum = 0.0

    # assert voiceunit_fund_give_sum == 1.0
    # assert voiceunit_fund_take_sum > 0.9999999
    # assert voiceunit_fund_take_sum < 1.00000001


def all_voiceunits_have_legitimate_values(x_belief: BeliefUnit):
    return not any(
        (
            voiceunit.fund_give is None
            or voiceunit.fund_give in [0.25, 0.5]
            or voiceunit.fund_take is None
            or voiceunit.fund_take in [0.8, 0.1]
        )
        for voiceunit in x_belief.voices.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_BeliefUnit_cashout_SetsAttrsWhenNoFactUnitsNoReasonUnitsEmpty_agenda_ratio_cred_debt():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    sue_voiceunit = voiceunit_shop(sue_str, 0.5, voice_debt_points=2)
    bob_voiceunit = voiceunit_shop(bob_str, 1.5, voice_debt_points=3)
    zia_voiceunit = voiceunit_shop(zia_str, 8, voice_debt_points=5)
    yao_belief.set_voiceunit(sue_voiceunit)
    yao_belief.set_voiceunit(bob_voiceunit)
    yao_belief.set_voiceunit(zia_voiceunit)
    sue_voice = yao_belief.get_voice(sue_str)
    bob_voice = yao_belief.get_voice(bob_str)
    zia_voice = yao_belief.get_voice(zia_str)

    assert not sue_voice.fund_give
    assert not sue_voice.fund_take
    assert not bob_voice.fund_give
    assert not bob_voice.fund_take
    assert not zia_voice.fund_give
    assert not zia_voice.fund_take
    assert not sue_voice.fund_agenda_give
    assert not sue_voice.fund_agenda_take
    assert not bob_voice.fund_agenda_give
    assert not bob_voice.fund_agenda_take
    assert not zia_voice.fund_agenda_give
    assert not zia_voice.fund_agenda_take
    assert not sue_voice.fund_agenda_ratio_give
    assert not sue_voice.fund_agenda_ratio_take
    assert not bob_voice.fund_agenda_ratio_give
    assert not bob_voice.fund_agenda_ratio_take
    assert not zia_voice.fund_agenda_ratio_give
    assert not zia_voice.fund_agenda_ratio_take

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.reason_contexts == set()
    assert sue_voice.fund_give == 50000000
    assert sue_voice.fund_take == 200000000
    assert bob_voice.fund_give == 150000000
    assert bob_voice.fund_take == 300000000
    assert zia_voice.fund_give == 800000000
    assert zia_voice.fund_take == 500000000
    assert sue_voice.fund_agenda_give == 50000000
    assert sue_voice.fund_agenda_take == 200000000
    assert bob_voice.fund_agenda_give == 150000000
    assert bob_voice.fund_agenda_take == 300000000
    assert zia_voice.fund_agenda_give == 800000000
    assert zia_voice.fund_agenda_take == 500000000
    assert sue_voice.fund_agenda_give == sue_voice.fund_give
    assert sue_voice.fund_agenda_take == sue_voice.fund_take
    assert bob_voice.fund_agenda_give == bob_voice.fund_give
    assert bob_voice.fund_agenda_take == bob_voice.fund_take
    assert zia_voice.fund_agenda_give == zia_voice.fund_give
    assert zia_voice.fund_agenda_take == zia_voice.fund_take
    assert sue_voice.fund_agenda_ratio_give == 0.05
    assert sue_voice.fund_agenda_ratio_take == 0.2
    assert bob_voice.fund_agenda_ratio_give == 0.15
    assert bob_voice.fund_agenda_ratio_take == 0.3
    assert zia_voice.fund_agenda_ratio_give == 0.8
    assert zia_voice.fund_agenda_ratio_take == 0.5


def test_BeliefUnit_cashout_CreatesGroupUnitWith_beliefunit_v001():
    # ESTABLISH / WHEN
    yao_belief = beliefunit_v001()
    yao_belief.cashout()

    # THEN
    assert yao_belief.groupunits is not None
    assert len(yao_belief.groupunits) == 34
    everyone_voices_len = None
    everyone_group = yao_belief.get_groupunit(";Everyone")
    everyone_voices_len = len(everyone_group.memberships)
    assert everyone_voices_len == 22

    # WHEN
    yao_belief.cashout()
    plan_dict = yao_belief._plan_dict

    # THEN
    # print(f"{len(plan_dict)=}")
    db_plan = plan_dict.get(yao_belief.make_l1_rope("D&B"))
    assert len(db_plan.awardunits) == 3
    # for plan_key in plan_dict:
    #     print(f"{plan_key=}")
    #     if plan.plan_label == "D&B":
    #         print(f"{plan.plan_label=} {plan.awardunits=}")
    #         db_awardunit_len = len(plan.awardunits)
    # assert db_awardunit_len == 3
