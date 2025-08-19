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
    print(f"{len(awardlinks_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardlink_dict = awardlinks_dict.get(sue_str)
    bob_awardlink_dict = awardlinks_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = add_small_dot(f"{sue_str}: Take 0.8, Give 1")
    expected_bob_readable = add_small_dot(f"{bob_str}: Take 0.9, Give 0.7")
    print(f"{sue_awardlink_dict.get(readable_str)=}")
    print(f"{bob_awardlink_dict.get(readable_str)=}")
    assert sue_awardlink_dict.get(readable_str) == expected_sue_readable
    assert bob_awardlink_dict.get(readable_str) == expected_bob_readable

    # _awardheirs
    awardheirs_dict = casa_dict.get("_awardheirs")
    assert len(awardheirs_dict) == 4
    print(f"{len(awardheirs_dict)=}")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_awardheir_dict = awardheirs_dict.get(sue_str)
    bob_awardheir_dict = awardheirs_dict.get(bob_str)
    readable_str = "readable"
    expected_sue_readable = f"{sue_str}: Take 0.8 (150000000), Give 1 (150000000)"
    expected_bob_readable = f"{bob_str}: Take 0.9 (168750000), Give 0.7 (105000000)"
    print(f"{sue_awardheir_dict.get(readable_str)=}")
    print(f"{bob_awardheir_dict.get(readable_str)=}")
    assert sue_awardheir_dict.get(readable_str) == add_small_dot(expected_sue_readable)
    assert bob_awardheir_dict.get(readable_str) == add_small_dot(expected_bob_readable)


# def test_get_plan_view_dict_ReturnsObj_Scenario5_PlanUnit_FactUnit():
#     # ESTABLISH
#     # TODO create FactUnits
#     # TODO create FactHeirs
#     assert 1 == 2
#     sue_believerunit = get_sue_casa_believerunit()
#     casa_rope = sue_believerunit.make_l1_rope("casa")
#     sue_believerunit.add_fact(casa_rope)
#     casa_plan = sue_believerunit.get_plan_obj(casa_rope)

#     # WHEN
#     casa_dict = get_plan_view_dict(casa_plan)

#     # THEN
#     awardlinks_dict = casa_dict.get("awardlinks")
#     assert len(awardlinks_dict) == 2
#     print(f"{len(awardlinks_dict)=}")
#     sue_str = "Sue"
#     bob_str = "Bob"
#     sue_awardlink_dict = awardlinks_dict.get(sue_str)
#     bob_awardlink_dict = awardlinks_dict.get(bob_str)
#     readable_str = "readable"
#     expected_sue_readable = add_small_dot(f"{sue_str}: Take 0.8, Give 1")
#     expected_bob_readable = add_small_dot(f"{bob_str}: Take 0.9, Give 0.7")
#     print(f"{sue_awardlink_dict.get(readable_str)=}")
#     print(f"{bob_awardlink_dict.get(readable_str)=}")
#     assert sue_awardlink_dict.get(readable_str) == expected_sue_readable
#     assert bob_awardlink_dict.get(readable_str) == expected_bob_readable
