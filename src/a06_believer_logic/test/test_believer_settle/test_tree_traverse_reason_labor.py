from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.labor import laborheir_shop, laborunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop


def test_believer_edit_plan_attr_SetsLaborUnit():
    # ESTABLISH
    xio_believer = believerunit_shop("Xio")
    run_str = "run"
    run_rope = xio_believer.make_l1_rope(run_str)
    xio_believer.set_l1_plan(planunit_shop(run_str))
    run_plan = xio_believer.get_plan_obj(run_rope)
    assert run_plan.laborunit == laborunit_shop()

    # WHEN
    x_laborunit = laborunit_shop()
    xio_believer.edit_plan_attr(run_rope, laborunit=x_laborunit)

    # THEN
    assert run_plan.laborunit == x_laborunit


def test_believer_planroot_laborunit_Sets_plan_laborheir():
    # ESTABLISH
    x_laborunit = laborunit_shop()

    yao_believer = believerunit_shop("Yao")
    root_rope = to_rope(yao_believer.belief_label)
    yao_believer.edit_plan_attr(root_rope, laborunit=x_laborunit)
    assert yao_believer.planroot.laborunit == x_laborunit
    assert yao_believer.planroot._laborheir is None

    # WHEN
    yao_believer.settle_believer()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    assert yao_believer.planroot._laborheir is not None
    assert yao_believer.planroot._laborheir == x_laborheir


def test_believer_plankid_laborunit_EmptySets_plan_laborheir():
    # ESTABLISH
    bob_str = "Bob"
    x_laborunit = laborunit_shop()
    bob_believer = believerunit_shop(bob_str)
    run_str = "run"
    run_rope = bob_believer.make_l1_rope(run_str)
    bob_believer.add_partnerunit(bob_str)
    bob_believer.set_l1_plan(planunit_shop(run_str))
    bob_believer.edit_plan_attr(run_rope, laborunit=x_laborunit)
    run_plan = bob_believer.get_plan_obj(run_rope)
    assert run_plan.laborunit == x_laborunit
    assert not run_plan._laborheir

    # WHEN
    bob_believer.settle_believer()

    # THEN
    assert run_plan._laborheir
    assert run_plan._laborheir._believer_name_is_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_believer._groupunits,
    )
    x_laborheir.set_believer_name_is_labor(
        bob_believer._groupunits, bob_believer.believer_name
    )
    print(f"{x_laborheir._believer_name_is_labor=}")
    assert (
        run_plan._laborheir._believer_name_is_labor
        == x_laborheir._believer_name_is_labor
    )
    assert run_plan._laborheir == x_laborheir


def test_believer_plankid_laborunit_Sets_grandchild_plan_laborheir():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    swim_str = "swimming"
    swim_rope = sue_believer.make_l1_rope(swim_str)
    morn_str = "morning"
    morn_rope = sue_believer.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_believer.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.add_partyunit(party_title=swimmers_str)

    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str)
    yao_partnerunit = sue_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(swimmers_str)

    sue_believer.set_l1_plan(planunit_shop(swim_str))
    sue_believer.set_plan(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_believer.set_plan(planunit_shop(four_str), parent_rope=morn_rope)
    sue_believer.edit_plan_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_believer.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_believer.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert four_plan._laborheir is None

    # WHEN
    sue_believer.settle_believer()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_believer._groupunits,
    )
    assert four_plan._laborheir is not None
    assert four_plan._laborheir == x_laborheir


def test_BelieverUnit__get_filtered_awardlinks_plan_CleansPlan_Laborunit():
    # ESTABLISH
    sue_str = "Sue"
    sue1_believer = believerunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_believer.add_partnerunit(xia_str)
    sue1_believer.add_partnerunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_believer.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_believer.make_l1_rope(swim_str)
    sue1_believer.set_plan(
        planunit_shop(casa_str), parent_rope=sue1_believer.belief_label
    )
    sue1_believer.set_plan(
        planunit_shop(swim_str), parent_rope=sue1_believer.belief_label
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_partyunit(party_title=xia_str)
    swim_laborunit.add_partyunit(party_title=zoa_str)
    sue1_believer.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_believer_swim_plan = sue1_believer.get_plan_obj(swim_rope)
    sue1_believer_swim_partys = sue1_believer_swim_plan.laborunit._partys
    assert len(sue1_believer_swim_partys) == 2

    # WHEN
    sue2_believer = believerunit_shop(sue_str)
    sue2_believer.add_partnerunit(xia_str)
    cleaned_plan = sue2_believer._get_filtered_awardlinks_plan(sue1_believer_swim_plan)

    # THEN
    cleaned_swim_partys = cleaned_plan.laborunit._partys
    assert len(cleaned_swim_partys) == 1
    assert list(cleaned_swim_partys) == [xia_str]


def test_BelieverUnit_set_plan_CleansPlan_awardlinks():
    # ESTABLISH
    sue1_believer = believerunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_believer.add_partnerunit(xia_str)
    sue1_believer.add_partnerunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_believer.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_believer.make_l1_rope(swim_str)
    sue1_believer.set_plan(
        planunit_shop(casa_str), parent_rope=sue1_believer.belief_label
    )
    sue1_believer.set_plan(
        planunit_shop(swim_str), parent_rope=sue1_believer.belief_label
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_partyunit(party_title=xia_str)
    swim_laborunit.add_partyunit(party_title=zoa_str)
    sue1_believer.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_believer_swim_plan = sue1_believer.get_plan_obj(swim_rope)
    sue1_believer_swim_partys = sue1_believer_swim_plan.laborunit._partys
    assert len(sue1_believer_swim_partys) == 2

    # WHEN
    sue2_believer = believerunit_shop("Sue")
    sue2_believer.add_partnerunit(xia_str)
    sue2_believer.set_l1_plan(
        sue1_believer_swim_plan, get_rid_of_missing_awardlinks_awardee_titles=False
    )

    # THEN
    sue2_believer_swim_plan = sue2_believer.get_plan_obj(swim_rope)
    sue2_believer_swim_partys = sue2_believer_swim_plan.laborunit._partys
    assert len(sue2_believer_swim_partys) == 1
    assert list(sue2_believer_swim_partys) == [xia_str]
