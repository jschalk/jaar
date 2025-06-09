from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    addin_str,
    awardee_title_str,
    begin_str,
    close_str,
    concept_label_str,
    concept_way_str,
    debtit_belief_str,
    debtit_vote_str,
    denom_str,
    fcontext_str,
    fopen_str,
    give_force_str,
    gogo_want_str,
    group_title_str,
    healer_name_str,
    mass_str,
    morph_str,
    numor_str,
    parent_way_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
    rconcept_active_requisite_str,
    rcontext_str,
    stop_want_str,
    take_force_str,
    task_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_tool import (
    plan_concept_factunit_get_obj,
    plan_concept_reason_premiseunit_get_obj as premiseunit_get_obj,
    plan_concept_reasonunit_get_obj,
)
from src.a08_plan_atom_logic._test_util.a08_str import INSERT_str, UPDATE_str
from src.a08_plan_atom_logic.atom import planatom_shop, sift_planatom


def test_sift_atom_ReturnsNoneIfGivenPlanAtomIsUPDATE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    casa_atom = planatom_shop(plan_conceptunit_str(), UPDATE_str())
    casa_atom.set_arg(parent_way_str(), sue_plan.vow_label)
    casa_atom.set_arg(concept_label_str(), casa_str)
    casa_atom.set_arg(mass_str(), 8)
    # THEN
    new_casa_atom = sift_planatom(sue_plan, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_planunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_bit = 34
    sue_credor_respect = 44
    sue_debtor_respect = 54
    sue_fund_iota = 66
    sue_fund_pool = 69
    sue_max_tree_traverse = 72
    sue_penny = 2
    sue_tally = 100
    zia_atom = planatom_shop(planunit_str(), INSERT_str())
    zia_atom.set_arg("respect_bit", sue_bit)
    zia_atom.set_arg("credor_respect", sue_credor_respect)
    zia_atom.set_arg("debtor_respect", sue_debtor_respect)
    zia_atom.set_arg("fund_iota", sue_fund_iota)
    zia_atom.set_arg("fund_pool", sue_fund_pool)
    zia_atom.set_arg("max_tree_traverse", sue_max_tree_traverse)
    zia_atom.set_arg("penny", sue_penny)
    zia_atom.set_arg("tally", sue_tally)

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues == {
        "respect_bit": sue_bit,
        "credor_respect": sue_credor_respect,
        "debtor_respect": sue_debtor_respect,
        "fund_iota": sue_fund_iota,
        "fund_pool": sue_fund_pool,
        "max_tree_traverse": sue_max_tree_traverse,
        "penny": sue_penny,
        "tally": sue_tally,
    }


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_acctunit():
    # ESTABLISH
    zia_str = "Zia"
    zia_debtit_belief = 51
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(zia_str)

    zia_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(debtit_belief_str(), zia_debtit_belief)

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues == {debtit_belief_str(): 51}


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_acct_membership():
    # ESTABLISH
    zia_str = "Zia"
    run_str = ";run"
    zia_run_debtit_vote = 76
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(zia_str)
    sue_plan.get_acct(zia_str).add_membership(run_str)

    zia_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)
    zia_atom.set_arg(group_title_str(), run_str)
    zia_atom.set_arg(debtit_vote_str(), zia_run_debtit_vote)

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues == {debtit_vote_str(): zia_run_debtit_vote}


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_conceptunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)

    sue_addin = 23
    sue_begin = 37
    sue_close = 43
    sue_denom = 47
    sue_gogo_want = 59
    sue_mass = 67
    sue_morph = 79
    sue_numor = 83
    sue_task = 97
    sue_problem_bool = True
    sue_stop_want = 107
    old_casa_atom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    old_casa_atom.set_arg(concept_way_str(), casa_way)
    old_casa_atom.set_arg(addin_str(), sue_addin)
    old_casa_atom.set_arg(begin_str(), sue_begin)
    old_casa_atom.set_arg(close_str(), sue_close)
    old_casa_atom.set_arg(denom_str(), sue_denom)
    old_casa_atom.set_arg(gogo_want_str(), sue_gogo_want)
    old_casa_atom.set_arg(mass_str(), sue_mass)
    old_casa_atom.set_arg(morph_str(), sue_morph)
    old_casa_atom.set_arg(numor_str(), sue_numor)
    old_casa_atom.set_arg(task_str(), sue_task)
    old_casa_atom.set_arg("problem_bool", sue_problem_bool)
    old_casa_atom.set_arg(stop_want_str(), sue_stop_want)
    # THEN
    new_casa_atom = sift_planatom(sue_plan, old_casa_atom)

    # THEN
    assert new_casa_atom
    assert new_casa_atom.crud_str == UPDATE_str()
    assert new_casa_atom.get_jvalues_dict()
    zia_jvalues = new_casa_atom.get_jvalues_dict()
    assert zia_jvalues.get(addin_str()) == sue_addin
    assert zia_jvalues.get(begin_str()) == sue_begin
    assert zia_jvalues.get(close_str()) == sue_close
    assert zia_jvalues.get(denom_str()) == sue_denom
    assert zia_jvalues.get(gogo_want_str()) == sue_gogo_want
    assert zia_jvalues.get(mass_str()) == sue_mass
    assert zia_jvalues.get(morph_str()) == sue_morph
    assert zia_jvalues.get(numor_str()) == sue_numor
    assert zia_jvalues.get(task_str()) == sue_task
    assert zia_jvalues.get("problem_bool") == sue_problem_bool
    assert zia_jvalues.get(stop_want_str()) == sue_stop_want


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_concept_awardlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    run_str = ";run"
    zia_run_give_force = 72
    zia_run_take_force = 76
    sue_plan.get_concept_obj(casa_way).set_awardlink(awardlink_shop(run_str, 2, 3))

    zia_atom = planatom_shop(plan_concept_awardlink_str(), INSERT_str())
    zia_atom.set_arg(concept_way_str(), casa_way)
    zia_atom.set_arg(awardee_title_str(), run_str)
    zia_atom.set_arg(give_force_str(), zia_run_give_force)
    zia_atom.set_arg(take_force_str(), zia_run_take_force)

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues.get(give_force_str()) == zia_run_give_force
    assert zia_jvalues.get(take_force_str()) == zia_run_take_force


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_concept_reasonunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    week_str = "week"
    week_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    sue_plan.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    new_rconcept_active_requisite = True
    casa_atom = planatom_shop(plan_concept_reasonunit_str(), INSERT_str())
    casa_atom.set_arg(concept_way_str(), casa_way)
    casa_atom.set_arg(rcontext_str(), week_way)
    casa_atom.set_arg(rconcept_active_requisite_str(), new_rconcept_active_requisite)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_reasonunit = plan_concept_reasonunit_get_obj(sue_plan, casa_jkeys)
    assert casa_reasonunit.rconcept_active_requisite != new_rconcept_active_requisite
    assert casa_reasonunit.rconcept_active_requisite is None

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, casa_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    zia_requisite_value = zia_jvalues.get(rconcept_active_requisite_str())
    assert zia_requisite_value == new_rconcept_active_requisite


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_concept_reason_premiseunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_plan.make_l1_way(week_str)
    thur_str = "thur"
    thur_way = sue_plan.make_way(week_way, thur_str)
    sue_plan.add_concept(clean_way)
    sue_plan.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))
    clean_concept = sue_plan.get_concept_obj(clean_way)
    clean_concept.set_reasonunit(reasonunit_shop(week_way))
    clean_concept.get_reasonunit(week_way).set_premise(thur_way)

    thur_pdivisor = 39
    thur_atom = planatom_shop(plan_concept_reason_premiseunit_str(), INSERT_str())
    thur_atom.set_arg(concept_way_str(), clean_way)
    thur_atom.set_arg(rcontext_str(), week_way)
    thur_atom.set_arg("pstate", thur_way)
    assert thur_atom.is_valid()
    thur_atom.set_arg("pdivisor", thur_pdivisor)
    thur_jkeys = thur_atom.get_jkeys_dict()
    thur_premiseunit = premiseunit_get_obj(sue_plan, thur_jkeys)
    assert thur_premiseunit.pdivisor != thur_pdivisor
    assert thur_premiseunit.pdivisor is None

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, thur_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues.get("pdivisor") == thur_pdivisor


def test_sift_atom_ReturnsObj_PlanAtom_UPDATE_plan_concept_factunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    week_str = "week"
    week_way = sue_plan.make_l1_way(casa_str)
    sue_plan.add_concept(casa_way)
    sue_plan.get_concept_obj(casa_way).set_factunit(factunit_shop(week_way))

    casa_fopen = 32
    casa_atom = planatom_shop(plan_concept_factunit_str(), INSERT_str())
    casa_atom.set_arg(concept_way_str(), casa_way)
    casa_atom.set_arg(fcontext_str(), week_way)
    casa_atom.set_arg(fopen_str(), casa_fopen)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_factunit = plan_concept_factunit_get_obj(sue_plan, casa_jkeys)
    assert casa_factunit.fopen != casa_fopen
    assert casa_factunit.fopen is None

    # WHEN
    new_zia_planatom = sift_planatom(sue_plan, casa_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom.crud_str == UPDATE_str()
    assert new_zia_planatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_planatom.get_jvalues_dict()
    assert zia_jvalues.get(fopen_str()) == casa_fopen
