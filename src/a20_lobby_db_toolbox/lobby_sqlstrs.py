from src.a00_data_toolbox.db_toolbox import sqlite_obj_str
from src.a17_creed_logic.creed_db_tool import (
    get_default_sorted_list,
    create_creed_sorted_table,
)
from src.a17_creed_logic.creed_config import (
    get_quick_creeds_column_ref,
    get_creed_sqlite_types,
)
from sqlite3 import Connection as sqlite3_Connection


CREATE_JOB_BUDMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL)"""
CREATE_JOB_BUDACCT_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL, _inallocable_debtit_belief REAL, _irrational_debtit_belief REAL)"""
CREATE_JOB_BUDGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_groupunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, group_label TEXT, fund_coin REAL, bridge TEXT, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL)"""
CREATE_JOB_BUDAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_awardlink_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL, _fund_give REAL, _fund_take REAL)"""
CREATE_JOB_BUDFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_factunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"""
CREATE_JOB_BUDHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_healerlink_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT)"""
CREATE_JOB_BUDPREM_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, _task INTEGER, _status INTEGER)"""
CREATE_JOB_BUDREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER, _task INTEGER, _status INTEGER, _rcontext_idea_active_value INTEGER)"""
CREATE_JOB_BUDLABOR_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_laborlink_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT, _owner_name_labor INTEGER)"""
CREATE_JOB_BUDIDEA_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_ideaunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, fund_coin REAL, _active INTEGER, _task INTEGER, _fund_onset REAL, _fund_cease REAL, _fund_ratio REAL, _gogo_calc REAL, _stop_calc REAL, _level INTEGER, _range_evaluated INTEGER, _descendant_pledge_count INTEGER, _healerlink_ratio REAL, _all_acct_cred INTEGER, _all_acct_debt INTEGER)"""
CREATE_JOB_BUDUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_job (world_id TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, _rational INTEGER, _keeps_justified INTEGER, _offtrack_fund REAL, _sum_healerlink_share REAL, _keeps_buildable INTEGER, _tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership_job": CREATE_JOB_BUDMEMB_SQLSTR,
        "bud_acctunit_job": CREATE_JOB_BUDACCT_SQLSTR,
        "bud_groupunit_job": CREATE_JOB_BUDGROU_SQLSTR,
        "bud_idea_awardlink_job": CREATE_JOB_BUDAWAR_SQLSTR,
        "bud_idea_factunit_job": CREATE_JOB_BUDFACT_SQLSTR,
        "bud_idea_healerlink_job": CREATE_JOB_BUDHEAL_SQLSTR,
        "bud_idea_reason_premiseunit_job": CREATE_JOB_BUDPREM_SQLSTR,
        "bud_idea_reasonunit_job": CREATE_JOB_BUDREAS_SQLSTR,
        "bud_idea_laborlink_job": CREATE_JOB_BUDLABOR_SQLSTR,
        "bud_ideaunit_job": CREATE_JOB_BUDIDEA_SQLSTR,
        "budunit_job": CREATE_JOB_BUDUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_budmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    acct_name = values_dict.get("acct_name")
    group_label = values_dict.get("group_label")
    credit_vote = values_dict.get("credit_vote")
    debtit_vote = values_dict.get("debtit_vote")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    _fund_agenda_ratio_give = values_dict.get("_fund_agenda_ratio_give")
    _fund_agenda_ratio_take = values_dict.get("_fund_agenda_ratio_take")
    real_str = "REAL"
    return f"""INSERT INTO bud_acct_membership_job (world_id, fisc_tag, owner_name, acct_name, group_label, credit_vote, debtit_vote, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(acct_name, "TEXT")}
, {sqlite_obj_str(group_label, "TEXT")}
, {sqlite_obj_str(credit_vote, real_str)}
, {sqlite_obj_str(debtit_vote, real_str)}
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


def create_budacct_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    acct_name = values_dict.get("acct_name")
    credit_belief = values_dict.get("credit_belief")
    debtit_belief = values_dict.get("debtit_belief")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    _fund_agenda_ratio_give = values_dict.get("_fund_agenda_ratio_give")
    _fund_agenda_ratio_take = values_dict.get("_fund_agenda_ratio_take")
    _inallocable_debtit_belief = values_dict.get("_inallocable_debtit_belief")
    _irrational_debtit_belief = values_dict.get("_irrational_debtit_belief")
    real_str = "REAL"
    return f"""INSERT INTO bud_acctunit_job (world_id, fisc_tag, owner_name, acct_name, credit_belief, debtit_belief, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take, _inallocable_debtit_belief, _irrational_debtit_belief)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(acct_name, "TEXT")}
