from pytest import raises as pytest_raises
from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factheir_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic._test_util.example_plans import (
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
)
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_clear_concept_dict_and_plan_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_concept_dict = {1: 2, 2: 4}
    sue_plan._rational = x_rational
    sue_plan._tree_traverse_count = x_tree_traverse_count
    sue_plan._concept_dict = x_concept_dict
    sue_plan._offtrack_kids_mass_set = "example"
    sue_plan._reason_rcontexts = {"example2"}
    sue_plan._range_inheritors = {"example2": 1}
    assert sue_plan._rational == x_rational
    assert sue_plan._tree_traverse_count == x_tree_traverse_count
    assert sue_plan._concept_dict == x_concept_dict
    assert sue_plan._offtrack_kids_mass_set != set()
    assert sue_plan._reason_rcontexts != set()
    assert sue_plan._range_inheritors != {}

    # WHEN
    sue_plan._clear_concept_dict_and_plan_obj_settle_attrs()

    # THEN
    assert sue_plan._rational != x_rational
    assert not sue_plan._rational
    assert sue_plan._tree_traverse_count != x_tree_traverse_count
    assert sue_plan._tree_traverse_count == 0
    assert sue_plan._concept_dict != x_concept_dict
    assert sue_plan._concept_dict == {
        sue_plan.conceptroot.get_concept_rope(): sue_plan.conceptroot
    }
    assert sue_plan._offtrack_kids_mass_set == set()
    assert not sue_plan._reason_rcontexts
    assert not sue_plan._range_inheritors


def test_PlanUnit_clear_concept_dict_and_plan_obj_settle_attrs_CorrectlySetsAttrs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerlink_share = 140
    sue_plan._keeps_justified = x_keep_justifed
    sue_plan._keeps_buildable = "swimmers"
    sue_plan._sum_healerlink_share = x_sum_healerlink_share
    sue_plan._keep_dict = {"run": "run"}
    sue_plan._healers_dict = {"run": "run"}
    assert sue_plan._keeps_justified == x_keep_justifed
    assert sue_plan._keeps_buildable
    assert sue_plan._sum_healerlink_share == x_sum_healerlink_share
    assert sue_plan._keep_dict != {}
    assert sue_plan._healers_dict != {}

    # WHEN
    sue_plan._clear_concept_dict_and_plan_obj_settle_attrs()

    # THEN
    assert sue_plan._keeps_justified != x_keep_justifed
    assert sue_plan._keeps_justified
    assert sue_plan._keeps_buildable is False
    assert sue_plan._sum_healerlink_share == 0
    assert not sue_plan._keep_dict
    assert not sue_plan._healers_dict


def test_PlanUnit_settle_plan_ClearsDescendantAttributes():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    # test root status:
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    mon_str = "Monday"
    mon_rope = sue_plan.make_rope(wk_rope, mon_str)
    mon_concept = sue_plan.get_concept_obj(mon_rope)
    assert sue_plan.conceptroot._descendant_task_count is None
    assert sue_plan.conceptroot._all_acct_cred is None
    assert sue_plan.conceptroot._all_acct_debt is None
    assert casa_concept._descendant_task_count is None
    assert casa_concept._all_acct_cred is None
    assert casa_concept._all_acct_debt is None
    assert mon_concept._descendant_task_count is None
    assert mon_concept._all_acct_cred is None
    assert mon_concept._all_acct_debt is None

    sue_plan.conceptroot._descendant_task_count = -2
    sue_plan.conceptroot._all_acct_cred = -2
    sue_plan.conceptroot._all_acct_debt = -2
    casa_concept._descendant_task_count = -2
    casa_concept._all_acct_cred = -2
    casa_concept._all_acct_debt = -2
    mon_concept._descendant_task_count = -2
    mon_concept._all_acct_cred = -2
    mon_concept._all_acct_debt = -2

    assert sue_plan.conceptroot._descendant_task_count == -2
    assert sue_plan.conceptroot._all_acct_cred == -2
    assert sue_plan.conceptroot._all_acct_debt == -2
    assert casa_concept._descendant_task_count == -2
    assert casa_concept._all_acct_cred == -2
    assert casa_concept._all_acct_debt == -2
    assert mon_concept._descendant_task_count == -2
    assert mon_concept._all_acct_cred == -2
    assert mon_concept._all_acct_debt == -2

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan.conceptroot._descendant_task_count == 2
    assert casa_concept._descendant_task_count == 0
    assert mon_concept._descendant_task_count == 0

    assert mon_concept._all_acct_cred is True
    assert mon_concept._all_acct_debt is True
    assert casa_concept._all_acct_cred is True
    assert casa_concept._all_acct_debt is True
    assert sue_plan.conceptroot._all_acct_cred is True
    assert sue_plan.conceptroot._all_acct_debt is True


