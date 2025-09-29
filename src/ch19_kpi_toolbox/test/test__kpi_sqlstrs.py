from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch19_kpi_toolbox._ref.ch19_keywords import (
    Ch04Keywords as wx,
    Ch07Keywords as wx,
    Ch18Keywords as wx,
    Ch19Keywords as wx,
    active_str,
    moment_label_str,
    plan_rope_str,
    pledge_str,
    task_str,
)
from src.ch19_kpi_toolbox.kpi_sqlstrs import (
    get_create_kpi001_sqlstr,
    get_create_kpi002_sqlstr,
)


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = wx.belief_planunit
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {wx.moment_kpi001_voice_nets} AS
SELECT
  {wx.moment_voice_nets}.{moment_label_str()}
, {wx.moment_voice_nets}.{wx.belief_name}
, {wx.belief_net_amount} AS funds
, RANK() OVER (ORDER BY {wx.belief_net_amount} DESC) AS fund_rank
, IFNULL(SUM({blrplan_job}.{pledge_str()}), 0) AS pledges_count
FROM {wx.moment_voice_nets}
LEFT JOIN {blrplan_job} ON
  {blrplan_job}.{moment_label_str()} = {wx.moment_voice_nets}.{moment_label_str()}
  AND {blrplan_job}.{wx.belief_name} = {wx.moment_voice_nets}.{wx.belief_name}
GROUP BY {wx.moment_voice_nets}.{moment_label_str()}, {wx.moment_voice_nets}.{wx.belief_name}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = wx.belief_planunit
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {wx.moment_kpi002_belief_pledges} AS
SELECT
  {moment_label_str()}
, {wx.belief_name}
, {plan_rope_str()}
, {pledge_str()}
, {active_str()}
, {task_str()}
FROM {blrplan_job}
WHERE {pledge_str()} == 1 AND {active_str()} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
