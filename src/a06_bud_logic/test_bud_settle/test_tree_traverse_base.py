from src.a01_way_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_idea import factheir_shop
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from pytest import raises as pytest_raises


def test_BudUnit_clear_idea_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_idea_dict = {1: 2, 2: 4}
    sue_bud._rational = x_rational
    sue_bud._tree_traverse_count = x_tree_traverse_count
    sue_bud._idea_dict = x_idea_dict
    sue_bud._offtrack_kids_mass_set = "example"
    sue_bud._reason_contexts = {"example2"}
    sue_bud._range_inheritors = {"example2": 1}
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._idea_dict == x_idea_dict
    assert sue_bud._offtrack_kids_mass_set != set()
    assert sue_bud._reason_contexts != set()
    assert sue_bud._range_inheritors != {}

    # WHEN
    sue_bud._clear_idea_dict_and_bud_obj_settle_attrs()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._idea_dict != x_idea_dict
    assert sue_bud._idea_dict == {sue_bud.idearoot.get_idea_way(): sue_bud.idearoot}
    assert sue_bud._offtrack_kids_mass_set == set()
    assert not sue_bud._reason_contexts
    assert not sue_bud._range_inheritors


def test_BudUnit_clear_idea_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerlink_share = 140
    sue_bud._keeps_justified = x_keep_justifed
    sue_bud._keeps_buildable = "swimmers"
    sue_bud._sum_healerlink_share = x_sum_healerlink_share
    sue_bud._keep_dict = {"run": "run"}
    sue_bud._healers_dict = {"run": "run"}
    assert sue_bud._keeps_justified == x_keep_justifed
    assert sue_bud._keeps_buildable
    assert sue_bud._sum_healerlink_share == x_sum_healerlink_share
    assert sue_bud._keep_dict != {}
    assert sue_bud._healers_dict != {}

    # WHEN
    sue_bud._clear_idea_dict_and_bud_obj_settle_attrs()

    # THEN
    assert sue_bud._keeps_justified != x_keep_justifed
    assert sue_bud._keeps_justified
    assert sue_bud._keeps_buildable is False
    assert sue_bud._sum_healerlink_share == 0
    assert not sue_bud._keep_dict
    assert not sue_bud._healers_dict