def test_PlanUnit_settle_plan_RootOnlyCorrectlySetsDescendantAttributes():
    # ESTABLISH
    yao_plan = planunit_shop(owner_name="Yao")
    assert yao_plan.conceptroot._descendant_task_count is None
    assert yao_plan.conceptroot._all_acct_cred is None
    assert yao_plan.conceptroot._all_acct_debt is None

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert yao_plan.conceptroot._descendant_task_count == 0
    assert yao_plan.conceptroot._all_acct_cred is True
    assert yao_plan.conceptroot._all_acct_debt is True


def test_PlanUnit_settle_plan_NLevelCorrectlySetsDescendantAttributes_1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wk_concept = sue_plan.get_concept_obj(wk_rope)
    mon_str = "Monday"
    mon_rope = sue_plan.make_rope(wk_rope, mon_str)
    mon_concept = sue_plan.get_concept_obj(mon_rope)

    email_str = "email"
    email_concept = conceptunit_shop(email_str, task=True)
    sue_plan.set_concept(email_concept, parent_rope=casa_rope)

    # test root status:
    root_rope = to_rope(sue_plan.vow_label)
    x_conceptroot = sue_plan.get_concept_obj(root_rope)
    assert x_conceptroot._descendant_task_count is None
    assert x_conceptroot._all_acct_cred is None
    assert x_conceptroot._all_acct_debt is None
    assert casa_concept._descendant_task_count is None
    assert casa_concept._all_acct_cred is None
    assert casa_concept._all_acct_debt is None
    assert mon_concept._descendant_task_count is None
    assert mon_concept._all_acct_cred is None
    assert mon_concept._all_acct_debt is None

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert x_conceptroot._descendant_task_count == 3
    assert casa_concept._descendant_task_count == 1
    assert casa_concept._kids[email_str]._descendant_task_count == 0
    assert mon_concept._descendant_task_count == 0
    assert x_conceptroot._all_acct_cred is True
    assert x_conceptroot._all_acct_debt is True
    assert casa_concept._all_acct_cred is True
    assert casa_concept._all_acct_debt is True
    assert mon_concept._all_acct_cred is True
    assert mon_concept._all_acct_debt is True


def test_PlanUnit_settle_plan_NLevelCorrectlySetsDescendantAttributes_2():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    email_str = "email"
    casa_str = "casa"
    wk_str = "wkdays"
    mon_str = "Monday"
    tue_str = "Tuesday"
    vacuum_str = "vacuum"
    sue_str = "Sue"

    casa_rope = sue_plan.make_l1_rope(casa_str)
    email_concept = conceptunit_shop(email_str, task=True)
    sue_plan.set_concept(email_concept, parent_rope=casa_rope)
    vacuum_concept = conceptunit_shop(vacuum_str, task=True)
    sue_plan.set_concept(vacuum_concept, parent_rope=casa_rope)

    sue_plan.add_acctunit(acct_name=sue_str)
    x_awardlink = awardlink_shop(awardee_title=sue_str)

    sue_plan.conceptroot._kids[casa_str]._kids[email_str].set_awardlink(
        awardlink=x_awardlink
    )
    # print(sue_plan._kids[casa_str]._kids[email_str])
    # print(sue_plan._kids[casa_str]._kids[email_str]._awardlink)

    # WHEN
    sue_plan.settle_plan()
    # print(sue_plan._kids[casa_str]._kids[email_str])
    # print(sue_plan._kids[casa_str]._kids[email_str]._awardlink)

    # THEN
    assert sue_plan.conceptroot._all_acct_cred is False
    assert sue_plan.conceptroot._all_acct_debt is False
    casa_concept = sue_plan.conceptroot._kids[casa_str]
    assert casa_concept._all_acct_cred is False
    assert casa_concept._all_acct_debt is False
    assert casa_concept._kids[email_str]._all_acct_cred is False
    assert casa_concept._kids[email_str]._all_acct_debt is False
    assert casa_concept._kids[vacuum_str]._all_acct_cred is True
    assert casa_concept._kids[vacuum_str]._all_acct_debt is True
    wk_concept = sue_plan.conceptroot._kids[wk_str]
    assert wk_concept._all_acct_cred is True
    assert wk_concept._all_acct_debt is True
    assert wk_concept._kids[mon_str]._all_acct_cred is True
    assert wk_concept._kids[mon_str]._all_acct_debt is True
    assert wk_concept._kids[tue_str]._all_acct_cred is True
    assert wk_concept._kids[tue_str]._all_acct_debt is True


