from src.a01_way_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_item import factheir_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from pytest import raises as pytest_raises


def test_BudUnit_clear_item_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_item_dict = {1: 2, 2: 4}
    sue_bud._rational = x_rational
    sue_bud._tree_traverse_count = x_tree_traverse_count
    sue_bud._item_dict = x_item_dict
    sue_bud._offtrack_kids_mass_set = "example"
    sue_bud._reason_bases = {"example2"}
    sue_bud._range_inheritors = {"example2": 1}
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._item_dict == x_item_dict
    assert sue_bud._offtrack_kids_mass_set != set()
    assert sue_bud._reason_bases != set()
    assert sue_bud._range_inheritors != {}

    # WHEN
    sue_bud._clear_item_dict_and_bud_obj_settle_attrs()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._item_dict != x_item_dict
    assert sue_bud._item_dict == {sue_bud.itemroot.get_way(): sue_bud.itemroot}
    assert sue_bud._offtrack_kids_mass_set == set()
    assert not sue_bud._reason_bases
    assert not sue_bud._range_inheritors


def test_BudUnit_clear_item_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
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
    sue_bud._clear_item_dict_and_bud_obj_settle_attrs()

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
    casa_item = sue_bud.get_item_obj(casa_way)
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(week_way, mon_str)
    mon_item = sue_bud.get_item_obj(mon_way)
    assert sue_bud.itemroot._descendant_pledge_count is None
    assert sue_bud.itemroot._all_acct_cred is None
    assert sue_bud.itemroot._all_acct_debt is None
    assert casa_item._descendant_pledge_count is None
    assert casa_item._all_acct_cred is None
    assert casa_item._all_acct_debt is None
    assert mon_item._descendant_pledge_count is None
    assert mon_item._all_acct_cred is None
    assert mon_item._all_acct_debt is None

    sue_bud.itemroot._descendant_pledge_count = -2
    sue_bud.itemroot._all_acct_cred = -2
    sue_bud.itemroot._all_acct_debt = -2
    casa_item._descendant_pledge_count = -2
    casa_item._all_acct_cred = -2
    casa_item._all_acct_debt = -2
    mon_item._descendant_pledge_count = -2
    mon_item._all_acct_cred = -2
    mon_item._all_acct_debt = -2

    assert sue_bud.itemroot._descendant_pledge_count == -2
    assert sue_bud.itemroot._all_acct_cred == -2
    assert sue_bud.itemroot._all_acct_debt == -2
    assert casa_item._descendant_pledge_count == -2
    assert casa_item._all_acct_cred == -2
    assert casa_item._all_acct_debt == -2
    assert mon_item._descendant_pledge_count == -2
    assert mon_item._all_acct_cred == -2
    assert mon_item._all_acct_debt == -2

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud.itemroot._descendant_pledge_count == 2
    assert casa_item._descendant_pledge_count == 0
    assert mon_item._descendant_pledge_count == 0

    assert mon_item._all_acct_cred is True
    assert mon_item._all_acct_debt is True
    assert casa_item._all_acct_cred is True
    assert casa_item._all_acct_debt is True
    assert sue_bud.itemroot._all_acct_cred is True
    assert sue_bud.itemroot._all_acct_debt is True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_bud = budunit_shop(owner_name="Yao")
    assert yao_bud.itemroot._descendant_pledge_count is None
    assert yao_bud.itemroot._all_acct_cred is None
    assert yao_bud.itemroot._all_acct_debt is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.itemroot._descendant_pledge_count == 0
    assert yao_bud.itemroot._all_acct_cred is True
    assert yao_bud.itemroot._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    casa_item = sue_bud.get_item_obj(casa_way)
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    week_item = sue_bud.get_item_obj(week_way)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(week_way, mon_str)
    mon_item = sue_bud.get_item_obj(mon_way)

    email_str = "email"
    email_item = itemunit_shop(email_str, pledge=True)
    sue_bud.set_item(email_item, parent_way=casa_way)

    # test root status:
    root_way = to_way(sue_bud.fisc_tag)
    x_itemroot = sue_bud.get_item_obj(root_way)
    assert x_itemroot._descendant_pledge_count is None
    assert x_itemroot._all_acct_cred is None
    assert x_itemroot._all_acct_debt is None
    assert casa_item._descendant_pledge_count is None
    assert casa_item._all_acct_cred is None
    assert casa_item._all_acct_debt is None
    assert mon_item._descendant_pledge_count is None
    assert mon_item._all_acct_cred is None
    assert mon_item._all_acct_debt is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert x_itemroot._descendant_pledge_count == 3
    assert casa_item._descendant_pledge_count == 1
    assert casa_item._kids[email_str]._descendant_pledge_count == 0
    assert mon_item._descendant_pledge_count == 0
    assert x_itemroot._all_acct_cred is True
    assert x_itemroot._all_acct_debt is True
    assert casa_item._all_acct_cred is True
    assert casa_item._all_acct_debt is True
    assert mon_item._all_acct_cred is True
    assert mon_item._all_acct_debt is True


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
    email_item = itemunit_shop(email_str, pledge=True)
    sue_bud.set_item(email_item, parent_way=casa_way)
    vacuum_item = itemunit_shop(vacuum_str, pledge=True)
    sue_bud.set_item(vacuum_item, parent_way=casa_way)

    sue_bud.add_acctunit(acct_name=sue_str)
    x_awardlink = awardlink_shop(awardee_title=sue_str)

    sue_bud.itemroot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_bud.settle_bud()
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_bud.itemroot._all_acct_cred is False
    assert sue_bud.itemroot._all_acct_debt is False
    casa_item = sue_bud.itemroot._kids[casa_str]
    assert casa_item._all_acct_cred is False
    assert casa_item._all_acct_debt is False
    assert casa_item._kids[email_str]._all_acct_cred is False
    assert casa_item._kids[email_str]._all_acct_debt is False
    assert casa_item._kids[vacuum_str]._all_acct_cred is True
    assert casa_item._kids[vacuum_str]._all_acct_debt is True
    week_item = sue_bud.itemroot._kids[week_str]
    assert week_item._all_acct_cred is True
    assert week_item._all_acct_debt is True
    assert week_item._kids[mon_str]._all_acct_cred is True
    assert week_item._kids[mon_str]._all_acct_debt is True
    assert week_item._kids[tue_str]._all_acct_cred is True
    assert week_item._kids[tue_str]._all_acct_debt is True


