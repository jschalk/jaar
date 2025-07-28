from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.db_toolbox import sqlite_obj_str
from src.a01_term_logic.term import BelieverName, GroupTitle, PartnerName, RopeTerm
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.a03_group_logic.partner import PartnerUnit
from src.a04_reason_logic.reason_labor import LaborHeir
from src.a04_reason_logic.reason_plan import CaseUnit, FactHeir, ReasonHeir
from src.a05_plan_logic.plan import HealerLink, PlanUnit
from src.a06_believer_logic.believer_main import BelieverUnit
from src.a11_bud_logic.bud import BeliefLabel


def create_blrmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    partner_name = values_dict.get("partner_name")
    group_title = values_dict.get("group_title")
    group_cred_points = values_dict.get("group_cred_points")
    group_debt_points = values_dict.get("group_debt_points")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    _fund_agenda_ratio_give = values_dict.get("_fund_agenda_ratio_give")
    _fund_agenda_ratio_take = values_dict.get("_fund_agenda_ratio_take")
    real_str = "REAL"
    return f"""INSERT INTO believer_partner_membership_job (belief_label, believer_name, partner_name, group_title, group_cred_points, group_debt_points, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(partner_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(group_cred_points, real_str)}
, {sqlite_obj_str(group_debt_points, real_str)}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_take, real_str)}
)
;
"""


def create_blrpern_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    partner_name = values_dict.get("partner_name")
    partner_cred_points = values_dict.get("partner_cred_points")
    partner_debt_points = values_dict.get("partner_debt_points")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    _fund_agenda_ratio_give = values_dict.get("_fund_agenda_ratio_give")
    _fund_agenda_ratio_take = values_dict.get("_fund_agenda_ratio_take")
    _inallocable_partner_debt_points = values_dict.get(
        "_inallocable_partner_debt_points"
    )
    _irrational_partner_debt_points = values_dict.get("_irrational_partner_debt_points")
    real_str = "REAL"
    return f"""INSERT INTO believer_partnerunit_job (belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take, _inallocable_partner_debt_points, _irrational_partner_debt_points)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(partner_name, "TEXT")}
, {sqlite_obj_str(partner_cred_points, real_str)}
, {sqlite_obj_str(partner_debt_points, real_str)}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_take, real_str)}
, {sqlite_obj_str(_inallocable_partner_debt_points, real_str)}
, {sqlite_obj_str(_irrational_partner_debt_points, real_str)}
)
;
"""


def create_blrgrou_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    group_title = values_dict.get("group_title")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    fund_iota = values_dict.get("fund_iota")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    knot = values_dict.get("knot")
    real_str = "REAL"
    return f"""INSERT INTO believer_groupunit_job (belief_label, believer_name, group_title, fund_iota, knot, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(fund_iota, real_str)}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
)
;
"""


def create_blrawar_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    awardee_title = values_dict.get("awardee_title")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    return f"""INSERT INTO believer_plan_awardlink_job (belief_label, believer_name, plan_rope, awardee_title, give_force, take_force, _fund_give, _fund_take)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(awardee_title, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(_fund_give, "REAL")}
, {sqlite_obj_str(_fund_take, "REAL")}
)
;
"""


def create_blrfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    fact_context = values_dict.get("fact_context")
    fact_state = values_dict.get("fact_state")
    fact_lower = values_dict.get("fact_lower")
    fact_upper = values_dict.get("fact_upper")
    return f"""INSERT INTO believer_plan_factunit_job (belief_label, believer_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(fact_context, "TEXT")}
, {sqlite_obj_str(fact_state, "TEXT")}
, {sqlite_obj_str(fact_lower, "REAL")}
, {sqlite_obj_str(fact_upper, "REAL")}
)
;
"""


def create_blrheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO believer_plan_healerlink_job (belief_label, believer_name, plan_rope, healer_name)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_blrprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    reason_state = values_dict.get("reason_state")
    reason_upper = values_dict.get("reason_upper")
    reason_lower = values_dict.get("reason_lower")
    reason_divisor = values_dict.get("reason_divisor")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    return f"""INSERT INTO believer_plan_reason_caseunit_job (belief_label, believer_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor, _chore, _status)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(reason_state, "TEXT")}
, {sqlite_obj_str(reason_upper, "REAL")}
, {sqlite_obj_str(reason_lower, "REAL")}
, {sqlite_obj_str(reason_divisor, "REAL")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
)
;
"""


