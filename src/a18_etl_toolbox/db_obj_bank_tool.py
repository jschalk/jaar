from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a02_finance_logic.bud import BankLabel
from src.a18_etl_toolbox.tran_sqlstrs import get_bank_voice_select1_sqlstrs


def get_bank_dict_from_voice_tables(
    cursor: sqlite3_Cursor, bank_label: BankLabel
) -> dict:
    fu1_sqlstrs = get_bank_voice_select1_sqlstrs(bank_label)
    return get_bank_dict_from_sqlstrs(cursor, fu1_sqlstrs, bank_label)


def get_bank_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], bank_label: BankLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("bankunit"))
    bankunit_row = cursor.fetchone()
    if not bankunit_row:
        return None  # bankunit not found

    timeline_label = bankunit_row[1]
    c400_number = bankunit_row[2]
    yr1_jan1_offset = bankunit_row[3]
    monthday_distortion = bankunit_row[4]

    bank_dict: dict[str, any] = {"bank_label": bankunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            bank_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            bank_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            bank_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            bank_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_iota := bankunit_row[5]:
        bank_dict["fund_iota"] = fund_iota
    if penny := bankunit_row[6]:
        bank_dict["penny"] = penny
    if respect_bit := bankunit_row[7]:
        bank_dict["respect_bit"] = respect_bit
    if knot := bankunit_row[8]:
        bank_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("bank_paybook"))
    _set_bank_dict_bnkpayy(cursor, bank_dict, bank_label)

    cursor.execute(fu1_sqlstrs.get("bank_budunit"))
    _set_bank_dict_bankbud(cursor, bank_dict)

    cursor.execute(fu1_sqlstrs.get("bank_timeline_hour"))
    _set_bank_dict_bnkhour(cursor, bank_dict)

    cursor.execute(fu1_sqlstrs.get("bank_timeline_month"))
    _set_bank_dict_bnkmont(cursor, bank_dict)

    cursor.execute(fu1_sqlstrs.get("bank_timeline_weekday"))
    _set_bank_dict_bnkweek(cursor, bank_dict)

    cursor.execute(fu1_sqlstrs.get("bank_timeoffi"))
    _set_bank_dict_timeoffi(cursor, bank_dict)
    return bank_dict


def _set_bank_dict_bnkpayy(cursor: sqlite3_Cursor, bank_dict: dict, x_bank_label: str):
    tranunits_dict = {}
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_owner_name = bnkpayy_row[1]
        row_acct_name = bnkpayy_row[2]
        row_tran_time = bnkpayy_row[3]
        row_amount = bnkpayy_row[4]
        keylist = [row_owner_name, row_acct_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"bank_label": x_bank_label, "tranunits": tranunits_dict}
    bank_dict["paybook"] = paybook_dict


def _set_bank_dict_bankbud(cursor: sqlite3_Cursor, bank_dict: dict):
    brokerunits_dict = {}
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_owner_name = bnkpayy_row[1]
        row_bud_time = bnkpayy_row[2]
        row_quota = bnkpayy_row[3]
        row_celldepth = bnkpayy_row[4]
        owner_keylist = [row_owner_name, "owner_name"]
        set_in_nested_dict(brokerunits_dict, owner_keylist, row_owner_name)
        keylist = [row_owner_name, "buds", row_bud_time]
        bud_timepoint_dict = {
            "bud_time": row_bud_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(brokerunits_dict, keylist, bud_timepoint_dict)
    bank_dict["brokerunits"] = brokerunits_dict


def _set_bank_dict_bnkhour(cursor: sqlite3_Cursor, bank_dict: dict):
    hours_config_list = []
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_cumulative_minute = bnkpayy_row[1]
        row_hour_label = bnkpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        bank_dict["timeline"]["hours_config"] = hours_config_list


def _set_bank_dict_bnkmont(cursor: sqlite3_Cursor, bank_dict: dict):
    months_config_list = []
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_cumulative_day = bnkpayy_row[1]
        row_month_label = bnkpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        bank_dict["timeline"]["months_config"] = months_config_list


def _set_bank_dict_bnkweek(cursor: sqlite3_Cursor, bank_dict: dict):
    weekday_dict = {}
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_weekday_order = bnkpayy_row[1]
        row_weekday_label = bnkpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        bank_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_bank_dict_timeoffi(cursor: sqlite3_Cursor, bank_dict: dict):
    offi_times_set = set()
    for bnkpayy_row in cursor.fetchall():
        row_bank_label = bnkpayy_row[0]
        row_offi_time = bnkpayy_row[1]
        offi_times_set.add(row_offi_time)
    bank_dict["offi_times"] = list(offi_times_set)
