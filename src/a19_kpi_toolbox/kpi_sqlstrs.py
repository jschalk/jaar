def get_belief_kpi001_acct_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE belief_kpi001_acct_nets AS
SELECT
  belief_acct_nets.belief_label
, belief_acct_nets.owner_name
, owner_net_amount AS funds
, RANK() OVER (ORDER BY owner_net_amount DESC) AS fund_rank
, IFNULL(SUM(owner_conceptunit_job.task), 0) AS tasks_count
FROM belief_acct_nets
LEFT JOIN owner_conceptunit_job ON
  owner_conceptunit_job.belief_label = belief_acct_nets.belief_label
  AND owner_conceptunit_job.owner_name = belief_acct_nets.owner_name
GROUP BY belief_acct_nets.belief_label, belief_acct_nets.owner_name
;
"""
