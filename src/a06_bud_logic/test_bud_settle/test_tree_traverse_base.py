from pytest import raises as pytest_raises
from src.a01_term_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factheir_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
)
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_clear_concept_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_concept_dict = {1: 2, 2: 4}
    sue_bud._rational = x_rational
    sue_bud._tree_traverse_count = x_tree_traverse_count
    sue_bud._concept_dict = x_concept_dict
    sue_bud._offtrack_kids_mass_set = "example"
    sue_bud._reason_rcontexts = {"example2"}
    sue_bud._range_inheritors = {"example2": 1}
    assert sue_bud._rational == x_rational
    assert sue_bud._tree_traverse_count == x_tree_traverse_count
    assert sue_bud._concept_dict == x_concept_dict
    assert sue_bud._offtrack_kids_mass_set != set()
    assert sue_bud._reason_rcontexts != set()
    assert sue_bud._range_inheritors != {}

    # WHEN
    sue_bud._clear_concept_dict_and_bud_obj_settle_attrs()

    # THEN
    assert sue_bud._rational != x_rational
    assert not sue_bud._rational
    assert sue_bud._tree_traverse_count != x_tree_traverse_count
    assert sue_bud._tree_traverse_count == 0
    assert sue_bud._concept_dict != x_concept_dict
    assert sue_bud._concept_dict == {
        sue_bud.conceptroot.get_concept_way(): sue_bud.conceptroot
    }
    assert sue_bud._offtrack_kids_mass_set == set()
    assert not sue_bud._reason_rcontexts
    assert not sue_bud._range_inheritors


def test_BudUnit_clear_concept_dict_and_bud_obj_settle_attrs_CorrectlySetsAttrs():
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
    sue_bud._clear_concept_dict_and_bud_obj_settle_attrs()

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
    casa_concept = sue_bud.get_concept_obj(casa_way)
    wk_str = "wkdays"
    wk_way = sue_bud.make_l1_way(wk_str)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(wk_way, mon_str)
    mon_concept = sue_bud.get_concept_obj(mon_way)
    assert sue_bud.conceptroot._descendant_pledge_count is None
    assert sue_bud.conceptroot._all_acct_cred is None
    assert sue_bud.conceptroot._all_acct_debt is None
    assert casa_concept._descendant_pledge_count is None
    assert casa_concept._all_acct_cred is None
    assert casa_concept._all_acct_debt is None
    assert mon_concept._descendant_pledge_count is None
    assert mon_concept._all_acct_cred is None
    assert mon_concept._all_acct_debt is None

    sue_bud.conceptroot._descendant_pledge_count = -2
    sue_bud.conceptroot._all_acct_cred = -2
    sue_bud.conceptroot._all_acct_debt = -2
    casa_concept._descendant_pledge_count = -2
    casa_concept._all_acct_cred = -2
    casa_concept._all_acct_debt = -2
    mon_concept._descendant_pledge_count = -2
    mon_concept._all_acct_cred = -2
    mon_concept._all_acct_debt = -2

    assert sue_bud.conceptroot._descendant_pledge_count == -2
    assert sue_bud.conceptroot._all_acct_cred == -2
    assert sue_bud.conceptroot._all_acct_debt == -2
    assert casa_concept._descendant_pledge_count == -2
    assert casa_concept._all_acct_cred == -2
    assert casa_concept._all_acct_debt == -2
    assert mon_concept._descendant_pledge_count == -2
    assert mon_concept._all_acct_cred == -2
    assert mon_concept._all_acct_debt == -2

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud.conceptroot._descendant_pledge_count == 2
    assert casa_concept._descendant_pledge_count == 0
    assert mon_concept._descendant_pledge_count == 0

    assert mon_concept._all_acct_cred is True
    assert mon_concept._all_acct_debt is True
    assert casa_concept._all_acct_cred is True
    assert casa_concept._all_acct_debt is True
    assert sue_bud.conceptroot._all_acct_cred is True
    assert sue_bud.conceptroot._all_acct_debt is True


