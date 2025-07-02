from pytest import raises as pytest_raises
from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factheir_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with_4_levels,
    get_ownerunit_with_4_levels_and_2reasons,
)


def test_OwnerUnit_clear_plan_dict_and_owner_obj_settle_attrs_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_plan_dict = {1: 2, 2: 4}
    sue_owner._rational = x_rational
    sue_owner._tree_traverse_count = x_tree_traverse_count
    sue_owner._plan_dict = x_plan_dict
    sue_owner._offtrack_kids_mass_set = "example"
    sue_owner._reason_rcontexts = {"example2"}
    sue_owner._range_inheritors = {"example2": 1}
    assert sue_owner._rational == x_rational
    assert sue_owner._tree_traverse_count == x_tree_traverse_count
    assert sue_owner._plan_dict == x_plan_dict
    assert sue_owner._offtrack_kids_mass_set != set()
    assert sue_owner._reason_rcontexts != set()
    assert sue_owner._range_inheritors != {}

    # WHEN
    sue_owner._clear_plan_dict_and_owner_obj_settle_attrs()

    # THEN
    assert sue_owner._rational != x_rational
    assert not sue_owner._rational
    assert sue_owner._tree_traverse_count != x_tree_traverse_count
    assert sue_owner._tree_traverse_count == 0
    assert sue_owner._plan_dict != x_plan_dict
    assert sue_owner._plan_dict == {
        sue_owner.planroot.get_plan_rope(): sue_owner.planroot
    }
    assert sue_owner._offtrack_kids_mass_set == set()
    assert not sue_owner._reason_rcontexts
    assert not sue_owner._range_inheritors


def test_OwnerUnit_clear_plan_dict_and_owner_obj_settle_attrs_SetsAttrs_Scenario1():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerlink_share = 140
    sue_owner._keeps_justified = x_keep_justifed
    sue_owner._keeps_buildable = "swimmers"
    sue_owner._sum_healerlink_share = x_sum_healerlink_share
    sue_owner._keep_dict = {"run": "run"}
    sue_owner._healers_dict = {"run": "run"}
    assert sue_owner._keeps_justified == x_keep_justifed
    assert sue_owner._keeps_buildable
    assert sue_owner._sum_healerlink_share == x_sum_healerlink_share
    assert sue_owner._keep_dict != {}
    assert sue_owner._healers_dict != {}

    # WHEN
    sue_owner._clear_plan_dict_and_owner_obj_settle_attrs()

    # THEN
    assert sue_owner._keeps_justified != x_keep_justifed
    assert sue_owner._keeps_justified
    assert sue_owner._keeps_buildable is False
    assert sue_owner._sum_healerlink_share == 0
    assert not sue_owner._keep_dict
    assert not sue_owner._healers_dict


def test_OwnerUnit_settle_owner_ClearsDescendantAttributes():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    # test root status:
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    casa_plan = sue_owner.get_plan_obj(casa_rope)
    wk_str = "wkdays"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    mon_str = "Monday"
    mon_rope = sue_owner.make_rope(wk_rope, mon_str)
    mon_plan = sue_owner.get_plan_obj(mon_rope)
    assert sue_owner.planroot._descendant_task_count is None
    assert sue_owner.planroot._all_acct_cred is None
    assert sue_owner.planroot._all_acct_debt is None
    assert casa_plan._descendant_task_count is None
    assert casa_plan._all_acct_cred is None
    assert casa_plan._all_acct_debt is None
    assert mon_plan._descendant_task_count is None
    assert mon_plan._all_acct_cred is None
    assert mon_plan._all_acct_debt is None

    sue_owner.planroot._descendant_task_count = -2
    sue_owner.planroot._all_acct_cred = -2
    sue_owner.planroot._all_acct_debt = -2
    casa_plan._descendant_task_count = -2
    casa_plan._all_acct_cred = -2
    casa_plan._all_acct_debt = -2
    mon_plan._descendant_task_count = -2
    mon_plan._all_acct_cred = -2
    mon_plan._all_acct_debt = -2

    assert sue_owner.planroot._descendant_task_count == -2
    assert sue_owner.planroot._all_acct_cred == -2
    assert sue_owner.planroot._all_acct_debt == -2
    assert casa_plan._descendant_task_count == -2
    assert casa_plan._all_acct_cred == -2
    assert casa_plan._all_acct_debt == -2
    assert mon_plan._descendant_task_count == -2
    assert mon_plan._all_acct_cred == -2
    assert mon_plan._all_acct_debt == -2

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner.planroot._descendant_task_count == 2
    assert casa_plan._descendant_task_count == 0
    assert mon_plan._descendant_task_count == 0

    assert mon_plan._all_acct_cred is True
    assert mon_plan._all_acct_debt is True
    assert casa_plan._all_acct_cred is True
    assert casa_plan._all_acct_debt is True
    assert sue_owner.planroot._all_acct_cred is True
    assert sue_owner.planroot._all_acct_debt is True