def test_PlanUnit_settle_plan_SetsConceptUnitAttr_awardlinks():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(zia_str)
    sue_plan.add_acctunit(Xio_str)

    assert len(sue_plan.accts) == 3
    assert len(sue_plan.get_acctunit_group_titles_dict()) == 3
    swim_str = "swim"
    sue_plan.set_l1_concept(conceptunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)
    swim_rope = sue_plan.make_l1_rope(swim_str)
    sue_plan.edit_concept_attr(swim_rope, awardlink=awardlink_yao)
    sue_plan.edit_concept_attr(swim_rope, awardlink=awardlink_zia)
    sue_plan.edit_concept_attr(swim_rope, awardlink=awardlink_Xio)

    street_str = "streets"
    sue_plan.set_concept(conceptunit_shop(street_str), parent_rope=swim_rope)
    assert sue_plan.conceptroot.awardlinks in (None, {})
    assert len(sue_plan.conceptroot._kids[swim_str].awardlinks) == 3

    # WHEN
    sue_plan.settle_plan()

    # THEN
    print(f"{sue_plan._concept_dict.keys()=} ")
    swim_concept = sue_plan._concept_dict.get(swim_rope)
    street_concept = sue_plan._concept_dict.get(
        sue_plan.make_rope(swim_rope, street_str)
    )

    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 3
    assert street_concept.awardlinks in (None, {})
    assert len(street_concept._awardheirs) == 3

    print(f"{len(sue_plan._concept_dict)}")
    print(f"{swim_concept.awardlinks}")
    print(f"{swim_concept._awardheirs}")
    print(f"{swim_concept._awardheirs}")
    assert len(sue_plan.conceptroot._kids["swim"]._awardheirs) == 3


def test_PlanUnit_settle_plan_TreeTraverseSetsClearsAwardLineestorsCorrectly():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    sue_plan.settle_plan()
    # concept tree has no awardlinks
    assert sue_plan.conceptroot._awardlines == {}
    sue_plan.conceptroot._awardlines = {1: "testtest"}
    assert sue_plan.conceptroot._awardlines != {}

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert not sue_plan.conceptroot._awardlines

    # WHEN
    # test for level 1 and level n
    casa_str = "casa"
    casa_concept = sue_plan.conceptroot._kids[casa_str]
    casa_concept._awardlines = {1: "testtest"}
    assert casa_concept._awardlines != {}
    sue_plan.settle_plan()

    # THEN
    assert not sue_plan.conceptroot._kids[casa_str]._awardlines


def test_PlanUnit_settle_plan_DoesNotKeepUnneeded_awardheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_plan.add_acctunit(yao_str)
    yao_plan.add_acctunit(zia_str)
    yao_plan.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_rope = yao_plan.make_l1_rope(swim_str)

    yao_plan.set_l1_concept(conceptunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_concept = yao_plan.get_concept_obj(swim_rope)
    yao_plan.edit_concept_attr(swim_rope, awardlink=awardlink_yao)
    yao_plan.edit_concept_attr(swim_rope, awardlink=awardlink_zia)
    yao_plan.edit_concept_attr(swim_rope, awardlink=awardlink_Xio)

    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 0

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert len(swim_concept.awardlinks) == 3
    assert len(swim_concept._awardheirs) == 3
    yao_plan.edit_concept_attr(swim_rope, awardlink_del=yao_str)
    assert len(swim_concept.awardlinks) == 2
    assert len(swim_concept._awardheirs) == 3

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert len(swim_concept.awardlinks) == 2
    assert len(swim_concept._awardheirs) == 2


def test_PlanUnit_get_concept_tree_ordered_rope_list_ReturnsObj():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "wkdays"
    assert sue_plan.get_concept_tree_ordered_rope_list()

    # WHEN
    ordered_label_list = sue_plan.get_concept_tree_ordered_rope_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_rope_in_ordered_list = sue_plan.get_concept_tree_ordered_rope_list()[0]
    root_rope = to_rope(sue_plan.vow_label)
    assert x_1st_rope_in_ordered_list == root_rope
    x_8th_rope_in_ordered_list = sue_plan.get_concept_tree_ordered_rope_list()[9]
    assert x_8th_rope_in_ordered_list == sue_plan.make_l1_rope(wk_str)

    # WHEN
    y_plan = planunit_shop(vow_label="accord23")

    # THEN
    y_1st_rope_in_ordered_list = y_plan.get_concept_tree_ordered_rope_list()[0]
    assert y_1st_rope_in_ordered_list == root_rope


def test_PlanUnit_get_concept_tree_ordered_rope_list_CorrectlyCleansRangedConceptRopeTerms():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")

    # WHEN
    time_str = "timeline"
    time_rope = yao_plan.make_l1_rope(time_str)
    yao_plan.set_l1_concept(conceptunit_shop(time_str, begin=0, close=700))
    wks_str = "wks"
    yao_plan.set_concept(conceptunit_shop(wks_str, denom=7), time_rope)

    # THEN
    assert len(yao_plan.get_concept_tree_ordered_rope_list()) == 3
    assert (
        len(yao_plan.get_concept_tree_ordered_rope_list(no_range_descendants=True)) == 2
    )


def test_PlanUnit_get_concept_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    sue_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    casa_str = "casa"
    sue_plan.set_l1_concept(conceptunit_shop(casa_str))

    # WHEN
    problems_dict = sue_plan.get_concept_dict(problem=True)

    # THEN
    assert sue_plan._keeps_justified
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_concept = sue_plan.get_concept_obj(texas_rope)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_rope: texas_concept}


def test_PlanUnit_settle_plan_CreatesFullyPopulated_concept_dict():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()

    # WHEN
    sue_planunit.settle_plan()

    # THEN
    assert len(sue_planunit._concept_dict) == 17


def test_PlanUnit_settle_plan_Resets_offtrack_kids_mass_set():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    sue_planunit._offtrack_kids_mass_set = set("ZZ")
    x_set = set()

    assert sue_planunit._offtrack_kids_mass_set != x_set

    # WHEN
    sue_planunit.settle_plan()

    # THEN
    assert sue_planunit._offtrack_kids_mass_set == x_set


def test_PlanUnit_settle_plan_WhenConceptRootHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    casa_concept = conceptunit_shop(casa_str, mass=0)
    sue_planunit.set_l1_concept(casa_concept)
    assert sue_planunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_planunit.settle_plan()

    # THEN
    root_rope = to_rope(sue_planunit.vow_label)
    assert sue_planunit._offtrack_kids_mass_set == {root_rope}

    # WHEN
    sue_planunit.edit_concept_attr(casa_rope, mass=2)
    sue_planunit.settle_plan()

    # THEN
    assert sue_planunit._offtrack_kids_mass_set == set()


