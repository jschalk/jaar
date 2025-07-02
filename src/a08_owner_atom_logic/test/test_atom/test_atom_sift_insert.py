from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    awardee_title_str,
    concept_rope_str,
    fcontext_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_concept_awardlink_str,
    owner_concept_factunit_str,
    owner_concept_healerlink_str,
    owner_concept_laborlink_str,
    owner_concept_reason_premiseunit_str,
    owner_concept_reasonunit_str,
    owner_conceptunit_str,
    rcontext_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop, sift_owneratom
from src.a08_owner_atom_logic.test._util.a08_str import INSERT_str


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_acctunit():
    # ESTABLISH
    bob_str = "Bob"
    zia_str = "Zia"
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(zia_str)

    bob_atom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    bob_atom.set_arg(acct_name_str(), bob_str)
    zia_atom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    zia_atom.set_arg(acct_name_str(), zia_str)

    # WHEN
    new_bob_owneratom = sift_owneratom(sue_owner, bob_atom)
    new_zia_owneratom = sift_owneratom(sue_owner, zia_atom)

    # THEN
    assert new_bob_owneratom
    assert new_bob_owneratom == bob_atom
    assert not new_zia_owneratom


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_acct_membership():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    run_str = ";run"
    sue_owner = ownerunit_shop("Sue")
    sue_owner.add_acctunit(yao_str)
    sue_owner.add_acctunit(bob_str)
    yao_acctunit = sue_owner.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    print(f"{yao_acctunit._memberships.keys()=}")

    bob_run_atom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
    bob_run_atom.set_arg(acct_name_str(), bob_str)
    bob_run_atom.set_arg(group_title_str(), run_str)
    yao_run_atom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
    yao_run_atom.set_arg(acct_name_str(), yao_str)
    yao_run_atom.set_arg(group_title_str(), run_str)

    # WHEN
    new_bob_run_owneratom = sift_owneratom(sue_owner, bob_run_atom)
    new_yao_run_owneratom = sift_owneratom(sue_owner, yao_run_atom)

    # THEN
    assert new_bob_run_owneratom
    assert new_bob_run_owneratom == bob_run_atom
    assert not new_yao_run_owneratom


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_conceptunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    root_rope = to_rope(sue_owner.belief_label)
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_owner.make_rope(clean_rope, sweep_str)

    root_atom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    root_atom.set_arg(concept_rope_str(), root_rope)
    casa_atom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    casa_atom.set_arg(concept_rope_str(), casa_rope)
    clean_atom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    clean_atom.set_arg(concept_rope_str(), clean_rope)
    sweep_atom = owneratom_shop(owner_conceptunit_str(), INSERT_str())
    sweep_atom.set_arg(concept_rope_str(), sweep_rope)
    assert not sift_owneratom(sue_owner, root_atom)
    assert sift_owneratom(sue_owner, casa_atom)
    assert sift_owneratom(sue_owner, clean_atom)
    assert sift_owneratom(sue_owner, sweep_atom)

    # WHEN
    sue_owner.add_concept(casa_rope)
    # THEN
    assert not sift_owneratom(sue_owner, casa_atom)
    assert sift_owneratom(sue_owner, clean_atom)
    assert sift_owneratom(sue_owner, sweep_atom)

    # WHEN
    sue_owner.add_concept(clean_rope)
    # THEN
    assert not sift_owneratom(sue_owner, casa_atom)
    assert not sift_owneratom(sue_owner, clean_atom)
    assert sift_owneratom(sue_owner, sweep_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_awardlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = owneratom_shop(owner_concept_awardlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(awardee_title_str(), swim_str)
    clean_swim_atom = owneratom_shop(owner_concept_awardlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(awardee_title_str(), swim_str)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    assert sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(clean_rope).set_awardlink(awardlink_shop(swim_str))
    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert not sift_owneratom(sue_owner, clean_swim_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_reasonunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(week_str)

    casa_week_atom = owneratom_shop(owner_concept_reasonunit_str(), INSERT_str())
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(rcontext_str(), week_rope)
    clean_week_atom = owneratom_shop(owner_concept_reasonunit_str(), INSERT_str())
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(rcontext_str(), week_rope)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    assert sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    sue_owner.get_concept_obj(casa_rope).set_reasonunit(reasonunit_shop(week_rope))

    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    sue_owner.get_concept_obj(clean_rope).set_reasonunit(reasonunit_shop(week_rope))
    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert not sift_owneratom(sue_owner, clean_week_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_reason_premiseunit_exists():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(week_str)
    thur_str = "thur"
    thur_rope = sue_owner.make_rope(week_rope, thur_str)

    casa_week_atom = owneratom_shop(
        owner_concept_reason_premiseunit_str(), INSERT_str()
    )
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(rcontext_str(), week_rope)
    casa_week_atom.set_arg("pstate", thur_rope)
    clean_week_atom = owneratom_shop(
        owner_concept_reason_premiseunit_str(), INSERT_str()
    )
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(rcontext_str(), week_rope)
    clean_week_atom.set_arg("pstate", thur_rope)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    casa_concept = sue_owner.get_concept_obj(casa_rope)
    clean_concept = sue_owner.get_concept_obj(clean_rope)
    casa_concept.set_reasonunit(reasonunit_shop(week_rope))
    clean_concept.set_reasonunit(reasonunit_shop(week_rope))
    assert sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    casa_concept.get_reasonunit(week_rope).set_premise(thur_rope)

    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    clean_concept.get_reasonunit(week_rope).set_premise(thur_rope)

    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert not sift_owneratom(sue_owner, clean_week_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_laborlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = owneratom_shop(owner_concept_laborlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(labor_title_str(), swim_str)
    clean_swim_atom = owneratom_shop(owner_concept_laborlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(labor_title_str(), swim_str)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    assert sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(casa_rope).laborunit.set_laborlink(swim_str)

    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(clean_rope).laborunit.set_laborlink(swim_str)
    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert not sift_owneratom(sue_owner, clean_swim_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_healerlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    swim_str = "Swim"

    casa_swim_atom = owneratom_shop(owner_concept_healerlink_str(), INSERT_str())
    casa_swim_atom.set_arg(concept_rope_str(), casa_rope)
    casa_swim_atom.set_arg(healer_name_str(), swim_str)
    clean_swim_atom = owneratom_shop(owner_concept_healerlink_str(), INSERT_str())
    clean_swim_atom.set_arg(concept_rope_str(), clean_rope)
    clean_swim_atom.set_arg(healer_name_str(), swim_str)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    assert sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(casa_rope).healerlink.set_healer_name(swim_str)

    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert sift_owneratom(sue_owner, clean_swim_atom)

    # WHEN
    sue_owner.get_concept_obj(clean_rope).healerlink.set_healer_name(swim_str)
    # THEN
    assert not sift_owneratom(sue_owner, casa_swim_atom)
    assert not sift_owneratom(sue_owner, clean_swim_atom)


def test_sift_atom_ReturnsObj_OwnerAtom_INSERT_owner_concept_factunit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_owner.make_rope(casa_rope, clean_str)
    week_str = "week"
    week_rope = sue_owner.make_l1_rope(week_str)

    casa_week_atom = owneratom_shop(owner_concept_factunit_str(), INSERT_str())
    casa_week_atom.set_arg(concept_rope_str(), casa_rope)
    casa_week_atom.set_arg(fcontext_str(), week_rope)
    clean_week_atom = owneratom_shop(owner_concept_factunit_str(), INSERT_str())
    clean_week_atom.set_arg(concept_rope_str(), clean_rope)
    clean_week_atom.set_arg(fcontext_str(), week_rope)
    sue_owner.add_concept(casa_rope)
    sue_owner.add_concept(clean_rope)
    assert sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    sue_owner.get_concept_obj(casa_rope).set_factunit(factunit_shop(week_rope))

    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert sift_owneratom(sue_owner, clean_week_atom)

    # WHEN
    sue_owner.get_concept_obj(clean_rope).set_factunit(factunit_shop(week_rope))
    # THEN
    assert not sift_owneratom(sue_owner, casa_week_atom)
    assert not sift_owneratom(sue_owner, clean_week_atom)
