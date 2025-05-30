from src.a01_term_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import reasonunit_shop, factunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    acct_name_str,
    awardee_title_str,
    group_title_str,
    labor_title_str,
    healer_name_str,
    concept_label_str,
    concept_way_str,
    rcontext_str,
    fcontext_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import DELETE_str
from src.a08_bud_atom_logic.atom import budatom_shop, sift_budatom


def test_sift_atom_ReturnsObj_BudAtom_DELETE_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_str)

    bob_atom = budatom_shop(bud_acctunit_str(), DELETE_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = budatom_shop(bud_acctunit_str(), DELETE_str())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_budatom = sift_budatom(sue_bud, bob_atom)
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_zia_budatom
    assert new_zia_budatom == zia_atom
    assert not new_bob_budatom


def test_sift_atom_ReturnsObj_BudAtom_DELETE_bud_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    bob_run_atom = budatom_shop(bud_acct_membership_str(), DELETE_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = budatom_shop(bud_acct_membership_str(), DELETE_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

    # WHEN
    new_bob_run_budatom = sift_budatom(sue_bud, bob_run_atom)
    new_yao_run_budatom = sift_budatom(sue_bud, yao_run_atom)

    # THEN
    assert new_yao_run_budatom
    assert new_yao_run_budatom == yao_run_atom
    assert not new_bob_run_budatom


def test_sift_atom_ReturnsObj_BudAtom_DELETE_bud_conceptunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    root_way = to_way(sue_bud.fisc_label)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep"
    sweep_way = sue_bud.make_way(clean_way, sweep_str)

    root_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    root_atom.set_arg(concept_way_str(), root_way)
    casa_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    casa_atom.set_arg(concept_way_str(), casa_way)
    clean_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    clean_atom.set_arg(concept_way_str(), clean_way)
    sweep_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    sweep_atom.set_arg(concept_way_str(), sweep_way)
    assert sift_budatom(sue_bud, root_atom)
    assert not sift_budatom(sue_bud, casa_atom)
    assert not sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_concept(casa_way)
    # THEN
    assert sift_budatom(sue_bud, root_atom)
    assert sift_budatom(sue_bud, casa_atom)
    assert not sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_concept(clean_way)
    # THEN
    assert sift_budatom(sue_bud, root_atom)
    assert sift_budatom(sue_bud, casa_atom)
    assert sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_conceptunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    root_way = to_way(sue_bud.fisc_label)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep"
    sweep_way = sue_bud.make_way(clean_way, sweep_str)

    casa_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    casa_atom.set_arg(concept_way_str(), casa_way)
    clean_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    clean_atom.set_arg(concept_way_str(), clean_way)
    sweep_atom = budatom_shop(bud_conceptunit_str(), DELETE_str())
    sweep_atom.set_arg(concept_way_str(), sweep_way)
    assert not sift_budatom(sue_bud, casa_atom)
    assert not sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_concept(casa_way)
    # THEN
    assert sift_budatom(sue_bud, casa_atom)
    assert not sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_concept(clean_way)
    # THEN
    assert sift_budatom(sue_bud, casa_atom)
    assert sift_budatom(sue_bud, clean_atom)
    assert not sift_budatom(sue_bud, sweep_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_concept_awardlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_concept_awardlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(clean_way).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_reasonunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)

    casa_week_atom = budatom_shop(bud_concept_reasonunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom = budatom_shop(bud_concept_reasonunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_concept_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_concept_obj(clean_way).set_reasonunit(reasonunit_shop(week_way))
    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_reason_premiseunit_exists():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)
    thur_str = "thur"
    thur_way = sue_bud.make_way(week_way, thur_str)

    casa_week_atom = budatom_shop(bud_concept_reason_premiseunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    casa_week_atom.set_arg("pstate", thur_way)
    clean_week_atom = budatom_shop(bud_concept_reason_premiseunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom.set_arg("pstate", thur_way)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    casa_concept = sue_bud.get_concept_obj(casa_way)
    clean_concept = sue_bud.get_concept_obj(clean_way)
    casa_concept.set_reasonunit(reasonunit_shop(week_way))
    clean_concept.set_reasonunit(reasonunit_shop(week_way))
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    casa_concept.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    clean_concept.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_laborlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_concept_laborlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(labor_title_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_concept_laborlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(labor_title_str(), swim_str)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(casa_way).laborunit.set_laborlink(swim_str)

    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(clean_way).laborunit.set_laborlink(swim_str)
    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_concept_healerlink_str(), DELETE_str())
    casa_swim_atom.set_arg(concept_way_str(), casa_way)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_concept_healerlink_str(), DELETE_str())
    clean_swim_atom.set_arg(concept_way_str(), clean_way)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(casa_way).healerlink.set_healer_name(swim_str)

    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_concept_obj(clean_way).healerlink.set_healer_name(swim_str)
    # THEN
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_SetsBudDeltaBudAtom_bud_concept_factunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)

    casa_week_atom = budatom_shop(bud_concept_factunit_str(), DELETE_str())
    casa_week_atom.set_arg(concept_way_str(), casa_way)
    casa_week_atom.set_arg(fcontext_str(), week_way)
    clean_week_atom = budatom_shop(bud_concept_factunit_str(), DELETE_str())
    clean_week_atom.set_arg(concept_way_str(), clean_way)
    clean_week_atom.set_arg(fcontext_str(), week_way)
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_concept_obj(casa_way).set_factunit(factunit_shop(week_way))

    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_concept_obj(clean_way).set_factunit(factunit_shop(week_way))
    # THEN
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)