, {sqlite_obj_str(credit_belief, real_str)}
, {sqlite_obj_str(debtit_belief, real_str)}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(_fund_agenda_ratio_take, real_str)}
, {sqlite_obj_str(_inallocable_debtit_belief, real_str)}
, {sqlite_obj_str(_irrational_debtit_belief, real_str)}
)
;
"""


def create_budgrou_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    group_label = values_dict.get("group_label")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    fund_coin = values_dict.get("fund_coin")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    bridge = values_dict.get("bridge")
    real_str = "REAL"
    return f"""INSERT INTO bud_groupunit_job (world_id, fisc_tag, owner_name, group_label, fund_coin, bridge, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(group_label, "TEXT")}
, {sqlite_obj_str(fund_coin, real_str)}
, {sqlite_obj_str(bridge, "TEXT")}
, {sqlite_obj_str(_credor_pool, real_str)}
, {sqlite_obj_str(_debtor_pool, real_str)}
, {sqlite_obj_str(_fund_give, real_str)}
, {sqlite_obj_str(_fund_take, real_str)}
, {sqlite_obj_str(_fund_agenda_give, real_str)}
, {sqlite_obj_str(_fund_agenda_take, real_str)}
)
;
"""


def create_budawar_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    awardee_label = values_dict.get("awardee_label")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    return f"""INSERT INTO bud_idea_awardlink_job (world_id, fisc_tag, owner_name, idea_way, awardee_label, give_force, take_force, _fund_give, _fund_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(awardee_label, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(_fund_give, "REAL")}
, {sqlite_obj_str(_fund_take, "REAL")}
)
;
"""


def create_budfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    fcontext = values_dict.get("fcontext")
    fbranch = values_dict.get("fbranch")
    fopen = values_dict.get("fopen")
    fnigh = values_dict.get("fnigh")
    return f"""INSERT INTO bud_idea_factunit_job (world_id, fisc_tag, owner_name, idea_way, fcontext, fbranch, fopen, fnigh)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(fcontext, "TEXT")}
, {sqlite_obj_str(fbranch, "TEXT")}
, {sqlite_obj_str(fopen, "REAL")}
, {sqlite_obj_str(fnigh, "REAL")}
)
;
"""


def create_budheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO bud_idea_healerlink_job (world_id, fisc_tag, owner_name, idea_way, healer_name)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_budprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    rcontext = values_dict.get("rcontext")
    pbranch = values_dict.get("pbranch")
    pnigh = values_dict.get("pnigh")
    popen = values_dict.get("popen")
    pdivisor = values_dict.get("pdivisor")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    return f"""INSERT INTO bud_idea_reason_premiseunit_job (world_id, fisc_tag, owner_name, idea_way, rcontext, pbranch, pnigh, popen, pdivisor, _task, _status)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(pbranch, "TEXT")}
, {sqlite_obj_str(pnigh, "REAL")}
, {sqlite_obj_str(popen, "REAL")}
, {sqlite_obj_str(pdivisor, "REAL")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
)
;
"""


def create_budreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    rcontext = values_dict.get("rcontext")
    rcontext_idea_active_requisite = values_dict.get("rcontext_idea_active_requisite")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    _rcontext_idea_active_value = values_dict.get("_rcontext_idea_active_value")
    return f"""INSERT INTO bud_idea_reasonunit_job (world_id, fisc_tag, owner_name, idea_way, rcontext, rcontext_idea_active_requisite, _task, _status, _rcontext_idea_active_value)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(rcontext_idea_active_requisite, "INTEGER")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_rcontext_idea_active_value, "INTEGER")}
)
;
"""


def create_budlabor_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    labor_label = values_dict.get("labor_label")
    _owner_name_labor = values_dict.get("_owner_name_labor")
    return f"""INSERT INTO bud_idea_laborlink_job (world_id, fisc_tag, owner_name, idea_way, labor_label, _owner_name_labor)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(labor_label, "TEXT")}
