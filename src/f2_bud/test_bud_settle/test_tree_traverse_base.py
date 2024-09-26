from src.f2_bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from src.f2_bud.group import awardlink_shop
from src.f2_bud.reason_idea import factheir_shop
from src.f2_bud.idea import ideaunit_shop
from src.f2_bud.bud import budunit_shop
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
    sue_bud._reason_bases = {"example2"}
    sue_bud._range_inheritors = {"example2": 1}
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._idea_dict == x_idea_dict
    assert sue_bud._offtrack_kids_mass_set != set()
    assert sue_bud._reason_bases != set()
    assert sue_bud._range_inheritors != {}

    # WHEN
    sue_bud._clear_idea_dict_and_bud_obj_settle_attrs()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._idea_dict != x_idea_dict
    assert sue_bud._idea_dict == {sue_bud._idearoot.get_road(): sue_bud._idearoot}
    assert sue_bud._offtrack_kids_mass_set == set()
    assert sue_bud._reason_bases == set()
    assert sue_bud._range_inheritors == {}


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
    casa_road = sue_bud.make_l1_road(casa_str)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    mon_str = "Monday"
    mon_road = sue_bud.make_road(week_road, mon_str)
    mon_idea = sue_bud.get_idea_obj(mon_road)
    assert sue_bud._idearoot._descendant_pledge_count is None
    assert sue_bud._idearoot._all_acct_cred is None
    assert sue_bud._idearoot._all_acct_debt is None
    assert casa_idea._descendant_pledge_count is None
    assert casa_idea._all_acct_cred is None
    assert casa_idea._all_acct_debt is None
    assert mon_idea._descendant_pledge_count is None
    assert mon_idea._all_acct_cred is None
    assert mon_idea._all_acct_debt is None

    sue_bud._idearoot._descendant_pledge_count = -2
    sue_bud._idearoot._all_acct_cred = -2
    sue_bud._idearoot._all_acct_debt = -2
    casa_idea._descendant_pledge_count = -2
    casa_idea._all_acct_cred = -2
    casa_idea._all_acct_debt = -2
    mon_idea._descendant_pledge_count = -2
    mon_idea._all_acct_cred = -2
    mon_idea._all_acct_debt = -2

    assert sue_bud._idearoot._descendant_pledge_count == -2
    assert sue_bud._idearoot._all_acct_cred == -2
    assert sue_bud._idearoot._all_acct_debt == -2
    assert casa_idea._descendant_pledge_count == -2
    assert casa_idea._all_acct_cred == -2
    assert casa_idea._all_acct_debt == -2
    assert mon_idea._descendant_pledge_count == -2
    assert mon_idea._all_acct_cred == -2
    assert mon_idea._all_acct_debt == -2

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._idearoot._descendant_pledge_count == 2
    assert casa_idea._descendant_pledge_count == 0
    assert mon_idea._descendant_pledge_count == 0

    assert mon_idea._all_acct_cred is True
    assert mon_idea._all_acct_debt is True
    assert casa_idea._all_acct_cred is True
    assert casa_idea._all_acct_debt is True
    assert sue_bud._idearoot._all_acct_cred is True
    assert sue_bud._idearoot._all_acct_debt is True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_bud = budunit_shop(_owner_id="Yao")
    assert yao_bud._idearoot._descendant_pledge_count is None
    assert yao_bud._idearoot._all_acct_cred is None
    assert yao_bud._idearoot._all_acct_debt is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud._idearoot._descendant_pledge_count == 0
    assert yao_bud._idearoot._all_acct_cred is True
    assert yao_bud._idearoot._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    week_idea = sue_bud.get_idea_obj(week_road)
    mon_str = "Monday"
    mon_road = sue_bud.make_road(week_road, mon_str)
    mon_idea = sue_bud.get_idea_obj(mon_road)

    email_str = "email"
    email_idea = ideaunit_shop(email_str, pledge=True)
    sue_bud.set_idea(email_idea, parent_road=casa_road)

    # test root status:
    x_idearoot = sue_bud.get_idea_obj(sue_bud._fiscal_id)
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

    casa_road = sue_bud.make_l1_road(casa_str)
    email_idea = ideaunit_shop(email_str, pledge=True)
    sue_bud.set_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(vacuum_str, pledge=True)
    sue_bud.set_idea(vacuum_idea, parent_road=casa_road)

    sue_bud.add_acctunit(acct_id=sue_str)
    x_awardlink = awardlink_shop(group_id=sue_str)

    sue_bud._idearoot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_bud.settle_bud()
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_bud._idearoot._all_acct_cred is False
    assert sue_bud._idearoot._all_acct_debt is False
    casa_idea = sue_bud._idearoot._kids[casa_str]
    assert casa_idea._all_acct_cred is False
    assert casa_idea._all_acct_debt is False
    assert casa_idea._kids[email_str]._all_acct_cred is False
    assert casa_idea._kids[email_str]._all_acct_debt is False
    assert casa_idea._kids[vacuum_str]._all_acct_cred is True
    assert casa_idea._kids[vacuum_str]._all_acct_debt is True
    week_idea = sue_bud._idearoot._kids[week_str]
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

    assert len(sue_bud._accts) == 3
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 3
    swim_str = "swim"
    sue_bud.set_l1_idea(ideaunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_road = sue_bud.make_l1_road(swim_str)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_bud.set_idea(ideaunit_shop(street_str), parent_road=swim_road)
    assert sue_bud._idearoot.awardlinks in (None, {})
    assert len(sue_bud._idearoot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._idea_dict.keys()=} ")
    swim_idea = sue_bud._idea_dict.get(swim_road)
    street_idea = sue_bud._idea_dict.get(sue_bud.make_road(swim_road, street_str))

    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea.awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(sue_bud._idea_dict)}")
    print(f"{swim_idea.awardlinks}")
    print(f"{swim_idea._awardheirs}")
    print(f"{swim_idea._awardheirs}")
    assert len(sue_bud._idearoot._kids["swim"]._awardheirs) == 3


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # idea tree has no awardlinks
    assert sue_bud._idearoot._awardlines == {}
    sue_bud._idearoot._awardlines = {1: "testtest"}
    assert sue_bud._idearoot._awardlines != {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud._idearoot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_idea = sue_bud._idearoot._kids[casa_str]
    casa_idea._awardlines = {1: "testtest"}
    assert casa_idea._awardlines != {}
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud._idearoot._kids[casa_str]._awardlines


def test_BudUnit_settle_bud_DoesNotKeepUnneeded_awardheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    yao_bud.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_road = yao_bud.make_l1_road(swim_str)

    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_idea = yao_bud.get_idea_obj(swim_road)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea.awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    yao_bud.edit_idea_attr(swim_road, awardlink_del=yao_str)
    assert len(swim_idea.awardlinks) == 2
    assert len(swim_idea._awardheirs) == 3

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea.awardlinks) == 2
    assert len(swim_idea._awardheirs) == 2


