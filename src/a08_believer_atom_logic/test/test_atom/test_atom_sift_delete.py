from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    awardee_title_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    fact_context_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    partner_name_str,
    plan_label_str,
    plan_rope_str,
    reason_context_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop, sift_believeratom
from src.a08_believer_atom_logic.test._util.a08_str import DELETE_str


def test_sift_atom_ReturnsObj_BelieverAtom_DELETE_believer_partnerunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(zia_str)

    bob_atom = believeratom_shop(believer_partnerunit_str(), DELETE_str())
    bob_atom.set_arg(partner_name_str(), bob_str)
    zia_atom = believeratom_shop(believer_partnerunit_str(), DELETE_str())
    zia_atom.set_arg(partner_name_str(), zia_str)

    # WHEN
    new_bob_believeratom = sift_believeratom(sue_believer, bob_atom)
    new_zia_believeratom = sift_believeratom(sue_believer, zia_atom)

    # THEN
    assert new_zia_believeratom
    assert new_zia_believeratom == zia_atom
    assert not new_bob_believeratom


def test_sift_atom_ReturnsObj_BelieverAtom_DELETE_believer_partner_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    yao_partnerunit = sue_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)
    print(f"{yao_partnerunit._memberships.keys()=}")

    bob_run_atom = believeratom_shop(believer_partner_membership_str(), DELETE_str())
    bob_run_atom.set_arg(partner_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = believeratom_shop(believer_partner_membership_str(), DELETE_str())
    yao_run_atom.set_arg(partner_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

    # WHEN
    new_bob_run_believeratom = sift_believeratom(sue_believer, bob_run_atom)
    new_yao_run_believeratom = sift_believeratom(sue_believer, yao_run_atom)

    # THEN
    assert new_yao_run_believeratom
    assert new_yao_run_believeratom == yao_run_atom
    assert not new_bob_run_believeratom


def test_sift_atom_ReturnsObj_BelieverAtom_DELETE_believer_planunit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    root_rope = to_rope(sue_believer.belief_label)
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_believer.make_rope(clean_rope, sweep_str)

    root_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    root_atom.set_arg(plan_rope_str(), root_rope)
    casa_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    casa_atom.set_arg(plan_rope_str(), casa_rope)
    clean_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    clean_atom.set_arg(plan_rope_str(), clean_rope)
    sweep_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    sweep_atom.set_arg(plan_rope_str(), sweep_rope)
    assert sift_believeratom(sue_believer, root_atom)
    assert not sift_believeratom(sue_believer, casa_atom)
    assert not sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)

    # WHEN
    sue_believer.add_plan(casa_rope)
    # THEN
    assert sift_believeratom(sue_believer, root_atom)
    assert sift_believeratom(sue_believer, casa_atom)
    assert not sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)

    # WHEN
    sue_believer.add_plan(clean_rope)
    # THEN
    assert sift_believeratom(sue_believer, root_atom)
    assert sift_believeratom(sue_believer, casa_atom)
    assert sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_planunit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    root_rope = to_rope(sue_believer.belief_label)
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_believer.make_rope(clean_rope, sweep_str)

    casa_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    casa_atom.set_arg(plan_rope_str(), casa_rope)
    clean_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    clean_atom.set_arg(plan_rope_str(), clean_rope)
    sweep_atom = believeratom_shop(believer_planunit_str(), DELETE_str())
    sweep_atom.set_arg(plan_rope_str(), sweep_rope)
    assert not sift_believeratom(sue_believer, casa_atom)
    assert not sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)

    # WHEN
    sue_believer.add_plan(casa_rope)
    # THEN
    assert sift_believeratom(sue_believer, casa_atom)
    assert not sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)

    # WHEN
    sue_believer.add_plan(clean_rope)
    # THEN
    assert sift_believeratom(sue_believer, casa_atom)
    assert sift_believeratom(sue_believer, clean_atom)
    assert not sift_believeratom(sue_believer, sweep_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_awardlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = believeratom_shop(believer_plan_awardlink_str(), DELETE_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = believeratom_shop(believer_plan_awardlink_str(), DELETE_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    assert not sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(clean_rope).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert sift_believeratom(sue_believer, clean_swim_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_reasonunit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_believer.make_l1_rope(week_str)

    casa_week_atom = believeratom_shop(believer_plan_reasonunit_str(), DELETE_str())
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(reason_context_str(), week_rope)
    clean_week_atom = believeratom_shop(believer_plan_reasonunit_str(), DELETE_str())
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(reason_context_str(), week_rope)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    assert not sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    sue_believer.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    sue_believer.get_plan_obj(clean_rope).set_reasonunit(reasonunit_shop(week_rope))
    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert sift_believeratom(sue_believer, clean_week_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_reason_caseunit_exists():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_believer.make_l1_rope(week_str)
    thur_str = "thur"
    thur_rope = sue_believer.make_rope(week_rope, thur_str)

    casa_week_atom = believeratom_shop(
        believer_plan_reason_caseunit_str(), DELETE_str()
    )
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(reason_context_str(), week_rope)
    casa_week_atom.set_arg("reason_state", thur_rope)
    clean_week_atom = believeratom_shop(
        believer_plan_reason_caseunit_str(), DELETE_str()
    )
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(reason_context_str(), week_rope)
    clean_week_atom.set_arg("reason_state", thur_rope)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    clean_plan = sue_believer.get_plan_obj(clean_rope)
    casa_plan.set_reasonunit(reasonunit_shop(week_rope))
    clean_plan.set_reasonunit(reasonunit_shop(week_rope))
    assert not sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    casa_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    clean_plan.get_reasonunit(week_rope).set_case(thur_rope)

    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert sift_believeratom(sue_believer, clean_week_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_laborlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = believeratom_shop(believer_plan_laborlink_str(), DELETE_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(labor_title_str(), swim_str)
    clean_swim_atom = believeratom_shop(believer_plan_laborlink_str(), DELETE_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(labor_title_str(), swim_str)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    assert not sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(casa_rope).laborunit.set_laborlink(swim_str)

    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(clean_rope).laborunit.set_laborlink(swim_str)
    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert sift_believeratom(sue_believer, clean_swim_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_healerlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = believeratom_shop(believer_plan_healerlink_str(), DELETE_str())
    casa_swim_atom.set_arg(plan_rope_str(), casa_rope)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = believeratom_shop(believer_plan_healerlink_str(), DELETE_str())
    clean_swim_atom.set_arg(plan_rope_str(), clean_rope)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    assert not sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(casa_rope).healerlink.set_healer_name(swim_str)

    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert not sift_believeratom(sue_believer, clean_swim_atom)

    # WHEN
    sue_believer.get_plan_obj(clean_rope).healerlink.set_healer_name(swim_str)
    # THEN
    assert sift_believeratom(sue_believer, casa_swim_atom)
    assert sift_believeratom(sue_believer, clean_swim_atom)


def test_sift_atom_SetsBelieverDeltaBelieverAtom_believer_plan_factunit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_believer.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_believer.make_l1_rope(week_str)

    casa_week_atom = believeratom_shop(believer_plan_factunit_str(), DELETE_str())
    casa_week_atom.set_arg(plan_rope_str(), casa_rope)
    casa_week_atom.set_arg(fact_context_str(), week_rope)
    clean_week_atom = believeratom_shop(believer_plan_factunit_str(), DELETE_str())
    clean_week_atom.set_arg(plan_rope_str(), clean_rope)
    clean_week_atom.set_arg(fact_context_str(), week_rope)
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    assert not sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    sue_believer.get_plan_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert not sift_believeratom(sue_believer, clean_week_atom)

    # WHEN
    sue_believer.get_plan_obj(clean_rope).set_factunit(factunit_shop(week_rope))
    # THEN
    assert sift_believeratom(sue_believer, casa_week_atom)
    assert sift_believeratom(sue_believer, clean_week_atom)
