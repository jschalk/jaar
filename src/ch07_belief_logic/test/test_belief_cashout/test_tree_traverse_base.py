from pytest import raises as pytest_raises
from src.ch03_voice.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason import factheir_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import (
    get_beliefunit_with_4_levels,
    get_beliefunit_with_4_levels_and_2reasons,
)


def test_BeliefUnit_clear_plan_dict_and_belief_obj_settle_attrs_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_plan_dict = {1: 2, 2: 4}
    sue_belief.rational = x_rational
    sue_belief.tree_traverse_count = x_tree_traverse_count
    sue_belief._plan_dict = x_plan_dict
    sue_belief.offtrack_kids_star_set = "example"
    sue_belief.reason_contexts = {"example2"}
    sue_belief.range_inheritors = {"example2": 1}
    assert sue_belief.rational == x_rational
    assert sue_belief.tree_traverse_count == x_tree_traverse_count
    assert sue_belief._plan_dict == x_plan_dict
    assert sue_belief.offtrack_kids_star_set != set()
    assert sue_belief.reason_contexts != set()
    assert sue_belief.range_inheritors != {}

    # WHEN
    sue_belief._clear_plan_dict_and_belief_obj_settle_attrs()

    # THEN
    assert sue_belief.rational != x_rational
    assert not sue_belief.rational
    assert sue_belief.tree_traverse_count != x_tree_traverse_count
    assert sue_belief.tree_traverse_count == 0
    assert sue_belief._plan_dict != x_plan_dict
    assert sue_belief._plan_dict == {
        sue_belief.planroot.get_plan_rope(): sue_belief.planroot
    }
    assert sue_belief.offtrack_kids_star_set == set()
    assert not sue_belief.reason_contexts
    assert not sue_belief.range_inheritors


def test_BeliefUnit_clear_plan_dict_and_belief_obj_settle_attrs_SetsAttrs_Scenario1():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerunit_plans_fund_total = 140
    sue_belief.keeps_justified = x_keep_justifed
    sue_belief.keeps_buildable = "swimmers"
    sue_belief.sum_healerunit_plans_fund_total = x_sum_healerunit_plans_fund_total
    sue_belief._keep_dict = {"run": "run"}
    sue_belief._healers_dict = {"run": "run"}
    assert sue_belief.keeps_justified == x_keep_justifed
    assert sue_belief.keeps_buildable
    assert (
        sue_belief.sum_healerunit_plans_fund_total == x_sum_healerunit_plans_fund_total
    )
    assert sue_belief._keep_dict != {}
    assert sue_belief._healers_dict != {}

    # WHEN
    sue_belief._clear_plan_dict_and_belief_obj_settle_attrs()

    # THEN
    assert sue_belief.keeps_justified != x_keep_justifed
    assert sue_belief.keeps_justified
    assert sue_belief.keeps_buildable is False
    assert sue_belief.sum_healerunit_plans_fund_total == 0
    assert not sue_belief._keep_dict
    assert not sue_belief._healers_dict


def test_BeliefUnit_cashout_ClearsDescendantAttributes():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = sue_belief.make_rope(wk_rope, mon_str)
    mon_plan = sue_belief.get_plan_obj(mon_rope)
    assert sue_belief.planroot.descendant_pledge_count is None
    assert sue_belief.planroot.all_voice_cred is None
    assert sue_belief.planroot.all_voice_debt is None
    assert casa_plan.descendant_pledge_count is None
    assert casa_plan.all_voice_cred is None
    assert casa_plan.all_voice_debt is None
    assert mon_plan.descendant_pledge_count is None
    assert mon_plan.all_voice_cred is None
    assert mon_plan.all_voice_debt is None

    sue_belief.planroot.descendant_pledge_count = -2
    sue_belief.planroot.all_voice_cred = -2
    sue_belief.planroot.all_voice_debt = -2
    casa_plan.descendant_pledge_count = -2
    casa_plan.all_voice_cred = -2
    casa_plan.all_voice_debt = -2
    mon_plan.descendant_pledge_count = -2
    mon_plan.all_voice_cred = -2
    mon_plan.all_voice_debt = -2

    assert sue_belief.planroot.descendant_pledge_count == -2
    assert sue_belief.planroot.all_voice_cred == -2
    assert sue_belief.planroot.all_voice_debt == -2
    assert casa_plan.descendant_pledge_count == -2
    assert casa_plan.all_voice_cred == -2
    assert casa_plan.all_voice_debt == -2
    assert mon_plan.descendant_pledge_count == -2
    assert mon_plan.all_voice_cred == -2
    assert mon_plan.all_voice_debt == -2

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.planroot.descendant_pledge_count == 2
    assert casa_plan.descendant_pledge_count == 0
    assert mon_plan.descendant_pledge_count == 0

    assert mon_plan.all_voice_cred is True
    assert mon_plan.all_voice_debt is True
    assert casa_plan.all_voice_cred is True
    assert casa_plan.all_voice_debt is True
    assert sue_belief.planroot.all_voice_cred is True
    assert sue_belief.planroot.all_voice_debt is True


