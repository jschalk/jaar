def get_coin_kpi001_partner_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE coin_kpi001_partner_nets AS
SELECT
  coin_partner_nets.coin_label
, coin_partner_nets.belief_name
, belief_net_amount AS funds
, RANK() OVER (ORDER BY belief_net_amount DESC) AS fund_rank
, IFNULL(SUM(belief_planunit_job.task), 0) AS tasks_count
FROM coin_partner_nets
LEFT JOIN belief_planunit_job ON
  belief_planunit_job.coin_label = coin_partner_nets.coin_label
  AND belief_planunit_job.belief_name = coin_partner_nets.belief_name
GROUP BY coin_partner_nets.coin_label, coin_partner_nets.belief_name
;
"""


def get_coin_kpi002_belief_tasks_sqlstr() -> str:
    return """
CREATE TABLE coin_kpi002_belief_tasks AS
SELECT
  belief_planunit_job.coin_label
, belief_planunit_job.belief_name
, belief_planunit_job.plan_rope
, belief_planunit_job.task
, belief_planunit_job._active
, belief_planunit_job._chore
FROM belief_planunit_job
;
"""
