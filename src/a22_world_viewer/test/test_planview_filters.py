from src.a05_plan_logic.test._util.a05_str import _kids_str, plan_label_str
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
    sue_beliverunit = believerunit_shop(sue_str, amy23_str)
    x1_rope = sue_beliverunit.make_l1_rope(x1_str)
    x2_rope = sue_beliverunit.make_l1_rope(x2_str)
    x3_rope = sue_beliverunit.make_l1_rope(x3_str)
    x4_rope = sue_beliverunit.make_rope(x3_rope, x4_str)
    sue_beliverunit.add_plan(x1_rope)
    sue_beliverunit.add_plan(x2_rope)
    sue_beliverunit.add_plan(x3_rope)
    sue_beliverunit.add_plan(x4_rope)

    # WHEN
    plan_label_dict = plan_label(sue_beliverunit.get_dict())

    # THEN
    expected_output = {amy23_str: {x1_str: {}, x2_str: {}, x3_str: {x4_str: {}}}}
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


# def test_plan_tasks_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output

# def test_plan_fund_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output

# def test_plan_awardees_ReturnsObj_Scenario0():
#     # ESTABLISH
#     input_data = {"key": "value"}
#     expected_output = {}  # Define expected output based on plan_label logic

#     # WHEN
#     result = plan_label(input_data)

#     # THEN
#     assert isinstance(result, dict)
#     assert result == expected_output

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