def test_BeliefUnit_cashout_RootOnlySetsDescendantAttributes():
    # ESTABLISH
    yao_belief = beliefunit_shop(belief_name="Yao")
    assert yao_belief.planroot.descendant_pledge_count is None
    assert yao_belief.planroot.all_voice_cred is None
    assert yao_belief.planroot.all_voice_debt is None

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.planroot.descendant_pledge_count == 0
    assert yao_belief.planroot.all_voice_cred is True
    assert yao_belief.planroot.all_voice_debt is True


def test_BeliefUnit_cashout_NLevelSetsDescendantAttributes_1():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wk_plan = sue_belief.get_plan_obj(wk_rope)
    mon_str = "Mon"
    mon_rope = sue_belief.make_rope(wk_rope, mon_str)
    mon_plan = sue_belief.get_plan_obj(mon_rope)

    email_str = "email"
    email_plan = planunit_shop(email_str, pledge=True)
    sue_belief.set_plan_obj(email_plan, parent_rope=casa_rope)

    root_rope = sue_belief.planroot.get_plan_rope()
    x_planroot = sue_belief.get_plan_obj(root_rope)
    assert x_planroot.descendant_pledge_count is None
    assert x_planroot.all_voice_cred is None
    assert x_planroot.all_voice_debt is None
    assert casa_plan.descendant_pledge_count is None
    assert casa_plan.all_voice_cred is None
    assert casa_plan.all_voice_debt is None
    assert mon_plan.descendant_pledge_count is None
    assert mon_plan.all_voice_cred is None
    assert mon_plan.all_voice_debt is None

    # WHEN
    sue_belief.cashout()

    # THEN
    assert x_planroot.descendant_pledge_count == 3
    assert casa_plan.descendant_pledge_count == 1
    assert casa_plan.kids[email_str].descendant_pledge_count == 0
    assert mon_plan.descendant_pledge_count == 0
    assert x_planroot.all_voice_cred is True
    assert x_planroot.all_voice_debt is True
    assert casa_plan.all_voice_cred is True
    assert casa_plan.all_voice_debt is True
    assert mon_plan.all_voice_cred is True
    assert mon_plan.all_voice_debt is True


