from src.ch02_rope.rope import to_rope
from src.ch04_voice.group import awardunit_shop
from src.ch05_reason.reason import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_attr_exists,
    belief_plan_awardunit_exists,
    belief_plan_factunit_exists,
    belief_plan_healerunit_exists,
    belief_plan_partyunit_exists,
    belief_plan_reason_caseunit_exists as caseunit_exists,
    belief_plan_reasonunit_exists,
    belief_planunit_exists,
    belief_voice_membership_exists,
    belief_voiceunit_exists,
    beliefunit_exists,
)
from src.ref.keywords import Ch07Keywords as wx


def test_beliefunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not beliefunit_exists(None)
    assert beliefunit_exists(beliefunit_shop("Sue"))


def test_belief_voiceunit_exists_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {wx.voice_name: yao_str}

    # WHEN / THEN
    assert not belief_voiceunit_exists(None, {})
    assert not belief_voiceunit_exists(sue_belief, jkeys)

    # WHEN
    sue_belief.add_voiceunit(yao_str)

    # THEN
    assert belief_voiceunit_exists(sue_belief, jkeys)


def test_belief_voice_membership_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {wx.voice_name: yao_str, wx.group_title: swim_str}

    # WHEN / THEN
    assert not belief_voice_membership_exists(None, {})
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    sue_belief.add_voiceunit(yao_str)
    # THEN
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    yao_plan = sue_belief.get_voice(yao_str)
    yao_plan.add_membership(";run")
    # THEN
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    yao_plan = sue_belief.get_voice(yao_str)
    yao_plan.add_membership(swim_str)
    # THEN
    assert belief_voice_membership_exists(sue_belief, jkeys)


def test_belief_planunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    root_rope = sue_belief.planroot.get_plan_rope()
    root_jkeys = {wx.plan_rope: root_rope}
    casa_jkeys = {wx.plan_rope: casa_rope}
    clean_jkeys = {wx.plan_rope: clean_rope}
    sweep_jkeys = {wx.plan_rope: sweep_rope}

    # WHEN / THEN
    assert not belief_planunit_exists(None, {})
    assert not belief_planunit_exists(sue_belief, {})
    assert belief_planunit_exists(sue_belief, root_jkeys)
    assert not belief_planunit_exists(sue_belief, casa_jkeys)
    assert not belief_planunit_exists(sue_belief, clean_jkeys)
    assert not belief_planunit_exists(sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_plan(casa_rope)
    # THEN
    assert not belief_planunit_exists(sue_belief, {})
    assert belief_planunit_exists(sue_belief, root_jkeys)
    assert belief_planunit_exists(sue_belief, casa_jkeys)
    assert not belief_planunit_exists(sue_belief, clean_jkeys)
    assert not belief_planunit_exists(sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_plan(clean_rope)
    # THEN
    assert not belief_planunit_exists(sue_belief, {})
    assert belief_planunit_exists(sue_belief, root_jkeys)
    assert belief_planunit_exists(sue_belief, casa_jkeys)
    assert belief_planunit_exists(sue_belief, clean_jkeys)
    assert not belief_planunit_exists(sue_belief, sweep_jkeys)


def test_belief_plan_awardunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    root_rope = sue_belief.planroot.get_plan_rope()
    root_jkeys = {wx.plan_rope: root_rope, wx.awardee_title: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.awardee_title: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.awardee_title: swim_str}

    # WHEN / THEN
    assert not belief_plan_awardunit_exists(None, {})
    assert not belief_plan_awardunit_exists(sue_belief, {})
    assert not belief_plan_awardunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_awardunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_awardunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.set_awardunit(awardunit_shop(swim_str))

    # THEN
    assert not belief_plan_awardunit_exists(sue_belief, {})
    assert belief_plan_awardunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_awardunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_awardunit_exists(sue_belief, clean_jkeys)


def test_belief_plan_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    root_jkeys = {wx.plan_rope: root_rope, wx.reason_context: wk_rope}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.reason_context: wk_rope}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.reason_context: wk_rope}

    # WHEN / THEN
    assert not belief_plan_reasonunit_exists(None, {})
    assert not belief_plan_reasonunit_exists(sue_belief, {})
    assert not belief_plan_reasonunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_reasonunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_reasonunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not belief_plan_reasonunit_exists(sue_belief, {})
    assert belief_plan_reasonunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_reasonunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_reasonunit_exists(sue_belief, clean_jkeys)


def test_belief_plan_reason_caseunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    root_jkeys = {
        wx.plan_rope: root_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }
    casa_jkeys = {
        wx.plan_rope: casa_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }
    clean_jkeys = {
        wx.plan_rope: clean_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not caseunit_exists(None, {})
    assert not caseunit_exists(sue_belief, {})
    assert not caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not caseunit_exists(sue_belief, {})
    assert not caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(thur_rope)
    sue_belief.planroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not caseunit_exists(sue_belief, {})
    assert caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)