def test_BudUnit_settle_bud_ClearsDescendantAttributes():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    # test root status:
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    casa_idea = sue_bud.get_idea_obj(casa_way)
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(week_way, mon_str)
    mon_idea = sue_bud.get_idea_obj(mon_way)
    assert sue_bud.idearoot._descendant_pledge_count is None
    assert sue_bud.idearoot._all_acct_cred is None
    assert sue_bud.idearoot._all_acct_debt is None
    assert casa_idea._descendant_pledge_count is None
    assert casa_idea._all_acct_cred is None
    assert casa_idea._all_acct_debt is None
    assert mon_idea._descendant_pledge_count is None
    assert mon_idea._all_acct_cred is None
    assert mon_idea._all_acct_debt is None

    sue_bud.idearoot._descendant_pledge_count = -2
    sue_bud.idearoot._all_acct_cred = -2
    sue_bud.idearoot._all_acct_debt = -2
    casa_idea._descendant_pledge_count = -2
    casa_idea._all_acct_cred = -2
    casa_idea._all_acct_debt = -2
    mon_idea._descendant_pledge_count = -2
    mon_idea._all_acct_cred = -2
    mon_idea._all_acct_debt = -2

    assert sue_bud.idearoot._descendant_pledge_count == -2
    assert sue_bud.idearoot._all_acct_cred == -2
    assert sue_bud.idearoot._all_acct_debt == -2
    assert casa_idea._descendant_pledge_count == -2
    assert casa_idea._all_acct_cred == -2
    assert casa_idea._all_acct_debt == -2
    assert mon_idea._descendant_pledge_count == -2
    assert mon_idea._all_acct_cred == -2
    assert mon_idea._all_acct_debt == -2

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud.idearoot._descendant_pledge_count == 2
    assert casa_idea._descendant_pledge_count == 0
    assert mon_idea._descendant_pledge_count == 0

    assert mon_idea._all_acct_cred is True
    assert mon_idea._all_acct_debt is True
    assert casa_idea._all_acct_cred is True
    assert casa_idea._all_acct_debt is True
    assert sue_bud.idearoot._all_acct_cred is True
    assert sue_bud.idearoot._all_acct_debt is True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_bud = budunit_shop(owner_name="Yao")
    assert yao_bud.idearoot._descendant_pledge_count is None
    assert yao_bud.idearoot._all_acct_cred is None
    assert yao_bud.idearoot._all_acct_debt is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.idearoot._descendant_pledge_count == 0
    assert yao_bud.idearoot._all_acct_cred is True
    assert yao_bud.idearoot._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    casa_idea = sue_bud.get_idea_obj(casa_way)
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    week_idea = sue_bud.get_idea_obj(week_way)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(week_way, mon_str)
    mon_idea = sue_bud.get_idea_obj(mon_way)

    email_str = "email"
    email_idea = ideaunit_shop(email_str, pledge=True)
    sue_bud.set_idea(email_idea, parent_way=casa_way)

    # test root status:
    root_way = to_way(sue_bud.fisc_tag)
    x_idearoot = sue_bud.get_idea_obj(root_way)
    assert x_idearoot._descendant_pledge_count is None
    assert x_idearoot._all_acct_cred is None
    assert x_idearoot._all_acct_debt is None
    assert casa_idea._descendant_pledge_count is None
    assert casa_idea._all_acct_cred is None
    assert casa_idea._all_acct_debt is None
    assert mon_idea._descendant_pledge_count is None
    assert mon_idea._all_acct_cred is None
    assert mon_idea._all_acct_debt is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert x_idearoot._descendant_pledge_count == 3
    assert casa_idea._descendant_pledge_count == 1
    assert casa_idea._kids[email_str]._descendant_pledge_count == 0
    assert mon_idea._descendant_pledge_count == 0
    assert x_idearoot._all_acct_cred is True
    assert x_idearoot._all_acct_debt is True
    assert casa_idea._all_acct_cred is True
    assert casa_idea._all_acct_debt is True
    assert mon_idea._all_acct_cred is True
    assert mon_idea._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    email_str = "email"
    casa_str = "casa"
    week_str = "weekdays"
    mon_str = "Monday"
    tue_str = "Tuesday"
    vacuum_str = "vacuum"
    sue_str = "Sue"

    casa_way = sue_bud.make_l1_way(casa_str)
    email_idea = ideaunit_shop(email_str, pledge=True)
    sue_bud.set_idea(email_idea, parent_way=casa_way)
    vacuum_idea = ideaunit_shop(vacuum_str, pledge=True)
    sue_bud.set_idea(vacuum_idea, parent_way=casa_way)

    sue_bud.add_acctunit(acct_name=sue_str)
    x_awardlink = awardlink_shop(awardee_label=sue_str)

    sue_bud.idearoot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_bud.settle_bud()
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_bud.idearoot._all_acct_cred is False
    assert sue_bud.idearoot._all_acct_debt is False
    casa_idea = sue_bud.idearoot._kids[casa_str]
    assert casa_idea._all_acct_cred is False
    assert casa_idea._all_acct_debt is False
    assert casa_idea._kids[email_str]._all_acct_cred is False
    assert casa_idea._kids[email_str]._all_acct_debt is False
    assert casa_idea._kids[vacuum_str]._all_acct_cred is True
    assert casa_idea._kids[vacuum_str]._all_acct_debt is True
    week_idea = sue_bud.idearoot._kids[week_str]
    assert week_idea._all_acct_cred is True
    assert week_idea._all_acct_debt is True
    assert week_idea._kids[mon_str]._all_acct_cred is True
    assert week_idea._kids[mon_str]._all_acct_debt is True
    assert week_idea._kids[tue_str]._all_acct_cred is True
    assert week_idea._kids[tue_str]._all_acct_debt is True