def test_BudUnit_get_idea_tree_ordered_road_list_ReturnsCorrectObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    assert sue_bud.get_idea_tree_ordered_road_list()

    # WHEN
    ordered_node_list = sue_bud.get_idea_tree_ordered_road_list()

    # THEN
    assert len(ordered_node_list) == 17
    x_1st_road_in_ordered_list = sue_bud.get_idea_tree_ordered_road_list()[0]
    assert x_1st_road_in_ordered_list == sue_bud._fiscal_id
    x_8th_road_in_ordered_list = sue_bud.get_idea_tree_ordered_road_list()[9]
    assert x_8th_road_in_ordered_list == sue_bud.make_l1_road(week_str)

    # WHEN
    y_bud = budunit_shop()

    # THEN
    y_1st_road_in_ordered_list = y_bud.get_idea_tree_ordered_road_list()[0]
    assert y_1st_road_in_ordered_list == sue_bud._fiscal_id


def test_BudUnit_get_idea_tree_ordered_road_list_CorrectlyFiltersRangedIdeaRoadUnits():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_road = yao_bud.make_l1_road(time_str)
    yao_bud.set_l1_idea(ideaunit_shop(time_str, begin=0, close=700))
    weeks_str = "weeks"
    yao_bud.set_idea(ideaunit_shop(weeks_str, denom=7), time_road)

    # THEN
    assert len(yao_bud.get_idea_tree_ordered_road_list()) == 3
    assert len(yao_bud.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_BudUnit_get_idea_dict_ReturnsCorrectObjWhenSingle():
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
    texas_road = sue_bud.make_l1_road(texas_str)
    texas_idea = sue_bud.get_idea_obj(texas_road)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_road: texas_idea}


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
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_idea = ideaunit_shop(casa_str, mass=0)
    sue_budunit.set_l1_idea(casa_idea)
    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == {sue_budunit._fiscal_id}

    # WHEN
    sue_budunit.edit_idea_attr(casa_road, mass=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == set()


def test_BudUnit_settle_bud_WhenIdeaUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_idea = ideaunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_road = sue_budunit.make_road(casa_road, swim_str)
    swim_idea = ideaunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_road = sue_budunit.make_road(casa_road, clean_str)
    clean_idea = ideaunit_shop(clean_str, mass=2)
    sue_budunit.set_idea(ideaunit_shop(clean_str), casa_road)

    sweep_str = "sweep"
    sweep_road = sue_budunit.make_road(clean_road, sweep_str)
    sweep_idea = ideaunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_road = sue_budunit.make_road(clean_road, vaccum_str)
    vaccum_idea = ideaunit_shop(vaccum_str, mass=0)

    sue_budunit.set_l1_idea(casa_idea)
    sue_budunit.set_idea(swim_idea, casa_road)
    sue_budunit.set_idea(clean_idea, casa_road)
    sue_budunit.set_idea(sweep_idea, clean_road)  # _mass=0
    sue_budunit.set_idea(vaccum_idea, clean_road)  # _mass=0

    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == {clean_road}


def test_BudUnit_settle_bud_CreatesNewGroupBoxsWhenNeeded_Scenario0():
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
    x_idearoot = yao_bud.get_idea_obj(yao_bud._fiscal_id)
    x_idearoot.set_awardlink(awardlink_shop(yao_str))
    x_idearoot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_idearoot.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert not yao_bud.groupbox_exists(yao_str)
    assert not yao_bud.groupbox_exists(zia_str)
    assert not yao_bud.groupbox_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupbox_exists(yao_str)
    assert yao_bud.groupbox_exists(zia_str)
    assert yao_bud.groupbox_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)
    assert len(yao_bud._groupboxs) == 3
    xio_groupbox = yao_bud.get_groupbox(xio_str)
    xio_symmerty_groupbox = yao_bud.create_symmetry_groupbox(xio_str)
    assert xio_groupbox._memberships.keys() == xio_symmerty_groupbox._memberships.keys()
    assert xio_groupbox.membership_exists(yao_str)
    assert xio_groupbox.membership_exists(zia_str)
    assert not xio_groupbox.membership_exists(xio_str)
    yao_membership = xio_groupbox.get_membership(yao_str)
    zia_membership = xio_groupbox.get_membership(zia_str)
    assert yao_membership.credit_vote == yao_credit_belief
    assert zia_membership.credit_vote == zia_credit_belief
    assert yao_membership.debtit_vote == yao_debtit_belief
    assert zia_membership.debtit_vote == zia_debtit_belief


