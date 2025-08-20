from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a11_bud_logic.bud import MomentLabel
from src.a18_etl_toolbox.tran_sqlstrs import get_moment_voice_select1_sqlstrs


def get_moment_dict_from_voice_tables(
    cursor: sqlite3_Cursor, moment_label: MomentLabel
) -> dict:
    fu1_sqlstrs = get_moment_voice_select1_sqlstrs(moment_label)
    return get_moment_dict_from_sqlstrs(cursor, fu1_sqlstrs, moment_label)


def get_moment_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], moment_label: MomentLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("momentunit"))
    momentunit_row = cursor.fetchone()
    if not momentunit_row:
        return None  # momentunit not found

    timeline_label = momentunit_row[1]
    c400_number = momentunit_row[2]
    yr1_jan1_offset = momentunit_row[3]
    monthday_distortion = momentunit_row[4]

    moment_dict: dict[str, any] = {"moment_label": momentunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            moment_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            moment_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            moment_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            moment_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_iota := momentunit_row[5]:
        moment_dict["fund_iota"] = fund_iota
    if penny := momentunit_row[6]:
        moment_dict["penny"] = penny
    if respect_bit := momentunit_row[7]:
        moment_dict["respect_bit"] = respect_bit
    if knot := momentunit_row[8]:
        moment_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("moment_paybook"))
    _set_moment_dict_blfpayy(cursor, moment_dict, moment_label)

    cursor.execute(fu1_sqlstrs.get("moment_budunit"))
    _set_moment_dict_momentbud(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeline_hour"))
    _set_moment_dict_blfhour(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeline_month"))
    _set_moment_dict_blfmont(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeline_weekday"))
    _set_moment_dict_blfweek(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeoffi"))
    _set_moment_dict_timeoffi(cursor, moment_dict)
    return moment_dict


def _set_moment_dict_blfpayy(
    cursor: sqlite3_Cursor, moment_dict: dict, x_moment_label: str
):
    tranunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_belief_name = blfpayy_row[1]
        row_partner_name = blfpayy_row[2]
        row_tran_time = blfpayy_row[3]
        row_amount = blfpayy_row[4]
        keylist = [row_belief_name, row_partner_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"moment_label": x_moment_label, "tranunits": tranunits_dict}
    moment_dict["paybook"] = paybook_dict


def _set_moment_dict_momentbud(cursor: sqlite3_Cursor, moment_dict: dict):
    brokerunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_belief_name = blfpayy_row[1]
        row_bud_time = blfpayy_row[2]
        row_quota = blfpayy_row[3]
        row_celldepth = blfpayy_row[4]
        belief_keylist = [row_belief_name, "belief_name"]
        set_in_nested_dict(brokerunits_dict, belief_keylist, row_belief_name)
        keylist = [row_belief_name, "buds", row_bud_time]
        bud_timepoint_dict = {
            "bud_time": row_bud_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(brokerunits_dict, keylist, bud_timepoint_dict)
    moment_dict["brokerunits"] = brokerunits_dict


def _set_moment_dict_blfhour(cursor: sqlite3_Cursor, moment_dict: dict):
    hours_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_cumulative_minute = blfpayy_row[1]
        row_hour_label = blfpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        moment_dict["timeline"]["hours_config"] = hours_config_list


def _set_moment_dict_blfmont(cursor: sqlite3_Cursor, moment_dict: dict):
    months_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_cumulative_day = blfpayy_row[1]
        row_month_label = blfpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        moment_dict["timeline"]["months_config"] = months_config_list


def _set_moment_dict_blfweek(cursor: sqlite3_Cursor, moment_dict: dict):
    weekday_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_weekday_order = blfpayy_row[1]
        row_weekday_label = blfpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        moment_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_moment_dict_timeoffi(cursor: sqlite3_Cursor, moment_dict: dict):
    offi_times_set = set()
    for blfpayy_row in cursor.fetchall():
        row_moment_label = blfpayy_row[0]
        row_offi_time = blfpayy_row[1]
        offi_times_set.add(row_offi_time)
    moment_dict["offi_times"] = list(offi_times_set)
