from pytest import raises as pytest_raises
from src.a01_term_logic.rope import create_rope, to_rope
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a05_plan_logic.plan import (
    get_default_belief_label as root_label,
    planunit_shop,
)
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import get_ownerunit_with_4_levels


def test_OwnerUnit_set_belief_label_CorrectlySetsAttr():
    # ESTABLISH
    x_belief_label = "amy45"
    sue_str = "Sue"
    sue_owner = ownerunit_shop(sue_str)
    assert sue_owner.belief_label == root_label()

    # WHEN
    sue_owner.set_belief_label(belief_label=x_belief_label)

    # THEN
    assert sue_owner.belief_label == x_belief_label


def test_OwnerUnit_set_plan_CorrectlySetsbelief_label_AND_fund_iota():
    # ESTABLISH'
    x_fund_iota = 500
    sue_owner = get_ownerunit_with_4_levels()
    sue_owner.fund_iota = x_fund_iota
    owner_belief_label = "Texas"
    sue_owner.set_belief_label(owner_belief_label)
    assert sue_owner.belief_label == owner_belief_label

    casa_rope = sue_owner.make_l1_rope("casa")
    clean_rope = sue_owner.make_rope(casa_rope, "cleaning")
    cookery_str = "cookery to use"
    cookery_rope = sue_owner.make_rope(clean_rope, cookery_str)

    # WHEN
    sue_owner.set_plan(planunit_shop(cookery_str), clean_rope)

    # THEN
    cookery_plan = sue_owner.get_plan_obj(cookery_rope)
    assert cookery_plan.belief_label == owner_belief_label
    assert cookery_plan.fund_iota == x_fund_iota


def test_owner_set_belief_label_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(owner_name=yao_str)
    casa_str = "casa"
    old_casa_rope = yao_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    old_swim_rope = yao_owner.make_rope(old_casa_rope, swim_str)
    yao_owner.set_l1_plan(planunit_shop(casa_str))
    yao_owner.set_plan(planunit_shop(swim_str), parent_rope=old_casa_rope)
    assert yao_owner.owner_name == yao_str
    assert yao_owner.planroot.plan_label == yao_owner.belief_label
    casa_plan = yao_owner.get_plan_obj(old_casa_rope)
    assert casa_plan.parent_rope == to_rope(yao_owner.belief_label)
    swim_plan = yao_owner.get_plan_obj(old_swim_rope)
    assert swim_plan.parent_rope == old_casa_rope
    assert yao_owner.belief_label == yao_owner.belief_label

    # WHEN
    x_belief_label = "amy45"
    yao_owner.set_belief_label(belief_label=x_belief_label)

    # THEN
    new_casa_rope = yao_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    new_swim_rope = yao_owner.make_rope(new_casa_rope, swim_str)
    assert yao_owner.belief_label == x_belief_label
    assert yao_owner.planroot.plan_label == x_belief_label
    casa_plan = yao_owner.get_plan_obj(new_casa_rope)
    assert casa_plan.parent_rope == to_rope(x_belief_label)
    swim_plan = yao_owner.get_plan_obj(new_swim_rope)
    assert swim_plan.parent_rope == new_casa_rope


