from src.a01_term_logic.way import to_way
from src.a04_reason_logic.reason_labor import laborheir_shop, laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop


def test_bud_edit_concept_attr_CorrectlySetsLaborUnit():
    # ESTABLISH
    xio_bud = budunit_shop("Xio")
    run_str = "run"
    run_way = xio_bud.make_l1_way(run_str)
    xio_bud.set_l1_concept(conceptunit_shop(run_str))
    run_concept = xio_bud.get_concept_obj(run_way)
    assert run_concept.laborunit == laborunit_shop()

    # WHEN
    x_laborunit = laborunit_shop()
    xio_bud.edit_concept_attr(run_way, laborunit=x_laborunit)

    # THEN
    assert run_concept.laborunit == x_laborunit


def test_bud_conceptroot_laborunit_CorrectlySets_concept_laborheir():
    # ESTABLISH
    x_laborunit = laborunit_shop()

    yao_bud = budunit_shop("Yao")
    root_way = to_way(yao_bud.fisc_label)
    yao_bud.edit_concept_attr(root_way, laborunit=x_laborunit)
    assert yao_bud.conceptroot.laborunit == x_laborunit
    assert yao_bud.conceptroot._laborheir is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    assert yao_bud.conceptroot._laborheir is not None
    assert yao_bud.conceptroot._laborheir == x_laborheir


def test_bud_conceptkid_laborunit_EmptyCorrectlySets_concept_laborheir():
    # ESTABLISH
    bob_str = "Bob"
    x_laborunit = laborunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_way = bob_bud.make_l1_way(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_concept(conceptunit_shop(run_str))
    bob_bud.edit_concept_attr(run_way, laborunit=x_laborunit)
    run_concept = bob_bud.get_concept_obj(run_way)
    assert run_concept.laborunit == x_laborunit
    assert run_concept._laborheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_concept._laborheir is not None
    assert run_concept._laborheir._owner_name_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_bud._groupunits,
    )
    x_laborheir.set_owner_name_labor(bob_bud._groupunits, bob_bud.owner_name)
    print(f"{x_laborheir._owner_name_labor=}")
    assert run_concept._laborheir._owner_name_labor == x_laborheir._owner_name_labor
    assert run_concept._laborheir == x_laborheir


def test_bud_conceptkid_laborunit_EmptyCorrectlySets_concept_laborheir():
    # ESTABLISH
    bob_str = "Bob"
    x_laborunit = laborunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_way = bob_bud.make_l1_way(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_concept(conceptunit_shop(run_str))
    bob_bud.edit_concept_attr(run_way, laborunit=x_laborunit)
    run_concept = bob_bud.get_concept_obj(run_way)
    assert run_concept.laborunit == x_laborunit
    assert run_concept._laborheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_concept._laborheir is not None
    assert run_concept._laborheir._owner_name_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_bud._groupunits,
    )
    x_laborheir.set_owner_name_labor(bob_bud._groupunits, bob_bud.owner_name)
    print(f"{x_laborheir._owner_name_labor=}")
    assert run_concept._laborheir._owner_name_labor == x_laborheir._owner_name_labor
    assert run_concept._laborheir == x_laborheir


def test_bud_conceptkid_laborunit_CorrectlySets_grandchild_concept_laborheir():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_str = "swimming"
    swim_way = sue_bud.make_l1_way(swim_str)
    morn_str = "morning"
    morn_way = sue_bud.make_way(swim_way, morn_str)
    four_str = "fourth"
    four_way = sue_bud.make_way(morn_way, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.set_laborlink(labor_title=swimmers_str)

    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(swimmers_str)

    sue_bud.set_l1_concept(conceptunit_shop(swim_str))
    sue_bud.set_concept(conceptunit_shop(morn_str), parent_way=swim_way)
    sue_bud.set_concept(conceptunit_shop(four_str), parent_way=morn_way)
    sue_bud.edit_concept_attr(swim_way, laborunit=x_laborunit)
    # print(sue_bud.make_way(four_way=}\n{morn_way=))
    four_concept = sue_bud.get_concept_obj(four_way)
    assert four_concept.laborunit == laborunit_shop()
    assert four_concept._laborheir is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_bud._groupunits,
    )
    assert four_concept._laborheir is not None
    assert four_concept._laborheir == x_laborheir


def test_BudUnit__get_filtered_awardlinks_concept_CorrectlyCleansConcept_Laborunit():
    # ESTABLISH
    sue_str = "Sue"
    sue1_bud = budunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = sue1_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = sue1_bud.make_l1_way(swim_str)
    sue1_bud.set_concept(conceptunit_shop(casa_str), parent_way=sue1_bud.fisc_label)
    sue1_bud.set_concept(conceptunit_shop(swim_str), parent_way=sue1_bud.fisc_label)
    swim_laborunit = laborunit_shop()
    swim_laborunit.set_laborlink(labor_title=xia_str)
    swim_laborunit.set_laborlink(labor_title=zoa_str)
    sue1_bud.edit_concept_attr(swim_way, laborunit=swim_laborunit)
    sue1_bud_swim_concept = sue1_bud.get_concept_obj(swim_way)
    sue1_bud_swim_laborlinks = sue1_bud_swim_concept.laborunit._laborlinks
    assert len(sue1_bud_swim_laborlinks) == 2

    # WHEN
    sue2_bud = budunit_shop(sue_str)
    sue2_bud.add_acctunit(xia_str)
    cleaned_concept = sue2_bud._get_filtered_awardlinks_concept(sue1_bud_swim_concept)

    # THEN
    cleaned_swim_laborlinks = cleaned_concept.laborunit._laborlinks
    assert len(cleaned_swim_laborlinks) == 1
    assert list(cleaned_swim_laborlinks) == [xia_str]


def test_BudUnit_set_concept_CorrectlyCleansConcept_awardlinks():
    # ESTABLISH
    sue1_bud = budunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = sue1_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = sue1_bud.make_l1_way(swim_str)
    sue1_bud.set_concept(conceptunit_shop(casa_str), parent_way=sue1_bud.fisc_label)
    sue1_bud.set_concept(conceptunit_shop(swim_str), parent_way=sue1_bud.fisc_label)
    swim_laborunit = laborunit_shop()
    swim_laborunit.set_laborlink(labor_title=xia_str)
    swim_laborunit.set_laborlink(labor_title=zoa_str)
    sue1_bud.edit_concept_attr(swim_way, laborunit=swim_laborunit)
    sue1_bud_swim_concept = sue1_bud.get_concept_obj(swim_way)
    sue1_bud_swim_laborlinks = sue1_bud_swim_concept.laborunit._laborlinks
    assert len(sue1_bud_swim_laborlinks) == 2

    # WHEN
    sue2_bud = budunit_shop("Sue")
    sue2_bud.add_acctunit(xia_str)
    sue2_bud.set_l1_concept(
        sue1_bud_swim_concept, get_rid_of_missing_awardlinks_awardee_titles=False
    )

    # THEN
    sue2_bud_swim_concept = sue2_bud.get_concept_obj(swim_way)
    sue2_bud_swim_laborlinks = sue2_bud_swim_concept.laborunit._laborlinks
    assert len(sue2_bud_swim_laborlinks) == 1
    assert list(sue2_bud_swim_laborlinks) == [xia_str]