def create_blrreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    reason_active_requisite = values_dict.get("reason_active_requisite")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    _rplan_active_value = values_dict.get("_rplan_active_value")
    return f"""INSERT INTO believer_plan_reasonunit_job (belief_label, believer_name, plan_rope, reason_context, reason_active_requisite, _chore, _status, _rplan_active_value)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(reason_active_requisite, "INTEGER")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_rplan_active_value, "INTEGER")}
)
;
"""


def create_blrlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    labor_title = values_dict.get("labor_title")
    _believer_name_labor = values_dict.get("_believer_name_labor")
    return f"""INSERT INTO believer_plan_laborlink_job (belief_label, believer_name, plan_rope, labor_title, _believer_name_labor)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(labor_title, "TEXT")}
, {sqlite_obj_str(_believer_name_labor, "INTEGER")}
)
;
"""


def create_blrplan_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    rope = values_dict.get("plan_rope")
    begin = values_dict.get("begin")
    close = values_dict.get("close")
    addin = values_dict.get("addin")
    numor = values_dict.get("numor")
    denom = values_dict.get("denom")
    morph = values_dict.get("morph")
    gogo_want = values_dict.get("gogo_want")
    stop_want = values_dict.get("stop_want")
    mass = values_dict.get("mass")
    task = values_dict.get("task")
    problem_bool = values_dict.get("problem_bool")
    _active = values_dict.get("_active")
    _chore = values_dict.get("_chore")
    fund_iota = values_dict.get("fund_iota")
    _fund_onset = values_dict.get("_fund_onset")
    _fund_cease = values_dict.get("_fund_cease")
    _fund_ratio = values_dict.get("_fund_ratio")
    _gogo_calc = values_dict.get("_gogo_calc")
    _stop_calc = values_dict.get("_stop_calc")
    _level = values_dict.get("_level")
    _range_evaluated = values_dict.get("_range_evaluated")
    _descendant_task_count = values_dict.get("_descendant_task_count")
    _healerlink_ratio = values_dict.get("_healerlink_ratio")
    _all_partner_cred = values_dict.get("_all_partner_cred")
    _all_partner_debt = values_dict.get("_all_partner_debt")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO believer_planunit_job (belief_label, believer_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool, fund_iota, _active, _chore, _fund_onset, _fund_cease, _fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_task_count, _healerlink_ratio, _all_partner_cred, _all_partner_debt)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(begin, real_str)}
, {sqlite_obj_str(close, real_str)}
, {sqlite_obj_str(addin, real_str)}
, {sqlite_obj_str(numor, "INTEGER")}
, {sqlite_obj_str(denom, "INTEGER")}
, {sqlite_obj_str(morph, real_str)}
, {sqlite_obj_str(gogo_want, real_str)}
, {sqlite_obj_str(stop_want, real_str)}
, {sqlite_obj_str(mass, real_str)}
, {sqlite_obj_str(task, real_str)}
, {sqlite_obj_str(problem_bool, "INTEGER")}
, {sqlite_obj_str(fund_iota, real_str)}
, {sqlite_obj_str(_active, "INTEGER")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_fund_onset, real_str)}
, {sqlite_obj_str(_fund_cease, real_str)}
, {sqlite_obj_str(_fund_ratio, real_str)}
, {sqlite_obj_str(_gogo_calc, real_str)}
, {sqlite_obj_str(_stop_calc, real_str)}
, {sqlite_obj_str(_level, "INTEGER")}
, {sqlite_obj_str(_range_evaluated, "INTEGER")}
, {sqlite_obj_str(_descendant_task_count, "INTEGER")}
, {sqlite_obj_str(_healerlink_ratio, real_str)}
, {sqlite_obj_str(_all_partner_cred, real_str)}
, {sqlite_obj_str(_all_partner_debt, real_str)}
)
;
"""


def create_believerunit_metrics_insert_sqlstr(values_dict: dict[str,]):
    belief_label = values_dict.get("belief_label")
    believer_name = values_dict.get("believer_name")
    integer_str = "INTEGER"
    real_str = "REAL"
    _keeps_buildable = values_dict.get("_keeps_buildable")
    _keeps_justified = values_dict.get("_keeps_justified")
    _offtrack_fund = values_dict.get("_offtrack_fund")
    _rational = values_dict.get("_rational")
    _sum_healerlink_share = values_dict.get("_sum_healerlink_share")
    _tree_traverse_count = values_dict.get("_tree_traverse_count")
    credor_respect = values_dict.get("credor_respect")
    debtor_respect = values_dict.get("debtor_respect")
    fund_iota = values_dict.get("fund_iota")
    fund_pool = values_dict.get("fund_pool")
    max_tree_traverse = values_dict.get("max_tree_traverse")
    penny = values_dict.get("penny")
    respect_bit = values_dict.get("respect_bit")
    tally = values_dict.get("tally")

    return f"""INSERT INTO believerunit_job (belief_label, believer_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerlink_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(belief_label, "TEXT")}