def test_BudUnit_settle_bud_CreatesNewGroupBoxsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_road = yao_bud.make_l1_road(swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_str))
    swim_idea.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert not yao_bud.groupbox_exists(yao_str)
    assert not yao_bud.groupbox_exists(zia_str)
    assert not yao_bud.groupbox_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupbox_exists(yao_str)
    assert yao_bud.groupbox_exists(zia_str)
    assert yao_bud.groupbox_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)
    assert len(yao_bud._groupboxs) == 3
    xio_groupbox = yao_bud.get_groupbox(xio_str)
    xio_symmerty_groupbox = yao_bud.create_symmetry_groupbox(xio_str)
    assert xio_groupbox._memberships.keys() == xio_symmerty_groupbox._memberships.keys()
    assert xio_groupbox.membership_exists(yao_str)
    assert xio_groupbox.membership_exists(zia_str)
    assert not xio_groupbox.membership_exists(xio_str)


def test_BudUnit_get_tree_traverse_generated_groupboxs_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_road = yao_bud.make_l1_road(swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_str))
    swim_idea.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_str))
    yao_bud.settle_bud()
    assert yao_bud.groupbox_exists(yao_str)
    assert yao_bud.groupbox_exists(zia_str)
    assert yao_bud.groupbox_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)

    # WHEN
    symmerty_group_ids = yao_bud.get_tree_traverse_generated_groupboxs()

    # THEN
    assert len(symmerty_group_ids) == 1
    assert symmerty_group_ids == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_idea.set_awardlink(awardlink_shop(run_str))
    assert not yao_bud.groupbox_exists(run_str)
    yao_bud.settle_bud()
    assert yao_bud.groupbox_exists(run_str)

    # WHEN
    symmerty_group_ids = yao_bud.get_tree_traverse_generated_groupboxs()

    # THEN
    assert len(symmerty_group_ids) == 2
    assert symmerty_group_ids == {xio_str, run_str}


