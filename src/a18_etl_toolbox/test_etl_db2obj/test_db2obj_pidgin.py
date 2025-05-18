# from src.a16_pidgin_logic.pidgin import get_pidginunit_from_dict
# from src.a16_pidgin_logic._utils.str_a16 import (
#     pidgin_title_str,
#     pidgin_name_str,
#     pidgin_way_str,
#     pidgin_label_str,
#     pidgin_core_str,
# )
# from src.a18_etl_toolbox.tran_sqlstrs import (
#     create_sound_and_voice_tables,
#     create_prime_tablename,
# )
# from src.a18_etl_toolbox.db_obj_tool import get_pidgin_dict_from_db
# from sqlite3 import connect as sqlite3_connect

# # dictionary data structure to follow per even
# # {
# #     "face_name": "Sue",
# #     "event_int": 0,
# #     "otx_bridge": ";",
# #     "inx_bridge": ";",
# #     "unknown_term": "UNKNOWN",
# #     "namemap": {
# #         "otx2inx": {},
# #     },
# #     "labelmap": {
# #         "otx2inx": {},
# #     },
# #     "titlemap": {
# #         "otx2inx": {},
# #     },
# #     "waymap": {
# #         "otx2inx": {},
# #     },
# # }


# def test_get_pidgin_dict_from_db_ReturnsObj_With_pidginunit_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     a23_timeline_label = "timeline88"
#     a23_c400_number = 3
#     a23_yr1_jan1_offset = 7
#     a23_monthday_distortion = 9
#     a23_fund_coin = 13
#     a23_penny = 17
#     a23_respect_bit = 23
#     a23_bridge = "."

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = f"""INSERT INTO pidginunit_agg (
#   pidgin_label
# , timeline_label
# , c400_number
# , yr1_jan1_offset
# , monthday_distortion
# , fund_coin
# , penny
# , respect_bit
# , bridge
# )
# VALUES (
# '{a23_str}'
# , '{a23_timeline_label}'
# , {a23_c400_number}
# , {a23_yr1_jan1_offset}
# , {a23_monthday_distortion}
# , {a23_fund_coin}
# , {a23_penny}
# , {a23_respect_bit}
# , '{a23_bridge}'
# )
# ;"""
#         cursor.execute(pidginunit_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     assert a23_dict
#     assert a23_dict.get("pidgin_label") == a23_str
#     print(f"{a23_dict=}")
#     a23_timeline_dict = a23_dict.get("timeline")
#     assert a23_timeline_dict.get("timeline_label") == a23_timeline_label
#     assert a23_timeline_dict.get("c400_number") == a23_c400_number
#     assert a23_timeline_dict.get("yr1_jan1_offset") == a23_yr1_jan1_offset
#     assert a23_timeline_dict.get("monthday_distortion") == a23_monthday_distortion
#     assert a23_dict.get("fund_coin") == a23_fund_coin
#     assert a23_dict.get("penny") == a23_penny
#     assert a23_dict.get("respect_bit") == a23_respect_bit
#     assert a23_dict.get("bridge") == a23_bridge


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fisunit_Attrs_Scenario1():
#     # ESTABLISH
#     a23_str = "accord23"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     assert a23_dict
#     assert a23_dict.get("pidgin_label") == a23_str
#     assert "timeline" in set(a23_dict.keys())
#     assert a23_dict.get("fund_coin") is None
#     assert a23_dict.get("penny") is None
#     assert a23_dict.get("respect_bit") is None
#     assert a23_dict.get("bridge") is None
#     assert set(a23_dict.keys()) == {
#         pidgin_label_str(),
#         "offi_times",
#         timeline_str(),
#         cashbook_str(),
#         brokerunits_str(),
#     }


