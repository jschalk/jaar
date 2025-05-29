from src.a00_data_toolbox.db_toolbox import sqlite_obj_str
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a01_way_logic.way import OwnerName, WayStr, AcctName, GroupTitle
from src.a02_finance_logic.deal import FiscLabel, OwnerName
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import MemberShip, GroupUnit, AwardHeir
from src.a04_reason_logic.reason_concept import FactHeir, PremiseUnit, ReasonHeir
from src.a04_reason_logic.reason_labor import LaborHeir
from src.a05_concept_logic.concept import HealerLink, ConceptUnit
from src.a06_bud_logic.bud import BudUnit
from src.a18_etl_toolbox.tran_sqlstrs import get_fisc_voice_select1_sqlstrs
from sqlite3 import Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


def get_fisc_dict_from_voice_tables(
    cursor: sqlite3_Cursor, fisc_label: FiscLabel
) -> dict:
    fu1_sqlstrs = get_fisc_voice_select1_sqlstrs(fisc_label)
    return get_fisc_dict_from_sqlstrs(cursor, fu1_sqlstrs, fisc_label)


def get_fisc_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], fisc_label: FiscLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("fiscunit"))
    fiscunit_row = cursor.fetchone()
    if not fiscunit_row:
        return None  # fiscunit not found

    timeline_label = fiscunit_row[1]
    c400_number = fiscunit_row[2]
    yr1_jan1_offset = fiscunit_row[3]
    monthday_distortion = fiscunit_row[4]

    fisc_dict: dict[str, any] = {"fisc_label": fiscunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            fisc_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            fisc_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            fisc_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            fisc_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_coin := fiscunit_row[5]:
        fisc_dict["fund_coin"] = fund_coin
    if penny := fiscunit_row[6]:
        fisc_dict["penny"] = penny
    if respect_bit := fiscunit_row[7]:
        fisc_dict["respect_bit"] = respect_bit
    if bridge := fiscunit_row[8]:
        fisc_dict["bridge"] = bridge

    cursor.execute(fu1_sqlstrs.get("fisc_cashbook"))
    _set_fisc_dict_fiscash(cursor, fisc_dict, fisc_label)

    cursor.execute(fu1_sqlstrs.get("fisc_dealunit"))
    _set_fisc_dict_fisdeal(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_hour"))
    _set_fisc_dict_fishour(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_month"))
    _set_fisc_dict_fismont(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_weekday"))
    _set_fisc_dict_fisweek(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeoffi"))
    _set_fisc_dict_timeoffi(cursor, fisc_dict)
    return fisc_dict


def _set_fisc_dict_fiscash(cursor: sqlite3_Cursor, fisc_dict: dict, x_fisc_label: str):
    tranunits_dict = {}
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_owner_name = fiscash_row[1]
        row_acct_name = fiscash_row[2]
        row_tran_time = fiscash_row[3]
        row_amount = fiscash_row[4]
        keylist = [row_owner_name, row_acct_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    cashbook_dict = {"fisc_label": x_fisc_label, "tranunits": tranunits_dict}
    fisc_dict["cashbook"] = cashbook_dict


def _set_fisc_dict_fisdeal(cursor: sqlite3_Cursor, fisc_dict: dict):
    brokerunits_dict = {}
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_owner_name = fiscash_row[1]
        row_deal_time = fiscash_row[2]
        row_quota = fiscash_row[3]
        row_celldepth = fiscash_row[4]
        owner_keylist = [row_owner_name, "owner_name"]
        set_in_nested_dict(brokerunits_dict, owner_keylist, row_owner_name)
        keylist = [row_owner_name, "deals", row_deal_time]
        deal_timepoint_dict = {
            "deal_time": row_deal_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(brokerunits_dict, keylist, deal_timepoint_dict)
    fisc_dict["brokerunits"] = brokerunits_dict


def _set_fisc_dict_fishour(cursor: sqlite3_Cursor, fisc_dict: dict):
    hours_config_list = []
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_cumlative_minute = fiscash_row[1]
        row_hour_label = fiscash_row[2]
        hours_config_list.append([row_hour_label, row_cumlative_minute])
    if hours_config_list:
        fisc_dict["timeline"]["hours_config"] = hours_config_list


def _set_fisc_dict_fismont(cursor: sqlite3_Cursor, fisc_dict: dict):
    months_config_list = []
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_cumlative_day = fiscash_row[1]
        row_month_label = fiscash_row[2]
        months_config_list.append([row_month_label, row_cumlative_day])
    if months_config_list:
        fisc_dict["timeline"]["months_config"] = months_config_list


def _set_fisc_dict_fisweek(cursor: sqlite3_Cursor, fisc_dict: dict):
    weekday_dict = {}
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_weekday_order = fiscash_row[1]
        row_weekday_label = fiscash_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        fisc_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_fisc_dict_timeoffi(cursor: sqlite3_Cursor, fisc_dict: dict):
    offi_times_set = set()
    for fiscash_row in cursor.fetchall():
        row_fisc_label = fiscash_row[0]
        row_offi_time = fiscash_row[1]
        offi_times_set.add(row_offi_time)
    fisc_dict["offi_times"] = list(offi_times_set)


def get_pidgin_dict_from_db(cursor: sqlite3_Cursor) -> dict[str,]:
    return {}


def create_budmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    acct_name = values_dict.get("acct_name")
    group_title = values_dict.get("group_title")
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
    return f"""INSERT INTO bud_acct_membership_job (fisc_label, owner_name, acct_name, group_title, credit_vote, debtit_vote, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(acct_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
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
    fisc_label = values_dict.get("fisc_label")
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
    return f"""INSERT INTO bud_acctunit_job (fisc_label, owner_name, acct_name, credit_belief, debtit_belief, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take, _inallocable_debtit_belief, _irrational_debtit_belief)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
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
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    group_title = values_dict.get("group_title")
    _credor_pool = values_dict.get("_credor_pool")
    _debtor_pool = values_dict.get("_debtor_pool")
    fund_coin = values_dict.get("fund_coin")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    _fund_agenda_give = values_dict.get("_fund_agenda_give")
    _fund_agenda_take = values_dict.get("_fund_agenda_take")
    bridge = values_dict.get("bridge")
    real_str = "REAL"
    return f"""INSERT INTO bud_groupunit_job (fisc_label, owner_name, group_title, fund_coin, bridge, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
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
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    awardee_title = values_dict.get("awardee_title")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    return f"""INSERT INTO bud_concept_awardlink_job (fisc_label, owner_name, concept_way, awardee_title, give_force, take_force, _fund_give, _fund_take)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(awardee_title, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(_fund_give, "REAL")}
, {sqlite_obj_str(_fund_take, "REAL")}
)
;
"""


def create_budfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    fcontext = values_dict.get("fcontext")
    fstate = values_dict.get("fstate")
    fopen = values_dict.get("fopen")
    fnigh = values_dict.get("fnigh")
    return f"""INSERT INTO bud_concept_factunit_job (fisc_label, owner_name, concept_way, fcontext, fstate, fopen, fnigh)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(fcontext, "TEXT")}
, {sqlite_obj_str(fstate, "TEXT")}
, {sqlite_obj_str(fopen, "REAL")}
, {sqlite_obj_str(fnigh, "REAL")}
)
;
"""


def create_budheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO bud_concept_healerlink_job (fisc_label, owner_name, concept_way, healer_name)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_budprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    rcontext = values_dict.get("rcontext")
    pstate = values_dict.get("pstate")
    pnigh = values_dict.get("pnigh")
    popen = values_dict.get("popen")
    pdivisor = values_dict.get("pdivisor")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    return f"""INSERT INTO bud_concept_reason_premiseunit_job (fisc_label, owner_name, concept_way, rcontext, pstate, pnigh, popen, pdivisor, _task, _status)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(pstate, "TEXT")}
, {sqlite_obj_str(pnigh, "REAL")}
, {sqlite_obj_str(popen, "REAL")}
, {sqlite_obj_str(pdivisor, "REAL")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
)
;
"""


def create_budreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    rcontext = values_dict.get("rcontext")
    rconcept_active_requisite = values_dict.get("rconcept_active_requisite")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    _rcontext_concept_active_value = values_dict.get("_rcontext_concept_active_value")
    return f"""INSERT INTO bud_concept_reasonunit_job (fisc_label, owner_name, concept_way, rcontext, rconcept_active_requisite, _task, _status, _rcontext_concept_active_value)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(rcontext, "TEXT")}
, {sqlite_obj_str(rconcept_active_requisite, "INTEGER")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_rcontext_concept_active_value, "INTEGER")}
)
;
"""


def create_budlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
    labor_title = values_dict.get("labor_title")
    _owner_name_labor = values_dict.get("_owner_name_labor")
    return f"""INSERT INTO bud_concept_laborlink_job (fisc_label, owner_name, concept_way, labor_title, _owner_name_labor)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(way, "TEXT")}
