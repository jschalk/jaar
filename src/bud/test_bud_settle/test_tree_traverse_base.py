from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from src.bud.group import awardlink_shop
from src.bud.reason_idea import factunit_shop, factheir_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.bud.graphic import display_ideatree
from pytest import raises as pytest_raises


def test_BudUnit_clear_settle_attrs_CorrectlySetsAttrs():
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
    sue_bud._clear_settle_attrs()

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


def test_BudUnit_pre_tree_traverse_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_econ_justifed = False
    x_sum_healerlink_share = 140
    sue_bud._econs_justified = x_econ_justifed
    sue_bud._econs_buildable = "swimmers"
    sue_bud._sum_healerlink_share = x_sum_healerlink_share
    sue_bud._econ_dict = {"run": "run"}
    sue_bud._healers_dict = {"run": "run"}
    assert sue_bud._econs_justified == x_econ_justifed
    assert sue_bud._econs_buildable
    assert sue_bud._sum_healerlink_share == x_sum_healerlink_share
    assert sue_bud._econ_dict != {}
    assert sue_bud._healers_dict != {}

    # WHEN
    sue_bud._pre_tree_traverse_attrs()

    # THEN
    assert sue_bud._econs_justified != x_econ_justifed
    assert sue_bud._econs_justified
    assert sue_bud._econs_buildable is False
    assert sue_bud._sum_healerlink_share == 0
    assert not sue_bud._econ_dict
    assert not sue_bud._healers_dict


def test_BudUnit_settle_bud_ClearsDescendantAttributes():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    # test root status:
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = sue_bud.make_road(week_road, mon_text)
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
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    week_idea = sue_bud.get_idea_obj(week_road)
    mon_text = "Monday"
    mon_road = sue_bud.make_road(week_road, mon_text)
    mon_idea = sue_bud.get_idea_obj(mon_road)

    email_text = "email"
    email_idea = ideaunit_shop(email_text, pledge=True)
    sue_bud.set_idea(email_idea, parent_road=casa_road)

    # test root status:
    x_idearoot = sue_bud.get_idea_obj(sue_bud._real_id)
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
    assert casa_idea._kids[email_text]._descendant_pledge_count == 0
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
    email_text = "email"
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    tue_text = "Tuesday"
    vacuum_text = "vacuum"
    sue_text = "Sue"

    casa_road = sue_bud.make_l1_road(casa_text)
    email_idea = ideaunit_shop(email_text, pledge=True)
    sue_bud.set_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(vacuum_text, pledge=True)
    sue_bud.set_idea(vacuum_idea, parent_road=casa_road)

    sue_bud.add_acctunit(acct_id=sue_text)
    x_awardlink = awardlink_shop(group_id=sue_text)

    sue_bud._idearoot._kids[casa_text]._kids[email_text].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_bud._kids[casa_text]._kids[email_text])
    # print(sue_bud._kids[casa_text]._kids[email_text]._awardlink)

    # WHEN
    sue_bud.settle_bud()
    # print(sue_bud._kids[casa_text]._kids[email_text])
    # print(sue_bud._kids[casa_text]._kids[email_text]._awardlink)

    # THEN
    assert sue_bud._idearoot._all_acct_cred is False
    assert sue_bud._idearoot._all_acct_debt is False
    casa_idea = sue_bud._idearoot._kids[casa_text]
    assert casa_idea._all_acct_cred is False
    assert casa_idea._all_acct_debt is False
    assert casa_idea._kids[email_text]._all_acct_cred is False
    assert casa_idea._kids[email_text]._all_acct_debt is False
    assert casa_idea._kids[vacuum_text]._all_acct_cred is True
    assert casa_idea._kids[vacuum_text]._all_acct_debt is True
    week_idea = sue_bud._idearoot._kids[week_text]
    assert week_idea._all_acct_cred is True
    assert week_idea._all_acct_debt is True
    assert week_idea._kids[mon_text]._all_acct_cred is True
    assert week_idea._kids[mon_text]._all_acct_debt is True
    assert week_idea._kids[tue_text]._all_acct_cred is True
    assert week_idea._kids[tue_text]._all_acct_debt is True


