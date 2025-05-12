from src.a01_way_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_idea import reasonunit_shop, factunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
    acct_name_str,
    awardee_label_str,
    group_label_str,
    team_label_str,
    healer_name_str,
    idea_way_str,
    rcontext_str,
    fcontext_str,
)

from src.a08_bud_atom_logic.atom import atom_insert, budatom_shop, sift_budatom


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_str)

    bob_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = budatom_shop(bud_acctunit_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_budatom = sift_budatom(sue_bud, bob_atom)
    new_zia_budatom = sift_budatom(sue_bud, zia_atom)

    # THEN
    assert new_bob_budatom
    assert new_bob_budatom == bob_atom
    assert not new_zia_budatom


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_acct_membership():
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

    bob_run_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_label_str(), run_str)
    yao_run_atom = budatom_shop(bud_acct_membership_str(), atom_insert())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_label_str(), run_str)

    # WHEN
    new_bob_run_budatom = sift_budatom(sue_bud, bob_run_atom)
    new_yao_run_budatom = sift_budatom(sue_bud, yao_run_atom)

    # THEN
    assert new_bob_run_budatom
    assert new_bob_run_budatom == bob_run_atom
    assert not new_yao_run_budatom


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_ideaunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    root_way = to_way(sue_bud.fisc_tag)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep"
    sweep_way = sue_bud.make_way(clean_way, sweep_str)

    root_atom = budatom_shop(bud_ideaunit_str(), atom_insert())
    root_atom.set_arg(idea_way_str(), root_way)
    casa_atom = budatom_shop(bud_ideaunit_str(), atom_insert())
    casa_atom.set_arg(idea_way_str(), casa_way)
    clean_atom = budatom_shop(bud_ideaunit_str(), atom_insert())
    clean_atom.set_arg(idea_way_str(), clean_way)
    sweep_atom = budatom_shop(bud_ideaunit_str(), atom_insert())
    sweep_atom.set_arg(idea_way_str(), sweep_way)
    assert not sift_budatom(sue_bud, root_atom)
    assert sift_budatom(sue_bud, casa_atom)
    assert sift_budatom(sue_bud, clean_atom)
    assert sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_idea(casa_way)
    # THEN
    assert not sift_budatom(sue_bud, casa_atom)
    assert sift_budatom(sue_bud, clean_atom)
    assert sift_budatom(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_idea(clean_way)
    # THEN
    assert not sift_budatom(sue_bud, casa_atom)
    assert not sift_budatom(sue_bud, clean_atom)
    assert sift_budatom(sue_bud, sweep_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_idea_awardlink_str(), atom_insert())
    casa_swim_atom.set_arg(idea_way_str(), casa_way)
    casa_swim_atom.set_arg(awardee_label_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_idea_awardlink_str(), atom_insert())
    clean_swim_atom.set_arg(idea_way_str(), clean_way)
    clean_swim_atom.set_arg(awardee_label_str(), swim_str)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_way).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_way).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_reasonunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)

    casa_week_atom = budatom_shop(bud_idea_reasonunit_str(), atom_insert())
    casa_week_atom.set_arg(idea_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom = budatom_shop(bud_idea_reasonunit_str(), atom_insert())
    clean_week_atom.set_arg(idea_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_way).set_reasonunit(reasonunit_shop(week_way))

    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_way).set_reasonunit(reasonunit_shop(week_way))
    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_reason_premiseunit_exists():
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

    casa_week_atom = budatom_shop(bud_idea_reason_premiseunit_str(), atom_insert())
    casa_week_atom.set_arg(idea_way_str(), casa_way)
    casa_week_atom.set_arg(rcontext_str(), week_way)
    casa_week_atom.set_arg("pbranch", thur_way)
    clean_week_atom = budatom_shop(bud_idea_reason_premiseunit_str(), atom_insert())
    clean_week_atom.set_arg(idea_way_str(), clean_way)
    clean_week_atom.set_arg(rcontext_str(), week_way)
    clean_week_atom.set_arg("pbranch", thur_way)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    casa_idea = sue_bud.get_idea_obj(casa_way)
    clean_idea = sue_bud.get_idea_obj(clean_way)
    casa_idea.set_reasonunit(reasonunit_shop(week_way))
    clean_idea.set_reasonunit(reasonunit_shop(week_way))
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    casa_idea.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    clean_idea.get_reasonunit(week_way).set_premise(thur_way)

    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_teamlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_idea_teamlink_str(), atom_insert())
    casa_swim_atom.set_arg(idea_way_str(), casa_way)
    casa_swim_atom.set_arg(team_label_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_idea_teamlink_str(), atom_insert())
    clean_swim_atom.set_arg(idea_way_str(), clean_way)
    clean_swim_atom.set_arg(team_label_str(), swim_str)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_way).teamunit.set_teamlink(swim_str)

    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_way).teamunit.set_teamlink(swim_str)
    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    swim_str = "Swim"

    casa_swim_atom = budatom_shop(bud_idea_healerlink_str(), atom_insert())
    casa_swim_atom.set_arg(idea_way_str(), casa_way)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = budatom_shop(bud_idea_healerlink_str(), atom_insert())
    clean_swim_atom.set_arg(idea_way_str(), clean_way)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    assert sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_way).healerlink.set_healer_name(swim_str)

    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert sift_budatom(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_way).healerlink.set_healer_name(swim_str)
    # THEN
    assert not sift_budatom(sue_bud, casa_swim_atom)
    assert not sift_budatom(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_BudAtom_INSERT_bud_idea_factunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = sue_bud.make_way(casa_way, clean_str)
    week_str = "week"
    week_way = sue_bud.make_l1_way(week_str)

    casa_week_atom = budatom_shop(bud_idea_factunit_str(), atom_insert())
    casa_week_atom.set_arg(idea_way_str(), casa_way)
    casa_week_atom.set_arg(fcontext_str(), week_way)
    clean_week_atom = budatom_shop(bud_idea_factunit_str(), atom_insert())
    clean_week_atom.set_arg(idea_way_str(), clean_way)
    clean_week_atom.set_arg(fcontext_str(), week_way)
    sue_bud.add_idea(casa_way)
    sue_bud.add_idea(clean_way)
    assert sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_way).set_factunit(factunit_shop(week_way))

    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert sift_budatom(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_way).set_factunit(factunit_shop(week_way))
    # THEN
    assert not sift_budatom(sue_bud, casa_week_atom)
    assert not sift_budatom(sue_bud, clean_week_atom)
