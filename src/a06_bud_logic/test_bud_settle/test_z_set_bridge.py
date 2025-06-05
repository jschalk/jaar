from pytest import raises as pytest_raises
from src.a01_term_logic.way import create_way, to_way
from src.a04_reason_logic.reason_concept import factunit_shop, reasonunit_shop
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_vow_label as root_label,
)
from src.a06_bud_logic._test_util.example_buds import get_budunit_with_4_levels
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_set_vow_label_CorrectlySetsAttr():
    # ESTABLISH
    x_vow_label = "accord45"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert sue_bud.vow_label == root_label()

    # WHEN
    sue_bud.set_vow_label(vow_label=x_vow_label)

    # THEN
    assert sue_bud.vow_label == x_vow_label


def test_BudUnit_set_concept_CorrectlySetsvow_label_AND_fund_iota():
    # ESTABLISH'
    x_fund_iota = 500
    sue_bud = get_budunit_with_4_levels()
    sue_bud.fund_iota = x_fund_iota
    bud_vow_label = "Texas"
    sue_bud.set_vow_label(bud_vow_label)
    assert sue_bud.vow_label == bud_vow_label

    casa_way = sue_bud.make_l1_way("casa")
    clean_way = sue_bud.make_way(casa_way, "cleaning")
    cookery_str = "cookery to use"
    cookery_way = sue_bud.make_way(clean_way, cookery_str)

    # WHEN
    sue_bud.set_concept(conceptunit_shop(cookery_str), clean_way)

    # THEN
    cookery_concept = sue_bud.get_concept_obj(cookery_way)
    assert cookery_concept.vow_label == bud_vow_label
    assert cookery_concept.fund_iota == x_fund_iota


def test_bud_set_vow_label_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    casa_str = "casa"
    old_casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    old_swim_way = yao_bud.make_way(old_casa_way, swim_str)
    yao_bud.set_l1_concept(conceptunit_shop(casa_str))
    yao_bud.set_concept(conceptunit_shop(swim_str), parent_way=old_casa_way)
    assert yao_bud.owner_name == yao_str
    assert yao_bud.conceptroot.concept_label == yao_bud.vow_label
    casa_concept = yao_bud.get_concept_obj(old_casa_way)
    assert casa_concept.parent_way == to_way(yao_bud.vow_label)
    swim_concept = yao_bud.get_concept_obj(old_swim_way)
    assert swim_concept.parent_way == old_casa_way
    assert yao_bud.vow_label == yao_bud.vow_label

    # WHEN
    x_vow_label = "accord45"
    yao_bud.set_vow_label(vow_label=x_vow_label)

    # THEN
    new_casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    new_swim_way = yao_bud.make_way(new_casa_way, swim_str)
    assert yao_bud.vow_label == x_vow_label
    assert yao_bud.conceptroot.concept_label == x_vow_label
    casa_concept = yao_bud.get_concept_obj(new_casa_way)
    assert casa_concept.parent_way == to_way(x_vow_label)
    swim_concept = yao_bud.get_concept_obj(new_swim_way)
    assert swim_concept.parent_way == new_casa_way


def test_bud_set_bridge_RaisesErrorIfNew_bridge_IsAnConcept_label():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    print(f"{zia_bud.max_tree_traverse=}")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_bud.set_concept(conceptunit_shop(casa_str), parent_way=casa_way)

    # WHEN / THEN
    casa_way = zia_bud.make_way(casa_way, casa_str)
    print(f"{casa_way=}")
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_bridge(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify bridge to '{slash_str}' because it exists an concept concept_label '{casa_way}'"
    )