, {sqlite_obj_str(_owner_name_labor, "INTEGER")}
)
;
"""


def create_budidea_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("idea_way")
    begin = values_dict.get("begin")
    close = values_dict.get("close")
    addin = values_dict.get("addin")
    numor = values_dict.get("numor")
    denom = values_dict.get("denom")
    morph = values_dict.get("morph")
    gogo_want = values_dict.get("gogo_want")
    stop_want = values_dict.get("stop_want")
    mass = values_dict.get("mass")
    pledge = values_dict.get("pledge")
    problem_bool = values_dict.get("problem_bool")
    _active = values_dict.get("_active")
    _task = values_dict.get("_task")
    fund_coin = values_dict.get("fund_coin")
    _fund_onset = values_dict.get("_fund_onset")
    _fund_cease = values_dict.get("_fund_cease")
    _fund_ratio = values_dict.get("_fund_ratio")
    _gogo_calc = values_dict.get("_gogo_calc")
    _stop_calc = values_dict.get("_stop_calc")
    _level = values_dict.get("_level")
    _range_evaluated = values_dict.get("_range_evaluated")
    _descendant_pledge_count = values_dict.get("_descendant_pledge_count")
    _healerlink_ratio = values_dict.get("_healerlink_ratio")
    _all_acct_cred = values_dict.get("_all_acct_cred")
    _all_acct_debt = values_dict.get("_all_acct_debt")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO bud_ideaunit_job (world_id, fisc_tag, owner_name, idea_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool, fund_coin, _active, _task, _fund_onset, _fund_cease, _fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_pledge_count, _healerlink_ratio, _all_acct_cred, _all_acct_debt)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(begin, real_str)}
, {sqlite_obj_str(close, real_str)}
, {sqlite_obj_str(addin, real_str)}
, {sqlite_obj_str(numor, "INTEGER")}
, {sqlite_obj_str(denom, "INTEGER")}
, {sqlite_obj_str(morph, real_str)}
, {sqlite_obj_str(gogo_want, real_str)}
, {sqlite_obj_str(stop_want, real_str)}
, {sqlite_obj_str(mass, real_str)}
, {sqlite_obj_str(pledge, real_str)}
, {sqlite_obj_str(problem_bool, "INTEGER")}
, {sqlite_obj_str(fund_coin, real_str)}
, {sqlite_obj_str(_active, "INTEGER")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_fund_onset, real_str)}
, {sqlite_obj_str(_fund_cease, real_str)}
, {sqlite_obj_str(_fund_ratio, real_str)}
, {sqlite_obj_str(_gogo_calc, real_str)}
, {sqlite_obj_str(_stop_calc, real_str)}
, {sqlite_obj_str(_level, "INTEGER")}
, {sqlite_obj_str(_range_evaluated, "INTEGER")}
, {sqlite_obj_str(_descendant_pledge_count, "INTEGER")}
, {sqlite_obj_str(_healerlink_ratio, real_str)}
, {sqlite_obj_str(_all_acct_cred, real_str)}
, {sqlite_obj_str(_all_acct_debt, real_str)}
)
;
"""


def create_budunit_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_tag = values_dict.get("fisc_tag")
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
    fund_coin = values_dict.get("fund_coin")
    fund_pool = values_dict.get("fund_pool")
    max_tree_traverse = values_dict.get("max_tree_traverse")
    penny = values_dict.get("penny")
    respect_bit = values_dict.get("respect_bit")
    tally = values_dict.get("tally")

    return f"""INSERT INTO budunit_job (world_id, fisc_tag, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerlink_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_tag, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(credor_respect, real_str)}
, {sqlite_obj_str(debtor_respect, real_str)}
, {sqlite_obj_str(fund_pool, real_str)}
, {sqlite_obj_str(max_tree_traverse, integer_str)}
, {sqlite_obj_str(tally, real_str)}
, {sqlite_obj_str(fund_coin, real_str)}
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
