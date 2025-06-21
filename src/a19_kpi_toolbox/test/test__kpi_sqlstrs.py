from src.a02_finance_logic.test._util.a02_str import bank_label_str, owner_name_str
from src.a06_plan_logic.test._util.a06_str import plan_conceptunit_str, task_str
from src.a18_etl_toolbox.test._util.a18_str import (
    bank_acct_nets_str,
    owner_net_amount_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a19_kpi_toolbox.kpi_sqlstrs import get_bank_kpi001_acct_nets_sqlstr
from src.a19_kpi_toolbox.test._util.a19_str import bank_kpi001_acct_nets_str


def test_get_bank_kpi001_acct_nets_sqlstr_ReturnsObj():
    # ESTABLISH
    plnconc_str = plan_conceptunit_str()
    plnconc_job = create_prime_tablename(plnconc_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_bank_kpi001_acct_nets_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {bank_kpi001_acct_nets_str()} AS
SELECT
  {bank_acct_nets_str()}.{bank_label_str()}
, {bank_acct_nets_str()}.{owner_name_str()}
, {owner_net_amount_str()} AS funds
, RANK() OVER (ORDER BY {owner_net_amount_str()} DESC) AS fund_rank
, IFNULL(SUM({plnconc_job}.{task_str()}), 0) AS tasks_count
FROM {bank_acct_nets_str()}
LEFT JOIN {plnconc_job} ON
  {plnconc_job}.{bank_label_str()} = {bank_acct_nets_str()}.{bank_label_str()}
  AND {plnconc_job}.{owner_name_str()} = {bank_acct_nets_str()}.{owner_name_str()}
GROUP BY {bank_acct_nets_str()}.{bank_label_str()}, {bank_acct_nets_str()}.{owner_name_str()}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr
