from src.a06_belief_logic.test._util.a06_str import (
    _active_str,
    _chore_str,
    belief_name_str,
    belief_planunit_str,
    coin_label_str,
    plan_rope_str,
    task_str,
)
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_net_amount_str,
    coin_partner_nets_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a19_kpi_toolbox.kpi_sqlstrs import (
    get_coin_kpi001_partner_nets_sqlstr,
    get_coin_kpi002_belief_tasks_sqlstr,
)
from src.a19_kpi_toolbox.test._util.a19_str import (
    coin_kpi001_partner_nets_str,
    coin_kpi002_belief_tasks_str,
)


def test_get_coin_kpi001_partner_nets_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = belief_planunit_str()
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_coin_kpi001_partner_nets_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {coin_kpi001_partner_nets_str()} AS
SELECT
  {coin_partner_nets_str()}.{coin_label_str()}
, {coin_partner_nets_str()}.{belief_name_str()}
, {belief_net_amount_str()} AS funds
, RANK() OVER (ORDER BY {belief_net_amount_str()} DESC) AS fund_rank
, IFNULL(SUM({blrplan_job}.{task_str()}), 0) AS tasks_count
FROM {coin_partner_nets_str()}
LEFT JOIN {blrplan_job} ON
  {blrplan_job}.{coin_label_str()} = {coin_partner_nets_str()}.{coin_label_str()}
  AND {blrplan_job}.{belief_name_str()} = {coin_partner_nets_str()}.{belief_name_str()}
GROUP BY {coin_partner_nets_str()}.{coin_label_str()}, {coin_partner_nets_str()}.{belief_name_str()}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_coin_kpi002_belief_tasks_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = belief_planunit_str()
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_coin_kpi002_belief_tasks_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {coin_kpi002_belief_tasks_str()} AS
SELECT
  {blrplan_job}.{coin_label_str()}
, {blrplan_job}.{belief_name_str()}
, {blrplan_job}.{plan_rope_str()}
, {blrplan_job}.{task_str()}
, {blrplan_job}.{_active_str()}
, {blrplan_job}.{_chore_str()}
FROM {blrplan_job}
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
