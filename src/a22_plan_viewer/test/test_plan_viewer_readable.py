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
    _healerunit_ratio_str,
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
    cases_str,
    close_str,
    coin_label_str,
    denom_str,
    factunits_str,
    fund_iota_str,
    fund_share_str,
    gogo_want_str,
    healerunit_str,
    knot_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    reason_state_str,
    reasonunits_str,
    star_str,
    stop_want_str,
    task_str,
)
from src.a06_belief_logic.test._util.a06_str import parent_rope_str, planroot_str
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a22_plan_viewer.plan_viewer import add_small_dot, get_plan_view_dict
from src.a22_plan_viewer.test._util.example22_beliefs import (
    best_run_str,
    best_soccer_str,
    best_sport_str,
    best_swim_str,
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
    play_run_str,
    play_soccer_str,
    play_str,
    play_swim_str,
)


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
        coin_label_str(),
        parent_rope_str(),
        _kids_str(),
        "root",
        star_str(),
        _uid_str(),
        awardunits_str(),
        reasonunits_str(),
        "laborunit",
        factunits_str(),
        healerunit_str(),
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
        _healerunit_ratio_str(),
        _level_str(),
        _range_evaluated_str(),
        "_reasonheirs",
        _chore_str(),
        "_laborheir",
        _gogo_calc_str(),
        _stop_calc_str(),
        "fund_share",
    }
    assert casa_dict.get("healerunit") == {"_healer_names": []}


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
    sue_beliefunit = get_sue_beliefunit()

    # WHEN
    root_plan_view_dict = get_plan_view_dict(sue_beliefunit.planroot)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    # expected_laborunit_dict = {
    #     "_partys": {sue_str: {"party_title": sue_str, "solo": False}}
    # }
    expected_parent_rope = add_small_dot("Root Plan parent_rope is empty str")
    assert root_plan_view_dict.get(parent_rope_str()) == expected_parent_rope


def test_get_plan_view_dict_ReturnsObj_Scenario3_PlanUnit_base_attrs():
    # ESTABLISH
    sue_beliefunit = get_sue_beliefunit()
    casa_rope = sue_beliefunit.make_l1_rope("casa")
    casa_plan = sue_beliefunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    assert casa_dict.get(fund_share_str()) > 0
    expected_parent_rope = add_small_dot(casa_plan.parent_rope)
    assert casa_dict.get(parent_rope_str()) == expected_parent_rope
    expected_all_partner_cred = f"all_partner_cred = {casa_plan._all_partner_cred}"
    expected_all_partner_debt = f"all_partner_debt = {casa_plan._all_partner_debt}"
    expected_all_partner_cred = add_small_dot(expected_all_partner_cred)
    expected_all_partner_debt = add_small_dot(expected_all_partner_debt)
    assert casa_dict.get(_all_partner_cred_str()) == expected_all_partner_cred
    assert casa_dict.get(_all_partner_debt_str()) == expected_all_partner_debt
    assert casa_dict.get(_fund_ratio_str()) == "38%"


