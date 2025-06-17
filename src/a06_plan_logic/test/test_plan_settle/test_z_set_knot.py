from pytest import raises as pytest_raises
from src.a01_term_logic.rope import create_rope, to_rope
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_vow_label as root_label,
)
from src.a06_plan_logic._util.example_plans import get_planunit_with_4_levels
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_set_vow_label_CorrectlySetsAttr():
    # ESTABLISH
    x_vow_label = "accord45"
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    assert sue_plan.vow_label == root_label()

    # WHEN
    sue_plan.set_vow_label(vow_label=x_vow_label)

    # THEN
    assert sue_plan.vow_label == x_vow_label


def test_PlanUnit_set_concept_CorrectlySetsvow_label_AND_fund_iota():
    # ESTABLISH'
    x_fund_iota = 500
    sue_plan = get_planunit_with_4_levels()
    sue_plan.fund_iota = x_fund_iota
    plan_vow_label = "Texas"
    sue_plan.set_vow_label(plan_vow_label)
    assert sue_plan.vow_label == plan_vow_label

    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, "cleaning")
    cookery_str = "cookery to use"
    cookery_rope = sue_plan.make_rope(clean_rope, cookery_str)

    # WHEN
    sue_plan.set_concept(conceptunit_shop(cookery_str), clean_rope)

    # THEN
    cookery_concept = sue_plan.get_concept_obj(cookery_rope)
    assert cookery_concept.vow_label == plan_vow_label
    assert cookery_concept.fund_iota == x_fund_iota


