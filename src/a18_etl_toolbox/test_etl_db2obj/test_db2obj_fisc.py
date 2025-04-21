from src.a02_finance_toolboxs.deal import fisc_title_str
from src.a15_fisc_logic.fisc import (
    fiscunit_shop,
    get_from_dict as fiscunit_get_from_dict,
)
from src.a15_fisc_logic.fisc_config import cashbook_str, brokerunits_str, timeline_str
from src.a18_etl_toolbox.tran_sqlstrs import create_fisc_tables
from src.a18_etl_toolbox.db_obj_tool import get_fisc_dict_from_db
from sqlite3 import connect as sqlite3_connect


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscunit_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    a23_timeline_title = "timeline88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_distortion = 9
    a23_fund_coin = 13
    a23_penny = 17
    a23_respect_bit = 23
    a23_bridge = "."

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = f"""INSERT INTO fiscunit_agg (
  fisc_title
, timeline_title
, c400_number
, yr1_jan1_offset
, monthday_distortion
, fund_coin
, penny
, respect_bit
, bridge
)
VALUES (
'{a23_str}'
, '{a23_timeline_title}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_distortion}
, {a23_fund_coin}
, {a23_penny}
, {a23_respect_bit}
, '{a23_bridge}'
)
;"""
        cursor.execute(fiscunit_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    assert a23_dict
    assert a23_dict.get("fisc_title") == a23_str
    print(f"{a23_dict=}")
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict.get("timeline_title") == a23_timeline_title
    assert a23_timeline_dict.get("c400_number") == a23_c400_number
    assert a23_timeline_dict.get("yr1_jan1_offset") == a23_yr1_jan1_offset
    assert a23_timeline_dict.get("monthday_distortion") == a23_monthday_distortion
    assert a23_dict.get("fund_coin") == a23_fund_coin
    assert a23_dict.get("penny") == a23_penny
    assert a23_dict.get("respect_bit") == a23_respect_bit
    assert a23_dict.get("bridge") == a23_bridge


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscunit_Attrs_Scenario1():
    # ESTABLISH
    a23_str = "accord23"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    assert a23_dict
    assert a23_dict.get("fisc_title") == a23_str
    assert "timeline" in set(a23_dict.keys())
    assert a23_dict.get("fund_coin") is None
    assert a23_dict.get("penny") is None
    assert a23_dict.get("respect_bit") is None
    assert a23_dict.get("bridge") is None
    assert set(a23_dict.keys()) == {
        fisc_title_str(),
        "offi_times",
        timeline_str(),
        cashbook_str(),
        brokerunits_str(),
    }


def test_get_fisc_dict_from_db_ReturnsObj_With_fisccash_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    tp55 = 55
    bob_sue_tp55_amount = 444
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_cashbook_agg (fisc_title, owner_name, acct_name, tran_time, amount) 
VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_cashbook_dict = a23_dict.get("cashbook")
    assert a23_cashbook_dict
    assert a23_cashbook_dict.get("fisc_title") == a23_str
    a23_tranunits_dict = a23_cashbook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict.get(tp55) == bob_sue_tp55_amount


def test_get_fisc_dict_from_db_ReturnsObj_With_fisccash_Attrs_Scenario1():
    # ESTABLISH
    a23_str = "accord23"
    a45_str = "accord45"
    bob_str = "Bob"
    sue_str = "Sue"
    tp55 = 55
    a23_bob_sue_tp55_amount = 444
    a45_bob_sue_tp55_amount = 800
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_cashbook_agg (fisc_title, owner_name, acct_name, tran_time, amount) 
VALUES 
  ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {a23_bob_sue_tp55_amount})