, {sqlite_obj_str(labor_title, "TEXT")}
, {sqlite_obj_str(_owner_name_labor, "INTEGER")}
)
;
"""


def create_budconc_metrics_insert_sqlstr(values_dict: dict[str,]):
    fisc_label = values_dict.get("fisc_label")
    owner_name = values_dict.get("owner_name")
    way = values_dict.get("concept_way")
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

    return f"""INSERT INTO bud_conceptunit_job (fisc_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool, fund_coin, _active, _task, _fund_onset, _fund_cease, _fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_pledge_count, _healerlink_ratio, _all_acct_cred, _all_acct_debt)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
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
    fisc_label = values_dict.get("fisc_label")
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

    return f"""INSERT INTO budunit_job (fisc_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerlink_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(fisc_label, "TEXT")}
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


@dataclass
class ObjKeysHolder:
    fisc_label: FiscLabel = None
    owner_name: OwnerName = None
    way: WayStr = None
    rcontext: WayStr = None
    acct_name: AcctName = None
    membership: GroupTitle = None
    group_name: GroupTitle = None
    fact_way: WayStr = None


def insert_job_budmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budacct(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_acct: AcctUnit,
):
    x_dict = copy_deepcopy(x_acct.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budacct_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budgrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budgrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "fisc_label": x_objkeysholder.fisc_label,
        "owner_name": x_objkeysholder.owner_name,
        "concept_way": x_objkeysholder.way,
    }
    for healer_name in sorted(x_healer._healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_budheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_budprem(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_premiseunit: PremiseUnit,
):
    x_dict = copy_deepcopy(x_premiseunit.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    x_dict["rcontext"] = x_objkeysholder.rcontext
    insert_sqlstr = create_budprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    insert_sqlstr = create_budreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_laborheir: LaborHeir,
):
    x_dict = copy_deepcopy(x_laborheir.__dict__)
    x_dict["fisc_label"] = x_objkeysholder.fisc_label
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["concept_way"] = x_objkeysholder.way
    for labor_title in sorted(x_laborheir._laborlinks):
        x_dict["labor_title"] = labor_title
        insert_sqlstr = create_budlabo_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_budconc(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_concept: ConceptUnit
):
    x_dict = copy_deepcopy(x_concept.__dict__)
    x_dict["concept_way"] = x_concept.get_concept_way()
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budconc_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_budunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_bud: BudUnit
):
    x_dict = copy_deepcopy(x_bud.__dict__)
    insert_sqlstr = create_budunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, job_bud: BudUnit):
    job_bud.settle_bud()
    x_objkeysholder = ObjKeysHolder(job_bud.fisc_label, job_bud.owner_name)
    insert_job_budunit(cursor, x_objkeysholder, job_bud)
    for x_concept in job_bud.get_concept_dict().values():
        x_objkeysholder.way = x_concept.get_concept_way()
        healerlink = x_concept.healerlink
        laborheir = x_concept._laborheir
        insert_job_budconc(cursor, x_objkeysholder, x_concept)
        insert_job_budheal(cursor, x_objkeysholder, healerlink)
        insert_job_budlabo(cursor, x_objkeysholder, laborheir)
        for x_awardheir in x_concept._awardheirs.values():
            insert_job_budawar(cursor, x_objkeysholder, x_awardheir)
        for rcontext, reasonheir in x_concept._reasonheirs.items():
            insert_job_budreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.rcontext = rcontext
            for prem in reasonheir.premises.values():
                insert_job_budprem(cursor, x_objkeysholder, prem)

    for x_acct in job_bud.accts.values():
        insert_job_budacct(cursor, x_objkeysholder, x_acct)
        for x_membership in x_acct._memberships.values():
            insert_job_budmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_bud._groupunits.values():
        insert_job_budgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_bud.conceptroot._factheirs.values():
        x_objkeysholder.fact_way = job_bud.conceptroot.get_concept_way()
        insert_job_budfact(cursor, x_objkeysholder, x_factheir)
