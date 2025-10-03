from src.ch04_voice_logic.group import awardunit_shop
from src.ch05_reason_logic.reason import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_plan_factunit_get_obj,
    belief_plan_reason_caseunit_get_obj as caseunit_get_obj,
    belief_plan_reasonunit_get_obj,
)
from src.ch09_belief_atom_logic._ref.ch09_keywords import Ch09Keywords as wx
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop, sift_beliefatom


def test_sift_atom_ReturnsNoneIfGivenBeliefAtomIsUPDATE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    casa_atom = beliefatom_shop(wx.belief_planunit, wx.UPDATE)
    casa_atom.set_arg(wx.parent_rope, sue_belief.get_nexus_label())
    casa_atom.set_arg(wx.plan_label, casa_str)
    casa_atom.set_arg(wx.star, 8)

    # WHEN
    new_casa_atom = sift_beliefatom(sue_belief, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_beliefunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_bit = 34
    sue_credor_respect = 44
    sue_debtor_respect = 54
    sue_fund_grain = 66
    sue_fund_pool = 69
    sue_max_tree_traverse = 72
    sue_penny = 2
    sue_tally = 100
    zia_atom = beliefatom_shop(wx.beliefunit, wx.INSERT)
    zia_atom.set_arg("respect_grain", sue_bit)
    zia_atom.set_arg("credor_respect", sue_credor_respect)
    zia_atom.set_arg("debtor_respect", sue_debtor_respect)
    zia_atom.set_arg("fund_grain", sue_fund_grain)
    zia_atom.set_arg("fund_pool", sue_fund_pool)
    zia_atom.set_arg("max_tree_traverse", sue_max_tree_traverse)
    zia_atom.set_arg("penny", sue_penny)
    zia_atom.set_arg("tally", sue_tally)

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues == {
        "respect_grain": sue_bit,
        "credor_respect": sue_credor_respect,
        "debtor_respect": sue_debtor_respect,
        "fund_grain": sue_fund_grain,
        "fund_pool": sue_fund_pool,
        "max_tree_traverse": sue_max_tree_traverse,
        "penny": sue_penny,
        "tally": sue_tally,
    }


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_voiceunit():
    # ESTABLISH
    zia_str = "Zia"
    zia_voice_debt_points = 51
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(zia_str)

    zia_atom = beliefatom_shop(wx.belief_voiceunit, wx.INSERT)
    zia_atom.set_arg(wx.voice_name, zia_str)
    zia_atom.set_arg(wx.voice_debt_points, zia_voice_debt_points)

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues == {wx.voice_debt_points: 51}


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_voice_membership():
    # ESTABLISH
    zia_str = "Zia"
    run_str = ";run"
    zia_run_group_debt_points = 76
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(zia_str)
    sue_belief.get_voice(zia_str).add_membership(run_str)

    zia_atom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
    zia_atom.set_arg(wx.voice_name, zia_str)
    zia_atom.set_arg(wx.group_title, run_str)
    zia_atom.set_arg(wx.group_debt_points, zia_run_group_debt_points)

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues == {wx.group_debt_points: zia_run_group_debt_points}


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_planunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)

    sue_addin = 23
    sue_begin = 37
    sue_close = 43
    sue_denom = 47
    sue_gogo_want = 59
    sue_star = 67
    sue_morph = 79
    sue_numor = 83
    sue_pledge = 97
    sue_problem_bool = True
    sue_stop_want = 107
    old_casa_atom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    old_casa_atom.set_arg(wx.plan_rope, casa_rope)
    old_casa_atom.set_arg(wx.addin, sue_addin)
    old_casa_atom.set_arg(wx.begin, sue_begin)
    old_casa_atom.set_arg(wx.close, sue_close)
    old_casa_atom.set_arg(wx.denom, sue_denom)
    old_casa_atom.set_arg(wx.gogo_want, sue_gogo_want)
    old_casa_atom.set_arg(wx.star, sue_star)
    old_casa_atom.set_arg(wx.morph, sue_morph)
    old_casa_atom.set_arg(wx.numor, sue_numor)
    old_casa_atom.set_arg(wx.pledge, sue_pledge)
    old_casa_atom.set_arg("problem_bool", sue_problem_bool)
    old_casa_atom.set_arg(wx.stop_want, sue_stop_want)

    # WHEN
    new_casa_atom = sift_beliefatom(sue_belief, old_casa_atom)

    # THEN
    assert new_casa_atom
    assert new_casa_atom.crud_str == wx.UPDATE
    assert new_casa_atom.get_jvalues_dict()
    zia_jvalues = new_casa_atom.get_jvalues_dict()
    assert zia_jvalues.get(wx.addin) == sue_addin
    assert zia_jvalues.get(wx.begin) == sue_begin
    assert zia_jvalues.get(wx.close) == sue_close
    assert zia_jvalues.get(wx.denom) == sue_denom
    assert zia_jvalues.get(wx.gogo_want) == sue_gogo_want
    assert zia_jvalues.get(wx.star) == sue_star
    assert zia_jvalues.get(wx.morph) == sue_morph
    assert zia_jvalues.get(wx.numor) == sue_numor
    assert zia_jvalues.get(wx.pledge) == sue_pledge
    assert zia_jvalues.get("problem_bool") == sue_problem_bool
    assert zia_jvalues.get(wx.stop_want) == sue_stop_want


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_plan_awardunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    run_str = ";run"
    zia_run_give_force = 72
    zia_run_take_force = 76
    sue_belief.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(run_str, 2, 3))

    zia_atom = beliefatom_shop(wx.belief_plan_awardunit, wx.INSERT)
    zia_atom.set_arg(wx.plan_rope, casa_rope)
    zia_atom.set_arg(wx.awardee_title, run_str)
    zia_atom.set_arg(wx.give_force, zia_run_give_force)
    zia_atom.set_arg(wx.take_force, zia_run_take_force)

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues.get(wx.give_force) == zia_run_give_force
    assert zia_jvalues.get(wx.take_force) == zia_run_take_force


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_plan_reasonunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    week_rope = sue_belief.make_l1_rope(casa_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    new_reason_active_requisite = True
    casa_atom = beliefatom_shop(wx.belief_plan_reasonunit, wx.INSERT)
    casa_atom.set_arg(wx.plan_rope, casa_rope)
    casa_atom.set_arg(wx.reason_context, week_rope)
    casa_atom.set_arg(wx.reason_active_requisite, new_reason_active_requisite)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_reasonunit = belief_plan_reasonunit_get_obj(sue_belief, casa_jkeys)
    assert casa_reasonunit.reason_active_requisite != new_reason_active_requisite
    assert casa_reasonunit.reason_active_requisite is None

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, casa_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    zia_requisite_value = zia_jvalues.get(wx.reason_active_requisite)
    assert zia_requisite_value == new_reason_active_requisite


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_plan_reason_caseunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_rope = sue_belief.make_l1_rope(wx.week)
    thur_str = "thur"
    thur_rope = sue_belief.make_rope(week_rope, thur_str)
    sue_belief.add_plan(clean_rope)
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))
    clean_plan = sue_belief.get_plan_obj(clean_rope)
    clean_plan.set_reasonunit(reasonunit_shop(week_rope))
    clean_plan.get_reasonunit(week_rope).set_case(thur_rope)

    thur_reason_divisor = 39
    thur_atom = beliefatom_shop(wx.belief_plan_reason_caseunit, wx.INSERT)
    thur_atom.set_arg(wx.plan_rope, clean_rope)
    thur_atom.set_arg(wx.reason_context, week_rope)
    thur_atom.set_arg(wx.reason_state, thur_rope)
    assert thur_atom.is_valid()
    thur_atom.set_arg("reason_divisor", thur_reason_divisor)
    thur_jkeys = thur_atom.get_jkeys_dict()
    thur_caseunit = caseunit_get_obj(sue_belief, thur_jkeys)
    assert thur_caseunit.reason_divisor != thur_reason_divisor
    assert thur_caseunit.reason_divisor is None

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, thur_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues.get("reason_divisor") == thur_reason_divisor


def test_sift_atom_ReturnsObj_BeliefAtom_UPDATE_belief_plan_factunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    week_rope = sue_belief.make_l1_rope(wx.week)
    sue_belief.add_plan(casa_rope)
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    casa_fact_lower = 32
    casa_atom = beliefatom_shop(wx.belief_plan_factunit, wx.INSERT)
    casa_atom.set_arg(wx.plan_rope, casa_rope)
    casa_atom.set_arg(wx.fact_context, week_rope)
    casa_atom.set_arg(wx.fact_lower, casa_fact_lower)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_factunit = belief_plan_factunit_get_obj(sue_belief, casa_jkeys)
    assert casa_factunit.fact_lower != casa_fact_lower
    assert casa_factunit.fact_lower is None

    # WHEN
    new_zia_beliefatom = sift_beliefatom(sue_belief, casa_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom.crud_str == wx.UPDATE
    assert new_zia_beliefatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_beliefatom.get_jvalues_dict()
    assert zia_jvalues.get(wx.fact_lower) == casa_fact_lower