, ('{a45_str}', '{bob_str}', '{sue_str}', {tp55}, {a45_bob_sue_tp55_amount})
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_cashbook_dict = a23_dict.get("cashbook")
    assert a23_cashbook_dict
    assert a23_cashbook_dict.get("fisc_title") == a23_str
    a23_tranunits_dict = a23_cashbook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict == {tp55: a23_bob_sue_tp55_amount}


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscdeal_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_dealunit_agg (fisc_title, owner_name, deal_time, quota, celldepth) 
VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_brokerunit_dict = a23_dict.get("brokerunits")
    print(f"{a23_brokerunit_dict=}")
    assert a23_brokerunit_dict
    a23_brokerunit_bob_dict = a23_brokerunit_dict.get(bob_str)
    assert a23_brokerunit_bob_dict
    a23_bob_deals_dict = a23_brokerunit_bob_dict.get("deals")
    assert a23_bob_deals_dict
    a23_brokerunit_bob_tp55_dict = a23_bob_deals_dict.get(tp55)
    assert a23_brokerunit_bob_tp55_dict
    expected_a23_brokerunit_bob_tp55_dict = {
        "deal_time": 55,
        "quota": bob_tp55_quota,
        "celldepth": bob_tp55_celldepth,
    }
    assert a23_brokerunit_bob_tp55_dict == expected_a23_brokerunit_bob_tp55_dict


def test_get_fisc_dict_from_db_ReturnsObj_With_fischour_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    hour3_min = 300
    hour4_min = 400
    hour3_title = "3xm"
    hour4_title = "4xm"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_hour_agg (fisc_title, cumlative_minute, hour_title) 
VALUES 
  ('{a23_str}', {hour3_min}, '{hour3_title}')