def test_PlanUnit_settle_plan_WhenConceptUnitHas_massButAll_kidsHaveZero_massAddTo_offtrack_kids_mass_set():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_planunit.make_l1_rope(casa_str)
    casa_concept = conceptunit_shop(casa_str, mass=1)

    swim_str = "swimming"
    swim_rope = sue_planunit.make_rope(casa_rope, swim_str)
    swim_concept = conceptunit_shop(swim_str, mass=8)

    clean_str = "cleaning"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    clean_concept = conceptunit_shop(clean_str, mass=2)
    sue_planunit.set_concept(conceptunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_planunit.make_rope(clean_rope, sweep_str)
    sweep_concept = conceptunit_shop(sweep_str, mass=0)
    vaccum_str = "vaccum"
    vaccum_rope = sue_planunit.make_rope(clean_rope, vaccum_str)
    vaccum_concept = conceptunit_shop(vaccum_str, mass=0)

    sue_planunit.set_l1_concept(casa_concept)
    sue_planunit.set_concept(swim_concept, casa_rope)
    sue_planunit.set_concept(clean_concept, casa_rope)
    sue_planunit.set_concept(sweep_concept, clean_rope)  # _mass=0
    sue_planunit.set_concept(vaccum_concept, clean_rope)  # _mass=0

    assert sue_planunit._offtrack_kids_mass_set == set()

    # WHEN
    sue_planunit.settle_plan()

    # THEN
    assert sue_planunit._offtrack_kids_mass_set == {clean_rope}


def test_PlanUnit_settle_plan_CreatesNewGroupUnitsWhenNeeded_Scenario0():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    zia_str = "Zia"
    yao_credit_score = 3
    yao_debt_score = 2
    zia_credit_score = 4
    zia_debt_score = 5
    yao_plan.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    yao_plan.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    root_rope = to_rope(yao_plan.vow_label)
    x_conceptroot = yao_plan.get_concept_obj(root_rope)
    x_conceptroot.set_awardlink(awardlink_shop(yao_str))
    x_conceptroot.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    x_conceptroot.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 2
    assert not yao_plan.groupunit_exists(yao_str)
    assert not yao_plan.groupunit_exists(zia_str)
    assert not yao_plan.groupunit_exists(xio_str)

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert yao_plan.groupunit_exists(yao_str)
    assert yao_plan.groupunit_exists(zia_str)
    assert yao_plan.groupunit_exists(xio_str)
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 2
    assert len(yao_plan.get_acctunit_group_titles_dict()) != len(yao_plan._groupunits)
    assert len(yao_plan._groupunits) == 3
    xio_groupunit = yao_plan.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_plan.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)
    yao_membership = xio_groupunit.get_membership(yao_str)
    zia_membership = xio_groupunit.get_membership(zia_str)
    assert yao_membership.credit_vote == yao_credit_score
    assert zia_membership.credit_vote == zia_credit_score
    assert yao_membership.debt_vote == yao_debt_score
    assert zia_membership.debt_vote == zia_debt_score


def test_PlanUnit_settle_plan_CreatesNewGroupUnitsWhenNeeded_Scenario1():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_plan.make_l1_rope(swim_str)
    yao_plan.set_l1_concept(conceptunit_shop(swim_str))
    zia_str = "Zia"
    yao_plan.add_acctunit(yao_str)
    yao_plan.add_acctunit(zia_str)
    swim_concept = yao_plan.get_concept_obj(swim_rope)
    swim_concept.set_awardlink(awardlink_shop(yao_str))
    swim_concept.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_concept.set_awardlink(awardlink_shop(xio_str))
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 2
    assert not yao_plan.groupunit_exists(yao_str)
    assert not yao_plan.groupunit_exists(zia_str)
    assert not yao_plan.groupunit_exists(xio_str)

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert yao_plan.groupunit_exists(yao_str)
    assert yao_plan.groupunit_exists(zia_str)
    assert yao_plan.groupunit_exists(xio_str)
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 2
    assert len(yao_plan.get_acctunit_group_titles_dict()) != len(yao_plan._groupunits)
    assert len(yao_plan._groupunits) == 3
    xio_groupunit = yao_plan.get_groupunit(xio_str)
    xio_symmerty_groupunit = yao_plan.create_symmetry_groupunit(xio_str)
    assert (
        xio_groupunit._memberships.keys() == xio_symmerty_groupunit._memberships.keys()
    )
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert not xio_groupunit.membership_exists(xio_str)


def test_PlanUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    swim_str = "swim"
    swim_rope = yao_plan.make_l1_rope(swim_str)
    yao_plan.set_l1_concept(conceptunit_shop(swim_str))
    zia_str = "Zia"
    yao_plan.add_acctunit(yao_str)
    yao_plan.add_acctunit(zia_str)
    swim_concept = yao_plan.get_concept_obj(swim_rope)
    swim_concept.set_awardlink(awardlink_shop(yao_str))
    swim_concept.set_awardlink(awardlink_shop(zia_str))
    xio_str = "Xio"
    swim_concept.set_awardlink(awardlink_shop(xio_str))
    yao_plan.settle_plan()
    assert yao_plan.groupunit_exists(yao_str)
    assert yao_plan.groupunit_exists(zia_str)
    assert yao_plan.groupunit_exists(xio_str)
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 2
    assert len(yao_plan.get_acctunit_group_titles_dict()) != len(yao_plan._groupunits)

    # WHEN
    symmerty_group_titles = yao_plan.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {xio_str}

    # ESTABLISH
    run_str = ";Run"
    swim_concept.set_awardlink(awardlink_shop(run_str))
    assert not yao_plan.groupunit_exists(run_str)
    yao_plan.settle_plan()
    assert yao_plan.groupunit_exists(run_str)

    # WHEN
    symmerty_group_titles = yao_plan.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {xio_str, run_str}


