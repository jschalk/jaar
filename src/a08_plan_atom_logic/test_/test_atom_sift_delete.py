from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_plan_logic._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_label_str,
    concept_rope_str,
    fcontext_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    rcontext_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._util.a08_str import DELETE_str
from src.a08_plan_atom_logic.atom import planatom_shop, sift_planatom


def test_sift_atom_ReturnsObj_PlanAtom_DELETE_plan_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(zia_str)

    bob_atom = planatom_shop(plan_acctunit_str(), DELETE_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = planatom_shop(plan_acctunit_str(), DELETE_str())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_planatom = sift_planatom(sue_plan, bob_atom)
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_zia_planatom
    assert new_zia_planatom == zia_atom
    assert not new_bob_planatom


def test_sift_atom_ReturnsObj_PlanAtom_DELETE_plan_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    yao_acctunit = sue_plan.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    bob_run_atom = planatom_shop(plan_acct_membership_str(), DELETE_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = planatom_shop(plan_acct_membership_str(), DELETE_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

    # WHEN
    new_bob_run_planatom = sift_planatom(sue_plan, bob_run_atom)
    new_yao_run_planatom = sift_planatom(sue_plan, yao_run_atom)

    # THEN
    assert new_yao_run_planatom
    assert new_yao_run_planatom == yao_run_atom
    assert not new_bob_run_planatom


def test_sift_atom_ReturnsObj_PlanAtom_DELETE_plan_conceptunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    root_rope = to_rope(sue_plan.vow_label)
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)

    root_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    root_atom.set_arg(concept_rope_str(), root_rope)
    casa_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    casa_atom.set_arg(concept_rope_str(), casa_rope)
    clean_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    clean_atom.set_arg(concept_rope_str(), clean_rope)
    sweep_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    sweep_atom.set_arg(concept_rope_str(), sweep_rope)
    assert sift_planatom(sue_plan, root_atom)
    assert not sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(casa_rope)
    # THEN
    assert sift_planatom(sue_plan, root_atom)
    assert sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(clean_rope)
    # THEN
    assert sift_planatom(sue_plan, root_atom)
    assert sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_conceptunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    root_rope = to_rope(sue_plan.vow_label)
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)

    casa_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    casa_atom.set_arg(concept_rope_str(), casa_rope)
    clean_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    clean_atom.set_arg(concept_rope_str(), clean_rope)
    sweep_atom = planatom_shop(plan_conceptunit_str(), DELETE_str())
    sweep_atom.set_arg(concept_rope_str(), sweep_rope)
    assert not sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(casa_rope)
    # THEN
    assert sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(clean_rope)
    # THEN
    assert sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert not sift_planatom(sue_plan, sweep_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_awardlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_awardlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_awardlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_rope).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_reasonunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_plan.make_l1_rope(week_str)

    casa_week_atom = planatom_shop(plan_concept_reasonunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(rcontext_str(), week_rope)
    clean_week_atom = planatom_shop(plan_concept_reasonunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(rcontext_str(), week_rope)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_rope).set_reasonunit(reasonunit_shop(week_rope))
    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_reason_premiseunit_exists():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_plan.make_l1_rope(week_str)
    thur_str = "thur"
    thur_rope = sue_plan.make_rope(week_rope, thur_str)

    casa_week_atom = planatom_shop(plan_concept_reason_premiseunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(rcontext_str(), week_rope)
    casa_week_atom.set_arg("pstate", thur_rope)
    clean_week_atom = planatom_shop(plan_concept_reason_premiseunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(rcontext_str(), week_rope)
    clean_week_atom.set_arg("pstate", thur_rope)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    clean_concept = sue_plan.get_concept_obj(clean_rope)
    casa_concept.set_reasonunit(reasonunit_shop(week_rope))
    clean_concept.set_reasonunit(reasonunit_shop(week_rope))
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    casa_concept.get_reasonunit(week_rope).set_premise(thur_rope)

    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    clean_concept.get_reasonunit(week_rope).set_premise(thur_rope)

    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_laborlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_laborlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(labor_title_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_laborlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(labor_title_str(), swim_str)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_rope).laborunit.set_laborlink(swim_str)

    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_rope).laborunit.set_laborlink(swim_str)
    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_healerlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_healerlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_healerlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_rope).healerlink.set_healer_name(swim_str)

    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_rope).healerlink.set_healer_name(swim_str)
    # THEN
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_SetsPlanDeltaPlanAtom_plan_concept_factunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_plan.make_l1_rope(week_str)

    casa_week_atom = planatom_shop(plan_concept_factunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(fcontext_str(), week_rope)
    clean_week_atom = planatom_shop(plan_concept_factunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(fcontext_str(), week_rope)
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_rope).set_factunit(factunit_shop(week_rope))
    # THEN
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)
