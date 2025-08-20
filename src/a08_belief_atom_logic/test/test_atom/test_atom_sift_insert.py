from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    awardee_title_str,
    belief_partner_membership_str,
    belief_partnerunit_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    fact_context_str,
    group_title_str,
    healer_name_str,
    partner_name_str,
    party_title_str,
    plan_rope_str,
    reason_context_str,
)
from src.a08_belief_atom_logic.atom_main import beliefatom_shop, sift_beliefatom
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_partnerunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(zia_str)

    bob_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    bob_atom.set_arg(partner_name_str(), bob_str)
    zia_atom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    zia_atom.set_arg(partner_name_str(), zia_str)

    # WHEN
    new_bob_beliefatom = sift_beliefatom(sue_belief, bob_atom)
    new_zia_beliefatom = sift_beliefatom(sue_belief, zia_atom)

    # THEN
    assert new_bob_beliefatom
    assert new_bob_beliefatom == bob_atom
    assert not new_zia_beliefatom


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_partner_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    yao_partnerunit = sue_belief.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)
    print(f"{yao_partnerunit._memberships.keys()=}")

    bob_run_atom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
    bob_run_atom.set_arg(partner_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = beliefatom_shop(belief_partner_membership_str(), INSERT_str())
    yao_run_atom.set_arg(partner_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

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
    root_rope = to_rope(sue_belief.coin_label)
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)

    root_atom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    root_atom.set_arg(plan_rope_str(), root_rope)
    casa_atom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    casa_atom.set_arg(plan_rope_str(), casa_rope)
    clean_atom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    clean_atom.set_arg(plan_rope_str(), clean_rope)
    sweep_atom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    sweep_atom.set_arg(plan_rope_str(), sweep_rope)
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

    casa_swim_atom = beliefatom_shop(belief_plan_awardunit_str(), INSERT_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = beliefatom_shop(belief_plan_awardunit_str(), INSERT_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
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


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_reasonunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_belief.make_l1_rope(week_str)

    casa_week_atom = beliefatom_shop(belief_plan_reasonunit_str(), INSERT_str())
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(reason_context_str(), week_rope)
    clean_week_atom = beliefatom_shop(belief_plan_reasonunit_str(), INSERT_str())
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(reason_context_str(), week_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_reasonunit(reasonunit_shop(week_rope))
    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_reason_caseunit_Exists():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_belief.make_l1_rope(week_str)
    thur_str = "thur"
    thur_rope = sue_belief.make_rope(week_rope, thur_str)

    casa_week_atom = beliefatom_shop(belief_plan_reason_caseunit_str(), INSERT_str())
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(reason_context_str(), week_rope)
    casa_week_atom.set_arg("reason_state", thur_rope)
    clean_week_atom = beliefatom_shop(belief_plan_reason_caseunit_str(), INSERT_str())
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(reason_context_str(), week_rope)
    clean_week_atom.set_arg("reason_state", thur_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    clean_plan = sue_belief.get_plan_obj(clean_rope)
    casa_plan.set_reasonunit(reasonunit_shop(week_rope))
    clean_plan.set_reasonunit(reasonunit_shop(week_rope))
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    casa_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    clean_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)


def test_sift_atom_ReturnsObj_BeliefAtom_INSERT_belief_plan_partyunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = beliefatom_shop(belief_plan_partyunit_str(), INSERT_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(party_title_str(), swim_str)
    clean_swim_atom = beliefatom_shop(belief_plan_partyunit_str(), INSERT_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(party_title_str(), swim_str)
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

    casa_swim_atom = beliefatom_shop(belief_plan_healerunit_str(), INSERT_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = beliefatom_shop(belief_plan_healerunit_str(), INSERT_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
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
    week_str = "week"
    week_rope = sue_belief.make_l1_rope(week_str)

    casa_week_atom = beliefatom_shop(belief_plan_factunit_str(), INSERT_str())
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(fact_context_str(), week_rope)
    clean_week_atom = beliefatom_shop(belief_plan_factunit_str(), INSERT_str())
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(fact_context_str(), week_rope)
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    assert sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert sift_beliefatom(sue_belief, clean_week_atom)

    # WHEN
    sue_belief.get_plan_obj(clean_rope).set_factunit(factunit_shop(week_rope))
    # THEN
    assert not sift_beliefatom(sue_belief, casa_week_atom)
    assert not sift_beliefatom(sue_belief, clean_week_atom)
