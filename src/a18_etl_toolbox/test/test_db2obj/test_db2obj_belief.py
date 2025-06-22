from sqlite3 import connect as sqlite3_connect
from src.a02_finance_logic.test._util.a02_str import belief_label_str
from src.a15_belief_logic.belief import get_from_dict as beliefunit_get_from_dict
from src.a15_belief_logic.test._util.a15_str import (
    brokerunits_str,
    paybook_str,
    timeline_str,
)
from src.a18_etl_toolbox.db_obj_belief_tool import get_belief_dict_from_voice_tables
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
)


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_beliefunit_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    a23_timeline_label = "timeline88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_distortion = 9
    a23_fund_iota = 13
    a23_penny = 17
    a23_respect_bit = 23
    a23_knot = "."

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefunit_insert_sqlstr = f"""INSERT INTO {beliefunit_v_agg_tablename} (
  belief_label
, timeline_label
, c400_number
, yr1_jan1_offset
, monthday_distortion
, fund_iota
, penny
, respect_bit
, knot
)
VALUES (
  '{a23_str}'
, '{a23_timeline_label}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_distortion}
, {a23_fund_iota}
, {a23_penny}
, {a23_respect_bit}
, '{a23_knot}'
)
;"""
        cursor.execute(beliefunit_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    assert a23_dict
    assert a23_dict.get("belief_label") == a23_str
    print(f"{a23_dict=}")
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict.get("timeline_label") == a23_timeline_label
    assert a23_timeline_dict.get("c400_number") == a23_c400_number
    assert a23_timeline_dict.get("yr1_jan1_offset") == a23_yr1_jan1_offset
    assert a23_timeline_dict.get("monthday_distortion") == a23_monthday_distortion
    assert a23_dict.get("fund_iota") == a23_fund_iota
    assert a23_dict.get("penny") == a23_penny
    assert a23_dict.get("respect_bit") == a23_respect_bit
    assert a23_dict.get("knot") == a23_knot


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_beliefunit_Attrs_Scenario1():
    # sourcery skip: extract-method, inline-immediately-returned-variable
    # ESTABLISH
    a23_str = "accord23"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    assert a23_dict
    assert a23_dict.get("belief_label") == a23_str
    assert "timeline" in set(a23_dict.keys())
    assert a23_dict.get("fund_iota") is None
    assert a23_dict.get("penny") is None
    assert a23_dict.get("respect_bit") is None
    assert a23_dict.get("knot") is None
    assert set(a23_dict.keys()) == {
        belief_label_str(),
        "offi_times",
        timeline_str(),
        paybook_str(),
        brokerunits_str(),
    }


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfpayy_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    tp55 = 55
    bob_sue_tp55_amount = 444
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefpay_v_agg_tablename = create_prime_tablename("blfpayy", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {beliefpay_v_agg_tablename} (belief_label, owner_name, acct_name, tran_time, amount)
VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_paybook_dict = a23_dict.get("paybook")
    assert a23_paybook_dict
    assert a23_paybook_dict.get("belief_label") == a23_str
    a23_tranunits_dict = a23_paybook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict.get(tp55) == bob_sue_tp55_amount


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfpayy_Attrs_Scenario1():
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
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefpay_v_agg_tablename = create_prime_tablename("blfpayy", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {beliefpay_v_agg_tablename} (belief_label, owner_name, acct_name, tran_time, amount)
VALUES
  ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {a23_bob_sue_tp55_amount})
, ('{a45_str}', '{bob_str}', '{sue_str}', {tp55}, {a45_bob_sue_tp55_amount})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_paybook_dict = a23_dict.get("paybook")
    assert a23_paybook_dict
    assert a23_paybook_dict.get("belief_label") == a23_str
    a23_tranunits_dict = a23_paybook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict == {tp55: a23_bob_sue_tp55_amount}


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_beliefbud_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefbud_v_agg_tablename = create_prime_tablename("blfbudd", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {beliefbud_v_agg_tablename} (belief_label, owner_name, bud_time, quota, celldepth)
VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_brokerunit_dict = a23_dict.get("brokerunits")
    print(f"{a23_brokerunit_dict=}")
    assert a23_brokerunit_dict
    a23_brokerunit_bob_dict = a23_brokerunit_dict.get(bob_str)
    assert a23_brokerunit_bob_dict
    a23_bob_buds_dict = a23_brokerunit_bob_dict.get("buds")
    assert a23_bob_buds_dict
    a23_brokerunit_bob_tp55_dict = a23_bob_buds_dict.get(tp55)
    assert a23_brokerunit_bob_tp55_dict
    expected_a23_brokerunit_bob_tp55_dict = {
        "bud_time": 55,
        "quota": bob_tp55_quota,
        "celldepth": bob_tp55_celldepth,
    }
    assert a23_brokerunit_bob_tp55_dict == expected_a23_brokerunit_bob_tp55_dict


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfhour_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    hour3_min = 300
    hour4_min = 400
    hour3_label = "3xm"
    hour4_label = "4xm"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfhour_v_agg_tablename = create_prime_tablename("blfhour", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfhour_v_agg_tablename} (belief_label, cumulative_minute, hour_label)
VALUES
  ('{a23_str}', {hour3_min}, '{hour3_label}')
, ('{a23_str}', {hour4_min}, '{hour4_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    print(f"{a23_timeline_dict=}")
    assert a23_timeline_dict
    a23_hours_config_dict = a23_timeline_dict.get("hours_config")
    print(f"{a23_hours_config_dict=}")
    assert a23_hours_config_dict == [[hour3_label, hour3_min], [hour4_label, hour4_min]]


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfmont_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    day111_min = 111
    day222_min = 222
    month111_label = "jan111"
    month222_label = "feb222"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfmont_v_agg_tablename = create_prime_tablename("blfmont", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfmont_v_agg_tablename} (belief_label, cumulative_day, month_label)
VALUES
  ('{a23_str}', {day111_min}, '{month111_label}')
, ('{a23_str}', {day222_min}, '{month222_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict
    a23_months_config_dict = a23_timeline_dict.get("months_config")
    assert a23_months_config_dict == [
        [month111_label, day111_min],
        [month222_label, day222_min],
    ]


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfweek_Attrs_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    ana_order = 1
    bee_order = 2
    ana_label = "ana_weekday"
    bee_label = "bee_weekday"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfweek_v_agg_tablename = create_prime_tablename("blfweek", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfweek_v_agg_tablename} (belief_label, weekday_order, weekday_label)
VALUES
  ('{a23_str}', {ana_order}, '{ana_label}')
, ('{a23_str}', {bee_order}, '{bee_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_timeline_dict = a23_dict.get("timeline")
    assert a23_timeline_dict
    a23_weekdays_config_dict = a23_timeline_dict.get("weekdays_config")
    assert a23_weekdays_config_dict == [ana_label, bee_label]


def test_get_belief_dict_from_voice_tables_ReturnsObj_With_blfoffi_Attrs_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "accord23"
    offi_time5 = 5
    offi_time7 = 7
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfoffi_v_agg_tablename = create_prime_tablename("blfoffi", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfoffi_v_agg_tablename} (belief_label, offi_time)
VALUES
  ('{a23_str}', {offi_time5})
, ('{a23_str}', {offi_time7})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)

        # WHEN
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # THEN
    a23_offi_times_config_dict = a23_dict.get("offi_times")
    print(f"{a23_offi_times_config_dict=}")
    assert a23_offi_times_config_dict == [offi_time5, offi_time7]


def test_get_belief_dict_from_voice_tables_ReturnsObj_IsCorrectlyFormatted_Scenario0_beliefunit():
    # ESTABLISH
    a23_str = "accord23"
    a23_timeline_label = "timeline88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_distortion = 9
    a23_fund_iota = 13
    a23_penny = 17
    a23_respect_bit = 23
    a23_knot = "."

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefunit_insert_sqlstr = f"""INSERT INTO {beliefunit_v_agg_tablename} (
  belief_label
, timeline_label
, c400_number
, yr1_jan1_offset
, monthday_distortion
, fund_iota
, penny
, respect_bit
, knot
)
VALUES (
  '{a23_str}'
, '{a23_timeline_label}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_distortion}
, {a23_fund_iota}
, {a23_penny}
, {a23_respect_bit}
, '{a23_knot}'
)
;"""
        cursor.execute(beliefunit_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    assert a23_beliefunit.belief_label == a23_str
    assert a23_beliefunit.timeline.timeline_label == a23_timeline_label
    assert a23_beliefunit.timeline.c400_number == a23_c400_number
    assert a23_beliefunit.timeline.yr1_jan1_offset == a23_yr1_jan1_offset
    assert a23_beliefunit.timeline.monthday_distortion == a23_monthday_distortion
    assert a23_beliefunit.fund_iota == a23_fund_iota
    assert a23_beliefunit.penny == a23_penny
    assert a23_beliefunit.respect_bit == a23_respect_bit
    assert a23_beliefunit.knot == a23_knot


def test_get_belief_dict_from_voice_tables_ReturnsObj_IsCorrectlyFormatted_Scenario1_blfpayy():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    tp55 = 55
    bob_sue_tp55_amount = 444
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefpay_v_agg_tablename = create_prime_tablename("blfpayy", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {beliefpay_v_agg_tablename} (belief_label, owner_name, acct_name, tran_time, amount)
VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    assert a23_beliefunit.belief_label == a23_str
    assert a23_beliefunit.paybook.tranunits.get(bob_str)
    bob_tranunit = a23_beliefunit.paybook.tranunits.get(bob_str)
    assert bob_tranunit == {sue_str: {tp55: bob_sue_tp55_amount}}


def test_get_belief_dict_from_voice_tables_ReturnsObj_IsCorrectlyFormatted_Scenario2_beliefbud():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        beliefbud_v_agg_tablename = create_prime_tablename("blfbudd", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {beliefbud_v_agg_tablename} (belief_label, owner_name, bud_time, quota, celldepth)
VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    a23_bob_brokerunit = a23_beliefunit.get_brokerunit(bob_str)
    print(f"{a23_bob_brokerunit=}")
    assert a23_bob_brokerunit
    a23_bob_55_bud = a23_bob_brokerunit.get_bud(tp55)
    assert a23_bob_55_bud.bud_time == tp55
    assert a23_bob_55_bud.quota == bob_tp55_quota
    assert a23_bob_55_bud.celldepth == bob_tp55_celldepth


def test_get_belief_dict_from_voice_tables_ReturnsObj_Scenario3_blfhour():
    # ESTABLISH
    a23_str = "accord23"
    hour3_min = 300
    hour4_min = 400
    hour3_label = "3xm"
    hour4_label = "4xm"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfhour_v_agg_tablename = create_prime_tablename("blfhour", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfhour_v_agg_tablename} (belief_label, cumulative_minute, hour_label)
VALUES
  ('{a23_str}', {hour3_min}, '{hour3_label}')
, ('{a23_str}', {hour4_min}, '{hour4_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    a23_beliefunit.timeline.hours_config == [
        [hour3_label, hour3_min],
        [hour4_label, hour4_min],
    ]


def test_get_belief_dict_from_voice_tables_ReturnsObj_Scenario4_blfmont():
    # ESTABLISH
    a23_str = "accord23"
    day111_min = 111
    day222_min = 222
    month111_label = "jan111"
    month222_label = "feb222"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfmont_v_agg_tablename = create_prime_tablename("blfmont", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfmont_v_agg_tablename} (belief_label, cumulative_day, month_label)
VALUES
  ('{a23_str}', {day111_min}, '{month111_label}')
, ('{a23_str}', {day222_min}, '{month222_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    assert a23_beliefunit.timeline.months_config == [
        [month111_label, day111_min],
        [month222_label, day222_min],
    ]


def test_get_belief_dict_from_voice_tables_ReturnsObj_Scenario5_blfweek():
    # ESTABLISH
    a23_str = "accord23"
    ana_order = 1
    bee_order = 2
    ana_label = "ana_weekday"
    bee_label = "bee_weekday"
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfweek_v_agg_tablename = create_prime_tablename("blfweek", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfweek_v_agg_tablename} (belief_label, weekday_order, weekday_label)
VALUES
  ('{a23_str}', {ana_order}, '{ana_label}')
, ('{a23_str}', {bee_order}, '{bee_label}')
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    assert a23_beliefunit.timeline.weekdays_config == [ana_label, bee_label]


def test_get_belief_dict_from_voice_tables_ReturnsObj_Scenario5_blfoffi():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "accord23"
    offi_time5 = 5
    offi_time7 = 7
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)
        beliefunit_v_agg_tablename = create_prime_tablename("beliefunit", "v", "agg")
        blfoffi_v_agg_tablename = create_prime_tablename("blfoffi", "v", "agg")
        beliefunit_insert_sqlstr = f"INSERT INTO {beliefunit_v_agg_tablename} (belief_label) VALUES ('{a23_str}');"
        cursor.execute(beliefunit_insert_sqlstr)
        blfpayy_insert_sqlstr = f"""INSERT INTO {blfoffi_v_agg_tablename} (belief_label, offi_time)
VALUES
  ('{a23_str}', {offi_time5})
, ('{a23_str}', {offi_time7})
;
"""
        cursor.execute(blfpayy_insert_sqlstr)
        a23_dict = get_belief_dict_from_voice_tables(cursor, a23_str)

    # WHEN
    a23_beliefunit = beliefunit_get_from_dict(a23_dict)

    # THEN
    assert a23_beliefunit.offi_times == {offi_time5, offi_time7}
