from src.a01_term_logic.rope import create_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a04_reason_logic.reason_plan import (
    caseunit_shop,
    factunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import (
    get_default_belief_label as root_label,
    get_obj_from_plan_dict,
    planunit_shop,
)


def test_get_obj_from_plan_dict_ReturnsObj():
    # ESTABLISH
    field_str = "_is_expanded"
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str)
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "task"
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "problem_bool"
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "_kids"
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: {}}, field_str) == {}
    assert get_obj_from_plan_dict({}, field_str) == {}


def test_get_obj_from_plan_dict_ReturnsCorrect_HealerLink():
    # ESTABLISH
    # WHEN / THEN
    healerlink_key = "healerlink"
    assert get_obj_from_plan_dict({}, healerlink_key) == healerlink_shop()

    # WHEN
    sue_str = "Sue"
    zia_str = "Zia"
    healerlink_dict = {"healerlink_healer_names": [sue_str, zia_str]}
    planunit_dict = {healerlink_key: healerlink_dict}

    # THEN
    static_healerlink = healerlink_shop()
    static_healerlink.set_healer_name(x_healer_name=sue_str)
    static_healerlink.set_healer_name(x_healer_name=zia_str)
    assert get_obj_from_plan_dict(planunit_dict, healerlink_key) is not None
    assert get_obj_from_plan_dict(planunit_dict, healerlink_key) == static_healerlink


def test_PlanUnit_get_dict_ReturnsCorrectCompleteDict():
    # ESTABLISH
    wk_str = "wkdays"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "Wednesday"
    wed_rope = create_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)

    wed_case = caseunit_shop(r_state=wed_rope)
    wed_case._status = True
    usa_case = caseunit_shop(r_state=usa_rope)
    usa_case._status = False

    x1_reasonunits = {
        wk_rope: reasonunit_shop(wk_rope, cases={wed_case.r_state: wed_case}),
        nation_rope: reasonunit_shop(nation_rope, {usa_case.r_state: usa_case}),
    }
    wed_cases = {wed_case.r_state: wed_case}
    usa_cases = {usa_case.r_state: usa_case}
    x1_reasonheirs = {
        wk_rope: reasonheir_shop(wk_rope, wed_cases, _status=True),
        nation_rope: reasonheir_shop(nation_rope, usa_cases, _status=False),
    }
    biker_awardee_title = "bikers"
    biker_give_force = 3.0
    biker_take_force = 7.0
    biker_awardlink = awardlink_shop(
        biker_awardee_title, biker_give_force, biker_take_force
    )
    flyer_awardee_title = "flyers"
    flyer_give_force = 6.0
    flyer_take_force = 9.0
    flyer_awardlink = awardlink_shop(
        awardee_title=flyer_awardee_title,
        give_force=flyer_give_force,
        take_force=flyer_take_force,
    )
    biker_and_flyer_awardlinks = {
        biker_awardlink.awardee_title: biker_awardlink,
        flyer_awardlink.awardee_title: flyer_awardlink,
    }
    biker_get_dict = {
        "awardee_title": biker_awardlink.awardee_title,
        "give_force": biker_awardlink.give_force,
        "take_force": biker_awardlink.take_force,
    }
    flyer_get_dict = {
        "awardee_title": flyer_awardlink.awardee_title,
        "give_force": flyer_awardlink.give_force,
        "take_force": flyer_awardlink.take_force,
    }
    x1_awardlinks = {
        biker_awardee_title: biker_get_dict,
        flyer_awardee_title: flyer_get_dict,
    }
    sue_str = "Sue"
    yao_str = "Yao"
    sue_laborunit = laborunit_shop({sue_str: -1, yao_str: -1})
    yao_healerlink = healerlink_shop({yao_str})
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    x_problem_bool = True
    casa_plan = planunit_shop(
        parent_rope=casa_rope,
        _kids=None,
        awardlinks=biker_and_flyer_awardlinks,
        mass=30,
        plan_label=casa_str,
        _level=1,
        reasonunits=x1_reasonunits,
        _reasonheirs=x1_reasonheirs,
        laborunit=sue_laborunit,
        healerlink=yao_healerlink,
        _active=True,
        task=True,
        problem_bool=x_problem_bool,
    )
    x_factunit = factunit_shop(
        f_context=wk_rope, f_state=wk_rope, f_lower=5, f_upper=59
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
    casa_plan._uid = 17
    casa_plan.add_kid(planunit_shop("paper"))

    # WHEN
    casa_dict = casa_plan.get_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict["_kids"]) == 1
    assert casa_dict["_kids"] == casa_plan.get_kids_dict()
    assert casa_dict["reasonunits"] == casa_plan.get_reasonunits_dict()
    assert casa_dict["awardlinks"] == casa_plan.get_awardlinks_dict()
    assert casa_dict["awardlinks"] == x1_awardlinks
    assert casa_dict["laborunit"] == sue_laborunit.get_dict()
    assert casa_dict["healerlink"] == yao_healerlink.get_dict()
    assert casa_dict["mass"] == casa_plan.mass
    assert casa_dict["plan_label"] == casa_plan.plan_label
    assert casa_dict["_uid"] == casa_plan._uid
    assert casa_dict["begin"] == casa_plan.begin
    assert casa_dict["close"] == casa_plan.close
    assert casa_dict["numor"] == casa_plan.numor
    assert casa_dict["denom"] == casa_plan.denom
    assert casa_dict["morph"] == casa_plan.morph
    assert casa_dict["gogo_want"] == casa_plan.gogo_want
    assert casa_dict["stop_want"] == casa_plan.stop_want
    assert casa_dict["task"] == casa_plan.task
    assert casa_dict["problem_bool"] == casa_plan.problem_bool
    assert casa_dict["problem_bool"] == x_problem_bool
    assert casa_plan._is_expanded
    assert casa_dict.get("_is_expanded") is None
    assert len(casa_dict["factunits"]) == len(casa_plan.get_factunits_dict())