def test_BudUnit_settle_bud_Sets_idearoot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_road = yao_bud.make_l1_road(week_str)
    week_addin = 10
    week_idea = ideaunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_str = "Tue"
    tue_road = yao_bud.make_road(week_road, tue_str)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_str, addin=tue_addin), week_road)
    x_fiscal_id = yao_bud._fiscal_id
    yao_bud.edit_idea_attr(x_fiscal_id, reason_base=tue_road, reason_premise=tue_road)

    week_open = 3
    week_nigh = 7
    yao_bud.set_fact(week_road, week_road, week_open, week_nigh)

    # assert len(ball_idea._reasonheirs) == 1
    # assert ball_idea._factheirs == {week_road: week_factheir}
    # assert ball_idea._factheirs.get(week_road)
    # assert len(ball_idea._factheirs) == 1
    # assert ball_idea._factheirs.get(tue_road) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.settle_bud()
    exception_str = f"Cannot have fact for range inheritor '{tue_road}'. A ranged fact idea must have _begin, _close attributes"
    assert str(excinfo.value) == exception_str

    # THEN
    # week_factunit = factunit_shop(week_road, week_road, week_open, week_nigh)
    # tue_reasonheirs = {tue_road: reasonheir_shop(tue_road, None, False)}
    # x_bud_idea_dict = {week_idea.get_road(): week_idea, tue_idea.get_road(): tue_idea}
    # ball_idea.set_reasonheirs(x_bud_idea_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_road: week_road}
    # week_factheir = factheir_shop(week_road, week_road, week_open, week_nigh)

    # tue_open = 113
    # tue_nigh = 117
    # tue_factheir = factheir_shop(tue_road, tue_road, tue_open, tue_nigh)
    # root_idea = yao_bud.get_idea_obj(yao_bud._fiscal_id)
    # print(f"{week_road=} {root_idea._factheirs.keys()=}")
    # assert root_idea._factheirs.get(week_road) == week_factheir
    # assert len(root_idea._factheirs) == 2
    # assert root_idea._factheirs == {tue_road: tue_factheir, week_road: week_factheir}


def test_BudUnit_settle_bud_SetsIdeaUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_road = yao_bud.make_l1_road(week_str)
    week_addin = 10
    week_idea = ideaunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_str = "Tue"
    tue_road = yao_bud.make_road(week_road, tue_str)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_str, addin=tue_addin), week_road)
    ball_str = "ball"
    ball_road = yao_bud.make_l1_road(ball_str)
    yao_bud.set_l1_idea(ideaunit_shop(ball_str))
    yao_bud.edit_idea_attr(ball_road, reason_base=tue_road, reason_premise=tue_road)

    week_open = 3
    week_nigh = 7
    yao_bud.set_fact(week_road, week_road, week_open, week_nigh)

    # assert len(ball_idea._reasonheirs) == 1
    # assert ball_idea._factheirs == {week_road: week_factheir}
    # assert ball_idea._factheirs.get(week_road)
    # assert len(ball_idea._factheirs) == 1
    # assert ball_idea._factheirs.get(tue_road) is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    # week_factunit = factunit_shop(week_road, week_road, week_open, week_nigh)
    # tue_reasonheirs = {tue_road: reasonheir_shop(tue_road, None, False)}
    # x_bud_idea_dict = {week_idea.get_road(): week_idea, tue_idea.get_road(): tue_idea}
    # ball_idea.set_reasonheirs(x_bud_idea_dict, tue_reasonheirs)
    x_range_inheritors = {tue_road: week_road}
    week_factheir = factheir_shop(week_road, week_road, week_open, week_nigh)

    tue_open = 113
    tue_nigh = 117
    tue_factheir = factheir_shop(tue_road, tue_road, tue_open, tue_nigh)
    ball_idea = yao_bud.get_idea_obj(ball_road)
    print(f"{week_road=} {ball_idea._factheirs.keys()=}")
    assert ball_idea._factheirs.get(week_road) == week_factheir
    assert len(ball_idea._factheirs) == 2
    assert ball_idea._factheirs == {tue_road: tue_factheir, week_road: week_factheir}
