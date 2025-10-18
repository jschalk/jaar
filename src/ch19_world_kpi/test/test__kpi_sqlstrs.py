from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename
from src.ch19_world_kpi.kpi_sqlstrs import (
    get_create_kpi001_sqlstr,
    get_create_kpi002_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = kw.belief_planunit
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {kw.moment_kpi001_voice_nets} AS
SELECT
  {kw.moment_voice_nets}.{kw.moment_label}
, {kw.moment_voice_nets}.{kw.belief_name}
, {kw.belief_net_amount} AS funds
, RANK() OVER (ORDER BY {kw.belief_net_amount} DESC) AS fund_rank
, IFNULL(SUM({blrplan_job}.{kw.pledge}), 0) AS pledges_count
FROM {kw.moment_voice_nets}
LEFT JOIN {blrplan_job} ON
  {blrplan_job}.{kw.moment_label} = {kw.moment_voice_nets}.{kw.moment_label}
  AND {blrplan_job}.{kw.belief_name} = {kw.moment_voice_nets}.{kw.belief_name}
GROUP BY {kw.moment_voice_nets}.{kw.moment_label}, {kw.moment_voice_nets}.{kw.belief_name}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = kw.belief_planunit
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {kw.moment_kpi002_belief_pledges} AS
SELECT
  {kw.moment_label}
, {kw.belief_name}
, {kw.plan_rope}
, {kw.pledge}
, {kw.plan_active}
, {kw.task}
FROM {blrplan_job}
WHERE {kw.pledge} == 1 AND {kw.plan_active} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
