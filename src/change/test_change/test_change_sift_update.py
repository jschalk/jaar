from src.bud.group import awardlink_shop
from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)
from src.change.atom import atom_insert, atom_update, atomunit_shop, sift_atomunit
from src.change.atom_config import (
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.change.change import changeunit_shop, sift_changeunit


def test_sift_changeunit_ReturnsObjUPDATEAtomUnit_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_credit_belief = 34
    new_bob_credit_belief = 7
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(bob_str, old_bob_credit_belief)
    sue_bud.add_acctunit(yao_str)

    accts_changeunit = changeunit_shop()
    bob_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_id_str(), bob_str)
    bob_atom.set_arg(credit_belief_str(), new_bob_credit_belief)
    yao_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    yao_atom.set_arg(acct_id_str(), yao_str)
    accts_changeunit.set_atomunit(bob_atom)
    accts_changeunit.set_atomunit(yao_atom)
    assert len(accts_changeunit.get_sorted_atomunits()) == 2

    # WHEN
    new_changeunit = sift_changeunit(accts_changeunit, sue_bud)

    # THEN
    assert len(new_changeunit.get_sorted_atomunits()) == 1
    new_atomunit = new_changeunit.get_sorted_atomunits()[0]
    assert new_atomunit.crud_str == atom_update()
    new_optional_args = new_atomunit.get_optional_args_dict()
    assert new_optional_args == {credit_belief_str(): new_bob_credit_belief}


# def test_sift_changeunit_ReturnsObjUPDATEAtomUnit_bud_acctunit():
#     # ESTABLISH
#     bob_str = "Bob"
#     yao_str = "Yao"
#     zia_str = "Zia"
#     sue_bud = budunit_shop("Sue")
#     sue_bud.add_acctunit(yao_str)
#     sue_bud.add_acctunit(bob_str)
#     yao_acctunit = sue_bud.get_acct(yao_str)
#     run_str = ";run"
#     yao_acctunit.add_membership(run_str)
#     print(f"{yao_acctunit._memberships.keys()=}")

#     accts_changeunit = changeunit_shop()
#     bob_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
#     bob_run_atom.set_arg(acct_id_str(), bob_str)
#     bob_run_atom.set_arg(group_id_str(), run_str)
#     yao_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
#     yao_run_atom.set_arg(acct_id_str(), yao_str)
#     yao_run_atom.set_arg(group_id_str(), run_str)
#     zia_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
#     zia_run_atom.set_arg(acct_id_str(), zia_str)
#     zia_run_atom.set_arg(group_id_str(), run_str)
#     accts_changeunit.set_atomunit(bob_run_atom)
#     accts_changeunit.set_atomunit(yao_run_atom)
#     accts_changeunit.set_atomunit(zia_run_atom)
#     print(f"{len(accts_changeunit.get_category_sorted_atomunits_list())=}")
#     assert len(accts_changeunit.get_category_sorted_atomunits_list()) == 3

#     # WHEN
#     new_changeunit = sift_changeunit(accts_changeunit, sue_bud)

#     # THEN
#     assert len(new_changeunit.get_category_sorted_atomunits_list()) == 2


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_ideaunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     sweep_str = "sweep"
#     sweep_road = sue_bud.make_road(clean_road, sweep_str)

#     root_atom = atomunit_shop(bud_ideaunit_str(), atom_insert())
#     root_atom.set_arg(parent_road_str(), "")
#     root_atom.set_arg(label_str(), sue_bud._tribe_id)
#     casa_atom = atomunit_shop(bud_ideaunit_str(), atom_insert())
#     casa_atom.set_arg(parent_road_str(), sue_bud._tribe_id)
#     casa_atom.set_arg(label_str(), casa_str)
#     clean_atom = atomunit_shop(bud_ideaunit_str(), atom_insert())
#     clean_atom.set_arg(parent_road_str(), casa_road)
#     clean_atom.set_arg(label_str(), clean_str)
#     sweep_atom = atomunit_shop(bud_ideaunit_str(), atom_insert())
#     sweep_atom.set_arg(parent_road_str(), clean_road)
#     sweep_atom.set_arg(label_str(), sweep_str)
#     assert not  sift_atomunit(sue_bud, root_atom)
#     assert  sift_atomunit(sue_bud, casa_atom)
#     assert  sift_atomunit(sue_bud, clean_atom)
#     assert  sift_atomunit(sue_bud, sweep_atom)