def test_PlanUnit_get_dict_ReturnsCorrectDictWithoutEmptyAttributes():
    # ESTABLISH
    casa_plan = planunit_shop()

    # WHEN
    casa_dict = casa_plan.get_dict()

    # THEN
    assert casa_dict is not None
    assert casa_dict == {"mass": 1}


def test_PlanUnit_get_dict_ReturnsDictWith_attrs_CorrectlySetTrue():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_plan._is_expanded = False
    casa_plan.task = True
    ignore_str = "ignore"

    a_str = "a"
    a_rope = create_rope(root_label(), a_str)
    casa_plan.set_factunit(factunit_shop(a_rope, a_rope))

    yao_str = "Yao"
    casa_plan.set_awardlink(awardlink_shop(yao_str))

    x_laborunit = casa_plan.laborunit
    x_laborunit.set_laborlink(labor_title=yao_str)

    clean_str = "clean"
    casa_plan.add_kid(planunit_shop(clean_str))

    assert not casa_plan._is_expanded
    assert casa_plan.task
    assert casa_plan.factunits is not None
    assert casa_plan.awardlinks is not None
    assert casa_plan.laborunit is not None
    assert casa_plan._kids != {}

    # WHEN
    casa_dict = casa_plan.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is False
    assert casa_dict.get("task")
    assert casa_dict.get("factunits") is not None
    assert casa_dict.get("awardlinks") is not None
    assert casa_dict.get("laborunit") is not None
    assert casa_dict.get("_kids") is not None


def test_PlanUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # ESTABLISH
    casa_plan = planunit_shop()
    assert casa_plan._is_expanded
    assert casa_plan.task is False
    assert casa_plan.factunits == {}
    assert casa_plan.awardlinks == {}
    assert casa_plan.laborunit == laborunit_shop()
    assert casa_plan.healerlink == healerlink_shop()
    assert casa_plan._kids == {}

    # WHEN
    casa_dict = casa_plan.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is None
    assert casa_dict.get("task") is None
    assert casa_dict.get("factunits") is None
    assert casa_dict.get("awardlinks") is None
    assert casa_dict.get("laborunit") is None
    assert casa_dict.get("healerlink") is None
    assert casa_dict.get("_kids") is None