def test_BudUnit_settle_bud_SetsItemUnitAttr_awardlinks():
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
    sue_bud.set_l1_item(itemunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_way = sue_bud.make_l1_way(swim_str)
    sue_bud.edit_item_attr(swim_way, awardlink=awardlink_yao)
    sue_bud.edit_item_attr(swim_way, awardlink=awardlink_zia)
    sue_bud.edit_item_attr(swim_way, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_bud.set_item(itemunit_shop(street_str), parent_way=swim_way)
    assert sue_bud.itemroot.awardlinks in (None, {})
    assert len(sue_bud.itemroot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._item_dict.keys()=} ")
    swim_item = sue_bud._item_dict.get(swim_way)
    street_item = sue_bud._item_dict.get(sue_bud.make_way(swim_way, street_str))

    assert len(swim_item.awardlinks) == 3
    assert len(swim_item._awardheirs) == 3
    assert street_item.awardlinks in (None, {})
    assert len(street_item._awardheirs) == 3

    print(f"{len(sue_bud._item_dict)}")
    print(f"{swim_item.awardlinks}")
    print(f"{swim_item._awardheirs}")
    print(f"{swim_item._awardheirs}")
    assert len(sue_bud.itemroot._kids["swim"]._awardheirs) == 3


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # item tree has no awardlinks
    assert sue_bud.itemroot._awardlines == {}
    sue_bud.itemroot._awardlines = {1: "testtest"}
    assert sue_bud.itemroot._awardlines != {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.itemroot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_item = sue_bud.itemroot._kids[casa_str]
    casa_item._awardlines = {1: "testtest"}
    assert casa_item._awardlines != {}
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.itemroot._kids[casa_str]._awardlines


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
    swim_way = yao_bud.make_l1_way(swim_str)

    yao_bud.set_l1_item(itemunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_item = yao_bud.get_item_obj(swim_way)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_yao)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_zia)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_Xio)

    assert len(swim_item.awardlinks) == 3
    assert len(swim_item._awardheirs) == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_item.awardlinks) == 3
    assert len(swim_item._awardheirs) == 3
    yao_bud.edit_item_attr(swim_way, awardlink_del=yao_str)
    assert len(swim_item.awardlinks) == 2
    assert len(swim_item._awardheirs) == 3

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_item.awardlinks) == 2
    assert len(swim_item._awardheirs) == 2


