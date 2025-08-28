from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.db_toolbox import sqlite_obj_str
from src.a01_term_logic.term import BeliefName, GroupTitle, RopeTerm, VoiceName
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.a03_group_logic.labor import LaborHeir
from src.a03_group_logic.voice import VoiceUnit
from src.a04_reason_logic.reason import CaseUnit, FactHeir, ReasonHeir
from src.a05_plan_logic.plan import HealerUnit, PlanUnit
from src.a06_belief_logic.belief_main import BeliefUnit
from src.a11_bud_logic.bud import MomentLabel


def create_blrmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    voice_name = values_dict.get("voice_name")
    group_title = values_dict.get("group_title")
    group_cred_points = values_dict.get("group_cred_points")
    group_debt_points = values_dict.get("group_debt_points")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
    fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
    real_str = "REAL"
    return f"""INSERT INTO belief_voice_membership_job (moment_label, belief_name, voice_name, group_title, group_cred_points, group_debt_points, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(voice_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(group_cred_points, real_str)}
, {sqlite_obj_str(group_debt_points, real_str)}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
)
;
"""


def create_blrpern_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    voice_name = values_dict.get("voice_name")
    voice_cred_points = values_dict.get("voice_cred_points")
    voice_debt_points = values_dict.get("voice_debt_points")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
    fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
    _inallocable_voice_debt_points = values_dict.get("_inallocable_voice_debt_points")
    _irrational_voice_debt_points = values_dict.get("_irrational_voice_debt_points")
    real_str = "REAL"
    return f"""INSERT INTO belief_voiceunit_job (moment_label, belief_name, voice_name, voice_cred_points, voice_debt_points, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take, _inallocable_voice_debt_points, _irrational_voice_debt_points)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(voice_name, "TEXT")}
, {sqlite_obj_str(voice_cred_points, real_str)}
, {sqlite_obj_str(voice_debt_points, real_str)}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
, {sqlite_obj_str(_inallocable_voice_debt_points, real_str)}
, {sqlite_obj_str(_irrational_voice_debt_points, real_str)}
)
;
"""


def create_blrgrou_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    group_title = values_dict.get("group_title")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_iota = values_dict.get("fund_iota")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    knot = values_dict.get("knot")
    real_str = "REAL"
    return f"""INSERT INTO belief_groupunit_job (moment_label, belief_name, group_title, fund_iota, knot, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(fund_iota, real_str)}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
)
;
"""


def create_blrawar_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    awardee_title = values_dict.get("awardee_title")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    return f"""INSERT INTO belief_plan_awardunit_job (moment_label, belief_name, plan_rope, awardee_title, give_force, take_force, fund_give, fund_take)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(awardee_title, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(fund_give, "REAL")}
, {sqlite_obj_str(fund_take, "REAL")}
)
;
"""


def create_blrfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    fact_context = values_dict.get("fact_context")
    fact_state = values_dict.get("fact_state")
    fact_lower = values_dict.get("fact_lower")
    fact_upper = values_dict.get("fact_upper")
    return f"""INSERT INTO belief_plan_factunit_job (moment_label, belief_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(fact_context, "TEXT")}
, {sqlite_obj_str(fact_state, "TEXT")}
, {sqlite_obj_str(fact_lower, "REAL")}
, {sqlite_obj_str(fact_upper, "REAL")}
)
;
"""


def create_blrheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO belief_plan_healerunit_job (moment_label, belief_name, plan_rope, healer_name)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_blrprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    reason_state = values_dict.get("reason_state")
    reason_upper = values_dict.get("reason_upper")
    reason_lower = values_dict.get("reason_lower")
    reason_divisor = values_dict.get("reason_divisor")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    return f"""INSERT INTO belief_plan_reason_caseunit_job (moment_label, belief_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor, _chore, _status)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
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
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    reason_active_requisite = values_dict.get("reason_active_requisite")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    _reason_active_heir = values_dict.get("_reason_active_heir")
    return f"""INSERT INTO belief_plan_reasonunit_job (moment_label, belief_name, plan_rope, reason_context, reason_active_requisite, _chore, _status, _reason_active_heir)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(reason_active_requisite, "INTEGER")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_reason_active_heir, "INTEGER")}
)
;
"""


def create_blrlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    party_title = values_dict.get("party_title")
    solo = values_dict.get("solo")
    _belief_name_is_labor = values_dict.get("_belief_name_is_labor")
    return f"""INSERT INTO belief_plan_partyunit_job (moment_label, belief_name, plan_rope, party_title, solo, _belief_name_is_labor)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(party_title, "TEXT")}