def test_OwnerUnit_settle_owner_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_owner = ownerunit_shop(owner_name="Yao")
    assert yao_owner.planroot._descendant_task_count is None
    assert yao_owner.planroot._all_acct_cred is None
    assert yao_owner.planroot._all_acct_debt is None

    # WHEN
    yao_owner.settle_owner()

    # THEN
    assert yao_owner.planroot._descendant_task_count == 0
    assert yao_owner.planroot._all_acct_cred is True
    assert yao_owner.planroot._all_acct_debt is True


def test_OwnerUnit_settle_owner_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    casa_plan = sue_owner.get_plan_obj(casa_rope)
    wk_str = "wkdays"
    wk_rope = sue_owner.make_l1_rope(wk_str)
    wk_plan = sue_owner.get_plan_obj(wk_rope)
    mon_str = "Monday"
    mon_rope = sue_owner.make_rope(wk_rope, mon_str)
    mon_plan = sue_owner.get_plan_obj(mon_rope)

    email_str = "email"
    email_plan = planunit_shop(email_str, task=True)
    sue_owner.set_plan(email_plan, parent_rope=casa_rope)

    # test root status:
    root_rope = to_rope(sue_owner.belief_label)
    x_planroot = sue_owner.get_plan_obj(root_rope)
    assert x_planroot._descendant_task_count is None
    assert x_planroot._all_acct_cred is None
    assert x_planroot._all_acct_debt is None
    assert casa_plan._descendant_task_count is None
    assert casa_plan._all_acct_cred is None
    assert casa_plan._all_acct_debt is None
    assert mon_plan._descendant_task_count is None
    assert mon_plan._all_acct_cred is None
    assert mon_plan._all_acct_debt is None

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert x_planroot._descendant_task_count == 3
    assert casa_plan._descendant_task_count == 1
    assert casa_plan._kids[email_str]._descendant_task_count == 0
    assert mon_plan._descendant_task_count == 0
    assert x_planroot._all_acct_cred is True
    assert x_planroot._all_acct_debt is True
    assert casa_plan._all_acct_cred is True
    assert casa_plan._all_acct_debt is True
    assert mon_plan._all_acct_cred is True
    assert mon_plan._all_acct_debt is True


