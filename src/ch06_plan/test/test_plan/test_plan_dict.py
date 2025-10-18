from src.ch02_rope.rope import create_rope
from src.ch04_voice.group import awardunit_shop
from src.ch04_voice.labor import laborunit_shop
from src.ch05_reason.reason import (
    caseunit_shop,
    factunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import get_obj_from_plan_dict, planunit_shop
from src.ref.keywords import Ch06Keywords as wx


def test_get_obj_from_plan_dict_ReturnsObj():
    # ESTABLISH
    field_str = wx.is_expanded
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str)
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = wx.pledge
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = wx.problem_bool
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = wx.kids
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: {}}, field_str) == {}
    assert get_obj_from_plan_dict({}, field_str) == {}


def test_get_obj_from_plan_dict_Returns_HealerUnit():
    # ESTABLISH
    # WHEN / THEN
    healerunit_key = wx.healerunit
    assert get_obj_from_plan_dict({}, healerunit_key) == healerunit_shop()

    # WHEN
    sue_str = "Sue"
    zia_str = "Zia"
    healerunit_dict = {"healerunit_healer_names": [sue_str, zia_str]}
    planunit_dict = {healerunit_key: healerunit_dict}

    # THEN
    static_healerunit = healerunit_shop()
    static_healerunit.set_healer_name(x_healer_name=sue_str)
    static_healerunit.set_healer_name(x_healer_name=zia_str)
    assert get_obj_from_plan_dict(planunit_dict, healerunit_key) is not None
    assert get_obj_from_plan_dict(planunit_dict, healerunit_key) == static_healerunit


def test_PlanUnit_to_dict_ReturnsCompleteDict():
    # ESTABLISH
    amy_str = "Amy23"
    wk_str = "wk"
    wk_rope = create_rope(amy_str, wk_str)
    wed_str = "Wed"
    wed_rope = create_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case.case_active = True
    usa_case = caseunit_shop(reason_state=usa_rope)
    usa_case.case_active = False

    x1_reasonunits = {
        wk_rope: reasonunit_shop(wk_rope, cases={wed_case.reason_state: wed_case}),
        nation_rope: reasonunit_shop(nation_rope, {usa_case.reason_state: usa_case}),
    }
    wed_cases = {wed_case.reason_state: wed_case}
    usa_cases = {usa_case.reason_state: usa_case}
    x1_reasonheirs = {
        wk_rope: reasonheir_shop(wk_rope, wed_cases, reason_active=True),
        nation_rope: reasonheir_shop(nation_rope, usa_cases, reason_active=False),
    }
    biker_awardee_title = "bikers"
    biker_give_force = 3.0
    biker_take_force = 7.0
    biker_awardunit = awardunit_shop(
        biker_awardee_title, biker_give_force, biker_take_force
    )
    flyer_awardee_title = "flyers"
    flyer_give_force = 6.0
    flyer_take_force = 9.0
    flyer_awardunit = awardunit_shop(
        awardee_title=flyer_awardee_title,
        give_force=flyer_give_force,
        take_force=flyer_take_force,
    )
    biker_and_flyer_awardunits = {
        biker_awardunit.awardee_title: biker_awardunit,
        flyer_awardunit.awardee_title: flyer_awardunit,
    }
    biker_get_dict = {
        wx.awardee_title: biker_awardunit.awardee_title,
        wx.give_force: biker_awardunit.give_force,
        wx.take_force: biker_awardunit.take_force,
    }
    flyer_get_dict = {
        wx.awardee_title: flyer_awardunit.awardee_title,
        wx.give_force: flyer_awardunit.give_force,
        wx.take_force: flyer_awardunit.take_force,
    }
    x1_awardunits = {
        biker_awardee_title: biker_get_dict,
        flyer_awardee_title: flyer_get_dict,
    }
    sue_str = "Sue"
    yao_str = "Yao"
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(sue_str)
    sue_laborunit.add_party(yao_str)
    yao_healerunit = healerunit_shop({yao_str})
    casa_str = "casa"
    casa_rope = create_rope(amy_str, casa_str)
    x_problem_bool = True
    casa_plan = planunit_shop(
        parent_rope=casa_rope,
        kids=None,
        awardunits=biker_and_flyer_awardunits,
        star=30,
        plan_label=casa_str,
        tree_level=1,
        reasonunits=x1_reasonunits,
        reasonheirs=x1_reasonheirs,
        laborunit=sue_laborunit,
        healerunit=yao_healerunit,
        active=True,
        pledge=True,
        problem_bool=x_problem_bool,
    )
    x_factunit = factunit_shop(
        fact_context=wk_rope, fact_state=wk_rope, fact_lower=5, fact_upper=59
    )
    casa_plan.set_factunit(factunit=x_factunit)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_morph = 16
    x_gogo_want = 81
    x_stop_want = 87
    casa_plan.begin = x_begin
    casa_plan.close = x_close
    casa_plan.addin = x_addin
    casa_plan.denom = x_denom
    casa_plan.numor = x_numor
    casa_plan.morph = x_morph
    casa_plan.gogo_want = x_gogo_want
    casa_plan.stop_want = x_stop_want
    casa_plan.uid = 17
    casa_plan.add_kid(planunit_shop("paper"))

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict[wx.kids]) == 1
    assert casa_dict[wx.kids] == casa_plan.get_kids_dict()
    assert casa_dict[wx.reasonunits] == casa_plan.get_reasonunits_dict()
    assert casa_dict[wx.awardunits] == casa_plan.get_awardunits_dict()
    assert casa_dict[wx.awardunits] == x1_awardunits
    assert casa_dict[wx.laborunit] == sue_laborunit.to_dict()
    assert casa_dict[wx.healerunit] == yao_healerunit.to_dict()
    assert casa_dict[wx.star] == casa_plan.star
    assert casa_dict[wx.plan_label] == casa_plan.plan_label
    assert casa_dict["uid"] == casa_plan.uid
    assert casa_dict[wx.begin] == casa_plan.begin
    assert casa_dict[wx.close] == casa_plan.close
    assert casa_dict[wx.numor] == casa_plan.numor
    assert casa_dict[wx.denom] == casa_plan.denom
    assert casa_dict[wx.morph] == casa_plan.morph
    assert casa_dict[wx.gogo_want] == casa_plan.gogo_want
    assert casa_dict[wx.stop_want] == casa_plan.stop_want
    assert casa_dict[wx.pledge] == casa_plan.pledge
    assert casa_dict[wx.problem_bool] == casa_plan.problem_bool
    assert casa_dict[wx.problem_bool] == x_problem_bool
    assert casa_plan.is_expanded
    assert casa_dict.get(wx.is_expanded) is None
    assert len(casa_dict[wx.factunits]) == len(casa_plan.get_factunits_dict())