def test_BudUnit_settle_bud_SetsIdeaUnitAttr_awardlinks():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.add_acctunit(Xio_str)

    assert len(sue_bud.accts) == 3
    assert len(sue_bud.get_acctunit_group_labels_dict()) == 3
    swim_str = "swim"
    sue_bud.set_l1_idea(ideaunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_way = sue_bud.make_l1_way(swim_str)
    sue_bud.edit_idea_attr(swim_way, awardlink=awardlink_yao)
    sue_bud.edit_idea_attr(swim_way, awardlink=awardlink_zia)
    sue_bud.edit_idea_attr(swim_way, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_bud.set_idea(ideaunit_shop(street_str), parent_way=swim_way)
    assert sue_bud.idearoot.awardlinks in (None, {})
    assert len(sue_bud.idearoot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._idea_dict.keys()=} ")
    swim_idea = sue_bud._idea_dict.get(swim_way)
    street_idea = sue_bud._idea_dict.get(sue_bud.make_way(swim_way, street_str))

    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea.awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(sue_bud._idea_dict)}")
    print(f"{swim_idea.awardlinks}")
    print(f"{swim_idea._awardheirs}")
    print(f"{swim_idea._awardheirs}")
    assert len(sue_bud.idearoot._kids["swim"]._awardheirs) == 3


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # idea tree has no awardlinks
    assert sue_bud.idearoot._awardlines == {}
    sue_bud.idearoot._awardlines = {1: "testtest"}
    assert sue_bud.idearoot._awardlines != {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.idearoot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_idea = sue_bud.idearoot._kids[casa_str]
    casa_idea._awardlines = {1: "testtest"}
    assert casa_idea._awardlines != {}
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.idearoot._kids[casa_str]._awardlines


def test_BudUnit_settle_bud_DoesNotKeepUnbranched_awardheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    yao_bud.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)

    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_idea = yao_bud.get_idea_obj(swim_way)
    yao_bud.edit_idea_attr(swim_way, awardlink=awardlink_yao)
    yao_bud.edit_idea_attr(swim_way, awardlink=awardlink_zia)
    yao_bud.edit_idea_attr(swim_way, awardlink=awardlink_Xio)

    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    yao_bud.edit_idea_attr(swim_way, awardlink_del=yao_str)
    assert len(swim_idea.awardlinks) == 2
    assert len(swim_idea._awardheirs) == 3

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea.awardlinks) == 2
    assert len(swim_idea._awardheirs) == 2


def test_BudUnit_get_idea_tree_ordered_way_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    assert sue_bud.get_idea_tree_ordered_way_list()

    # WHEN
    ordered_tag_list = sue_bud.get_idea_tree_ordered_way_list()

    # THEN
    assert len(ordered_tag_list) == 17
    x_1st_way_in_ordered_list = sue_bud.get_idea_tree_ordered_way_list()[0]
    root_way = to_way(sue_bud.fisc_tag)
    assert x_1st_way_in_ordered_list == root_way
    x_8th_way_in_ordered_list = sue_bud.get_idea_tree_ordered_way_list()[9]
    assert x_8th_way_in_ordered_list == sue_bud.make_l1_way(week_str)

    # WHEN
    y_bud = budunit_shop()

    # THEN
    y_1st_way_in_ordered_list = y_bud.get_idea_tree_ordered_way_list()[0]
    assert y_1st_way_in_ordered_list == root_way


def test_BudUnit_get_idea_tree_ordered_way_list_CorrectlyCleansRangedIdeaWayStrs():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_way = yao_bud.make_l1_way(time_str)
    yao_bud.set_l1_idea(ideaunit_shop(time_str, begin=0, close=700))
    weeks_str = "weeks"
    yao_bud.set_idea(ideaunit_shop(weeks_str, denom=7), time_way)

    # THEN
    assert len(yao_bud.get_idea_tree_ordered_way_list()) == 3
    assert len(yao_bud.get_idea_tree_ordered_way_list(no_range_descendants=True)) == 2


def test_BudUnit_get_idea_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    sue_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_bud.set_l1_idea(ideaunit_shop(casa_str))

    # WHEN
    problems_dict = sue_bud.get_idea_dict(problem=True)

    # THEN
    assert sue_bud._keeps_justified
    texas_way = sue_bud.make_l1_way(texas_str)
    texas_idea = sue_bud.get_idea_obj(texas_way)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_way: texas_idea}


