from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a11_bud_logic.bud import CoinLabel
from src.a18_etl_toolbox.tran_sqlstrs import get_coin_voice_select1_sqlstrs


def get_coin_dict_from_voice_tables(
    cursor: sqlite3_Cursor, coin_label: CoinLabel
) -> dict:
    fu1_sqlstrs = get_coin_voice_select1_sqlstrs(coin_label)
    return get_coin_dict_from_sqlstrs(cursor, fu1_sqlstrs, coin_label)


def get_coin_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], coin_label: CoinLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("coinunit"))
    coinunit_row = cursor.fetchone()
    if not coinunit_row:
        return None  # coinunit not found

    timeline_label = coinunit_row[1]
    c400_number = coinunit_row[2]
    yr1_jan1_offset = coinunit_row[3]
    monthday_distortion = coinunit_row[4]

    coin_dict: dict[str, any] = {"coin_label": coinunit_row[0], "timeline": {}}
    if (
        timeline_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_distortion is not None
    ):
        if timeline_label:
            coin_dict["timeline"]["timeline_label"] = timeline_label
        if c400_number:
            coin_dict["timeline"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            coin_dict["timeline"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_distortion:
            coin_dict["timeline"]["monthday_distortion"] = monthday_distortion

    if fund_iota := coinunit_row[5]:
        coin_dict["fund_iota"] = fund_iota
    if penny := coinunit_row[6]:
        coin_dict["penny"] = penny
    if respect_bit := coinunit_row[7]:
        coin_dict["respect_bit"] = respect_bit
    if knot := coinunit_row[8]:
        coin_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("coin_paybook"))
    _set_coin_dict_blfpayy(cursor, coin_dict, coin_label)

    cursor.execute(fu1_sqlstrs.get("coin_budunit"))
    _set_coin_dict_coinbud(cursor, coin_dict)

    cursor.execute(fu1_sqlstrs.get("coin_timeline_hour"))
    _set_coin_dict_blfhour(cursor, coin_dict)

    cursor.execute(fu1_sqlstrs.get("coin_timeline_month"))
    _set_coin_dict_blfmont(cursor, coin_dict)

    cursor.execute(fu1_sqlstrs.get("coin_timeline_weekday"))
    _set_coin_dict_blfweek(cursor, coin_dict)

    cursor.execute(fu1_sqlstrs.get("coin_timeoffi"))
    _set_coin_dict_timeoffi(cursor, coin_dict)
    return coin_dict


def _set_coin_dict_blfpayy(cursor: sqlite3_Cursor, coin_dict: dict, x_coin_label: str):
    tranunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
        row_belief_name = blfpayy_row[1]
        row_partner_name = blfpayy_row[2]
        row_tran_time = blfpayy_row[3]
        row_amount = blfpayy_row[4]
        keylist = [row_belief_name, row_partner_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"coin_label": x_coin_label, "tranunits": tranunits_dict}
    coin_dict["paybook"] = paybook_dict


def _set_coin_dict_coinbud(cursor: sqlite3_Cursor, coin_dict: dict):
    brokerunits_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
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
    coin_dict["brokerunits"] = brokerunits_dict


def _set_coin_dict_blfhour(cursor: sqlite3_Cursor, coin_dict: dict):
    hours_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
        row_cumulative_minute = blfpayy_row[1]
        row_hour_label = blfpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        coin_dict["timeline"]["hours_config"] = hours_config_list


def _set_coin_dict_blfmont(cursor: sqlite3_Cursor, coin_dict: dict):
    months_config_list = []
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
        row_cumulative_day = blfpayy_row[1]
        row_month_label = blfpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        coin_dict["timeline"]["months_config"] = months_config_list


def _set_coin_dict_blfweek(cursor: sqlite3_Cursor, coin_dict: dict):
    weekday_dict = {}
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
        row_weekday_order = blfpayy_row[1]
        row_weekday_label = blfpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        coin_dict["timeline"]["weekdays_config"] = weekday_config_list


def _set_coin_dict_timeoffi(cursor: sqlite3_Cursor, coin_dict: dict):
    offi_times_set = set()
    for blfpayy_row in cursor.fetchall():
        row_coin_label = blfpayy_row[0]
        row_offi_time = blfpayy_row[1]
        offi_times_set.add(row_offi_time)
    coin_dict["offi_times"] = list(offi_times_set)