def test_BeliefUnit_cashout_NLevelSetsDescendantAttributes_2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    email_str = "email"
    casa_str = "casa"
    wk_str = "sem_jours"
    mon_str = "Mon"
    tue_str = "Tue"
    vacuum_str = "vacuum"
    sue_str = "Sue"

    casa_rope = sue_belief.make_l1_rope(casa_str)
    email_plan = planunit_shop(email_str, pledge=True)
    sue_belief.set_plan_obj(email_plan, parent_rope=casa_rope)
    vacuum_plan = planunit_shop(vacuum_str, pledge=True)
    sue_belief.set_plan_obj(vacuum_plan, parent_rope=casa_rope)

    sue_belief.add_voiceunit(voice_name=sue_str)
    x_awardunit = awardunit_shop(awardee_title=sue_str)

    sue_belief.planroot.kids[casa_str].kids[email_str].set_awardunit(
        awardunit=x_awardunit
    )
    # print(sue_belief.kids[casa_str].kids[email_str])
    # print(sue_belief.kids[casa_str].kids[email_str].awardunit)

    # WHEN
    sue_belief.cashout()
    # print(sue_belief.kids[casa_str].kids[email_str])
    # print(sue_belief.kids[casa_str].kids[email_str].awardunit)

    # THEN
    assert sue_belief.planroot.all_voice_cred is False
    assert sue_belief.planroot.all_voice_debt is False
    casa_plan = sue_belief.planroot.kids[casa_str]
    assert casa_plan.all_voice_cred is False
    assert casa_plan.all_voice_debt is False
    assert casa_plan.kids[email_str].all_voice_cred is False
    assert casa_plan.kids[email_str].all_voice_debt is False
    assert casa_plan.kids[vacuum_str].all_voice_cred is True
    assert casa_plan.kids[vacuum_str].all_voice_debt is True
    wk_plan = sue_belief.planroot.kids[wk_str]
    assert wk_plan.all_voice_cred is True
    assert wk_plan.all_voice_debt is True
    assert wk_plan.kids[mon_str].all_voice_cred is True
    assert wk_plan.kids[mon_str].all_voice_debt is True
    assert wk_plan.kids[tue_str].all_voice_cred is True
    assert wk_plan.kids[tue_str].all_voice_debt is True


def test_BeliefUnit_cashout_SetsPlanUnitAttr_awardunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_belief.add_voiceunit(yao_str)
    sue_belief.add_voiceunit(zia_str)
    sue_belief.add_voiceunit(Xio_str)

    assert len(sue_belief.voices) == 3
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 3
    swim_str = "swim"
    sue_belief.set_l1_plan(planunit_shop(swim_str))
    awardunit_yao = awardunit_shop(yao_str, give_force=10)
    awardunit_zia = awardunit_shop(zia_str, give_force=10)
    awardunit_Xio = awardunit_shop(Xio_str, give_force=10)
    swim_rope = sue_belief.make_l1_rope(swim_str)
    sue_belief.edit_plan_attr(swim_rope, awardunit=awardunit_yao)
    sue_belief.edit_plan_attr(swim_rope, awardunit=awardunit_zia)
    sue_belief.edit_plan_attr(swim_rope, awardunit=awardunit_Xio)

    street_str = "streets"
    sue_belief.set_plan_obj(planunit_shop(street_str), parent_rope=swim_rope)
    assert sue_belief.planroot.awardunits in (None, {})
    assert len(sue_belief.planroot.kids[swim_str].awardunits) == 3

    # WHEN
    sue_belief.cashout()

    # THEN
    print(f"{sue_belief._plan_dict.keys()=} ")
    swim_plan = sue_belief._plan_dict.get(swim_rope)
    street_plan = sue_belief._plan_dict.get(sue_belief.make_rope(swim_rope, street_str))

    assert len(swim_plan.awardunits) == 3
    assert len(swim_plan.awardheirs) == 3
    assert street_plan.awardunits in (None, {})
    assert len(street_plan.awardheirs) == 3

    print(f"{len(sue_belief._plan_dict)}")
    print(f"{swim_plan.awardunits}")
    print(f"{swim_plan.awardheirs}")
    print(f"{swim_plan.awardheirs}")
    assert len(sue_belief.planroot.kids["swim"].awardheirs) == 3


def test_BeliefUnit_cashout_TreeTraverseSetsClearsAwardLineestors():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.cashout()
    # plan tree has no awardunits
    assert sue_belief.planroot.awardlines == {}
    sue_belief.planroot.awardlines = {1: "testtest"}
    assert sue_belief.planroot.awardlines != {}

    # WHEN
    sue_belief.cashout()

    # THEN
    assert not sue_belief.planroot.awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_plan = sue_belief.planroot.kids[casa_str]
    casa_plan.awardlines = {1: "testtest"}
    assert casa_plan.awardlines != {}
    sue_belief.cashout()

    # THEN
    assert not sue_belief.planroot.kids[casa_str].awardlines


