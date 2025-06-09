from src.a01_term_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_way_str,
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
from src.a08_plan_atom_logic._test_util.a08_str import INSERT_str
from src.a08_plan_atom_logic.atom import planatom_shop, sift_planatom


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(zia_str)

    bob_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = planatom_shop(plan_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_planatom = sift_planatom(sue_plan, bob_atom)
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_bob_planatom
    assert new_bob_planatom == bob_atom
    assert not new_zia_planatom


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_acct_membership():
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

    bob_run_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

    # WHEN
    new_bob_run_planatom = sift_planatom(sue_plan, bob_run_atom)
    new_yao_run_planatom = sift_planatom(sue_plan, yao_run_atom)

    # THEN
    assert new_bob_run_planatom
    assert new_bob_run_planatom == bob_run_atom
    assert not new_yao_run_planatom


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_conceptunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    root_way = to_way(sue_plan.vow_label)
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    sweep_str = "sweep"
    sweep_way = sue_plan.make_way(clean_way, sweep_str)

    root_atom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    root_atom.set_arg(concept_way_str(), root_way)
    casa_atom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    casa_atom.set_arg(concept_way_str(), casa_way)
    clean_atom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    clean_atom.set_arg(concept_way_str(), clean_way)
    sweep_atom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    sweep_atom.set_arg(concept_way_str(), sweep_way)
    assert not sift_planatom(sue_plan, root_atom)
    assert sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(casa_way)
    # THEN
    assert not sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_concept(clean_way)
    # THEN
    assert not sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_awardlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_awardlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_awardlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_way).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_reasonunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_plan.make_l1_way(week_str)

    casa_week_atom = planatom_shop(plan_concept_reasonunit_str(), INSERT_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom = planatom_shop(plan_concept_reasonunit_str(), INSERT_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_way).set_reasonunit(reasonunit_shop(week_way))
    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_reason_premiseunit_exists():
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

    casa_week_atom = planatom_shop(plan_concept_reason_premiseunit_str(), INSERT_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    casa_week_atom.set_arg("pstate", thur_way)
    clean_week_atom = planatom_shop(plan_concept_reason_premiseunit_str(), INSERT_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom.set_arg("pstate", thur_way)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    casa_concept = sue_plan.get_concept_obj(casa_way)
    clean_concept = sue_plan.get_concept_obj(clean_way)
    casa_concept.set_reasonunit(reasonunit_shop(week_way))
    clean_concept.set_reasonunit(reasonunit_shop(week_way))
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    casa_concept.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    clean_concept.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_laborlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_laborlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(labor_title_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_laborlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(labor_title_str(), swim_str)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_way).laborunit.set_laborlink(swim_str)

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_way).laborunit.set_laborlink(swim_str)
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_healerlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(plan_concept_healerlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = planatom_shop(plan_concept_healerlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_way).healerlink.set_healer_name(swim_str)

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_way).healerlink.set_healer_name(swim_str)
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_concept_factunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_plan.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_plan.make_l1_way(week_str)

    casa_week_atom = planatom_shop(plan_concept_factunit_str(), INSERT_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(fcontext_str(), week_way)
    clean_week_atom = planatom_shop(plan_concept_factunit_str(), INSERT_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(fcontext_str(), week_way)
    sue_plan.add_concept(casa_way)
    sue_plan.add_concept(clean_way)
    assert sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(casa_way).set_factunit(factunit_shop(week_way))

    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert sift_planatom(sue_plan, clean_week_atom)

    # WHEN
    sue_plan.get_concept_obj(clean_way).set_factunit(factunit_shop(week_way))
    # THEN
    assert not sift_planatom(sue_plan, casa_week_atom)
    assert not sift_planatom(sue_plan, clean_week_atom)