def test_BudUnit_settle_bud_SetsIdeaUnitAttr_awardlinks():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(zia_text)
    sue_bud.add_acctunit(Xio_text)

    assert len(sue_bud._accts) == 3
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 3
    swim_text = "swim"
    sue_bud.set_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, give_force=10)
    awardlink_zia = awardlink_shop(zia_text, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_text, give_force=10)
    swim_road = sue_bud.make_l1_road(swim_text)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    street_text = "streets"
    sue_bud.set_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_bud._idearoot._awardlinks in (None, {})
    assert len(sue_bud._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._idea_dict.keys()=} ")
    swim_idea = sue_bud._idea_dict.get(swim_road)
    street_idea = sue_bud._idea_dict.get(sue_bud.make_road(swim_road, street_text))

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea._awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(sue_bud._idea_dict)}")
    print(f"{swim_idea._awardlinks}")
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
    casa_text = "casa"
    casa_idea = sue_bud._idearoot._kids[casa_text]
    casa_idea._awardlines = {1: "testtest"}
    assert casa_idea._awardlines != {}
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud._idearoot._kids[casa_text]._awardlines


def test_BudUnit_settle_bud_DoesNotKeepUnneeded_awardheirs():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    Xio_text = "Xio"
    yao_bud.add_acctunit(yao_text)
    yao_bud.add_acctunit(zia_text)
    yao_bud.add_acctunit(Xio_text)

    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)

    yao_bud.set_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, give_force=10)
    awardlink_zia = awardlink_shop(zia_text, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_text, give_force=10)

    swim_idea = yao_bud.get_idea_obj(swim_road)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    yao_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    yao_bud.edit_idea_attr(swim_road, awardlink_del=yao_text)
    assert len(swim_idea._awardlinks) == 2
    assert len(swim_idea._awardheirs) == 3

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_idea._awardlinks) == 2
    assert len(swim_idea._awardheirs) == 2


def test_BudUnit_get_idea_tree_ordered_road_list_ReturnsCorrectObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_text = "weekdays"
    assert sue_bud.get_idea_tree_ordered_road_list()

    # WHEN
    ordered_node_list = sue_bud.get_idea_tree_ordered_road_list()

    # THEN
    assert len(ordered_node_list) == 17
    x_1st_road_in_ordered_list = sue_bud.get_idea_tree_ordered_road_list()[0]
    assert x_1st_road_in_ordered_list == sue_bud._real_id
    x_8th_road_in_ordered_list = sue_bud.get_idea_tree_ordered_road_list()[9]
    assert x_8th_road_in_ordered_list == sue_bud.make_l1_road(week_text)

    # WHEN
    y_bud = budunit_shop()

    # THEN
    y_1st_road_in_ordered_list = y_bud.get_idea_tree_ordered_road_list()[0]
    assert y_1st_road_in_ordered_list == sue_bud._real_id


