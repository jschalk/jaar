from src.bud.group import awardlink_shop
from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_teamlink_text,
    bud_idea_healerlink_text,
    bud_idea_factunit_text,
)
from src.gift.atom import atom_insert, atomunit_shop
from src.gift.atom_config import (
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
)
from src.gift.change import changeunit_shop, sift_changeunit, _sift_atomunit


def test_sift_changeunit_ReturnsObjWithoutUnecessaryINSERT_bud_acctunit():
    # ESTABLISH changeunit with 2 acctunits, changeunit INSERT 3 changeunits,
    # assert changeunit has 3 atoms
    bob_text = "Bob"
    yao_text = "Yao"
    zia_text = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(bob_text)

    accts_changeunit = changeunit_shop()
    bob_atom = atomunit_shop(bud_acctunit_text(), atom_insert())
    bob_atom.set_arg(acct_id_str(), bob_text)
    yao_atom = atomunit_shop(bud_acctunit_text(), atom_insert())
    yao_atom.set_arg(acct_id_str(), yao_text)
    zia_atom = atomunit_shop(bud_acctunit_text(), atom_insert())
    zia_atom.set_arg(acct_id_str(), zia_text)
    accts_changeunit.set_atomunit(bob_atom)
    accts_changeunit.set_atomunit(yao_atom)
    accts_changeunit.set_atomunit(zia_atom)
    assert len(accts_changeunit.get_sorted_atomunits()) == 3
    assert len(sue_bud._accts) == 2

    # WHEN
    new_changeunit = sift_changeunit(accts_changeunit, sue_bud)

    # THEN
    assert len(new_changeunit.get_sorted_atomunits()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_bud_acct_membership():
    # ESTABLISH changeunit with 2 acctunits, changeunit INSERT 3 changeunits,
    # assert changeunit has 3 atoms
    bob_text = "Bob"
    yao_text = "Yao"
    zia_text = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(bob_text)
    yao_acctunit = sue_bud.get_acct(yao_text)
    run_text = ";run"
    run_text = ";run"
    yao_acctunit.add_membership(run_text)
    print(f"{yao_acctunit._memberships.keys()=}")

    accts_changeunit = changeunit_shop()
    bob_run_atom = atomunit_shop(bud_acct_membership_text(), atom_insert())
    bob_run_atom.set_arg(acct_id_str(), bob_text)
    bob_run_atom.set_arg(group_id_str(), run_text)
    yao_run_atom = atomunit_shop(bud_acct_membership_text(), atom_insert())
    yao_run_atom.set_arg(acct_id_str(), yao_text)
    yao_run_atom.set_arg(group_id_str(), run_text)
    zia_run_atom = atomunit_shop(bud_acct_membership_text(), atom_insert())
    zia_run_atom.set_arg(acct_id_str(), zia_text)
    zia_run_atom.set_arg(group_id_str(), run_text)
    accts_changeunit.set_atomunit(bob_run_atom)
    accts_changeunit.set_atomunit(yao_run_atom)
    accts_changeunit.set_atomunit(zia_run_atom)
    print(f"{len(accts_changeunit.get_category_sorted_atomunits_list())=}")
    assert len(accts_changeunit.get_category_sorted_atomunits_list()) == 3

    # WHEN
    new_changeunit = sift_changeunit(accts_changeunit, sue_bud)

    # THEN
    assert len(new_changeunit.get_category_sorted_atomunits_list()) == 2


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_ideaunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_text = "sweep"
    sweep_road = sue_bud.make_road(clean_road, sweep_text)

    root_atom = atomunit_shop(bud_ideaunit_text(), atom_insert())
    root_atom.set_arg(parent_road_str(), "")
    root_atom.set_arg(label_str(), sue_bud._real_id)
    casa_atom = atomunit_shop(bud_ideaunit_text(), atom_insert())
    casa_atom.set_arg(parent_road_str(), sue_bud._real_id)
    casa_atom.set_arg(label_str(), casa_text)
    clean_atom = atomunit_shop(bud_ideaunit_text(), atom_insert())
    clean_atom.set_arg(parent_road_str(), casa_road)
    clean_atom.set_arg(label_str(), clean_text)
    sweep_atom = atomunit_shop(bud_ideaunit_text(), atom_insert())
    sweep_atom.set_arg(parent_road_str(), clean_road)
    sweep_atom.set_arg(label_str(), sweep_text)
    assert not _sift_atomunit(sue_bud, root_atom)
    assert _sift_atomunit(sue_bud, casa_atom)
    assert _sift_atomunit(sue_bud, clean_atom)
    assert _sift_atomunit(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_idea(casa_road)
    # THEN
    assert not _sift_atomunit(sue_bud, casa_atom)
    assert _sift_atomunit(sue_bud, clean_atom)
    assert _sift_atomunit(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_idea(clean_road)
    # THEN
    assert not _sift_atomunit(sue_bud, casa_atom)
    assert not _sift_atomunit(sue_bud, clean_atom)
    assert _sift_atomunit(sue_bud, sweep_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    swim_text = "Swim"

    casa_swim_atom = atomunit_shop(bud_idea_awardlink_text(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(group_id_str(), swim_text)
    clean_swim_atom = atomunit_shop(bud_idea_awardlink_text(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(group_id_str(), swim_text)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    assert _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_text))

    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_road).set_awardlink(awardlink_shop(swim_text))
    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert not _sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_reasonunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    casa_week_atom = atomunit_shop(bud_idea_reasonunit_text(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    clean_week_atom = atomunit_shop(bud_idea_reasonunit_text(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    assert _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_road).set_reasonunit(reasonunit_shop(week_road))
    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert not _sift_atomunit(sue_bud, clean_week_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_reason_premiseunit_exists():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_text = "thur"
    thur_road = sue_bud.make_road(week_road, thur_text)

    casa_week_atom = atomunit_shop(bud_idea_reason_premiseunit_text(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    casa_week_atom.set_arg("need", thur_road)
    clean_week_atom = atomunit_shop(bud_idea_reason_premiseunit_text(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    clean_week_atom.set_arg("need", thur_road)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    clean_idea = sue_bud.get_idea_obj(clean_road)
    casa_idea.set_reasonunit(reasonunit_shop(week_road))
    clean_idea.set_reasonunit(reasonunit_shop(week_road))
    assert _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    casa_idea.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    clean_idea.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert not _sift_atomunit(sue_bud, clean_week_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_teamlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    swim_text = "Swim"

    casa_swim_atom = atomunit_shop(bud_idea_teamlink_text(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(group_id_str(), swim_text)
    clean_swim_atom = atomunit_shop(bud_idea_teamlink_text(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(group_id_str(), swim_text)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    assert _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_road)._teamunit.set_teamlink(swim_text)

    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_road)._teamunit.set_teamlink(swim_text)
    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert not _sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    swim_text = "Swim"

    casa_swim_atom = atomunit_shop(bud_idea_healerlink_text(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(healer_id_str(), swim_text)
    clean_swim_atom = atomunit_shop(bud_idea_healerlink_text(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(healer_id_str(), swim_text)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    assert _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_road)._healerlink.set_healer_id(swim_text)

    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert _sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_road)._healerlink.set_healer_id(swim_text)
    # THEN
    assert not _sift_atomunit(sue_bud, casa_swim_atom)
    assert not _sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_factunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    casa_week_atom = atomunit_shop(bud_idea_factunit_text(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    clean_week_atom = atomunit_shop(bud_idea_factunit_text(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    sue_bud.add_idea(casa_road)
    sue_bud.add_idea(clean_road)
    assert _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert _sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_idea_obj(clean_road).set_factunit(factunit_shop(week_road))
    # THEN
    assert not _sift_atomunit(sue_bud, casa_week_atom)
    assert not _sift_atomunit(sue_bud, clean_week_atom)