def test_OwnerUnit_settle_owner_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    email_str = "email"
    casa_str = "casa"
    wk_str = "wkdays"
    mon_str = "Monday"
    tue_str = "Tuesday"
    vacuum_str = "vacuum"
    sue_str = "Sue"

    casa_rope = sue_owner.make_l1_rope(casa_str)
    email_plan = planunit_shop(email_str, task=True)
    sue_owner.set_plan(email_plan, parent_rope=casa_rope)
    vacuum_plan = planunit_shop(vacuum_str, task=True)
    sue_owner.set_plan(vacuum_plan, parent_rope=casa_rope)

    sue_owner.add_acctunit(acct_name=sue_str)
    x_awardlink = awardlink_shop(awardee_title=sue_str)

    sue_owner.planroot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_owner._kids[casa_str]._kids[email_str])
    # print(sue_owner._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_owner.settle_owner()
    # print(sue_owner._kids[casa_str]._kids[email_str])
    # print(sue_owner._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_owner.planroot._all_acct_cred is False
    assert sue_owner.planroot._all_acct_debt is False
    casa_plan = sue_owner.planroot._kids[casa_str]
    assert casa_plan._all_acct_cred is False
    assert casa_plan._all_acct_debt is False
    assert casa_plan._kids[email_str]._all_acct_cred is False
    assert casa_plan._kids[email_str]._all_acct_debt is False
    assert casa_plan._kids[vacuum_str]._all_acct_cred is True
    assert casa_plan._kids[vacuum_str]._all_acct_debt is True
    wk_plan = sue_owner.planroot._kids[wk_str]
    assert wk_plan._all_acct_cred is True
    assert wk_plan._all_acct_debt is True
    assert wk_plan._kids[mon_str]._all_acct_cred is True
    assert wk_plan._kids[mon_str]._all_acct_debt is True
    assert wk_plan._kids[tue_str]._all_acct_cred is True
    assert wk_plan._kids[tue_str]._all_acct_debt is True