def test_get_plan_view_dict_ReturnsObj_Scenario4_PlanUnit_AwardUnits():
    # ESTABLISH
    sue_beliefunit = get_sue_beliefunit()
    casa_rope = sue_beliefunit.make_l1_rope("casa")
    casa_plan = sue_beliefunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # awardunits
    awardunits_dict = casa_dict.get(awardunits_str())
    assert len(awardunits_dict) == 2
    # print(f"{len(awardunits_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardunit_dict = awardunits_dict.get(sue_str)
    bob_awardunit_dict = awardunits_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = add_small_dot(f"{sue_str}: Take 0.8, Give 1")
    expected_bob_readable = add_small_dot(f"{bob_str}: Take 0.9, Give 0.7")
    # print(f"{sue_awardunit_dict.get(readable_str)=}")
    # print(f"{bob_awardunit_dict.get(readable_str)=}")
    assert sue_awardunit_dict.get(readable_str) == expected_sue_readable
    assert bob_awardunit_dict.get(readable_str) == expected_bob_readable

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
    sue_belief = get_sue_belief_with_facts_and_reasons()

    # WHEN
    root_dict = get_plan_view_dict(sue_belief.planroot)

    # THEN
    # sports ropes
    sports_rope = sue_belief.make_l1_rope("sports")
    best_sport_str = "best sport"
    best_rope = sue_belief.make_rope(sports_rope, best_sport_str)

    # casa ropes
    casa_rope = sue_belief.make_l1_rope("casa")
    tidi_rope = sue_belief.make_rope(casa_rope, "tidiness")

    # factunits
    root_factunits_dict = root_dict.get(factunits_str())
    assert len(root_factunits_dict) == 2
    # print(f"{len(factunits_dict)=}")
    tidi_factunit_dict = root_factunits_dict.get(tidi_rope)
    best_factunit_dict = root_factunits_dict.get(best_rope)
    # print(f"{tidi_factunit_dict=}")
    # print(f"{best_factunit_dict=}")
    readable_str = "readable"
    tidi_factunit = sue_belief.get_fact(tidi_rope)
    best_factunit = sue_belief.get_fact(best_rope)
    tidi_factunit_readable = get_fact_state_readable_str(
        tidi_factunit, None, sue_belief
    )
    best_factunit_readable = get_fact_state_readable_str(
        best_factunit, None, sue_belief
    )
    expected_tidi_factunit_str = add_small_dot(tidi_factunit_readable)
    expected_best_factunit_str = add_small_dot(best_factunit_readable)
    # print(f"{expected_tidi_factunit_str=}")
    # print(f"{expected_best_factunit_str=}")
    assert tidi_factunit_dict.get(readable_str) == expected_tidi_factunit_str
    assert best_factunit_dict.get(readable_str) == expected_best_factunit_str

    # factheirs
    casa_factheirs_dict = root_dict.get("_factheirs")
    assert len(casa_factheirs_dict) == 2
    print(f"{len(casa_factheirs_dict)=}")
    casa_tidi_factheir_dict = casa_factheirs_dict.get(tidi_rope)
    casa_best_factheir_dict = casa_factheirs_dict.get(best_rope)
    print(f"{casa_tidi_factheir_dict=}")
    print(f"{casa_best_factheir_dict=}")
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    tidi_factheir = casa_plan._factheirs.get(tidi_rope)
    best_factheir = casa_plan._factheirs.get(best_rope)
    casa_tidi_factheir_readable = get_fact_state_readable_str(
        tidi_factheir, None, sue_belief
    )
    casa_best_factheir_readable = get_fact_state_readable_str(
        best_factheir, None, sue_belief
    )
    expected_casa_tidi_factheir_str = add_small_dot(casa_tidi_factheir_readable)
    expected_casa_best_factheir_str = add_small_dot(casa_best_factheir_readable)
    assert casa_tidi_factheir_dict.get(readable_str) == expected_casa_tidi_factheir_str
    assert casa_best_factheir_dict.get(readable_str) == expected_casa_best_factheir_str


# def test_get_plan_view_dict_ReturnsObj_Scenario6_PlanUnit_ReasonUnit():
#     # ESTABLISH
#     sue_belief = get_sue_belief_with_facts_and_reasons()
#     casa_rope = sue_belief.make_l1_rope("casa")
#     clean_rope = sue_belief.make_rope(casa_rope, "clean")
#     mop_rope = sue_belief.make_rope(clean_rope, "mop")
#     sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
#     tidi_rope = sue_belief.make_rope(casa_rope, "tidiness")
#     dirty_rope = sue_belief.make_rope(casa_rope, "dirty")
#     tidy_rope = sue_belief.make_rope(casa_rope, "tidy")
#     sports_rope = sue_belief.make_l1_rope("sports")
#     best_rope = sue_belief.make_rope(sports_rope, best_sport_str())
#     best_soccer_rope = sue_belief.make_rope(best_rope, best_soccer_str())
#     best_swim_rope = sue_belief.make_rope(best_rope, best_swim_str())
#     best_run_rope = sue_belief.make_rope(best_rope, best_run_str())
#     play_rope = sue_belief.make_rope(sports_rope, play_str())
#     play_soccer_rope = sue_belief.make_rope(play_rope, play_soccer_str())
#     play_swim_rope = sue_belief.make_rope(play_rope, play_swim_str())
#     play_run_rope = sue_belief.make_rope(play_rope, play_run_str())
#     play_soccer_plan = sue_belief.get_plan_obj(play_soccer_rope)

#     # WHEN
#     play_soccer_dict = get_plan_view_dict(play_soccer_plan)

