def get_vow_kpi001_acct_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE vow_kpi001_acct_nets AS
SELECT 
  vow_label
, owner_name
, owner_net_amount AS funds
, NULL AS fund_rank
, NULL AS tasks_count
FROM vow_acct_nets
"""
