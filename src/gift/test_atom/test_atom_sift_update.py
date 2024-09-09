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
from src.gift.atom import atom_insert, atom_update, atomunit_shop, sift_atomunit
from src.gift.atom_config import (
    acct_id_str,
    group_id_str,
    healer_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
    debtit_belief_str,
    debtit_vote_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    gogo_want_str,
    mass_str,
    morph_str,
    numor_str,
    pledge_str,
    stop_want_str,
)


def test_sift_atom_ReturnsNoneIfGivenAtomUnitIsUPDATE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.add_idea(casa_road)
    casa_atom = atomunit_shop(bud_ideaunit_text(), atom_update())
    casa_atom.set_arg(parent_road_str(), sue_bud._real_id)
    casa_atom.set_arg(label_str(), casa_text)
    casa_atom.set_arg(mass_str(), 8)
    # THEN
    new_casa_atom = sift_atomunit(sue_bud, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_acctunit():
    # ESTABLISH
    zia_text = "Zia"
    zia_debtit_belief = 51
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_text)

    zia_atom = atomunit_shop(bud_acctunit_text(), atom_insert())
    zia_atom.set_arg(acct_id_str(), zia_text)
    zia_atom.set_arg(debtit_belief_str(), zia_debtit_belief)

    # WHEN
    new_zia_atomunit = sift_atomunit(sue_bud, zia_atom)

    # THEN
    assert new_zia_atomunit
    assert new_zia_atomunit.crud_text == atom_update()
    assert new_zia_atomunit.get_optional_args_dict() != {}
    zia_optional_args = new_zia_atomunit.get_optional_args_dict()
    assert zia_optional_args == {debtit_belief_str(): 51}


def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_acct_membership():
    # ESTABLISH
    zia_text = "Zia"
    run_text = ";run"
    zia_run_debtit_vote = 76
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_text)
    sue_bud.get_acct(zia_text).add_membership(run_text)

    zia_atom = atomunit_shop(bud_acct_membership_text(), atom_insert())
    zia_atom.set_arg(acct_id_str(), zia_text)
    zia_atom.set_arg(group_id_str(), run_text)
    zia_atom.set_arg(debtit_vote_str(), zia_run_debtit_vote)

    # WHEN
    new_zia_atomunit = sift_atomunit(sue_bud, zia_atom)

    # THEN
    assert new_zia_atomunit
    assert new_zia_atomunit.crud_text == atom_update()
    assert new_zia_atomunit.get_optional_args_dict() != {}
    zia_optional_args = new_zia_atomunit.get_optional_args_dict()
    assert zia_optional_args == {debtit_vote_str(): zia_run_debtit_vote}


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_ideaunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     sue_bud.add_idea(casa_road)

#     # sue_addin = 55
#     # sue_begin = 55
#     # sue_close = 55
#     # sue_denom = 55
#     # sue_gogo_want = 55
#     sue_mass = 7
#     # sue_morph = 44
#     # sue_numor = 44
#     # sue_pledge = 44
#     # sue_problem_bool = 44
#     # sue_stop_want = 44
#     old_casa_atom = atomunit_shop(bud_ideaunit_text(), atom_insert())
#     old_casa_atom.set_arg(parent_road_str(), sue_bud._real_id)
#     old_casa_atom.set_arg(label_str(), casa_text)
#     old_casa_atom.set_arg(mass_str(), sue_mass)
#     # THEN
#     new_casa_atom = sift_atomunit(sue_bud, old_casa_atom)

#     # THEN
#     assert new_casa_atom
#     assert new_casa_atom.crud_text == atom_update()
#     assert new_casa_atom.get_optional_args_dict()
#     zia_optional_args = new_casa_atom.get_optional_args_dict()
#     assert zia_optional_args == {mass_str(): sue_mass}
#     assert 1 == 2


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_awardlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     swim_text = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_awardlink_text(), atom_update())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(group_id_str(), swim_text)
#     clean_swim_atom = atomunit_shop(bud_idea_awardlink_text(), atom_update())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(group_id_str(), swim_text)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_awardlink(awardlink_shop(swim_text))

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_awardlink(awardlink_shop(swim_text))
#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert not sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_reasonunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     week_text = "week"
#     week_road = sue_bud.make_l1_road(week_text)