def test_OwnerUnit_settle_owner_SetsPlanUnitAttr_awardlinks():
    # ESTABLISH
    sue_str = "Sue"
    sue_owner = ownerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_owner.add_acctunit(yao_str)
    sue_owner.add_acctunit(zia_str)
    sue_owner.add_acctunit(Xio_str)

    assert len(sue_owner.accts) == 3
    assert len(sue_owner.get_acctunit_group_titles_dict()) == 3
    swim_str = "swim"
    sue_owner.set_l1_plan(planunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_rope = sue_owner.make_l1_rope(swim_str)
    sue_owner.edit_plan_attr(swim_rope, awardlink=awardlink_yao)
    sue_owner.edit_plan_attr(swim_rope, awardlink=awardlink_zia)
    sue_owner.edit_plan_attr(swim_rope, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_owner.set_plan(planunit_shop(street_str), parent_rope=swim_rope)
    assert sue_owner.planroot.awardlinks in (None, {})
    assert len(sue_owner.planroot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_owner.settle_owner()

    # THEN
    print(f"{sue_owner._plan_dict.keys()=} ")
    swim_plan = sue_owner._plan_dict.get(swim_rope)
    street_plan = sue_owner._plan_dict.get(sue_owner.make_rope(swim_rope, street_str))

    assert len(swim_plan.awardlinks) == 3
    assert len(swim_plan._awardheirs) == 3
    assert street_plan.awardlinks in (None, {})
    assert len(street_plan._awardheirs) == 3

    print(f"{len(sue_owner._plan_dict)}")
    print(f"{swim_plan.awardlinks}")
    print(f"{swim_plan._awardheirs}")
    print(f"{swim_plan._awardheirs}")
    assert len(sue_owner.planroot._kids["swim"]._awardheirs) == 3


def test_OwnerUnit_settle_owner_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    sue_owner.settle_owner()
    # plan tree has no awardlinks
    assert sue_owner.planroot._awardlines == {}
    sue_owner.planroot._awardlines = {1: "testtest"}
    assert sue_owner.planroot._awardlines != {}

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert not sue_owner.planroot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_plan = sue_owner.planroot._kids[casa_str]
    casa_plan._awardlines = {1: "testtest"}
    assert casa_plan._awardlines != {}
    sue_owner.settle_owner()

    # THEN
    assert not sue_owner.planroot._kids[casa_str]._awardlines


def test_OwnerUnit_settle_owner_DoesNotKeepUnneeded_awardheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_owner.add_acctunit(yao_str)
    yao_owner.add_acctunit(zia_str)
    yao_owner.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_rope = yao_owner.make_l1_rope(swim_str)

    yao_owner.set_l1_plan(planunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_plan = yao_owner.get_plan_obj(swim_rope)
    yao_owner.edit_plan_attr(swim_rope, awardlink=awardlink_yao)
    yao_owner.edit_plan_attr(swim_rope, awardlink=awardlink_zia)
    yao_owner.edit_plan_attr(swim_rope, awardlink=awardlink_Xio)

    assert len(swim_plan.awardlinks) == 3
    assert len(swim_plan._awardheirs) == 0

    # WHEN
    yao_owner.settle_owner()

    # THEN
    assert len(swim_plan.awardlinks) == 3
    assert len(swim_plan._awardheirs) == 3
    yao_owner.edit_plan_attr(swim_rope, awardlink_del=yao_str)
    assert len(swim_plan.awardlinks) == 2
    assert len(swim_plan._awardheirs) == 3

    # WHEN
    yao_owner.settle_owner()

    # THEN
    assert len(swim_plan.awardlinks) == 2
    assert len(swim_plan._awardheirs) == 2


def test_OwnerUnit_get_plan_tree_ordered_rope_list_ReturnsObj():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    wk_str = "wkdays"
    assert sue_owner.get_plan_tree_ordered_rope_list()

    # WHEN
    ordered_label_list = sue_owner.get_plan_tree_ordered_rope_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_rope_in_ordered_list = sue_owner.get_plan_tree_ordered_rope_list()[0]
    root_rope = to_rope(sue_owner.belief_label)
    assert x_1st_rope_in_ordered_list == root_rope
    x_8th_rope_in_ordered_list = sue_owner.get_plan_tree_ordered_rope_list()[9]
    assert x_8th_rope_in_ordered_list == sue_owner.make_l1_rope(wk_str)

    # WHEN
    y_owner = ownerunit_shop(belief_label="amy23")

    # THEN
    y_1st_rope_in_ordered_list = y_owner.get_plan_tree_ordered_rope_list()[0]
    assert y_1st_rope_in_ordered_list == root_rope


def test_OwnerUnit_get_plan_tree_ordered_rope_list_CorrectlyCleansRangedPlanRopeTerms():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_rope = yao_owner.make_l1_rope(time_str)
    yao_owner.set_l1_plan(planunit_shop(time_str, begin=0, close=700))
    wks_str = "wks"
    yao_owner.set_plan(planunit_shop(wks_str, denom=7), time_rope)

    # THEN
    assert len(yao_owner.get_plan_tree_ordered_rope_list()) == 3
    assert (
        len(yao_owner.get_plan_tree_ordered_rope_list(no_range_descendants=True)) == 2
    )


def test_OwnerUnit_get_plan_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    texas_str = "Texas"
    sue_owner.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_owner.set_l1_plan(planunit_shop(casa_str))

    # WHEN
    problems_dict = sue_owner.get_plan_dict(problem=True)

    # THEN
    assert sue_owner._keeps_justified
    texas_rope = sue_owner.make_l1_rope(texas_str)
    texas_plan = sue_owner.get_plan_obj(texas_rope)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_rope: texas_plan}


def test_OwnerUnit_settle_owner_CreatesFullyPopulated_plan_dict():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    assert len(sue_ownerunit._plan_dict) == 17


def test_OwnerUnit_settle_owner_Resets_offtrack_kids_mass_set():
    # ESTABLISH
    sue_ownerunit = ownerunit_shop("Sue")
    sue_ownerunit._offtrack_kids_mass_set = set("ZZ")
    x_set = set()

    assert sue_ownerunit._offtrack_kids_mass_set != x_set

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    assert sue_ownerunit._offtrack_kids_mass_set == x_set


def test_OwnerUnit_settle_owner_WhenPlanRootHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set_Scenario0():
    # ESTABLISH
    sue_ownerunit = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    casa_plan = planunit_shop(casa_str, mass=0)
    sue_ownerunit.set_l1_plan(casa_plan)
    assert sue_ownerunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    root_rope = to_rope(sue_ownerunit.belief_label)
    assert sue_ownerunit._offtrack_kids_mass_set == {root_rope}

    # WHEN
    sue_ownerunit.edit_plan_attr(casa_rope, mass=2)
    sue_ownerunit.settle_owner()

    # THEN
    assert sue_ownerunit._offtrack_kids_mass_set == set()


def test_OwnerUnit_settle_owner_WhenPlanUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_ownerunit = ownerunit_shop("Sue")
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

    assert sue_ownerunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    assert sue_ownerunit._offtrack_kids_mass_set == {clean_rope}


def test_OwnerUnit_settle_owner_CreatesNewGroupUnitsWhenNeeded_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    zia_str = "Zia"
    yao_acct_cred_points = 3
    yao_acct_debt_points = 2
    zia_acct_cred_points = 4
    zia_acct_debt_points = 5
    yao_owner.add_acctunit(yao_str, yao_acct_cred_points, yao_acct_debt_points)
    yao_owner.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    root_rope = to_rope(yao_owner.belief_label)
    x_planroot = yao_owner.get_plan_obj(root_rope)
    x_planroot.set_awardlink(awardlink_shop(yao_str))
    x_planroot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_planroot.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_owner.get_acctunit_group_titles_dict()) == 2
    assert not yao_owner.groupunit_exists(yao_str)
    assert not yao_owner.groupunit_exists(zia_str)
    assert not yao_owner.groupunit_exists(xio_str)

    # WHEN
    yao_owner.settle_owner()

    # THEN
    assert yao_owner.groupunit_exists(yao_str)
    assert yao_owner.groupunit_exists(zia_str)
    assert yao_owner.groupunit_exists(xio_str)
    assert len(yao_owner.get_acctunit_group_titles_dict()) == 2
    assert len(yao_owner.get_acctunit_group_titles_dict()) != len(yao_owner._groupunits)
    assert len(yao_owner._groupunits) == 3
    xio_groupunit = yao_owner.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_owner.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)
    yao_membership = xio_groupunit.get_membership(yao_str)
    zia_membership = xio_groupunit.get_membership(zia_str)
    assert yao_membership.group_cred_points == yao_acct_cred_points
    assert zia_membership.group_cred_points == zia_acct_cred_points
    assert yao_membership.group_debt_points == yao_acct_debt_points
    assert zia_membership.group_debt_points == zia_acct_debt_points


def test_OwnerUnit_settle_owner_CreatesNewGroupUnitsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_owner.make_l1_rope(swim_str)
    yao_owner.set_l1_plan(planunit_shop(swim_str))
    zia_str = "Zia"
    yao_owner.add_acctunit(yao_str)
    yao_owner.add_acctunit(zia_str)
    swim_plan = yao_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(awardlink_shop(yao_str))
    swim_plan.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_plan.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_owner.get_acctunit_group_titles_dict()) == 2
    assert not yao_owner.groupunit_exists(yao_str)
    assert not yao_owner.groupunit_exists(zia_str)
    assert not yao_owner.groupunit_exists(xio_str)

    # WHEN
    yao_owner.settle_owner()

    # THEN
    assert yao_owner.groupunit_exists(yao_str)
    assert yao_owner.groupunit_exists(zia_str)
    assert yao_owner.groupunit_exists(xio_str)
    assert len(yao_owner.get_acctunit_group_titles_dict()) == 2
    assert len(yao_owner.get_acctunit_group_titles_dict()) != len(yao_owner._groupunits)
    assert len(yao_owner._groupunits) == 3
    xio_groupunit = yao_owner.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_owner.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)