, ('{a23_str}', {hour4_min}, '{hour4_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    print(f"{a23_timeline_dict=}")
    assert a23_timeline_dict
    a23_hours_config_dict = a23_timeline_dict.get("hours_config")
    print(f"{a23_hours_config_dict=}")
    assert a23_hours_config_dict == [[hour3_title, hour3_min], [hour4_title, hour4_min]]


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscmont_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    day111_min = 111
    day222_min = 222
    month111_title = "jan111"
    month222_title = "feb222"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_month_agg (fisc_title, cumlative_day, month_title) 
VALUES 
  ('{a23_str}', {day111_min}, '{month111_title}')
, ('{a23_str}', {day222_min}, '{month222_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict
    a23_months_config_dict = a23_timeline_dict.get("months_config")
    assert a23_months_config_dict == [
        [month111_title, day111_min],
        [month222_title, day222_min],
    ]


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscweek_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    ana_order = 1
    bee_order = 2
    ana_title = "ana_weekday"
    bee_title = "bee_weekday"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_weekday_agg (fisc_title, weekday_order, weekday_title) 
VALUES 
  ('{a23_str}', {ana_order}, '{ana_title}')
, ('{a23_str}', {bee_order}, '{bee_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict
    a23_weekdays_config_dict = a23_timeline_dict.get("weekdays_config")
    assert a23_weekdays_config_dict == [ana_title, bee_title]


def test_get_fisc_dict_from_db_ReturnsObj_With_fiscoffi_Attrs_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "accord23"
    offi_time5 = 5
    offi_time7 = 7
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeoffi_agg (fisc_title, offi_time) 
VALUES 
  ('{a23_str}', {offi_time5})
, ('{a23_str}', {offi_time7})
;
"""
        cursor.execute(fisccash_insert_sqlstr)

        # WHEN
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # THEN
    a23_offi_times_config_dict = a23_dict.get("offi_times")
    print(f"{a23_offi_times_config_dict=}")
    assert a23_offi_times_config_dict == [offi_time5, offi_time7]


def test_get_fisc_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario0_fiscunit():
    # ESTABLISH
    a23_str = "accord23"
    a23_timeline_title = "timeline88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_distortion = 9
    a23_fund_coin = 13
    a23_penny = 17
    a23_respect_bit = 23
    a23_bridge = "."

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = f"""INSERT INTO fiscunit_agg (
  fisc_title
, timeline_title
, c400_number
, yr1_jan1_offset
, monthday_distortion
, fund_coin
, penny
, respect_bit
, bridge
)
VALUES (
'{a23_str}'
, '{a23_timeline_title}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_distortion}
, {a23_fund_coin}
, {a23_penny}
, {a23_respect_bit}
, '{a23_bridge}'
)
;"""
        cursor.execute(fiscunit_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    assert a23_fiscunit.fisc_title == a23_str
    assert a23_fiscunit.timeline.timeline_title == a23_timeline_title
    assert a23_fiscunit.timeline.c400_number == a23_c400_number
    assert a23_fiscunit.timeline.yr1_jan1_offset == a23_yr1_jan1_offset
    assert a23_fiscunit.timeline.monthday_distortion == a23_monthday_distortion
    assert a23_fiscunit.fund_coin == a23_fund_coin
    assert a23_fiscunit.penny == a23_penny
    assert a23_fiscunit.respect_bit == a23_respect_bit
    assert a23_fiscunit.bridge == a23_bridge


def test_get_fisc_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario1_fisccash():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    tp55 = 55
    bob_sue_tp55_amount = 444
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_cashbook_agg (fisc_title, owner_name, acct_name, tran_time, amount) 
VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    assert a23_fiscunit.fisc_title == a23_str
    assert a23_fiscunit.cashbook.tranunits.get(bob_str)
    bob_tranunit = a23_fiscunit.cashbook.tranunits.get(bob_str)
    assert bob_tranunit == {sue_str: {tp55: bob_sue_tp55_amount}}


def test_get_fisc_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario2_fiscdeal():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_dealunit_agg (fisc_title, owner_name, deal_time, quota, celldepth)
VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    a23_bob_brokerunit = a23_fiscunit.get_brokerunit(bob_str)
    print(f"{a23_bob_brokerunit=}")
    assert a23_bob_brokerunit
    a23_bob_55_deal = a23_bob_brokerunit.get_deal(tp55)
    assert a23_bob_55_deal.deal_time == tp55
    assert a23_bob_55_deal.quota == bob_tp55_quota
    assert a23_bob_55_deal.celldepth == bob_tp55_celldepth


def test_get_fisc_dict_from_db_ReturnsObj_With_fischour_Attrs_Scenario3_fischour():
    # ESTABLISH
    a23_str = "accord23"
    hour3_min = 300
    hour4_min = 400
    hour3_title = "3xm"
    hour4_title = "4xm"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_hour_agg (fisc_title, cumlative_minute, hour_title)
VALUES
  ('{a23_str}', {hour3_min}, '{hour3_title}')
, ('{a23_str}', {hour4_min}, '{hour4_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    a23_fiscunit.timeline.hours_config == [
        [hour3_title, hour3_min],
        [hour4_title, hour4_min],
    ]


def test_get_fisc_dict_from_db_ReturnsObj_With_fischour_Attrs_Scenario4_fiscmont():
    # ESTABLISH
    a23_str = "accord23"
    day111_min = 111
    day222_min = 222
    month111_title = "jan111"
    month222_title = "feb222"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_month_agg (fisc_title, cumlative_day, month_title)
VALUES
  ('{a23_str}', {day111_min}, '{month111_title}')
, ('{a23_str}', {day222_min}, '{month222_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    assert a23_fiscunit.timeline.months_config == [
        [month111_title, day111_min],
        [month222_title, day222_min],
    ]


def test_get_fisc_dict_from_db_ReturnsObj_With_fischour_Attrs_Scenario5_fiscweek():
    # ESTABLISH
    a23_str = "accord23"
    ana_order = 1
    bee_order = 2
    ana_title = "ana_weekday"
    bee_title = "bee_weekday"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeline_weekday_agg (fisc_title, weekday_order, weekday_title)
VALUES
  ('{a23_str}', {ana_order}, '{ana_title}')
, ('{a23_str}', {bee_order}, '{bee_title}')
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    assert a23_fiscunit.timeline.weekdays_config == [ana_title, bee_title]


def test_get_fisc_dict_from_db_ReturnsObj_With_fischour_Attrs_Scenario5_fiscweek():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "accord23"
    offi_time5 = 5
    offi_time7 = 7
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        fiscunit_insert_sqlstr = (
            f"INSERT INTO fiscunit_agg (fisc_title) VALUES ('{a23_str}');"
        )
        cursor.execute(fiscunit_insert_sqlstr)
        fisccash_insert_sqlstr = f"""INSERT INTO fisc_timeoffi_agg (fisc_title, offi_time)
VALUES
  ('{a23_str}', {offi_time5})
, ('{a23_str}', {offi_time7})
;
"""
        cursor.execute(fisccash_insert_sqlstr)
        a23_dict = get_fisc_dict_from_db(cursor, a23_str)

    # WHEN
    a23_fiscunit = fiscunit_get_from_dict(a23_dict)

    # THEN
    a23_fiscunit.offi_times == {offi_time5, offi_time7}
