from src.ch02_rope_logic.rope import to_rope
from src.ch04_voice_logic.group import awardunit_shop
from src.ch05_reason_logic.reason import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic._ref.ch09_keywords import Ch09Keywords as wx
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop, sift_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_DELETE_belief_voiceunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(zia_str)

    bob_atom = beliefatom_shop(wx.belief_voiceunit, wx.DELETE)
    bob_atom.set_arg(wx.voice_name, bob_str)
    zia_atom = beliefatom_shop(wx.belief_voiceunit, wx.DELETE)
    zia_atom.set_arg(wx.voice_name, zia_str)

    # WHEN
    new_bob_beliefatom = sift_beliefatom(sue_belief, bob_atom)
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_zia_beliefatom
    assert new_zia_beliefatom == zia_atom
    assert not new_bob_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_DELETE_belief_voice_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(yao_str)
    sue_belief.add_voiceunit(bob_str)
    yao_voiceunit = sue_belief.get_voice(yao_str)
    yao_voiceunit.add_membership(run_str)
    print(f"{yao_voiceunit.memberships.keys()=}")

    bob_run_atom = beliefatom_shop(wx.belief_voice_membership, wx.DELETE)
    bob_run_atom.set_arg(wx.voice_name, bob_str)
    bob_run_atom.set_arg(wx.group_title, run_str)
    yao_run_atom = beliefatom_shop(wx.belief_voice_membership, wx.DELETE)
    yao_run_atom.set_arg(wx.voice_name, yao_str)
    yao_run_atom.set_arg(wx.group_title, run_str)

    # WHEN
    new_bob_run_beliefatom = sift_beliefatom(sue_belief, bob_run_atom)
    new_yao_run_beliefatom = sift_beliefatom(sue_belief, yao_run_atom)

    # THEN
    assert new_yao_run_beliefatom
    assert new_yao_run_beliefatom == yao_run_atom
    assert not new_bob_run_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_DELETE_belief_planunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    root_rope = sue_belief.planroot.get_plan_rope()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)

    root_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    root_atom.set_arg(wx.plan_rope, root_rope)
    casa_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    casa_atom.set_arg(wx.plan_rope, casa_rope)
    clean_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    clean_atom.set_arg(wx.plan_rope, clean_rope)
    sweep_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    sweep_atom.set_arg(wx.plan_rope, sweep_rope)
    assert sift_beliefatom(sue_belief, root_atom)
    assert not sift_beliefatom(sue_belief, casa_atom)
    assert not sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(casa_rope)
    # THEN
    assert sift_beliefatom(sue_belief, root_atom)
    assert sift_beliefatom(sue_belief, casa_atom)
    assert not sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(clean_rope)
    # THEN
    assert sift_beliefatom(sue_belief, root_atom)
    assert sift_beliefatom(sue_belief, casa_atom)
    assert sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_planunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    root_rope = sue_belief.planroot.get_plan_rope()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)

    casa_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    casa_atom.set_arg(wx.plan_rope, casa_rope)
    clean_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    clean_atom.set_arg(wx.plan_rope, clean_rope)
    sweep_atom = beliefatom_shop(wx.belief_planunit, wx.DELETE)
    sweep_atom.set_arg(wx.plan_rope, sweep_rope)
    assert not sift_beliefatom(sue_belief, casa_atom)
    assert not sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(casa_rope)
    # THEN
    assert sift_beliefatom(sue_belief, casa_atom)
    assert not sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(clean_rope)
    # THEN
    assert sift_beliefatom(sue_belief, casa_atom)
    assert sift_beliefatom(sue_belief, clean_atom)
    assert not sift_beliefatom(sue_belief, sweep_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_awardunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(wx.belief_plan_awardunit, wx.DELETE)
    casa_swim_atom.set_arg(wx.plan_rope, casa_rope)
    casa_swim_atom.set_arg(wx.awardee_title, swim_str)
    clean_swim_atom = beliefatom_shop(wx.belief_plan_awardunit, wx.DELETE)
    clean_swim_atom.set_arg(wx.plan_rope, clean_rope)
    clean_swim_atom.set_arg(wx.awardee_title, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(swim_str))

    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_awardunit(awardunit_shop(swim_str))
    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_reasonunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_rope = sue_belief.make_l1_rope(wx.week)

    casa_week_atom = beliefatom_shop(wx.belief_plan_reasonunit, wx.DELETE)
    casa_week_atom.set_arg(wx.plan_rope, casa_rope)
    casa_week_atom.set_arg(wx.reason_context, week_rope)
    clean_week_atom = beliefatom_shop(wx.belief_plan_reasonunit, wx.DELETE)
    clean_week_atom.set_arg(wx.plan_rope, clean_rope)
    clean_week_atom.set_arg(wx.reason_context, week_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_reasonunit(reasonunit_shop(week_rope))
    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_reason_caseunit_Exists():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_rope = sue_belief.make_l1_rope(wx.week)
    thur_str = "thur"
    thur_rope = sue_belief.make_rope(week_rope, thur_str)

    casa_week_atom = beliefatom_shop(wx.belief_plan_reason_caseunit, wx.DELETE)
    casa_week_atom.set_arg(wx.plan_rope, casa_rope)
    casa_week_atom.set_arg(wx.reason_context, week_rope)
    casa_week_atom.set_arg(wx.reason_state, thur_rope)
    clean_week_atom = beliefatom_shop(wx.belief_plan_reason_caseunit, wx.DELETE)
    clean_week_atom.set_arg(wx.plan_rope, clean_rope)
    clean_week_atom.set_arg(wx.reason_context, week_rope)
    clean_week_atom.set_arg(wx.reason_state, thur_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    clean_plan = sue_belief.get_plan_obj(clean_rope)
    casa_plan.set_reasonunit(reasonunit_shop(week_rope))
    clean_plan.set_reasonunit(reasonunit_shop(week_rope))
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    casa_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    clean_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_partyunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(wx.belief_plan_partyunit, wx.DELETE)
    casa_swim_atom.set_arg(wx.plan_rope, casa_rope)
    casa_swim_atom.set_arg(wx.party_title, swim_str)
    clean_swim_atom = beliefatom_shop(wx.belief_plan_partyunit, wx.DELETE)
    clean_swim_atom.set_arg(wx.plan_rope, clean_rope)
    clean_swim_atom.set_arg(wx.party_title, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).laborunit.add_party(swim_str)

    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).laborunit.add_party(swim_str)
    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_healerunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(wx.belief_plan_healerunit, wx.DELETE)
    casa_swim_atom.set_arg(wx.plan_rope, casa_rope)
    casa_swim_atom.set_arg(wx.healer_name, swim_str)
    clean_swim_atom = beliefatom_shop(wx.belief_plan_healerunit, wx.DELETE)
    clean_swim_atom.set_arg(wx.plan_rope, clean_rope)
    clean_swim_atom.set_arg(wx.healer_name, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).healerunit.set_healer_name(swim_str)

    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).healerunit.set_healer_name(swim_str)
    # THEN
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)


def test_sift_atom_SetsBeliefDeltaBeliefAtom_belief_plan_factunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_rope = sue_belief.make_l1_rope(wx.week)

    casa_week_atom = beliefatom_shop(wx.belief_plan_factunit, wx.DELETE)
    casa_week_atom.set_arg(wx.plan_rope, casa_rope)
    casa_week_atom.set_arg(wx.fact_context, week_rope)
    clean_week_atom = beliefatom_shop(wx.belief_plan_factunit, wx.DELETE)
    clean_week_atom.set_arg(wx.plan_rope, clean_rope)
    clean_week_atom.set_arg(wx.fact_context, week_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_factunit(factunit_shop(week_rope))
    # THEN
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)
