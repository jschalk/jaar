from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
)

# create function add_plan_reason_daily given BeliefUnit, plan_rope,beginning time, duration

# create exception if add_plan_reason_daily plan_rope,beginning time + duration is greater then 1440 (must stay within day)

# create function del_plan_reason_daily given BeliefUnit, plan_rope,beginning time, duration

# create test with multiple add_plan_reason_daily added to single plan

# create test with multiple daily reasons added and del_plan_reason_daily only deletes the correct one
