from src.ch03_voice.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom.atom_main import beliefatom_shop, sift_beliefatom
from src.ref.keywords import Ch08Keywords as kw


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_voiceunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(zia_str)

    bob_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    bob_atom.set_arg(kw.voice_name, bob_str)
    zia_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    zia_atom.set_arg(kw.voice_name, zia_str)

    # WHEN
    new_bob_beliefatom = sift_beliefatom(sue_belief, bob_atom)
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_bob_beliefatom
    assert new_bob_beliefatom == bob_atom
    assert not new_zia_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_voice_membership():
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

    bob_run_atom = beliefatom_shop(kw.belief_voice_membership, kw.INSERT)
    bob_run_atom.set_arg(kw.voice_name, bob_str)
    bob_run_atom.set_arg(kw.group_title, run_str)
    yao_run_atom = beliefatom_shop(kw.belief_voice_membership, kw.INSERT)
    yao_run_atom.set_arg(kw.voice_name, yao_str)
    yao_run_atom.set_arg(kw.group_title, run_str)

    # WHEN
    new_bob_run_beliefatom = sift_beliefatom(sue_belief, bob_run_atom)
    new_yao_run_beliefatom = sift_beliefatom(sue_belief, yao_run_atom)

    # THEN
    assert new_bob_run_beliefatom
    assert new_bob_run_beliefatom == bob_run_atom
    assert not new_yao_run_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_planunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    root_rope = sue_belief.planroot.get_plan_rope()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)

    root_atom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    root_atom.set_arg(kw.plan_rope, root_rope)
    casa_atom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    casa_atom.set_arg(kw.plan_rope, casa_rope)
    clean_atom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    clean_atom.set_arg(kw.plan_rope, clean_rope)
    sweep_atom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    sweep_atom.set_arg(kw.plan_rope, sweep_rope)
    assert not sift_beliefatom(sue_belief, root_atom)
    assert sift_beliefatom(sue_belief, casa_atom)
    assert sift_beliefatom(sue_belief, clean_atom)
    assert sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(casa_rope)
    # THEN
    assert not sift_beliefatom(sue_belief, casa_atom)
    assert sift_beliefatom(sue_belief, clean_atom)
    assert sift_beliefatom(sue_belief, sweep_atom)

    # WHEN
    sue_belief.add_plan(clean_rope)
    # THEN
    assert not sift_beliefatom(sue_belief, casa_atom)
    assert not sift_beliefatom(sue_belief, clean_atom)
    assert sift_beliefatom(sue_belief, sweep_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_awardunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = create_xxx_swim_atom(casa_rope, swim_str)
    clean_swim_atom = create_xxx_swim_atom(clean_rope, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(swim_str))

    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_awardunit(awardunit_shop(swim_str))
    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)


def create_xxx_swim_atom(x_rope, swim_str):
    result = beliefatom_shop(kw.belief_plan_awardunit, kw.INSERT)
    result.set_arg(kw.plan_rope, x_rope)
    result.set_arg(kw.awardee_title, swim_str)
    return result


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_reasonunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    wk_rope = sue_belief.make_l1_rope("wk")

    casa_wk_atom = create_wk_atom(casa_rope, wk_rope)
    clean_wk_atom = create_wk_atom(clean_rope, wk_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_reasonunit(reasonunit_shop(wk_rope))
    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert not sift_beliefatom(sue_belief, clean_wk_atom)


def create_wk_atom(casa_rope, wk_rope):
    result = beliefatom_shop(kw.belief_plan_reasonunit, kw.INSERT)
    result.set_arg(kw.plan_rope, casa_rope)
    result.set_arg(kw.reason_context, wk_rope)
    return result


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_reason_caseunit_Exists():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    wk_rope = sue_belief.make_l1_rope("wk")
    thur_str = "thur"
    thur_rope = sue_belief.make_rope(wk_rope, thur_str)

    casa_wk_atom = beliefatom_shop(kw.belief_plan_reason_caseunit, kw.INSERT)
    casa_wk_atom.set_arg(kw.plan_rope, casa_rope)
    casa_wk_atom.set_arg(kw.reason_context, wk_rope)
    casa_wk_atom.set_arg(kw.reason_state, thur_rope)
    clean_wk_atom = beliefatom_shop(kw.belief_plan_reason_caseunit, kw.INSERT)
    clean_wk_atom.set_arg(kw.plan_rope, clean_rope)
    clean_wk_atom.set_arg(kw.reason_context, wk_rope)
    clean_wk_atom.set_arg(kw.reason_state, thur_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    clean_plan = sue_belief.get_plan_obj(clean_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    clean_plan.set_reasonunit(reasonunit_shop(wk_rope))
    assert sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    clean_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert not sift_beliefatom(sue_belief, clean_wk_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_partyunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(kw.belief_plan_partyunit, kw.INSERT)
    casa_swim_atom.set_arg(kw.plan_rope, casa_rope)
    casa_swim_atom.set_arg(kw.party_title, swim_str)
    clean_swim_atom = beliefatom_shop(kw.belief_plan_partyunit, kw.INSERT)
    clean_swim_atom.set_arg(kw.plan_rope, clean_rope)
    clean_swim_atom.set_arg(kw.party_title, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).laborunit.add_party(swim_str)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).laborunit.add_party(swim_str)
    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_healerunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(kw.belief_plan_healerunit, kw.INSERT)
    casa_swim_atom.set_arg(kw.plan_rope, casa_rope)
    casa_swim_atom.set_arg(kw.healer_name, swim_str)
    clean_swim_atom = beliefatom_shop(kw.belief_plan_healerunit, kw.INSERT)
    clean_swim_atom.set_arg(kw.plan_rope, clean_rope)
    clean_swim_atom.set_arg(kw.healer_name, swim_str)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).healerunit.set_healer_name(swim_str)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert sift_beliefatom(sue_belief, clean_swim_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).healerunit.set_healer_name(swim_str)
    # THEN
    assert not sift_beliefatom(sue_belief, casa_swim_atom)
    assert not sift_beliefatom(sue_belief, clean_swim_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_factunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    wk_rope = sue_belief.make_l1_rope("wk")

    casa_wk_atom = beliefatom_shop(kw.belief_plan_factunit, kw.INSERT)
    casa_wk_atom.set_arg(kw.plan_rope, casa_rope)
    casa_wk_atom.set_arg(kw.fact_context, wk_rope)
    clean_wk_atom = beliefatom_shop(kw.belief_plan_factunit, kw.INSERT)
    clean_wk_atom.set_arg(kw.plan_rope, clean_rope)
    clean_wk_atom.set_arg(kw.fact_context, wk_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert sift_beliefatom(sue_belief, clean_wk_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_factunit(factunit_shop(wk_rope))
    # THEN
    assert not sift_beliefatom(sue_belief, casa_wk_atom)
    assert not sift_beliefatom(sue_belief, clean_wk_atom)