def test_BudUnit_get_idea_tree_ordered_road_list_CorrectlyFiltersRangedIdeaRoadUnits():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN
    time_text = "timeline"
    time_road = yao_bud.make_l1_road(time_text)
    yao_bud.set_l1_idea(ideaunit_shop(time_text, _begin=0, _close=700))
    weeks_text = "weeks"
    yao_bud.set_idea(ideaunit_shop(weeks_text, _denom=7), time_road)

    # THEN
    assert len(yao_bud.get_idea_tree_ordered_road_list()) == 3
    assert len(yao_bud.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_BudUnit_get_idea_dict_ReturnsCorrectObjWhenSingle():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_text = "Texas"
    sue_bud.set_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    casa_text = "casa"
    sue_bud.set_l1_idea(ideaunit_shop(casa_text))

    # WHEN
    problems_dict = sue_bud.get_idea_dict(problem=True)

    # THEN
    assert sue_bud._econs_justified
    texas_road = sue_bud.make_l1_road(texas_text)
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
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text, mass=0)
    sue_budunit.set_l1_idea(casa_idea)
    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == {sue_budunit._real_id}

    # WHEN
    sue_budunit.edit_idea_attr(casa_road, mass=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == set()


def test_BudUnit_settle_bud_WhenIdeaUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_budunit.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text, mass=1)

    swim_text = "swimming"
    swim_road = sue_budunit.make_road(casa_road, swim_text)
    swim_idea = ideaunit_shop(swim_text, mass=8)

    clean_text = "cleaning"
    clean_road = sue_budunit.make_road(casa_road, clean_text)
    clean_idea = ideaunit_shop(clean_text, mass=2)
    sue_budunit.set_idea(ideaunit_shop(clean_text), casa_road)

    sweep_text = "sweep"
    sweep_road = sue_budunit.make_road(clean_road, sweep_text)
    sweep_idea = ideaunit_shop(sweep_text, mass=0)
    vaccum_text = "vaccum"
    vaccum_road = sue_budunit.make_road(clean_road, vaccum_text)
    vaccum_idea = ideaunit_shop(vaccum_text, mass=0)

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
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    yao_credit_belief = 3
    yao_debtit_belief = 2
    zia_credit_belief = 4
    zia_debtit_belief = 5
    yao_bud.add_acctunit(yao_text, yao_credit_belief, yao_debtit_belief)
    yao_bud.add_acctunit(zia_text, zia_credit_belief, zia_debtit_belief)
    x_idearoot = yao_bud.get_idea_obj(yao_bud._real_id)
    x_idearoot.set_awardlink(awardlink_shop(yao_text))
    x_idearoot.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    x_idearoot.set_awardlink(awardlink_shop(xio_text))
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert not yao_bud.groupbox_exists(yao_text)
    assert not yao_bud.groupbox_exists(zia_text)
    assert not yao_bud.groupbox_exists(xio_text)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupbox_exists(yao_text)
    assert yao_bud.groupbox_exists(zia_text)
    assert yao_bud.groupbox_exists(xio_text)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)
    assert len(yao_bud._groupboxs) == 3
    xio_groupbox = yao_bud.get_groupbox(xio_text)
    xio_symmerty_groupbox = yao_bud.create_symmetry_groupbox(xio_text)
    assert xio_groupbox._memberships.keys() == xio_symmerty_groupbox._memberships.keys()
    assert xio_groupbox.membership_exists(yao_text)
    assert xio_groupbox.membership_exists(zia_text)
    assert not xio_groupbox.membership_exists(xio_text)
    yao_membership = xio_groupbox.get_membership(yao_text)
    zia_membership = xio_groupbox.get_membership(zia_text)
    assert yao_membership.credit_vote == yao_credit_belief
    assert zia_membership.credit_vote == zia_credit_belief
    assert yao_membership.debtit_vote == yao_debtit_belief
    assert zia_membership.debtit_vote == zia_debtit_belief


def test_BudUnit_settle_bud_CreatesNewGroupBoxsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.set_l1_idea(ideaunit_shop(swim_text))
    zia_text = "Zia"
    yao_bud.add_acctunit(yao_text)
    yao_bud.add_acctunit(zia_text)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_text))
    swim_idea.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_text))
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert not yao_bud.groupbox_exists(yao_text)
    assert not yao_bud.groupbox_exists(zia_text)
    assert not yao_bud.groupbox_exists(xio_text)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupbox_exists(yao_text)
    assert yao_bud.groupbox_exists(zia_text)
    assert yao_bud.groupbox_exists(xio_text)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)
    assert len(yao_bud._groupboxs) == 3
    xio_groupbox = yao_bud.get_groupbox(xio_text)
    xio_symmerty_groupbox = yao_bud.create_symmetry_groupbox(xio_text)
    assert xio_groupbox._memberships.keys() == xio_symmerty_groupbox._memberships.keys()
    assert xio_groupbox.membership_exists(yao_text)
    assert xio_groupbox.membership_exists(zia_text)
    assert not xio_groupbox.membership_exists(xio_text)


