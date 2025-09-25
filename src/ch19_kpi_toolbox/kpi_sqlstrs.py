def get_create_kpi001_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 voice nets table.
    """
    return """
CREATE TABLE moment_kpi001_voice_nets AS
SELECT
  moment_voice_nets.moment_label
, moment_voice_nets.belief_name
, belief_net_amount AS funds
, RANK() OVER (ORDER BY belief_net_amount DESC) AS fund_rank
, IFNULL(SUM(belief_planunit_job.task), 0) AS tasks_count
FROM moment_voice_nets
LEFT JOIN belief_planunit_job ON
  belief_planunit_job.moment_label = moment_voice_nets.moment_label
  AND belief_planunit_job.belief_name = moment_voice_nets.belief_name
GROUP BY moment_voice_nets.moment_label, moment_voice_nets.belief_name
;
"""


def get_create_kpi002_sqlstr() -> str:
    return """
CREATE TABLE moment_kpi002_belief_tasks AS
SELECT
  moment_label
, belief_name
, plan_rope
, task
, active
, chore
FROM belief_planunit_job
WHERE task == 1 AND active == 1
;
"""