def test_plan_set_vow_label_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(owner_name=yao_str)
    casa_str = "casa"
    old_casa_rope = yao_plan.make_l1_rope(casa_str)
    swim_str = "swim"
    old_swim_rope = yao_plan.make_rope(old_casa_rope, swim_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    yao_plan.set_concept(conceptunit_shop(swim_str), parent_rope=old_casa_rope)
    assert yao_plan.owner_name == yao_str
    assert yao_plan.conceptroot.concept_label == yao_plan.vow_label
    casa_concept = yao_plan.get_concept_obj(old_casa_rope)
    assert casa_concept.parent_rope == to_rope(yao_plan.vow_label)
    swim_concept = yao_plan.get_concept_obj(old_swim_rope)
    assert swim_concept.parent_rope == old_casa_rope
    assert yao_plan.vow_label == yao_plan.vow_label

    # WHEN
    x_vow_label = "accord45"
    yao_plan.set_vow_label(vow_label=x_vow_label)

    # THEN
    new_casa_rope = yao_plan.make_l1_rope(casa_str)
    swim_str = "swim"
    new_swim_rope = yao_plan.make_rope(new_casa_rope, swim_str)
    assert yao_plan.vow_label == x_vow_label
    assert yao_plan.conceptroot.concept_label == x_vow_label
    casa_concept = yao_plan.get_concept_obj(new_casa_rope)
    assert casa_concept.parent_rope == to_rope(x_vow_label)
    swim_concept = yao_plan.get_concept_obj(new_swim_rope)
    assert swim_concept.parent_rope == new_casa_rope


def test_plan_set_knot_RaisesErrorIfNew_knot_IsAnConcept_label():
    # ESTABLISH
    zia_plan = planunit_shop("Zia", "Texas")
    print(f"{zia_plan.max_tree_traverse=}")
    casa_str = "casa"
    casa_rope = zia_plan.make_l1_rope(casa_str)
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_plan.set_concept(conceptunit_shop(casa_str), parent_rope=casa_rope)

    # WHEN / THEN
    casa_rope = zia_plan.make_rope(casa_rope, casa_str)
    print(f"{casa_rope=}")
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_knot(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify knot to '{slash_str}' because it exists an concept concept_label '{casa_rope}'"
    )


def test_plan_set_knot_CorrectlyModifies_parent_rope():
    # ESTABLISH
    zia_plan = planunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    semicolon_casa_rope = zia_plan.make_l1_rope(casa_str)
    cook_str = "cook"
    zia_plan.set_concept(conceptunit_shop(cook_str), semicolon_casa_rope)
    semicolon_cook_rope = zia_plan.make_rope(semicolon_casa_rope, cook_str)
    cook_concept = zia_plan.get_concept_obj(semicolon_cook_rope)
    semicolon_str = ";"
    assert zia_plan.knot == semicolon_str
    semicolon_cook_rope = zia_plan.make_rope(semicolon_casa_rope, cook_str)
    # print(f"{zia_plan.vow_label=} {zia_plan.conceptroot.concept_label=} {casa_rope=}")
    # print(f"{cook_concept.parent_rope=} {cook_concept.concept_label=}")
    # semicolon_casa_concept = zia_plan.get_concept_obj(semicolon_casa_rope)
    # print(f"{semicolon_casa_concept.parent_rope=} {semicolon_casa_concept.concept_label=}")
    assert cook_concept.get_concept_rope() == semicolon_cook_rope

    # WHEN
    slash_str = "/"
    zia_plan.set_knot(slash_str)

    # THEN
    assert cook_concept.get_concept_rope() != semicolon_cook_rope
    zia_vow_label = zia_plan.vow_label
    slash_casa_rope = create_rope(zia_vow_label, casa_str, knot=slash_str)
    slash_cook_rope = create_rope(slash_casa_rope, cook_str, knot=slash_str)
    assert cook_concept.get_concept_rope() == slash_cook_rope


def test_plan_set_knot_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_plan = planunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    time_str = "time"
    semicolon_time_rope = zia_plan.make_l1_rope(time_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_plan.make_rope(semicolon_time_rope, _8am_str)

    semicolon_time_reasonunit = reasonunit_shop(rcontext=semicolon_time_rope)
    semicolon_time_reasonunit.set_premise(semicolon_8am_rope)

    semicolon_casa_rope = zia_plan.make_l1_rope(casa_str)
    zia_plan.edit_concept_attr(semicolon_casa_rope, reason=semicolon_time_reasonunit)
    casa_concept = zia_plan.get_concept_obj(semicolon_casa_rope)
    assert casa_concept.reasonunits.get(semicolon_time_rope) is not None
    gen_time_reasonunit = casa_concept.reasonunits.get(semicolon_time_rope)
    assert gen_time_reasonunit.premises.get(semicolon_8am_rope) is not None

    # WHEN
    slash_str = "/"
    zia_plan.set_knot(slash_str)

    # THEN
    slash_time_rope = zia_plan.make_l1_rope(time_str)
    slash_8am_rope = zia_plan.make_rope(slash_time_rope, _8am_str)
    slash_casa_rope = zia_plan.make_l1_rope(casa_str)
    casa_concept = zia_plan.get_concept_obj(slash_casa_rope)
    slash_time_rope = zia_plan.make_l1_rope(time_str)
    slash_8am_rope = zia_plan.make_rope(slash_time_rope, _8am_str)
    assert casa_concept.reasonunits.get(slash_time_rope) is not None
    gen_time_reasonunit = casa_concept.reasonunits.get(slash_time_rope)
    assert gen_time_reasonunit.premises.get(slash_8am_rope) is not None

    assert casa_concept.reasonunits.get(semicolon_time_rope) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_rope) is None


def test_plan_set_knot_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_plan = planunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    time_str = "time"
    semicolon_time_rope = zia_plan.make_l1_rope(time_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_plan.make_rope(semicolon_time_rope, _8am_str)
    semicolon_time_factunit = factunit_shop(semicolon_time_rope, semicolon_8am_rope)

    semicolon_casa_rope = zia_plan.make_l1_rope(casa_str)
    zia_plan.edit_concept_attr(semicolon_casa_rope, factunit=semicolon_time_factunit)
    casa_concept = zia_plan.get_concept_obj(semicolon_casa_rope)
    print(f"{casa_concept.factunits=} {semicolon_time_rope=}")
    assert casa_concept.factunits.get(semicolon_time_rope) is not None
    gen_time_factunit = casa_concept.factunits.get(semicolon_time_rope)

    # WHEN
    slash_str = "/"
    zia_plan.set_knot(slash_str)

    # THEN
    slash_time_rope = zia_plan.make_l1_rope(time_str)
    slash_casa_rope = zia_plan.make_l1_rope(casa_str)
    casa_concept = zia_plan.get_concept_obj(slash_casa_rope)
    slash_time_rope = zia_plan.make_l1_rope(time_str)
    slash_8am_rope = zia_plan.make_rope(slash_time_rope, _8am_str)
    assert casa_concept.factunits.get(slash_time_rope) is not None
    gen_time_factunit = casa_concept.factunits.get(slash_time_rope)
    assert gen_time_factunit.fcontext is not None
    assert gen_time_factunit.fcontext == slash_time_rope
    assert gen_time_factunit.fstate is not None
    assert gen_time_factunit.fstate == slash_8am_rope

    assert casa_concept.factunits.get(semicolon_time_rope) is None


def test_PlanUnit_set_knot_CorrectlySetsAttr():
    # ESTABLISH
    x_vow_label = "accord45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str, x_vow_label, knot=slash_knot)
    assert sue_plan.knot == slash_knot

    # WHEN
    at_label_knot = "@"
    sue_plan.set_knot(new_knot=at_label_knot)

    # THEN
    assert sue_plan.knot == at_label_knot