#     # WHEN
#     sue_bud.add_idea(casa_road)
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_atom)
#     assert  sift_atomunit(sue_bud, clean_atom)
#     assert  sift_atomunit(sue_bud, sweep_atom)

#     # WHEN
#     sue_bud.add_idea(clean_road)
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_atom)
#     assert not  sift_atomunit(sue_bud, clean_atom)
#     assert  sift_atomunit(sue_bud, sweep_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_awardlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     swim_str = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_awardlink_str(), atom_insert())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(group_id_str(), swim_str)
#     clean_swim_atom = atomunit_shop(bud_idea_awardlink_str(), atom_insert())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(group_id_str(), swim_str)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_awardlink(awardlink_shop(swim_str))
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert not  sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_reasonunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     week_str = "week"
#     week_road = sue_bud.make_l1_road(week_str)

#     casa_week_atom = atomunit_shop(bud_idea_reasonunit_str(), atom_insert())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom = atomunit_shop(bud_idea_reasonunit_str(), atom_insert())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_reasonunit(reasonunit_shop(week_road))
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert not  sift_atomunit(sue_bud, clean_week_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_reason_premiseunit_exists():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     week_str = "week"
#     week_road = sue_bud.make_l1_road(week_str)
#     thur_str = "thur"
#     thur_road = sue_bud.make_road(week_road, thur_str)

#     casa_week_atom = atomunit_shop(bud_idea_reason_premiseunit_str(), atom_insert())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     casa_week_atom.set_arg("need", thur_road)
#     clean_week_atom = atomunit_shop(bud_idea_reason_premiseunit_str(), atom_insert())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom.set_arg("need", thur_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     casa_idea = sue_bud.get_idea_obj(casa_road)
#     clean_idea = sue_bud.get_idea_obj(clean_road)
#     casa_idea.set_reasonunit(reasonunit_shop(week_road))
#     clean_idea.set_reasonunit(reasonunit_shop(week_road))
#     assert  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     casa_idea.get_reasonunit(week_road).set_premise(thur_road)

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     clean_idea.get_reasonunit(week_road).set_premise(thur_road)

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert not  sift_atomunit(sue_bud, clean_week_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_teamlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     swim_str = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_teamlink_str(), atom_insert())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(group_id_str(), swim_str)
#     clean_swim_atom = atomunit_shop(bud_idea_teamlink_str(), atom_insert())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(group_id_str(), swim_str)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).teamunit.set_teamlink(swim_str)

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).teamunit.set_teamlink(swim_str)
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert not  sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_healerlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     swim_str = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_healerlink_str(), atom_insert())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(healer_id_str(), swim_str)
#     clean_swim_atom = atomunit_shop(bud_idea_healerlink_str(), atom_insert())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(healer_id_str(), swim_str)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).healerlink.set_healer_id(swim_str)

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert  sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).healerlink.set_healer_id(swim_str)
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_swim_atom)
#     assert not  sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_SetsChangeUnitINSERTAtomUnit_bud_idea_factunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_str = "casa"
#     casa_road = sue_bud.make_l1_road(casa_str)
#     clean_str = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_str)
#     week_str = "week"
#     week_road = sue_bud.make_l1_road(week_str)

#     casa_week_atom = atomunit_shop(bud_idea_factunit_str(), atom_insert())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom = atomunit_shop(bud_idea_factunit_str(), atom_insert())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert  sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_factunit(factunit_shop(week_road))
#     # THEN
#     assert not  sift_atomunit(sue_bud, casa_week_atom)
#     assert not  sift_atomunit(sue_bud, clean_week_atom)