def test_BudUnit_get_item_tree_ordered_way_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    assert sue_bud.get_item_tree_ordered_way_list()

    # WHEN
    ordered_tag_list = sue_bud.get_item_tree_ordered_way_list()

    # THEN
    assert len(ordered_tag_list) == 17
    x_1st_way_in_ordered_list = sue_bud.get_item_tree_ordered_way_list()[0]
    root_way = to_way(sue_bud.fisc_tag)
    assert x_1st_way_in_ordered_list == root_way
    x_8th_way_in_ordered_list = sue_bud.get_item_tree_ordered_way_list()[9]
    assert x_8th_way_in_ordered_list == sue_bud.make_l1_way(week_str)

    # WHEN
    y_bud = budunit_shop()

    # THEN
    y_1st_way_in_ordered_list = y_bud.get_item_tree_ordered_way_list()[0]
    assert y_1st_way_in_ordered_list == root_way


def test_BudUnit_get_item_tree_ordered_way_list_CorrectlyCleansRangedItemWayUnits():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_way = yao_bud.make_l1_way(time_str)
    yao_bud.set_l1_item(itemunit_shop(time_str, begin=0, close=700))
    weeks_str = "weeks"
    yao_bud.set_item(itemunit_shop(weeks_str, denom=7), time_way)

    # THEN
    assert len(yao_bud.get_item_tree_ordered_way_list()) == 3
    assert len(yao_bud.get_item_tree_ordered_way_list(no_range_descendants=True)) == 2


def test_BudUnit_get_item_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    sue_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_bud.set_l1_item(itemunit_shop(casa_str))

    # WHEN
    problems_dict = sue_bud.get_item_dict(problem=True)

    # THEN
    assert sue_bud._keeps_justified
    texas_way = sue_bud.make_l1_way(texas_str)
    texas_item = sue_bud.get_item_obj(texas_way)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_way: texas_item}


def test_BudUnit_settle_bud_CreatesFullyPopulated_item_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._item_dict) == 17


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


