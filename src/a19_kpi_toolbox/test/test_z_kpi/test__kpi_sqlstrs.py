from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a18_etl_toolbox._test_util.a18_str import (
    owner_net_amount_str,
    vow_acct_nets_str,
)
from src.a19_kpi_toolbox._test_util.a19_str import vow_kpi001_acct_nets_str
from src.a19_kpi_toolbox.kpi_sqlstrs import get_vow_kpi001_acct_nets_sqlstr


def test_get_vow_kpi001_acct_nets_sqlstr_ReturnsObj():
    # ESTABLISH

    # WHEN
    kpi001_sqlstr = get_vow_kpi001_acct_nets_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {vow_kpi001_acct_nets_str()} AS
SELECT 
  {vow_label_str()}
, {owner_name_str()}
, {owner_net_amount_str()} AS funds
, NULL AS fund_rank
, NULL AS tasks_count
FROM {vow_acct_nets_str()}
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr
