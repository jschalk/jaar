from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.labor import laborheir_shop, laborunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop


def test_BeliefUnit_cash_out_Sets_planroot_laborheirFrom_planroot_laborunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(sue_str)
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    yao_belief.edit_plan_attr(root_rope, laborunit=sue_laborunit)
    assert yao_belief.planroot.laborunit == sue_laborunit
    assert not yao_belief.planroot._laborheir

    # WHEN
    yao_belief.cash_out()

    # THEN
    assert yao_belief.planroot._laborheir is not None
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None, laborunit=sue_laborunit, groupunits=None
    )
    assert yao_belief.planroot._laborheir == expected_laborheir


def test_BeliefUnit_cash_out_Set_child_plan_laborheir_FromParent_laborunit():
    # ESTABLISH
    bob_str = "Bob"
    x_laborunit = laborunit_shop()
    bob_belief = beliefunit_shop(bob_str)
    run_str = "run"
    run_rope = bob_belief.make_l1_rope(run_str)
    bob_belief.add_partnerunit(bob_str)
    bob_belief.set_l1_plan(planunit_shop(run_str))
    bob_belief.edit_plan_attr(run_rope, laborunit=x_laborunit)
    run_plan = bob_belief.get_plan_obj(run_rope)
    assert run_plan.laborunit == x_laborunit
    assert not run_plan._laborheir

    # WHEN
    bob_belief.cash_out()

    # THEN
    assert run_plan._laborheir
    assert run_plan._laborheir._belief_name_is_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_belief._groupunits,
    )
    x_laborheir.set_belief_name_is_labor(bob_belief._groupunits, bob_belief.belief_name)
    print(f"{x_laborheir._belief_name_is_labor=}")
    assert (
        run_plan._laborheir._belief_name_is_labor == x_laborheir._belief_name_is_labor
    )
    assert run_plan._laborheir == x_laborheir


def test_BeliefUnit_cash_out_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    swim_str = "swimming"
    swim_rope = sue_belief.make_l1_rope(swim_str)
    morn_str = "morning"
    morn_rope = sue_belief.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_belief.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.add_party(party_title=swimmers_str)

    yao_str = "Yao"
    sue_belief.add_partnerunit(yao_str)
    yao_partnerunit = sue_belief.get_partner(yao_str)
    yao_partnerunit.add_membership(swimmers_str)

    sue_belief.set_l1_plan(planunit_shop(swim_str))
    sue_belief.set_plan(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_belief.set_plan(planunit_shop(four_str), parent_rope=morn_rope)
    sue_belief.edit_plan_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_belief.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_belief.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert four_plan._laborheir is None

    # WHEN
    sue_belief.cash_out()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_belief._groupunits,
    )
    assert four_plan._laborheir is not None
    assert four_plan._laborheir == x_laborheir


def test_BeliefUnit_cash_out_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario1_solo_AttrIsPassed():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    swim_str = "swimming"
    swim_rope = sue_belief.make_l1_rope(swim_str)
    morn_str = "morning"
    morn_rope = sue_belief.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_belief.make_rope(morn_rope, four_str)
    swimmers_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    swimmers_solo_bool = True
    swimmers_laborunit.add_party(swimmers_str, solo=swimmers_solo_bool)

    yao_str = "Yao"
    sue_belief.add_partnerunit(yao_str)
    yao_partnerunit = sue_belief.get_partner(yao_str)
    yao_partnerunit.add_membership(swimmers_str)

    sue_belief.set_l1_plan(planunit_shop(swim_str))
    sue_belief.set_plan(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_belief.set_plan(planunit_shop(four_str), parent_rope=morn_rope)
    sue_belief.edit_plan_attr(swim_rope, laborunit=swimmers_laborunit)
    # print(sue_belief.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_belief.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert not four_plan._laborheir

    # WHEN
    sue_belief.cash_out()

    # THEN
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=swimmers_laborunit,
        groupunits=sue_belief._groupunits,
    )
    assert four_plan._laborheir
    assert four_plan._laborheir == expected_laborheir
    swimmers_party = four_plan._laborheir._partys.get(swimmers_str)
    assert swimmers_party.solo == swimmers_solo_bool


def test_BeliefUnit__get_filtered_awardunits_plan_CleansPlan_Laborunit():
    # ESTABLISH
    sue_str = "Sue"
    sue1_belief = beliefunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_belief.add_partnerunit(xia_str)
    sue1_belief.add_partnerunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_belief.make_l1_rope(swim_str)
    sue1_belief.set_plan(planunit_shop(casa_str), parent_rope=sue1_belief.moment_label)
    sue1_belief.set_plan(planunit_shop(swim_str), parent_rope=sue1_belief.moment_label)
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=xia_str)
    swim_laborunit.add_party(party_title=zoa_str)
    sue1_belief.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_belief_swim_plan = sue1_belief.get_plan_obj(swim_rope)
    sue1_belief_swim_partys = sue1_belief_swim_plan.laborunit._partys
    assert len(sue1_belief_swim_partys) == 2

    # WHEN
    sue2_belief = beliefunit_shop(sue_str)
    sue2_belief.add_partnerunit(xia_str)
    cleaned_plan = sue2_belief._get_filtered_awardunits_plan(sue1_belief_swim_plan)

    # THEN
    cleaned_swim_partys = cleaned_plan.laborunit._partys
    assert len(cleaned_swim_partys) == 1
    assert list(cleaned_swim_partys) == [xia_str]


def test_BeliefUnit_set_plan_CleansPlan_awardunits():
    # ESTABLISH
    sue1_belief = beliefunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_belief.add_partnerunit(xia_str)
    sue1_belief.add_partnerunit(zoa_str)

    casa_str = "casa"
    casa_rope = sue1_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = sue1_belief.make_l1_rope(swim_str)
    sue1_belief.set_plan(planunit_shop(casa_str), parent_rope=sue1_belief.moment_label)
    sue1_belief.set_plan(planunit_shop(swim_str), parent_rope=sue1_belief.moment_label)
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=xia_str)
    swim_laborunit.add_party(party_title=zoa_str)
    sue1_belief.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_belief_swim_plan = sue1_belief.get_plan_obj(swim_rope)
    sue1_belief_swim_partys = sue1_belief_swim_plan.laborunit._partys
    assert len(sue1_belief_swim_partys) == 2

    # WHEN
    sue2_belief = beliefunit_shop("Sue")
    sue2_belief.add_partnerunit(xia_str)
    sue2_belief.set_l1_plan(
        sue1_belief_swim_plan, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_belief_swim_plan = sue2_belief.get_plan_obj(swim_rope)
    sue2_belief_swim_partys = sue2_belief_swim_plan.laborunit._partys
    assert len(sue2_belief_swim_partys) == 1
    assert list(sue2_belief_swim_partys) == [xia_str]