, {sqlite_obj_str(believer_name, "TEXT")}
, {sqlite_obj_str(credor_respect, real_str)}
, {sqlite_obj_str(debtor_respect, real_str)}
, {sqlite_obj_str(fund_pool, real_str)}
, {sqlite_obj_str(max_tree_traverse, integer_str)}
, {sqlite_obj_str(tally, real_str)}
, {sqlite_obj_str(fund_iota, real_str)}
, {sqlite_obj_str(penny, real_str)}
, {sqlite_obj_str(respect_bit, real_str)}
, {sqlite_obj_str(_rational, integer_str)}
, {sqlite_obj_str(_keeps_justified, integer_str)}
, {sqlite_obj_str(_offtrack_fund, real_str)}
, {sqlite_obj_str(_sum_healerlink_share, real_str)}
, {sqlite_obj_str(_keeps_buildable, integer_str)}
, {sqlite_obj_str(_tree_traverse_count, integer_str)}
)
;
"""


@dataclass
class ObjKeysHolder:
    belief_label: BeliefLabel = None
    believer_name: BelieverName = None
    rope: RopeTerm = None
    reason_context: RopeTerm = None
    partner_name: PartnerName = None
    membership: GroupTitle = None
    group_title: GroupTitle = None
    fact_rope: RopeTerm = None


def insert_job_blrmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    insert_sqlstr = create_blrmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrpern(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_partner: PartnerUnit,
):
    x_dict = copy_deepcopy(x_partner.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    insert_sqlstr = create_blrpern_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrgrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    insert_sqlstr = create_blrgrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "belief_label": x_objkeysholder.belief_label,
        "believer_name": x_objkeysholder.believer_name,
        "plan_rope": x_objkeysholder.rope,
    }
    for healer_name in sorted(x_healer._healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_blrheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_blrprem(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_caseunit: CaseUnit,
):
    x_dict = copy_deepcopy(x_caseunit.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["reason_context"] = x_objkeysholder.reason_context
    insert_sqlstr = create_blrprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_laborheir: LaborHeir,
):
    x_dict = copy_deepcopy(x_laborheir.__dict__)
    x_dict["belief_label"] = x_objkeysholder.belief_label
    x_dict["believer_name"] = x_objkeysholder.believer_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    for labor_title in sorted(x_laborheir._laborlinks):
        x_dict["labor_title"] = labor_title
        insert_sqlstr = create_blrlabo_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_blrplan(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_plan: PlanUnit
):
    x_dict = copy_deepcopy(x_plan.__dict__)
    x_dict["plan_rope"] = x_plan.get_plan_rope()
    x_dict["believer_name"] = x_objkeysholder.believer_name
    insert_sqlstr = create_blrplan_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_believer: BelieverUnit
):
    x_dict = copy_deepcopy(x_believer.__dict__)
    insert_sqlstr = create_believerunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, job_believer: BelieverUnit):
    job_believer.settle_believer()
    x_objkeysholder = ObjKeysHolder(
        job_believer.belief_label, job_believer.believer_name
    )
    insert_job_blrunit(cursor, x_objkeysholder, job_believer)
    for x_plan in job_believer.get_plan_dict().values():
        x_objkeysholder.rope = x_plan.get_plan_rope()
        healerlink = x_plan.healerlink
        laborheir = x_plan._laborheir
        insert_job_blrplan(cursor, x_objkeysholder, x_plan)
        insert_job_blrheal(cursor, x_objkeysholder, healerlink)
        insert_job_blrlabo(cursor, x_objkeysholder, laborheir)
        for x_awardheir in x_plan._awardheirs.values():
            insert_job_blrawar(cursor, x_objkeysholder, x_awardheir)
        for reason_context, reasonheir in x_plan._reasonheirs.items():
            insert_job_blrreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.reason_context = reason_context
            for prem in reasonheir.cases.values():
                insert_job_blrprem(cursor, x_objkeysholder, prem)

    for x_partner in job_believer.partners.values():
        insert_job_blrpern(cursor, x_objkeysholder, x_partner)
        for x_membership in x_partner._memberships.values():
            insert_job_blrmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_believer._groupunits.values():
        insert_job_blrgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_believer.planroot._factheirs.values():
        x_objkeysholder.fact_rope = job_believer.planroot.get_plan_rope()
        insert_job_blrfact(cursor, x_objkeysholder, x_factheir)