def test_BudUnit_settle_bud_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_bud = budunit_shop(owner_name="Yao")
    assert yao_bud.conceptroot._descendant_pledge_count is None
    assert yao_bud.conceptroot._all_acct_cred is None
    assert yao_bud.conceptroot._all_acct_debt is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.conceptroot._descendant_pledge_count == 0
    assert yao_bud.conceptroot._all_acct_cred is True
    assert yao_bud.conceptroot._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    casa_concept = sue_bud.get_concept_obj(casa_way)
    wk_str = "wkdays"
    wk_way = sue_bud.make_l1_way(wk_str)
    wk_concept = sue_bud.get_concept_obj(wk_way)
    mon_str = "Monday"
    mon_way = sue_bud.make_way(wk_way, mon_str)
    mon_concept = sue_bud.get_concept_obj(mon_way)

    email_str = "email"
    email_concept = conceptunit_shop(email_str, pledge=True)
    sue_bud.set_concept(email_concept, parent_way=casa_way)

    # test root status:
    root_way = to_way(sue_bud.fisc_label)
    x_conceptroot = sue_bud.get_concept_obj(root_way)
    assert x_conceptroot._descendant_pledge_count is None
    assert x_conceptroot._all_acct_cred is None
    assert x_conceptroot._all_acct_debt is None
    assert casa_concept._descendant_pledge_count is None
    assert casa_concept._all_acct_cred is None
    assert casa_concept._all_acct_debt is None
    assert mon_concept._descendant_pledge_count is None
    assert mon_concept._all_acct_cred is None
    assert mon_concept._all_acct_debt is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert x_conceptroot._descendant_pledge_count == 3
    assert casa_concept._descendant_pledge_count == 1
    assert casa_concept._kids[email_str]._descendant_pledge_count == 0
    assert mon_concept._descendant_pledge_count == 0
    assert x_conceptroot._all_acct_cred is True
    assert x_conceptroot._all_acct_debt is True
    assert casa_concept._all_acct_cred is True
    assert casa_concept._all_acct_debt is True
    assert mon_concept._all_acct_cred is True
    assert mon_concept._all_acct_debt is True


def test_BudUnit_settle_bud_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    email_str = "email"
    casa_str = "casa"
    wk_str = "wkdays"
    mon_str = "Monday"
    tue_str = "Tuesday"
    vacuum_str = "vacuum"
    sue_str = "Sue"

    casa_way = sue_bud.make_l1_way(casa_str)
    email_concept = conceptunit_shop(email_str, pledge=True)
    sue_bud.set_concept(email_concept, parent_way=casa_way)
    vacuum_concept = conceptunit_shop(vacuum_str, pledge=True)
    sue_bud.set_concept(vacuum_concept, parent_way=casa_way)

    sue_bud.add_acctunit(acct_name=sue_str)
    x_awardlink = awardlink_shop(awardee_title=sue_str)

    sue_bud.conceptroot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_bud.settle_bud()
    # print(sue_bud._kids[casa_str]._kids[email_str])
    # print(sue_bud._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_bud.conceptroot._all_acct_cred is False
    assert sue_bud.conceptroot._all_acct_debt is False
    casa_concept = sue_bud.conceptroot._kids[casa_str]
    assert casa_concept._all_acct_cred is False
    assert casa_concept._all_acct_debt is False
    assert casa_concept._kids[email_str]._all_acct_cred is False
    assert casa_concept._kids[email_str]._all_acct_debt is False
    assert casa_concept._kids[vacuum_str]._all_acct_cred is True
    assert casa_concept._kids[vacuum_str]._all_acct_debt is True
    wk_concept = sue_bud.conceptroot._kids[wk_str]
    assert wk_concept._all_acct_cred is True
    assert wk_concept._all_acct_debt is True
    assert wk_concept._kids[mon_str]._all_acct_cred is True
    assert wk_concept._kids[mon_str]._all_acct_debt is True
    assert wk_concept._kids[tue_str]._all_acct_cred is True
    assert wk_concept._kids[tue_str]._all_acct_debt is True


