def get_belief_kpi001_partner_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE belief_kpi001_partner_nets AS
SELECT
  belief_partner_nets.belief_label
, belief_partner_nets.believer_name
, believer_net_amount AS funds
, RANK() OVER (ORDER BY believer_net_amount DESC) AS fund_rank
, IFNULL(SUM(believer_planunit_job.task), 0) AS tasks_count
FROM belief_partner_nets
LEFT JOIN believer_planunit_job ON
  believer_planunit_job.belief_label = belief_partner_nets.belief_label
  AND believer_planunit_job.believer_name = belief_partner_nets.believer_name
GROUP BY belief_partner_nets.belief_label, belief_partner_nets.believer_name
;
"""


def get_belief_kpi002_believer_tasks_sqlstr() -> str:
    return """
CREATE TABLE belief_kpi002_believer_tasks AS
SELECT
  believer_planunit_job.belief_label
, believer_planunit_job.believer_name
, believer_planunit_job.plan_rope
, believer_planunit_job.task
, believer_planunit_job._active
, believer_planunit_job._chore
FROM believer_planunit_job
;
"""