def test_BudUnit_settle_bud_CreatesFullyPopulated_idea_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._idea_dict) == 17


def test_BudUnit_settle_bud_Resets_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    sue_budunit._offtrack_kids_mass_set = set("ZZ")
    x_set = set()

    assert sue_budunit._offtrack_kids_mass_set != x_set

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == x_set


def test_BudUnit_settle_bud_WhenIdeaRootHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_idea = ideaunit_shop(casa_str, mass=0)
    sue_budunit.set_l1_idea(casa_idea)
    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    root_way = to_way(sue_budunit.fisc_tag)
    assert sue_budunit._offtrack_kids_mass_set == {root_way}

    # WHEN
    sue_budunit.edit_idea_attr(casa_way, mass=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == set()


def test_BudUnit_settle_bud_WhenIdeaUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_idea = ideaunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_way = sue_budunit.make_way(casa_way, swim_str)
    swim_idea = ideaunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_way = sue_budunit.make_way(casa_way, clean_str)
    clean_idea = ideaunit_shop(clean_str, mass=2)
    sue_budunit.set_idea(ideaunit_shop(clean_str), casa_way)

    sweep_str = "sweep"
    sweep_way = sue_budunit.make_way(clean_way, sweep_str)
    sweep_idea = ideaunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_way = sue_budunit.make_way(clean_way, vaccum_str)
    vaccum_idea = ideaunit_shop(vaccum_str, mass=0)

    sue_budunit.set_l1_idea(casa_idea)
    sue_budunit.set_idea(swim_idea, casa_way)
    sue_budunit.set_idea(clean_idea, casa_way)
    sue_budunit.set_idea(sweep_idea, clean_way)  # _mass=0
    sue_budunit.set_idea(vaccum_idea, clean_way)  # _mass=0

    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == {clean_way}


def test_BudUnit_settle_bud_CreatesNewGroupUnitsWhenBranched_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    yao_credit_belief = 3
    yao_debtit_belief = 2
    zia_credit_belief = 4
    zia_debtit_belief = 5
    yao_bud.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    yao_bud.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    root_way = to_way(yao_bud.fisc_tag)
    x_idearoot = yao_bud.get_idea_obj(root_way)
    x_idearoot.set_awardlink(awardlink_shop(yao_str))
    x_idearoot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_idearoot.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_labels_dict()) == 2
    assert not yao_bud.groupunit_exists(yao_str)
    assert not yao_bud.groupunit_exists(zia_str)
    assert not yao_bud.groupunit_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_labels_dict()) == 2
    assert len(yao_bud.get_acctunit_group_labels_dict()) != len(yao_bud._groupunits)
    assert len(yao_bud._groupunits) == 3
    xio_groupunit = yao_bud.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_bud.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)
    yao_membership = xio_groupunit.get_membership(yao_str)
    zia_membership = xio_groupunit.get_membership(zia_str)
    assert yao_membership.credit_vote == yao_credit_belief
    assert zia_membership.credit_vote == zia_credit_belief
    assert yao_membership.debtit_vote == yao_debtit_belief
    assert zia_membership.debtit_vote == zia_debtit_belief


def test_BudUnit_settle_bud_CreatesNewGroupUnitsWhenBranched_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_idea = yao_bud.get_idea_obj(swim_way)
    swim_idea.set_awardlink(awardlink_shop(yao_str))
    swim_idea.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_labels_dict()) == 2
    assert not yao_bud.groupunit_exists(yao_str)
    assert not yao_bud.groupunit_exists(zia_str)
    assert not yao_bud.groupunit_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_labels_dict()) == 2
    assert len(yao_bud.get_acctunit_group_labels_dict()) != len(yao_bud._groupunits)
    assert len(yao_bud._groupunits) == 3
    xio_groupunit = yao_bud.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_bud.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)


def test_BudUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_idea = yao_bud.get_idea_obj(swim_way)
    swim_idea.set_awardlink(awardlink_shop(yao_str))
    swim_idea.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_str))
    yao_bud.settle_bud()
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_labels_dict()) == 2
    assert len(yao_bud.get_acctunit_group_labels_dict()) != len(yao_bud._groupunits)

    # WHEN
    symmerty_group_labels = yao_bud.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_labels) == 1
    assert symmerty_group_labels == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_idea.set_awardlink(awardlink_shop(run_str))
    assert not yao_bud.groupunit_exists(run_str)
    yao_bud.settle_bud()
    assert yao_bud.groupunit_exists(run_str)

    # WHEN
    symmerty_group_labels = yao_bud.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_labels) == 2
    assert symmerty_group_labels == {xio_str, run_str}


