def get_belief_kpi001_person_nets_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 account nets table.
    """
    return """
CREATE TABLE belief_kpi001_person_nets AS
SELECT
  belief_person_nets.belief_label
, belief_person_nets.believer_name
, believer_net_amount AS funds
, RANK() OVER (ORDER BY believer_net_amount DESC) AS fund_rank
, IFNULL(SUM(believer_planunit_job.task), 0) AS tasks_count
FROM belief_person_nets
LEFT JOIN believer_planunit_job ON
  believer_planunit_job.belief_label = belief_person_nets.belief_label
  AND believer_planunit_job.believer_name = belief_person_nets.believer_name
GROUP BY belief_person_nets.belief_label, belief_person_nets.believer_name
;
"""
