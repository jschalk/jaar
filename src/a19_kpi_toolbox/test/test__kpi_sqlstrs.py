from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    believer_planunit_str,
    task_str,
)
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_person_nets_str,
    believer_net_amount_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a19_kpi_toolbox.kpi_sqlstrs import (
    get_belief_kpi001_person_nets_sqlstr,
    get_belief_kpi002_person_tasks_sqlstr,
)
from src.a19_kpi_toolbox.test._util.a19_str import (
    belief_kpi001_person_nets_str,
    belief_kpi002_person_tasks_str,
)


def test_get_belief_kpi001_person_nets_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = believer_planunit_str()
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_belief_kpi001_person_nets_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {belief_kpi001_person_nets_str()} AS
SELECT
  {belief_person_nets_str()}.{belief_label_str()}
, {belief_person_nets_str()}.{believer_name_str()}
, {believer_net_amount_str()} AS funds
, RANK() OVER (ORDER BY {believer_net_amount_str()} DESC) AS fund_rank
, IFNULL(SUM({blrplan_job}.{task_str()}), 0) AS tasks_count
FROM {belief_person_nets_str()}
LEFT JOIN {blrplan_job} ON
  {blrplan_job}.{belief_label_str()} = {belief_person_nets_str()}.{belief_label_str()}
  AND {blrplan_job}.{believer_name_str()} = {belief_person_nets_str()}.{believer_name_str()}
GROUP BY {belief_person_nets_str()}.{belief_label_str()}, {belief_person_nets_str()}.{believer_name_str()}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


# def test_get_belief_kpi002_person_tasks_sqlstr_ReturnsObj():
#     # ESTABLISH
#     blrplan_str = believer_planunit_str()
#     blrplan_job = create_prime_tablename(blrplan_str, "job", None)

#     # WHEN
#     kpi002_sqlstr = get_belief_kpi002_person_tasks_sqlstr()

#     # THEN
#     expected_kpi002_sqlstr = f"""
# CREATE TABLE {belief_kpi002_person_tasks_str()} AS
# SELECT
#   {belief_person_nets_str()}.{belief_label_str()}
# , {belief_person_nets_str()}.{believer_name_str()}
# , {belief_person_nets_str()}.{believer_name_str()}
# , {believer_net_amount_str()} AS funds
# , RANK() OVER (ORDER BY {believer_net_amount_str()} DESC) AS fund_rank
# , IFNULL(SUM({blrplan_job}.{task_str()}), 0) AS tasks_count
# FROM {belief_person_nets_str()}
# LEFT JOIN {blrplan_job} ON
#   {blrplan_job}.{belief_label_str()} = {belief_person_nets_str()}.{belief_label_str()}
#   AND {blrplan_job}.{believer_name_str()} = {belief_person_nets_str()}.{believer_name_str()}
# GROUP BY {belief_person_nets_str()}.{belief_label_str()}, {belief_person_nets_str()}.{believer_name_str()}
# ;
# """
#     assert kpi002_sqlstr == expected_kpi002_sqlstr