, {sqlite_obj_str(solo, "INTEGER")}
, {sqlite_obj_str(_belief_name_is_labor, "INTEGER")}
)
;
"""


def create_blrplan_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    rope = values_dict.get("plan_rope")
    begin = values_dict.get("begin")
    close = values_dict.get("close")
    addin = values_dict.get("addin")
    numor = values_dict.get("numor")
    denom = values_dict.get("denom")
    morph = values_dict.get("morph")
    gogo_want = values_dict.get("gogo_want")
    stop_want = values_dict.get("stop_want")
    star = values_dict.get("star")
    task = values_dict.get("task")
    problem_bool = values_dict.get("problem_bool")
    _active = values_dict.get("_active")
    _chore = values_dict.get("_chore")
    fund_iota = values_dict.get("fund_iota")
    fund_onset = values_dict.get("fund_onset")
    fund_cease = values_dict.get("fund_cease")
    fund_ratio = values_dict.get("fund_ratio")
    _gogo_calc = values_dict.get("_gogo_calc")
    _stop_calc = values_dict.get("_stop_calc")
    _level = values_dict.get("_level")
    _range_evaluated = values_dict.get("_range_evaluated")
    _descendant_task_count = values_dict.get("_descendant_task_count")
    _healerunit_ratio = values_dict.get("_healerunit_ratio")
    _all_voice_cred = values_dict.get("_all_voice_cred")
    _all_voice_debt = values_dict.get("_all_voice_debt")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO belief_planunit_job (moment_label, belief_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool, fund_iota, _active, _chore, fund_onset, fund_cease, fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_task_count, _healerunit_ratio, _all_voice_cred, _all_voice_debt)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(begin, real_str)}
, {sqlite_obj_str(close, real_str)}
, {sqlite_obj_str(addin, real_str)}
, {sqlite_obj_str(numor, "INTEGER")}
, {sqlite_obj_str(denom, "INTEGER")}
, {sqlite_obj_str(morph, real_str)}
, {sqlite_obj_str(gogo_want, real_str)}
, {sqlite_obj_str(stop_want, real_str)}
, {sqlite_obj_str(star, real_str)}
, {sqlite_obj_str(task, real_str)}
, {sqlite_obj_str(problem_bool, "INTEGER")}
, {sqlite_obj_str(fund_iota, real_str)}
, {sqlite_obj_str(_active, "INTEGER")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(fund_onset, real_str)}
, {sqlite_obj_str(fund_cease, real_str)}
, {sqlite_obj_str(fund_ratio, real_str)}
, {sqlite_obj_str(_gogo_calc, real_str)}
, {sqlite_obj_str(_stop_calc, real_str)}
, {sqlite_obj_str(_level, "INTEGER")}
, {sqlite_obj_str(_range_evaluated, "INTEGER")}
, {sqlite_obj_str(_descendant_task_count, "INTEGER")}
, {sqlite_obj_str(_healerunit_ratio, real_str)}
, {sqlite_obj_str(_all_voice_cred, real_str)}
, {sqlite_obj_str(_all_voice_debt, real_str)}
)
;
"""