def test_BudUnit_settle_bud_SetsConceptUnitAttr_awardlinks():
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
    assert len(sue_bud.get_acctunit_group_titles_dict()) == 3
    swim_str = "swim"
    sue_bud.set_l1_concept(conceptunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_way = sue_bud.make_l1_way(swim_str)
    sue_bud.edit_concept_attr(swim_way, awardlink=awardlink_yao)
    sue_bud.edit_concept_attr(swim_way, awardlink=awardlink_zia)
    sue_bud.edit_concept_attr(swim_way, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_bud.set_concept(conceptunit_shop(street_str), parent_way=swim_way)
    assert sue_bud.conceptroot.awardlinks in (None, {})
    assert len(sue_bud.conceptroot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_bud.settle_bud()

    # THEN
    print(f"{sue_bud._concept_dict.keys()=} ")
    swim_concept = sue_bud._concept_dict.get(swim_way)
    street_concept = sue_bud._concept_dict.get(sue_bud.make_way(swim_way, street_str))

    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 3
    assert street_concept.awardlinks in (None, {})
    assert len(street_concept._awardheirs) == 3

    print(f"{len(sue_bud._concept_dict)}")
    print(f"{swim_concept.awardlinks}")
    print(f"{swim_concept._awardheirs}")
    print(f"{swim_concept._awardheirs}")
    assert len(sue_bud.conceptroot._kids["swim"]._awardheirs) == 3


def test_BudUnit_settle_bud_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    # concept tree has no awardlinks
    assert sue_bud.conceptroot._awardlines == {}
    sue_bud.conceptroot._awardlines = {1: "testtest"}
    assert sue_bud.conceptroot._awardlines != {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.conceptroot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_concept = sue_bud.conceptroot._kids[casa_str]
    casa_concept._awardlines = {1: "testtest"}
    assert casa_concept._awardlines != {}
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud.conceptroot._kids[casa_str]._awardlines


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

    yao_bud.set_l1_concept(conceptunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_concept = yao_bud.get_concept_obj(swim_way)
    yao_bud.edit_concept_attr(swim_way, awardlink=awardlink_yao)
    yao_bud.edit_concept_attr(swim_way, awardlink=awardlink_zia)
    yao_bud.edit_concept_attr(swim_way, awardlink=awardlink_Xio)

    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 0

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 3
    yao_bud.edit_concept_attr(swim_way, awardlink_del=yao_str)
    assert len(swim_concept.awardlinks) == 2
    assert len(swim_concept._awardheirs) == 3

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert len(swim_concept.awardlinks) == 2
    assert len(swim_concept._awardheirs) == 2


def test_BudUnit_get_concept_tree_ordered_way_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    wk_str = "wkdays"
    assert sue_bud.get_concept_tree_ordered_way_list()

    # WHEN
    ordered_label_list = sue_bud.get_concept_tree_ordered_way_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_way_in_ordered_list = sue_bud.get_concept_tree_ordered_way_list()[0]
    root_way = to_way(sue_bud.fisc_label)
    assert x_1st_way_in_ordered_list == root_way
    x_8th_way_in_ordered_list = sue_bud.get_concept_tree_ordered_way_list()[9]
    assert x_8th_way_in_ordered_list == sue_bud.make_l1_way(wk_str)

    # WHEN
    y_bud = budunit_shop(fisc_label="accord23")

    # THEN
    y_1st_way_in_ordered_list = y_bud.get_concept_tree_ordered_way_list()[0]
    assert y_1st_way_in_ordered_list == root_way


def test_BudUnit_get_concept_tree_ordered_way_list_CorrectlyCleansRangedConceptWayTerms():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_way = yao_bud.make_l1_way(time_str)
    yao_bud.set_l1_concept(conceptunit_shop(time_str, begin=0, close=700))
    wks_str = "wks"
    yao_bud.set_concept(conceptunit_shop(wks_str, denom=7), time_way)

    # THEN
    assert len(yao_bud.get_concept_tree_ordered_way_list()) == 3
    assert (
        len(yao_bud.get_concept_tree_ordered_way_list(no_range_descendants=True)) == 2
    )


def test_BudUnit_get_concept_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    sue_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_bud.set_l1_concept(conceptunit_shop(casa_str))

    # WHEN
    problems_dict = sue_bud.get_concept_dict(problem=True)

    # THEN
    assert sue_bud._keeps_justified
    texas_way = sue_bud.make_l1_way(texas_str)
    texas_concept = sue_bud.get_concept_obj(texas_way)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_way: texas_concept}


def test_BudUnit_settle_bud_CreatesFullyPopulated_concept_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._concept_dict) == 17


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


def test_BudUnit_settle_bud_WhenConceptRootHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set_Scenario0():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_concept = conceptunit_shop(casa_str, mass=0)
    sue_budunit.set_l1_concept(casa_concept)
    assert sue_budunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    root_way = to_way(sue_budunit.fisc_label)
    assert sue_budunit._offtrack_kids_mass_set == {root_way}

    # WHEN
    sue_budunit.edit_concept_attr(casa_way, mass=2)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._offtrack_kids_mass_set == set()


def test_BudUnit_settle_bud_WhenConceptUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_concept = conceptunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_way = sue_budunit.make_way(casa_way, swim_str)
    swim_concept = conceptunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_way = sue_budunit.make_way(casa_way, clean_str)
    clean_concept = conceptunit_shop(clean_str, mass=2)
    sue_budunit.set_concept(conceptunit_shop(clean_str), casa_way)

    sweep_str = "sweep"
    sweep_way = sue_budunit.make_way(clean_way, sweep_str)
    sweep_concept = conceptunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_way = sue_budunit.make_way(clean_way, vaccum_str)
    vaccum_concept = conceptunit_shop(vaccum_str, mass=0)

    sue_budunit.set_l1_concept(casa_concept)
    sue_budunit.set_concept(swim_concept, casa_way)
    sue_budunit.set_concept(clean_concept, casa_way)
    sue_budunit.set_concept(sweep_concept, clean_way)  # _mass=0
    sue_budunit.set_concept(vaccum_concept, clean_way)  # _mass=0

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
    root_way = to_way(yao_bud.fisc_label)
    x_conceptroot = yao_bud.get_concept_obj(root_way)
    x_conceptroot.set_awardlink(awardlink_shop(yao_str))
    x_conceptroot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_conceptroot.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_titles_dict()) == 2
    assert not yao_bud.groupunit_exists(yao_str)
    assert not yao_bud.groupunit_exists(zia_str)
    assert not yao_bud.groupunit_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_titles_dict()) == 2
    assert len(yao_bud.get_acctunit_group_titles_dict()) != len(yao_bud._groupunits)
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
    yao_bud.set_l1_concept(conceptunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_concept = yao_bud.get_concept_obj(swim_way)
    swim_concept.set_awardlink(awardlink_shop(yao_str))
    swim_concept.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_concept.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_bud.get_acctunit_group_titles_dict()) == 2
    assert not yao_bud.groupunit_exists(yao_str)
    assert not yao_bud.groupunit_exists(zia_str)
    assert not yao_bud.groupunit_exists(xio_str)

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_titles_dict()) == 2
    assert len(yao_bud.get_acctunit_group_titles_dict()) != len(yao_bud._groupunits)
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
    yao_bud.set_l1_concept(conceptunit_shop(swim_str))
    zia_str = "Zia"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    swim_concept = yao_bud.get_concept_obj(swim_way)
    swim_concept.set_awardlink(awardlink_shop(yao_str))
    swim_concept.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_concept.set_awardlink(awardlink_shop(xio_str))
    yao_bud.settle_bud()
    assert yao_bud.groupunit_exists(yao_str)
    assert yao_bud.groupunit_exists(zia_str)
    assert yao_bud.groupunit_exists(xio_str)
    assert len(yao_bud.get_acctunit_group_titles_dict()) == 2
    assert len(yao_bud.get_acctunit_group_titles_dict()) != len(yao_bud._groupunits)

    # WHEN
    symmerty_group_titles = yao_bud.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_concept.set_awardlink(awardlink_shop(run_str))
    assert not yao_bud.groupunit_exists(run_str)
    yao_bud.settle_bud()
    assert yao_bud.groupunit_exists(run_str)

    # WHEN
    symmerty_group_titles = yao_bud.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {xio_str, run_str}