# def test_get_pidgin_dict_from_db_ReturnsObj_With_pidginash_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     tp55 = 55
#     bob_sue_tp55_amount = 444
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_cashbook_agg (pidgin_label, owner_name, acct_name, tran_time, amount)
# VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_cashbook_dict = a23_dict.get("cashbook")
#     assert a23_cashbook_dict
#     assert a23_cashbook_dict.get("pidgin_label") == a23_str
#     a23_tranunits_dict = a23_cashbook_dict.get("tranunits")
#     assert a23_tranunits_dict
#     a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
#     assert a23_trans_bob_dict
#     a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
#     assert a23_trans_bob_sue_dict
#     assert a23_trans_bob_sue_dict.get(tp55) == bob_sue_tp55_amount


# def test_get_pidgin_dict_from_db_ReturnsObj_With_pidginash_Attrs_Scenario1():
#     # ESTABLISH
#     a23_str = "accord23"
#     a45_str = "accord45"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     tp55 = 55
#     a23_bob_sue_tp55_amount = 444
#     a45_bob_sue_tp55_amount = 800
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_cashbook_agg (pidgin_label, owner_name, acct_name, tran_time, amount)
# VALUES
#   ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {a23_bob_sue_tp55_amount})
# , ('{a45_str}', '{bob_str}', '{sue_str}', {tp55}, {a45_bob_sue_tp55_amount})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_cashbook_dict = a23_dict.get("cashbook")
#     assert a23_cashbook_dict
#     assert a23_cashbook_dict.get("pidgin_label") == a23_str
#     a23_tranunits_dict = a23_cashbook_dict.get("tranunits")
#     assert a23_tranunits_dict
#     a23_trans_bob_dict = a23_tranunits_dict.get(bob_str)
#     assert a23_trans_bob_dict
#     a23_trans_bob_sue_dict = a23_trans_bob_dict.get(sue_str)
#     assert a23_trans_bob_sue_dict
#     assert a23_trans_bob_sue_dict == {tp55: a23_bob_sue_tp55_amount}


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fisdeal_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     tp55 = 55
#     bob_tp55_quota = 444
#     bob_tp55_celldepth = 3
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_dealunit_agg (pidgin_label, owner_name, deal_time, quota, celldepth)
# VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_brokerunit_dict = a23_dict.get("brokerunits")
#     print(f"{a23_brokerunit_dict=}")
#     assert a23_brokerunit_dict
#     a23_brokerunit_bob_dict = a23_brokerunit_dict.get(bob_str)
#     assert a23_brokerunit_bob_dict
#     a23_bob_deals_dict = a23_brokerunit_bob_dict.get("deals")
#     assert a23_bob_deals_dict
#     a23_brokerunit_bob_tp55_dict = a23_bob_deals_dict.get(tp55)
#     assert a23_brokerunit_bob_tp55_dict
#     expected_a23_brokerunit_bob_tp55_dict = {
#         "deal_time": 55,
#         "quota": bob_tp55_quota,
#         "celldepth": bob_tp55_celldepth,
#     }
#     assert a23_brokerunit_bob_tp55_dict == expected_a23_brokerunit_bob_tp55_dict


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fishour_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     hour3_min = 300
#     hour4_min = 400
#     hour3_label = "3xm"
#     hour4_label = "4xm"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_hour_agg (pidgin_label, cumlative_minute, hour_label)
# VALUES
#   ('{a23_str}', {hour3_min}, '{hour3_label}')
# , ('{a23_str}', {hour4_min}, '{hour4_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_timeline_dict = a23_dict.get("timeline")
#     print(f"{a23_timeline_dict=}")
#     assert a23_timeline_dict
#     a23_hours_config_dict = a23_timeline_dict.get("hours_config")
#     print(f"{a23_hours_config_dict=}")
#     assert a23_hours_config_dict == [[hour3_label, hour3_min], [hour4_label, hour4_min]]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fismont_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     day111_min = 111
#     day222_min = 222
#     month111_label = "jan111"
#     month222_label = "feb222"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_month_agg (pidgin_label, cumlative_day, month_label)
# VALUES
#   ('{a23_str}', {day111_min}, '{month111_label}')
# , ('{a23_str}', {day222_min}, '{month222_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_timeline_dict = a23_dict.get("timeline")
#     assert a23_timeline_dict
#     a23_months_config_dict = a23_timeline_dict.get("months_config")
#     assert a23_months_config_dict == [
#         [month111_label, day111_min],
#         [month222_label, day222_min],
#     ]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fisweek_Attrs_Scenario0():
#     # ESTABLISH
#     a23_str = "accord23"
#     ana_order = 1
#     bee_order = 2
#     ana_label = "ana_weekday"
#     bee_label = "bee_weekday"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_weekday_agg (pidgin_label, weekday_order, weekday_label)
# VALUES
#   ('{a23_str}', {ana_order}, '{ana_label}')
# , ('{a23_str}', {bee_order}, '{bee_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_timeline_dict = a23_dict.get("timeline")
#     assert a23_timeline_dict
#     a23_weekdays_config_dict = a23_timeline_dict.get("weekdays_config")
#     assert a23_weekdays_config_dict == [ana_label, bee_label]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fisoffi_Attrs_Scenario0():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     a23_str = "accord23"
#     offi_time5 = 5
#     offi_time7 = 7
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeoffi_agg (pidgin_label, offi_time)
# VALUES
#   ('{a23_str}', {offi_time5})
# , ('{a23_str}', {offi_time7})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)