def test_bud_set_bridge_CorrectlyModifies_parent_way():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    cook_str = "cook"
    zia_bud.set_concept(conceptunit_shop(cook_str), semicolon_casa_way)
    semicolon_cook_way = zia_bud.make_way(semicolon_casa_way, cook_str)
    cook_concept = zia_bud.get_concept_obj(semicolon_cook_way)
    semicolon_str = ";"
    assert zia_bud.bridge == semicolon_str
    semicolon_cook_way = zia_bud.make_way(semicolon_casa_way, cook_str)
    # print(f"{zia_bud.vow_label=} {zia_bud.conceptroot.concept_label=} {casa_way=}")
    # print(f"{cook_concept.parent_way=} {cook_concept.concept_label=}")
    # semicolon_casa_concept = zia_bud.get_concept_obj(semicolon_casa_way)
    # print(f"{semicolon_casa_concept.parent_way=} {semicolon_casa_concept.concept_label=}")
    assert cook_concept.get_concept_way() == semicolon_cook_way

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    assert cook_concept.get_concept_way() != semicolon_cook_way
    zia_vow_label = zia_bud.vow_label
    slash_casa_way = create_way(zia_vow_label, casa_str, bridge=slash_str)
    slash_cook_way = create_way(slash_casa_way, cook_str, bridge=slash_str)
    assert cook_concept.get_concept_way() == slash_cook_way


def test_bud_set_bridge_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    time_str = "time"
    semicolon_time_way = zia_bud.make_l1_way(time_str)
    _8am_str = "8am"
    semicolon_8am_way = zia_bud.make_way(semicolon_time_way, _8am_str)

    semicolon_time_reasonunit = reasonunit_shop(rcontext=semicolon_time_way)
    semicolon_time_reasonunit.set_premise(semicolon_8am_way)

    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.edit_concept_attr(semicolon_casa_way, reason=semicolon_time_reasonunit)
    casa_concept = zia_bud.get_concept_obj(semicolon_casa_way)
    assert casa_concept.reasonunits.get(semicolon_time_way) is not None
    gen_time_reasonunit = casa_concept.reasonunits.get(semicolon_time_way)
    assert gen_time_reasonunit.premises.get(semicolon_8am_way) is not None

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    slash_casa_way = zia_bud.make_l1_way(casa_str)
    casa_concept = zia_bud.get_concept_obj(slash_casa_way)
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    assert casa_concept.reasonunits.get(slash_time_way) is not None
    gen_time_reasonunit = casa_concept.reasonunits.get(slash_time_way)
    assert gen_time_reasonunit.premises.get(slash_8am_way) is not None

    assert casa_concept.reasonunits.get(semicolon_time_way) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_way) is None


def test_bud_set_bridge_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    time_str = "time"
    semicolon_time_way = zia_bud.make_l1_way(time_str)
    _8am_str = "8am"
    semicolon_8am_way = zia_bud.make_way(semicolon_time_way, _8am_str)
    semicolon_time_factunit = factunit_shop(semicolon_time_way, semicolon_8am_way)

    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.edit_concept_attr(semicolon_casa_way, factunit=semicolon_time_factunit)
    casa_concept = zia_bud.get_concept_obj(semicolon_casa_way)
    print(f"{casa_concept.factunits=} {semicolon_time_way=}")
    assert casa_concept.factunits.get(semicolon_time_way) is not None
    gen_time_factunit = casa_concept.factunits.get(semicolon_time_way)

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_casa_way = zia_bud.make_l1_way(casa_str)
    casa_concept = zia_bud.get_concept_obj(slash_casa_way)
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    assert casa_concept.factunits.get(slash_time_way) is not None
    gen_time_factunit = casa_concept.factunits.get(slash_time_way)
    assert gen_time_factunit.fcontext is not None
    assert gen_time_factunit.fcontext == slash_time_way
    assert gen_time_factunit.fstate is not None
    assert gen_time_factunit.fstate == slash_8am_way

    assert casa_concept.factunits.get(semicolon_time_way) is None


def test_BudUnit_set_bridge_CorrectlySetsAttr():
    # ESTABLISH
    x_vow_label = "accord45"
    slash_bridge = "/"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, x_vow_label, bridge=slash_bridge)
    assert sue_bud.bridge == slash_bridge

    # WHEN
    at_label_bridge = "@"
    sue_bud.set_bridge(new_bridge=at_label_bridge)

    # THEN
    assert sue_bud.bridge == at_label_bridge