def test_BudUnit_settle_bud_Sets_conceptroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    wk_str = "wk"
    wk_way = yao_bud.make_l1_way(wk_str)
    wk_addin = 10
    wk_concept = conceptunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_bud.set_l1_concept(wk_concept)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(wk_way, tue_str)
    tue_addin = 100
    yao_bud.set_concept(conceptunit_shop(tue_str, addin=tue_addin), wk_way)
    root_way = to_way(yao_bud.fisc_label)
    yao_bud.edit_concept_attr(root_way, reason_rcontext=tue_way, reason_premise=tue_way)

    wk_popen = 3
    wk_pnigh = 7
    yao_bud.add_fact(wk_way, wk_way, wk_popen, wk_pnigh)

    # assert len(ball_concept._reasonheirs) == 1
    # assert ball_concept._factheirs == {wk_way: wk_factheir}
    # assert ball_concept._factheirs.get(wk_way)
    # assert len(ball_concept._factheirs) == 1
    # assert ball_concept._factheirs.get(tue_way) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.settle_bud()
    exception_str = f"Cannot have fact for range inheritor '{tue_way}'. A ranged fact concept must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_way, wk_way, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_concept_dict = {wk_concept.get_concept_way(): wk_concept, tue_concept.get_concept_way(): tue_concept}
    # ball_concept.set_reasonheirs(x_bud_concept_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_way: wk_way}
    # wk_factheir = factheir_shop(wk_way, wk_way, wk_popen, wk_pnigh)

    # tue_popen = 113
    # tue_pnigh = 117
    # tue_factheir = factheir_shop(tue_way, tue_way, tue_popen, tue_pnigh)
    # root_concept = yao_bud.get_concept_obj(root_way)
    # print(f"{wk_way=} {root_concept._factheirs.keys()=}")
    # assert root_concept._factheirs.get(wk_way) == wk_factheir
    # assert len(root_concept._factheirs) == 2
    # assert root_concept._factheirs == {tue_way: tue_factheir, wk_way: wk_factheir}