def test_BudUnit_settle_bud_Sets_idearoot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_way = yao_bud.make_l1_way(week_str)
    week_addin = 10
    week_idea = ideaunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(week_way, tue_str)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_str, addin=tue_addin), week_way)
    root_way = to_way(yao_bud.fisc_tag)
    yao_bud.edit_idea_attr(root_way, reason_context=tue_way, reason_premise=tue_way)

    week_open = 3
    week_nigh = 7
    yao_bud.add_fact(week_way, week_way, week_open, week_nigh)

    # assert len(ball_idea._reasonheirs) == 1
    # assert ball_idea._factheirs == {week_way: week_factheir}
    # assert ball_idea._factheirs.get(week_way)
    # assert len(ball_idea._factheirs) == 1
    # assert ball_idea._factheirs.get(tue_way) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.settle_bud()
    exception_str = f"Cannot have fact for range inheritor '{tue_way}'. A ranged fact idea must have _begin, _close attributes"
    assert str(excinfo.value) == exception_str

    # THEN
    # week_factunit = factunit_shop(week_way, week_way, week_open, week_nigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_idea_dict = {week_idea.get_idea_way(): week_idea, tue_idea.get_idea_way(): tue_idea}
    # ball_idea.set_reasonheirs(x_bud_idea_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_way: week_way}
    # week_factheir = factheir_shop(week_way, week_way, week_open, week_nigh)

    # tue_open = 113
    # tue_nigh = 117
    # tue_factheir = factheir_shop(tue_way, tue_way, tue_open, tue_nigh)
    # root_idea = yao_bud.get_idea_obj(root_way)
    # print(f"{week_way=} {root_idea._factheirs.keys()=}")
    # assert root_idea._factheirs.get(week_way) == week_factheir
    # assert len(root_idea._factheirs) == 2
    # assert root_idea._factheirs == {tue_way: tue_factheir, week_way: week_factheir}


def test_BudUnit_settle_bud_SetsIdeaUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_way = yao_bud.make_l1_way(week_str)
    week_addin = 10
    week_idea = ideaunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(week_way, tue_str)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_str, addin=tue_addin), week_way)
    ball_str = "ball"
    ball_way = yao_bud.make_l1_way(ball_str)
    yao_bud.set_l1_idea(ideaunit_shop(ball_str))
    yao_bud.edit_idea_attr(ball_way, reason_context=tue_way, reason_premise=tue_way)

    week_open = 3
    week_nigh = 7
    yao_bud.add_fact(week_way, week_way, week_open, week_nigh)

    # assert len(ball_idea._reasonheirs) == 1
    # assert ball_idea._factheirs == {week_way: week_factheir}
    # assert ball_idea._factheirs.get(week_way)
    # assert len(ball_idea._factheirs) == 1
    # assert ball_idea._factheirs.get(tue_way) is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    # week_factunit = factunit_shop(week_way, week_way, week_open, week_nigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_idea_dict = {week_idea.get_idea_way(): week_idea, tue_idea.get_idea_way(): tue_idea}
    # ball_idea.set_reasonheirs(x_bud_idea_dict, tue_reasonheirs)
    x_range_inheritors = {tue_way: week_way}
    week_factheir = factheir_shop(week_way, week_way, week_open, week_nigh)

    tue_open = 113
    tue_nigh = 117
    tue_factheir = factheir_shop(tue_way, tue_way, tue_open, tue_nigh)
    ball_idea = yao_bud.get_idea_obj(ball_way)
    print(f"{week_way=} {ball_idea._factheirs.keys()=}")
    assert ball_idea._factheirs.get(week_way) == week_factheir
    assert len(ball_idea._factheirs) == 2
    assert ball_idea._factheirs == {tue_way: tue_factheir, week_way: week_factheir}