def test_OwnerUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_owner.make_l1_rope(swim_str)
    yao_owner.set_l1_plan(planunit_shop(swim_str))
    zia_str = "Zia"
    yao_owner.add_acctunit(yao_str)
    yao_owner.add_acctunit(zia_str)
    swim_plan = yao_owner.get_plan_obj(swim_rope)
    swim_plan.set_awardlink(awardlink_shop(yao_str))
    swim_plan.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_plan.set_awardlink(awardlink_shop(xio_str))
    yao_owner.settle_owner()
    assert yao_owner.groupunit_exists(yao_str)
    assert yao_owner.groupunit_exists(zia_str)
    assert yao_owner.groupunit_exists(xio_str)
    assert len(yao_owner.get_acctunit_group_titles_dict()) == 2
    assert len(yao_owner.get_acctunit_group_titles_dict()) != len(yao_owner._groupunits)

    # WHEN
    symmerty_group_titles = yao_owner.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_plan.set_awardlink(awardlink_shop(run_str))
    assert not yao_owner.groupunit_exists(run_str)
    yao_owner.settle_owner()
    assert yao_owner.groupunit_exists(run_str)

    # WHEN
    symmerty_group_titles = yao_owner.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {xio_str, run_str}


def test_OwnerUnit_settle_owner_Sets_planroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_owner.make_l1_rope(wk_str)
    wk_addin = 10
    wk_plan = planunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_owner.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_owner.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_owner.set_plan(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    root_rope = to_rope(yao_owner.belief_label)
    yao_owner.edit_plan_attr(
        root_rope, reason_rcontext=tue_rope, reason_premise=tue_rope
    )

    wk_popen = 3
    wk_pnigh = 7
    yao_owner.add_fact(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # assert len(ball_plan._reasonheirs) == 1
    # assert ball_plan._factheirs == {wk_rope: wk_factheir}
    # assert ball_plan._factheirs.get(wk_rope)
    # assert len(ball_plan._factheirs) == 1
    # assert ball_plan._factheirs.get(tue_rope) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_owner.settle_owner()
    exception_str = f"Cannot have fact for range inheritor '{tue_rope}'. A ranged fact plan must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_owner_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_owner_plan_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_rope: wk_rope}
    # wk_factheir = factheir_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # tue_popen = 113
    # tue_pnigh = 117
    # tue_factheir = factheir_shop(tue_rope, tue_rope, tue_popen, tue_pnigh)
    # root_plan = yao_owner.get_plan_obj(root_rope)
    # print(f"{wk_rope=} {root_plan._factheirs.keys()=}")
    # assert root_plan._factheirs.get(wk_rope) == wk_factheir
    # assert len(root_plan._factheirs) == 2
    # assert root_plan._factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_OwnerUnit_settle_owner_SetsPlanUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_owner.make_l1_rope(wk_str)
    wk_addin = 10
    wk_plan = planunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_owner.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_owner.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_owner.set_plan(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    ball_str = "ball"
    ball_rope = yao_owner.make_l1_rope(ball_str)
    yao_owner.set_l1_plan(planunit_shop(ball_str))
    yao_owner.edit_plan_attr(
        ball_rope, reason_rcontext=tue_rope, reason_premise=tue_rope
    )

    wk_popen = 3
    wk_pnigh = 7
    yao_owner.add_fact(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # assert len(ball_plan._reasonheirs) == 1
    # assert ball_plan._factheirs == {wk_rope: wk_factheir}
    # assert ball_plan._factheirs.get(wk_rope)
    # assert len(ball_plan._factheirs) == 1
    # assert ball_plan._factheirs.get(tue_rope) is None

    # WHEN
    yao_owner.settle_owner()

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_owner_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_owner_plan_dict, tue_reasonheirs)
    x_range_inheritors = {tue_rope: wk_rope}
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)

    tue_popen = 113
    tue_pnigh = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_popen, tue_pnigh)
    ball_plan = yao_owner.get_plan_obj(ball_rope)
    print(f"{wk_rope=} {ball_plan._factheirs.keys()=}")
    assert ball_plan._factheirs.get(wk_rope) == wk_factheir
    assert len(ball_plan._factheirs) == 2
    assert ball_plan._factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}
