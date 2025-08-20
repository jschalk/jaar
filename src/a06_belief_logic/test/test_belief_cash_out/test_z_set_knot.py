from pytest import raises as pytest_raises
from src.a01_term_logic.rope import create_rope, to_rope
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a05_plan_logic.plan import get_default_coin_label as root_label, planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.example_beliefs import get_beliefunit_with_4_levels


def test_BeliefUnit_set_coin_label_SetsAttr():
    # ESTABLISH
    x_coin_label = "amy45"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    assert sue_belief.coin_label == root_label()

    # WHEN
    sue_belief.set_coin_label(coin_label=x_coin_label)

    # THEN
    assert sue_belief.coin_label == x_coin_label


def test_BeliefUnit_set_plan_Setscoin_label_AND_fund_iota():
    # ESTABLISH'
    x_fund_iota = 500
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.fund_iota = x_fund_iota
    belief_coin_label = "Texas"
    sue_belief.set_coin_label(belief_coin_label)
    assert sue_belief.coin_label == belief_coin_label

    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "cleaning")
    cookery_str = "cookery to use"
    cookery_rope = sue_belief.make_rope(clean_rope, cookery_str)

    # WHEN
    sue_belief.set_plan(planunit_shop(cookery_str), clean_rope)

    # THEN
    cookery_plan = sue_belief.get_plan_obj(cookery_rope)
    assert cookery_plan.coin_label == belief_coin_label
    assert cookery_plan.fund_iota == x_fund_iota


def test_belief_set_coin_label_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(belief_name=yao_str)
    casa_str = "casa"
    old_casa_rope = yao_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    old_swim_rope = yao_belief.make_rope(old_casa_rope, swim_str)
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(swim_str), parent_rope=old_casa_rope)
    assert yao_belief.belief_name == yao_str
    assert yao_belief.planroot.plan_label == yao_belief.coin_label
    casa_plan = yao_belief.get_plan_obj(old_casa_rope)
    assert casa_plan.parent_rope == to_rope(yao_belief.coin_label)
    swim_plan = yao_belief.get_plan_obj(old_swim_rope)
    assert swim_plan.parent_rope == old_casa_rope
    assert yao_belief.coin_label == yao_belief.coin_label

    # WHEN
    x_coin_label = "amy45"
    yao_belief.set_coin_label(coin_label=x_coin_label)

    # THEN
    new_casa_rope = yao_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    new_swim_rope = yao_belief.make_rope(new_casa_rope, swim_str)
    assert yao_belief.coin_label == x_coin_label
    assert yao_belief.planroot.plan_label == x_coin_label
    casa_plan = yao_belief.get_plan_obj(new_casa_rope)
    assert casa_plan.parent_rope == to_rope(x_coin_label)
    swim_plan = yao_belief.get_plan_obj(new_swim_rope)
    assert swim_plan.parent_rope == new_casa_rope


def test_belief_set_knot_RaisesErrorIfNew_knot_IsAnPlan_label():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    print(f"{zia_belief.max_tree_traverse=}")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_belief.set_plan(planunit_shop(casa_str), parent_rope=casa_rope)

    # WHEN / THEN
    casa_rope = zia_belief.make_rope(casa_rope, casa_str)
    print(f"{casa_rope=}")
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_knot(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify knot to '{slash_str}' because it exists an plan plan_label '{casa_rope}'"
    )


def test_belief_set_knot_Modifies_parent_rope():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    semicolon_casa_rope = zia_belief.make_l1_rope(casa_str)
    cook_str = "cook"
    zia_belief.set_plan(planunit_shop(cook_str), semicolon_casa_rope)
    semicolon_cook_rope = zia_belief.make_rope(semicolon_casa_rope, cook_str)
    cook_plan = zia_belief.get_plan_obj(semicolon_cook_rope)
    semicolon_str = ";"
    assert zia_belief.knot == semicolon_str
    semicolon_cook_rope = zia_belief.make_rope(semicolon_casa_rope, cook_str)
    # print(f"{zia_belief.coin_label=} {zia_belief.planroot.plan_label=} {casa_rope=}")
    # print(f"{cook_plan.parent_rope=} {cook_plan.plan_label=}")
    # semicolon_casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    # print(f"{semicolon_casa_plan.parent_rope=} {semicolon_casa_plan.plan_label=}")
    assert cook_plan.get_plan_rope() == semicolon_cook_rope

    # WHEN
    slash_str = "/"
    zia_belief.set_knot(slash_str)

    # THEN
    assert cook_plan.get_plan_rope() != semicolon_cook_rope
    zia_coin_label = zia_belief.coin_label
    slash_casa_rope = create_rope(zia_coin_label, casa_str, knot=slash_str)
    slash_cook_rope = create_rope(slash_casa_rope, cook_str, knot=slash_str)
    assert cook_plan.get_plan_rope() == slash_cook_rope