#     casa_week_atom = atomunit_shop(bud_idea_reasonunit_text(), atom_update())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom = atomunit_shop(bud_idea_reasonunit_text(), atom_update())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_reasonunit(reasonunit_shop(week_road))
#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert not sift_atomunit(sue_bud, clean_week_atom)


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_reason_premiseunit_exists():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     week_text = "week"
#     week_road = sue_bud.make_l1_road(week_text)
#     thur_text = "thur"
#     thur_road = sue_bud.make_road(week_road, thur_text)

#     casa_week_atom = atomunit_shop(bud_idea_reason_premiseunit_text(), atom_update())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     casa_week_atom.set_arg("need", thur_road)
#     clean_week_atom = atomunit_shop(bud_idea_reason_premiseunit_text(), atom_update())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom.set_arg("need", thur_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     casa_idea = sue_bud.get_idea_obj(casa_road)
#     clean_idea = sue_bud.get_idea_obj(clean_road)
#     casa_idea.set_reasonunit(reasonunit_shop(week_road))
#     clean_idea.set_reasonunit(reasonunit_shop(week_road))
#     assert sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     casa_idea.get_reasonunit(week_road).set_premise(thur_road)

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     clean_idea.get_reasonunit(week_road).set_premise(thur_road)

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert not sift_atomunit(sue_bud, clean_week_atom)


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_teamlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     swim_text = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_teamlink_text(), atom_update())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(group_id_str(), swim_text)
#     clean_swim_atom = atomunit_shop(bud_idea_teamlink_text(), atom_update())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(group_id_str(), swim_text)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road)._teamunit.set_teamlink(swim_text)

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road)._teamunit.set_teamlink(swim_text)
#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert not sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_healerlink():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     swim_text = "Swim"

#     casa_swim_atom = atomunit_shop(bud_idea_healerlink_text(), atom_update())
#     casa_swim_atom.set_arg(road_str(), casa_road)
#     casa_swim_atom.set_arg(healer_id_str(), swim_text)
#     clean_swim_atom = atomunit_shop(bud_idea_healerlink_text(), atom_update())
#     clean_swim_atom.set_arg(road_str(), clean_road)
#     clean_swim_atom.set_arg(healer_id_str(), swim_text)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road)._healerlink.set_healer_id(swim_text)

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert sift_atomunit(sue_bud, clean_swim_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road)._healerlink.set_healer_id(swim_text)
#     # THEN
#     assert not sift_atomunit(sue_bud, casa_swim_atom)
#     assert not sift_atomunit(sue_bud, clean_swim_atom)


# def test_sift_atom_ReturnsObj_AtomUnit_UPDATE_bud_idea_factunit():
#     # ESTABLISH
#     sue_bud = budunit_shop("Sue")
#     casa_text = "casa"
#     casa_road = sue_bud.make_l1_road(casa_text)
#     clean_text = "clean"
#     clean_road = sue_bud.make_road(casa_road, clean_text)
#     week_text = "week"
#     week_road = sue_bud.make_l1_road(week_text)

#     casa_week_atom = atomunit_shop(bud_idea_factunit_text(), atom_update())
#     casa_week_atom.set_arg(road_str(), casa_road)
#     casa_week_atom.set_arg(base_str(), week_road)
#     clean_week_atom = atomunit_shop(bud_idea_factunit_text(), atom_update())
#     clean_week_atom.set_arg(road_str(), clean_road)
#     clean_week_atom.set_arg(base_str(), week_road)
#     sue_bud.add_idea(casa_road)
#     sue_bud.add_idea(clean_road)
#     assert sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(casa_road).set_factunit(factunit_shop(week_road))

#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert sift_atomunit(sue_bud, clean_week_atom)

#     # WHEN
#     sue_bud.get_idea_obj(clean_road).set_factunit(factunit_shop(week_road))
#     # THEN
#     assert not sift_atomunit(sue_bud, casa_week_atom)
#     assert not sift_atomunit(sue_bud, clean_week_atom)
