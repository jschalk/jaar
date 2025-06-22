from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.db_toolbox import sqlite_obj_str
from src.a01_term_logic.term import AcctName, GroupTitle, OwnerName, RopeTerm
from src.a02_finance_logic.bud import BankLabel
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.a04_reason_logic.reason_concept import FactHeir, PremiseUnit, ReasonHeir
from src.a04_reason_logic.reason_labor import LaborHeir
from src.a05_concept_logic.concept import ConceptUnit, HealerLink
from src.a06_plan_logic.plan import PlanUnit


def create_plnmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    acct_name = values_dict.get("acct_name")
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
    return f"""INSERT INTO plan_acct_membership_job (bank_label, owner_name, acct_name, group_title, group_cred_points, group_debt_points, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(acct_name, "TEXT")}
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


def create_plnacct_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    acct_name = values_dict.get("acct_name")
    acct_cred_points = values_dict.get("acct_cred_points")
    acct_debt_points = values_dict.get("acct_debt_points")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    _fund_agenda_ratio_give = values_dict.get("_fund_agenda_ratio_give")
    _fund_agenda_ratio_take = values_dict.get("_fund_agenda_ratio_take")
    _inallocable_acct_debt_points = values_dict.get("_inallocable_acct_debt_points")
    _irrational_acct_debt_points = values_dict.get("_irrational_acct_debt_points")
    real_str = "REAL"
    return f"""INSERT INTO plan_acctunit_job (bank_label, owner_name, acct_name, acct_cred_points, acct_debt_points, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take, _inallocable_acct_debt_points, _irrational_acct_debt_points)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(acct_name, "TEXT")}
