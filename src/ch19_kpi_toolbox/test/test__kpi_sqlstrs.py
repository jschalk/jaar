from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch19_kpi_toolbox._ref.ch19_keywords import (
    active_str,
    belief_name_str,
    belief_net_amount_str,
    belief_planunit_str,
    chore_str,
    moment_kpi001_voice_nets_str,
    moment_kpi002_belief_pledges_str,
    moment_label_str,
    moment_voice_nets_str,
    plan_rope_str,
    pledge_str,
)
from src.ch19_kpi_toolbox.kpi_sqlstrs import (
    get_create_kpi001_sqlstr,
    get_create_kpi002_sqlstr,
)


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = belief_planunit_str()
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {moment_kpi001_voice_nets_str()} AS
SELECT
  {moment_voice_nets_str()}.{moment_label_str()}
, {moment_voice_nets_str()}.{belief_name_str()}
, {belief_net_amount_str()} AS funds
, RANK() OVER (ORDER BY {belief_net_amount_str()} DESC) AS fund_rank
, IFNULL(SUM({blrplan_job}.{pledge_str()}), 0) AS pledges_count
FROM {moment_voice_nets_str()}
LEFT JOIN {blrplan_job} ON
  {blrplan_job}.{moment_label_str()} = {moment_voice_nets_str()}.{moment_label_str()}
  AND {blrplan_job}.{belief_name_str()} = {moment_voice_nets_str()}.{belief_name_str()}
GROUP BY {moment_voice_nets_str()}.{moment_label_str()}, {moment_voice_nets_str()}.{belief_name_str()}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    blrplan_str = belief_planunit_str()
    blrplan_job = create_prime_tablename(blrplan_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {moment_kpi002_belief_pledges_str()} AS
SELECT
  {moment_label_str()}
, {belief_name_str()}
, {plan_rope_str()}
, {pledge_str()}
, {active_str()}
, {chore_str()}
FROM {blrplan_job}
WHERE {pledge_str()} == 1 AND {active_str()} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
