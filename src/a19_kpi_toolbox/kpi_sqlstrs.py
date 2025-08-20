def get_moment_kpi001_partner_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE moment_kpi001_partner_nets AS
SELECT
  moment_partner_nets.moment_label
, moment_partner_nets.belief_name
, belief_net_amount AS funds
, RANK() OVER (ORDER BY belief_net_amount DESC) AS fund_rank
, IFNULL(SUM(belief_planunit_job.task), 0) AS tasks_count
FROM moment_partner_nets
LEFT JOIN belief_planunit_job ON
  belief_planunit_job.moment_label = moment_partner_nets.moment_label
  AND belief_planunit_job.belief_name = moment_partner_nets.belief_name
GROUP BY moment_partner_nets.moment_label, moment_partner_nets.belief_name
;
"""


def get_moment_kpi002_belief_tasks_sqlstr() -> str:
    return """
CREATE TABLE moment_kpi002_belief_tasks AS
SELECT
  belief_planunit_job.moment_label
, belief_planunit_job.belief_name
, belief_planunit_job.plan_rope
, belief_planunit_job.task
, belief_planunit_job._active
, belief_planunit_job._chore
FROM belief_planunit_job
;
"""