#         # WHEN
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # THEN
#     a23_offi_times_config_dict = a23_dict.get("offi_times")
#     print(f"{a23_offi_times_config_dict=}")
#     assert a23_offi_times_config_dict == [offi_time5, offi_time7]


# def test_get_pidgin_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario0_pidginunit():
#     # ESTABLISH
#     a23_str = "accord23"
#     a23_timeline_label = "timeline88"
#     a23_c400_number = 3
#     a23_yr1_jan1_offset = 7
#     a23_monthday_distortion = 9
#     a23_fund_coin = 13
#     a23_penny = 17
#     a23_respect_bit = 23
#     a23_bridge = "."

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = f"""INSERT INTO pidginunit_agg (
#   pidgin_label
# , timeline_label
# , c400_number
# , yr1_jan1_offset
# , monthday_distortion
# , fund_coin
# , penny
# , respect_bit
# , bridge
# )
# VALUES (
# '{a23_str}'
# , '{a23_timeline_label}'
# , {a23_c400_number}
# , {a23_yr1_jan1_offset}
# , {a23_monthday_distortion}
# , {a23_fund_coin}
# , {a23_penny}
# , {a23_respect_bit}
# , '{a23_bridge}'
# )
# ;"""
#         cursor.execute(pidginunit_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     assert a23_pidginunit.pidgin_label == a23_str
#     assert a23_pidginunit.timeline.timeline_label == a23_timeline_label
#     assert a23_pidginunit.timeline.c400_number == a23_c400_number
#     assert a23_pidginunit.timeline.yr1_jan1_offset == a23_yr1_jan1_offset
#     assert a23_pidginunit.timeline.monthday_distortion == a23_monthday_distortion
#     assert a23_pidginunit.fund_coin == a23_fund_coin
#     assert a23_pidginunit.penny == a23_penny
#     assert a23_pidginunit.respect_bit == a23_respect_bit
#     assert a23_pidginunit.bridge == a23_bridge


# def test_get_pidgin_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario1_pidginash():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     sue_str = "Sue"
#     tp55 = 55
#     bob_sue_tp55_amount = 444
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_cashbook_agg (pidgin_label, owner_name, acct_name, tran_time, amount)
# VALUES ('{a23_str}', '{bob_str}', '{sue_str}', {tp55}, {bob_sue_tp55_amount})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     assert a23_pidginunit.pidgin_label == a23_str
#     assert a23_pidginunit.cashbook.tranunits.get(bob_str)
#     bob_tranunit = a23_pidginunit.cashbook.tranunits.get(bob_str)
#     assert bob_tranunit == {sue_str: {tp55: bob_sue_tp55_amount}}


