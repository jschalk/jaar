def get_vow_kpi001_acct_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE vow_kpi001_acct_nets AS
SELECT
  vow_acct_nets.vow_label
, vow_acct_nets.owner_name
, owner_net_amount AS funds
, RANK() OVER (ORDER BY owner_net_amount DESC) AS fund_rank
, IFNULL(SUM(plan_conceptunit_job.task), 0) AS tasks_count
FROM vow_acct_nets
LEFT JOIN plan_conceptunit_job ON
  plan_conceptunit_job.vow_label = vow_acct_nets.vow_label
  AND plan_conceptunit_job.owner_name = vow_acct_nets.owner_name
GROUP BY vow_acct_nets.vow_label, vow_acct_nets.owner_name
;
"""
