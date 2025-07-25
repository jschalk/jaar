from src.a03_group_logic.group import awardlink_shop
from src.a05_plan_logic.test._util.a05_str import (
    _kids_str,
    fund_share_str,
    plan_label_str,
    task_str,
)
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import believerunit_v002
from src.a22_world_viewer.planview_filters import (
    plan_awardees,
    plan_facts,
    plan_fund,
    plan_label,
    plan_reasons,
    plan_tasks,
    plan_time,
)


def test_plan_label_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    amy23_str = "Amy23"
    x1_str = "x1"
    x2_str = "x2"
    x3_str = "x3"
    x4_str = "x4"
    sue_believerunit = believerunit_shop(sue_str, amy23_str)
    x1_rope = sue_believerunit.make_l1_rope(x1_str)
    x2_rope = sue_believerunit.make_l1_rope(x2_str)
    x3_rope = sue_believerunit.make_l1_rope(x3_str)
    x4_rope = sue_believerunit.make_rope(x3_rope, x4_str)
    sue_believerunit.add_plan(x1_rope)
    sue_believerunit.add_plan(x2_rope)
    sue_believerunit.add_plan(x3_rope)
    sue_believerunit.add_plan(x4_rope)

    # WHEN
    plan_label_dict = plan_label(sue_believerunit.get_dict())

    # THEN
    expected_output = {amy23_str: {x1_str: "", x2_str: "", x3_str: {x4_str: ""}}}
    print(f"{plan_label_dict=}")
    print(f"{expected_output=}")
    assert isinstance(plan_label_dict, dict)
    assert plan_label_dict == expected_output


def test_plan_label_ReturnsObj_Scenario1_LargeBelieverJSON():
    # ESTABLISH
    x_believerunit = believerunit_v002()
    believer_dict = x_believerunit.get_dict()

    # WHEN
    plan_label_dict = plan_label(believer_dict)

    # THEN
    planroot_dict = plan_label_dict.get(x_believerunit.belief_label)
    print(f"{planroot_dict.keys()=}")
    plan_label_dict.get(x_believerunit.belief_label)
    assert len(planroot_dict) == 17


def test_plan_tasks_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    amy23_str = "Amy23"
    x1_str = "x1"
    x2_str = "x2"
    x3_str = "x3"
    x4_str = "x4"
    x5_str = "x5"
    sue_believerunit = believerunit_shop(sue_str, amy23_str)
    x1_rope = sue_believerunit.make_l1_rope(x1_str)
    x2_rope = sue_believerunit.make_l1_rope(x2_str)
    x3_rope = sue_believerunit.make_l1_rope(x3_str)
    x4_rope = sue_believerunit.make_rope(x3_rope, x4_str)
    x5_rope = sue_believerunit.make_rope(x4_rope, x5_str)
    sue_believerunit.add_plan(x1_rope, task=True)
    sue_believerunit.add_plan(x2_rope)
    sue_believerunit.add_plan(x3_rope)
    sue_believerunit.add_plan(x4_rope, task=True)
    sue_believerunit.add_plan(x5_rope, task=True)

    # WHEN
    plan_display_dict = plan_tasks(sue_believerunit.get_dict())

    # THEN
    expected_output = {
        amy23_str: {x3_str: {"x4 (TASK)": {"x5 (TASK)": {}}}, "x1 (TASK)": {}}
    }
    print(f"{plan_display_dict=}")
    print(f"  {expected_output=}")
    assert plan_display_dict == expected_output


def test_plan_fund_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy26_str = "Amy2026"
    x1_str = "x1"
    x2_str = "x2"
    sue_believerunit = believerunit_shop(sue_str, amy26_str, fund_pool=20)
    x1_rope = sue_believerunit.make_l1_rope(x1_str)
    x2_rope = sue_believerunit.make_l1_rope(x2_str)
    sue_believerunit.add_plan(x1_rope, mass=4)
    sue_believerunit.add_plan(x2_rope, mass=1)

    # WHEN
    plan_display_dict = plan_fund(sue_believerunit.get_dict())

    # THEN
    expected_output = {"Amy2026 (fund 20)": {"x2 (fund 4)": {}, "x1 (fund 16)": {}}}
    print(f"{plan_display_dict=}")
    print(f"  {expected_output=}")
    assert plan_display_dict == expected_output


def test_plan_fund_ReturnsObj_Scenario1_CheckCommasInNumber():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    amy26_str = "Amy2026"
    x1_str = "x1"
    x2_str = "x2"
    sue_believerunit = believerunit_shop(sue_str, amy26_str, fund_pool=33333)
    x1_rope = sue_believerunit.make_l1_rope(x1_str)
    x2_rope = sue_believerunit.make_l1_rope(x2_str)
    sue_believerunit.add_plan(x1_rope, mass=4)
    sue_believerunit.add_plan(x2_rope, mass=1)

    # WHEN
    plan_display_dict = plan_fund(sue_believerunit.get_dict())

    # THEN
    expected_output = {
        "Amy2026 (fund 33,333)": {"x2 (fund 6,667)": {}, "x1 (fund 26,666)": {}}
    }
    print(f"{plan_display_dict=}")
    print(f"  {expected_output=}")
    assert plan_display_dict == expected_output


def test_plan_awardees_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    amy26_str = "Amy2026"
    x1_str = "x1"
    x2_str = "x2"
    sue_believerunit = believerunit_shop(sue_str, amy26_str, fund_pool=33333)
    sue_believerunit.add_partnerunit(bob_str, 1, 7)
    sue_believerunit.add_partnerunit(yao_str, 5, 1)
    x1_rope = sue_believerunit.make_l1_rope(x1_str)
    x2_rope = sue_believerunit.make_l1_rope(x2_str)
    sue_believerunit.add_plan(x1_rope, mass=4)
    sue_believerunit.add_plan(x2_rope, mass=1)
    bob_awardlink = awardlink_shop(bob_str, 1, 3)
    yao_awardlink = awardlink_shop(yao_str, 4, 1)
    sue_believerunit.edit_plan_attr(x1_rope, awardlink=bob_awardlink)
    sue_believerunit.edit_plan_attr(x1_rope, awardlink=yao_awardlink)
    assert sue_believerunit.get_plan_obj(x1_rope).awardlinks != {}

    # WHEN
    plan_display_dict = plan_awardees(sue_believerunit.get_dict())

    # THEN
    expected_output = {
        "Amy2026 (fund 33,333)": {
            "x2 (fund 6,667)": {},
            "x1 (fund 26,666)": {
                "Bob": "Give 5,333, Take 20,000",
                "Yao": "Give 21,333, Take 6,666",
            },
        }
    }
    print(f"{plan_display_dict=}")
    print(f"  {expected_output=}")
    assert plan_display_dict == expected_output


# def test_plan_reasons_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output

# def test_plan_facts_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output

# def test_plan_time_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output