def test_BeliefUnit_cashout_DoesNotKeepNonRequired_awardheirs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(zia_str)
    yao_belief.add_voiceunit(Xio_str)

    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)

    yao_belief.set_l1_plan(planunit_shop(swim_str))
    awardunit_yao = awardunit_shop(yao_str, give_force=10)
    awardunit_zia = awardunit_shop(zia_str, give_force=10)
    awardunit_Xio = awardunit_shop(Xio_str, give_force=10)

    swim_plan = yao_belief.get_plan_obj(swim_rope)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_yao)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_zia)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_Xio)

    assert len(swim_plan.awardunits) == 3
    assert len(swim_plan.awardheirs) == 0

    # WHEN
    yao_belief.cashout()

    # THEN
    assert len(swim_plan.awardunits) == 3
    assert len(swim_plan.awardheirs) == 3
    yao_belief.edit_plan_attr(swim_rope, awardunit_del=yao_str)
    assert len(swim_plan.awardunits) == 2
    assert len(swim_plan.awardheirs) == 3

    # WHEN
    yao_belief.cashout()

    # THEN
    assert len(swim_plan.awardunits) == 2
    assert len(swim_plan.awardheirs) == 2


def test_BeliefUnit_get_plan_tree_ordered_rope_list_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    wk_str = "sem_jours"
    assert sue_belief.get_plan_tree_ordered_rope_list()

    # WHEN
    ordered_label_list = sue_belief.get_plan_tree_ordered_rope_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_rope_in_ordered_list = sue_belief.get_plan_tree_ordered_rope_list()[0]
    root_rope = sue_belief.planroot.get_plan_rope()
    assert x_1st_rope_in_ordered_list == root_rope
    x_8th_rope_in_ordered_list = sue_belief.get_plan_tree_ordered_rope_list()[9]
    assert x_8th_rope_in_ordered_list == sue_belief.make_l1_rope(wk_str)


def test_BeliefUnit_get_plan_tree_ordered_rope_list_ReturnsObj_Scenario1():
    # ESTABLISH
    y_belief = beliefunit_shop("Bob", "amy23")
    root_rope = y_belief.planroot.get_plan_rope()

    # WHEN
    y_1st_rope_in_ordered_list = y_belief.get_plan_tree_ordered_rope_list()[0]
    # THEN
    assert y_1st_rope_in_ordered_list == root_rope


def test_BeliefUnit_get_plan_tree_ordered_rope_list_Scenario2_CleansRangedPlanRopeTerms():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")

    # WHEN
    ziet_str = "zietline"
    ziet_rope = yao_belief.make_l1_rope(ziet_str)
    yao_belief.set_l1_plan(planunit_shop(ziet_str, begin=0, close=700))
    wks_str = "wks"
    yao_belief.set_plan_obj(planunit_shop(wks_str, denom=7), ziet_rope)

    # THEN
    assert len(yao_belief.get_plan_tree_ordered_rope_list()) == 3
    assert (
        len(yao_belief.get_plan_tree_ordered_rope_list(no_range_descendants=True)) == 2
    )


def test_BeliefUnit_get_plan_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    texas_str = "Texas"
    sue_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_belief.set_l1_plan(planunit_shop(casa_str))

    # WHEN
    problems_dict = sue_belief.get_plan_dict(problem=True)

    # THEN
    assert sue_belief.keeps_justified
    texas_rope = sue_belief.make_l1_rope(texas_str)
    texas_plan = sue_belief.get_plan_obj(texas_rope)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_rope: texas_plan}


def test_BeliefUnit_cashout_CreatesFullyPopulated_plan_dict():
    # ESTABLISH
    sue_beliefunit = get_beliefunit_with_4_levels_and_2reasons()

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    assert len(sue_beliefunit._plan_dict) == 17


def test_BeliefUnit_cashout_Resets_offtrack_kids_star_set():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    sue_beliefunit.offtrack_kids_star_set = set("YY")
    x_set = set()

    assert sue_beliefunit.offtrack_kids_star_set != x_set

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    assert sue_beliefunit.offtrack_kids_star_set == x_set


def test_BeliefUnit_cashout_WhenPlanRootHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_plan = planunit_shop(casa_str, star=0)
    sue_beliefunit.set_l1_plan(casa_plan)
    assert sue_beliefunit.offtrack_kids_star_set == set()

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    root_rope = sue_beliefunit.planroot.get_plan_rope()
    assert sue_beliefunit.offtrack_kids_star_set == {root_rope}

    # WHEN
    sue_beliefunit.edit_plan_attr(casa_rope, star=2)
    sue_beliefunit.cashout()

    # THEN
    assert sue_beliefunit.offtrack_kids_star_set == set()


