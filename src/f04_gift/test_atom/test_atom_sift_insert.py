from src.f02_bud.group import awardlink_shop
from src.f02_bud.reason_item import reasonunit_shop, factunit_shop
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
)
from src.f04_gift.atom import atom_insert, atomunit_shop, sift_atomunit
from src.f04_gift.atom_config import (
    acct_name_str,
    awardee_tag_str,
    group_label_str,
    team_tag_str,
    healer_name_str,
    parent_road_str,
    item_title_str,
    road_str,
    base_str,
)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(zia_str)

    bob_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = atomunit_shop(bud_acctunit_str(), atom_insert())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_atomunit = sift_atomunit(sue_bud, bob_atom)
    new_zia_atomunit = sift_atomunit(sue_bud, zia_atom)

    # THEN
    assert new_bob_atomunit
    assert new_bob_atomunit == bob_atom
    assert not new_zia_atomunit


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_acct_membership():
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

    bob_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_label_str(), run_str)
    yao_run_atom = atomunit_shop(bud_acct_membership_str(), atom_insert())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_label_str(), run_str)

    # WHEN
    new_bob_run_atomunit = sift_atomunit(sue_bud, bob_run_atom)
    new_yao_run_atomunit = sift_atomunit(sue_bud, yao_run_atom)

    # THEN
    assert new_bob_run_atomunit
    assert new_bob_run_atomunit == bob_run_atom
    assert not new_yao_run_atomunit


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_itemunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    sweep_str = "sweep"
    sweep_road = sue_bud.make_road(clean_road, sweep_str)

    root_atom = atomunit_shop(bud_itemunit_str(), atom_insert())
    root_atom.set_arg(parent_road_str(), "")
    root_atom.set_arg(item_title_str(), sue_bud.fisc_title)
    casa_atom = atomunit_shop(bud_itemunit_str(), atom_insert())
    casa_atom.set_arg(parent_road_str(), sue_bud.fisc_title)
    casa_atom.set_arg(item_title_str(), casa_str)
    clean_atom = atomunit_shop(bud_itemunit_str(), atom_insert())
    clean_atom.set_arg(parent_road_str(), casa_road)
    clean_atom.set_arg(item_title_str(), clean_str)
    sweep_atom = atomunit_shop(bud_itemunit_str(), atom_insert())
    sweep_atom.set_arg(parent_road_str(), clean_road)
    sweep_atom.set_arg(item_title_str(), sweep_str)
    assert not sift_atomunit(sue_bud, root_atom)
    assert sift_atomunit(sue_bud, casa_atom)
    assert sift_atomunit(sue_bud, clean_atom)
    assert sift_atomunit(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_item(casa_road)
    # THEN
    assert not sift_atomunit(sue_bud, casa_atom)
    assert sift_atomunit(sue_bud, clean_atom)
    assert sift_atomunit(sue_bud, sweep_atom)

    # WHEN
    sue_bud.add_item(clean_road)
    # THEN
    assert not sift_atomunit(sue_bud, casa_atom)
    assert not sift_atomunit(sue_bud, clean_atom)
    assert sift_atomunit(sue_bud, sweep_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_awardlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    swim_str = "Swim"

    casa_swim_atom = atomunit_shop(bud_item_awardlink_str(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(awardee_tag_str(), swim_str)
    clean_swim_atom = atomunit_shop(bud_item_awardlink_str(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(awardee_tag_str(), swim_str)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    assert sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(casa_road).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(clean_road).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert not sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_reasonunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)

    casa_week_atom = atomunit_shop(bud_item_reasonunit_str(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    clean_week_atom = atomunit_shop(bud_item_reasonunit_str(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    assert sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_item_obj(casa_road).set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_item_obj(clean_road).set_reasonunit(reasonunit_shop(week_road))
    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert not sift_atomunit(sue_bud, clean_week_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_reason_premiseunit_exists():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)
    thur_str = "thur"
    thur_road = sue_bud.make_road(week_road, thur_str)

    casa_week_atom = atomunit_shop(bud_item_reason_premiseunit_str(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    casa_week_atom.set_arg("need", thur_road)
    clean_week_atom = atomunit_shop(bud_item_reason_premiseunit_str(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    clean_week_atom.set_arg("need", thur_road)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    casa_item = sue_bud.get_item_obj(casa_road)
    clean_item = sue_bud.get_item_obj(clean_road)
    casa_item.set_reasonunit(reasonunit_shop(week_road))
    clean_item.set_reasonunit(reasonunit_shop(week_road))
    assert sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    casa_item.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    clean_item.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert not sift_atomunit(sue_bud, clean_week_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_teamlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    swim_str = "Swim"

    casa_swim_atom = atomunit_shop(bud_item_teamlink_str(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(team_tag_str(), swim_str)
    clean_swim_atom = atomunit_shop(bud_item_teamlink_str(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(team_tag_str(), swim_str)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    assert sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(casa_road).teamunit.set_teamlink(swim_str)

    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(clean_road).teamunit.set_teamlink(swim_str)
    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert not sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    swim_str = "Swim"

    casa_swim_atom = atomunit_shop(bud_item_healerlink_str(), atom_insert())
    casa_swim_atom.set_arg(road_str(), casa_road)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = atomunit_shop(bud_item_healerlink_str(), atom_insert())
    clean_swim_atom.set_arg(road_str(), clean_road)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    assert sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(casa_road).healerlink.set_healer_name(swim_str)

    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert sift_atomunit(sue_bud, clean_swim_atom)

    # WHEN
    sue_bud.get_item_obj(clean_road).healerlink.set_healer_name(swim_str)
    # THEN
    assert not sift_atomunit(sue_bud, casa_swim_atom)
    assert not sift_atomunit(sue_bud, clean_swim_atom)


def test_sift_atom_ReturnsObj_AtomUnit_INSERT_bud_item_factunit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    clean_str = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_str)
    week_str = "week"
    week_road = sue_bud.make_l1_road(week_str)

    casa_week_atom = atomunit_shop(bud_item_factunit_str(), atom_insert())
    casa_week_atom.set_arg(road_str(), casa_road)
    casa_week_atom.set_arg(base_str(), week_road)
    clean_week_atom = atomunit_shop(bud_item_factunit_str(), atom_insert())
    clean_week_atom.set_arg(road_str(), clean_road)
    clean_week_atom.set_arg(base_str(), week_road)
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    assert sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_item_obj(casa_road).set_factunit(factunit_shop(week_road))

    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert sift_atomunit(sue_bud, clean_week_atom)

    # WHEN
    sue_bud.get_item_obj(clean_road).set_factunit(factunit_shop(week_road))
    # THEN
    assert not sift_atomunit(sue_bud, casa_week_atom)
    assert not sift_atomunit(sue_bud, clean_week_atom)
