from src.a01_term_logic.rope import create_rope
from src.a03_group_logic.group import awardunit_shop
from src.a03_group_logic.labor import laborunit_shop
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
from src.a05_plan_logic.test._util.a05_str import (
    _active_hx_str,
    _active_str,
    _all_partner_cred_str,
    _all_partner_debt_str,
    _awardheirs_str,
    _awardlines_str,
    _chore_str,
    _descendant_task_count_str,
    _factheirs_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerlink_ratio_str,
    _is_expanded_str,
    _kids_str,
    _level_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    addin_str,
    awardunits_str,
    begin_str,
    belief_label_str,
    close_str,
    denom_str,
    fund_iota_str,
    fund_share_str,
    gogo_want_str,
    healerlink_str,
    knot_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    star_str,
    stop_want_str,
    task_str,
)


def test_get_obj_from_plan_dict_ReturnsObj():
    # ESTABLISH
    field_str = _is_expanded_str()
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str)
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = task_str()
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = problem_bool_str()
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: True}, field_str)
    assert get_obj_from_plan_dict({}, field_str) is False
    assert get_obj_from_plan_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = _kids_str()
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: {}}, field_str) == {}
    assert get_obj_from_plan_dict({}, field_str) == {}


def test_get_obj_from_plan_dict_Returns_HealerLink():
    # ESTABLISH
    # WHEN / THEN
    healerlink_key = healerlink_str()
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


def test_PlanUnit_to_dict_ReturnsCompleteDict():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "Wed"
    wed_rope = create_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case._status = True
    usa_case = caseunit_shop(reason_state=usa_rope)
    usa_case._status = False

    x1_reasonunits = {
        wk_rope: reasonunit_shop(wk_rope, cases={wed_case.reason_state: wed_case}),
        nation_rope: reasonunit_shop(nation_rope, {usa_case.reason_state: usa_case}),
    }
    wed_cases = {wed_case.reason_state: wed_case}
    usa_cases = {usa_case.reason_state: usa_case}
    x1_reasonheirs = {
        wk_rope: reasonheir_shop(wk_rope, wed_cases, _status=True),
        nation_rope: reasonheir_shop(nation_rope, usa_cases, _status=False),
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
        "awardee_title": biker_awardunit.awardee_title,
        "give_force": biker_awardunit.give_force,
        "take_force": biker_awardunit.take_force,
    }
    flyer_get_dict = {
        "awardee_title": flyer_awardunit.awardee_title,
        "give_force": flyer_awardunit.give_force,
        "take_force": flyer_awardunit.take_force,
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
    yao_healerlink = healerlink_shop({yao_str})
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    x_problem_bool = True
    casa_plan = planunit_shop(
        parent_rope=casa_rope,
        _kids=None,
        awardunits=biker_and_flyer_awardunits,
        star=30,
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
    casa_plan._uid = 17
    casa_plan.add_kid(planunit_shop("paper"))

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict["_kids"]) == 1
    assert casa_dict["_kids"] == casa_plan.get_kids_dict()
    assert casa_dict["reasonunits"] == casa_plan.get_reasonunits_dict()
    assert casa_dict[awardunits_str()] == casa_plan.get_awardunits_dict()
    assert casa_dict[awardunits_str()] == x1_awardunits
    assert casa_dict["laborunit"] == sue_laborunit.to_dict()
    assert casa_dict["healerlink"] == yao_healerlink.to_dict()
    assert casa_dict["star"] == casa_plan.star
    assert casa_dict["plan_label"] == casa_plan.plan_label
    assert casa_dict["_uid"] == casa_plan._uid
    assert casa_dict[begin_str()] == casa_plan.begin
    assert casa_dict[close_str()] == casa_plan.close
    assert casa_dict[numor_str()] == casa_plan.numor
    assert casa_dict[denom_str()] == casa_plan.denom
    assert casa_dict[morph_str()] == casa_plan.morph
    assert casa_dict[gogo_want_str()] == casa_plan.gogo_want
    assert casa_dict[stop_want_str()] == casa_plan.stop_want
    assert casa_dict[task_str()] == casa_plan.task
    assert casa_dict[problem_bool_str()] == casa_plan.problem_bool
    assert casa_dict[problem_bool_str()] == x_problem_bool
    assert casa_plan._is_expanded
    assert casa_dict.get("_is_expanded") is None
    assert len(casa_dict["factunits"]) == len(casa_plan.get_factunits_dict())


def test_PlanUnit_to_dict_ReturnsDictWithoutEmptyAttributes():
    # ESTABLISH
    casa_plan = planunit_shop()

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict is not None
    assert casa_dict == {"star": 1}


def test_PlanUnit_to_dict_ReturnsDictWith_attrs_SetToTrue():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_plan._is_expanded = False
    casa_plan.task = True
    ignore_str = "ignore"

    a_str = "a"
    a_rope = create_rope(root_label(), a_str)
    casa_plan.set_factunit(factunit_shop(a_rope, a_rope))

    yao_str = "Yao"
    casa_plan.set_awardunit(awardunit_shop(yao_str))

    x_laborunit = casa_plan.laborunit
    x_laborunit.add_party(party_title=yao_str)

    clean_str = "clean"
    casa_plan.add_kid(planunit_shop(clean_str))

    assert not casa_plan._is_expanded
    assert casa_plan.task
    assert casa_plan.factunits is not None
    assert casa_plan.awardunits is not None
    assert casa_plan.laborunit is not None
    assert casa_plan._kids != {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is False
    assert casa_dict.get("task")
    assert casa_dict.get("factunits") is not None
    assert casa_dict.get(awardunits_str()) is not None
    assert casa_dict.get("laborunit") is not None
    assert casa_dict.get("_kids") is not None


def test_PlanUnit_to_dict_ReturnsDictWithAttrsEmpty():
    # ESTABLISH
    casa_plan = planunit_shop()
    assert casa_plan._is_expanded
    assert casa_plan.task is False
    assert casa_plan.factunits == {}
    assert casa_plan.awardunits == {}
    assert casa_plan.laborunit == laborunit_shop()
    assert casa_plan.healerlink == healerlink_shop()
    assert casa_plan._kids == {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is None
    assert casa_dict.get("task") is None
    assert casa_dict.get("factunits") is None
    assert casa_dict.get(awardunits_str()) is None
    assert casa_dict.get("laborunit") is None
    assert casa_dict.get("healerlink") is None
    assert casa_dict.get("_kids") is None