def create_beliefunit_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_label = values_dict.get("moment_label")
    belief_name = values_dict.get("belief_name")
    integer_str = "INTEGER"
    real_str = "REAL"
    _keeps_buildable = values_dict.get("_keeps_buildable")
    _keeps_justified = values_dict.get("_keeps_justified")
    _offtrack_fund = values_dict.get("_offtrack_fund")
    _rational = values_dict.get("_rational")
    _sum_healerunit_share = values_dict.get("_sum_healerunit_share")
    _tree_traverse_count = values_dict.get("_tree_traverse_count")
    credor_respect = values_dict.get("credor_respect")
    debtor_respect = values_dict.get("debtor_respect")
    fund_iota = values_dict.get("fund_iota")
    fund_pool = values_dict.get("fund_pool")
    max_tree_traverse = values_dict.get("max_tree_traverse")
    penny = values_dict.get("penny")
    respect_bit = values_dict.get("respect_bit")
    tally = values_dict.get("tally")

    return f"""INSERT INTO beliefunit_job (moment_label, belief_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerunit_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(moment_label, "TEXT")}
, {sqlite_obj_str(belief_name, "TEXT")}
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
, {sqlite_obj_str(_sum_healerunit_share, real_str)}
, {sqlite_obj_str(_keeps_buildable, integer_str)}
, {sqlite_obj_str(_tree_traverse_count, integer_str)}
)
;
"""


@dataclass
class ObjKeysHolder:
    moment_label: MomentLabel = None
    belief_name: BeliefName = None
    rope: RopeTerm = None
    reason_context: RopeTerm = None
    voice_name: VoiceName = None
    membership: GroupTitle = None
    group_title: GroupTitle = None
    fact_rope: RopeTerm = None


def insert_job_blrmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    insert_sqlstr = create_blrmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrpern(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_voice: VoiceUnit,
):
    x_dict = copy_deepcopy(x_voice.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    insert_sqlstr = create_blrpern_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrgrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    insert_sqlstr = create_blrgrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerUnit,
):
    x_dict = {
        "moment_label": x_objkeysholder.moment_label,
        "belief_name": x_objkeysholder.belief_name,
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
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
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
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_blrreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_laborheir: LaborHeir,
):
    x_dict = copy_deepcopy(x_laborheir.__dict__)
    x_dict["moment_label"] = x_objkeysholder.moment_label
    x_dict["belief_name"] = x_objkeysholder.belief_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    for party_title in sorted(x_laborheir._partys):
        partyheir = x_laborheir._partys.get(party_title)
        x_dict["party_title"] = partyheir.party_title
        x_dict["solo"] = partyheir.solo
        insert_sqlstr = create_blrlabo_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_blrplan(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_plan: PlanUnit
):
    x_dict = copy_deepcopy(x_plan.__dict__)
    x_dict["plan_rope"] = x_plan.get_plan_rope()
    x_dict["belief_name"] = x_objkeysholder.belief_name
    insert_sqlstr = create_blrplan_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_blrunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_belief: BeliefUnit
):
    x_dict = copy_deepcopy(x_belief.__dict__)
    insert_sqlstr = create_beliefunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, job_belief: BeliefUnit):
    job_belief.cash_out()
    x_objkeysholder = ObjKeysHolder(job_belief.moment_label, job_belief.belief_name)
    insert_job_blrunit(cursor, x_objkeysholder, job_belief)
    for x_plan in job_belief.get_plan_dict().values():
        x_objkeysholder.rope = x_plan.get_plan_rope()
        healerunit = x_plan.healerunit
        laborheir = x_plan._laborheir
        insert_job_blrplan(cursor, x_objkeysholder, x_plan)
        insert_job_blrheal(cursor, x_objkeysholder, healerunit)
        insert_job_blrlabo(cursor, x_objkeysholder, laborheir)
        for x_awardheir in x_plan._awardheirs.values():
            insert_job_blrawar(cursor, x_objkeysholder, x_awardheir)
        for reason_context, reasonheir in x_plan._reasonheirs.items():
            insert_job_blrreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.reason_context = reason_context
            for prem in reasonheir.cases.values():
                insert_job_blrprem(cursor, x_objkeysholder, prem)

    for x_voice in job_belief.voices.values():
        insert_job_blrpern(cursor, x_objkeysholder, x_voice)
        for x_membership in x_voice._memberships.values():
            insert_job_blrmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_belief.groupunits.values():
        insert_job_blrgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_belief.planroot._factheirs.values():
        x_objkeysholder.fact_rope = job_belief.planroot.get_plan_rope()
        insert_job_blrfact(cursor, x_objkeysholder, x_factheir)
