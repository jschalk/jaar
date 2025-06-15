from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a02_finance_logic.deal import VowLabel
from src.a18_etl_toolbox.tran_sqlstrs import get_vow_voice_select1_sqlstrs


def get_vow_dict_from_voice_tables(cursor: sqlite3_Cursor, vow_label: VowLabel) -> dict:
    fu1_sqlstrs = get_vow_voice_select1_sqlstrs(vow_label)
    return get_vow_dict_from_sqlstrs(cursor, fu1_sqlstrs, vow_label)


def get_vow_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], vow_label: VowLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("vowunit"))
    vowunit_row = cursor.fetchone()
    if not vowunit_row:
        return None  # vowunit not found

    timeline_label = vowunit_row[1]
    c400_number = vowunit_row[2]
    yr1_jan1_offset = vowunit_row[3]
    monthday_distortion = vowunit_row[4]

    vow_dict: dict[str, any] = {"vow_label": vowunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            vow_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            vow_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            vow_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            vow_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_iota := vowunit_row[5]:
        vow_dict["fund_iota"] = fund_iota
    if penny := vowunit_row[6]:
        vow_dict["penny"] = penny
    if respect_bit := vowunit_row[7]:
        vow_dict["respect_bit"] = respect_bit
    if knot := vowunit_row[8]:
        vow_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("vow_paybook"))
    _set_vow_dict_vowpayy(cursor, vow_dict, vow_label)

    cursor.execute(fu1_sqlstrs.get("vow_dealunit"))
    _set_vow_dict_vowdeal(cursor, vow_dict)

    cursor.execute(fu1_sqlstrs.get("vow_timeline_hour"))
    _set_vow_dict_vowhour(cursor, vow_dict)

    cursor.execute(fu1_sqlstrs.get("vow_timeline_month"))
    _set_vow_dict_vowmont(cursor, vow_dict)

    cursor.execute(fu1_sqlstrs.get("vow_timeline_weekday"))
    _set_vow_dict_vowweek(cursor, vow_dict)

    cursor.execute(fu1_sqlstrs.get("vow_timeoffi"))
    _set_vow_dict_timeoffi(cursor, vow_dict)
    return vow_dict


def _set_vow_dict_vowpayy(cursor: sqlite3_Cursor, vow_dict: dict, x_vow_label: str):
    tranunits_dict = {}
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_owner_name = vowpayy_row[1]
        row_acct_name = vowpayy_row[2]
        row_tran_time = vowpayy_row[3]
        row_amount = vowpayy_row[4]
        keylist = [row_owner_name, row_acct_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"vow_label": x_vow_label, "tranunits": tranunits_dict}
    vow_dict["paybook"] = paybook_dict


def _set_vow_dict_vowdeal(cursor: sqlite3_Cursor, vow_dict: dict):
    brokerunits_dict = {}
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_owner_name = vowpayy_row[1]
        row_deal_time = vowpayy_row[2]
        row_quota = vowpayy_row[3]
        row_celldepth = vowpayy_row[4]
        owner_keylist = [row_owner_name, "owner_name"]
        set_in_nested_dict(brokerunits_dict, owner_keylist, row_owner_name)
        keylist = [row_owner_name, "deals", row_deal_time]
        deal_timepoint_dict = {
            "deal_time": row_deal_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(brokerunits_dict, keylist, deal_timepoint_dict)
    vow_dict["brokerunits"] = brokerunits_dict


def _set_vow_dict_vowhour(cursor: sqlite3_Cursor, vow_dict: dict):
    hours_config_list = []
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_cumlative_minute = vowpayy_row[1]
        row_hour_label = vowpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumlative_minute])
    if hours_config_list:
        vow_dict["timeline"]["hours_config"] = hours_config_list


def _set_vow_dict_vowmont(cursor: sqlite3_Cursor, vow_dict: dict):
    months_config_list = []
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_cumlative_day = vowpayy_row[1]
        row_month_label = vowpayy_row[2]
        months_config_list.append([row_month_label, row_cumlative_day])
    if months_config_list:
        vow_dict["timeline"]["months_config"] = months_config_list


def _set_vow_dict_vowweek(cursor: sqlite3_Cursor, vow_dict: dict):
    weekday_dict = {}
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_weekday_order = vowpayy_row[1]
        row_weekday_label = vowpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        vow_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_vow_dict_timeoffi(cursor: sqlite3_Cursor, vow_dict: dict):
    offi_times_set = set()
    for vowpayy_row in cursor.fetchall():
        row_vow_label = vowpayy_row[0]
        row_offi_time = vowpayy_row[1]
        offi_times_set.add(row_offi_time)
    vow_dict["offi_times"] = list(offi_times_set)