def test_belief_plan_partyunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    root_jkeys = {wx.plan_rope: root_rope, wx.party_title: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.party_title: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.party_title: swim_str}

    # WHEN / THEN
    assert not belief_plan_partyunit_exists(None, {})
    assert not belief_plan_partyunit_exists(sue_belief, {})
    assert not belief_plan_partyunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_partyunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_partyunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.laborunit.add_party(swim_str)

    # THEN
    assert not belief_plan_partyunit_exists(sue_belief, {})
    assert belief_plan_partyunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_partyunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_partyunit_exists(sue_belief, clean_jkeys)


def test_belief_plan_healerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    root_jkeys = {wx.plan_rope: root_rope, wx.healer_name: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.healer_name: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.healer_name: swim_str}

    # WHEN / THEN
    assert not belief_plan_healerunit_exists(None, {})
    assert not belief_plan_healerunit_exists(sue_belief, {})
    assert not belief_plan_healerunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_healerunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_healerunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.healerunit.set_healer_name(swim_str)

    # THEN
    assert not belief_plan_healerunit_exists(sue_belief, {})
    assert belief_plan_healerunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_healerunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_healerunit_exists(sue_belief, clean_jkeys)


def test_belief_plan_factunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    root_jkeys = {wx.plan_rope: root_rope, wx.fact_context: wk_rope}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.fact_context: wk_rope}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.fact_context: wk_rope}

    # WHEN / THEN
    assert not belief_plan_factunit_exists(None, {})
    assert not belief_plan_factunit_exists(sue_belief, {})
    assert not belief_plan_factunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_factunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_factunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not belief_plan_factunit_exists(sue_belief, {})
    assert belief_plan_factunit_exists(sue_belief, root_jkeys)
    assert not belief_plan_factunit_exists(sue_belief, casa_jkeys)
    assert not belief_plan_factunit_exists(sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_beliefunit():
    # ESTABLISH / WHEN / THEN
    assert not belief_attr_exists(wx.beliefunit, None, {})
    assert belief_attr_exists(wx.beliefunit, beliefunit_shop("Sue"), {})


def test_belief_attr_exists_ReturnsObj_belief_voiceunit():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    x_jkeys = {wx.voice_name: yao_str}

    # WHEN / THEN
    assert not belief_attr_exists(wx.belief_voiceunit, None, {})
    assert not belief_attr_exists(wx.belief_voiceunit, sue_belief, x_jkeys)

    # WHEN
    sue_belief.add_voiceunit(yao_str)

    # THEN
    assert belief_attr_exists(wx.belief_voiceunit, sue_belief, x_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_voice_membership():
    # ESTABLISH
    yao_str = "Yao"
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    x_jkeys = {wx.voice_name: yao_str, wx.group_title: swim_str}
    x_dimen = wx.belief_voice_membership

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    sue_belief.add_voiceunit(yao_str)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    yao_plan = sue_belief.get_voice(yao_str)
    yao_plan.add_membership(";run")
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    yao_plan = sue_belief.get_voice(yao_str)
    yao_plan.add_membership(swim_str)
    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, x_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_planunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    x_parent_rope = sue_belief.planroot.get_plan_rope()
    root_jkeys = {wx.plan_rope: x_parent_rope}
    casa_jkeys = {wx.plan_rope: casa_rope}
    clean_jkeys = {wx.plan_rope: clean_rope}
    sweep_jkeys = {wx.plan_rope: sweep_rope}
    x_dimen = wx.belief_planunit

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_plan(casa_rope)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_plan(clean_rope)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_awardunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    x_dimen = wx.belief_plan_awardunit
    root_jkeys = {wx.plan_rope: root_rope, wx.awardee_title: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.awardee_title: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.awardee_title: swim_str}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.set_awardunit(awardunit_shop(swim_str))

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_reasonunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    x_dimen = wx.belief_plan_reasonunit
    root_jkeys = {wx.plan_rope: root_rope, wx.reason_context: wk_rope}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.reason_context: wk_rope}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.reason_context: wk_rope}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_reason_caseunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    x_dimen = wx.belief_plan_reason_caseunit
    root_jkeys = {
        wx.plan_rope: root_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }
    casa_jkeys = {
        wx.plan_rope: casa_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }
    clean_jkeys = {
        wx.plan_rope: clean_rope,
        wx.reason_context: wk_rope,
        wx.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(thur_rope)
    sue_belief.planroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_partyunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    x_dimen = wx.belief_plan_partyunit
    root_jkeys = {wx.plan_rope: root_rope, wx.party_title: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.party_title: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.party_title: swim_str}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.laborunit.add_party(swim_str)

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_healerunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    swim_str = "Swim"
    x_dimen = wx.belief_plan_healerunit
    root_jkeys = {wx.plan_rope: root_rope, wx.healer_name: swim_str}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.healer_name: swim_str}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.healer_name: swim_str}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.planroot.healerunit.set_healer_name(swim_str)

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_plan_factunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = sue_belief.make_rope(casa_rope, clean_str)
    root_rope = sue_belief.planroot.get_plan_rope()
    wk_str = "wk"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    x_dimen = wx.belief_plan_factunit
    root_jkeys = {wx.plan_rope: root_rope, wx.fact_context: wk_rope}
    casa_jkeys = {wx.plan_rope: casa_rope, wx.fact_context: wk_rope}
    clean_jkeys = {wx.plan_rope: clean_rope, wx.fact_context: wk_rope}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_plan(wk_rope)
    sue_belief.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
