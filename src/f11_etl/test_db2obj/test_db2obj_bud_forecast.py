from src.f00_instrument.db_toolbox import get_row_count
from src.f01_road.deal import fisc_title_str
from src.f02_bud.bud import budunit_shop
from src.f08_fisc.fisc import fiscunit_shop, get_from_dict as fiscunit_get_from_dict
from src.f08_fisc.fisc_config import cashbook_str, brokerunits_str, timeline_str
from src.f11_etl.tran_sqlstrs import create_forecast_tables
from src.f11_etl.db_obj_tool import get_fisc_dict_from_db, insert_forecast_obj
from sqlite3 import connect as sqlite3_connect

# create tests to convert settled budunit to database
# create budunit object
# check that row does not exist in database
# insert obj
# check that row does exist in database
# select row
# prove selected row = obj __dict__


# def test_insert_forecast_obj_CreatesTableRowsFor_budunit_forecast():
#     # ESTABLISH
#     sue_str = "Sue"
#     iowa_fisc_title = "Iowa"
#     slash_bridge = "/"
#     x_fund_pool = 777
#     x_fund_coin = 7
#     x_respect_bit = 5
#     x_penny = 1
#     x_tally = 55
#     sue_bud = budunit_shop(
#         owner_name=sue_str,
#         fisc_title=iowa_fisc_title,
#         bridge=slash_bridge,
#         fund_pool=x_fund_pool,
#         fund_coin=x_fund_coin,
#         respect_bit=x_respect_bit,
#         penny=x_penny,
#         tally=x_tally,
#     )
#     sue_bud.settle_bud()

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_forecast_tables(cursor)
#         x_table_name = "budunit_forecast"
#         assert get_row_count(cursor, x_table_name) == 0

#         # WHEN
#         insert_forecast_obj(cursor, sue_bud)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_data = [(1, "John Doe", 30, "john@example.com")]
#         assert rows == expected_data

#     assert 1 == 2


# "budunit_forecast"
# "bud_acct_membership_forecast"
# "bud_acctunit_forecast"
# "bud_groupunit_forecast"
# "bud_item_awardlink_forecast"
# "bud_item_factunit_forecast"
# "bud_item_healerlink_forecast"
# "bud_item_reason_premiseunit_forecast"
# "bud_item_reasonunit_forecast"
# "bud_item_teamlink_forecast"
# "bud_itemunit_forecast"
