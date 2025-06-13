def get_vow_kpi001_acct_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE vow_kpi001_acct_nets AS
SELECT 
  vow_label
, owner_name
, NULL vow_fund_amount
, NULL vow_fund_rank
, NULL as vow_tasks
FROM vow_acct_nets
"""