def test_belief_set_knot_ModifiesReasonUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    ziet_str = "ziet"
    semicolon_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_belief.make_rope(semicolon_ziet_rope, _8am_str)

    semicolon_ziet_reasonunit = reasonunit_shop(reason_context=semicolon_ziet_rope)
    semicolon_ziet_reasonunit.set_case(semicolon_8am_rope)

    semicolon_casa_rope = zia_belief.make_l1_rope(casa_str)
    zia_belief.edit_plan_attr(semicolon_casa_rope, reason=semicolon_ziet_reasonunit)
    casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    assert casa_plan.reasonunits.get(semicolon_ziet_rope) is not None
    gen_ziet_reasonunit = casa_plan.reasonunits.get(semicolon_ziet_rope)
    assert gen_ziet_reasonunit.cases.get(semicolon_8am_rope) is not None

    # WHEN
    slash_str = "/"
    zia_belief.set_knot(slash_str)

    # THEN
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    slash_casa_rope = zia_belief.make_l1_rope(casa_str)
    casa_plan = zia_belief.get_plan_obj(slash_casa_rope)
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    assert casa_plan.reasonunits.get(slash_ziet_rope) is not None
    gen_ziet_reasonunit = casa_plan.reasonunits.get(slash_ziet_rope)
    assert gen_ziet_reasonunit.cases.get(slash_8am_rope) is not None

    assert casa_plan.reasonunits.get(semicolon_ziet_rope) is None
    assert gen_ziet_reasonunit.cases.get(semicolon_8am_rope) is None


def test_belief_set_knot_ModifiesFactUnit():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    ziet_str = "ziet"
    semicolon_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_belief.make_rope(semicolon_ziet_rope, _8am_str)
    semicolon_ziet_factunit = factunit_shop(semicolon_ziet_rope, semicolon_8am_rope)

    semicolon_casa_rope = zia_belief.make_l1_rope(casa_str)
    zia_belief.edit_plan_attr(semicolon_casa_rope, factunit=semicolon_ziet_factunit)
    casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    print(f"{casa_plan.factunits=} {semicolon_ziet_rope=}")
    assert casa_plan.factunits.get(semicolon_ziet_rope) is not None
    gen_ziet_factunit = casa_plan.factunits.get(semicolon_ziet_rope)

    # WHEN
    slash_str = "/"
    zia_belief.set_knot(slash_str)

    # THEN
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_casa_rope = zia_belief.make_l1_rope(casa_str)
    casa_plan = zia_belief.get_plan_obj(slash_casa_rope)
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    assert casa_plan.factunits.get(slash_ziet_rope) is not None
    gen_ziet_factunit = casa_plan.factunits.get(slash_ziet_rope)
    assert gen_ziet_factunit.fact_context is not None
    assert gen_ziet_factunit.fact_context == slash_ziet_rope
    assert gen_ziet_factunit.fact_state is not None
    assert gen_ziet_factunit.fact_state == slash_8am_rope

    assert casa_plan.factunits.get(semicolon_ziet_rope) is None


def test_BeliefUnit_set_knot_SetsAttr():
    # ESTABLISH
    x_coin_label = "amy45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, x_coin_label, knot=slash_knot)
    assert sue_belief.knot == slash_knot

    # WHEN
    at_label_knot = "@"
    sue_belief.set_knot(new_knot=at_label_knot)

    # THEN
    assert sue_belief.knot == at_label_knot
