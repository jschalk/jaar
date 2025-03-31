from src.f00_instrument.dict_toolbox import set_in_nested_dict
from src.f01_road.road import FiscTitle
from src.f10_etl.tran_sqlstrs import get_fisc_fu1_select_sqlstrs
from sqlite3 import Cursor as sqlite3_Cursor


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