def test_PlanUnit_settle_plan_Sets_conceptroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_plan.make_l1_rope(wk_str)
    wk_addin = 10
    wk_concept = conceptunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_plan.set_l1_concept(wk_concept)
    tue_str = "Tue"
    tue_rope = yao_plan.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_plan.set_concept(conceptunit_shop(tue_str, addin=tue_addin), wk_rope)
    root_rope = to_rope(yao_plan.vow_label)
    yao_plan.edit_concept_attr(
        root_rope, reason_rcontext=tue_rope, reason_premise=tue_rope
    )

    wk_popen = 3
    wk_pnigh = 7
    yao_plan.add_fact(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # assert len(ball_concept._reasonheirs) == 1
    # assert ball_concept._factheirs == {wk_rope: wk_factheir}
    # assert ball_concept._factheirs.get(wk_rope)
    # assert len(ball_concept._factheirs) == 1
    # assert ball_concept._factheirs.get(tue_rope) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_plan.settle_plan()
    exception_str = f"Cannot have fact for range inheritor '{tue_rope}'. A ranged fact concept must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_plan_concept_dict = {wk_concept.get_concept_rope(): wk_concept, tue_concept.get_concept_rope(): tue_concept}
    # ball_concept.set_reasonheirs(x_plan_concept_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_rope: wk_rope}
    # wk_factheir = factheir_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # tue_popen = 113
    # tue_pnigh = 117
    # tue_factheir = factheir_shop(tue_rope, tue_rope, tue_popen, tue_pnigh)
    # root_concept = yao_plan.get_concept_obj(root_rope)
    # print(f"{wk_rope=} {root_concept._factheirs.keys()=}")
    # assert root_concept._factheirs.get(wk_rope) == wk_factheir
    # assert len(root_concept._factheirs) == 2
    # assert root_concept._factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_PlanUnit_settle_plan_SetsConceptUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    wk_str = "wk"
    wk_rope = yao_plan.make_l1_rope(wk_str)
    wk_addin = 10
    wk_concept = conceptunit_shop(wk_str, begin=10, close=15, addin=wk_addin)
    yao_plan.set_l1_concept(wk_concept)
    tue_str = "Tue"
    tue_rope = yao_plan.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_plan.set_concept(conceptunit_shop(tue_str, addin=tue_addin), wk_rope)
    ball_str = "ball"
    ball_rope = yao_plan.make_l1_rope(ball_str)
    yao_plan.set_l1_concept(conceptunit_shop(ball_str))
    yao_plan.edit_concept_attr(
        ball_rope, reason_rcontext=tue_rope, reason_premise=tue_rope
    )

    wk_popen = 3
    wk_pnigh = 7
    yao_plan.add_fact(wk_rope, wk_rope, wk_popen, wk_pnigh)

    # assert len(ball_concept._reasonheirs) == 1
    # assert ball_concept._factheirs == {wk_rope: wk_factheir}
    # assert ball_concept._factheirs.get(wk_rope)
    # assert len(ball_concept._factheirs) == 1
    # assert ball_concept._factheirs.get(tue_rope) is None

    # WHEN
    yao_plan.settle_plan()

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_plan_concept_dict = {wk_concept.get_concept_rope(): wk_concept, tue_concept.get_concept_rope(): tue_concept}
    # ball_concept.set_reasonheirs(x_plan_concept_dict, tue_reasonheirs)
    x_range_inheritors = {tue_rope: wk_rope}
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_popen, wk_pnigh)

    tue_popen = 113
    tue_pnigh = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_popen, tue_pnigh)
    ball_concept = yao_plan.get_concept_obj(ball_rope)
    print(f"{wk_rope=} {ball_concept._factheirs.keys()=}")
    assert ball_concept._factheirs.get(wk_rope) == wk_factheir
    assert len(ball_concept._factheirs) == 2
    assert ball_concept._factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}
