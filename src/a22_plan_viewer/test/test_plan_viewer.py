from src.a03_group_logic.labor import laborunit_shop
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a22_plan_viewer.plan_viewer import get_plan_view_dict


def test_get_plan_view_dict_ReturnsObj_Scenario0_EmptyPlan():
    # ESTABLISH
    casa_plan = planunit_shop()
    assert casa_plan._kids == {}
    print(f"{type(casa_plan)=}")

    # WHEN
    # casa_dict = dataclasses_asdict(casa_plan)
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    assert set(casa_dict.keys()) == {
        "plan_label",
        "belief_label",
        "parent_rope",
        "_kids",
        "root",
        "star",
        "_uid",
        "awardlinks",
        "reasonunits",
        "laborunit",
        "factunits",
        "healerlink",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
        "gogo_want",
        "stop_want",
        "task",
        "problem_bool",
        "knot",
        "_is_expanded",
        "_active",
        "_active_hx",
        "_all_partner_cred",
        "_all_partner_debt",
        "_awardheirs",
        "_awardlines",
        "_descendant_task_count",
        "_factheirs",
        "_fund_ratio",
        "fund_iota",
        "_fund_onset",
        "_fund_cease",
        "_healerlink_ratio",
        "_level",
        "_range_evaluated",
        "_reasonheirs",
        "_chore",
        "_laborheir",
        "_gogo_calc",
        "_stop_calc",
    }
    assert casa_dict.get("healerlink") == {"_healer_names": []}


def test_get_plan_view_dict_ReturnsObj_Scenario1_laborunit():
    # ESTABLISH
    casa_plan = planunit_shop()
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
