from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a11_bud_logic.bud import BeliefLabel
from src.a18_etl_toolbox.tran_sqlstrs import get_belief_voice_select1_sqlstrs


def get_belief_dict_from_voice_tables(
    cursor: sqlite3_Cursor, belief_label: BeliefLabel
) -> dict:
    fu1_sqlstrs = get_belief_voice_select1_sqlstrs(belief_label)
    return get_belief_dict_from_sqlstrs(cursor, fu1_sqlstrs, belief_label)


def get_belief_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], belief_label: BeliefLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("beliefunit"))
    beliefunit_row = cursor.fetchone()
    if not beliefunit_row:
        return None  # beliefunit not found

    timeline_label = beliefunit_row[1]
    c400_number = beliefunit_row[2]
    yr1_jan1_offset = beliefunit_row[3]
    monthday_distortion = beliefunit_row[4]

    belief_dict: dict[str, any] = {"belief_label": beliefunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            belief_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            belief_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            belief_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            belief_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_iota := beliefunit_row[5]:
        belief_dict["fund_iota"] = fund_iota
    if penny := beliefunit_row[6]:
        belief_dict["penny"] = penny
    if respect_bit := beliefunit_row[7]:
        belief_dict["respect_bit"] = respect_bit
    if knot := beliefunit_row[8]:
        belief_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("belief_paybook"))
    _set_belief_dict_blfpayy(cursor, belief_dict, belief_label)

    cursor.execute(fu1_sqlstrs.get("belief_budunit"))
    _set_belief_dict_beliefbud(cursor, belief_dict)

    cursor.execute(fu1_sqlstrs.get("belief_timeline_hour"))
    _set_belief_dict_blfhour(cursor, belief_dict)

    cursor.execute(fu1_sqlstrs.get("belief_timeline_month"))
    _set_belief_dict_blfmont(cursor, belief_dict)

    cursor.execute(fu1_sqlstrs.get("belief_timeline_weekday"))
    _set_belief_dict_blfweek(cursor, belief_dict)

    cursor.execute(fu1_sqlstrs.get("belief_timeoffi"))
    _set_belief_dict_timeoffi(cursor, belief_dict)
    return belief_dict


def _set_belief_dict_blfpayy(
    cursor: sqlite3_Cursor, belief_dict: dict, x_belief_label: str
):
    tranunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_believer_name = blfpayy_row[1]
        row_acct_name = blfpayy_row[2]
        row_tran_time = blfpayy_row[3]
        row_amount = blfpayy_row[4]
        keylist = [row_believer_name, row_acct_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"belief_label": x_belief_label, "tranunits": tranunits_dict}
    belief_dict["paybook"] = paybook_dict


def _set_belief_dict_beliefbud(cursor: sqlite3_Cursor, belief_dict: dict):
    brokerunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_believer_name = blfpayy_row[1]
        row_bud_time = blfpayy_row[2]
        row_quota = blfpayy_row[3]
        row_celldepth = blfpayy_row[4]
        believer_keylist = [row_believer_name, "believer_name"]
        set_in_nested_dict(brokerunits_dict, believer_keylist, row_believer_name)
        keylist = [row_believer_name, "buds", row_bud_time]
        bud_timepoint_dict = {
            "bud_time": row_bud_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(brokerunits_dict, keylist, bud_timepoint_dict)
    belief_dict["brokerunits"] = brokerunits_dict


def _set_belief_dict_blfhour(cursor: sqlite3_Cursor, belief_dict: dict):
    hours_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_cumulative_minute = blfpayy_row[1]
        row_hour_label = blfpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        belief_dict["timeline"]["hours_config"] = hours_config_list


def _set_belief_dict_blfmont(cursor: sqlite3_Cursor, belief_dict: dict):
    months_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_cumulative_day = blfpayy_row[1]
        row_month_label = blfpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        belief_dict["timeline"]["months_config"] = months_config_list


def _set_belief_dict_blfweek(cursor: sqlite3_Cursor, belief_dict: dict):
    weekday_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_weekday_order = blfpayy_row[1]
        row_weekday_label = blfpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        belief_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_belief_dict_timeoffi(cursor: sqlite3_Cursor, belief_dict: dict):
    offi_times_set = set()
    for blfpayy_row in cursor.fetchall():
        row_belief_label = blfpayy_row[0]
        row_offi_time = blfpayy_row[1]
        offi_times_set.add(row_offi_time)
    belief_dict["offi_times"] = list(offi_times_set)