#     # THEN
#     # reasonunits
#     play_soccer_reasonunits_dict = play_soccer_dict.get(reasonunits_str())
#     assert len(play_soccer_reasonunits_dict) == 2
#     print(f"{len(play_soccer_reasonunits_dict)=}")
#     best_reasonunit_dict = play_soccer_reasonunits_dict.get(best_rope)
#     tidi_reasonunit_dict = play_soccer_reasonunits_dict.get(tidi_rope)
#     best_cases_dict = best_reasonunit_dict.get(cases_str())
#     tidi_cases_dict = tidi_reasonunit_dict.get(cases_str())
#     best_soccer_case_dict = best_cases_dict.get(best_soccer_rope)
#     clean_case_dict = tidi_cases_dict.get(clean_rope)
#     print(f"{best_soccer_case_dict.get(reason_state_str())=}")
#     print(f"{clean_case_dict.get(reason_state_str())=}")
#     assert best_soccer_case_dict.get(reason_state_str()) == best_soccer_rope
#     assert clean_case_dict.get(reason_state_str()) == clean_rope

#     best_reasonunit = play_soccer_plan.get_reasonunit(best_rope)
#     tidi_reasonunit = play_soccer_plan.get_reasonunit(tidi_rope)
#     print(f"{best_reasonunit.cases.keys()=}")
#     print(f"{tidi_reasonunit.cases.keys()=}")
#     best_soccer_caseunit = best_reasonunit.get_case(best_soccer_rope)
#     best_run_caseunit = best_reasonunit.get_case(best_run_rope)
#     tidy_caseunit = tidi_reasonunit.get_case(clean_rope)
#     expected_soccer_case_readable = get_reason_case_readable_str(
#         best_rope, best_soccer_caseunit, None, sue_belief
#     )
#     expected_run_case_readable = get_reason_case_readable_str(
#         best_rope, best_run_caseunit, None, sue_belief
#     )
#     expected_tidy_case_readable = get_reason_case_readable_str(
#         tidi_rope, tidy_caseunit, None, sue_belief
#     )
#     expected_soccer_case_readable = add_small_dot(expected_soccer_case_readable)
#     expected_run_case_readable = add_small_dot(expected_run_case_readable)
#     expected_tidy_case_readable = add_small_dot(expected_tidy_case_readable)
#     # print(f"{expected_tidi_reasonunit_str=}")
#     # print(f"{expected_best_reasonunit_str=}")
#     readable_str = "readable"
#     assert best_soccer_case_dict.get(readable_str) == expected_soccer_case_readable
#     assert best_soccer_case_dict.get(readable_str) == expected_run_case_readable
#     assert clean_case_dict.get(readable_str) == expected_tidy_case_readable

#     # # reasonheirs
#     # casa_reasonheirs_dict = root_dict.get("_reasonheirs")
#     # assert len(casa_reasonheirs_dict) == 2
#     # print(f"{len(casa_reasonheirs_dict)=}")
#     # casa_tidi_reasonheir_dict = casa_reasonheirs_dict.get(tidi_rope)
#     # casa_best_reasonheir_dict = casa_reasonheirs_dict.get(best_rope)
#     # print(f"{casa_tidi_reasonheir_dict=}")
#     # print(f"{casa_best_reasonheir_dict=}")
#     # casa_plan = sue_belief.get_plan_obj(casa_rope)
#     # tidi_reasonheir = casa_plan._reasonheirs.get(tidi_rope)
#     # best_reasonheir = casa_plan._reasonheirs.get(best_rope)
#     # casa_tidi_reasonheir_readable = get_reason_state_readable_str(
#     #     tidi_reasonheir, None, sue_belief
#     # )
#     # casa_best_reasonheir_readable = get_reason_state_readable_str(
#     #     best_reasonheir, None, sue_belief
#     # )
#     # expected_casa_tidi_reasonheir_str = add_small_dot(casa_tidi_reasonheir_readable)
#     # expected_casa_best_reasonheir_str = add_small_dot(casa_best_reasonheir_readable)
#     # assert (
#     #     casa_tidi_reasonheir_dict.get(readable_str) == expected_casa_tidi_reasonheir_str
#     # )
#     # assert (
#     #     casa_best_reasonheir_dict.get(readable_str) == expected_casa_best_reasonheir_str
#     # )
#     assert 1 == 2