def test_BudUnit_get_tree_traverse_generated_groupboxs_ReturnsObj():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    swim_text = "swim"
    swim_road = yao_bud.make_l1_road(swim_text)
    yao_bud.set_l1_idea(ideaunit_shop(swim_text))
    zia_text = "Zia"
    yao_bud.add_acctunit(yao_text)
    yao_bud.add_acctunit(zia_text)
    swim_idea = yao_bud.get_idea_obj(swim_road)
    swim_idea.set_awardlink(awardlink_shop(yao_text))
    swim_idea.set_awardlink(awardlink_shop(zia_text))
    xio_text = "Xio"
    swim_idea.set_awardlink(awardlink_shop(xio_text))
    yao_bud.settle_bud()
    assert yao_bud.groupbox_exists(yao_text)
    assert yao_bud.groupbox_exists(zia_text)
    assert yao_bud.groupbox_exists(xio_text)
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 2
    assert len(yao_bud.get_acctunit_group_ids_dict()) != len(yao_bud._groupboxs)

    # WHEN
    symmerty_group_ids = yao_bud.get_tree_traverse_generated_groupboxs()

    # THEN
    assert len(symmerty_group_ids) == 1
    assert symmerty_group_ids == {xio_text}

    # ESTABLISH
    run_text = ";Run"
    swim_idea.set_awardlink(awardlink_shop(run_text))
    assert not yao_bud.groupbox_exists(run_text)
    yao_bud.settle_bud()
    assert yao_bud.groupbox_exists(run_text)

    # WHEN
    symmerty_group_ids = yao_bud.get_tree_traverse_generated_groupboxs()

    # THEN
    assert len(symmerty_group_ids) == 2
    assert symmerty_group_ids == {xio_text, run_text}


def test_BudUnit_settle_bud_Sets_idearoot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    week_text = "week"
    week_road = yao_bud.make_l1_road(week_text)
    week_addin = 10
    week_idea = ideaunit_shop(week_text, _begin=10, _close=15, _addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_text = "Tue"
    tue_road = yao_bud.make_road(week_road, tue_text)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_text, _addin=tue_addin), week_road)
    x_real_id = yao_bud._real_id
    yao_bud.edit_idea_attr(x_real_id, reason_base=tue_road, reason_premise=tue_road)

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
    exception_text = f"Cannot have fact for range inheritor '{tue_road}'. A ranged fact idea must have _begin, _close attributes"
    assert str(excinfo.value) == exception_text

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
    # root_idea = yao_bud.get_idea_obj(yao_bud._real_id)
    # print(f"{week_road=} {root_idea._factheirs.keys()=}")
    # assert root_idea._factheirs.get(week_road) == week_factheir
    # assert len(root_idea._factheirs) == 2
    # assert root_idea._factheirs == {tue_road: tue_factheir, week_road: week_factheir}


def test_BudUnit_settle_bud_SetsIdeaUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_text = "yao"
    yao_bud = budunit_shop(yao_text)
    week_text = "week"
    week_road = yao_bud.make_l1_road(week_text)
    week_addin = 10
    week_idea = ideaunit_shop(week_text, _begin=10, _close=15, _addin=week_addin)
    yao_bud.set_l1_idea(week_idea)
    tue_text = "Tue"
    tue_road = yao_bud.make_road(week_road, tue_text)
    tue_addin = 100
    yao_bud.set_idea(ideaunit_shop(tue_text, _addin=tue_addin), week_road)
    ball_text = "ball"
    ball_road = yao_bud.make_l1_road(ball_text)
    yao_bud.set_l1_idea(ideaunit_shop(ball_text))
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
