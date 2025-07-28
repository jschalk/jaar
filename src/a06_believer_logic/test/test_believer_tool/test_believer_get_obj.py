from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.believer_tool import (
    believer_get_obj,
    believer_partner_membership_get_obj,
    believer_partnerunit_get_obj,
    believer_plan_awardlink_get_obj,
    believer_plan_factunit_get_obj,
    believer_plan_reason_caseunit_get_obj as caseunit_get_obj,
    believer_plan_reasonunit_get_obj,
    believer_planunit_get_obj,
)
from src.a06_believer_logic.test._util.a06_str import (
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str as caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    f_context_str,
    f_state_str,
    plan_rope_str,
    reason_context_str,
    reason_state_str,
)


def test_believer_partnerunit_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_believer.add_partnerunit(yao_str)

    # WHEN
    x_obj = believer_partnerunit_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_partner(yao_str)


def test_believer_partner_membership_get_obj_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_believer = believerunit_shop("Sue")
    jkeys = {"partner_name": yao_str, "group_title": swim_str}
    sue_believer.add_partnerunit(yao_str)
    sue_believer.get_partner(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = believer_partner_membership_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_partner(yao_str).get_membership(swim_str)


def test_believer_planunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope}

    # WHEN
    x_obj = believer_planunit_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope)


def test_believer_plan_awardlink_get_obj_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_believer.add_plan(casa_rope)
    sue_believer.get_plan_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = believer_plan_awardlink_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).get_awardlink(swim_str)


def test_believer_plan_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    wk_rope = sue_believer.make_l1_rope("wk")
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, reason_context_str(): wk_rope}
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = believer_plan_reasonunit_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_believer_plan_reason_caseunit_get_obj_ReturnsObj():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    thur_rope = sue_believer.make_rope(wk_rope, "thur")
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        reason_context_str(): wk_rope,
        reason_state_str(): thur_rope,
    }
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.add_plan(thur_rope)
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_believer, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_believer_plan_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    wk_rope = sue_believer.make_l1_rope("wk")
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, f_context_str(): wk_rope}
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = believer_plan_factunit_get_obj(sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).factunits.get(wk_rope)


def test_believer_get_obj_ReturnsObj_BelieverUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_believer.add_partnerunit(yao_str)

    # WHEN
    x_obj = believer_get_obj(believerunit_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer


def test_believer_get_obj_ReturnsObj_believer_partnerunit_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    jkeys = {"partner_name": yao_str}
    sue_believer.add_partnerunit(yao_str)

    # WHEN
    x_obj = believer_get_obj(believer_partnerunit_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_partner(yao_str)


def test_believer_get_obj_ReturnsObj_believer_partner_membership_get_obj():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_believer = believerunit_shop("Sue")
    jkeys = {"partner_name": yao_str, "group_title": swim_str}
    sue_believer.add_partnerunit(yao_str)
    sue_believer.get_partner(yao_str).add_membership(swim_str)

    # WHEN
    x_obj = believer_get_obj(believer_partner_membership_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_partner(yao_str).get_membership(swim_str)


def test_believer_get_obj_ReturnsObj_believer_planunit_get_obj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope}

    # WHEN
    x_obj = believer_get_obj(believer_planunit_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope)


def test_believer_get_obj_ReturnsObj_believer_plan_awardlink_get_obj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    swim_str = "swim"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, "awardee_title": swim_str}
    sue_believer.add_plan(casa_rope)
    sue_believer.get_plan_obj(casa_rope).set_awardlink(awardlink_shop(swim_str))

    # WHEN
    x_obj = believer_get_obj(believer_plan_awardlink_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).get_awardlink(swim_str)


def test_believer_get_obj_ReturnsObj_believer_plan_reasonunit_get_obj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    wk_rope = sue_believer.make_l1_rope("wk")
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, reason_context_str(): wk_rope}
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = believer_get_obj(believer_plan_reasonunit_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_believer_get_obj_ReturnsObj_believer_plan_reason_caseunit_get_obj():
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    wk_str = "wk"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    thur_rope = sue_believer.make_rope(wk_rope, "thur")
    casa_jkeys = {
        plan_rope_str(): casa_rope,
        reason_context_str(): wk_rope,
        reason_state_str(): thur_rope,
    }
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.add_plan(thur_rope)
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = believer_get_obj(caseunit_str(), sue_believer, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_believer_get_obj_ReturnsObj_believer_plan_factunit_get_obj():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    wk_rope = sue_believer.make_l1_rope("wk")
    sue_believer.add_plan(casa_rope)
    jkeys = {plan_rope_str(): casa_rope, f_context_str(): wk_rope}
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(wk_rope)
    sue_believer.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = believer_get_obj(believer_plan_factunit_str(), sue_believer, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_believer.get_plan_obj(casa_rope).factunits.get(wk_rope)