def test_BeliefUnit_cashout_WhenPlanUnitHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_beliefunit.make_l1_rope(casa_str)
    casa_plan = planunit_shop(casa_str, star=1)

    swim_str = "swimming"
    swim_rope = sue_beliefunit.make_rope(casa_rope, swim_str)
    swim_plan = planunit_shop(swim_str, star=8)

    clean_str = "cleaning"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    clean_plan = planunit_shop(clean_str, star=2)
    sue_beliefunit.set_plan_obj(planunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_beliefunit.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, star=0)
    vacuum_str = "vacuum"
    vacuum_rope = sue_beliefunit.make_rope(clean_rope, vacuum_str)
    vacuum_plan = planunit_shop(vacuum_str, star=0)

    sue_beliefunit.set_l1_plan(casa_plan)
    sue_beliefunit.set_plan_obj(swim_plan, casa_rope)
    sue_beliefunit.set_plan_obj(clean_plan, casa_rope)
    sue_beliefunit.set_plan_obj(sweep_plan, clean_rope)  # _star=0
    sue_beliefunit.set_plan_obj(vacuum_plan, clean_rope)  # _star=0

    assert sue_beliefunit.offtrack_kids_star_set == set()

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    assert sue_beliefunit.offtrack_kids_star_set == {clean_rope}


def test_BeliefUnit_cashout_CreatesNewGroupUnits_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    zia_str = "Zia"
    yao_voice_cred_lumen = 3
    yao_voice_debt_lumen = 2
    zia_voice_cred_lumen = 4
    zia_voice_debt_lumen = 5
    yao_belief.add_voiceunit(yao_str, yao_voice_cred_lumen, yao_voice_debt_lumen)
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    root_rope = yao_belief.planroot.get_plan_rope()
    x_planroot = yao_belief.get_plan_obj(root_rope)
    x_planroot.set_awardunit(awardunit_shop(yao_str))
    x_planroot.set_awardunit(awardunit_shop(zia_str))
    xio_str = "Xio"
    x_planroot.set_awardunit(awardunit_shop(xio_str))
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 2
    assert not yao_belief.groupunit_exists(yao_str)
    assert not yao_belief.groupunit_exists(zia_str)
    assert not yao_belief.groupunit_exists(xio_str)

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.groupunit_exists(yao_str)
    assert yao_belief.groupunit_exists(zia_str)
    assert yao_belief.groupunit_exists(xio_str)
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 2
    assert len(yao_belief.get_voiceunit_group_titles_dict()) != len(
        yao_belief.groupunits
    )
    assert len(yao_belief.groupunits) == 3
    xio_groupunit = yao_belief.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_belief.create_symmetry_groupunit(xio_str)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(yao_str)
    assert xio_groupunit.group_membership_exists(zia_str)
    assert not xio_groupunit.group_membership_exists(xio_str)
    yao_membership = xio_groupunit.get_voice_membership(yao_str)
    zia_membership = xio_groupunit.get_voice_membership(zia_str)
    assert yao_membership.group_cred_lumen == yao_voice_cred_lumen
    assert zia_membership.group_cred_lumen == zia_voice_cred_lumen
    assert yao_membership.group_debt_lumen == yao_voice_debt_lumen
    assert zia_membership.group_debt_lumen == zia_voice_debt_lumen