def test_PlanUnit_to_dict_ReturnsObj_WithoutEmptyAttributes():
    # ESTABLISH
    casa_str = "casa"
    casa_plan = planunit_shop(casa_str)

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict is not None
    assert casa_dict == {wx.plan_label: casa_str, wx.star: 1}


def test_PlanUnit_to_dict_ReturnsObj_DictWith_attrs_SetToTrue():
    # ESTABLISH
    casa_str = "casa"
    casa_plan = planunit_shop(casa_str)
    casa_plan.is_expanded = False
    casa_plan.pledge = True
    ignore_str = "ignore"

    amy_str = "Amy23"
    a_str = "a"
    a_rope = create_rope(amy_str, a_str)
    casa_plan.set_factunit(factunit_shop(a_rope, a_rope))

    yao_str = "Yao"
    casa_plan.set_awardunit(awardunit_shop(yao_str))

    x_laborunit = casa_plan.laborunit
    x_laborunit.add_party(party_title=yao_str)

    clean_str = "clean"
    casa_plan.add_kid(planunit_shop(clean_str))

    assert not casa_plan.is_expanded
    assert casa_plan.pledge
    assert casa_plan.factunits is not None
    assert casa_plan.awardunits is not None
    assert casa_plan.laborunit is not None
    assert casa_plan.kids != {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get(wx.is_expanded) is False
    assert casa_dict.get(wx.pledge)
    assert casa_dict.get(wx.factunits) is not None
    assert casa_dict.get(wx.awardunits) is not None
    assert casa_dict.get(wx.laborunit) is not None
    assert casa_dict.get(wx.kids) is not None


def test_PlanUnit_to_dict_ReturnsDictWithAttrsEmpty():
    # ESTABLISH
    casa_str = "casa"
    casa_plan = planunit_shop(casa_str)
    assert casa_plan.is_expanded
    assert casa_plan.pledge is False
    assert casa_plan.factunits == {}
    assert casa_plan.awardunits == {}
    assert casa_plan.laborunit == laborunit_shop()
    assert casa_plan.healerunit == healerunit_shop()
    assert casa_plan.kids == {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get(wx.is_expanded) is None
    assert casa_dict.get(wx.pledge) is None
    assert casa_dict.get(wx.factunits) is None
    assert casa_dict.get(wx.awardunits) is None
    assert casa_dict.get(wx.laborunit) is None
    assert casa_dict.get(wx.healerunit) is None
    assert casa_dict.get(wx.kids) is None
