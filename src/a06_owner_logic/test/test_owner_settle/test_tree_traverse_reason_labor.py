from src.a01_term_logic.rope import to_rope
from src.a04_reason_logic.reason_labor import laborheir_shop, laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_owner_logic.owner import ownerunit_shop


def test_owner_edit_concept_attr_CorrectlySetsLaborUnit():
    # ESTABLISH
    xio_owner = ownerunit_shop("Xio")
    run_str = "run"
    run_rope = xio_owner.make_l1_rope(run_str)
    xio_owner.set_l1_concept(conceptunit_shop(run_str))
    run_concept = xio_owner.get_concept_obj(run_rope)
    assert run_concept.laborunit == laborunit_shop()

    # WHEN
    x_laborunit = laborunit_shop()
    xio_owner.edit_concept_attr(run_rope, laborunit=x_laborunit)

    # THEN
    assert run_concept.laborunit == x_laborunit


def test_owner_conceptroot_laborunit_CorrectlySets_concept_laborheir():
    # ESTABLISH
    x_laborunit = laborunit_shop()

    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    yao_owner.edit_concept_attr(root_rope, laborunit=x_laborunit)
    assert yao_owner.conceptroot.laborunit == x_laborunit
    assert yao_owner.conceptroot._laborheir is None

    # WHEN
    yao_owner.settle_owner()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    assert yao_owner.conceptroot._laborheir is not None
    assert yao_owner.conceptroot._laborheir == x_laborheir


def test_owner_conceptkid_laborunit_EmptyCorrectlySets_concept_laborheir():
    # ESTABLISH
    bob_str = "Bob"
    x_laborunit = laborunit_shop()
    bob_owner = ownerunit_shop(bob_str)
    run_str = "run"
    run_rope = bob_owner.make_l1_rope(run_str)
    bob_owner.add_acctunit(bob_str)
    bob_owner.set_l1_concept(conceptunit_shop(run_str))
    bob_owner.edit_concept_attr(run_rope, laborunit=x_laborunit)
    run_concept = bob_owner.get_concept_obj(run_rope)
    assert run_concept.laborunit == x_laborunit
    assert run_concept._laborheir is None

    # WHEN
    bob_owner.settle_owner()

    # THEN
    assert run_concept._laborheir is not None
    assert run_concept._laborheir._owner_name_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_owner._groupunits,
    )
    x_laborheir.set_owner_name_labor(bob_owner._groupunits, bob_owner.owner_name)
    print(f"{x_laborheir._owner_name_labor=}")
    assert run_concept._laborheir._owner_name_labor == x_laborheir._owner_name_labor
    assert run_concept._laborheir == x_laborheir


def test_owner_conceptkid_laborunit_CorrectlySets_grandchild_concept_laborheir():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    swim_str = "swimming"
    swim_rope = sue_owner.make_l1_rope(swim_str)
    morn_str = "morning"
    morn_rope = sue_owner.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_owner.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.set_laborlink(labor_title=swimmers_str)

    yao_str = "Yao"
    sue_owner.add_acctunit(yao_str)
    yao_acctunit = sue_owner.get_acct(yao_str)
    yao_acctunit.add_membership(swimmers_str)

    sue_owner.set_l1_concept(conceptunit_shop(swim_str))
    sue_owner.set_concept(conceptunit_shop(morn_str), parent_rope=swim_rope)
    sue_owner.set_concept(conceptunit_shop(four_str), parent_rope=morn_rope)
    sue_owner.edit_concept_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_owner.make_rope(four_rope=}\n{morn_rope=))
    four_concept = sue_owner.get_concept_obj(four_rope)
    assert four_concept.laborunit == laborunit_shop()
    assert four_concept._laborheir is None

    # WHEN
    sue_owner.settle_owner()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_owner._groupunits,
    )
    assert four_concept._laborheir is not None
    assert four_concept._laborheir == x_laborheir


def test_OwnerUnit__get_filtered_awardlinks_concept_CorrectlyCleansConcept_Laborunit():
    # ESTABLISH
    sue_str = "Sue"
    sue1_owner = ownerunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_owner.add_acctunit(xia_str)
    sue1_owner.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_owner.make_l1_rope(swim_str)
    sue1_owner.set_concept(
        conceptunit_shop(casa_str), parent_rope=sue1_owner.belief_label
    )
    sue1_owner.set_concept(
        conceptunit_shop(swim_str), parent_rope=sue1_owner.belief_label
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.set_laborlink(labor_title=xia_str)
    swim_laborunit.set_laborlink(labor_title=zoa_str)
    sue1_owner.edit_concept_attr(swim_rope, laborunit=swim_laborunit)
    sue1_owner_swim_concept = sue1_owner.get_concept_obj(swim_rope)
    sue1_owner_swim_laborlinks = sue1_owner_swim_concept.laborunit._laborlinks
    assert len(sue1_owner_swim_laborlinks) == 2

    # WHEN
    sue2_owner = ownerunit_shop(sue_str)
    sue2_owner.add_acctunit(xia_str)
    cleaned_concept = sue2_owner._get_filtered_awardlinks_concept(
        sue1_owner_swim_concept
    )

    # THEN
    cleaned_swim_laborlinks = cleaned_concept.laborunit._laborlinks
    assert len(cleaned_swim_laborlinks) == 1
    assert list(cleaned_swim_laborlinks) == [xia_str]


def test_OwnerUnit_set_concept_CorrectlyCleansConcept_awardlinks():
    # ESTABLISH
    sue1_owner = ownerunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_owner.add_acctunit(xia_str)
    sue1_owner.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_owner.make_l1_rope(swim_str)
    sue1_owner.set_concept(
        conceptunit_shop(casa_str), parent_rope=sue1_owner.belief_label
    )
    sue1_owner.set_concept(
        conceptunit_shop(swim_str), parent_rope=sue1_owner.belief_label
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.set_laborlink(labor_title=xia_str)
    swim_laborunit.set_laborlink(labor_title=zoa_str)
    sue1_owner.edit_concept_attr(swim_rope, laborunit=swim_laborunit)
    sue1_owner_swim_concept = sue1_owner.get_concept_obj(swim_rope)
    sue1_owner_swim_laborlinks = sue1_owner_swim_concept.laborunit._laborlinks
    assert len(sue1_owner_swim_laborlinks) == 2

    # WHEN
    sue2_owner = ownerunit_shop("Sue")
    sue2_owner.add_acctunit(xia_str)
    sue2_owner.set_l1_concept(
        sue1_owner_swim_concept, get_rid_of_missing_awardlinks_awardee_titles=False
    )

    # THEN
    sue2_owner_swim_concept = sue2_owner.get_concept_obj(swim_rope)
    sue2_owner_swim_laborlinks = sue2_owner_swim_concept.laborunit._laborlinks
    assert len(sue2_owner_swim_laborlinks) == 1
    assert list(sue2_owner_swim_laborlinks) == [xia_str]