def test_BeliefUnit_cashout_CreatesNewGroupUnits_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)
    yao_belief.set_l1_plan(planunit_shop(swim_str))
    zia_str = "Zia"
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(zia_str)
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(awardunit_shop(yao_str))
    swim_plan.set_awardunit(awardunit_shop(zia_str))
    xio_str = "Xio"
    swim_plan.set_awardunit(awardunit_shop(xio_str))
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 2
    assert not yao_belief.groupunit_exists(yao_str)
    assert not yao_belief.groupunit_exists(zia_str)
    assert not yao_belief.groupunit_exists(xio_str)

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.groupunit_exists(yao_str)
    assert yao_belief.groupunit_exists(zia_str)
    assert yao_belief.groupunit_exists(xio_str)
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 2
    assert len(yao_belief.get_voiceunit_group_titles_dict()) != len(
        yao_belief.groupunits
    )
    assert len(yao_belief.groupunits) == 3
    xio_groupunit = yao_belief.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_belief.create_symmetry_groupunit(xio_str)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(yao_str)
    assert xio_groupunit.group_membership_exists(zia_str)
    assert not xio_groupunit.group_membership_exists(xio_str)


def test_BeliefUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)
    yao_belief.set_l1_plan(planunit_shop(swim_str))
    zia_str = "Zia"
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(zia_str)
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    swim_plan.set_awardunit(awardunit_shop(yao_str))
    swim_plan.set_awardunit(awardunit_shop(zia_str))
    xio_str = "Xio"
    swim_plan.set_awardunit(awardunit_shop(xio_str))
    yao_belief.cashout()
    assert yao_belief.groupunit_exists(yao_str)
    assert yao_belief.groupunit_exists(zia_str)
    assert yao_belief.groupunit_exists(xio_str)
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 2
    assert len(yao_belief.get_voiceunit_group_titles_dict()) != len(
        yao_belief.groupunits
    )

    # WHEN
    symmerty_group_titles = yao_belief.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_plan.set_awardunit(awardunit_shop(run_str))
    assert not yao_belief.groupunit_exists(run_str)
    yao_belief.cashout()
    assert yao_belief.groupunit_exists(run_str)

    # WHEN
    symmerty_group_titles = yao_belief.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {xio_str, run_str}


def test_BeliefUnit_cashout_Sets_planroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_belief.make_l1_rope(wk_str)
    wk_addin = 10
    wk_plan = planunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_belief.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_belief.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_belief.set_plan_obj(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    root_rope = yao_belief.planroot.get_plan_rope()
    yao_belief.edit_plan_attr(root_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_belief.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_plan.reasonheirs) == 1
    # assert ball_plan.factheirs == {wk_rope: wk_factheir}
    # assert ball_plan.factheirs.get(wk_rope)
    # assert len(ball_plan.factheirs) == 1
    # assert ball_plan.factheirs.get(tue_rope) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_belief.cashout()

    # THEN
    exception_str = f"Cannot have fact for range inheritor '{tue_rope}'. A ranged fact plan must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_belief_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_belief_plan_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_rope: wk_rope}
    # wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # tue_reason_lower = 113
    # tue_reason_upper = 117
    # tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    # root_plan = yao_belief.get_plan_obj(root_rope)
    # print(f"{wk_rope=} {root_plan.factheirs.keys()=}")
    # assert root_plan.factheirs.get(wk_rope) == wk_factheir
    # assert len(root_plan.factheirs) == 2
    # assert root_plan.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_BeliefUnit_cashout_SetsPlanUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_belief.make_l1_rope(wk_str)
    wk_addin = 10
    wk_plan = planunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_belief.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_belief.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_belief.set_plan_obj(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    ball_str = "ball"
    ball_rope = yao_belief.make_l1_rope(ball_str)
    yao_belief.set_l1_plan(planunit_shop(ball_str))
    yao_belief.edit_plan_attr(ball_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_belief.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_plan.reasonheirs) == 1
    # assert ball_plan.factheirs == {wk_rope: wk_factheir}
    # assert ball_plan.factheirs.get(wk_rope)
    # assert len(ball_plan.factheirs) == 1
    # assert ball_plan.factheirs.get(tue_rope) is None

    # WHEN
    yao_belief.cashout()

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_belief_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_belief_plan_dict, tue_reasonheirs)
    x_range_inheritors = {tue_rope: wk_rope}
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    tue_reason_lower = 113
    tue_reason_upper = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    ball_plan = yao_belief.get_plan_obj(ball_rope)
    print(f"{wk_rope=} {ball_plan.factheirs.keys()=}")
    assert ball_plan.factheirs.get(wk_rope) == wk_factheir
    assert len(ball_plan.factheirs) == 2
    assert ball_plan.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}