def test_BudUnit_settle_bud_WhenItemRootHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_item = itemunit_shop(casa_str, mass=0)
    sue_budunit.set_l1_item(casa_item)
    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    root_way = to_way(sue_budunit.fisc_tag)
    assert sue_budunit._offtrack_kids_mass_set == {root_way}

    # WHEN
    sue_budunit.edit_item_attr(casa_way, mass=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == set()


def test_BudUnit_settle_bud_WhenItemUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
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

    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == {clean_way}


def test_BudUnit_settle_bud_CreatesNewGroupUnitsWhenNeeded_Scenario0():
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
    x_itemroot = yao_bud.get_item_obj(root_way)
    x_itemroot.set_awardlink(awardlink_shop(yao_str))
    x_itemroot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_itemroot.set_awardlink(awardlink_shop(xio_str))
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


def test_BudUnit_settle_bud_CreatesNewGroupUnitsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    swim_str = "swim"
    swim_way = yao_bud.make_l1_way(swim_str)
    yao_bud.set_l1_item(itemunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_item = yao_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(awardlink_shop(yao_str))
    swim_item.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_item.set_awardlink(awardlink_shop(xio_str))
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
    yao_bud.set_l1_item(itemunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_item = yao_bud.get_item_obj(swim_way)
    swim_item.set_awardlink(awardlink_shop(yao_str))
    swim_item.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_item.set_awardlink(awardlink_shop(xio_str))
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
    swim_item.set_awardlink(awardlink_shop(run_str))
    assert not yao_bud.groupunit_exists(run_str)
    yao_bud.settle_bud()
    assert yao_bud.groupunit_exists(run_str)

    # WHEN
    symmerty_group_labels = yao_bud.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_labels) == 2
    assert symmerty_group_labels == {xio_str, run_str}


def test_BudUnit_settle_bud_Sets_itemroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_way = yao_bud.make_l1_way(week_str)
    week_addin = 10
    week_item = itemunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_item(week_item)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(week_way, tue_str)
    tue_addin = 100
    yao_bud.set_item(itemunit_shop(tue_str, addin=tue_addin), week_way)
    root_way = to_way(yao_bud.fisc_tag)
    yao_bud.edit_item_attr(root_way, reason_base=tue_way, reason_premise=tue_way)

    week_open = 3
    week_nigh = 7
    yao_bud.add_fact(week_way, week_way, week_open, week_nigh)

    # assert len(ball_item._reasonheirs) == 1
    # assert ball_item._factheirs == {week_way: week_factheir}
    # assert ball_item._factheirs.get(week_way)
    # assert len(ball_item._factheirs) == 1
    # assert ball_item._factheirs.get(tue_way) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.settle_bud()
    exception_str = f"Cannot have fact for range inheritor '{tue_way}'. A ranged fact item must have _begin, _close attributes"
    assert str(excinfo.value) == exception_str

    # THEN
    # week_factunit = factunit_shop(week_way, week_way, week_open, week_nigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_item_dict = {week_item.get_way(): week_item, tue_item.get_way(): tue_item}
    # ball_item.set_reasonheirs(x_bud_item_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_way: week_way}
    # week_factheir = factheir_shop(week_way, week_way, week_open, week_nigh)

    # tue_open = 113
    # tue_nigh = 117
    # tue_factheir = factheir_shop(tue_way, tue_way, tue_open, tue_nigh)
    # root_item = yao_bud.get_item_obj(root_way)
    # print(f"{week_way=} {root_item._factheirs.keys()=}")
    # assert root_item._factheirs.get(week_way) == week_factheir
    # assert len(root_item._factheirs) == 2
    # assert root_item._factheirs == {tue_way: tue_factheir, week_way: week_factheir}


def test_BudUnit_settle_bud_SetsItemUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    week_str = "week"
    week_way = yao_bud.make_l1_way(week_str)
    week_addin = 10
    week_item = itemunit_shop(week_str, begin=10, close=15, addin=week_addin)
    yao_bud.set_l1_item(week_item)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(week_way, tue_str)
    tue_addin = 100
    yao_bud.set_item(itemunit_shop(tue_str, addin=tue_addin), week_way)
    ball_str = "ball"
    ball_way = yao_bud.make_l1_way(ball_str)
    yao_bud.set_l1_item(itemunit_shop(ball_str))
    yao_bud.edit_item_attr(ball_way, reason_base=tue_way, reason_premise=tue_way)

    week_open = 3
    week_nigh = 7
    yao_bud.add_fact(week_way, week_way, week_open, week_nigh)

    # assert len(ball_item._reasonheirs) == 1
    # assert ball_item._factheirs == {week_way: week_factheir}
    # assert ball_item._factheirs.get(week_way)
    # assert len(ball_item._factheirs) == 1
    # assert ball_item._factheirs.get(tue_way) is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    # week_factunit = factunit_shop(week_way, week_way, week_open, week_nigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_item_dict = {week_item.get_way(): week_item, tue_item.get_way(): tue_item}
    # ball_item.set_reasonheirs(x_bud_item_dict, tue_reasonheirs)
    x_range_inheritors = {tue_way: week_way}
    week_factheir = factheir_shop(week_way, week_way, week_open, week_nigh)

    tue_open = 113
    tue_nigh = 117
    tue_factheir = factheir_shop(tue_way, tue_way, tue_open, tue_nigh)
    ball_item = yao_bud.get_item_obj(ball_way)
    print(f"{week_way=} {ball_item._factheirs.keys()=}")
    assert ball_item._factheirs.get(week_way) == week_factheir
    assert len(ball_item._factheirs) == 2
    assert ball_item._factheirs == {tue_way: tue_factheir, week_way: week_factheir}