def test_get_plan_view_dict_ReturnsObj_Scenario7_gogo_stop():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_gogo_want = 13
    casa_stop_want = 17
    casa_gogo_calc = 53
    casa_stop_calc = 57
    casa_plan.gogo_want = casa_gogo_want
    casa_plan.stop_want = casa_stop_want
    casa_plan._gogo_calc = casa_gogo_calc
    casa_plan._stop_calc = casa_stop_calc
    casa_plan._fund_ratio = 0

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    gogo_want_readable = casa_dict.get(gogo_want_str())
    stop_want_readable = casa_dict.get(stop_want_str())
    gogo_calc_readable = casa_dict.get(_gogo_calc_str())
    stop_calc_readable = casa_dict.get(_stop_calc_str())
    expected_gogo_want_readable = add_small_dot(f"gogo_want: {casa_plan.gogo_want}")
    expected_stop_want_readable = add_small_dot(f"stop_want: {casa_plan.stop_want}")
    expected_gogo_calc_readable = add_small_dot(f"gogo_calc: {casa_plan._gogo_calc}")
    expected_stop_calc_readable = add_small_dot(f"stop_calc: {casa_plan._stop_calc}")
    assert gogo_want_readable == expected_gogo_want_readable
    assert stop_want_readable == expected_stop_want_readable
    assert gogo_calc_readable == expected_gogo_calc_readable
    assert stop_calc_readable == expected_stop_calc_readable


def test_get_plan_view_dict_ReturnsObj_Scenario8_numeric_range_attrs():
    # ESTABLISH
    casa_plan = planunit_shop()
    casa_addin = 11
    casa_begin = 17
    casa_close = 23
    casa_denom = 29
    casa_morph = 37
    casa_numor = 43
    casa_plan.addin = casa_addin
    casa_plan.begin = casa_begin
    casa_plan.close = casa_close
    casa_plan.denom = casa_denom
    casa_plan.morph = casa_morph
    casa_plan.numor = casa_numor
    casa_plan._fund_ratio = 0

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    casa_addin_readable = casa_dict.get(addin_str())
    casa_begin_readable = casa_dict.get(begin_str())
    casa_close_readable = casa_dict.get(close_str())
    casa_denom_readable = casa_dict.get(denom_str())
    casa_morph_readable = casa_dict.get(morph_str())
    casa_numor_readable = casa_dict.get(numor_str())
    expected_casa_addin_readable = add_small_dot(f"addin: {casa_plan.addin}")
    expected_casa_begin_readable = add_small_dot(f"begin: {casa_plan.begin}")
    expected_casa_close_readable = add_small_dot(f"close: {casa_plan.close}")
    expected_casa_denom_readable = add_small_dot(f"denom: {casa_plan.denom}")
    expected_casa_morph_readable = add_small_dot(f"morph: {casa_plan.morph}")
    expected_casa_numor_readable = add_small_dot(f"numor: {casa_plan.numor}")
    assert casa_addin_readable == expected_casa_addin_readable
    assert casa_begin_readable == expected_casa_begin_readable
    assert casa_close_readable == expected_casa_close_readable
    assert casa_denom_readable == expected_casa_denom_readable
    assert casa_morph_readable == expected_casa_morph_readable
    assert casa_numor_readable == expected_casa_numor_readable


def test_get_plan_view_dict_ReturnsObj_Scenario9_active_hx():
    # ESTABLISH
    hatter_belief = get_beliefunit_irrational_example()
    hatter_belief.set_max_tree_traverse(8)
    hatter_belief.cash_out()
    egg_str = "egg first"
    egg_rope = hatter_belief.make_l1_rope(egg_str)
    chicken_str = "chicken first"
    chicken_rope = hatter_belief.make_l1_rope(chicken_str)
    chicken_plan = hatter_belief.get_plan_obj(chicken_rope)

    # WHEN
    chicken_dict = get_plan_view_dict(chicken_plan)

    # THEN
    print(f"{chicken_plan._active_hx=}")
    # sports ropes
    chicken_active_hx_str = chicken_dict.get(_active_hx_str())
    expected_chicken_active_hx_str = f"active_hx: {chicken_plan._active_hx}"
    expected_chicken_active_hx_str = add_small_dot(expected_chicken_active_hx_str)
    assert expected_chicken_active_hx_str == chicken_active_hx_str