def test_BudUnit_settle_bud_SetsConceptUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    wk_str = "wk"
    wk_way = yao_bud.make_l1_way(wk_str)
    wk_addin = 10
    wk_concept = conceptunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_bud.set_l1_concept(wk_concept)
    tue_str = "Tue"
    tue_way = yao_bud.make_way(wk_way, tue_str)
    tue_addin = 100
    yao_bud.set_concept(conceptunit_shop(tue_str, addin=tue_addin), wk_way)
    ball_str = "ball"
    ball_way = yao_bud.make_l1_way(ball_str)
    yao_bud.set_l1_concept(conceptunit_shop(ball_str))
    yao_bud.edit_concept_attr(ball_way, reason_rcontext=tue_way, reason_premise=tue_way)

    wk_popen = 3
    wk_pnigh = 7
    yao_bud.add_fact(wk_way, wk_way, wk_popen, wk_pnigh)

    # assert len(ball_concept._reasonheirs) == 1
    # assert ball_concept._factheirs == {wk_way: wk_factheir}
    # assert ball_concept._factheirs.get(wk_way)
    # assert len(ball_concept._factheirs) == 1
    # assert ball_concept._factheirs.get(tue_way) is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    # wk_factunit = factunit_shop(wk_way, wk_way, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    # x_bud_concept_dict = {wk_concept.get_concept_way(): wk_concept, tue_concept.get_concept_way(): tue_concept}
    # ball_concept.set_reasonheirs(x_bud_concept_dict, tue_reasonheirs)
    x_range_inheritors = {tue_way: wk_way}
    wk_factheir = factheir_shop(wk_way, wk_way, wk_popen, wk_pnigh)

    tue_popen = 113
    tue_pnigh = 117
    tue_factheir = factheir_shop(tue_way, tue_way, tue_popen, tue_pnigh)
    ball_concept = yao_bud.get_concept_obj(ball_way)
    print(f"{wk_way=} {ball_concept._factheirs.keys()=}")
    assert ball_concept._factheirs.get(wk_way) == wk_factheir
    assert len(ball_concept._factheirs) == 2
    assert ball_concept._factheirs == {tue_way: tue_factheir, wk_way: wk_factheir}