, {sqlite_obj_str(acct_cred_points, real_str)}
, {sqlite_obj_str(acct_debt_points, real_str)}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_take, real_str)}
, {sqlite_obj_str(_inallocable_acct_debt_points, real_str)}
, {sqlite_obj_str(_irrational_acct_debt_points, real_str)}
)
;
"""


def create_plngrou_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
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
    return f"""INSERT INTO plan_groupunit_job (bank_label, owner_name, group_title, fund_iota, knot, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
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


def create_plnawar_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    awardee_title = values_dict.get("awardee_title")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    return f"""INSERT INTO plan_concept_awardlink_job (bank_label, owner_name, concept_rope, awardee_title, give_force, take_force, _fund_give, _fund_take)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(awardee_title, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(_fund_give, "REAL")}
, {sqlite_obj_str(_fund_take, "REAL")}
)
;
"""


def create_plnfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    fcontext = values_dict.get("fcontext")
    fstate = values_dict.get("fstate")
    fopen = values_dict.get("fopen")
    fnigh = values_dict.get("fnigh")
    return f"""INSERT INTO plan_concept_factunit_job (bank_label, owner_name, concept_rope, fcontext, fstate, fopen, fnigh)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(fcontext, "TEXT")}
, {sqlite_obj_str(fstate, "TEXT")}
, {sqlite_obj_str(fopen, "REAL")}
, {sqlite_obj_str(fnigh, "REAL")}
)
;
"""


def create_plnheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO plan_concept_healerlink_job (bank_label, owner_name, concept_rope, healer_name)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_plnprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    rcontext = values_dict.get("rcontext")
    pstate = values_dict.get("pstate")
    pnigh = values_dict.get("pnigh")
    popen = values_dict.get("popen")
    pdivisor = values_dict.get("pdivisor")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    return f"""INSERT INTO plan_concept_reason_premiseunit_job (bank_label, owner_name, concept_rope, rcontext, pstate, pnigh, popen, pdivisor, _chore, _status)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(pstate, "TEXT")}
, {sqlite_obj_str(pnigh, "REAL")}
, {sqlite_obj_str(popen, "REAL")}
, {sqlite_obj_str(pdivisor, "REAL")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
)
;
"""


def create_plnreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    rcontext = values_dict.get("rcontext")
    rconcept_active_requisite = values_dict.get("rconcept_active_requisite")
    _chore = values_dict.get("_chore")
    _status = values_dict.get("_status")
    _rconcept_active_value = values_dict.get("_rconcept_active_value")
    return f"""INSERT INTO plan_concept_reasonunit_job (bank_label, owner_name, concept_rope, rcontext, rconcept_active_requisite, _chore, _status, _rconcept_active_value)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(rconcept_active_requisite, "INTEGER")}
, {sqlite_obj_str(_chore, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_rconcept_active_value, "INTEGER")}
)
;
"""


def create_plnlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
    labor_title = values_dict.get("labor_title")
    _owner_name_labor = values_dict.get("_owner_name_labor")
    return f"""INSERT INTO plan_concept_laborlink_job (bank_label, owner_name, concept_rope, labor_title, _owner_name_labor)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(labor_title, "TEXT")}
, {sqlite_obj_str(_owner_name_labor, "INTEGER")}
)
;
"""


def create_plnconc_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
    rope = values_dict.get("concept_rope")
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
    _all_acct_cred = values_dict.get("_all_acct_cred")
    _all_acct_debt = values_dict.get("_all_acct_debt")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO plan_conceptunit_job (bank_label, owner_name, concept_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool, fund_iota, _active, _chore, _fund_onset, _fund_cease, _fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_task_count, _healerlink_ratio, _all_acct_cred, _all_acct_debt)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
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
, {sqlite_obj_str(_all_acct_cred, real_str)}
, {sqlite_obj_str(_all_acct_debt, real_str)}
)
;
"""


def create_planunit_metrics_insert_sqlstr(values_dict: dict[str,]):
    bank_label = values_dict.get("bank_label")
    owner_name = values_dict.get("owner_name")
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

    return f"""INSERT INTO planunit_job (bank_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerlink_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(bank_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
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
    bank_label: BankLabel = None
    owner_name: OwnerName = None
    rope: RopeTerm = None
    rcontext: RopeTerm = None
    acct_name: AcctName = None
    membership: GroupTitle = None
    group_title: GroupTitle = None
    fact_rope: RopeTerm = None


def insert_job_plnmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_plnmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnacct(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_acct: AcctUnit,
):
    x_dict = copy_deepcopy(x_acct.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_plnacct_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plngrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_plngrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_plnawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_plnfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "bank_label": x_objkeysholder.bank_label,
        "owner_name": x_objkeysholder.owner_name,
        "concept_rope": x_objkeysholder.rope,
    }
    for healer_name in sorted(x_healer._healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_plnheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_plnprem(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_premiseunit: PremiseUnit,
):
    x_dict = copy_deepcopy(x_premiseunit.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_rope"] = x_objkeysholder.rope
    x_dict["rcontext"] = x_objkeysholder.rcontext
    insert_sqlstr = create_plnprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_plnreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_laborheir: LaborHeir,
):
    x_dict = copy_deepcopy(x_laborheir.__dict__)
    x_dict["bank_label"] = x_objkeysholder.bank_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_rope"] = x_objkeysholder.rope
    for labor_title in sorted(x_laborheir._laborlinks):
        x_dict["labor_title"] = labor_title
        insert_sqlstr = create_plnlabo_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_plnconc(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_concept: ConceptUnit
):
    x_dict = copy_deepcopy(x_concept.__dict__)
    x_dict["concept_rope"] = x_concept.get_concept_rope()
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_plnconc_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_plnunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_plan: PlanUnit
):
    x_dict = copy_deepcopy(x_plan.__dict__)
    insert_sqlstr = create_planunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, job_plan: PlanUnit):
    job_plan.settle_plan()
    x_objkeysholder = ObjKeysHolder(job_plan.bank_label, job_plan.owner_name)
    insert_job_plnunit(cursor, x_objkeysholder, job_plan)
    for x_concept in job_plan.get_concept_dict().values():
        x_objkeysholder.rope = x_concept.get_concept_rope()
        healerlink = x_concept.healerlink
        laborheir = x_concept._laborheir
        insert_job_plnconc(cursor, x_objkeysholder, x_concept)
        insert_job_plnheal(cursor, x_objkeysholder, healerlink)
        insert_job_plnlabo(cursor, x_objkeysholder, laborheir)
        for x_awardheir in x_concept._awardheirs.values():
            insert_job_plnawar(cursor, x_objkeysholder, x_awardheir)
        for rcontext, reasonheir in x_concept._reasonheirs.items():
            insert_job_plnreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.rcontext = rcontext
            for prem in reasonheir.premises.values():
                insert_job_plnprem(cursor, x_objkeysholder, prem)

    for x_acct in job_plan.accts.values():
        insert_job_plnacct(cursor, x_objkeysholder, x_acct)
        for x_membership in x_acct._memberships.values():
            insert_job_plnmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_plan._groupunits.values():
        insert_job_plngrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_plan.conceptroot._factheirs.values():
        x_objkeysholder.fact_rope = job_plan.conceptroot.get_concept_rope()
        insert_job_plnfact(cursor, x_objkeysholder, x_factheir)
