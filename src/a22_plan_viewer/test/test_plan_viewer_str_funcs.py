from src.a05_plan_logic.plan import planunit_shop
from src.a05_plan_logic.test._util.a05_str import (
    _active_hx_str,
    _active_str,
    _all_partner_cred_str,
    _all_partner_debt_str,
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
from src.a06_believer_logic.believer_tool import believer_plan_factunit_get_obj
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a22_plan_viewer.plan_viewer import add_small_dot, get_plan_view_dict
from src.a22_plan_viewer.test._util.example22_believers import get_sue_casa_believerunit


def test_get_plan_view_dict_ReturnsObj_Scenario0_EmptyPlan():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_plan._fund_ratio = 1
    assert casa_plan._kids == {}
    print(f"{type(casa_plan)=}")

    # WHEN
    # casa_dict = dataclasses_asdict(casa_plan)
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    assert set(casa_dict.keys()) == {
        plan_label_str(),
        belief_label_str(),
        "parent_rope",
        _kids_str(),
        "root",
        star_str(),
        _uid_str(),
        "awardlinks",
        "reasonunits",
        "laborunit",
        "factunits",
        healerlink_str(),
        begin_str(),
        close_str(),
        addin_str(),
        denom_str(),
        numor_str(),
        morph_str(),
        gogo_want_str(),
        stop_want_str(),
        task_str(),
        problem_bool_str(),
        knot_str(),
        _is_expanded_str(),
        _active_str(),
        _active_hx_str(),
        _all_partner_cred_str(),
        _all_partner_debt_str(),
        "_awardheirs",
        "_awardlines",
        _descendant_task_count_str(),
        "_factheirs",
        _fund_ratio_str(),
        fund_iota_str(),
        _fund_onset_str(),
        _fund_cease_str(),
        _healerlink_ratio_str(),
        _level_str(),
        _range_evaluated_str(),
        "_reasonheirs",
        _chore_str(),
        "_laborheir",
        _gogo_calc_str(),
        _stop_calc_str(),
        "fund_share",
    }
    assert casa_dict.get("healerlink") == {"_healer_names": []}


def test_get_plan_view_dict_ReturnsObj_Scenario1_laborunit():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_plan._fund_ratio = 1
    sue_str = "Sue"
    casa_plan.laborunit.add_party(sue_str)
    assert casa_plan._kids == {}
    print(f"{type(casa_plan)=}")

    # WHEN
    # casa_dict = dataclasses_asdict(casa_plan)
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    casa_laborunit_dict = casa_dict.get("laborunit")
    expected_laborunit_dict = {
        "_partys": {sue_str: {"party_title": sue_str, "solo": False}}
    }
    assert casa_laborunit_dict == expected_laborunit_dict


def test_get_plan_view_dict_ReturnsObj_Scenario2_RootPlanUnit_attrs():
    # ESTABLISH
    sue_believerunit = get_sue_casa_believerunit()

    # WHEN
    root_plan_view_dict = get_plan_view_dict(sue_believerunit.planroot)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    # expected_laborunit_dict = {
    #     "_partys": {sue_str: {"party_title": sue_str, "solo": False}}
    # }
    expected_parent_rope = add_small_dot("Root Plan parent_rope is empty str")
    assert root_plan_view_dict.get("parent_rope") == expected_parent_rope


def test_get_plan_view_dict_ReturnsObj_Scenario3_PlanUnit_base_attrs():
    # ESTABLISH
    sue_believerunit = get_sue_casa_believerunit()
    casa_rope = sue_believerunit.make_l1_rope("casa")
    casa_plan = sue_believerunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    assert casa_dict.get(fund_share_str()) > 0
    expected_parent_rope = add_small_dot(casa_plan.parent_rope)
    assert casa_dict.get("parent_rope") == expected_parent_rope
    expected_all_partner_cred = f"all_partner_cred = {casa_plan._all_partner_cred}"
    expected_all_partner_debt = f"all_partner_debt = {casa_plan._all_partner_debt}"
    expected_all_partner_cred = add_small_dot(expected_all_partner_cred)
    expected_all_partner_debt = add_small_dot(expected_all_partner_debt)
    assert casa_dict.get(_all_partner_cred_str()) == expected_all_partner_cred
    assert casa_dict.get(_all_partner_debt_str()) == expected_all_partner_debt
    assert casa_dict.get(_fund_ratio_str()) == "38%"


def test_get_plan_view_dict_ReturnsObj_Scenario4_PlanUnit_AwardLinks():
    # ESTABLISH
    sue_believerunit = get_sue_casa_believerunit()
    casa_rope = sue_believerunit.make_l1_rope("casa")
    casa_plan = sue_believerunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # awardlinks
    awardlinks_dict = casa_dict.get("awardlinks")
    assert len(awardlinks_dict) == 2
    # print(f"{len(awardlinks_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardlink_dict = awardlinks_dict.get(sue_str)
    bob_awardlink_dict = awardlinks_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = add_small_dot(f"{sue_str}: Take 0.8, Give 1")
    expected_bob_readable = add_small_dot(f"{bob_str}: Take 0.9, Give 0.7")
    # print(f"{sue_awardlink_dict.get(readable_str)=}")
    # print(f"{bob_awardlink_dict.get(readable_str)=}")
    assert sue_awardlink_dict.get(readable_str) == expected_sue_readable
    assert bob_awardlink_dict.get(readable_str) == expected_bob_readable

    # _awardheirs
    awardheirs_dict = casa_dict.get("_awardheirs")
    assert len(awardheirs_dict) == 4
    # print(f"{len(awardheirs_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardheir_dict = awardheirs_dict.get(sue_str)
    bob_awardheir_dict = awardheirs_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = f"{sue_str}: Take 0.8 (150000000), Give 1 (150000000)"
    expected_bob_readable = f"{bob_str}: Take 0.9 (168750000), Give 0.7 (105000000)"
    # print(f"{sue_awardheir_dict.get(readable_str)=}")
    # print(f"{bob_awardheir_dict.get(readable_str)=}")
    assert sue_awardheir_dict.get(readable_str) == add_small_dot(expected_sue_readable)
    assert bob_awardheir_dict.get(readable_str) == add_small_dot(expected_bob_readable)

    # _awardlines
    awardlines_dict = casa_dict.get("_awardlines")
    assert len(awardlines_dict) == 4
    print(f"{len(awardlines_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardline_dict = awardlines_dict.get(sue_str)
    bob_awardline_dict = awardlines_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = f"{sue_str}: take_fund (150000000), give_fund (149999999)"
    expected_bob_readable = f"{bob_str}: take_fund (168750000), give_fund (105000000)"
    print(f"{sue_awardline_dict.get(readable_str)=}")
    print(f"{bob_awardline_dict.get(readable_str)=}")
    assert sue_awardline_dict.get(readable_str) == add_small_dot(expected_sue_readable)
    assert bob_awardline_dict.get(readable_str) == add_small_dot(expected_bob_readable)


def test_get_plan_view_dict_ReturnsObj_Scenario5_PlanUnit_FactUnit():
    # ESTABLISH
    # TODO create FactUnits
    # TODO create FactHeirs
    sue_believer = get_sue_casa_believerunit()

    # WHEN
    casa_dict = get_plan_view_dict(sue_believer.planroot)

    # THEN
    # sports ropes
    sports_rope = sue_believer.make_l1_rope("sports")
    best_sport_str = "best sport"
    best_rope = sue_believer.make_rope(sports_rope, best_sport_str)
    soccer_str = "soccer"
    swim_str = "swim"
    run_str = "run"
    best_soccer_rope = sue_believer.make_rope(best_rope, soccer_str)
    best_swim_rope = sue_believer.make_rope(best_rope, swim_str)
    best_run_rope = sue_believer.make_rope(best_rope, run_str)

    # casa ropes
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_rope(casa_rope, "clean")
    mop_rope = sue_believer.make_rope(clean_rope, "mop")
    sweep_rope = sue_believer.make_rope(clean_rope, "sweep")
    tidi_rope = sue_believer.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_believer.make_rope(casa_rope, "dirty")
    tidy_rope = sue_believer.make_rope(casa_rope, "tidy")

    # factunits
    factunits_dict = casa_dict.get("factunits")
    assert len(factunits_dict) == 2
    # print(f"{len(factunits_dict)=}")
    tidi_factunit_dict = factunits_dict.get(tidi_rope)
    best_factunit_dict = factunits_dict.get(best_rope)
    # print(f"{tidi_factunit_dict=}")
    # print(f"{best_factunit_dict=}")
    readable_str = "readable"
    tidi_factunit = sue_believer.get_fact(tidi_rope)
    best_factunit = sue_believer.get_fact(best_rope)
    tidi_factunit_readable = get_fact_state_readable_str(
        tidi_factunit, None, sue_believer
    )
    best_factunit_readable = get_fact_state_readable_str(
        best_factunit, None, sue_believer
    )
    expected_tidi_factunit_str = add_small_dot(tidi_factunit_readable)
    expected_best_factunit_str = add_small_dot(best_factunit_readable)
    # print(f"{expected_tidi_factunit_str=}")
    # print(f"{expected_best_factunit_str=}")
    assert tidi_factunit_dict.get(readable_str) == expected_tidi_factunit_str
    assert best_factunit_dict.get(readable_str) == expected_best_factunit_str

    # factheirs
    casa_factheirs_dict = casa_dict.get("_factheirs")
    assert len(casa_factheirs_dict) == 2
    print(f"{len(casa_factheirs_dict)=}")
    casa_tidi_factheir_dict = casa_factheirs_dict.get(tidi_rope)
    casa_best_factheir_dict = casa_factheirs_dict.get(best_rope)
    print(f"{casa_tidi_factheir_dict=}")
    print(f"{casa_best_factheir_dict=}")
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    tidi_factheir = casa_plan._factheirs.get(tidi_rope)
    best_factheir = casa_plan._factheirs.get(best_rope)
    casa_tidi_factheir_readable = get_fact_state_readable_str(
        tidi_factheir, None, sue_believer
    )
    casa_best_factheir_readable = get_fact_state_readable_str(
        best_factheir, None, sue_believer
    )
    expected_casa_tidi_factheir_str = add_small_dot(casa_tidi_factheir_readable)
    expected_casa_best_factheir_str = add_small_dot(casa_best_factheir_readable)
    assert casa_tidi_factheir_dict.get(readable_str) == expected_casa_tidi_factheir_str
    assert casa_best_factheir_dict.get(readable_str) == expected_casa_best_factheir_str