# def test_get_pidgin_dict_from_db_ReturnsObj_IsCorrectlyFormatted_Scenario2_fisdeal():
#     # ESTABLISH
#     a23_str = "accord23"
#     bob_str = "Bob"
#     tp55 = 55
#     bob_tp55_quota = 444
#     bob_tp55_celldepth = 3
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_dealunit_agg (pidgin_label, owner_name, deal_time, quota, celldepth)
# VALUES ('{a23_str}', '{bob_str}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     a23_bob_brokerunit = a23_pidginunit.get_brokerunit(bob_str)
#     print(f"{a23_bob_brokerunit=}")
#     assert a23_bob_brokerunit
#     a23_bob_55_deal = a23_bob_brokerunit.get_deal(tp55)
#     assert a23_bob_55_deal.deal_time == tp55
#     assert a23_bob_55_deal.quota == bob_tp55_quota
#     assert a23_bob_55_deal.celldepth == bob_tp55_celldepth


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fishour_Attrs_Scenario3_fishour():
#     # ESTABLISH
#     a23_str = "accord23"
#     hour3_min = 300
#     hour4_min = 400
#     hour3_label = "3xm"
#     hour4_label = "4xm"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_hour_agg (pidgin_label, cumlative_minute, hour_label)
# VALUES
#   ('{a23_str}', {hour3_min}, '{hour3_label}')
# , ('{a23_str}', {hour4_min}, '{hour4_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     a23_pidginunit.timeline.hours_config == [
#         [hour3_label, hour3_min],
#         [hour4_label, hour4_min],
#     ]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fishour_Attrs_Scenario4_fismont():
#     # ESTABLISH
#     a23_str = "accord23"
#     day111_min = 111
#     day222_min = 222
#     month111_label = "jan111"
#     month222_label = "feb222"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_month_agg (pidgin_label, cumlative_day, month_label)
# VALUES
#   ('{a23_str}', {day111_min}, '{month111_label}')
# , ('{a23_str}', {day222_min}, '{month222_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     assert a23_pidginunit.timeline.months_config == [
#         [month111_label, day111_min],
#         [month222_label, day222_min],
#     ]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fishour_Attrs_Scenario5_fisweek():
#     # ESTABLISH
#     a23_str = "accord23"
#     ana_order = 1
#     bee_order = 2
#     ana_label = "ana_weekday"
#     bee_label = "bee_weekday"
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeline_weekday_agg (pidgin_label, weekday_order, weekday_label)
# VALUES
#   ('{a23_str}', {ana_order}, '{ana_label}')
# , ('{a23_str}', {bee_order}, '{bee_label}')
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     assert a23_pidginunit.timeline.weekdays_config == [ana_label, bee_label]


# def test_get_pidgin_dict_from_db_ReturnsObj_With_fishour_Attrs_Scenario5_fisweek():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     a23_str = "accord23"
#     offi_time5 = 5
#     offi_time7 = 7
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidginunit_insert_sqlstr = (
#             f"INSERT INTO pidginunit_agg (pidgin_label) VALUES ('{a23_str}');"
#         )
#         cursor.execute(pidginunit_insert_sqlstr)
#         pidginash_insert_sqlstr = f"""INSERT INTO pidgin_timeoffi_agg (pidgin_label, offi_time)
# VALUES
#   ('{a23_str}', {offi_time5})
# , ('{a23_str}', {offi_time7})
# ;
# """
#         cursor.execute(pidginash_insert_sqlstr)
#         a23_dict = get_pidgin_dict_from_db(cursor, a23_str)

#     # WHEN
#     a23_pidginunit = pidginunit_get_from_dict(a23_dict)

#     # THEN
#     a23_pidginunit.offi_times == {offi_time5, offi_time7}