def test_owner_set_knot_RaisesErrorIfNew_knot_IsAnPlan_label():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia", "Texas")
    print(f"{zia_owner.max_tree_traverse=}")
    casa_str = "casa"
    casa_rope = zia_owner.make_l1_rope(casa_str)
    zia_owner.set_l1_plan(planunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_owner.set_plan(planunit_shop(casa_str), parent_rope=casa_rope)

    # WHEN / THEN
    casa_rope = zia_owner.make_rope(casa_rope, casa_str)
    print(f"{casa_rope=}")
    with pytest_raises(Exception) as excinfo:
        zia_owner.set_knot(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify knot to '{slash_str}' because it exists an plan plan_label '{casa_rope}'"
    )


def test_owner_set_knot_CorrectlyModifies_parent_rope():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_owner.set_l1_plan(planunit_shop(casa_str))
    semicolon_casa_rope = zia_owner.make_l1_rope(casa_str)
    cook_str = "cook"
    zia_owner.set_plan(planunit_shop(cook_str), semicolon_casa_rope)
    semicolon_cook_rope = zia_owner.make_rope(semicolon_casa_rope, cook_str)
    cook_plan = zia_owner.get_plan_obj(semicolon_cook_rope)
    semicolon_str = ";"
    assert zia_owner.knot == semicolon_str
    semicolon_cook_rope = zia_owner.make_rope(semicolon_casa_rope, cook_str)
    # print(f"{zia_owner.belief_label=} {zia_owner.planroot.plan_label=} {casa_rope=}")
    # print(f"{cook_plan.parent_rope=} {cook_plan.plan_label=}")
    # semicolon_casa_plan = zia_owner.get_plan_obj(semicolon_casa_rope)
    # print(f"{semicolon_casa_plan.parent_rope=} {semicolon_casa_plan.plan_label=}")
    assert cook_plan.get_plan_rope() == semicolon_cook_rope

    # WHEN
    slash_str = "/"
    zia_owner.set_knot(slash_str)

    # THEN
    assert cook_plan.get_plan_rope() != semicolon_cook_rope
    zia_belief_label = zia_owner.belief_label
    slash_casa_rope = create_rope(zia_belief_label, casa_str, knot=slash_str)
    slash_cook_rope = create_rope(slash_casa_rope, cook_str, knot=slash_str)
    assert cook_plan.get_plan_rope() == slash_cook_rope


def test_owner_set_knot_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_owner.set_l1_plan(planunit_shop(casa_str))
    time_str = "time"
    semicolon_time_rope = zia_owner.make_l1_rope(time_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_owner.make_rope(semicolon_time_rope, _8am_str)

    semicolon_time_reasonunit = reasonunit_shop(rcontext=semicolon_time_rope)
    semicolon_time_reasonunit.set_premise(semicolon_8am_rope)

    semicolon_casa_rope = zia_owner.make_l1_rope(casa_str)
    zia_owner.edit_plan_attr(semicolon_casa_rope, reason=semicolon_time_reasonunit)
    casa_plan = zia_owner.get_plan_obj(semicolon_casa_rope)
    assert casa_plan.reasonunits.get(semicolon_time_rope) is not None
    gen_time_reasonunit = casa_plan.reasonunits.get(semicolon_time_rope)
    assert gen_time_reasonunit.premises.get(semicolon_8am_rope) is not None

    # WHEN
    slash_str = "/"
    zia_owner.set_knot(slash_str)

    # THEN
    slash_time_rope = zia_owner.make_l1_rope(time_str)
    slash_8am_rope = zia_owner.make_rope(slash_time_rope, _8am_str)
    slash_casa_rope = zia_owner.make_l1_rope(casa_str)
    casa_plan = zia_owner.get_plan_obj(slash_casa_rope)
    slash_time_rope = zia_owner.make_l1_rope(time_str)
    slash_8am_rope = zia_owner.make_rope(slash_time_rope, _8am_str)
    assert casa_plan.reasonunits.get(slash_time_rope) is not None
    gen_time_reasonunit = casa_plan.reasonunits.get(slash_time_rope)
    assert gen_time_reasonunit.premises.get(slash_8am_rope) is not None

    assert casa_plan.reasonunits.get(semicolon_time_rope) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_rope) is None


def test_owner_set_knot_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_owner.set_l1_plan(planunit_shop(casa_str))
    time_str = "time"
    semicolon_time_rope = zia_owner.make_l1_rope(time_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_owner.make_rope(semicolon_time_rope, _8am_str)
    semicolon_time_factunit = factunit_shop(semicolon_time_rope, semicolon_8am_rope)

    semicolon_casa_rope = zia_owner.make_l1_rope(casa_str)
    zia_owner.edit_plan_attr(semicolon_casa_rope, factunit=semicolon_time_factunit)
    casa_plan = zia_owner.get_plan_obj(semicolon_casa_rope)
    print(f"{casa_plan.factunits=} {semicolon_time_rope=}")
    assert casa_plan.factunits.get(semicolon_time_rope) is not None
    gen_time_factunit = casa_plan.factunits.get(semicolon_time_rope)

    # WHEN
    slash_str = "/"
    zia_owner.set_knot(slash_str)

    # THEN
    slash_time_rope = zia_owner.make_l1_rope(time_str)
    slash_casa_rope = zia_owner.make_l1_rope(casa_str)
    casa_plan = zia_owner.get_plan_obj(slash_casa_rope)
    slash_time_rope = zia_owner.make_l1_rope(time_str)
    slash_8am_rope = zia_owner.make_rope(slash_time_rope, _8am_str)
    assert casa_plan.factunits.get(slash_time_rope) is not None
    gen_time_factunit = casa_plan.factunits.get(slash_time_rope)
    assert gen_time_factunit.fcontext is not None
    assert gen_time_factunit.fcontext == slash_time_rope
    assert gen_time_factunit.fstate is not None
    assert gen_time_factunit.fstate == slash_8am_rope

    assert casa_plan.factunits.get(semicolon_time_rope) is None


def test_OwnerUnit_set_knot_CorrectlySetsAttr():
    # ESTABLISH
    x_belief_label = "amy45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_owner = ownerunit_shop(sue_str, x_belief_label, knot=slash_knot)
    assert sue_owner.knot == slash_knot

    # WHEN
    at_label_knot = "@"
    sue_owner.set_knot(new_knot=at_label_knot)

    # THEN
    assert sue_owner.knot == at_label_knot
