from src.a00_data_toolboxs.dict_toolbox import set_in_nested_dict
from src.a00_data_toolboxs.db_toolbox import sqlite_obj_str
from src.a02_finance_toolboxs.deal import OwnerName, FiscTitle
from src.a01_word_logic.road import RoadUnit, WorldID
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import AwardHeir, GroupUnit, MemberShip
from src.f02_bud.healer import HealerLink
from src.f02_bud.reason_item import ReasonHeir, PremiseUnit, FactHeir
from src.f02_bud.reason_team import TeamHeir
from src.f02_bud.item import ItemUnit
from src.f02_bud.bud import BudUnit
from src.f11_etl.tran_sqlstrs import get_fisc_fu1_select_sqlstrs
from sqlite3 import Cursor as sqlite3_Cursor
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


def get_fisc_dict_from_db(cursor: sqlite3_Cursor, fisc_title: FiscTitle) -> dict:
    """Fetches a FiscUnit's data from multiple tables and returns it as a dictionary."""

    fu1_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_title)
    cursor.execute(fu1_sqlstrs.get("fiscunit"))
    fiscunit_row = cursor.fetchone()
    if not fiscunit_row:
        return None  # fiscunit not found

    timeline_title = fiscunit_row[1]
    c400_number = fiscunit_row[2]
    yr1_jan1_offset = fiscunit_row[3]
    monthday_distortion = fiscunit_row[4]

    fisc_dict: dict[str, any] = {"fisc_title": fiscunit_row[0], "timeline": {}}
    if (
        timeline_title is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_title:
            fisc_dict["timeline"]["timeline_title"] = timeline_title
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
    _set_fisc_dict_fisccash(cursor, fisc_dict, fisc_title)

    cursor.execute(fu1_sqlstrs.get("fisc_dealunit"))
    _set_fisc_dict_fiscdeal(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_hour"))
    _set_fisc_dict_fischour(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_month"))
    _set_fisc_dict_fiscmont(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeline_weekday"))
    _set_fisc_dict_fiscweek(cursor, fisc_dict)

    cursor.execute(fu1_sqlstrs.get("fisc_timeoffi"))
    _set_fisc_dict_timeoffi(cursor, fisc_dict)
    return fisc_dict


def _set_fisc_dict_fisccash(cursor: sqlite3_Cursor, fisc_dict: dict, x_fisc_title: str):
    tranunits_dict = {}
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_owner_name = fisccash_row[1]
        row_acct_name = fisccash_row[2]
        row_tran_time = fisccash_row[3]
        row_amount = fisccash_row[4]
        keylist = [row_owner_name, row_acct_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    cashbook_dict = {"fisc_title": x_fisc_title, "tranunits": tranunits_dict}
    fisc_dict["cashbook"] = cashbook_dict


def _set_fisc_dict_fiscdeal(cursor: sqlite3_Cursor, fisc_dict: dict):
    brokerunits_dict = {}
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_owner_name = fisccash_row[1]
        row_deal_time = fisccash_row[2]
        row_quota = fisccash_row[3]
        row_celldepth = fisccash_row[4]
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


def _set_fisc_dict_fischour(cursor: sqlite3_Cursor, fisc_dict: dict):
    hours_config_list = []
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_cumlative_minute = fisccash_row[1]
        row_hour_title = fisccash_row[2]
        hours_config_list.append([row_hour_title, row_cumlative_minute])
    if hours_config_list:
        fisc_dict["timeline"]["hours_config"] = hours_config_list


def _set_fisc_dict_fiscmont(cursor: sqlite3_Cursor, fisc_dict: dict):
    months_config_list = []
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_cumlative_day = fisccash_row[1]
        row_month_title = fisccash_row[2]
        months_config_list.append([row_month_title, row_cumlative_day])
    if months_config_list:
        fisc_dict["timeline"]["months_config"] = months_config_list


def _set_fisc_dict_fiscweek(cursor: sqlite3_Cursor, fisc_dict: dict):
    weekday_dict = {}
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_weekday_order = fisccash_row[1]
        row_weekday_title = fisccash_row[2]
        weekday_dict[row_weekday_order] = row_weekday_title
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        fisc_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_fisc_dict_timeoffi(cursor: sqlite3_Cursor, fisc_dict: dict):
    offi_times_set = set()
    for fisccash_row in cursor.fetchall():
        row_fisc_title = fisccash_row[0]
        row_offi_time = fisccash_row[1]
        offi_times_set.add(row_offi_time)
    fisc_dict["offi_times"] = list(offi_times_set)


def create_budmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
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
    return f"""INSERT INTO bud_acct_membership_plan (world_id, fisc_title, owner_name, acct_name, group_label, credit_vote, debtit_vote, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
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
    fisc_title = values_dict.get("fisc_title")
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
    return f"""INSERT INTO bud_acctunit_plan (world_id, fisc_title, owner_name, acct_name, credit_belief, debtit_belief, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take, _fund_agenda_ratio_give, _fund_agenda_ratio_take, _inallocable_debtit_belief, _irrational_debtit_belief)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
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
    fisc_title = values_dict.get("fisc_title")
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
    return f"""INSERT INTO bud_groupunit_plan (world_id, fisc_title, owner_name, group_label, fund_coin, bridge, _credor_pool, _debtor_pool, _fund_give, _fund_take, _fund_agenda_give, _fund_agenda_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
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
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    awardee_tag = values_dict.get("awardee_tag")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    _fund_give = values_dict.get("_fund_give")
    _fund_take = values_dict.get("_fund_take")
    return f"""INSERT INTO bud_item_awardlink_plan (world_id, fisc_title, owner_name, road, awardee_tag, give_force, take_force, _fund_give, _fund_take)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(awardee_tag, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(_fund_give, "REAL")}
, {sqlite_obj_str(_fund_take, "REAL")}
)
;
"""


def create_budfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    base = values_dict.get("base")
    pick = values_dict.get("pick")
    fopen = values_dict.get("fopen")
    fnigh = values_dict.get("fnigh")
    return f"""INSERT INTO bud_item_factunit_plan (world_id, fisc_title, owner_name, road, base, pick, fopen, fnigh)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(base, "TEXT")}
, {sqlite_obj_str(pick, "TEXT")}
, {sqlite_obj_str(fopen, "REAL")}
, {sqlite_obj_str(fnigh, "REAL")}
)
;
"""


def create_budheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO bud_item_healerlink_plan (world_id, fisc_title, owner_name, road, healer_name)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
)
;
"""


def create_budprem_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    base = values_dict.get("base")
    need = values_dict.get("need")
    nigh = values_dict.get("nigh")
    open = values_dict.get("open")
    divisor = values_dict.get("divisor")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    return f"""INSERT INTO bud_item_reason_premiseunit_plan (world_id, fisc_title, owner_name, road, base, need, nigh, open, divisor, _task, _status)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(base, "TEXT")}
, {sqlite_obj_str(need, "TEXT")}
, {sqlite_obj_str(nigh, "REAL")}
, {sqlite_obj_str(open, "REAL")}
, {sqlite_obj_str(divisor, "REAL")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
)
;
"""


def create_budreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    base = values_dict.get("base")
    base_item_active_requisite = values_dict.get("base_item_active_requisite")
    _task = values_dict.get("_task")
    _status = values_dict.get("_status")
    _base_item_active_value = values_dict.get("_base_item_active_value")
    return f"""INSERT INTO bud_item_reasonunit_plan (world_id, fisc_title, owner_name, road, base, base_item_active_requisite, _task, _status, _base_item_active_value)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(base, "TEXT")}
, {sqlite_obj_str(base_item_active_requisite, "INTEGER")}
, {sqlite_obj_str(_task, "INTEGER")}
, {sqlite_obj_str(_status, "INTEGER")}
, {sqlite_obj_str(_base_item_active_value, "INTEGER")}
)
;
"""


def create_budteam_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    road = values_dict.get("road")
    team_tag = values_dict.get("team_tag")
    _owner_name_team = values_dict.get("_owner_name_team")
    return f"""INSERT INTO bud_item_teamlink_plan (world_id, fisc_title, owner_name, road, team_tag, _owner_name_team)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(road, "TEXT")}
, {sqlite_obj_str(team_tag, "TEXT")}
, {sqlite_obj_str(_owner_name_team, "INTEGER")}
)
;
"""


def create_buditem_metrics_insert_sqlstr(values_dict: dict[str,]):
    world_id = values_dict.get("world_id")
    fisc_title = values_dict.get("fisc_title")
    owner_name = values_dict.get("owner_name")
    parent_road = values_dict.get("parent_road")
    item_title = values_dict.get("item_title")
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

    return f"""INSERT INTO bud_itemunit_plan (world_id, fisc_title, owner_name, parent_road, item_title, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool, fund_coin, _active, _task, _fund_onset, _fund_cease, _fund_ratio, _gogo_calc, _stop_calc, _level, _range_evaluated, _descendant_pledge_count, _healerlink_ratio, _all_acct_cred, _all_acct_debt)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
, {sqlite_obj_str(owner_name, "TEXT")}
, {sqlite_obj_str(parent_road, "TEXT")}
, {sqlite_obj_str(item_title, "TEXT")}
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
    fisc_title = values_dict.get("fisc_title")
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

    return f"""INSERT INTO budunit_plan (world_id, fisc_title, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit, _rational, _keeps_justified, _offtrack_fund, _sum_healerlink_share, _keeps_buildable, _tree_traverse_count)
VALUES (
  {sqlite_obj_str(world_id, "TEXT")}
, {sqlite_obj_str(fisc_title, "TEXT")}
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
    world_id: WorldID = None
    fisc_title: FiscTitle = None
    owner_name: OwnerName = None
    road: RoadUnit = None
    base: RoadUnit = None
    acct_name: AcctUnit = None
    membership: GroupUnit = None
    group_name: GroupUnit = None
    fact_road: RoadUnit = None


def insert_plan_budmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budacct(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_acct: AcctUnit,
):
    x_dict = copy_deepcopy(x_acct.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budacct_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budgrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_budgrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerLink,
):
    x_dict = {
        "world_id": x_objkeysholder.world_id,
        "fisc_title": x_objkeysholder.fisc_title,
        "owner_name": x_objkeysholder.owner_name,
        "road": x_objkeysholder.road,
    }
    for healer_name in sorted(x_healer._healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_budheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_plan_budprem(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_premiseunit: PremiseUnit,
):
    x_dict = copy_deepcopy(x_premiseunit.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    x_dict["base"] = x_objkeysholder.base
    insert_sqlstr = create_budprem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    insert_sqlstr = create_budreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budteam(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_teamheir: TeamHeir,
):
    x_dict = copy_deepcopy(x_teamheir.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["fisc_title"] = x_objkeysholder.fisc_title
    x_dict["owner_name"] = x_objkeysholder.owner_name
    x_dict["road"] = x_objkeysholder.road
    for team_tag in sorted(x_teamheir._teamlinks):
        x_dict["team_tag"] = team_tag
        insert_sqlstr = create_budteam_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_plan_buditem(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_item: ItemUnit
):
    x_dict = copy_deepcopy(x_item.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    x_dict["owner_name"] = x_objkeysholder.owner_name
    insert_sqlstr = create_buditem_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_budunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_bud: BudUnit
):
    x_dict = copy_deepcopy(x_bud.__dict__)
    x_dict["world_id"] = x_objkeysholder.world_id
    insert_sqlstr = create_budunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_plan_obj(cursor: sqlite3_Cursor, world_id: WorldID, plan_bud: BudUnit):
    plan_bud.settle_bud()
    x_objkeysholder = ObjKeysHolder(world_id, plan_bud.fisc_title, plan_bud.owner_name)
    insert_plan_budunit(cursor, x_objkeysholder, plan_bud)
    for x_item in plan_bud.get_item_dict().values():
        x_objkeysholder.road = x_item.get_road()
        healerlink = x_item.healerlink
        teamheir = x_item._teamheir
        insert_plan_buditem(cursor, x_objkeysholder, x_item)
        insert_plan_budheal(cursor, x_objkeysholder, healerlink)
        insert_plan_budteam(cursor, x_objkeysholder, teamheir)
        for x_awardheir in x_item._awardheirs.values():
            insert_plan_budawar(cursor, x_objkeysholder, x_awardheir)
        for base, reasonheir in x_item._reasonheirs.items():
            insert_plan_budreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.base = base
            for prem in reasonheir.premises.values():
                insert_plan_budprem(cursor, x_objkeysholder, prem)

    for x_acct in plan_bud.accts.values():
        insert_plan_budacct(cursor, x_objkeysholder, x_acct)
        for x_membership in x_acct._memberships.values():
            insert_plan_budmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in plan_bud._groupunits.values():
        insert_plan_budgrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in plan_bud.itemroot._factheirs.values():
        x_objkeysholder.fact_road = plan_bud.itemroot.get_road()
        insert_plan_budfact(cursor, x_objkeysholder, x_factheir)
