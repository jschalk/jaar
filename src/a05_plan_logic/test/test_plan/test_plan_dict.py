from src.a01_term_logic.rope import create_rope
from src.a03_group_logic.group import awardunit_shop
from src.a03_group_logic.labor import laborunit_shop
from src.a04_reason_logic.reason import (
    caseunit_shop,
    factunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_plan_logic.healer import healerunit_shop
from src.a05_plan_logic.plan import (
    get_default_moment_label as root_label,
    get_obj_from_plan_dict,
    planunit_shop,
)
from src.a05_plan_logic.test._util.a05_str import (
    active_hx_str,
    active_str,
    addin_str,
    all_voice_cred_str,
    all_voice_debt_str,
    awardheirs_str,
    awardlines_str,
    awardunits_str,
    begin_str,
    chore_str,
    close_str,
    denom_str,
    descendant_task_count_str,
    factheirs_str,
    factunits_str,
    fund_cease_str,
    fund_iota_str,
    fund_onset_str,
    fund_ratio_str,
    fund_share_str,
    gogo_calc_str,
    gogo_want_str,
    healerunit_ratio_str,
    healerunit_str,
    is_expanded_str,
    kids_str,
    knot_str,
    laborunit_str,
    level_str,
    moment_label_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    range_evaluated_str,
    reasonheirs_str,
    reasonunits_str,
    star_str,
    stop_calc_str,
    stop_want_str,
    task_str,
    uid_str,
)


def test_get_obj_from_plan_dict_ReturnsObj():
    # ESTABLISH
    field_str = is_expanded_str()
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
    field_str = kids_str()
    # WHEN / THEN
    assert get_obj_from_plan_dict({field_str: {}}, field_str) == {}
    assert get_obj_from_plan_dict({}, field_str) == {}


def test_get_obj_from_plan_dict_Returns_HealerUnit():
    # ESTABLISH
    # WHEN / THEN
    healerunit_key = healerunit_str()
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
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wed_str = "Wed"
    wed_rope = create_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case.status = True
    usa_case = caseunit_shop(reason_state=usa_rope)
    usa_case.status = False

    x1_reasonunits = {
        wk_rope: reasonunit_shop(wk_rope, cases={wed_case.reason_state: wed_case}),
        nation_rope: reasonunit_shop(nation_rope, {usa_case.reason_state: usa_case}),
    }
    wed_cases = {wed_case.reason_state: wed_case}
    usa_cases = {usa_case.reason_state: usa_case}
    x1_reasonheirs = {
        wk_rope: reasonheir_shop(wk_rope, wed_cases, status=True),
        nation_rope: reasonheir_shop(nation_rope, usa_cases, status=False),
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
    yao_healerunit = healerunit_shop({yao_str})
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    x_problem_bool = True
    casa_plan = planunit_shop(
        parent_rope=casa_rope,
        kids=None,
        awardunits=biker_and_flyer_awardunits,
        star=30,
        plan_label=casa_str,
        level=1,
        reasonunits=x1_reasonunits,
        reasonheirs=x1_reasonheirs,
        laborunit=sue_laborunit,
        healerunit=yao_healerunit,
        active=True,
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
    casa_plan.uid = 17
    casa_plan.add_kid(planunit_shop("paper"))

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict["kids"]) == 1
    assert casa_dict["kids"] == casa_plan.get_kids_dict()
    assert casa_dict[reasonunits_str()] == casa_plan.get_reasonunits_dict()
    assert casa_dict[awardunits_str()] == casa_plan.get_awardunits_dict()
    assert casa_dict[awardunits_str()] == x1_awardunits
    assert casa_dict[laborunit_str()] == sue_laborunit.to_dict()
    assert casa_dict["healerunit"] == yao_healerunit.to_dict()
    assert casa_dict[star_str()] == casa_plan.star
    assert casa_dict[plan_label_str()] == casa_plan.plan_label
    assert casa_dict["uid"] == casa_plan.uid
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
    assert casa_plan.is_expanded
    assert casa_dict.get("is_expanded") is None
    assert len(casa_dict[factunits_str()]) == len(casa_plan.get_factunits_dict())


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
    casa_plan.is_expanded = False
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

    assert not casa_plan.is_expanded
    assert casa_plan.task
    assert casa_plan.factunits is not None
    assert casa_plan.awardunits is not None
    assert casa_plan.laborunit is not None
    assert casa_plan.kids != {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get("is_expanded") is False
    assert casa_dict.get(task_str())
    assert casa_dict.get(factunits_str()) is not None
    assert casa_dict.get(awardunits_str()) is not None
    assert casa_dict.get(laborunit_str()) is not None
    assert casa_dict.get("kids") is not None


def test_PlanUnit_to_dict_ReturnsDictWithAttrsEmpty():
    # ESTABLISH
    casa_plan = planunit_shop()
    assert casa_plan.is_expanded
    assert casa_plan.task is False
    assert casa_plan.factunits == {}
    assert casa_plan.awardunits == {}
    assert casa_plan.laborunit == laborunit_shop()
    assert casa_plan.healerunit == healerunit_shop()
    assert casa_plan.kids == {}

    # WHEN
    casa_dict = casa_plan.to_dict()

    # THEN
    assert casa_dict.get("is_expanded") is None
    assert casa_dict.get(task_str()) is None
    assert casa_dict.get(factunits_str()) is None
    assert casa_dict.get(awardunits_str()) is None
    assert casa_dict.get(laborunit_str()) is None
    assert casa_dict.get("healerunit") is None
    assert casa_dict.get("kids") is None
